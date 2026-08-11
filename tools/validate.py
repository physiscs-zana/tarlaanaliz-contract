#!/usr/bin/env python3
"""
TarlaAnaliz Contracts Validator
Validates all JSON Schema and OpenAPI files
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, NamedTuple

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


# --- ALAN SIZMASI (field drift) kapısı — AĞACIN TAMAMI --------------------------
# 2026-08-11: bu kapı yalnız KÖK şemayı ve `$defs` altındaki BİRİNCİ seviye object'leri
# denetliyordu. Ölçüldü: `schemas/` ağacındaki 310 object düğümünün 79'u o iki konumun
# dışındaydı ve **28'i hiçbir koruma taşımıyordu** — yani dizi öğeleri (`items`) ve iç içe
# nesneler sözleşmede TANIMSIZ alanları sessizce kabul ediyordu. Davranışsal kanıt
# (KR-073 AV tarama raporu, `datasets/scan_report.v1`):
#     kök'e tanımsız alan  -> 1 hata (kapı çalışıyor)
#     findings[]'e aynı alan -> 0 hata (SESSİZCE GEÇİYOR)
# İlk tarayıcı `"type": ["object", "null"]` BİRLEŞİK tiplerini de kaçırmıştı (7 düğüm daha).
#
# KURAL: her object düğümü politikasını **BEYAN ETMEK ZORUNDADIR** —
#   * `unevaluatedProperties: false`  → kapalı (tercih edilen), ya da
#   * `additionalProperties` (true/false) → bilinçli, gerekçesi yazılı karar.
# Yasak olan **sessizlik**tir: beyansız object, sızmayı kaza eseri kabul eder.
#
# NEDEN `additionalProperties: true` kabul ediliyor: bazı düğümler gerçekten serbest
# biçimlidir (`metadata` uzantı blokları, keyfi GeoJSON geometrileri). Onları kapatmak
# sözleşmeyi yanlış yere daraltırdı. Ama açıklık bir KARAR olmalı, kaza değil — bu yüzden
# anahtarın AÇIKÇA yazılması gerekir.
#
# ⚠️ `additionalProperties: false` kompozisyon (allOf/oneOf/anyOf) içinde kardeş şemaların
# tanımladığı alanları GÖREMEZ ve yanlış reddeder. Ölçüldü (2026-08-11): bu depodaki
# `additionalProperties: false` taşıyan 19 düğümün **hiçbiri** kompozisyon içinde değil.
# Yeni bir kompozisyon düğümünde `unevaluatedProperties` tercih edin.

#: Şema İÇİNDE yaşayan ama şema OLMAYAN bloklar — içleri örnek/açıklama verisidir,
#: kural oralarda koşmaz (yoksa bir örnek payload'daki `"type": "object"` yanlış alarm üretir).
_NON_SCHEMA_KEYS = frozenset({'examples', 'example', 'default', 'const', 'enum', 'notes'})

# --- PARİTE-KİLİTLİ İSTİSNA — TEK GİRİŞ, GEREKÇESİ ÖLÇÜLDÜ ----------------------
# I-4: worker `analysis_result.v1`'i dar bir alt küme olarak vendor'lar ve
# `tests/test_vendored_parity.py::TestSubsetPairsMayOmitButNotContradict` ortak `$defs`
# alanlarının doğrulama anlamının AYNI kalmasını zorlar. O kapı `_strip_annotations` ile
# `additionalProperties` ve `unevaluatedProperties`'i TEK anahtara (`__no_extra__`)
# indirger (test_vendored_parity.py:262-265) — yani kanonik tarafa **hangi politika
# anahtarını koyarsak koyalım**, vendored kopyada karşılığı yokken çelişki üretir.
# Ölçüldü (2026-08-11): `unevaluatedProperties: false` denendi → parite kapısı kırmızı;
# `additionalProperties: true` denendi → yine kırmızı (anahtarın VARLIĞI fark sayılıyor).
#
# Daraltmanın kendisi de ölçümle desteklenmiyordu: tüketicide alan opak taşınıyor
# (`tarlaanaliz-worker/src/core/domain/analysis_result.py:29` → `bbox: dict[str, float] | None`,
# `:249` → doğrudan aktarım) ve anahtar kümesini kısıtlayan tek satır yok.
#
# ÇIKIŞ KOŞULU (bu istisna kalıcı DEĞİLDİR — I-5): worker'ın vendored kopyasına aynı
# politika anahtarı yayılır (`tools/propagate_vendored.py`), sonra bu giriş SİLİNİR.
# Not: yayılım bu turda YAPILMADI çünkü worker deposunda eşzamanlı başka bir aktör
# çalışıyordu (`denetim/cerrahi-kalite-2026-08-11` dalı, kirli ağaç).
_PARITY_LOCKED_OPEN: Dict[str, tuple] = {
    'schemas/worker/analysis_result.v1.schema.json': (
        '$.$defs.Detection.properties.bbox',
    ),
}


#: "anahtar hiç yok" ile "anahtar var ama değeri None" ayrımı — ikincisi de bir HATADIR.
_MISSING = object()


def _is_object_node(node: Any) -> bool:
    """`type` doğrudan 'object' ya da 'object' içeren bir BİRLEŞİK tip mi?"""
    declared = node.get('type')
    if declared == 'object':
        return True
    return isinstance(declared, list) and 'object' in declared


def _check_object_policy(schema: Any, schema_path: Path) -> List[str]:
    """Ağacın TAMAMINDA: her object düğümü sızma politikasını beyan etmeli."""
    errors: List[str] = []
    locked = _PARITY_LOCKED_OPEN.get(_rel(schema_path), ())

    def walk(node: Any, pointer: str) -> None:
        if isinstance(node, dict):
            if pointer in locked:
                pass
            elif pointer != "$" and _is_object_node(node):
                declared = node.get('unevaluatedProperties', _MISSING)
                if declared is not _MISSING and declared is not False:
                    # Yazılmış ama YANLIŞ yazılmış: `unevaluatedProperties: true` kuralı
                    # kapatmaz, açar. Bunu "beyansız" saymak teşhisi gizlerdi.
                    errors.append(
                        f"unevaluatedProperties must be false (got {declared!r}) "
                        f"at {pointer} in {schema_path}"
                    )
                elif declared is _MISSING and 'additionalProperties' not in node:
                    errors.append(
                        f"UNDECLARED object policy at {pointer} in {schema_path}: "
                        "her object düğümü ya `unevaluatedProperties: false` (kapalı) ya da "
                        "`additionalProperties` (bilinçli açık, gerekçesi description'da) "
                        "beyan etmelidir. Beyansız düğüm, sözleşmede tanımsız alanları "
                        "sessizce kabul eder (alan sızması)."
                    )
            for key, value in node.items():
                if key in _NON_SCHEMA_KEYS or key.startswith('x-'):
                    continue
                walk(value, f"{pointer}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{pointer}[{index}]")

    walk(schema, "$")
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

        # Alan sızması: AĞACIN TAMAMI ($defs birinci seviyesi değil — dizi öğeleri,
        # iç içe nesneler ve birleşik tipler dahil). Kök yukarıda ayrıca ve DAHA SIKI
        # denetlenir (kökte "bilinçli açık" seçeneği yoktur), bu yüzden walker kökü atlar.
        errors.extend(_check_object_policy(schema, schema_path))

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


class Target(NamedTuple):
    """Doğrulanacak TEK dosya: yolu · hangi doğrulayıcı · çıktıdaki etiketi."""

    path: Path
    kind: str    # 'schema' | 'enum' | 'openapi'
    label: str   # "Validating <yol><label>..."


#: Hangi `kind` hangi doğrulayıcıya gider. `main()` bu tabloyu kullanır — ikinci bir
#: `if/elif` zinciri yazmak, ÖD-13'ün düzelttiği "ayna" hatasının küçük hâli olurdu.
_VALIDATORS: Dict[str, Any] = {
    'schema': validate_json_schema,
    'enum': validate_enum_file,
    'openapi': validate_openapi_pii,
}


def validation_targets(base_dir: Path) -> List[Target]:
    """Kapının FİİLEN taradığı dosyalar — **`main()` BU listeyi kullanır.**

    ⚠️ 2026-08-11 · ÖD-13'ün kendi hatası düzeltildi: bu fonksiyonun docstring'i
    *"main() bu listeyi kullanır"* diyordu ama **KULLANMIYORDU** — `main()` aynı dört
    ağacı kendi `rglob` döngüleriyle yeniden geziyordu. Yani `tests/test_publication_
    tree_gates.py` **aynayı** ölçüyordu, `main()`'i değil. Mutasyonla kanıtlandı
    (taze klon, master): `main()`'den `dist` bloğu silindiğinde doğrulanan dosya
    **165 → 97** düştü ve ÖD-13 kapısı **17 passed** ile YEŞİL kaldı; tüm süit de
    yeşildi. Kapı, koruduğunu iddia ettiği davranışı hiç ölçmüyordu.

    Artık **tek kaynak**: `main()` yalnız bu listeyi dolaşır, doğrulayıcıyı
    `_VALIDATORS[kind]` tablosundan seçer. `tests/test_publication_tree_gates.py`
    hem listeyi hem de *"main gerçekten bunu kullanıyor mu"* sorusunu ölçer.
    """
    targets: List[Target] = []
    targets.extend(
        Target(path, 'schema', '') for path in sorted((base_dir / 'schemas').rglob('*.json'))
    )
    enums_dir = base_dir / 'enums'
    if enums_dir.exists():
        targets.extend(
            Target(path, 'enum', '') for path in sorted(enums_dir.rglob('*.json'))
        )
    # ÖD-13: YAYIN AĞACI. `dist/schemas/` hava-boşluklu M1'in tükettiği biçimdir (harici
    # `$ref` yok) ve bir zamanlar HİÇBİR kapıdan geçmiyordu: ne validate, ne PII taraması,
    # ne checksum. Bayatlık ayrı bir kapının işidir (`inline_refs.py --check`); burada
    # İÇERİK kuralları koşar.
    dist_dir = base_dir / 'dist' / 'schemas'
    if dist_dir.exists():
        targets.extend(
            Target(path, 'schema', ' (yayın ağacı)') for path in sorted(dist_dir.rglob('*.json'))
        )
    # D18/K4: `api/` ağacı önceden HİÇBİR PII kapısından geçmiyordu.
    api_dir = base_dir / 'api'
    if api_dir.exists():
        targets.extend(
            Target(path, 'openapi', ' (PII scope)') for path in sorted(api_dir.rglob('*.yaml'))
        )
    return targets


def validate_drone_registry_sync(base_dir: Path) -> List[str]:
    """`drone_type` enum ↔ `drone_registry.yaml` ↔ `drone_capability_matrix.yaml`.

    ⚠️ 2026-08-11: bu kural **YAZILIYDI ama KOŞMUYORDU**. Kanonik enum'un kendi
    üstverisi kapıyı ADIYLA çağırıyordu —
        `enums/drone_type.enum.v1.json → x-registry-sync.ci_check`
        = *"tools/validate.py — drone_type enum değerleri drone_registry.yaml ile eşleşmeli"*
    — ama `tools/validate.py` içinde `drone_registry` geçen **sıfır satır** vardı ve
    hiçbir test dosyayı okumuyordu (2 isabetin ikisi de prose). `SDLC_GATES.md` de
    üç ayrı yerde (§56/§88/§133) kapı olarak listeliyordu. Yani kanonik dosya,
    var olmayan bir kapıya atıfla kendini garantiliyordu.

    Veri o gün hizalıydı (5/5/5, sıfır fark) — yani eksik olan **kural değil KAPIYDI**.
    Bu fonksiyon iddiayı DOĞRU hâle getirir.
    """
    errors: List[str] = []
    enum_path = base_dir / 'enums' / 'drone_type.enum.v1.json'
    registry_path = base_dir / 'drone_registry.yaml'
    matrix_path = base_dir / 'drone_capability_matrix.yaml'
    if not enum_path.exists():
        return [f"{enum_path.name} yok — drone senkron kapısı KOŞAMAZ (fail-closed)."]

    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        # Sessiz atlama yeşil sayılmaz (D4/Q2 dersi).
        return [
            "pyyaml kurulu değil — drone_type ↔ drone_registry senkron kapısı KOŞMADI. "
            "requirements-dev.txt'i kurun."
        ]

    def _keys(document: Any, section: str) -> set:
        node = document.get(section) if isinstance(document, dict) else None
        if isinstance(node, dict):
            return set(node)
        if isinstance(node, list):
            found = set()
            for item in node:
                if isinstance(item, dict):
                    for key in ('drone_type', 'type', 'code', 'id', 'model'):
                        if key in item:
                            found.add(item[key])
                            break
            return found
        return set()

    enum_values = set(json.loads(enum_path.read_text(encoding='utf-8')).get('enum', []))
    for path, section, label in (
        (registry_path, 'drones', 'drone_registry.yaml'),
        (matrix_path, 'capabilities', 'drone_capability_matrix.yaml'),
    ):
        if not path.exists():
            errors.append(f"{label} yok — drone senkron kapısı koşamaz (fail-closed).")
            continue
        keys = _keys(yaml.safe_load(path.read_text(encoding='utf-8')), section)
        eksik = sorted(enum_values - keys)
        fazla = sorted(keys - enum_values)
        if eksik:
            errors.append(
                f"drone_type enum'unda VAR, {label} içinde YOK: {eksik}. "
                "Yeni model akışı: registry → capability matrix → enum (enum SON adımdır)."
            )
        if fazla:
            errors.append(
                f"{label} içinde VAR, drone_type enum'unda YOK: {fazla}. "
                "Kayıtlı ama enum'a girmemiş model, sözleşmede kullanılamaz."
            )
    return errors


def cross_file_checks(base_dir: Path) -> List[str]:
    """Tek dosyaya sığmayan (çapraz-dosya) kurallar — `main()` bunu DA koşar.

    `validation_targets()` dosya BAŞINA çalışan kuralları taşır; buradakiler iki ya da
    daha fazla dosyanın BİRLİKTE tutması gereken değişmezlerdir.
    """
    return validate_drone_registry_sync(base_dir)


def main() -> None:
    """Main validation"""
    # Windows consoles default to a legacy code page (e.g. cp1254) that cannot
    # encode the status emoji below and raises UnicodeEncodeError. Force UTF-8.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")

    print("🔍 TarlaAnaliz Contracts Validator\n")

    base_dir = Path(__file__).parent.parent

    all_errors = []
    total_files = 0

    # TEK KAYNAK: kapsam `validation_targets()`'ta tanımlıdır, burada YENİDEN yazılmaz.
    # Eskiden burada dört ayrı `rglob` döngüsü vardı ve kapı o listeyi değil aynasını
    # ölçüyordu (bkz. `validation_targets` docstring'indeki mutasyon kanıtı).
    for target in validation_targets(base_dir):
        total_files += 1
        print(f"Validating {target.path.relative_to(base_dir)}{target.label}...")
        all_errors.extend(_VALIDATORS[target.kind](target.path))

    # Çapraz-dosya değişmezleri (dosya başına koşmayan kurallar).
    print("Checking cross-file invariants (drone_type ↔ registry ↔ capability matrix)...")
    all_errors.extend(cross_file_checks(base_dir))

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
