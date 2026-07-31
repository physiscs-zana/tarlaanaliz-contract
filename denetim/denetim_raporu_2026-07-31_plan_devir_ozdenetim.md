# DENETİM RAPORU — Eylem Planı + Devir Notu · ÖZ-DENETİMDEN GEÇMİŞ

> ## 📐 BU DOSYA **KANIT ARŞİVİDİR — İŞ LİSTESİ DEĞİLDİR** (2026-07-31)
>
> Aşağıdaki bulguların **çözüm planları eylem planına işlendi**; yapılacak işler için
> **tek kaynak** odur. Bu dosya yalnız *"neden değişti"* sorusunun `dosya:satır` dayanağını tutar.
>
> | Ne arıyorsanız | Nereye bakın |
> |---|---|
> | **Yapılacak işler** (C/E/W/P/WEB/AL kalemleri, dalgalar) | ⭐ `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` |
> | Bu denetimin plana yansıması (D-1…D-16) | eylem planı **§9 → "2026-07-31 BAĞIMSIZ DENETİM TURU"** |
> | Depo sürümü / senkron durumu | `docs/SESSION_HANDOFF.md` §1, §3 |
> | Bir bulgunun **kanıtı** | bu dosya |
>
> **İşlenme durumu:** 19 bulgunun tamamı plana/devir notuna yansıtıldı (2026-07-31).

**Tarih:** 2026-07-31
**Kapsam:** `docs/SESSION_HANDOFF.md` · `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`
**Yöntem:** İki turlu. **Tur 1** — her iddia bugünkü koda/şemaya karşı ölçüldü (doküman değil **kod otoritatif**).
**Tur 2 (öz-denetim)** — Tur 1'in kendi bulguları tersine sınandı; 1 iddia **geri çekildi**, 1 iddianın
**şiddeti düşürüldü**, **4 yeni bulgu** çıktı.
**Depo durumu (ölçüldü):** contract `7.2.0` · `pin_version.py --verify` ✅ `5d3c204d…` · `validate.py` ✅ 89 dosya / 0 hata.

> **Dürüstlük kaydı:** Tur 1 raporu **%100 doğru değildi.** P-1'in "ölü şema" alt-iddiası yanlıştı,
> P-2'nin şiddeti abartılıydı. Aşağıdaki **düzeltilmiş küme** %100 kaynak-doğrulanmıştır;
> her satırın `dosya:satır` kanıtı vardır ve tersine sınanmıştır.

---

## 0. Öz-denetim karar tablosu

