#!/usr/bin/env python3
"""
TarlaAnaliz Breaking Change Detector

Detects breaking changes between two versions of JSON Schema contracts.
Generates machine-readable report and PR comment format.

Usage:
    python3 tools/breaking_change_detector.py --old v1.0.0 --new v1.1.0
    python3 tools/breaking_change_detector.py --pr-comment
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from enum import Enum


class ChangeType(Enum):
    """Types of schema changes"""
    # Breaking changes (require MAJOR version bump)
    FIELD_REMOVED = "FIELD_REMOVED"
    FIELD_TYPE_CHANGED = "FIELD_TYPE_CHANGED"
    FIELD_MADE_REQUIRED = "FIELD_MADE_REQUIRED"
    ENUM_VALUE_REMOVED = "ENUM_VALUE_REMOVED"
    SCHEMA_REMOVED = "SCHEMA_REMOVED"
    ARRAY_ITEMS_CHANGED = "ARRAY_ITEMS_CHANGED"
    MIN_MAX_TIGHTENED = "MIN_MAX_TIGHTENED"
    PATTERN_TIGHTENED = "PATTERN_TIGHTENED"
    
    # Non-breaking changes (allow MINOR version bump)
    FIELD_ADDED_OPTIONAL = "FIELD_ADDED_OPTIONAL"
    ENUM_VALUE_ADDED = "ENUM_VALUE_ADDED"
    SCHEMA_ADDED = "SCHEMA_ADDED"
    DESCRIPTION_CHANGED = "DESCRIPTION_CHANGED"
    MIN_MAX_RELAXED = "MIN_MAX_RELAXED"
    PATTERN_RELAXED = "PATTERN_RELAXED"
    
    # Documentation only (allow PATCH version bump)
    EXAMPLE_CHANGED = "EXAMPLE_CHANGED"
    NOTES_CHANGED = "NOTES_CHANGED"


class BreakingChangeDetector:
    """Detects breaking changes in JSON Schema"""
    
    def __init__(self, old_dir: Path, new_dir: Path):
        self.old_dir = old_dir
        self.new_dir = new_dir
        self.changes: List[Dict[str, Any]] = []
    
    def load_schema(self, path: Path) -> Dict:
        """Load JSON Schema file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load {path}: {e}")
            return {}
    
    def get_schema_files(self, directory: Path) -> Set[Path]:
        """Get all schema files in directory"""
        return set(directory.rglob('*.json'))
    
    def compare_schemas(self, old_schema: Dict, new_schema: Dict, schema_path: str):
        """Compare two schema versions and detect changes"""
        
        # Check if schema was removed
        if old_schema and not new_schema:
            self.changes.append({
                'type': ChangeType.SCHEMA_REMOVED.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'message': f"Schema removed: {schema_path}"
            })
            return
        
        # Check if schema was added
        if not old_schema and new_schema:
            self.changes.append({
                'type': ChangeType.SCHEMA_ADDED.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'message': f"Schema added: {schema_path}"
            })
            return
        
        # Compare properties
        old_props = old_schema.get('properties', {})
        new_props = new_schema.get('properties', {})
        
        old_required = set(old_schema.get('required', []))
        new_required = set(new_schema.get('required', []))
        
        # Check for removed fields
        removed_fields = set(old_props.keys()) - set(new_props.keys())
        for field in removed_fields:
            self.changes.append({
                'type': ChangeType.FIELD_REMOVED.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'field': field,
                'message': f"Field removed: {field} in {schema_path}"
            })
        
        # Check for added required fields (breaking)
        added_required = new_required - old_required
        for field in added_required:
            if field in new_props and field not in old_props:
                self.changes.append({
                    'type': ChangeType.FIELD_MADE_REQUIRED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': field,
                    'message': f"New required field added: {field} in {schema_path}"
                })
            elif field in old_props:
                self.changes.append({
                    'type': ChangeType.FIELD_MADE_REQUIRED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': field,
                    'message': f"Field made required: {field} in {schema_path}"
                })
        
        # Check for type changes
        for field in set(old_props.keys()) & set(new_props.keys()):
            old_type = old_props[field].get('type')
            new_type = new_props[field].get('type')
            
            if old_type and new_type and old_type != new_type:
                self.changes.append({
                    'type': ChangeType.FIELD_TYPE_CHANGED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': field,
                    'old_type': old_type,
                    'new_type': new_type,
                    'message': f"Type changed: {field} from {old_type} to {new_type} in {schema_path}"
                })
            
            # Check for pattern changes
            old_pattern = old_props[field].get('pattern')
            new_pattern = new_props[field].get('pattern')
            
            if old_pattern and new_pattern and old_pattern != new_pattern:
                # This is potentially breaking (tightened pattern)
                self.changes.append({
                    'type': ChangeType.PATTERN_TIGHTENED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': field,
                    'old_pattern': old_pattern,
                    'new_pattern': new_pattern,
                    'message': f"Pattern changed: {field} in {schema_path} (potentially breaking)"
                })
            
            # Check for min/max changes
            self.check_constraint_changes(old_props[field], new_props[field], schema_path, field)
        
        # Check for added optional fields (non-breaking)
        added_optional = set(new_props.keys()) - set(old_props.keys()) - added_required
        for field in added_optional:
            self.changes.append({
                'type': ChangeType.FIELD_ADDED_OPTIONAL.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'field': field,
                'message': f"Optional field added: {field} in {schema_path}"
            })
        
        # Check enum changes
        self.compare_enums(old_schema, new_schema, schema_path)
        
        # Check description changes (documentation only)
        if old_schema.get('description') != new_schema.get('description'):
            self.changes.append({
                'type': ChangeType.DESCRIPTION_CHANGED.value,
                'severity': 'DOCUMENTATION',
                'file': schema_path,
                'message': f"Description updated in {schema_path}"
            })
    
    def check_constraint_changes(self, old_prop: Dict, new_prop: Dict, schema_path: str, field: str):
        """Check for constraint changes (min/max, minLength/maxLength, etc.)"""
        
        constraints = [
            ('minimum', 'increased'),
            ('maximum', 'decreased'),
            ('minLength', 'increased'),
            ('maxLength', 'decreased'),
            ('minItems', 'increased'),
            ('maxItems', 'decreased')
        ]
        
        for constraint, direction in constraints:
            old_val = old_prop.get(constraint)
            new_val = new_prop.get(constraint)
            
            if old_val is not None and new_val is not None:
                if direction == 'increased' and new_val > old_val:
                    self.changes.append({
                        'type': ChangeType.MIN_MAX_TIGHTENED.value,
                        'severity': 'BREAKING',
                        'file': schema_path,
                        'field': field,
                        'constraint': constraint,
                        'old_value': old_val,
                        'new_value': new_val,
                        'message': f"Constraint tightened: {field}.{constraint} {direction} from {old_val} to {new_val} in {schema_path}"
                    })
                elif direction == 'decreased' and new_val < old_val:
                    self.changes.append({
                        'type': ChangeType.MIN_MAX_TIGHTENED.value,
                        'severity': 'BREAKING',
                        'file': schema_path,
                        'field': field,
                        'constraint': constraint,
                        'old_value': old_val,
                        'new_value': new_val,
                        'message': f"Constraint tightened: {field}.{constraint} {direction} from {old_val} to {new_val} in {schema_path}"
                    })
    
    def compare_enums(self, old_schema: Dict, new_schema: Dict, schema_path: str):
        """Compare enum values"""
        old_enum = set(old_schema.get('enum', []))
        new_enum = set(new_schema.get('enum', []))
        
        if not old_enum and not new_enum:
            return
        
        # Check for removed enum values (breaking)
        removed_values = old_enum - new_enum
        for value in removed_values:
            self.changes.append({
                'type': ChangeType.ENUM_VALUE_REMOVED.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'value': value,
                'message': f"Enum value removed: {value} in {schema_path}"
            })
        
        # Check for added enum values (non-breaking)
        added_values = new_enum - old_enum
        for value in added_values:
            self.changes.append({
                'type': ChangeType.ENUM_VALUE_ADDED.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'value': value,
                'message': f"Enum value added: {value} in {schema_path}"
            })
    
    def scan_tree(self, old_dir: Path, new_dir: Path) -> None:
        """Walk a matched old/new directory tree and accumulate detected changes.

        Callable more than once on the same detector to cover several roots
        (e.g. schemas/ then enums/); results append to self.changes.
        """
        old_files = self.get_schema_files(old_dir)
        new_files = self.get_schema_files(new_dir)

        # Get relative paths
        old_rel_paths = {f.relative_to(old_dir) for f in old_files}
        new_rel_paths = {f.relative_to(new_dir) for f in new_files}

        # Check all files
        all_rel_paths = old_rel_paths | new_rel_paths

        for rel_path in sorted(all_rel_paths):
            old_file = old_dir / rel_path
            new_file = new_dir / rel_path

            old_schema = self.load_schema(old_file) if old_file.exists() else {}
            new_schema = self.load_schema(new_file) if new_file.exists() else {}

            self.compare_schemas(old_schema, new_schema, str(rel_path))

    def categorize(self) -> Dict[str, List[Dict]]:
        """Categorize accumulated changes by severity"""
        breaking = [c for c in self.changes if c['severity'] == 'BREAKING']
        non_breaking = [c for c in self.changes if c['severity'] == 'NON_BREAKING']
        documentation = [c for c in self.changes if c['severity'] == 'DOCUMENTATION']

        return {
            'breaking': breaking,
            'non_breaking': non_breaking,
            'documentation': documentation,
            'total': len(self.changes),
            'has_breaking': len(breaking) > 0
        }

    def detect_changes(self) -> Dict[str, List[Dict]]:
        """Detect all changes between old and new versions (single root)"""
        self.scan_tree(self.old_dir, self.new_dir)
        return self.categorize()
    
    def generate_report(self, categorized_changes: Dict) -> str:
        """Generate human-readable report"""
        
        report = "# Breaking Change Detection Report\n\n"
        
        # Summary
        report += "## Summary\n\n"
        report += f"- **Total Changes:** {categorized_changes['total']}\n"
        report += f"- **Breaking Changes:** {len(categorized_changes['breaking'])}\n"
        report += f"- **Non-Breaking Changes:** {len(categorized_changes['non_breaking'])}\n"
        report += f"- **Documentation Changes:** {len(categorized_changes['documentation'])}\n\n"
        
        if categorized_changes['has_breaking']:
            report += "⚠️  **BREAKING CHANGES DETECTED** - Requires MAJOR version bump\n\n"
        else:
            report += "✅ No breaking changes detected\n\n"
        
        # Breaking changes
        if categorized_changes['breaking']:
            report += "## ⚠️  Breaking Changes\n\n"
            for change in categorized_changes['breaking']:
                report += f"### {change['type']}\n"
                report += f"- **File:** `{change['file']}`\n"
                if 'field' in change:
                    report += f"- **Field:** `{change['field']}`\n"
                report += f"- **Message:** {change['message']}\n\n"
        
        # Non-breaking changes
        if categorized_changes['non_breaking']:
            report += "## ✨ Non-Breaking Changes\n\n"
            for change in categorized_changes['non_breaking']:
                report += f"- {change['message']}\n"
            report += "\n"
        
        # Documentation changes
        if categorized_changes['documentation']:
            report += "## 📝 Documentation Changes\n\n"
            for change in categorized_changes['documentation']:
                report += f"- {change['message']}\n"
            report += "\n"
        
        return report
    
    def generate_pr_comment(self, categorized_changes: Dict) -> str:
        """Generate PR comment format"""
        
        comment = "## 🔍 Contract Changes Analysis\n\n"
        
        if categorized_changes['has_breaking']:
            comment += "### ⚠️  BREAKING CHANGES DETECTED\n\n"
            comment += "**Action Required:** This PR requires a **MAJOR** version bump.\n\n"
            comment += "**Breaking Changes:**\n"
            for change in categorized_changes['breaking']:
                comment += f"- ❌ `{change['file']}`: {change['message']}\n"
            comment += "\n"
        else:
            comment += "### ✅ No Breaking Changes\n\n"
        
        if categorized_changes['non_breaking']:
            comment += "**Non-Breaking Changes:**\n"
            for change in categorized_changes['non_breaking'][:5]:  # Limit to 5
                comment += f"- ✨ {change['message']}\n"
            if len(categorized_changes['non_breaking']) > 5:
                comment += f"- ... and {len(categorized_changes['non_breaking']) - 5} more\n"
            comment += "\n"
        
        # Version recommendation
        comment += "### 📌 Recommended Version Bump\n\n"
        if categorized_changes['has_breaking']:
            comment += "```bash\npython3 tools/pin_version.py --major --breaking\n```\n"
        elif categorized_changes['non_breaking']:
            comment += "```bash\npython3 tools/pin_version.py --minor\n```\n"
        else:
            comment += "```bash\npython3 tools/pin_version.py --patch\n```\n"
        
        return comment


