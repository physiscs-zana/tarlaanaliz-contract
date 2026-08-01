# E13-R · ÖD-4 · ÖD-5 · ÖD-6 · ÖD-7 — ölçüm ve kapı kanıtı (2026-08-01, ikinci oturum)

> ⚠️ **BU DOSYA BİR İŞ LİSTESİ DEĞİLDİR.** Kanıt arşividir. Yapılacak işlerin tek kaynağı
> `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` **§14.8**'dir.

---

## 1. ÖD-5 → **E13-R**: karar geri alındı (koordinatör onayı)

### 1.1 Ölçüm — üç kanonik kaynak da E13'ün tersini söylüyordu

| # | Kaynak | Hüküm |
|---|---|---|
| 1 | `drone_capability_matrix.yaml:9-21` | `DJI_MAVIC_3M` → `calibration_class: relative` · notu: *"Pix4Dfields göreli kalibrasyon sağlar"* |
| 2 | `docs/TARLAANALIZ_SSOT_v1_2_0.txt:79` | *"⚠️ DJI Mavic 3M Radyometri Notu (KR-018 ile birlikte okuyun): Pix4Dfields, M3M için 'tam radyometrik kalibrasyon değil, göreli (relative) kalibrasyon' sağlar…"* |
| 3 | aynı dosya `:1014` | *"Pix4Dfields ile M3M için üretilen kalibrasyon **görelidir (relative)**… Mutlak radyometrik tutarlılık gerektiren kullanım durumlarında…"* |
| 4 | platform `src/core/domain/value_objects/calibration_class.py:41` | `"DJI_MAVIC_3M": CalibrationClass.RELATIVE` — ve `:63-66` `RELATIVE → 2.0×` tolerans gevşemesi |

**SSOT'un iddia edilen iç çelişkisi ölçüldü ve YUMUŞAK çıktı:** `:457` (*"Pix4Dfields ile
tam radyometrik kalibrasyon"*) M1 istasyonunun **genel akış** tarifidir ve tüm markaları
kapsayan bir listenin (`:77-78`) altındadır; `:79`/`:1014` ise **M3M'e özgü istisnadır**.
Yani "aynı cümlenin iki değeri" değil, "genel kural + özel istisna". Yine de `:457`'nin
niteliksiz ifadesi imprecise — ayrı kalem olarak §14.8'e yazıldı (SSOT metni çapraz-repo
bayt-özdeş olduğu için düzeltmesi 3 depoya senkron ister).

### 1.2 Neden kritik — sonucun ölçülen zinciri

`src/core/domain/enums.py:73` (worker):

```python
FINETUNE_ALLOWED_CALIBRATIONS = frozenset({ABSOLUTE, PANEL_ABSOLUTE, DLS2_RELATIVE})
SSL_ALLOWED_CALIBRATIONS      = FINETUNE_ALLOWED_CALIBRATIONS | {RELATIVE}
```

⇒ E13'ün filo-geneli `ABSOLUTE` kararı uygulansaydı (E14 yazıcısı geldiğinde), **göreli
kalibre edilmiş M3M verisi ince ayara girecekti** — K-3'ün *"fine-tuning: SADECE
PANEL+DLS2"* kuralı, kuralın kendisi değişmeden, **etiket üzerinden** delinirdi. Ayrıca
platformun göreli sınıfa ayırdığı 2.0× tolerans devreye girmez, zaman serisi
karşılaştırmaları SSOT `:1014`'ün açıkça reddettiği bir varsayıma otururdu.

### 1.3 Karar ve bedeli

**E13-R:** değer `capabilities[drone_type].calibration_class`'tan türetilir
(`relative→RELATIVE` · `absolute→ABSOLUTE|PANEL_ABSOLUTE`). Kural **makine-okunur**:
`enums/calibration_type.enum.v1.json → x-derivation`.

💰 **Kabul edilen bedel (kararın gövdesinde yazılı):** demo/pilot filosu M3M olduğu için
M3M verisi ince ayara girmez, yalnız SSL ön-eğitimine girer. Alternatifi göreli veriyi
mutlak etiketle eğitime sokmaktı.

✅ **E13'ün ayakta kalan yarısı:** `DLS2_RELATIVE` reddi (satıcı adı + eksen karışıklığı).

### 1.4 Kapı kanıtı — **8/8 mutasyon kırmızı**