| Bulgu | Tur 1 | Tur 2 kararı |
|---|---|---|
| H-1 sürüm bayatlığı | 🔴 | ✅ **ONAYLANDI + güçlendi** (tag'ler *annotated* → I-2 tutuyor) |
| H-2 AL-C1/C2 tur çelişkisi | 🔴 | ✅ ONAYLANDI |
| H-3 devir notu 5 yeni dokümanı bilmiyor | 🟠 | ✅ ONAYLANDI |
| H-4 dal/PR tablosu tarihi | 🟢 | ✅ ONAYLANDI |
| P-1 C1/C2/C3 hedef şema | 🔴🔴 | ⚠️ **DÜZELTİLDİ** — "ölü/yetim şema" **geri çekildi**; çekirdek onaylandı ve keskinleşti |
| P-2 0.a-EK Kural 3 | 🔴 | ⚠️ **ŞİDDET DÜŞÜRÜLDÜ** (🔴→🟠); yapısal iddia %100 ayakta |
| P-3 "şema değişmez" | 🔴 | ✅ **BÜYÜK ÖLÇÜDE GÜÇLENDİ** — ikinci eksen (zamanlama) eklendi |
| P-4 C6 "iş yok" | 🔴 | ✅ ONAYLANDI |
| P-5 frontend kalemi yok | 🔴 | ✅ ONAYLANDI (plan geneli tarandı: **0** web kalemi) |
| P-6 E12 ↔ KİLİT-2 çelişkisi | 🔴 | ✅ ONAYLANDI (plan geneli "kota" tarandı) |
| P-7 §9.1 bayat karar metni | 🟠 | ✅ ONAYLANDI |
| P-8 Tur 1 kapsam ikiliği | 🟠 | ✅ ONAYLANDI |
| P-9 ADR-009 çakışması | 🟡 | ✅ ONAYLANDI |
| P-10 KR-093 sarkan atıf | 🟡 | ✅ ONAYLANDI (hem `kr_registry` hem `contracts_ssot`'ta yok) |
| P-11 okuyucu listesi eksik | ⚪ | ✅ ONAYLANDI |
| **P-12 C4 contract kalemi değil** | — | 🆕 **YENİ** (öz-denetimde çıktı) |
| **P-13 C5 fiilen yapılmış** | — | 🆕 **YENİ** |
| **P-14 E9 gerekçesi bayat** | — | 🆕 **YENİ** |
| **P-15 `report_phase` kanonik-dışı statü adı** | — | 🆕 **YENİ** (hijyen) |

---

## 1. BULGULAR VE GÜNCELLENMİŞ ÇÖZÜM PLANLARI

### 🔴 H-1 · Devir notu §1/§3 **iki sürüm bayat**

| | Devir notu | Ölçülen gerçek |
|---|---|---|
| Contract | `7.0.1` / `32c747a5…` | **`7.2.0` / `5d3c204d…`** (`CONTRACTS_VERSION.md:3`) |
| Platform pini | "⚠ GERİDE (4.3.0→7.0.1), re-pin gerekli" | **7.2.0 · hizalı** |
| Worker pini | "⚠ AKSİYON" | **v7.2.0 · hizalı** |
| Edge | "1.2.0" | **1.3.0** (kendi şeması, 7.2.0'a atıflı) |

Aradaki iki sürüm: **7.1.0** (`analysis_result.v1 → tile_counts`, KR-088) · **7.2.0** (`intake_manifest.v1` edge karantina sayaçları).
Etiket türü doğrulandı: `git for-each-ref` → dördü de `objecttype=tag` yani **annotated** → **I-2 değişmezi TUTUYOR.**
Yani **I-1 ve I-2 fiilen sağlam**; devir notu sağlam olmadığını sanıyor.

**ÇÖZÜM PLANI (güncellenmiş):**
1. `docs/SESSION_HANDOFF.md` §1'i yeniden yaz: sürüm `7.2.0`, checksum `5d3c204d…`, "önceki: 7.1.0 / 7.0.1".
2. §3 tüketici tablosunu **"üçü de 7.2.0'da hizalı"** olarak düzelt; "re-pin gerekli" satırlarını kaldır.
3. §1'e **kalıcı kural** ekle: *"Bu bölüm sürüm bump'ında C8 töreninin parçası olarak güncellenir; güncellenmemişse release eksiktir."*
4. Dal/PR tablosunun tarihini bugüne çek (H-4 birlikte kapanır).

---

### 🔴 H-2 · AL-C1/C2 hangi turda? — iki dosya çelişiyor

- Devir notu satır 69: *"AL-C1/C2 + C1/C2/C3 **aynı sürüm turunda** birleştirilmeli (tek C8 tören maliyeti)"* → **Tur 1**
- Eylem planı satır 1216: *"**C-Tur-2** ile birleştirilebilir"* → Tur 2 = **Dalga 3 = demo sonrası**

AL-C1/C2 planın kendi ifadesiyle *"tek gerçek bugün alınabilir kilit"* (§11.5) ve **[0] ölçüm temelinin** ön koşulu.

**ÇÖZÜM PLANI:** **Tur 1'de birleştir** (devir notu haklı). Gerekçe: (a) C8 töreni +1-2 gün ve tur başına
tekrarlanıyor; (b) AL-C1/C2 saf **additive** (7. enum değeri + 2 opsiyonel alan) → C1/C2/C3 ile aynı MINOR'a
sığar; (c) Tur 2'ye giderse dedup canlı bağlama ve S2 bütçesi demo sonrasına kayar.
→ Planın satır 1216'sı *"C-Tur-1'e dâhildir"* olarak düzeltilir; §5.1 Dalga 1'in "C: Tur 1" satırına
`+ AL-C1 + AL-C2` eklenir.

---

### 🟠 H-3 · Devir notu, kendi commit'inden sonra gelen 5 dokümanı bilmiyor

`git diff --name-only c6ceda9..HEAD` → `Görev Haritası.txt` · `PAMUK UZMANLAR.txt` ·
**`REPO_BOUNDARY_RULES.txt`** · `SECURITY_AUDIT_REPORT.txt` · `TarlaAnaliz_Etkilesim_Haritasi.docx/png`.

`REPO_BOUNDARY_RULES.txt` kendini **"BAĞLAYICI"** ilan ediyor ve **`tarlaanaliz-web`**'i 5. tüketici
sayıyor — plan/devir notunun ikisinde de web işi yok (bkz. **P-5**).

**ÇÖZÜM PLANI:** Devir notu §0'a *"Bu oturumda repoya giren bağlayıcı dokümanlar"* alt başlığı; her birine
bir satır + planla kesişimi. `REPO_BOUNDARY_RULES.txt`'in web maddesi P-5'in gerekçesine bağlanır.

---

### 🔴 P-1 · C1/C2/C3 hedef şemayı **yanlış/belirsiz** gösteriyor · ⚠️ Tur 1'den DÜZELTİLDİ

**Geri çekilen alt-iddia:** *"`schemas/platform/calibrated_dataset_manifest.v1` yetim/ölü şemadır."*
**YANLIŞ.** İki form **bilinçli ve belgelidir** — kanıt, edge şemasının kendi açıklaması:
> `schemas/edge/calibrated_dataset_manifest.v1.schema.json:5` → *"Platform/dataset-katmanı paket manifesti
> için bkz. `schemas/platform/calibrated_dataset_manifest.v1` (**outputs[]/reports[] aggregation formu**)"*

ve `ssot/contracts_ssot.md:93` onu kanonik listede sayıyor. Bu, denetim kapsamı kuralı gereği
**tasarım kararıdır, kusur değil.**

**Ayakta kalan (ve keskinleşen) çekirdek — üçü de %100 doğrulandı:**

| # | Bulgu | Kanıt |
|---|---|---|
| a | **`patches` alanı contract'ın HİÇBİR şemasında yok** | `schemas/` + `enums/` geneli: **0 eşleşme** |
| b | C2'nin "deprecate edilecek göreli yol alanı" başka dosyada | `schemas/edge/intake_manifest.v1.schema.json:506-523` → `EdgeForm.priority_zones[].visualizations`, regex `^patches/[a-f0-9]{32}/ndvi_overlay\.png$` · edge aynası `priority_zone.py:31,55` |
| c | C1'in istediklerinin çoğu **platform formunda zaten var** | `producer_tool` · `reflectance_scale` (enum: `reflectance_0_1 / reflectance_0_100 / scaled_int / unknown`) · `outputs[]` (`file_artifact{uri,sha256,type}`) |
| d | `priority_zones` **yalnız `EdgeForm`'da**, `PlatformForm`'da yok | `intake_manifest.v1` `$defs` karşılaştırması |

(d) ile **0.a-EK arasında doğrudan çelişki var:** 0.a-EK *"manifestteki `object_key` platformun **döndürdüğü**
değerdir"* diyor; ama C2 onu **edge'in yaydığı** forma koyuyor. Anahtarı platform üretiyorsa alan
`PlatformForm`'a aittir.

**ÇÖZÜM PLANI (yeniden yazılmış C1/C2/C3):**

| Yeni # | İş | Hedef dosya (kesin) | Tip |
|---|---|---|---|
| **C1′** | `index_layers[]` **yeni alan açma** — `outputs[]` zaten var. Yapılacak: `file_artifact`'e opsiyonel `layer_type` (ortho/ndvi/ndre/ndwi) + `calibration_tier` ekle; `reflectance_scale`/`producer_tool` **kullanılır, tekrarlanmaz** | `schemas/platform/calibrated_dataset_manifest.v1` | MINOR |
| **C2′** | `object_key` **`PlatformForm.priority_zones[].visualizations`'a** ekle (yeni alan; `EdgeForm`'daki göreli yol `x-deprecated` işaretlenir, **kaldırılmaz** = non-breaking). ⚠️ `PlatformForm`'da `priority_zones` **hiç yok** → önce oraya eklenmeli | `schemas/edge/intake_manifest.v1` | MINOR |
| **C2″** | Edge `priority_zone.py:31,55` regex'i + `max_length=128` `object_key` için genişletilir | edge (vendored senkron) | — |
| **C3′** | `raw_frames[]` → **hangi form?** Karar: ham kare seçimi kalibrasyon çıktısıdır → `schemas/edge/calibrated_dataset_manifest.v1`'e opsiyonel dizi | `schemas/edge/…` | MINOR |
| **C0 (yeni, ön koşul)** | İki `calibated_dataset_manifest` formunun rol ayrımını `docs/` veya şema açıklamasına **tek cümleyle** sabitle: *"edge formu = kiosk kanıt manifesti · platform formu = dataset-katmanı paket agregası"* | contract docs | PATCH |

⚠️ Edge şema açıklaması *"Edge `interface/contracts/…` ile **birebir** uyumludur"* diyor → edge formuna
dokunan her değişiklik **edge vendored kopya + KR-041 hash** turunu tetikler; C8 planına yazılmalı.

---

### 🟠 P-2 · 0.a-EK Kural 3, kapatmayı iddia ettiği açığı kapatmıyor · ⚠️ şiddet 🔴→🟠

> Kural 3: *"Presigned GET üretilirken anahtar **DB'den** okunur; istekten/manifestten gelen bir yol asla
> doğrudan imzalanmaz."*

**Kod bugün zaten bunu yapıyor** → kural **işlevsiz (no-op)**:
- Platform'daki **tüm** presign çağrıları: `patches.py:165 / :169 / :173` — üçü de `viz_paths = patch_row.visualization_paths` (**DB**) ile besleniyor (`patches.py:151`). İstekten anahtar alan başka çağrı yeri **yok** (tam tarama yapıldı).
- Kirlilik zinciri gerçek ama **DB üzerinden dolaylı**: `ingest_service_impl.py:258-266` edge'in `pz.visualizations.model_dump()` değerini aynen kalıcılaştırıyor.

**Şiddet düzeltmesi:** Sömürü **iki koşul** ister — (1) ele geçirilmiş/hatalı edge kiosk **ve**
(2) o dataset'in mission'ına **atanmış uzman** kimliği. Çünkü `patches.py:118-148`'de gerçek bir sahiplik
kapısı var (`DatasetModel ⨝ ExpertReviewModel.expert_id`, aksi hâlde `403 PATCH.OWNERSHIP_DENIED`).
→ Planın *"çapraz-kiracı veri sızıntısı"* ifadesi **anlık risk olarak abartılı**; doğru ifade
*"ele geçirilmiş edge + atanmış uzman bileşiminde çapraz-dataset okuma"*.

**Yapısal iddia %100 ayakta:** Açığı **yalnız Kural 1** kapatır (anahtarı platform üretir; edge'in önerdiği
yol **hiç kalıcılaştırılmaz**). Kural 3 olduğu gibi kalırsa P4'ün "güvenlik yarısı" yanlışlıkla
*"zaten yapılmış"* sayılabilir.

**ÇÖZÜM PLANI:**
1. 0.a-EK Kural 3'ü yeniden yaz: *"Anahtar DB'den okunur **ve DB'ye yalnız platformun ürettiği anahtar yazılır**;
   edge'in önerdiği yol hiçbir aşamada kalıcılaştırılmaz."* (Kural 1'in kalıcılaştırma yarısı burada eksikti.)
2. `ingest_service_impl.py:266`'ya kabul kriteri: `visualization_paths` **platform tarafından üretilmiş**
   anahtar şemasıyla yazılır; edge değeri yalnız *eşleştirme anahtarı* olarak kullanılır.
3. Kabul testini P4 ile aynı turda yaz **ve iki koşullu kur**: sahte manifest **+ atanmış uzman** →
   kapsam dışı anahtar `SECURITY.DENY`. (Tek koşullu test bugün de yeşil geçer, hiçbir şey kanıtlamaz.)
4. Şiddet etiketini plan metninde 🔴→🟠 düzelt; gerekçeye sahiplik kapısını yaz.

---

### 🔴 P-3 · "Şema değişmez" iddiası **iki eksende** kanonikle çelişiyor · ⚠️ Tur 1'den GÜÇLENDİ

**P-3a — İÇERİK.** İki bağımsız kanonik artefakt PRELIMINARY içeriğini **sayarak ve "YALNIZ/ONLY" diyerek** kapatıyor:

| Artefakt | Metin |
|---|---|
| `schemas/events/analysis_preliminary_ready.v1.schema.json` | *"the preliminary phase carries **ONLY** deterministic index layers (HEALTH/NITROGEN_STRESS/WATER_STRESS) + overall_health_index"* |
| `enums/report_phase.enum.v1.json` → `x-enum-descriptions.PRELIMINARY` | *"**Yalnız** deterministik indeks katmanları (NDVI→HEALTH, NDRE→NITROGEN_STRESS, stress_ratio→WATER_STRESS) + overall_health_index sunulur."* |

Y-D'nin göstereceği içerik — `analysis_priority_zones`: **patch poligonu + `ndvi_value` + `ndvi_overlay` PNG** —
bu dört kalemin **hiçbiri değil**.

**P-3b — ZAMANLAMA (yeni).** `report_phase.x-derived-from.mapping` **tam dört giriş**:
`ANALYZING→PRELIMINARY` · `PENDING_REVIEW→PRELIMINARY` · `DONE→FULL` · `EXPERT_REJECTED→WITHDRAWN`.
Y-D raporu **kalibrasyondan hemen sonra, worker'dan önce** gösteriyor; o anda mission
`UPLOADED` civarında (`mission.py:84`: `UPLOADED → ANALYZING`). **`UPLOADED` için mapping'de karşılık YOK.**
Bunun "zaten çalışıyor" görünmesinin tek sebebi platform kodunun **catch-all**'u:
`results_service_impl.py:227` → `"FULL" if mission_status == "DONE" else "PRELIMINARY"` —
yani **platform kanonik mapping'den daha geniş.** Demo, contract-first (KR-081) projede
**kanonik olmayan bir genişlemenin** üstüne kuruluyor.

**ÇÖZÜM PLANI (yeni C-kalemi gerekiyor — planda yok):**

| Yeni # | İş | Tip |
|---|---|---|
| **C9** | KR-093 iki-fazlı teslimat tanımını **genişlet**: PRELIMINARY içeriğine *"önceliklendirme bölgeleri (poligon + indeks değeri + overlay görseli)"* eklenir; `analysis_preliminary_ready.v1` ve `report_phase.enum.v1` metinlerindeki **"ONLY/YALNIZ" listesi** buna göre güncellenir | MINOR (metin/enum açıklaması) |
| **C10** | `report_phase.x-derived-from.mapping`'e **kalibrasyon-sonrası statü** eklenir (ör. `UPLOADED → PRELIMINARY`) **veya** açıkça yazılır ki *"listelenmeyen statüler PRELIMINARY'dir (fail-closed)"* — platform'un catch-all'u kanonikleşir | MINOR |
| **P12′** | P12 kabul kriterine ek: dönen `report_phase` değeri **C10 mapping'iyle** doğrulanır (kanonik mapping'e karşı test) | — |

