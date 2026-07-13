#!/usr/bin/env bash
#
# TarlaAnaliz Contracts Sync Tool
# Syncs contracts to consumer repositories (platform, edge, worker)
# Validates hash integrity after sync
#
# Usage:
#   ./tools/sync_to_repos.sh --target platform
#   ./tools/sync_to_repos.sh --target edge --verify-only
#   ./tools/sync_to_repos.sh --all
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTRACTS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Logging
log_info() { echo -e "${BLUE}ℹ${NC} $1"; }
log_success() { echo -e "${GREEN}✓${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }
log_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

# LF-normalized SHA-256 (CRLF/CR -> LF), matching the worker's
# scripts/compute_contracts_hash.py so Windows/Linux checkouts compare equal.
_lf_sha256() {
    local py
    py="$(command -v python3 || command -v python)"
    "$py" - "$1" <<'PY'
import sys, hashlib
b = open(sys.argv[1], "rb").read().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
print(hashlib.sha256(b).hexdigest())
PY
}

# Read expected checksum from CONTRACTS_VERSION.md
get_expected_checksum() {
    local version_file="$CONTRACTS_DIR/CONTRACTS_VERSION.md"
    
    if [ ! -f "$version_file" ]; then
        log_error "CONTRACTS_VERSION.md not found"
        return 1
    fi
    
    # Extract checksum
    local checksum=$(grep -oP 'Contracts Checksum \(SHA-256\):\*\* `\K[a-f0-9]{64}' "$version_file")
    
    if [ -z "$checksum" ]; then
        log_error "Could not parse checksum from CONTRACTS_VERSION.md"
        return 1
    fi
    
    echo "$checksum"
}

# Compute actual checksum
compute_actual_checksum() {
    local temp_file=$(mktemp)
    
    # Collect all schema file hashes
    find "$CONTRACTS_DIR/schemas" -name "*.json" -type f -print0 | \
        sort -z | \
        while IFS= read -r -d '' file; do
            local rel_path="${file#$CONTRACTS_DIR/}"
            local hash=$(sha256sum "$file" | awk '{print $1}')
            echo "$rel_path:$hash" >> "$temp_file"
        done
    
    # Collect API file hashes
    find "$CONTRACTS_DIR/api" -name "*.yaml" -type f -print0 | \
        sort -z | \
        while IFS= read -r -d '' file; do
            local rel_path="${file#$CONTRACTS_DIR/}"
            local hash=$(sha256sum "$file" | awk '{print $1}')
            echo "$rel_path:$hash" >> "$temp_file"
        done
    
    # Compute combined hash
    local combined_hash=$(sha256sum "$temp_file" | awk '{print $1}')
    rm -f "$temp_file"
    
    echo "$combined_hash"
}

# Verify checksums
verify_checksums() {
    log_info "Verifying contracts checksums..."
    
    local expected=$(get_expected_checksum)
    local actual=$(compute_actual_checksum)
    
    if [ "$expected" == "$actual" ]; then
        log_success "Checksums match: $actual"
        return 0
    else
        log_error "Checksum mismatch!"
        log_error "  Expected: $expected"
        log_error "  Actual:   $actual"
        return 1
    fi
}

# Sync to platform repository
sync_to_platform() {
    local platform_dir="$1"
    log_info "Syncing to platform repository: $platform_dir"
    
    # Validate platform repo structure
    if [ ! -d "$platform_dir/.git" ]; then
        log_error "Not a git repository: $platform_dir"
        return 1
    fi
    
    local contracts_target="$platform_dir/contracts"
    
    # Create contracts directory if not exists
    mkdir -p "$contracts_target"
    
    # Sync schemas (platform needs all schemas)
    log_info "Syncing schemas..."
    rsync -av --delete \
        --exclude='*.md' \
        --exclude='examples/' \
        "$CONTRACTS_DIR/schemas/" \
        "$contracts_target/schemas/"
    
    # Sync API specs (platform needs public + internal APIs)
    log_info "Syncing API specs..."
    rsync -av \
        "$CONTRACTS_DIR/api/platform_public.v1.yaml" \
        "$CONTRACTS_DIR/api/platform_internal.v1.yaml" \
        "$CONTRACTS_DIR/api/components/" \
        "$contracts_target/api/"
    
    # Copy version file
    cp "$CONTRACTS_DIR/CONTRACTS_VERSION.md" "$contracts_target/"
    
    # Generate types for platform
    log_info "Generating TypeScript types for platform..."
    (cd "$CONTRACTS_DIR" && ./tools/generate_types.sh --typescript)
    
    if [ -d "$CONTRACTS_DIR/generated/typescript" ]; then
        rsync -av "$CONTRACTS_DIR/generated/typescript/" "$platform_dir/src/types/contracts/"
    fi
    
    log_success "Synced to platform repository"
}

# Sync to edge repository
sync_to_edge() {
    local edge_dir="$1"
    log_info "Syncing to edge repository: $edge_dir"
    
    if [ ! -d "$edge_dir/.git" ]; then
        log_error "Not a git repository: $edge_dir"
        return 1
    fi
    
    local contracts_target="$edge_dir/contracts"
    mkdir -p "$contracts_target"
    
    # Edge needs: edge schemas, intake, quarantine, metadata
    log_info "Syncing edge-specific schemas..."
    
    mkdir -p "$contracts_target/schemas/edge"
    mkdir -p "$contracts_target/schemas/shared"
    mkdir -p "$contracts_target/schemas/enums"
    
    # Sync required schemas only
    rsync -av "$CONTRACTS_DIR/schemas/edge/" "$contracts_target/schemas/edge/"
    rsync -av "$CONTRACTS_DIR/schemas/shared/" "$contracts_target/schemas/shared/"
    rsync -av \
        "$CONTRACTS_DIR/schemas/enums/threat_type.enum.v1.json" \
        "$CONTRACTS_DIR/schemas/enums/quarantine_decision.enum.v1.json" \
        "$contracts_target/schemas/enums/"
    
    # Sync edge API
    log_info "Syncing edge API spec..."
    rsync -av \
        "$CONTRACTS_DIR/api/edge_local.v1.yaml" \
        "$CONTRACTS_DIR/api/components/" \
        "$contracts_target/api/"
    
    # Copy version file
    cp "$CONTRACTS_DIR/CONTRACTS_VERSION.md" "$contracts_target/"
    
    # Generate Python types for edge
    log_info "Generating Python types for edge..."
    (cd "$CONTRACTS_DIR" && ./tools/generate_types.sh --python)
    
    if [ -d "$CONTRACTS_DIR/generated/python" ]; then
        rsync -av "$CONTRACTS_DIR/generated/python/" "$edge_dir/src/contracts/"
    fi
    
    log_success "Synced to edge repository"
}

# Worker's KR-041 hash-tracked contract files (EXACTLY 8), vendored FLAT in the
# worker's interface/contracts/. Source == worker CONTRACTS_VERSION.md "Tracked files".
# Deliberately EXCLUDED (worker does not vendor these):
#   - crop_type.enum          → crop_type is INLINE inside the worker schemas, not a separate file
#   - phenology_stage.enum     → worker does not consume phenology; the v7.0.0 MAIZE_*->CORN_*
#                                rename is a NO-OP for the worker (see worker CONTRACTS_VERSION.md v7.0.1)
#   - thermal_analysis_result  → present in schemas/worker/ but NOT a worker-tracked contract file
#   - shared/geojson           → not in the worker's tracked set
#
# DATA-FLOW DIRECTION (critical): this list is used ONLY for a READ-ONLY drift
# comparison, NOT a copy. Per worker CLAUDE.md §2.1 + AK-4 ("worker önden gider,
# kanonik sonra aynalar"), the WORKER LEADS canonical for the 7 schema files —
# it keeps its own permissive runtime form (additionalProperties) and often lands
# fields ahead of the canonical repo, which mirrors later. A canonical→worker copy
# would clobber that ahead-of-canonical work and break the worker's hash gate.
WORKER_TRACKED_FILES=(
    "schemas/worker/analysis_job.v1.schema.json"
    "schemas/worker/analysis_result.v1.schema.json"
    "schemas/worker/calibrated_dataset.v1.schema.json"
    "schemas/worker/calibration_metadata.v1.schema.json"
    "schemas/worker/expert_feedback.v1.schema.json"
    "schemas/worker/expert_labeling_card.v1.schema.json"
    "schemas/worker/expert_review_queue.v1.schema.json"
    "enums/analysis_type.enum.v1.json"
)

# Check the worker's vendored contracts against canonical — READ-ONLY drift report.
#
# This does NOT copy files. The worker vendors its 8 hash-tracked files FLAT in
# interface/contracts/ (NOT a submodule), but per AK-4 the worker LEADS canonical:
# a canonical→worker copy would overwrite the worker's ahead-of-canonical runtime
# form and stale its independent KR-041 hash gate. So we only compare and report;
# a human reconciles any legitimate divergence via a denetim/*_devir_spec_*.md.
sync_to_worker() {
    local worker_dir="$1"
    log_info "Checking worker vendored contracts against canonical: $worker_dir"

    if [ ! -d "$worker_dir/.git" ]; then
        log_error "Not a git repository: $worker_dir"
        return 1
    fi

    local contracts_target="$worker_dir/interface/contracts"
    if [ ! -d "$contracts_target" ]; then
        log_error "Worker vendored dir not found: $contracts_target"
        return 1
    fi

    log_warning "READ-ONLY drift check — the worker LEADS canonical (AK-4); no files are copied."
    local same=0 diff=0 missing=0
    for rel in "${WORKER_TRACKED_FILES[@]}"; do
        local src="$CONTRACTS_DIR/$rel"
        local dst="$contracts_target/$(basename "$rel")"
        if [ ! -f "$dst" ]; then
            log_warning "  MISSING (worker): $(basename "$rel")"
            missing=$((missing + 1))
            continue
        fi
        local hs hd
        hs="$(_lf_sha256 "$src")"
        hd="$(_lf_sha256 "$dst")"
        if [ "$hs" = "$hd" ]; then
            log_success "  SAME:  $(basename "$rel")"
            same=$((same + 1))
        else
            log_warning "  DIFF:  $(basename "$rel")  (canonical=${hs:0:12} worker=${hd:0:12})"
            diff=$((diff + 1))
        fi
    done

    log_info "Worker drift summary: SAME=$same DIFF=$diff MISSING=$missing (of ${#WORKER_TRACKED_FILES[@]})"
    if [ "$diff" -gt 0 ] || [ "$missing" -gt 0 ]; then
        log_warning "Divergence is EXPECTED for worker-led (AK-4) files. Do NOT copy canonical"
        log_warning "over the worker; reconcile via a denetim/*_devir_spec_*.md. After any"
        log_warning "legitimate change: cd $worker_dir && python scripts/compute_contracts_hash.py --update"
    fi
    log_success "Worker drift check complete (no files modified)"
}

# Create sync commit
create_sync_commit() {
    local target_dir="$1"
    local target_name="$2"
    
    log_info "Creating sync commit in $target_name..."
    
    cd "$target_dir"
    
    # Check if there are changes
    if git diff --quiet && git diff --cached --quiet; then
        log_info "No changes to commit"
        return 0
    fi

    if [ "$target_name" = "worker" ]; then
        # sync_to_worker() is READ-ONLY (drift check, no copy — the worker LEADS
        # canonical via AK-4), so this tool never stages or commits worker files.
        # The worker owns its vendored copies + independent KR-041 hash gate; any
        # changes shown here belong to the worker's own work and are committed there.
        log_warning "Worker: this tool made NO changes (read-only drift check)."
        log_warning "Worker commits its own vendored changes + re-pins its hash gate:"
        log_warning "  cd $target_dir && python scripts/compute_contracts_hash.py --update && \\"
        log_warning "    git add interface/contracts/ CONTRACTS_VERSION.md && git commit -m '...'"
        return 0
    fi

    # platform / edge: files live under contracts/ (+ generated types); version + checksum
    # come from the synced contract version file.
    local version=$(grep -oP 'Version: \K[0-9]+\.[0-9]+\.[0-9]+' "$target_dir/contracts/CONTRACTS_VERSION.md" | head -1)

    git add contracts/
    git add src/types/contracts/ 2>/dev/null || true
    git add src/contracts/ 2>/dev/null || true

    git commit -m "chore: sync contracts to v${version}

Synced from tarlaanaliz-contracts@${version}
Checksum: $(get_expected_checksum)

This is an automated sync of contract schemas and types."

    log_success "Created sync commit"
    log_info "To push changes: cd $target_dir && git push"
}

# Main function
main() {
    echo ""
    log_info "TarlaAnaliz Contracts Sync Tool"
    echo ""
    
    local target=""
    local verify_only=false
    local auto_commit=false
    local sync_all=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --target)
                target="$2"
                shift 2
                ;;
            --verify-only)
                verify_only=true
                shift
                ;;
            --auto-commit)
                auto_commit=true
                shift
                ;;
            --all)
                sync_all=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --target <platform|edge|worker>  Sync to specific target"
                echo "  --all                             Sync to all targets"
                echo "  --verify-only                     Only verify checksums"
                echo "  --auto-commit                     Auto-commit changes in target repo"
                echo "  --help, -h                        Show this help"
                echo ""
                echo "Environment variables:"
                echo "  PLATFORM_DIR   Path to platform repository"
                echo "  EDGE_DIR       Path to edge repository"
                echo "  WORKER_DIR     Path to worker repository"
                echo ""
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Verify checksums first
    if ! verify_checksums; then
        log_error "Checksum verification failed!"
        log_error "Please run: python3 tools/pin_version.py --verify"
        exit 1
    fi
    
    if [ "$verify_only" = true ]; then
        log_success "Verification complete"
        exit 0
    fi
    
    # Sync to targets
    if [ "$sync_all" = true ]; then
        # Sync to all targets
        if [ -n "${PLATFORM_DIR:-}" ]; then
            sync_to_platform "$PLATFORM_DIR"
            [ "$auto_commit" = true ] && create_sync_commit "$PLATFORM_DIR" "platform"
        fi
        
        if [ -n "${EDGE_DIR:-}" ]; then
            sync_to_edge "$EDGE_DIR"
            [ "$auto_commit" = true ] && create_sync_commit "$EDGE_DIR" "edge"
        fi
        
        if [ -n "${WORKER_DIR:-}" ]; then
            sync_to_worker "$WORKER_DIR"
            [ "$auto_commit" = true ] && create_sync_commit "$WORKER_DIR" "worker"
        fi
    elif [ -n "$target" ]; then
        # Sync to specific target
        case $target in
            platform)
                if [ -z "${PLATFORM_DIR:-}" ]; then
                    log_error "PLATFORM_DIR environment variable not set"
                    exit 1
                fi
                sync_to_platform "$PLATFORM_DIR"
                [ "$auto_commit" = true ] && create_sync_commit "$PLATFORM_DIR" "platform"
                ;;
            edge)
                if [ -z "${EDGE_DIR:-}" ]; then
                    log_error "EDGE_DIR environment variable not set"
                    exit 1
                fi
                sync_to_edge "$EDGE_DIR"
                [ "$auto_commit" = true ] && create_sync_commit "$EDGE_DIR" "edge"
                ;;
            worker)
                if [ -z "${WORKER_DIR:-}" ]; then
                    log_error "WORKER_DIR environment variable not set"
                    exit 1
                fi
                sync_to_worker "$WORKER_DIR"
                [ "$auto_commit" = true ] && create_sync_commit "$WORKER_DIR" "worker"
                ;;
            *)
                log_error "Invalid target: $target"
                log_error "Valid targets: platform, edge, worker"
                exit 1
                ;;
        esac
    else
        log_error "No target specified"
        log_info "Use --target <platform|edge|worker> or --all"
        exit 1
    fi
    
    echo ""
    log_success "Sync complete!"
    echo ""
}

# Run main
main "$@"