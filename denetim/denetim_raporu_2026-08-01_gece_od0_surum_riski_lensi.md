# ÖD-0 — `sürüm-riski` lensi (denetim borcu KAPANDI)

**Tarih:** 2026-08-01 gece · **Yöntem:** elle ölçüm, çok-ajanlı tur **açılmadı** (kullanıcı
istemedikçe ajan turu açılmıyor) · **Kapsam:** `v7.3.0` → çalışma ağacı, C8 töreni (v7.4.0)
öncesi · **Tetik:** §14.9 *"Denetim borcu — C8'den ÖNCE"*.

> Kanıt arşivi. Açık işler yalnız `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` §14.9'da.

---

## 0. Lensin sorduğu 9 soru ve cevapları

| # | Soru | Cevap |
|---|---|---|
| 1 | Yayımlanacak içerik ↔ CHANGELOG örtüşüyor mu? | ⚠️ **Kalemler tam, ama 3 cümle bayattı** → düzeltildi (§1) |
| 2 | Migration guide gerekiyor mu? | ✅ **Hayır** — MINOR; politika (`versioning_policy.md:253`) yalnız breaking'te şart koşuyor |
| 3 | MINOR kararı doğru mu? (iki bağımsız ölçüm) | ✅ **Evet** — dedektör 9/0 · bağımsız düzleştirilmiş tarama 89 dosya / 0 (§2) |
| 4 | I-2 etiket hijyeni tutuyor mu? | ✅ **22 sürüm / 22 annotated tag**, `git describe` = `v7.3.0-28-g…` (temiz biçim) |
| 5 | Yayımlanan sürümün notları olduğunu ölçen kapı var mı? | 🔴 **YOKTU** → kapı yazıldı, 2/2 mutasyon (§3) |
| 6 | Re-pin penceresinde üretici/tüketici uyuşmazlığı doğar mı? | ✅ **Hayır** — yeni alanların **canlı üreticisi yok** (§4) |
| 7 | Aktif deprecation'ların penceresi doldu mu? | ⚠️ **Doldu** — v8.0.0 içeriğine girmeli (§5) |
| 8 | Dedektörün *"manual review required"* dediği değişiklik incelendi mi? | ✅ **Evet** — `x-normalization`, gerekçesi CHANGELOG'da yazılı (§6) |
| 9 | Sürümün etkilediği tüketici zinciri sağlam mı? | 🔴 **İki gerçek bulgu** — E18 · P19 (+ W15 küçük) (§7) |

---

## 1. CHANGELOG: kalemler tam, üç cümle turun ORTASINI anlatıyordu

Dedektörün bulduğu **9 değişikliğin 9'u da** `[Unreleased]` bölümünde adıyla anılıyor
(`RGB`/S7 · `PANEL_ABSOLUTE`/C6b-S2 · `reflectance_scale`/S6 · `analysis_job $defs` ×2/ÖD-2 ·
`x-normalization` · `calibration_method`/S4 · `scale`/S5 · `x-context-subsets`/ÖD-1). ✅

**Ama üç cümle turun ortasında donmuştu** ve C8 onları `[7.4.0]` başlığı altında
**yayımlayacaktı** — yani sürüm notları, sürümün kendisiyle çelişecekti:

| Bayat cümle | Gerçek |
|---|---|
| `PENDING_PROPAGATION` listesinde *"worker `analysis_job` `$defs/CalibrationMetadata`"* | **W13 aynı turda kapattı**; beyan `527c174`'te silindi → açık beyan **2** |
| *"`KNOWN_VENDORED_AHEAD`, 4 dosya / 5 pointer / 16 değer"* | **E16 iki girişi sildi** → **2 dosya / 3 pointer / 6 değer** |
| *"edge `worker_result` ve `intake_manifest.sorties[]` crop sözlüğü **küçük harf**"* | **E16 kapandı** — edge sınırda `strip().upper()` normalize ediyor (PR #50) |

Ek olarak turun **son üç kararı** (W13 kapanışı · W14 eksen farkı · SD11) CHANGELOG'da hiç
yoktu. Üçü de eklendi. ⇒ *Aynı sınıf, öz-denetimdeki Ö4/Ö5/Ö6 ile birebir: karar uygulandı,
çevresindeki metin eski dünyayı anlatmaya devam etti.* Fark: **burası yayımlanan yüzey.**

---

## 2. MINOR kararı — ikinci ölçüm dedektörden BAĞIMSIZ yazıldı

`tools/breaking_change_detector.py --old v7.3.0 --new .` → **9 değişiklik / 0 breaking**.

İkinci ölçüm dedektörün kodunu **hiç kullanmadan** yapıldı: `v7.3.0` ağacı `git show` ile
okundu, her JSON **düzleştirildi** (`$defs` · `items` · `oneOf/allOf/anyOf` · liste indeksleri
dâhil) ve yalnız breaking sınıfları arandı — alan silme · `required` ekleme · enum değeri
kaldırma · `type` değişimi · kapanan `additionalProperties`/`unevaluatedProperties`.

**Sonuç: 89 dosya karşılaştırıldı, 0 bulgu.** İki bağımsız ölçüm aynı şeyi söylüyor ⇒ MINOR.

**Aracın kendisi de ölçüldü** (kapsamı ölçülmeyen kapı, olmayan kapıdır) — üç mutasyon,
üçü de **iç içe** yollara yerleştirildi:

| Mutasyon | Yakalandı mı |
|---|---|
| `analysis_job → $defs/CalibrationMetadata/…/calibration_type` enum'undan `NONE` silindi | ✅ |
| `analysis_result → $defs/Detection/required`'a alan eklendi | ✅ |
| `field.v1 → properties/name/type` `string`→`integer` | ✅ |

---

## 3. 🔴 Yayın kapısı boşluğu — sürüm notları "Unreleased" etiketiyle yayımlanabilirdi

`pin_version.py` **yalnız `CONTRACTS_VERSION.md`'yi** yazar. `CHANGELOG.md`'deki
`## [Unreleased]` başlığını `## [7.4.0] - <tarih>` yapmak **elle** bir adımdır ve
**hiçbir kapı ölçmüyordu** — unutulsa tüm kapılar yeşil kalır, sürüm notları
"Unreleased" etiketiyle donardı. Asimetri ölçüldü: **worker** deposunun CI'ında CHANGELOG
kapısı **var**, SSOT deposunda **yoktu**.

Kapı yazıldı (`tests/test_pin_version.py`, `release_gate` işaretli — C8 öncesi deselect
edilemez):

* `test_changelog_has_a_section_for_the_pinned_version` — `CONTRACTS_VERSION.md`'deki sürüm
  için `## [X.Y.Z]` bölümü olmalı. Sürüm kanonik okuyucudan alınır (`read_contracts_version`),
  yeni regex yazılmadı (D16 dersi).
* `test_pinned_version_section_is_not_empty` — başlık atmak yetmez, gövde ≥200 karakter
  (ÖD-12'nin dersi: kapı **başlık** sayarsa gövde silinince yeşil kalır).

| Mutasyon | Beklenen | Ölçülen |
|---|---|---|
| `CONTRACTS_VERSION` 7.3.0→7.4.0, CHANGELOG'a dokunma | kırmızı | ✅ **2 FAILED** |
| `[7.3.0]` başlığı dursun, **gövdesi** silinsin | yalnız gövde kapısı kırmızı | ✅ **1 FAILED** (başlık kapısı yeşil kaldı → ikisi bağımsız) |

---

## 4. Re-pin penceresi — bu turda risk YOK (ölçüldü)

Tehlike deseni: contract etiketlenir, üç depo **sırayla** re-pin edilir; arada bir üretici
yeni alanı yazmaya başlarsa, henüz re-pin edilmemiş tüketici (`unevaluatedProperties: false`)
**geçerli belgeyi reddeder** — S5 ve ÖD-2 tam bu delikten düşmüştü.

Ölçüm (`src/` ağaçları, `__pycache__` hariç):

| Yeni yüzey | platform | edge | worker |
|---|---|---|---|
| `calibration_method` yazan | **0** | **0** | 0 (yalnız yanlış bir docstring — §7c) |
| `reflectance_scale` yazan | **0** | **0** | 13 (**okuyan** taraf, W12) |
| `PANEL_ABSOLUTE` kalibre manifeste yazan | — | **0** (3 eşleşme de **yorum**) | — |
| `raw_frames[].band = "RGB"` yazan | — | **0** (eşleşmeler PIL `Image.new("RGB")` ve doküman) | — |

⇒ Yeni alanların **hiçbirinin canlı üreticisi yok**; pencere bu turda güvenli. *(Bu, S4
beyanının gerekçesini de tazeler: `calibration_method`'u okuyan kod hâlâ yok.)*

---

## 5. ⚠️ Aktif deprecation'lar — pencere doldu, MAJOR turunun içeriğine girmeli

| Nesne | Beyan | Durum |
|---|---|---|
| `schemas/platform/payment_intent.v1.schema.json` | `"deprecated": true`, v2 kanonik, migration guide yazılı | v2 yayımlandı; tüketiciler v2'ye pinli |
| `enums/payment_status.enum.v1.json` | `x-deprecated.since: "6.2.0"`, `removal_plan: "Gelecek bir MAJOR sürümde kaldırılabilir"` | **6.2.0'dan beri** — arada 7.0/7.1/7.2/7.3 var, minimum pencere fazlasıyla doldu |

Beyanlar düzgün yazılmış (silinme planı **var**), ama v8.0.0 içerik listesinde (S3 · S7-b · K1)
**yoklar**. Eklendi.

---

## 6. `x-normalization` — dedektörün "manual review" bayrağı kapatıldı

Dedektör: *"Normative annotation changed: `x-normalization` at `<root>` in
`worker/calibration_metadata.v1` — validation is unaffected but CONSUMER BEHAVIOUR may be."*

İnceleme **yapılmış ve yazılı**: `x-normalization.scale.missing = DECLARED_FALLBACK`;
CHANGELOG'da neden bilerek **fail-open** olduğu (bugün hiçbir üretici `scale` yazmıyor, sert
kapı filoyu durdururdu) ve sapmanın **geçici** olduğu (I-5 — üretici E14 alanı yazmaya
başlayınca `FAIL_CLOSED`'a çevrilir) kayıtlı. ✅ Ek işlem gerekmiyor.

---

## 7. 🔴 Tüketici zinciri — lensin asıl yakaladığı iki bulgu

### (a) E18 — edge sessizce yutuyor ve gerekçesi P14 ile ÇÜRÜDÜ

`tarlaanaliz-edge/src/core/services/pipeline/calibration_pipeline.py`

```python
def _read_calibration_type(calibrated_manifest_path: Path) -> str | None:
    try:
        data = json.loads(calibrated_manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None            # <-- her okuma/ayrıştırma hatası SESSİZ
```

`_with_calibration_type` bunu alır ve `None` ise manifesti **alan eklemeden** döndürür.
Üç yerde gerekçesi yazılı ve **üçü de artık yanlış**:

* `calibration_pipeline.py:450-451` — *"Backward compatible: … platform keeps its safety-net."*
* `calibration_pipeline.py:282` — *"otherwise the platform falls back to its PANEL_ABSOLUTE assumption"*
* `batch/manifest_writer.py:224` — *"Opsiyonel/geriye uyumlu: yoksa platform CALIBRATED→PANEL_ABSOLUTE varsayar."*

**O güvenlik ağı 2026-08-01'de P14 ile KALDIRILDI** (platform PR #351; doğrulandı:
`worker_job_publisher.py` 3. adım artık `return "NONE"` ve docstring'i kaldırmayı
ölçümüyle anlatıyor).

**Bugünkü zincir:** okunamayan/bozuk kalibre manifest → edge sessizce alanı **atlar** →
platform tipi türetemez → **`NONE`** → worker KR-018/082 **sert kapısı işi reddeder**.
Operatör *"radyometrik kalibrasyon reddedildi"* görür; **gerçek sebep** edge istasyonunda
okunamayan bir dosyadır. Sessizlik P14'ten önce *yükseltme* (tehlikeli), sonra *ret*
(güvenli ama **teşhis edilemez**) anlamına geliyor.

⇒ **E15'in tıpatıp kardeşi** (`qc_report_writer`: `except → 0.0` sessiz yolu). Sınıf aynı:
*fail-loud yerine sessiz varsayılan*. Aynı turda çözülmeli. Yorumlar da düzeltilmeli —
`manifest_writer.py:224` tam da alanın atlanmasına karar veren `if` satırının üstünde
duruyor ve **yanlış değişmezi öğretiyor**.

### (b) P19 — platform'un "3 adımlı" türetmesi fiilen 2 adım; ortadaki ölü

`worker_job_publisher.py::_derive_calibration_type` üç kaynak sayıyor:
1. edge `Dataset.manifest.calibration_type` · 2. `CalibrationRecord.calibration_manifest`
açık tipi · 3. fail-closed `NONE`.

Ölçüldü: **2. adımı besleyen kod yok.** `calibration_manifest` alanına `src/`, `tests/`,
`scripts/`, `alembic/` içinde **hiçbir yerde** değer atanmıyor — yalnız repository onu
DB'den okuyup geri yazıyor (kolon `nullable=True`, hep NULL). ⇒ Gerçek zincir **tek
kaynak + fail-closed**'dır; docstring okuyan biri var olmayan bir yedeklilik sanır. Bu,
(a)'nın etkisini de büyütür: tek kaynak sessizce kaybolunca yakalayacak ikinci kaynak yok.

### (c) W15 (küçük) — worker docstring'i okumadığı alanı okuduğunu söylüyor

`worker/src/preprocessing/radiometric/calibration_input_parser.py:3` →
*"Reads calibration_method from Producer output"*. Fonksiyon `parse_calibration_level`
aslında **`calibration_type`** okur. Önemi: §14.9 S4 beyanı *"okuyan kod yok — ya okuma kodu
yazılır ya gerekçe tazelenir"* diyor; bir sonraki oturum `calibration_method` diye grep atınca
**bu satırı** bulur ve "okuyucu var" diye yanlış sonuca varır. (Ayrıca `_CALIBRATION_MAP`
kanonik olmayan `"PANEL"`/`"DLS2"`/küçük harf anahtarları kabul ediyor; şema doğrulaması
önce koştuğu için bugün ölü esneklik, delik değil.)

---

## 8. Denetimin kendi sınırı

* Çok-ajanlı lens turu **açılmadı**; bu tur elle koşturuldu. ÖD-0'ın *"ajan turunun ne
  bulacağı bilinmiyor"* kalemi bu raporla **kapanmıştır** — soru listesi yazıldı, dokuzu da
  ölçüldü ve ikisi gerçek bulgu verdi.
* Kapsam **sürüm riski**dir: güvenlik, performans ve ML/DL eksenleri bu lensin dışında.
* (a)/(b)/(c) kardeş depolarda; bu turda **ölçüldü ve yazıldı**, düzeltmeleri kendi
  depolarının kalemleri (E18 · P19 · W15).