⚠️ Bu yapılmazsa: P6/P12 kanonik tanımın dışına çıkar; ilk fark eden sözleşme testi/CI olur ve
**demo haftasında** çıkar.

---

### 🔴 P-4 · C6 "KAPANDI — iş yok" **yanlış**; E13'ü çıkmaza sokuyor

`enums/calibration_type.enum.v1.json` → `x-context-subsets`:
```
edge/intake_manifest             : ABSOLUTE, RELATIVE, PANEL_ABSOLUTE, DLS2_RELATIVE
edge/calibrated_dataset_manifest : ABSOLUTE, RELATIVE          ← DLS2_RELATIVE YOK
```
Edge manifest şemasındaki `calibration_result.calibration_type` enum'u da birebir `["ABSOLUTE","RELATIVE"]`.
Planın C6 notu *"M3M'in dahili ışık sensörü olduğu için `DLS2_RELATIVE` daha doğru tier olabilir —
E13'te karara bağlanmalı"* diyor. O karar `DLS2_RELATIVE` çıkarsa **contract değişikliği zorunlu.**

Ayrıca **E13'teki `calibration_tier` alan adı contract'ta yok**; kanonik ad `calibration_result.calibration_type`.

**ÇÖZÜM PLANI:**
1. C6'yı **"KAPANDI"dan "KOŞULLU AÇIK"a** çevir: *"E13 kararı `RELATIVE` ise iş yok; `DLS2_RELATIVE` ise
   `x-context-subsets['edge/calibrated_dataset_manifest']` + şema enum'u genişletilir (**MINOR, breaking değil**)."*