def main():
    """Main CLI"""
    parser = argparse.ArgumentParser(
        description='Detect breaking changes in TarlaAnaliz contracts'
    )
    
    parser.add_argument('--old', required=True, help='Old version directory or tag')
    parser.add_argument('--new', default='.', help='New version directory (default: current)')
    parser.add_argument('--pr-comment', action='store_true', help='Output PR comment format')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    
    args = parser.parse_args()
    
    old_dir = Path(args.old)
    new_dir = Path(args.new)
    
    if not old_dir.exists():
        print(f"❌ Old directory not found: {old_dir}")
        sys.exit(1)
    
    if not new_dir.exists():
        print(f"❌ New directory not found: {new_dir}")
        sys.exit(1)
    
    # Detect changes across the checksummed contract trees: schemas/ AND enums/.
    # The canonical enum SSOT (crop_type, phenology_stage, analysis_type, ...)
    # lives at top-level enums/; enum value removals/renames are MAJOR breaking
    # and must not be invisible to the detector.
    print(f"🔍 Comparing contracts (schemas/ + enums/)...")
    print(f"   Old: {old_dir}")
    print(f"   New: {new_dir}\n")

    detector = BreakingChangeDetector(old_dir / 'schemas', new_dir / 'schemas')
    detector.scan_tree(detector.old_dir, detector.new_dir)  # schemas/

    enums_old = old_dir / 'enums'
    enums_new = new_dir / 'enums'
    if enums_old.exists() or enums_new.exists():
        detector.scan_tree(enums_old, enums_new)  # enums/

    categorized_changes = detector.categorize()
    
    # Output format
    if args.json:
        print(json.dumps(categorized_changes, indent=2))
    elif args.pr_comment:
        print(detector.generate_pr_comment(categorized_changes))
    else:
        print(detector.generate_report(categorized_changes))
    
    # Exit code
    if categorized_changes['has_breaking']:
        sys.exit(1)  # Breaking changes detected
    else:
        sys.exit(0)  # No breaking changes


if __name__ == '__main__':
    main()