| # | Mutasyon | Düşen test |
|---|---|---|
| M1 | Göreli sınıf `ABSOLUTE` üretir (**E13'ün geri alınan hâli**) | `test_relative_class_cannot_produce_an_absolute_label` |
| M2 | `x-derivation` bloğu silinir | 10 test birden (kural makine-okunur kaynağını kaybeder) |
| M3 | Matriste M3M → `absolute` | `test_fleet_primary_drone_is_still_relative` |
| M4 | `RELATIVE` kalibre alt-kümeden çıkarılır | `test_mapped_values_are_writable_on_the_calibrated_surface` |
| M5 | Geri alma kaydından `cost_accepted` silinir | `test_reversal_is_recorded_with_its_cost` |
| M6′ | Matristen `calibration_class` satırları silinir | `test_every_drone_declares_a_calibration_class` |
| M7 | Türetme `DLS2_RELATIVE` üretir | `test_dls2_rejection_survives_the_reversal` (+ yazılabilirlik) |
| M8 | `edge` tüketici yükümlülüğü silinir | `test_obligation_exists[edge]` |

> 🔴 **Yöntem notu — uygulanmamış mutasyon YEŞİL verir ve kapıyı kör sandırır.** M6 ilk
> denemede yeşil döndü; sebep kapı değil **mutasyon script'iydi**: matris dosyası CRLF
> satır sonu kullanıyor, desen `\n` ile yazılmıştı ve **hiç eşleşmedi** (dosya
> değişmemişti). M6′ satır-bazlı silmeye çevrildi ve *"mutasyon gerçekten uygulandı mı"*
> kontrolü script'e eklendi. Ders: mutasyon doğrulamasında **önce mutasyonun uygulandığını
> ölç**, sonra kırmızıyı yorumla.

---

## 2. ÖD-4 — vendored kopyalar yayımlanmış `v7.3.0`'ın önünde mi?

Yöntem: 16 vendored dosya `git show v7.3.0:<kanonik yol>` içeriğiyle karşılaştırıldı
(çalışma ağacı değil **etiket**).

| Bulgu | Sınıf | Karşılık |
|---|---|---|
| worker `calibration_metadata.v1` ← `scale` | geçici, **beyanı eksikti** | worker `denetim/scale_wire_devir_spec_2026_08_01.md` (bu turda yazıldı) |
| worker `analysis_job.v1` ← `scale` + `calibration_method` | geçici, bu turda oluştu | aynı devir spesi (W13) |
| worker `expert_labeling_card.v1` ← `EGE` (2 pointer) | **gerçek borç** | **W14** |
| worker `expert_review_queue.v1` ← `APPLE/CHERRY/FIG/PEACH` | **gerçek borç** | **W14** |
| edge `worker_result.v1` ← küçük harf crop | **gerçek borç** | **E16** |
| edge `intake_manifest`/`scan_report`/`transfer_batch` "üst düzey alan fazlası" | ⚠️ **YANLIŞ POZİTİF** | kanonik `oneOf[$defs]`, vendored **düz** — yapı farkı; yeni parite kapısı SUBSET kipinde doğru sayıyor |

---

## 3. ÖD-6 — platform fail-open canlı mı?

**Canlı.** `tarlaanaliz-platform/src/infrastructure/messaging/worker_job_publisher.py:80-84`:

```python
# 3. status CALIBRATED → PANEL_ABSOLUTE (güvenlik-ağı).
if status_val == "CALIBRATED":
    return "PANEL_ABSOLUTE"
```

Aynı fonksiyonun 4. adımı zaten `NONE` üretiyor (fail-closed yolu mevcut). **P14** kalemiyle
birleştirildi. 🔴 **E13-R bu kalemi acilleştirdi:** M3M paketleri artık `RELATIVE` taşıyacak;
tipi boş gelen bir pakette `PANEL_ABSOLUTE` yükseltmesi, göreli veriyi mutlak etiketle
worker'a gönderen **tek kalan yol** hâline geliyor.

*(Yan ölçüm: aynı dosyanın `:38` yorumu hâlâ "platform contract 6.1.0'e PİN'lidir" diyor —
gerçek pin `7.3.0`. ÖD-14 sınıfının bir üyesi; plana yazıldı.)*

---

## 4. ÖD-7 — SD8 nüfusu eksik ölçülmüştü

**Ölçüm biçimden bağımsız yapıldı:** `CONTRACTS_VERSION.md`'nin her commit'indeki blob
okundu ve başlıktaki sürüm `^#{0,2}\s*\**Version:\**\s*v?X.Y.Z` deseniyle çıkarıldı.

| | Sayı |
|---|---|
| Başlıkta görülen sürüm | **22** |
| Etiketli | 19 |
| **Etiketsiz** | **3** → `2.0.1` · `2.1.0` · `4.1.2` |
| Etiketi olup başlıkta hiç görülmeyen | 0 |

**Neden SD8 kaçırdı:** SD8 sabit `## Version: X.Y.Z` biçimini arıyordu; bu üç sürüm dosyaya
**farklı biçimde** yazılmıştı. Aynı ders D2'de KR başlık çıkarıcısında öğrenilmişti
(*"her başlık düzeyi + 4 biçim"*) — sabit biçim varsayımı ikinci kez nüfus kaybettirdi.

**Yöntem doğrulaması (SD8'in 4/4'ünden güçlü):** ölçüm **19/19** etiketli sürümde mevcut
tag'in commit'ini birebir verdi. Sonra üç annotated retro-tag atıldı ve push'landı:

```
v2.0.1  f77f62d8  (2026-03-06)  audit(contracts): deep SSOT v1.2.0 compliance
v2.1.0  6b802fd8  (2026-03-29)  feat: KR-088..091 veri katmanı genişleme
v4.1.2  fb021e3e  (2026-06-23)  fix(contracts): denetim bulguları — 4.1.2 bump
```

⇒ **I-2 artık 22/22 tutuyor.** Tek kayıtlı istisna `2.0.2` (CONTRACTS_VERSION.md'ye hiç
yazılmadı → release commit'i ölçülemez; `docs/versioning_policy.md` §Release'de kayıtlı).

---

## 5. Kapı durumu

| Ölçüm | Sonuç |
|---|---|
| Dedektör (`origin/master` ↔ çalışma ağacı) | **0 değişiklik / 0 breaking** (yalnız `x-` açıklama bloğu + test) |
| `pytest tests/` | **1186 passed · 0 skipped · 2 beyanlı xfail** |
| `tools/validate.py` | 96 dosya / 0 hata |
| `tools/inline_refs.py --check` | ✅ güncel |
| E13-R mutasyonları | **8/8 kırmızı** |