2. E13'i **C6'dan önce** karara bağla — sıra planda ters (`E13 → bağımlılık: C1, C6`).
3. Plandaki `calibration_tier` geçişlerini `calibration_result.calibration_type` olarak düzelt (C1′ ve E13).

---

### 🔴 P-5 · Demo kritik yolunda **arayüz adımı yok**

Plan geneli tarandı (`tarlaanaliz-web|frontend|PWA|Next.js|arayüz|ekran|UI`): **tek bir web iş kalemi yok.**
Eşleşmelerin hepsi alakasız (kalibrasyon paneli "ekran ortasında", Terra arayüzü, DJI CLI sorusu).
Oysa: `tarlaanaliz-platform/web/` (`web/package.json`) **mevcut** ve `REPO_BOUNDARY_RULES.txt`
`tarlaanaliz-web`'i bağımsız tüketici sayıyor.

①–⑥ adımlarının hepsi şema/edge/backend'de bitiyor. KG-0.b-R'nin direktifi *"çiftçi **görsün**"*di.

**ÇÖZÜM PLANI:** Demo kritik yoluna **⑦** eklenir ve Dalga 2'ye alınır:

| Yeni # | İş | Süre |
|---|---|---|
| **WEB1** 🔴 | **ÖN RAPOR ekranı** — tarla haritası üzerinde `analysis_priority_zones` poligonları (`geom`), `ndvi_value` ile renk skalası, poligona tıklayınca presigned `ndvi_overlay` görseli. Başlık: **"ÖN RAPOR"** | 3-4 gün |
| **WEB2** 🟠 | Boş-durum ve kapı mesajları: ödeme kapılı (KR-033), henüz bölge yok, `report_phase=FULL`'a geçince tam rapora yönlendirme | 1 gün |

