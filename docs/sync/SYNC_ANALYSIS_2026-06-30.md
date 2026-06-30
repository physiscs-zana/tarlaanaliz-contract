# Contract ↔ Worker / Platform / Edge — %100 Senkronizasyon Derin Analizi

**Tarih:** 2026-06-30
**Kanonik kaynak (SSOT):** `tarlaanaliz-contract` @ `2535de2` = **v4.2.1** (SHA-256 `614d41d2…`)
**Kapsam:** `schemas/`, `enums/`, `api/` + her tüketicinin yerel kopyaları
**Mod:** Auto (otonom analiz). **Hiçbir şema dosyası değiştirilmedi** — gerekçe §6.

---

## 1. Yönetici Özeti — Senkronizasyon Skor Kartı

| Tüketici | Bağlanma yöntemi | Pin | Kanonik | Byte-aynı? | Drift sınıfı |
|---|---|---|---|---|---|
| **Platform** | git **submodule** (`contracts/`) | `99ecf06` = **4.1.1** | 4.2.1 | Pin içinde 1:1 | **Sürüm gecikmesi** (1 minor geride) — crop_type BREAKING |
| **Worker** | elle kopya (`interface/contracts/`, 7 dosya) | yerel **v5.1.1** | 4.2.1 (`schemas/worker/`, 8 dosya) | 0/7 | **Kasıtlı overlay + sözlük farkı** |
| **Edge** | elle kopya (`interface/contracts/schemas/edge/`, 8 dosya) | yerel **v1.2.0** | 4.2.1 (`schemas/edge/`, 14 dosya) | 0/8 | **Yapısal soğurma (oneOf) + $id host** |

**Ana sonuç:** Hiçbir tüketici contract 4.2.1 ile byte düzeyinde senkron değil. Ancak driftlerin
çoğunluğu **kasıtlı ve belgeli** (overlay, GAP-8 sözlük kararı, oneOf superset). Gerçekten
"yanlışlıkla sapmış" ve güvenle düzeltilebilecek kalem **azdır** (Edge `$id` host + Platform
pin tazeleme). crop_type birleştirmesi **ortak tasarım kararı** gerektirir (B4 Faz 1/2 / AK-4).

---

## 2. Topoloji

```
                tarlaanaliz-contract  (SSOT, 4.2.1, HEAD 2535de2)
                 ├── schemas/worker/*  (8)  ──┐
                 ├── schemas/edge/*    (14) ──┤ kanonik
                 ├── enums/*           (21) ──┘
                 │
   ┌─────────────┼──────────────────────────────┐
   │             │                              │
 PLATFORM      WORKER                          EDGE
 submodule     elle kopya                      elle kopya
 contracts/    interface/contracts/*.json (7)  interface/contracts/schemas/edge/*.json (8)
 @99ecf06      KR-041 kendi hash şeması        verify_contracts_hashes.py kendi hash
 (=4.1.1)      (byte-concat, LF-norm)          (LF-norm SHA-256)
```

