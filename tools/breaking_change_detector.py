#!/usr/bin/env python3
"""
TarlaAnaliz Breaking Change Detector

Detects breaking changes between two versions of JSON Schema contracts.
Generates machine-readable report and PR comment format.

Usage:
    python3 tools/breaking_change_detector.py --old v1.0.0 --new v1.1.0
    python3 tools/breaking_change_detector.py --pr-comment

KAPSAM — 2026-07-31 (KADEME 0 / D3) ile ÖZYİNELEMELİ hâle getirildi
--------------------------------------------------------------------
Karşılaştırma artık şema ağacının HER düğümünde yapılır. Her düğümde
enum / const / type / required / properties / pattern / min-max eksenleri
karşılaştırılır; alt şemalara şu anahtarlardan inilir:

    harita : properties, patternProperties, $defs, definitions, dependentSchemas
    tekil  : items, contains, if, then, else, not, propertyNames,
             additionalProperties, unevaluatedProperties,
             additionalItems, unevaluatedItems
    liste  : allOf, anyOf, oneOf, prefixItems   (indekse göre eşlenir)

Ayrıca `x-context-subsets` (bağlam-bazlı KABUL listeleri; bkz.
`enums/calibration_type.enum.v1.json`) enum ekseniyle aynı kuralla karşılaştırılır:
bir bağlamdan değer düşmesi o bağlam için MAJOR'dır.

NEDEN (ölçüm, 2026-07-31 10-disiplin denetimi — SD1/SD2/Y5):
    `schemas/worker/expert_review_queue.v1.schema.json` içindeki
    `properties.escalation_reason.enum`'dan `QUARANTINE_CAUTION` silindi (= MAJOR
    breaking) ve araç **"Breaking Changes: 0"** dedi. Eski sürüm yalnız KÖK düzeyindeki
    `enum` ve `properties` sözlüğünü okuyordu; `$defs`, `items`, `oneOf/allOf/if-then`
    altındaki her şey görünmezdi. O turun 17 semantik değişikliğinin yalnız 4'ü görülmüştü.
    Kural: "Yeşil ama yalan bir kapı, kırmızı bir kapıdan tehlikelidir."

BEYANLI DARALTMA — `x-compat-accepted` (2026-07-31, D7 ile eklendi)
--------------------------------------------------------------------
Kısıt/desen/enum EKLEMEK biçimsel olarak breaking'dir, ama bazen gerçek dünyada
kimseyi kırmaz (tipik: alanın ÖLÇÜLMÜŞ biçimde hiç üreticisi yoktur). Böyle bir
değişiklik ya sürümü gereksiz MAJOR'a çeker ya da ekip kapıyı görmezden gelmeye
başlar — ikisi de kapıyı öldürür. Bu yüzden istisna **sessiz değil beyanlıdır**:

    "observed_footprint_wkt": {
      "maxLength": 4096,
      "x-compat-accepted": {"change": "...", "date": "...", "rationale": "...", "ref": "..."}
    }

Dedektör o düğümdeki daraltmayı NON_BREAKING'e indirir ama **gerekçeyi raporda
yankılar** (PR yorumunda görünür kalır). Kapsam bilerek dar: yalnız
`MIN_MAX_TIGHTENED`, `PATTERN_TIGHTENED`, `ENUM_CONSTRAINT_ADDED` indirilebilir.
**Alan silme · enum DEĞERİ silme · `required` genişletme · tip daraltma ASLA indirilemez.**

BİLİNEN SINIRLAR (bilerek — kapı bunları GÖRDÜĞÜNÜ iddia etmez):
    * `$ref` **çözülmez**. `$ref` hedefi değişirse `REF_CHANGED` olarak raporlanır
      (NON_BREAKING) ama sınıflandırılmaz — insan incelemesi gerekir (SDLC_GATES §3E).
    * `description` farkları yalnız KÖK düzeyde raporlanır (aksi hâlde her tur binlerce
      DOCUMENTATION satırı üretirdi).
    * Desen (`pattern`) değişikliği daraltma/genişletme ayrımı yapılmadan BREAKING
      sayılır (karar verilemez problem; muhafazakâr taraf seçildi).

ÇIKIŞ KODLARI:
    0 = breaking yok · 1 = breaking var · 2 = ARACIN KENDİSİ ÇALIŞAMADI
    (okunamayan/bozuk şema, beklenmeyen hata). 2, CI'da "kapı bozuk" demektir ve
    "breaking yok" ile karıştırılmamalıdır.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum

#: Depo kökü — `--old v7.2.0` gibi bir git ref verildiğinde worktree buradan çıkarılır.
ROOT = Path(__file__).resolve().parents[1]


class ChangeType(Enum):
    """Types of schema changes"""
    # Breaking changes (require MAJOR version bump)
    FIELD_REMOVED = "FIELD_REMOVED"
    FIELD_TYPE_CHANGED = "FIELD_TYPE_CHANGED"
    FIELD_MADE_REQUIRED = "FIELD_MADE_REQUIRED"
    ENUM_VALUE_REMOVED = "ENUM_VALUE_REMOVED"
    ENUM_CONSTRAINT_ADDED = "ENUM_CONSTRAINT_ADDED"
    CONST_CHANGED = "CONST_CHANGED"
    CONTEXT_SUBSET_VALUE_REMOVED = "CONTEXT_SUBSET_VALUE_REMOVED"
    COMPOSITION_BRANCH_CHANGED = "COMPOSITION_BRANCH_CHANGED"
    SCHEMA_REMOVED = "SCHEMA_REMOVED"
    ARRAY_ITEMS_CHANGED = "ARRAY_ITEMS_CHANGED"
    MIN_MAX_TIGHTENED = "MIN_MAX_TIGHTENED"
    PATTERN_TIGHTENED = "PATTERN_TIGHTENED"

    # Non-breaking changes (allow MINOR version bump)
    FIELD_ADDED_OPTIONAL = "FIELD_ADDED_OPTIONAL"
    ENUM_VALUE_ADDED = "ENUM_VALUE_ADDED"
    CONTEXT_SUBSET_VALUE_ADDED = "CONTEXT_SUBSET_VALUE_ADDED"
    TYPE_WIDENED = "TYPE_WIDENED"
    REF_CHANGED = "REF_CHANGED"
    NORMATIVE_ANNOTATION_CHANGED = "NORMATIVE_ANNOTATION_CHANGED"
    SCHEMA_ADDED = "SCHEMA_ADDED"
    DESCRIPTION_CHANGED = "DESCRIPTION_CHANGED"
    MIN_MAX_RELAXED = "MIN_MAX_RELAXED"
    PATTERN_RELAXED = "PATTERN_RELAXED"

    # Documentation only (allow PATCH version bump)
    EXAMPLE_CHANGED = "EXAMPLE_CHANGED"
    NOTES_CHANGED = "NOTES_CHANGED"


# --- Draft 2020-12 alt-şema taşıyan anahtarlar ------------------------------
# Değeri TEK bir alt şema olanlar
SUBSCHEMA_SINGLE: Tuple[str, ...] = (
    "items", "contains", "if", "then", "else", "not", "propertyNames",
    "additionalProperties", "unevaluatedProperties",
    "additionalItems", "unevaluatedItems",
)
# Değeri {ad: alt şema} haritası olanlar
SUBSCHEMA_MAPS: Tuple[str, ...] = (
    "properties", "patternProperties", "$defs", "definitions", "dependentSchemas",
)
# Değeri alt şema LİSTESİ olanlar (indekse göre eşlenir)
SUBSCHEMA_LISTS: Tuple[str, ...] = ("allOf", "anyOf", "oneOf", "prefixItems")

# Bileşim (composition) anahtarlarında hangi yön kırıcıdır:
#   allOf/prefixItems  → dal EKLEMEK kısıt ekler   ⇒ breaking
#   anyOf/oneOf        → dal ÇIKARMAK seçenek siler ⇒ breaking
COMPOSITION_BREAKING_ON: Dict[str, str] = {
    "allOf": "added",
    "prefixItems": "added",
    "anyOf": "removed",
    "oneOf": "removed",
}

# --- Beyanlı daraltma (accepted tightening) ---------------------------------
# Bir DARALTMA (kısıt/desen/enum EKLEME) biçimsel olarak breaking'dir; ama bazen
# gerçek dünyada kimseyi kırmaz — tipik örnek: alanın HİÇ ÜRETİCİSİ yoktur
# (ölçülmüş), yalnız tüketicileri vardır. Böyle bir değişiklik ya sürümü gereksiz
# MAJOR'a çeker ya da ekip kapıyı görmezden gelmeye başlar; ikisi de kapıyı öldürür.
#
# Çözüm: SESSİZ istisna değil, BEYANLI istisna. İlgili düğüme `x-compat-accepted`
# konur; dedektör o düğümdeki daraltmayı NON_BREAKING'e indirir ama gerekçeyi
# RAPORDA yankılar (PR yorumunda görünür, incelenebilir kalır).
#
# ⚠️ Kapsam bilerek DAR: yalnız aşağıdaki sınıflar indirilebilir. Alan silme,
# enum DEĞERİ silme, `required` genişletme ve tip daraltma ASLA indirilemez.
# Tüketicinin KOD olarak uyguladığı `x-` blokları. Şema doğrulamasını değiştirmezler,
# davranışı değiştirirler → sessiz kalamazlar (bkz. _compare_normative_annotations).
# `x-updated` bilerek YOK: her turda değişir, sinyal değil gürültü üretir.
NORMATIVE_ANNOTATION_KEYS: Tuple[str, ...] = (
    "x-normalization",
    "x-layer-classes",
    "x-form-role",
    "x-derived-from",
    "x-preliminary-content",
)

ACCEPTANCE_KEY = "x-compat-accepted"
ACCEPTABLE_TYPES = frozenset({
    ChangeType.MIN_MAX_TIGHTENED.value,
    ChangeType.PATTERN_TIGHTENED.value,
    ChangeType.ENUM_CONSTRAINT_ADDED.value,
    ChangeType.COMPOSITION_BRANCH_CHANGED.value,
})
#: Beyan bu alanları taşımak ZORUNDA (boş kaşe olmasın diye; tests ile zorlanır).
ACCEPTANCE_REQUIRED_FIELDS = ("change", "date", "rationale", "ref")


class BreakingChangeDetector:
    """Detects breaking changes in JSON Schema"""
    
    def __init__(self, old_dir: Path, new_dir: Path):
        self.old_dir = old_dir
        self.new_dir = new_dir
        self.changes: List[Dict[str, Any]] = []
        # Okunamayan dosyalar SESSİZ geçilemez: okunamayan bir şema "değişiklik yok"
        # gibi görünür ve kapı yalan söyler. main() bu sayaç >0 iken exit 2 verir.
        self.load_errors: List[str] = []

    def load_schema(self, path: Path) -> Dict:
        """Load JSON Schema file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load {path}: {e}")
            self.load_errors.append(f"{path}: {e}")
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
        
        # ÖZYİNELEMELİ karşılaştırma — kök düğümden başlar, tüm alt şemalara iner.
        self.compare_node(old_schema, new_schema, schema_path, "")

        # Check description changes (documentation only) — YALNIZ kök düzeyde;
        # her düğümde raporlansaydı gürültü sinyali bastırırdı.
        if old_schema.get('description') != new_schema.get('description'):
            self.changes.append({
                'type': ChangeType.DESCRIPTION_CHANGED.value,
                'severity': 'DOCUMENTATION',
                'file': schema_path,
                'message': f"Description updated in {schema_path}"
            })

    # ------------------------------------------------------------------ #
    # Özyinelemeli çekirdek (D3)                                          #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _loc(pointer: str, field: str = "") -> str:
        """İnsan-okunur konum: `properties.escalation_reason.enum` gibi."""
        parts = [p for p in (pointer, field) if p]
        return ".".join(parts) if parts else "<root>"

    @staticmethod
    def _type_set(node: Dict) -> Optional[Set[str]]:
        """`type` değerini kümeye çevir (dize veya dizi olabilir)."""
        raw = node.get('type')
        if raw is None:
            return None
        if isinstance(raw, str):
            return {raw}
        if isinstance(raw, list):
            return {t for t in raw if isinstance(t, str)}
        return None

    @staticmethod
    def _value_key(value: Any) -> str:
        """Hashlenemeyen enum değerleri (dict/list) için kararlı anahtar."""
        if isinstance(value, (str, int, float, bool)) or value is None:
            return json.dumps(value, sort_keys=True, ensure_ascii=False)
        return json.dumps(value, sort_keys=True, ensure_ascii=False)

    def compare_node(self, old_node: Any, new_node: Any, schema_path: str, pointer: str) -> None:
        """Bir şema düğümünü karşılaştır ve TÜM alt şemalara in.

        `pointer` düğümün kök'e göre yolu (`properties.escalation_reason` gibi);
        mesajlarda konum olarak kullanılır.
        """
        if not isinstance(old_node, dict) or not isinstance(new_node, dict):
            return

        loc = self._loc(pointer)

        self._compare_value_list(
            old_node.get('enum'), new_node.get('enum'), schema_path, loc,
            ChangeType.ENUM_VALUE_REMOVED, ChangeType.ENUM_VALUE_ADDED, "Enum value",
        )
        self._compare_enum_constraint_added(old_node, new_node, schema_path, loc)
        self._compare_context_subsets(old_node, new_node, schema_path, loc)
        self._compare_normative_annotations(old_node, new_node, schema_path, loc)
        self._compare_const(old_node, new_node, schema_path, loc)
        self._compare_type(old_node, new_node, schema_path, loc)
        self._compare_pattern(old_node, new_node, schema_path, loc)
        self.check_constraint_changes(old_node, new_node, schema_path, loc)
        self._compare_ref(old_node, new_node, schema_path, loc)
        self._compare_properties_and_required(old_node, new_node, schema_path, pointer)
        self._recurse(old_node, new_node, schema_path, pointer)

    def _recurse(self, old_node: Dict, new_node: Dict, schema_path: str, pointer: str) -> None:
        """Alt şema taşıyan tüm anahtarlara in (yalnız İKİ tarafta da var olanlara).

        Yalnız kesişime inilir: yeni eklenen bir alt şemanın iç kısıtları eski veriyi
        kırmaz (o alan zaten yoktu) — aksi hâlde her yeni alan sahte breaking üretirdi.
        """
        for key in SUBSCHEMA_SINGLE:
            if isinstance(old_node.get(key), dict) and isinstance(new_node.get(key), dict):
                self.compare_node(old_node[key], new_node[key], schema_path,
                                  self._loc(pointer, key))

        for key in SUBSCHEMA_MAPS:
            old_map, new_map = old_node.get(key), new_node.get(key)
            if not isinstance(old_map, dict) or not isinstance(new_map, dict):
                continue
            # `properties` add/remove ayrıca _compare_properties_and_required'da raporlanır;
            # burada yalnız ORTAK olanların İÇİNE iniyoruz.
            for name in set(old_map) & set(new_map):
                self.compare_node(old_map[name], new_map[name], schema_path,
                                  self._loc(pointer, f"{key}.{name}"))

        for key in SUBSCHEMA_LISTS:
            old_list, new_list = old_node.get(key), new_node.get(key)
            if not isinstance(old_list, list) or not isinstance(new_list, list):
                # HİÇ YOKKEN bileşim kısıtı EKLEMEK de bir daraltmadır ve eski sürümde
                # sessizdi: iki tarafta da liste şartı arandığı için `allOf` yokken
                # eklenmesi HİÇ raporlanmıyordu (2026-07-31/KADEME 3'te ölçüldü —
                # expert_review_queue'ya 5 blok eklendi, dedektör "0 değişiklik" dedi).
                if isinstance(new_list, list) and old_list is None:
                    self._record({
                        'type': ChangeType.COMPOSITION_BRANCH_CHANGED.value,
                        'severity': 'BREAKING',
                        'file': schema_path,
                        'field': self._loc(pointer, key),
                        'old_count': 0,
                        'new_count': len(new_list),
                        'message': (
                            f"Composition constraint added: {self._loc(pointer, key)} did not "
                            f"exist, now has {len(new_list)} branch(es) in {schema_path}"
                        ),
                    }, new_node)
                continue
            self._compare_composition_arity(key, old_list, new_list, schema_path, pointer)
            for index in range(min(len(old_list), len(new_list))):
                self.compare_node(old_list[index], new_list[index], schema_path,
                                  self._loc(pointer, f"{key}[{index}]"))

    def _compare_composition_arity(self, key: str, old_list: List, new_list: List,
                                   schema_path: str, pointer: str) -> None:
        """`allOf/anyOf/oneOf/prefixItems` dal SAYISI değişimi."""
        if len(old_list) == len(new_list):
            return
        grew = len(new_list) > len(old_list)
        direction = 'added' if grew else 'removed'
        breaking = COMPOSITION_BREAKING_ON.get(key) == direction
        self.changes.append({
            'type': ChangeType.COMPOSITION_BRANCH_CHANGED.value,
            'severity': 'BREAKING' if breaking else 'NON_BREAKING',
            'file': schema_path,
            'field': self._loc(pointer, key),
            'old_count': len(old_list),
            'new_count': len(new_list),
            'message': (
                f"Composition branch {direction}: {self._loc(pointer, key)} "
                f"{len(old_list)} -> {len(new_list)} in {schema_path}"
            ),
        })

    def _compare_value_list(self, old_values: Any, new_values: Any, schema_path: str,
                            loc: str, removed_type: ChangeType, added_type: ChangeType,
                            label: str) -> None:
        """Kabul listesi (enum / bağlam alt kümesi) karşılaştırması."""
        if not isinstance(old_values, list) or not isinstance(new_values, list):
            return
        old_map = {self._value_key(v): v for v in old_values}
        new_map = {self._value_key(v): v for v in new_values}
        if not old_map and not new_map:
            return

        for key in old_map.keys() - new_map.keys():
            self.changes.append({
                'type': removed_type.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'field': loc,
                'value': old_map[key],
                'message': f"{label} removed: {old_map[key]} at {loc} in {schema_path}",
            })
        for key in new_map.keys() - old_map.keys():
            self.changes.append({
                'type': added_type.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'field': loc,
                'value': new_map[key],
                'message': f"{label} added: {new_map[key]} at {loc} in {schema_path}",
            })

    # -- beyanlı daraltma ------------------------------------------------- #

    @staticmethod
    def _acceptance(node: Dict) -> Optional[Dict]:
        """Düğümdeki `x-compat-accepted` beyanı (varsa)."""
        declaration = node.get(ACCEPTANCE_KEY)
        return declaration if isinstance(declaration, dict) else None

    def _record(self, change: Dict[str, Any], new_node: Dict) -> None:
        """Değişikliği kaydet; beyanlı DARALTMA ise NON_BREAKING'e indir.

        İndirme SESSİZ DEĞİLDİR: gerekçe mesaja yazılır ve raporda görünür.
        """
        declaration = self._acceptance(new_node)
        if (
            declaration is not None
            and change['severity'] == 'BREAKING'
            and change['type'] in ACCEPTABLE_TYPES
        ):
            change = dict(change)
            change['severity'] = 'NON_BREAKING'
            change['accepted'] = declaration
            change['message'] = (
                f"ACCEPTED TIGHTENING (declared): {change['message']} "
                f"| gerekçe: {declaration.get('rationale', '<gerekçe yok>')} "
                f"| ref: {declaration.get('ref', '<ref yok>')}"
            )
        self.changes.append(change)

    def _compare_enum_constraint_added(self, old_node: Dict, new_node: Dict,
                                       schema_path: str, loc: str) -> None:
        """Serbest bir alana SONRADAN `enum` koymak daraltmadır.

        Eski değer listesi karşılaştırması iki tarafta da `enum` şartı koştuğu için
        bu sınıfı HİÇ görmüyordu: `{"type":"string"}` → `{"type":"string","enum":[...]}`
        değişikliği sessizce geçiyordu (ör. `qc_report.flags[]` kapalı vocabulary'ye
        çevrilirken).
        """
        if 'enum' in old_node or not isinstance(new_node.get('enum'), list):
            return
        self._record({
            'type': ChangeType.ENUM_CONSTRAINT_ADDED.value,
            'severity': 'BREAKING',
            'file': schema_path,
            'field': loc,
            'new_values': new_node['enum'],
            'message': (
                f"Enum constraint added: {loc} was unconstrained, now limited to "
                f"{new_node['enum']} in {schema_path}"
            ),
        }, new_node)

    def _compare_context_subsets(self, old_node: Dict, new_node: Dict,
                                 schema_path: str, loc: str) -> None:
        """`x-context-subsets` — bağlam-bazlı KABUL listeleri (enum ile aynı ağırlık).

        Bir bağlamdan değer düşerse o bağlamdaki üreticiler kırılır; şema `enum`'u
        değişmediği için klasik enum karşılaştırması bunu göremez
        (bkz. `enums/calibration_type.enum.v1.json`).
        """
        old_subsets = old_node.get('x-context-subsets')
        new_subsets = new_node.get('x-context-subsets')
        if not isinstance(old_subsets, dict) or not isinstance(new_subsets, dict):
            return
        for context in set(old_subsets) & set(new_subsets):
            self._compare_value_list(
                old_subsets[context], new_subsets[context], schema_path,
                self._loc(loc if loc != "<root>" else "", f"x-context-subsets.{context}"),
                ChangeType.CONTEXT_SUBSET_VALUE_REMOVED,
                ChangeType.CONTEXT_SUBSET_VALUE_ADDED,
                "Context-subset value",
            )
        for context in set(old_subsets) - set(new_subsets):
            if isinstance(old_subsets[context], list):
                self.changes.append({
                    'type': ChangeType.CONTEXT_SUBSET_VALUE_REMOVED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': f"x-context-subsets.{context}",
                    'message': (
                        f"Context subset removed: {context} in {schema_path} "
                        "(that context loses its declared vocabulary)"
                    ),
                })
        for context in set(new_subsets) - set(old_subsets):
            if isinstance(new_subsets[context], list):
                self.changes.append({
                    'type': ChangeType.CONTEXT_SUBSET_VALUE_ADDED.value,
                    'severity': 'NON_BREAKING',
                    'file': schema_path,
                    'field': f"x-context-subsets.{context}",
                    'message': (
                        f"Context subset added: {context} = {new_subsets[context]} "
                        f"in {schema_path}"
                    ),
                })

    def _compare_normative_annotations(self, old_node: Dict, new_node: Dict,
                                       schema_path: str, loc: str) -> None:
        """Doğrulamayı değiştirmeyen ama DAVRANIŞI belirleyen `x-` bloklarını görünür kıl.

        Bu depoda bazı `x-` blokları normatiftir: tüketiciler onları KOD olarak uygular.
        Örnek (2026-07-31/D8): `calibration_type.enum` → `x-normalization` bloğundaki
        *"eksikse PANEL_ABSOLUTE varsay"* kuralı platform kodunda birebir uygulanıyordu
        (`worker_job_publisher.py:80-84`). Bu kuralın fail-open'dan FAIL-CLOSED'a çevrilmesi
        hiçbir belgeyi/şemayı 'geçersiz' yapmaz — yani klasik şema diff'i onu HİÇ GÖRMEZ,
        ama tüketicinin davranışını değiştirmesi ZORUNLUDUR.

        Bu yüzden bu bloklar NON_BREAKING olarak ama **"manual review required"** damgasıyla
        raporlanır. `x-updated` gibi tarih alanları bilerek KAPSAM DIŞIDIR (gürültü).
        """
        for key in NORMATIVE_ANNOTATION_KEYS:
            old_value, new_value = old_node.get(key), new_node.get(key)
            if old_value == new_value or (old_value is None and new_value is None):
                continue
            self.changes.append({
                'type': ChangeType.NORMATIVE_ANNOTATION_CHANGED.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'field': self._loc(loc if loc != "<root>" else "", key),
                'message': (
                    f"Normative annotation changed: {key} at {loc} in {schema_path} "
                    "— validation is unaffected but CONSUMER BEHAVIOUR may be; manual review required"
                ),
            })

    def _compare_const(self, old_node: Dict, new_node: Dict, schema_path: str, loc: str) -> None:
        if 'const' not in old_node and 'const' not in new_node:
            return
        if old_node.get('const') == new_node.get('const'):
            return
        self.changes.append({
            'type': ChangeType.CONST_CHANGED.value,
            'severity': 'BREAKING',
            'file': schema_path,
            'field': loc,
            'old_value': old_node.get('const'),
            'new_value': new_node.get('const'),
            'message': (
                f"Const changed: {loc} {old_node.get('const')!r} -> "
                f"{new_node.get('const')!r} in {schema_path}"
            ),
        })

    def _compare_type(self, old_node: Dict, new_node: Dict, schema_path: str, loc: str) -> None:
        """Tip kümesi DARALMASI kırıcıdır; genişleme (`["string","null"]`) değildir."""
        old_types, new_types = self._type_set(old_node), self._type_set(new_node)
        if not old_types or not new_types or old_types == new_types:
            return
        dropped = old_types - new_types
        if dropped:
            self.changes.append({
                'type': ChangeType.FIELD_TYPE_CHANGED.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'field': loc,
                'old_type': sorted(old_types),
                'new_type': sorted(new_types),
                'message': (
                    f"Type changed: {loc} from {sorted(old_types)} to {sorted(new_types)} "
                    f"in {schema_path}"
                ),
            })
        else:
            self.changes.append({
                'type': ChangeType.TYPE_WIDENED.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'field': loc,
                'message': (
                    f"Type widened: {loc} {sorted(old_types)} -> {sorted(new_types)} "
                    f"in {schema_path}"
                ),
            })

    def _compare_pattern(self, old_node: Dict, new_node: Dict, schema_path: str, loc: str) -> None:
        """Desen değişimi/eklenmesi — daraltma/genişletme ayrımı KARAR VERİLEMEZ,
        muhafazakâr taraf seçilir (BREAKING)."""
        old_pattern, new_pattern = old_node.get('pattern'), new_node.get('pattern')
        if new_pattern is None or old_pattern == new_pattern:
            return
        self._record({
            'type': ChangeType.PATTERN_TIGHTENED.value,
            'severity': 'BREAKING',
            'file': schema_path,
            'field': loc,
            'old_pattern': old_pattern,
            'new_pattern': new_pattern,
            'message': (
                f"Pattern {'added' if old_pattern is None else 'changed'}: {loc} in "
                f"{schema_path} (potentially breaking)"
            ),
        }, new_node)

    def _compare_ref(self, old_node: Dict, new_node: Dict, schema_path: str, loc: str) -> None:
        """`$ref` hedefi değişimi — ÇÖZÜLMEZ, yalnız görünür kılınır (bilinen sınır)."""
        old_ref, new_ref = old_node.get('$ref'), new_node.get('$ref')
        if old_ref == new_ref or (old_ref is None and new_ref is None):
            return
        self.changes.append({
            'type': ChangeType.REF_CHANGED.value,
            'severity': 'NON_BREAKING',
            'file': schema_path,
            'field': loc,
            'old_ref': old_ref,
            'new_ref': new_ref,
            'message': (
                f"$ref retargeted: {loc} {old_ref} -> {new_ref} in {schema_path} "
                "(NOT resolved by this tool — manual review required)"
            ),
        })

    def _compare_properties_and_required(self, old_node: Dict, new_node: Dict,
                                         schema_path: str, pointer: str) -> None:
        """Bu düğümdeki `properties` ekleme/silme + `required` genişlemesi."""
        old_props = old_node.get('properties')
        new_props = new_node.get('properties')
        old_props = old_props if isinstance(old_props, dict) else {}
        new_props = new_props if isinstance(new_props, dict) else {}

        old_required = set(old_node.get('required', []) or [])
        new_required = set(new_node.get('required', []) or [])

        if not old_props and not new_props and old_required == new_required:
            return

        for field in sorted(set(old_props) - set(new_props)):
            self.changes.append({
                'type': ChangeType.FIELD_REMOVED.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'field': self._loc(pointer, field),
                'message': f"Field removed: {self._loc(pointer, field)} in {schema_path}",
            })

        added_required = new_required - old_required
        for field in sorted(added_required):
            if field in new_props and field not in old_props:
                detail = "New required field added"
            else:
                # `field in old_props` VE `required`da olmayan alanlar burada;
                # `properties`de hiç tanımlı olmayan required alanlar da (eski sürüm
                # bunları SESSİZ atlıyordu) buraya düşer.
                detail = "Field made required"
            self.changes.append({
                'type': ChangeType.FIELD_MADE_REQUIRED.value,
                'severity': 'BREAKING',
                'file': schema_path,
                'field': self._loc(pointer, field),
                'message': f"{detail}: {self._loc(pointer, field)} in {schema_path}",
            })

        for field in sorted(set(new_props) - set(old_props) - added_required):
            self.changes.append({
                'type': ChangeType.FIELD_ADDED_OPTIONAL.value,
                'severity': 'NON_BREAKING',
                'file': schema_path,
                'field': self._loc(pointer, field),
                'message': f"Optional field added: {self._loc(pointer, field)} in {schema_path}",
            })

    def check_constraint_changes(self, old_prop: Dict, new_prop: Dict, schema_path: str, field: str):
        """Check for constraint changes (min/max, minLength/maxLength, etc.)

        Kısıtın SONRADAN EKLENMESİ de daraltmadır (eski sürüm yalnız iki tarafta da
        var olan kısıtları karşılaştırıyordu; `maxLength` eklemek görünmezdi).
        """

        constraints = [
            ('minimum', 'increased'),
            ('exclusiveMinimum', 'increased'),
            ('maximum', 'decreased'),
            ('exclusiveMaximum', 'decreased'),
            ('minLength', 'increased'),
            ('maxLength', 'decreased'),
            ('minItems', 'increased'),
            ('maxItems', 'decreased'),
            ('minProperties', 'increased'),
            ('maxProperties', 'decreased'),
        ]

        for constraint, direction in constraints:
            old_val = old_prop.get(constraint)
            new_val = new_prop.get(constraint)

            if new_val is None or not isinstance(new_val, (int, float)):
                continue

            if old_val is None:
                self._record({
                    'type': ChangeType.MIN_MAX_TIGHTENED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': field,
                    'constraint': constraint,
                    'old_value': None,
                    'new_value': new_val,
                    'message': (
                        f"Constraint added: {field}.{constraint} = {new_val} in {schema_path}"
                    ),
                }, new_prop)
                continue

            if not isinstance(old_val, (int, float)):
                continue

            tightened = (direction == 'increased' and new_val > old_val) or \
                        (direction == 'decreased' and new_val < old_val)
            if tightened:
                self._record({
                    'type': ChangeType.MIN_MAX_TIGHTENED.value,
                    'severity': 'BREAKING',
                    'file': schema_path,
                    'field': field,
                    'constraint': constraint,
                    'old_value': old_val,
                    'new_value': new_val,
                    'message': (
                        f"Constraint tightened: {field}.{constraint} {direction} from "
                        f"{old_val} to {new_val} in {schema_path}"
                    ),
                }, new_prop)
            elif new_val != old_val:
                self.changes.append({
                    'type': ChangeType.MIN_MAX_RELAXED.value,
                    'severity': 'NON_BREAKING',
                    'file': schema_path,
                    'field': field,
                    'constraint': constraint,
                    'old_value': old_val,
                    'new_value': new_val,
                    'message': (
                        f"Constraint relaxed: {field}.{constraint} from {old_val} to "
                        f"{new_val} in {schema_path}"
                    ),
                })

    def compare_enums(self, old_schema: Dict, new_schema: Dict, schema_path: str):
        """Kök düzeyi enum karşılaştırması (geriye uyumluluk kabuğu).

        Özyinelemeli yol `compare_node` üzerindedir; bu metot dış çağrıcılar için durur.
        """
        self._compare_value_list(
            old_schema.get('enum'), new_schema.get('enum'), schema_path, "<root>",
            ChangeType.ENUM_VALUE_REMOVED, ChangeType.ENUM_VALUE_ADDED, "Enum value",
        )

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
    # Windows konsolu (cp1254) UTF-8 olmayan çıktıda çöker — `tools/validate.py` ile
    # aynı kalıcı düzeltme (2026-07-05). Bu satır olmadan araç Windows'ta HİÇ koşmuyordu
    # ve SDLC_GATES §1C "detector çalıştırıldı" maddesi uygulanamıyordu.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description='Detect breaking changes in TarlaAnaliz contracts'
    )
    
    parser.add_argument('--old', required=True, help='Old version directory or tag')
    parser.add_argument('--new', default='.', help='New version directory (default: current)')
    parser.add_argument('--pr-comment', action='store_true', help='Output PR comment format')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    
    args = parser.parse_args()

    cleanups: list = []
    try:
        old_dir = _materialize(args.old, cleanups)
        new_dir = _materialize(args.new, cleanups)
        return _run(args, old_dir, new_dir)
    finally:
        for cleanup in cleanups:
            cleanup()