⚠️ Dalga 2 süresi **+3-5 gün** uzar; §5.1 takvimi buna göre güncellenmeli — WEB1 olmadan demo API cevabında kalır.

---

### 🔴 P-6 · E12 için plan kendi içinde çelişiyor, çözüm hiçbir kaleme bağlı değil

| Yer | Ne diyor |
|---|---|
| §5.1 demo kritik yolu ③ | E12 **demo öncesi zorunlu** |
| §10.5 satır 1167 · §11.5 satır 1253 | *"E12, KİLİT-2 kapalıyken **açılmaz**; ya dedup bağlanır ya kota manuel sınırlanır"* |

KİLİT-2 gerçekten kapalı: `should_send_to_expert` worker'da `prototype_manager.py:546`'da tanımlı,
**çağrısız** (diğer eşleşmeler yorum).
Plan geneli "kota" tarandı: tek kota kalemi **P9** ve **Dalga 4'te** (satır 306), yani **demodan sonra**.
→ §10.5'in tanıdığı **iki kaçış yolundan hiçbiri** bir iş kalemine bağlanmamış.

**ÇÖZÜM PLANI:** P9 **ikiye bölünür**:

| Yeni # | İş | Dalga |
|---|---|---|
| **P9a** 🔴 | **Pilot kota tavanı** — `daily_image_capacity` için sabit üst sınır + aşımda kuyruğa alma; E12 ile **aynı sürümde** devreye girer. §10.5'in "kota manuel sınırlanır" kaçış yolunun uygulaması | **Dalga 2 (E12 ile birlikte)** |
| **P9b** | Gerçek uzman kapasitesi ölçümü + kalıcı kota (S2 bütçesi B girdisi) | Dalga 4 (mevcut hâli) |

E12 satırına ön koşul yazılır: **"P9a olmadan açılmaz."**

---

### 🟠 P-7 · §9.1 "kopyala-yapıştır" blokları bayat karar metni taşıyor

| Satır | İçerik | Sorun |
|---|---|---|
| 955 | Özet tablo: `0.b · **Y-C** melez ön rapor` | Yürürlükten kalktı |
| 984 | Defter satırı: `KG-0.b … **Y-C** (rapor değil durum bildirimi)` | Deftere **iki çelişen karar** girer |
| 1026 | ADR-007 notu: *"KG-0.b ile **Y-C** biçiminde karşılandı"* | Satır 687 *"not **Y-D'yi** anlatacak"* diyor → kopyalanacak metin yanlış olanı |