- **Platform** kanonik ağacı submodule olarak *aynen* taşır → kopya-drift imkânsız; tek fark **hangi commit'e pinli** olduğu.
- **Worker & Edge** şemaları elle tutar → hem sürüm hem içerik driftine açık. Her ikisi de kendi bağımsız KR-041 hash kapısıyla *kendi* kopyalarını kilitler (SSOT checksum'ından bağımsız).

---

## 3. Sistematik (çapraz-kesen) Drift Kalıpları

Bunlar **15 tüketici dosyasının tamamında** görülür ve tek tek değil toplu ele alınmalıdır.

### P1 — `additionalProperties:false` (tüketici) ⟷ `unevaluatedProperties:false` (kanonik)
- Worker 7/7 + Edge 8/8 dosya `additionalProperties:false` kullanıyor; **0** dosya `unevaluatedProperties` kullanıyor.
- Kanonik kural (contract CLAUDE.md §1): tüm `object` tiplerinde `unevaluatedProperties:false` zorunlu (22 kanonik worker+edge dosyası uyumlu).
- **Anlamsal fark:** `$ref`/`allOf`/`oneOf` kompozisyonu varlığında `additionalProperties:false` *daha katı*tır (kompozisyonla gelen alanları reddeder). Tüketiciler şemalarını **düzleştirdiği** (kompozisyon yok) için yerelde sorun çıkmaz; fakat kanonik kompozisyonlu şema birebir kopyalanırsa `additionalProperties:false`'a çevrilince geçerli payload'ları yanlış reddedebilir. Bu yüzden iki repo aynı dosyada farklı anahtar kullanır.

### P2 — Kanonik `oneOf` superset ⟷ tüketici düz (flat) şema
- Edge `intake_manifest`, `scan_report`, `transfer_batch`: kanonik `$defs.EdgeForm / AbstractForm / OperationalForm / BatchLevelForm / ChunkedForm` + `oneOf` superset kullanır (edge=üretici ↔ platform=tüketici kontrat boşluğunu kapatmak için). Edge'in elindeki kopya ise **tek düz form** (sadece üst düzey `properties`).
- Sonuç: Edge'in ürettiği örnek, kanonik oneOf'un **bir dalı** olarak geçerlidir (anlamsal uyum korunur) ama **şema dosyaları yapısal olarak farklıdır** (byte-aynı asla olmaz).

---

## 4. Tüketici Bazında Detaylı Bulgular

### 4.A PLATFORM (submodule pin gecikmesi)

`git diff 99ecf06..2535de2` (4.1.1 → 4.2.1) — platform'un *kaçırdığı* kanonik değişiklikler:

| Dosya | Değişiklik | Etki |
|---|---|---|
| `enums/crop_type.enum.v1.json` | **14-set → 8-set** | 🔴 **BREAKING** |
| `enums/calibration_type.enum.v1.json` | **YENİ enum** (4.2.1'de eklendi) | 🟡 eksik |
| `enums/phenology_stage.enum.v1.json` | değişti (43 satır) | 🟡 |
| `enums/payment_method.enum.v1.json` | değişti | 🟢 minor |
| `schemas/worker/*` (6 dosya) | analysis_job/result, calibrated_dataset, calibration_metadata, expert_labeling_card, expert_review_queue | 🟡 |
| `schemas/edge/intake_manifest, calibrated_dataset_manifest` | değişti | 🟡 |
| `schemas/events/dataset_unquarantined.v1` | değişti | 🟡 |
| `schemas/core/phenology_flight_profile.v1` | değişti | 🟢 |

**crop_type detayı (kritik):**
- Platform-pinli 4.1.1: `[COTTON, CORN, WHEAT, SUNFLOWER, PISTACHIO, GRAPE, OLIVE, LENTIL, APPLE, PEACH, HAZELNUT, CHERRY, FIG, RICE]` (14)
- Kanonik 4.2.1: `[COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL]` (8)
- 4.2.1, 4.1.x'te benimsenen "worker-kanonik 14 bitki"yi **geri aldı** → GAP-8 (`MAIZE`/`RED_LENTIL`, HAZELNUT kaldırıldı).
- ⚠️ Platform pin'i 4.2.1'e yükseltmek platform için **breaking**tir: `CORN→MAIZE`, `LENTIL→RED_LENTIL` yeniden adlandırma + `APPLE/PEACH/HAZELNUT/CHERRY/FIG/RICE` kaldırma. Migration: `docs/migration_guides/crop_type_hazelnut_removal.md`.

> **Not:** Platform `CONTRACTS_VERSION.md` 4.1.1 diyor; submodule fiilen `chore/remove-taris-deduction` dalı `99ecf06`'da. Platform belgesi crop_type'ı "worker-kanonik 14 bitki (+RICE)" olarak tanımlıyor — bu 4.1.x dünyasıyla tutarlı, 4.2.1 ile **çelişik**.

### 4.B WORKER (kasıtlı overlay + sözlük farkı)

7/7 dosya drift; ana eksenler:

**(1) crop_type sözlüğü — KASITLI, BELGELİ (B4 Faz 1/2 / AK-4):**
- Worker: `CORN`, `LENTIL` + Ege bitkileri `APPLE/CHERRY/FIG/PEACH/RICE`
- Kanonik: `MAIZE`, `RED_LENTIL`, GAP-8
- Kanonik enum `metadata.aliases` bunu **resmen** köprüler: `MAIZE↔CORN`, `RED_LENTIL↔LENTIL`; `worker_alignment` notu "1:1 DEĞİL" der. → **Drift değil, kararlaştırılmış interop boşluğu.**

**(2) `expert_labeling_card` — `EGE` bölgesi:**
- Worker `endemic_regions` ve `tr_resistance_notes[].region` içinde `EGE` taşır; kanonikte **yok**. GAP odaklı kanonik bilinçli olarak EGE'yi dışlar. → Aynı AK-4 kararının parçası.

**(3) Overlay = worker DAHA KATI (güvenlik):** `analysis_result.$defs.Detection`
- Worker `required = [class_id, class_name, confidence, risk_level]` (15 alan)
- Kanonik `required = [confidence]` (22 alan = worker'ın superseti + `detection_id/type/class/severity/area_hectares/geometry/description`)
- Yani **kanonik alan-superseti + gevşek required**, worker **alan-altkümesi + katı required**. Worker örneği kanonikçe geçerli; kanonik-şekilli payload worker `additionalProperties:false` tarafından **reddedilir** → çift yönlü uyumlu DEĞİL (kasıtlı fail-closed profili). Bu tam olarak korunması gereken "overlay"dir.

**(4) `analysis_job` / `analysis_result` yapısal fark:** kanonik 4.2.1 "master/sibling" soyundan zengin `$defs` taşır (`AnalysisParameters`, `InputRef`, `LayerRef`, `Date`, zengin `Detection`); worker daha dar/runtime-özelleşmiş (`result_mode`, `confidence_score` required, `summary.yield_estimate`). Birleştirme **taban=kanonik + worker katı kuralları overlay** modeliyle yapılmalı (düz kopya güvenliği geriletir).

**(5) `calibration_type` iç tutarsızlığı (worker-içi):** sync doc item #3 — `analysis_job→CalibrationMetadata` `ABSOLUTE` içerir, `calibration_metadata.v1` + `calibrated_dataset.v1` içermez. Worker kendi içinde birleştirmeli; SSOT bunu kasıtlı yansıtıyor.

**Kapanan kalemler (worker artık uyumlu):**
- ✅ `$id` host: worker zaten `https://api.tarlaanaliz.com/...` (sync doc item #4 çözüldü)
- ✅ `expert_feedback.v1` ham `0x7F` DEL byte: artık yok, strict-JSON geçerli (item #5 çözüldü)

**Worker'da eksik kanonik dosya:** `thermal_analysis_result.v1.schema.json` (kanonikte var, worker'da yok — KR-084 termal pipeline; worker vendor etmiyor).

### 4.C EDGE (yapısal soğurma + $id host)

8/8 dosya drift; ama yapısı temiz:

**(1) `$id` host drifti — GERÇEK, GÜVENLE DÜZELTİLEBİLİR:**
- Edge: `https://tarlaanaliz.com/schemas/edge/...`
- Kanonik: `https://api.tarlaanaliz.com/schemas/edge/...`
- 8 dosyanın hepsinde `api.` öneki eksik. Worker bunu zaten düzeltti; edge geride. Kozmetik ama tek byte-drift kaynaklarından biri.

**(2) oneOf superset farkı (P2):** `intake_manifest`, `scan_report`, `transfer_batch` → kanonik oneOf superset, edge düz form. Anlamsal uyum korunur (edge dalı valide). Edge `CONTRACTS_VERSION.md` bunu açıkça belgeliyor.

**(3) `worker_result.crop_type` — edge DAHA KATI (overlay):**
- Edge: `enum:[corn, cotton, grape, pistachio, rice]` (lowercase)
- Kanonik: sadece `minLength` (serbest string, enum yok)
- Edge enum koyarak kanonikten katı → overlay. (Ayrıca lowercase `corn`, worker'ın UPPERCASE `CORN`'u ve kanonik `MAIZE` ile üçüncü bir varyant — sözlük birleştirmesine dahil edilmeli.)

**(4) Edge'in vendor etmediği kanonik edge şemaları (6):** `calibration_result`, `dataset_manifest`, `edge_metadata`, `qc_report`, `quarantine_event`, `verification_report`. Edge yalnız 8 operasyonel şemayı tutar; bu kasıtlı (edge `CONTRACTS_VERSION.md` "8 edge şeması" der).

---

## 5. Drift Sınıflandırması (kök neden)

| # | Bulgu | Sınıf | Aksiyon sahibi |
|---|---|---|---|
| D1 | crop_type CORN/MAIZE, LENTIL/RED_LENTIL, EGE/Ege bitkileri | **Kasıtlı / belgeli** (aliases) | Contract + Worker ortak (AK-4) |
| D2 | Worker Detection katı `required` (overlay) | **Kasıtlı güvenlik** | Korunmalı |
| D3 | Edge `worker_result.crop_type` enum (overlay) | **Kasıtlı güvenlik** | Korunmalı |
| D4 | P1: additionalProperties⟷unevaluatedProperties | **Sistematik konvansiyon farkı** | Tasarım kararı |
| D5 | P2: oneOf superset ⟷ düz form | **Kasıtlı yapısal soğurma** | Korunmalı |
| D6 | Platform pin 4.1.1 < 4.2.1 (crop_type breaking) | **Sürüm gecikmesi** | Platform (migration) |
| D7 | Platform `calibration_type` enum eksik | **Sürüm gecikmesi** | Platform (pin tazeleme) |
| D8 | **Edge `$id` host `tarlaanaliz.com`** | **Yanlışlıkla drift** | Edge (güvenli fix) |
| D9 | Worker iç `calibration_type` tutarsızlığı | **Worker-içi bug** | Worker |
| D10 | Worker `thermal_analysis_result` vendor edilmemiş | Kapsam kararı | Worker |

---

## 6. Neden Otomatik Düzeltme YAPILMADI

"100% senkronizasyon"u şemaları kanoniğe **düz kopyalayarak** sağlamak YANLIŞ olurdu:
- D2/D3 overlay'leri (katı required, edge crop enum) **güvenlik geriletir** — KR-018/fail-closed profilini bozar. Worker'ın kilitleyici testi bunu zaten koruyor.
- D1 (crop_type) kanonik enum'da `worker_alignment` + `aliases` ile **bilinçli** bırakılmış; birleştirme yönü (MAIZE mı CORN mu? overlay modeli?) **ortak tasarım kararı** gerektirir (B4 Faz 1/2 / AK-4). Tek taraflı override etmek doğru-olmayan tarafı kanonlaştırabilir.
- D6 (platform crop_type) tek yönde **breaking**; migration olmadan uygulanırsa platform DB/enum'ları kırılır.

Güvenle ve tek-yönlü uygulanabilir **tek** kalemler: **D8 (Edge `$id` host)** ve **D7/D6 (Platform submodule pin tazeleme + migration)**. Bunlar onay verilirse uygulanabilir (§7).

---

## 7. Remediation Yol Haritası

### Şimdi güvenle yapılabilir (mekanik, geri-uyumlu)
1. **D8 — Edge `$id` host:** 8 edge dosyasında `https://tarlaanaliz.com/` → `https://api.tarlaanaliz.com/`. Yerel `$ref`'ler etkilenmez; edge KR-041 hash'i yeniden hesaplanır (`scripts/verify_contracts_hashes.py --update`). *Worker bu adımı zaten yaptı.*

### Sürüm koordinasyonu gerektirir (breaking — migration ile)
2. **D6/D7 — Platform pin 4.1.1 → 4.2.1:** submodule'ü 2535de2'ye al, `crop_type` migration (`CORN→MAIZE`, `LENTIL→RED_LENTIL`, APPLE/PEACH/HAZELNUT/CHERRY/FIG/RICE kaldır), `calibration_type` enum'unu tüket. `CONTRACTS_VERSION.md` + `CONTRACTS_SHA256.txt` güncelle. Frontend (PWA) crop sözlüğü de güncellenmeli.

### Ortak tasarım kararı gerektirir (TEK BAŞINA YAPILAMAZ — AK-4 / B4 Faz 1/2)
3. **D1 — crop_type sözlük standardı:** Hangi ad kanonik (MAIZE vs CORN), Ege bitkileri (CHERRY/FIG/APPLE/PEACH) kanonik GAP setine girecek mi, lowercase/uppercase normalizasyonu. Karar sonrası `aliases` köprüsü kalkar veya resmîleşir.
4. **D2/D3/D4/D5 — overlay modeli:** "taban=kanonik + tüketici katı kuralları overlay" mekanizmasının resmîleştirilmesi (additionalProperties/unevaluatedProperties + required sıkılaştırma katmanı). Worker'ın katı profilini koruyan kilit testi referans alınmalı.

---

## 8. Doğrulama Komutları (tekrar-üretilebilirlik)

```bash
# Platform sürüm gecikmesi
git -C tarlaanaliz-contract diff --name-status 99ecf06 2535de2 -- schemas enums api

# crop_type karşılaştırma
git -C tarlaanaliz-contract show 99ecf06:enums/crop_type.enum.v1.json   # 14-set
cat tarlaanaliz-contract/enums/crop_type.enum.v1.json                   # 8-set

# Worker/Edge kopya vs kanonik (byte + yapısal)  → scratchpad/compare.py
```

**Özet sayaç:** 15/15 tüketici dosyası kanonikten farklı. Sınıf dağılımı:
kasıtlı/belgeli **5**, sürüm-gecikmesi **2**, yanlışlıkla-drift **1** (Edge $id), worker-içi-bug **1**, kapsam-kararı **1**, sistematik-konvansiyon **1** (P1, tüm dosyalara dokunur).