def _materialize(target: str, cleanups: list) -> Path:
    """Dizin ya da **git ref** kabul et; ref ise geçici bir worktree'ye çıkar.

    ÖD-16 (2026-08-01): aracın kendi kullanım satırı `--old v1.0.0 --new v1.1.0` diyordu
    ve CHANGELOG bu biçimi **yayımlıyordu** (`--old v7.2.0 --new .`), ama kod yalnız
    dizin kabul ediyordu → yayımlanan komut `❌ Old directory not found: v7.2.0` ile
    düşüyordu. Bu, deponun kendi *"sayıyı değil ÜRETECİ yayınla"* kuralının ihlaliydi:
    yayımlanan üreteç koşmuyorsa, yanındaki sayı da doğrulanamaz.
    """
    path = Path(target)
    if path.exists():
        return path

    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{target}^{{commit}}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if resolved.returncode != 0:
        print(f"❌ Not a directory and not a git ref: {target}", file=sys.stderr)
        sys.exit(1)

    workdir = Path(tempfile.mkdtemp(prefix="bcd-"))
    checkout = workdir / "tree"
    added = subprocess.run(
        ["git", "worktree", "add", "--detach", str(checkout), resolved.stdout.strip()],
        cwd=ROOT, capture_output=True, text=True,
    )
    if added.returncode != 0:
        shutil.rmtree(workdir, ignore_errors=True)
        print(f"❌ git worktree add failed for {target}: {added.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    def cleanup() -> None:
        subprocess.run(["git", "worktree", "remove", "--force", str(checkout)],
                       cwd=ROOT, capture_output=True, text=True)
        shutil.rmtree(workdir, ignore_errors=True)
        # `remove` başarısız olsa bile (ör. dosya kilidi) yönetim kaydı geride kalmasın:
        # ölçüldü — kayıt kalırsa `git worktree list` çıktısı "prunable" satırlarla dolar
        # ve bir sonraki oturum bunu gerçek bir worktree sanar.
        subprocess.run(["git", "worktree", "prune"], cwd=ROOT, capture_output=True, text=True)

    cleanups.append(cleanup)
    print(f"   {target} → geçici worktree: {checkout}", file=sys.stderr)
    return checkout


def _run(args, old_dir: Path, new_dir: Path):
    if not new_dir.exists():
        print(f"❌ New directory not found: {new_dir}")
        sys.exit(1)

    # Detect changes across the checksummed contract trees: schemas/ AND enums/.
    # The canonical enum SSOT (crop_type, phenology_stage, analysis_type, ...)
    # lives at top-level enums/; enum value removals/renames are MAJOR breaking
    # and must not be invisible to the detector.
    #
    # ⚠️ İLERLEME METNİ **stderr**'e gider. 2026-07-31'de ölçüldü: bu üç satır stdout'a
    # basıldığı için CI'ın `--json > breaking_changes.json` çıktısı geçersiz JSON oluyordu;
    # `json.load` patlıyor, CI'daki `if` bloğu else dalına düşüp **has_breaking=false**
    # yazıyordu. Yani kapı, `continue-on-error` olmasa bile DAİMA "breaking yok" derdi.
    print("🔍 Comparing contracts (schemas/ + enums/)...", file=sys.stderr)
    print(f"   Old: {old_dir}", file=sys.stderr)
    print(f"   New: {new_dir}\n", file=sys.stderr)

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

    # Okunamayan şema = kapı KÖR. "breaking yok" ile karıştırılmamalı → exit 2.
    if detector.load_errors:
        for err in detector.load_errors:
            print(f"❌ Unreadable schema (gate is blind): {err}", file=sys.stderr)
        sys.exit(2)

    # Exit code
    if categorized_changes['has_breaking']:
        sys.exit(1)  # Breaking changes detected
    else:
        sys.exit(0)  # No breaking changes


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 — kapı sessizce ölmemeli
        print(f"❌ breaking_change_detector crashed: {exc}", file=sys.stderr)
        sys.exit(2)