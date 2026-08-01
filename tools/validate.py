#!/usr/bin/env python3
"""
TarlaAnaliz Contracts Validator
Validates all JSON Schema and OpenAPI files
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Forbidden fields (per KR-050: NO email, NO TCKN, NO OTP)
# ⚠️ TEK KAYNAK: `pyproject.toml → [tool.tarlaanaliz.schema].forbidden_fields` bu listeyi
# AYNALAR ve `tests/test_pii_scope_gate.py` ikisinin ayrışmasını yasaklar (2026-07-31/D18 —
# ölçüldü: pyproject 3 değer taşırken buradaki liste 6 değerdi, yani politika iki farklı
# şey söylüyordu).
FORBIDDEN_FIELDS = ['email', 'e_mail', 'tckn', 'tc_kimlik_no', 'otp', 'one_time_password']

# --- KAPSAM-DUYARLI alanlar (D18 / K4) --------------------------------------
# `phone` KR-050'de YASAK DEĞİLDİR — kimlik modelinin ta kendisidir (telefon + 6 haneli PIN).
# Ama yeri BELLİDİR: numara `user_pii.v1`de saklanır ve kimlik doğrulama yüzeyinde taşınır;
# başka hiçbir şemaya sızmamalıdır (`user.v1` bunu kendi notunda da söylüyor:
# "Phone is stored in user_pii, NOT here"). Bu kural bugüne kadar YAZILIYDI ama
# ZORLANMIYORDU; SDLC_GATES §1B'nin "user_pii.v1 dışında zorunlu alan değildir" maddesini
# hiçbir araç kontrol etmiyordu.
SCOPED_FIELDS: Dict[str, tuple] = {
    'phone': (
        'schemas/core/user_pii.v1.schema.json',   # numaranın kanonik yeri
        'api/components/schemas.yaml',            # LoginRequest — kimlik doğrulama yüzeyi
        'api/components/security_schemes.yaml',   # auth şeması açıklaması
        'api/platform_public.v1.yaml',            # public login uçları
    ),
}


# --- BELGE ÜSTVERİSİ istisnası — ŞU AN BOŞ, ÖYLE KALMALI --------------------
# 2026-07-31/D18: `api/` ağacı ilk kez tarandığında tek isabet çıkmıştı —
# `api/platform_public.v1.yaml → $.info.contact.email` (destek adresi). Kısa süre için
# dar bir istisna tanımlandı, sonra **D18-b kararıyla adres SİLİNDİ** ve istisna boşaldı.
#
# 🔒 KURAL: bu sözlük BOŞ kalır. Bir güvenlik kapısındaki her istisna, sonraki
# değişikliklerin arkasına saklanabileceği kalıcı bir yüzeydir; sıfır istisnalı kapı
# tek istisnalı kapıdan kesinlikle güçlüdür. `tests/test_pii_scope_gate.py` boşluğu
# ZORLAR — yeni bir istisna eklemek testi de bilinçli olarak değiştirmeyi gerektirir.
METADATA_EXCEPTIONS: Dict[str, tuple] = {}


def _rel(path: Path) -> str:
    """Depo köküne göre posix yol (kapsam kuralları bununla eşleşir).

    ÖD-13 (2026-08-01): `dist/schemas/...` yayın kopyası **kaynağının kapsamını devralır**.
    Yayın ağacı araçla üretilir (`tools/inline_refs.py`); ikizini ayrı bir dosya sayarsak
    `user_pii.v1` gibi meşru bir PII taşıyıcısı yayın tarafında "kapsam dışı" diye kırmızı
    verir — kapı gürültüye boğulur ve ilk refleks onu kapatmak olur. Bayatlık ayrı bir
    kapının işidir (`inline_refs.py --check`); burada İÇERİK kuralı koşar.
    """
    try:
        relative = path.resolve().relative_to(Path(__file__).resolve().parents[1]).as_posix()
    except ValueError:  # pragma: no cover — depo dışı yol
        return path.as_posix()
    return relative[len("dist/"):] if relative.startswith("dist/schemas/") else relative


def _check_forbidden_recursive(obj: Any, path: str, schema_path: Path) -> List[str]:
    """Recursively check for forbidden PII fields in nested objects.

    İki kural:
      1. `FORBIDDEN_FIELDS` — her yerde yasak (KR-050 sert kuralı).
      2. `SCOPED_FIELDS`    — yalnız izinli dosyalarda; başka yerde alan adı olarak
         görünmesi hatadır. `phone_verified` gibi TÜREV adlar etkilenmez (eşleşme TAM
         alan adı üzerindedir, alt dize DEĞİL).
    """
    errors = []
    relative = _rel(schema_path)
    exempt = METADATA_EXCEPTIONS.get(relative, ())
    if isinstance(obj, dict):
        for key, value in obj.items():
            lowered = key.lower()
            if lowered in FORBIDDEN_FIELDS and f"{path}.{key}" not in exempt:
                errors.append(
                    f"FORBIDDEN field '{key}' found at {path}.{key} in {schema_path}"
                )
            allowed = SCOPED_FIELDS.get(lowered)
            if allowed is not None and relative not in allowed:
                errors.append(
                    f"OUT-OF-SCOPE PII field '{key}' at {path}.{key} in {relative} "
                    f"(KR-050: yalnız {', '.join(allowed)} içinde taşınabilir)"
                )
            errors.extend(_check_forbidden_recursive(value, f"{path}.{key}", schema_path))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            errors.extend(_check_forbidden_recursive(item, f"{path}[{i}]", schema_path))
    return errors


def validate_openapi_pii(spec_path: Path) -> List[str]:
    """OpenAPI dosyalarında PII taraması (D18 / K4).

    NEDEN: `api/` ağacı bugüne kadar **hiçbir** PII kapısından geçmiyordu — ne bu araç
    (yalnız `schemas/` + `enums/` tarıyordu) ne de CI'ın grep işi (yalnız `schemas/`).
    Oysa `api/components/schemas.yaml` kimlik yüzeyini (telefon + PIN) tanımlıyor; oraya
    eklenecek bir `email` alanı hiçbir kapıya takılmazdı.
    """
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return [
            f"{_rel(spec_path)}: pyyaml kurulu değil — OpenAPI PII taraması KOŞMADI. "
            "Sessiz atlama yeşil sayılmaz (requirements-dev.txt'i kurun)."
        ]
    try:
        document = yaml.safe_load(spec_path.read_text(encoding='utf-8'))
    except Exception as exc:  # noqa: BLE001 — okunamayan dosya kapıyı körleştirir
        return [f"{_rel(spec_path)}: OpenAPI ayrıştırılamadı ({exc})"]
    return _check_forbidden_recursive(document, "$", spec_path)


def _check_unevaluated_in_defs(schema: dict, schema_path: Path) -> List[str]:
    """Check that all object-type $defs have unevaluatedProperties: false."""
    errors = []
    defs = schema.get('$defs', {})
    if not isinstance(defs, dict):
        return errors
    for def_name, def_schema in defs.items():
        if not isinstance(def_schema, dict):
            continue
        if def_schema.get('type') == 'object':
            if 'unevaluatedProperties' not in def_schema:
                errors.append(
                    f"Missing unevaluatedProperties in $defs.{def_name} in {schema_path}"
                )
            elif def_schema['unevaluatedProperties'] is not False:
                errors.append(
                    f"unevaluatedProperties must be false in $defs.{def_name} in {schema_path}"
                )
    return errors


def validate_json_schema(schema_path: Path) -> List[str]:
    """Validate JSON Schema file"""
    errors = []

    try:
        with open(schema_path, encoding='utf-8') as f:
            schema = json.load(f)

        # Check $schema
        if '$schema' not in schema:
            errors.append(f"Missing $schema in {schema_path}")
        elif 'draft/2020-12' not in schema['$schema']:
            errors.append(f"Wrong draft version in {schema_path} (must be 2020-12)")

        # Check $id (KR-081: mandatory, must use canonical URL)
        if '$id' not in schema:
            errors.append(f"Missing $id in {schema_path}")
        elif not schema['$id'].startswith('https://api.tarlaanaliz.com/schemas/'):
            errors.append(
                f"Invalid $id format in {schema_path}: "
                f"must start with https://api.tarlaanaliz.com/schemas/"
            )

        # Check title (KR-081: mandatory)
        if 'title' not in schema:
            errors.append(f"Missing title in {schema_path}")

        # Check type (KR-081: mandatory)
        if 'type' not in schema:
            errors.append(f"Missing type in {schema_path}")

        # Check unevaluatedProperties at root level
        if schema.get('type') == 'object':
            if 'unevaluatedProperties' not in schema:
                errors.append(f"Missing unevaluatedProperties in {schema_path}")
            elif schema['unevaluatedProperties'] is not False:
                errors.append(f"unevaluatedProperties must be false in {schema_path}")

        # Check unevaluatedProperties in $defs
        errors.extend(_check_unevaluated_in_defs(schema, schema_path))

        # Check for forbidden fields recursively (KR-050)
        errors.extend(_check_forbidden_recursive(schema, "$", schema_path))

    except json.JSONDecodeError as e:
        errors.append(f"JSON parse error in {schema_path}: {e}")
    except Exception as e:
        errors.append(f"Error validating {schema_path}: {e}")

    return errors


def validate_enum_file(enum_path: Path) -> List[str]:
    """Validate enum file structure."""
    errors = []

    try:
        with open(enum_path, encoding='utf-8') as f:
            data = json.load(f)

        # Check required fields
        if 'enum' not in data:
            errors.append(f"Missing 'enum' array in {enum_path}")
        else:
            values = data['enum']
            if len(values) != len(set(values)):
                errors.append(f"Duplicate enum values in {enum_path}")
            if not values:
                errors.append(f"Empty enum array in {enum_path}")

        # Check for forbidden fields
        errors.extend(_check_forbidden_recursive(data, "$", enum_path))

    except json.JSONDecodeError as e:
        errors.append(f"JSON parse error in {enum_path}: {e}")
    except Exception as e:
        errors.append(f"Error validating {enum_path}: {e}")

    return errors


def validation_targets(base_dir: Path) -> List[Path]:
    """Kapının FİİLEN taradığı dosyalar — kapsam iddiası burada ölçülebilir olsun.

    `main()` bu listeyi kullanır; `tests/test_publication_tree_gates.py` de aynı listeyi
    okur. Böylece "yayın ağacı da taranıyor" iddiası kaynak koda bakarak değil
    **ölçülerek** doğrulanır (ÖD-13).
    """
    targets: List[Path] = []
    targets.extend(sorted((base_dir / 'schemas').rglob('*.json')))
    enums_dir = base_dir / 'enums'
    if enums_dir.exists():
        targets.extend(sorted(enums_dir.rglob('*.json')))
    dist_dir = base_dir / 'dist' / 'schemas'
    if dist_dir.exists():
        targets.extend(sorted(dist_dir.rglob('*.json')))
    api_dir = base_dir / 'api'
    if api_dir.exists():
        targets.extend(sorted(api_dir.rglob('*.yaml')))
    return targets


def main():
    """Main validation"""
    # Windows consoles default to a legacy code page (e.g. cp1254) that cannot
    # encode the status emoji below and raises UnicodeEncodeError. Force UTF-8.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")

    print("🔍 TarlaAnaliz Contracts Validator\n")

    base_dir = Path(__file__).parent.parent
    schemas_dir = base_dir / 'schemas'
    enums_dir = base_dir / 'enums'

    all_errors = []
    total_files = 0

    # Validate all JSON Schema files
    for schema_file in schemas_dir.rglob('*.json'):
        total_files += 1
        print(f"Validating {schema_file.relative_to(base_dir)}...")
        errors = validate_json_schema(schema_file)
        all_errors.extend(errors)

    # Validate enum files
    if enums_dir.exists():
        for enum_file in enums_dir.rglob('*.json'):
            total_files += 1
            print(f"Validating {enum_file.relative_to(base_dir)}...")
            errors = validate_enum_file(enum_file)
            all_errors.extend(errors)

    # ÖD-13 (2026-08-01): YAYIN AĞACI da doğrulanır. `dist/schemas/` hava-boşluklu M1'in
    # tükettiği biçimdir (harici `$ref` yok) ve bugüne kadar HİÇBİR kapıdan geçmiyordu:
    # ne validate, ne PII taraması, ne checksum. Yani kaynağa giremeyen bir PII alanı
    # yayın ağacına elle eklenebilir ya da bayat bir kopya orada yaşamaya devam edebilirdi.
    # (Bayatlık `inline_refs.py --check` ile ayrıca ölçülür; burada İÇERİK kuralları koşar.)
    dist_dir = base_dir / 'dist' / 'schemas'
    if dist_dir.exists():
        for dist_file in sorted(dist_dir.rglob('*.json')):
            total_files += 1
            print(f"Validating {dist_file.relative_to(base_dir)} (yayın ağacı)...")
            all_errors.extend(validate_json_schema(dist_file))

    # OpenAPI PII taraması (D18/K4) — `api/` ağacı önceden HİÇBİR kapıdan geçmiyordu.
    api_dir = base_dir / 'api'
    if api_dir.exists():
        for spec_file in sorted(api_dir.rglob('*.yaml')):
            total_files += 1
            print(f"Validating {spec_file.relative_to(base_dir)} (PII scope)...")
            all_errors.extend(validate_openapi_pii(spec_file))

    # Print results
    print(f"\n{'='*60}")
    print(f"Total files validated: {total_files}")
    print(f"Total errors: {len(all_errors)}")

    if all_errors:
        print("\n❌ VALIDATION FAILED\n")
        for error in all_errors:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print("\n✅ ALL VALIDATIONS PASSED")
        sys.exit(0)


if __name__ == '__main__':
    main()