**ÇÖZÜM PLANI:** Üç satır da Y-D'ye göre yeniden yazılır. Yöntem: KG-0.b satırı **silinmez**, ancak
`| KG-0.b | ~~Y-C~~ → **KG-0.b-R ile değiştirildi (Y-D)** | SUPERSEDED |` biçimine çevrilir
(karar tarihçesi korunur, yürürlükteki karar tekil kalır). Satır 1026'daki ADR-007 not metni
Y-D anlatısıyla değiştirilir.

---

### 🟠 P-8 · Tur 1 kapsamı iki yerde farklı + AL-C1/C2 takvimde yok

- §3.1 satır 172: `Tur 1 = C1+C2+C3+C5+**C6**` — ama C6 "iş yok" işaretli (ve P-4'e göre koşullu açık)
- §5.1 Dalga 1: `Tur 1 (C1,C2,C3,C5)`
- **AL-C1/AL-C2 dalga şemasında hiç geçmiyor** (H-2 ile aynı kök)

**ÇÖZÜM PLANI:** Tek kanonik Tur-1 tanımı yazılır ve iki yere de aynısı konur:
**Tur 1 = C0 + C1′ + C2′ + C3′ + C9 + C10 + AL-C1 + AL-C2** *(C5 düşer — bkz. P-13; C6 koşullu — bkz. P-4)*.

---

### 🟡 P-9 · ADR-009 numarası iki işe verilmiş

Satır 42/643: Y-A alternatifi = "ADR-009, yeni faz". Satır 1027: dev-station = "ADR-009-dev-station-profile.md".
Platform ADR'leri **ADR-008'de bitiyor** (doğrulandı) → 009 boş; ama Y-A FAZ 1'de canlanırsa çakışır.

**ÇÖZÜM PLANI:** ADR-009 = **dev-station** (yazılacak olan). Y-A'nın metnindeki "ADR-009" atıfları
**"ileride tahsis edilecek ADR"** olarak nötrleştirilir.

---

### 🟡 P-10 · KR-093 kanonik registry'de **yok** (SSOT boşluğu)

Contract kendi artefaktlarında KR-093'e **normatif** atıf yapıyor:
- `enums/report_phase.enum.v1.json` → *"KR-093 (İki-Fazlı Teslimat) **kanonik**"*
- `schemas/events/analysis_preliminary_ready.v1.schema.json` → *"Under KR-093 (two-phase delivery)…"*

Ama `ssot/kr_registry.md` **KR-092'de bitiyor** ve `ssot/contracts_ssot.md`'de de geçmiyor.
KR-093 yalnız `tarlaanaliz-platform/docs/kr/kr_registry.md`'de tanımlı. CLAUDE.md: *"kanonik kaynak
`ssot/kr_registry.md`"* → **sarkan (dangling) kanonik atıf.**

**ÇÖZÜM PLANI:** KR-093 kaydı platform registry'sinden `ssot/kr_registry.md`'ye **taşınır/aynalanır**
(KR-092'den sonra). **C9 ile aynı turda** yapılır — çünkü C9 zaten KR-093 metnini değiştiriyor;
tanımı olmayan bir KR'yi değiştirmek mümkün değil.

---

### 🆕 🔴 P-12 · C4 bir **contract kalemi değil** — contract'ta `sorties` diye bir alan yok

C4: *"`intake_manifest.v1` → `sorties[].bbox` politikası: zorunlu yapmak **breaking**; öneri opsiyonel kalsın."*

Ölçüm: `sorties` **contract'ın hiçbir şemasında/enum'unda geçmiyor** (repo geneli `*.json/*.yaml/*.md`
taraması; tek eşleşme planın kendi satır 168'i). `intake_manifest.v1`'de de yok, `dataset_manifest.v1`'de de yok.
`sorties` yalnızca **edge-yerel görev manifestinde** yaşıyor: `aggregator.py:101,151` → `manifest.get("sorties")`.

→ *"Zorunlu yapmak breaking"* önermesi konusuz: **var olmayan alan required yapılamaz.**

**ÇÖZÜM PLANI:**
1. C4 §3.1 **CONTRACT** tablosundan **çıkarılır**, §3.2 EDGE tablosuna **E9'un ön koşulu** olarak taşınır.
2. Gerçek karar yeniden ifade edilir: *"Edge-yerel görev manifestinde `sorties[].bbox` zorunlu mu?"* —
   bu bir **edge şema kararıdır**, contract turu gerektirmez, C8 töreni maliyeti **yoktur**.
3. Eğer `bbox`'ın platforma taşınması isteniyorsa **ayrı ve yeni** bir contract kalemi açılır
   (bugün taşınmıyor).

---

### 🆕 🟠 P-13 · C5 **fiilen yapılmış** — Tur 1'i gereksiz şişiriyor

C5: *"`analysis_type.enum.v1` → metadata'ya 'üretilemez' notu: BENEFICIAL (model yok),
THERMAL_STRESS (M3M'de termal bant yok)."*

Ölçüm (`analysis_type.enum.v1.json`, `metadata.version = 1.4.1`):
- `BENEFICIAL → availability: "enum_valid_not_yet_emittable"`, tanımı: *"Enum'da parite için geçerli, ancak
  mevcut multispektral çözünürlük + **model olgunluğuyla** henüz emit edilemez; model olgunlaşınca aktifleşir."*
- `THERMAL_STRESS → availability: "requires_thermal_payload"`, tanımı: *"LWIR (termal) bandı gerekir…
  **Mavic 3M'de üretilemez**."*

KG-0.f'in istediği **iki not da makine-okunur biçimde zaten var** — üstelik serbest metin değil,
enum'lu `availability` alanı olarak.

**ÇÖZÜM PLANI:** C5 **"YAPILDI"** işaretlenir. Kalan tek gerçek delta: `metadata.changeNote`'a
**KG-0.f çapraz atfı** (*"karar kaydı: KG-0.f, 2026-07-30"*) — izlenebilirlik için, PATCH bile
gerektirmeyecek kadar küçük; C0 ile aynı commit'te gider. **Tur 1 kapsamından düşer.**

---

### 🆕 🟠 P-14 · E9'un gerekçesi bayat — "sessiz çöküş" zaten giderilmiş

E9: *"bbox yoksa `PRIORITIZATION_MIXED_CROP` **sessiz çöküşü** yerine açık hata."*

Ölçüm — çöküş **zaten sesli**:
- `calibration_pipeline.py:207` yorumu: *"PRIORITIZATION.MIXED_CROP **instead of happening silently**"*
- `calibration_pipeline.py:230`: `event=PRIORITIZATION_MIXED_CROP` yayılıyor
- `custody_logger.py:93`: `PRIORITIZATION.MIXED_CROP` kanonik denetim olayı
- `calibration_pipeline.py:399` docstring: *"so the collapse is **audited rather than silent**"*

→ Kalan iş *"sessizi sesli yap"* değil; **"denetim uyarısını sert hataya çevir"**. Bu **farklı ve daha
küçük** bir karar; üstelik ters yönde bir risk taşıyor (mixed-crop tarlada pilot uçuşu tamamen bloke olur).

**ÇÖZÜM PLANI:** E9 yeniden yazılır: *"`PRIORITIZATION.MIXED_CROP` **denetim uyarısı olarak kalsın mı,
sert hata mı olsun?** — pilotta **uyarı** (uçuş bloke olmasın), üretimde **sert hata**. Karar
`build_profiles.yaml` (dev-station vs production) üzerinden profillenir."* → Süre tahmini düşer;
E1 (dev-station profili) ile birleşir.

---

### 🆕 🟡 P-15 · `report_phase.enum.v1` kanonik-**olmayan** statü adı haritalıyor (hijyen)

`report_phase.x-derived-from.mapping` **`ANALYZING`** diyor; `mission_status.enum.v1`'in 19 değeri arasında
`ANALYZING` **yok** (`IN_ANALYSIS` var). `ANALYZING` platform-**içi** addır ve çevirisi platformda belgeli
(`mission.py:27` → `_STATUS_TO_CONTRACT: ANALYZING->IN_ANALYSIS`).

→ Kanonik bir enum, **kanonik olmayan bir değeri** haritalıyor. Aktif kırık yok (platform çeviriyor),
ama contract-first ilkesine aykırı ve **C10'u yazacak kişiyi yanıltır.**

**ÇÖZÜM PLANI:** C10 ile aynı turda mapping kanonik adlara çevrilir
(`IN_ANALYSIS → PRELIMINARY`, `PENDING_REVIEW → PRELIMINARY`, …) ve altına bir satır not düşülür:
*"Platform-içi `ANALYZING` adı `IN_ANALYSIS`'e karşılık gelir (bkz. platform `_STATUS_TO_CONTRACT`)."*

---

### ⚪ P-11 · Küçük eksiklik (kararı etkilemez)

Plan `analysis_priority_zones` okuyucularını *"yalnız `worker_dispatch_handler` + `expert_review_prioritization_service`"*
sayıyor; ayrıca `worker_bridge_consumer.py:1088` (kota) ve `worker_job_publisher.py:115` okuyor.
**Çiftçi ucunun olmadığı iddiası doğru** ✅. → Cümleye iki okuyucu eklenir.

---

## 2. Planın DOĞRULANAN tarafı (kanıtla geçti — düzeltme gerekmiyor)

| İddia | Kanıt |
|---|---|
| **E14** — `calibration_result` 5 yerde tüketiliyor, **0 yerde üretiliyor** | `dataset.py:123-125` · `calibrated_validator.py:114-122` · `qc_report_writer.py:220/254/340` · `package_assembler.py:52` · `ndvi_prioritizer.py:5`; `json.dump` ile yazan **yok** |
| **E10** — `ndvi_overlay` yerel diske, manifeste göreli yol | `calibration_pipeline.py:332-336` + `expert_image_renderer.py:143-144` |
| **E12** — bayrak kapalı | `config.py:160` = `False` · `.env.example:113` |
| **E2** — edge'de S3/MinIO yok | `boto3\|minio\|presigned` → **0 eşleşme** |
| **E3** — `submit_manifest` çağrısız | `cloud_client.py:140` yalnız tanım |
| **E6** — runner süreç-başlatıcı varsayımı | `pix4d_runner.py:4` *"Invokes the Pix4Dfields headless CLI"* + `safe_subprocess_sync` |
| `results_service_impl.py:227/247` · `ingest.py:71` · `ingest_service_impl.py:266` · `patches.py:165-175` · `worker_bridge_consumer.py:1088` · `layer_registry.py:109-113` · `flight_route_generator.py:331` | Satır satır birebir |
| **AL-C1** — `escalation_reason` tam 6 değer | Kanonik **ve** worker vendored kopya birebir |
| **C7** — `frame_analysis_job.v1` yok (yeni şema doğru) | `schemas/worker/` listesi |
| **Ç-3** — contract 8 · readiness 12 · edge 5 ürün | 8 = COTTON/PISTACHIO/CORN/WHEAT/SUNFLOWER/GRAPE/OLIVE/RICE · edge = COTTON/CORN/PISTACHIO/GRAPE/RICE |
| **KİRAZ** `bookable:True`, enum'da ve edge tablosunda yok | `crop_readiness.json` + iki kaynak |
| **KİLİT-2** · `cluster_margin/supcon/diversity_select` 0 eşleşme · `router_density: null` | üçü de |
| **W2** — ODM 0-1 varsayımı gömülü | `orthomosaic_to_tiles.py:224` *"float32 reflectance [0,1] … scale = 65535"* |
| **W4** — worker yalnız GeoTIFF | `pipeline.py:379` + TIFF magic guard |
| **Ç-1** — Botrytis seti multi-angle + MicaSense RedEdge 3 | `grape_datasets.yaml:83` ↔ `odm_run_botrytis.sh:5-6,45` çelişkisi gerçek |
| **§2.2 uçuş tablosu** | Protokol §10.1 satır 370/374 ile **birebir**; sütunlar Y/v/MS+RGB; aritmetik tutarlı (irtifayla artmayan tetik sayısı **hız değişiminden** kaynaklanıyor, hata değil) |

---

## 3. GÜNCELLENMİŞ İCRA SIRASI

| # | İş | Neden bu sırada |
|---|---|---|
| **0** | Devir notu §1/§3 → **7.2.0** | Yanlış bilgi sonraki oturuma taşınıyor (H-1) |
| **1** | **C0** — iki manifest formunun rol ayrımını sabitle | C1′/C2′/C3′ bu karar olmadan yazılamaz (P-1) |
| **2** | **KR-093'ü kanonik registry'ye taşı** (P-10) → sonra **C9 + C10** (P-3a/P-3b) | Tanımı olmayan KR değiştirilemez; P6/P12 buna dayanıyor |
| **3** | **E13 kararı → C6 koşullu açık** (P-4) | Ters bağımlılık düzeltilir |
| **4** | **Tur 1'i yeniden tanımla:** C0+C1′+C2′+C3′+C9+C10+AL-C1+AL-C2 · C5 düşer · C4 edge'e taşınır | P-8, P-12, P-13, H-2 birlikte kapanır |
| **5** | **§9.1 bloklarını Y-D'ye göre düzelt** (satır 955/984/1026) | Yanlış metin kalıcı kayda girer (P-7) |
| **6** | **WEB1/WEB2** demo kritik yoluna ⑦ · **P9a** Dalga 2'ye | Demo API'de kalmasın; plan kendi kuralını ihlal etmesin (P-5, P-6) |
| **7** | **E9'u yeniden yaz** (uyarı mı sert hata mı, profil bazlı) | Bayat gerekçe (P-14); E1 ile birleşir |
| **8** | Sonra planın kendi Dalga 1'i — **E14 ilk iş** | Bu tespit **tam doğrulandı**, sağlam |

---

## 4. Doğrulama komutları (bu raporu yeniden üretmek için)

> Hepsi **yerel geliştirme makinesinde**, ilgili depo kökünde koşar. Canlı sunucuda çalıştırılmaz.

```bash
cd tarlaanaliz-contract && git for-each-ref --format='%(refname:short) %(objecttype)' refs/tags && python -X utf8 tools/pin_version.py --verify && python -X utf8 tools/validate.py
```

```bash
cd tarlaanaliz-contract && grep -rn "\"patches\"" schemas/ enums/ ; grep -rn "sorties" schemas/ enums/ ; echo "iki tarama da BOS donmeli"
```

```bash
cd tarlaanaliz-edge && grep -rn "calibration_result" src/ --include=*.py | grep -v __pycache__ ; echo "yazan (json.dump) OLMAMALI = E14 dogrulanir"
```

---

**Rapor sonu.** Tur 1'de 15 bulgu vardı; öz-denetimde **1 alt-iddia geri çekildi**, **1 şiddet düşürüldü**,
**4 yeni bulgu** eklendi. Yukarıdaki **19 maddelik küme kaynak-doğrulanmıştır**; her madde
`dosya:satır` ile tekrar sınanabilir.
