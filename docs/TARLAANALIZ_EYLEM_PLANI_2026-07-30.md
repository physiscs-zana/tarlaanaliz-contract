# TARLAANALIZ — EYLEM PLANI, İŞ AKIŞI VE REPO BAZLI İŞ SIRALAMASI

> **Tarih:** 2026-07-30 · **Son revizyon:** 2026-07-31 (bağımsız denetim turu)
> **Statü:** Kamu araştırma projesi · **Koordinatör:** proje sahibi
> **Bu dosya YAPILACAK İŞLERİN TEK KAYNAĞIDIR.** Başka hiçbir dosyada iş listesi tutulmaz.
> Ayrıntılı yazılım karşılaştırması + kaynak listesi **§8'e özetlendi** (ayrı karşılaştırma dosyası silindi).
> **Referans donanım:** DJI Mavic 3M (tek drone) · işleme: RTX 3090 masaüstü (24 GB VRAM / 32 GB RAM / 1 TB)
> **M1/M2 istasyonları henüz ALINMADI** — planın tamamı bunu varsayar.
>
> ### 📐 Dosya rolleri (karışıklık önleyici — 2026-07-31)
> | Dosya | Rolü | İş listesi tutar mı? |
> |---|---|---|
> | **bu dosya** | **Yapılacak işlerin tek kaynağı** (C/E/W/P/WEB/AL kalemleri) | ✅ **EVET — tek** |
> | `docs/SESSION_HANDOFF.md` | Depo durumu fotoğrafı + oturumlar arası devir | ❌ hayır (buraya işaret eder) |
> | `denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` | **Kanıt arşivi** — her düzeltmenin `dosya:satır` dayanağı | ❌ hayır (gerekçe arşivi) |
> | `denetim/` altındaki diğer raporlar | Tarihsel denetim kayıtları | ❌ hayır |

---

# 0. KAMU ARAŞTIRMA PROJESİ OLMASININ ETKİSİ (önceki planlardan sapmalar)

Proje ticari değil, protokollerle **kamunun araştırma projesi**. Bu, önceki analizlerdeki
**üç engeli kaldırıyor, bir yenisini ekliyor.**

| Konu | Ticari varsayımıyla (eski) | Kamu araştırma projesi olarak (yeni) |
|---|---|---|
| **3. şahıs mali mesuliyet sigortası** | ZORUNLU (ağırlıktan bağımsız) | Protokol §2.2 tetikleyicisi **"yalnızca TİCARİ faaliyet"** → **düşer.** ⚠️ Kurumun kendi uçuş izin/sorumluluk prosedürü geçerli olur — **kurum hukuk birimine teyit ettirin** |
| **Ticari pilot eğitimi (12 sa teori)** | ZORUNLU | Ticari tetikleyici düşer; kurum içi yetkinlik politikası geçerli. **SHGM'ye yazılı teyit** |
| **SHGM Kayıt Sistemi kaydı** | ZORUNLU | **YİNE ZORUNLU** — ağırlık bazlı (M3M ~951 g → İHA-0, 7 gün içinde kayıt). Statü bunu değiştirmez |
| **120 m AGL · VLOS 500 m · yasak bölge izinleri** | geçerli | **AYNEN GEÇERLİ** (5 iş günü meskûn mahal / 10 iş günü yasak bölge yakını) |
| **TKGM MEGSİS parsel verisi** | ❌ Kapalı ("ticari amaçla kullanılamaz") | ✅ **AÇILIYOR.** MEGSİS zaten "çeşitli kurum ve kuruluşlar ile internet servisleri aracılığıyla" paylaşılıyor. **Kamu-kamu kurumsal protokol tam bu kanal.** Kod hazır (bkz. §3-**P7**) |
| **Agisoft Service Provider ($6.736/yıl)** | Gerekebilirdi | **Muhtemelen gereksiz** — servis satmıyorsunuz. Node-locked $3.499 yeterli; kurum akredite araştırma/eğitim kuruluşuysa **eğitim lisansı** çok daha ucuz |
| **Pix4D EULA servis-bürosu sorusu** | Belirsiz risk | Gevşer; PIX4Dfields'in de **eğitim lisansı** var |
| **Yazılım satın alma** | serbest | ⚠️ **YENİ ENGEL: kamu satın alma prosedürü** (doğrudan temin / ihale) → takvim uzar. Lisans ihtiyacını **en az 2 ay önceden** başlatın |
| **Veri yönetimi** | ticari gizlilik | ⚠️ Kamu araştırma projesi → **veri yönetim planı**, çiftçi rızası, yayın/veri paylaşım politikası. Muhtemelen **daha katı** |

**Sonuç:** Önceki planımdaki "önce lisans sorusunu cevaplat" blokeri **büyük ölçüde çözüldü.**
Yeni sorular artık şunlar (§1'de eyleme dönüştü): eğitim/araştırma lisansı uygunluğu + kamu satın
alma takvimi + kurum uçuş izin prosedürü + TKGM protokol başvurusu.

---

# 1. ADIM 0 — KARAR GÜNÜ (1 gün, kod yazılmaz) — **7 karar birlikte alınır**

Bu yedi karar birbirini etkiliyor; ayrı ayrı verilemez. Hepsi yazılı hâle gelmeden kod yazılmaz
(KR-081 contract-first).

| # | Karar | Öneri | Neden birlikte |
|---|---|---|---|
| **0.a** | **C13 taşıma mimarisi**: (1) platformda parça-yükleme ucu · (2) manifest + presigned PUT | **(2)** | C16'yı da çözer; platformu veri yolundan çıkarır |
| **0.b** | **C15 ön rapor**: Y-A (yeni faz + yeni ADR) · Y-B (direktifi reddet) · Y-C (durum bildirimi) · **Y-D (öncelik bölgesi kaynaklı ÖN RAPOR)** | **Y-D** ⟵ *KG-0.b-R ile revize; Y-C yürürlükten kalktı* | ADR-007 §2/§5 korunur, üç ADR birden açılmaz |
| **0.c** | **Ham kare politikası**: (i) hiç gitmez · (ii) tamamı · (iii) yalnız işaretli yamaları gören kareler | **(iii)** | 0.a'nın anahtar şemasını belirler |
| **0.d** | **Pilot + demo ürünü** | **GRAPE birincil** · PISTACHIO ikincil (§2.1) | Eğitim veri seti + eşik tablosu kesişimi |
| **0.e** | **Dev-station modu**: M1+M2 rolü tek makinede; hangi güvenlik gevşetmeleri, nasıl denetime yazılır | **Gerekli** | M1/M2 alınmadı; yoksa hiçbir veri platforma girmez |
| **0.f** | **Etiket şeması**: "böcek türü + sayısı" → **"zararlı hasar izi sınıfı + şiddeti"** | **Değiştir** | Pilot verisi toplanırken yanlışsa 3 haftalık veri boşa gider |
| **0.g** | **Lisans yolu**: eğitim/araştırma lisansı mı, tam ticari mi | **Eğitim/araştırma sor** | Kamu satın alma takvimini başlatır |

**Çıktılar:** 7 kararın yazılı kaydı · gerekiyorsa ADR · `end_to_end_workflow.md`'de C13/C15/C16
durum güncellemesi · `open_items_decisions_2026-06.md`'ye COORDINATE/DEFER kaydı.

---

# 2. PİLOT VE DEMO: ÜRÜN SEÇİMİ VE UÇUŞ ÇERÇEVESİ

## 2.1 Ürün hazırlık matrisi — hangi ürünle ne gösterilebilir

**Kanonik kaynak:** `tarlaanaliz-platform/data/crop_readiness.json`
(üretildiği yer: `tarlaanaliz-worker/config/crop_readiness.yaml`, 2026-07-11).
⚠️ **`config/*_datasets.yaml` dosyasının varlığı hazırlık göstergesi DEĞİLDİR** — tek yetkili
sinyal `crop_readiness.json`'dır (zeytin buna örnek: `olive_datasets.yaml` var ama `bookable: False`).

| Ürün | stage1 | data_status | bookable | Edge NDVI eşiği + fenoloji | Demo uygunluğu |
|---|---|---|---|---|---|
| **GRAPE (üzüm/bağ)** | pilot | **strong** | ✅ | ✅ | ✅✅ **en iyi — tam** |
| **CORN (mısır)** | pilot | **strong** | ✅ | ✅ | ✅✅ **tam** |
| **PISTACHIO (antep fıstığı)** | pilot | **limited** | ✅ | ✅ | ✅ **yapılabilir** — tespit kalitesi zayıf olur, ÖN RAPOR sorunsuz |
| COTTON (pamuk) | pilot | critical_gap | ✅ | ✅ | ⚠️ koşar ama tespit güvenilmez |
| CHERRY (kiraz) | pilot | limited | ✅ | ❌ | ⚠️ eşik tablosu yok |
| **WHEAT (buğday)** | pilot | **strong** | ✅ | ❌ **eksik** | ⚠️ **veri güçlü, tek engel iki YAML girdisi** → E8 |
| OLIVE (zeytin) | research | critical_gap | ❌ | ❌ | ❌ |
| RICE (çeltik) | research | critical_gap | ❌ | ✅ | ❌ `bookable:False` |
| SUNFLOWER (ayçiçeği) | research | critical_gap | ❌ | ❌ | ❌ |

**İki ayrı "ön rapor" kavramını karıştırmayın:**

| | Kaynak | Worker gerekir mi? |
|---|---|---|
| **(a) C15 / Y-C durum bildirimi** | Edge `DATASET.STATE_TRANSITION → CALIBRATED` | ❌ **hayır** — kalibrasyon biter, çiftçiye "işlendi, analiz sürüyor" gider |
| **(b) ADR-007 PRELIMINARY rapor fazı** | `report_phase`, mission.status'tan türetilir (ANALYZING/PENDING_REVIEW) | ✅ **evet** — mission bu duruma **worker sonucu gelince** girer |

Yani **(b) için eğitim veri seti gerekmez** (ön rapor tespit içermez, yalnız indeks katmanı) **ama
worker'ın koşması gerekir.** Worker veri-yoksun ürünlerde çökmez — `blocked_by_data` durumunda
skor `None` döner (0,5 değil), `check_stage_allowed` kapısı devrededir.

### Öneri: ikili demo tasarımı

| Rol | Ürün | Gösterilen |
|---|---|---|
| **Ana hikâye (bahçe)** | **ANTEP FISTIĞI** (`bookable`, pilot, limited) | Kayıt → ada/parsel → otomatik uçuş planı → uçuş → kalibrasyon → **ÖN RAPOR** (NDVI/NDRE + zonasyon) → çiftçiye harita. Uçtan uca gerçek |
| **YZ tespit kalitesi (tek slayt)** | **ÜZÜM (bağ)** (`strong`) | Aynı hattın sonunda eğitilmiş modelin tespit çıktısı (Botrytis veri seti) |

Demoda ayrımı **açıkça söyleyin:** *"indeks katmanı bookable ürünlerin hepsinde hazır; tespit
kalitesi ürün bazlı veri olgunluğuna bağlı — üzüm ve mısır `strong`, fıstık `limited` ve pilot
aşamasında."* Bu zayıflık değil **yol haritası** olarak okunur.

**En ucuz kazanç:** BUĞDAY `data_status: strong` ve `bookable: True` ama **edge eşik/fenoloji
tablosunda yok** — iki YAML girdisi (birkaç saat) güçlü verili bir ürünü daha açar (§3-E8).

## 2.2 Uçuş çerçevesi — 1 drone, günde 10-12 uçuş × 30 dk

Tamamen `tarlaanaliz-edge/docs/operations/Tarama_Protokolu_v1.6_Birlesik.txt` §10 tablosundan
türetildi (MS+RGB modu = tetik başına
5 dosya; tetik sayısı = dosya/5).

| İrtifa | 1 uçuş: tetik / dosya / alan | 10 uçuş/gün: dosya / alan | 12 uçuş/gün: dosya / alan |
|---|---|---|---|
| 25 m | ~1.046 / **5.229** / 42 dönüm | 52.290 / 420 dönüm | 62.748 / 504 dönüm |
| 30 m | ~871 / 4.357 / 50 dönüm | 43.570 / 500 dönüm | 52.284 / 600 dönüm |
| **35 m** | ~934 / **4.669** / 73 dönüm | **46.690 / 730 dönüm** | 56.028 / 876 dönüm |
| 40 m | ~817 / 4.085 / 84 dönüm | 40.850 / 840 dönüm | 49.020 / 1.008 dönüm |
| 60 m | ~654 / 3.268 / 151 dönüm | 32.680 / 1.510 dönüm | 39.216 / 1.812 dönüm |

**Operasyonel gerçeklik:** 12 × 30 dk = **6 saat havada** → en az 4-6 batarya + saha şarjı.
Güneş >30° penceresi Ağustos'ta GAP'ta ~09:00-17:00 (8-9 saat). **İlk hafta 8-10 uçuş gerçekçi.**

**Depolama üst sınırı** (ÇS 2592×1944 16-bit sıkıştırmasız = 10,1 MB/bant × 4 + RGB JPEG ~11 MB
≈ **51 MB/tetik**):

| İrtifa | Uçuş başına | 10 uçuş/gün | 1 TB diskte |
|---|---|---|---|
| 25 m | ~53 GB | ~533 GB | **~2 gün** |
| 35 m | ~48 GB | ~476 GB | ~2 gün |
| 60 m | ~33 GB | ~334 GB | ~3 gün |

⚠️ **Gerçek değer bunun altında** — DJI TIFF'i sıkıştırılmış olabilir, bit derinliği EXIF
`Bits Per Sample`'da. **İlk uçuşta ölçülecek.**
⚠️ **256 GB SD kart 25 m'de ancak 4-5 uçuş** → çoklu kart + uçuşlar arası boşaltma zorunlu.

## 2.3 Sabit uçuş kuralları (protokolden — her uçuşta aynı)

| Kural | Değer |
|---|---|
| Güneş yüksekliği | **>30°** |
| Gimbal | **−90°** |
| Panel | Uçuştan **önce ve sonra**; ekran ortasında; yükseklik = panel kenarının **7 katı** (h=7d); **gölgesiz** |
| Kamera | RGB: AUTO + AE lock + EV 0 · ÇS: NDVI + ortalama ölçüm |
| Bindirme | ileri ve yan **≥%60** (protokol formülleri %80/%70 varsayar) |
| Hız tavanı | **v ≤ H/3,9** (25 m→max 6,4 m/s, güvenli 4-5) |
| İrtifa | **Pilot penceresinde TEK irtifa** (öneri 35 m). Protokol fenolojiye göre irtifa değiştirdiğinde seri **yeniden temellenir**, eski seriyle aynı grafikte kıyaslanmaz |
| Saat | Her hafta **aynı saat ±1 saat** |

## 2.4 İlk uçuşta ölçülecek 5 şey (hepsi 1 günde biter)

1. **Dosya boyutları** — ÇS TIFF ve RGB JPEG gerçek MB + EXIF `Bits Per Sample`
2. **Terra çıktı dosya adları** — `_discover_output` config'i buna göre yazılacak
3. **Terra arayüzünde M3M için ışık sensörü seçeneği var mı** — DJI'ın M3M radyometri dokümanı
   panel odaklı, ışık sensöründen söz etmiyor; oysa M3M'de sensör **var** ve `Irradiance` XMP
   etiketi tanımlı. Yoksa Terra reflektansı yalnız panele dayanır → bulutlu günlerde seri kayar
4. **M3M ham kare XMP'sinde** `SensorGain`, `ExposureTime`, `Irradiance` ve **vinyet parametreleri**
   gerçekten var mı (§3-W1'in ön koşulu)
5. **ODM'nin M3M bant hizalaması** — topluluk kayması bildiriyor; sizde de var mı
6. **Terra çıktısında filigran/logo var mı** — `.tif`'i QGIS'te aç + `gdalinfo` metadata.
   Hiçbir kaynak filigran bildirmiyor ama DJI'ın açık beyanı da yok (§12.6). Filigran
   çıkarsa demo görselini **ODM ortosundan** üretin

---

# 3. REPO BAZLI İŞ SIRALAMASI

## 3.1 CONTRACT (`tarlaanaliz-contract`) — **her zaman ilk** (KR-081)

| # | İş | Tip | Bağımlılık |
|---|---|---|---|
| ✅ **C0** | **YAPILDI (2026-07-31, dal `feat/contract-tur1`).** İki `calibrated_dataset_manifest.v1` formunun rol ayrımı **makine-okunur** hâle getirildi. ⚠️ *Uygulama sırasında düzeltilen varsayım:* prose çapraz-atıf **iki yönde de zaten vardı** (`edge/…:5` **ve** `platform/…:5`) — eksik olan belge değil, **zorlanabilirlik**ti; prose C1/C2/C3'ün yanlış dosyayı hedeflemesini engelleyememişti. **Yapılan:** her iki şemaya `x-form-role` (`role`, `emitter`, `purpose`, `counterpart`=karşı `$id`, `owns[]`, `not_owned_here`, `field_placement_rule`) + `x-updated` · `ssot/contracts_ssot.md` KR-072'ye alan-sahipliği tablosu · **`tests/test_manifest_form_roles.py` (12 test)** — `counterpart`↔`$id` birebir, `owns[]` hayalî alan sayamaz, iki form aynı alanı sahiplenemez, **C2 regresyon kapısı** (`patches`/`priority_zones` calibrated manifest'e sızmaz). **C5 kalan deltası da bu commit'te:** `analysis_type.enum` v1.4.1→**v1.4.2** KG-0.f çapraz atfı (davranış değişikliği yok). **Doğrulama:** validate 89/0 · pytest 560+12 · breaking **0** | PATCH | — |
| **C1′** | **`schemas/platform/calibrated_dataset_manifest.v1`** → `outputs[].file_artifact`'e opsiyonel **`layer_type`** (ortho/ndvi/ndre/ndwi) + **`calibration_tier`** ekle. ⚠️ **Yeni `index_layers[]` dizisi AÇILMAZ** — `outputs[]`, `reflectance_scale` (`reflectance_0_1/0_100/scaled_int/unknown`) ve `producer_tool` **zaten mevcut**, tekrarlanmaz | MINOR | 0.a, 0.c, C0 |
| ✅ **C2′** | **YAPILDI (2026-07-31).** `PlatformForm`'a **`priority_zones`** eklendi (opsiyonel, `maxItems:500`) — EdgeForm ile **aynı zone verisi + aynı `required`**, ama `visualizations` **göreli yol değil nesne anahtarı** tutar. **Plandan bilinçli sapma:** EdgeForm'daki göreli yol **deprecate EDİLMEDİ** — edge hangi dosyaları ürettiğini bildirmek zorunda ve anahtarı üretemez; fiilen deprecate edilen *"bu yolu S3 anahtarı olarak kullanmak"* ve bu artık açıklamada yazılı. ⚠️ **Desen ölçülerek sertleştirildi:** ilk yazım tenant/dataset **biçimini donduruyordu** (platformun `dataset_…` önekiyle çakışırdı) **ve `a/../b` traversal geçiyordu**; biçim yerine **güvenlik-anlamlı yapı** zorlanıyor (mutlak yol RED · `..` RED · `/patches/` öncesi ≥2 segment ⇒ edge göreli yolu anahtar olarak **sızamaz**). 7 vaka ile doğrulandı. ⚠️ **`oneOf` ayrımı ölçüldü:** tek dayanağın `unevaluatedProperties` olduğunu varsaymıştım — gerçekte **üç katman** var (① unevaluated ② kimlik biçimleri `^batch_[a-z0-9]{24}$` ③ `files[].sha256_hash`↔`sha256`). Ayrım sağlam; test yine de iki örneğin **tam olarak bir** dala uyduğunu doğruluyor. **Kapı:** `tests/test_intake_manifest_forms.py` (16 test) + platform örneğine `object_key` gösterimi | MINOR | ✅ |
| **C2″** | Edge aynası: `priority_zone.py:31,55` regex + `max_length=128` `object_key` için genişletilir (vendored senkron) | — | C2′ |
| **C3′** | **`schemas/edge/calibrated_dataset_manifest.v1`** → `raw_frames[]` ekle (opsiyonel; yalnız seçilmiş kareler: `{object_key, frame_id, footprint_wkt, band}`). Kare seçimi kalibrasyon çıktısıdır → **edge formu** | MINOR | 0.c, C0 |
| **C4** ⚠️ | **İKİ KEZ DÜZELTİLDİ (2026-07-31).** ~~"contract kalemi değil"~~ hükmü de **eksikti.** Ölçüm: `sorties` **kanonik** contract'ta yok — ama **edge'in vendored interface sözleşmesinde VAR** (`tarlaanaliz-edge/interface/contracts/schemas/edge/intake_manifest.v1.schema.json`), üstelik `mission_date` ile birlikte. Yani bu bir **AK-4 edge-ileri sapmasıdır** (edge kanonikten önce re-pinlemiş), "yok" değil. **Ayrıca planın önermesi de yanlıştı:** *"bbox'ı zorunlu yapmak breaking"* — `bbox` o şemada **ZATEN `required`** (`sorties[].required = [sortie_id, field_id, crop_type, bbox]`). Yani karar verilecek bir şey kalmamış. **Gerçek durum:** `sorties` **dizisi** opsiyonel → hiç sortie yoksa bbox da yok → E9'un mixed-crop yolu. **Yapılacak → C11** | — | → **C11** |
| **C11** ⬜ | **AK-4 absorpsiyonu: `sorties[]` + `mission_date` kanoniğe alınsın.** Edge vendored sözleşmesinde canlı, kanonikte yok → I-5 gereği sapma **yalnız geçici** olabilir. `sorties[]`: `{sortie_id, field_id, field_name, crop_type, area_ha, planned_altitude_m, bbox}`, `required=[sortie_id, field_id, crop_type, bbox]`, dizi **opsiyonel** (geriye uyumlu) · `mission_date`: `["string","null"]`, `format: date`. Eklendiğinde `EdgeForm`'a girer (kaynak edge'dir) | MINOR | C0 |
| ~~**C5**~~ | ~~`analysis_type.enum.v1` → "üretilemez" notu~~ → **YAPILDI (v1.4.1'de mevcut, 2026-07-31 doğrulandı).** `BENEFICIAL → availability: enum_valid_not_yet_emittable` (*"model olgunluğuyla henüz emit edilemez"*) · `THERMAL_STRESS → requires_thermal_payload` (*"**Mavic 3M'de üretilemez**"*). İkisi de **makine-okunur**. Kalan tek delta: `changeNote`'a KG-0.f çapraz atfı → **C0 ile aynı commit** | — | — |
| ✅ **C9** | **YAPILDI (2026-07-31).** KR-093 kanonik registry'ye taşındı (`ssot/kr_registry.md`, 8 bölümlü format, platform normatif metninden; **KG-0.b-R eklentisi işaretli** + AK-4 çapraz-repo notu). `report_phase.enum.v1`'e **`x-preliminary-content`** kapalı listesi eklendi: **Aşama A** (kalibrasyon sonrası — `geom`/`ndvi_value`/`priority_level`/`ndvi_overlay`) · **Aşama B** (worker sonrası — ortho + HEALTH/NITROGEN_STRESS/WATER_STRESS + `overall_health_index`, **özgün tanım değişmedi**) · **`never`** (findings/detections/prescription…). `analysis_preliminary_ready.v1`'in faz-düzeyi *"ONLY"* iddiası **olayın kendi payload'ına daraltıldı**. ⚠️ **Ek bulgu:** contract'ın kendi `docs/TARLAANALIZ_SSOT_v1_2_0.txt` kopyası **KR-084'te bitiyor**, platform kopyası KR-093'e gidiyor — aynı adlı iki SSOT metni **ayrışmış** (hizalama ayrı kalem). **Platform borcu:** iki kopyanın aynalanması | MINOR | ✅ |
| ~~**C9-eski**~~ | ~~**KR-093 içerik tanımını genişlet (2026-07-31 denetimi).**~~ Bugün iki kanonik artefakt PRELIMINARY içeriğini **"YALNIZ/ONLY"** diyerek kapatıyor: `analysis_preliminary_ready.v1` (*"carries **ONLY** deterministic index layers (HEALTH/NITROGEN_STRESS/WATER_STRESS) + overall_health_index"*) ve `report_phase.enum.v1` (*"**Yalnız** deterministik indeks katmanları… sunulur"*). Y-D'nin göstereceği **öncelik bölgesi (poligon + `ndvi_value` + `ndvi_overlay`)** bu listede **YOK** → liste genişletilir. **Ön koşul: KR-093 kaydı `ssot/kr_registry.md`'ye taşınmalı (bugün KR-092'de bitiyor)** | MINOR | 0.b-R |
| ✅ **C10** | **YAPILDI (2026-07-31).** Mapping **kanonik adlarla** yeniden yazıldı ve Y-D anı eklendi: `UPLOADED`/`IN_ANALYSIS`/`PENDING_REVIEW` → `PRELIMINARY` · `DELIVERED` → `FULL` · `EXPERT_REJECTED` → WITHDRAWN(409). **`unlisted_status_behavior: FAIL-CLOSED`** eklendi — *"listelenmeyen = PRELIMINARY"* yasaklandı (aksi hâlde `DRAFT`/`PLANNED` ön rapor üretirdi). **`platform_internal_aliases`** ile platform çevrimi belgelendi. ⚠️ **Denetimde sanılandan büyük çıktı:** kanonik-dışı ad **iki taneydi** — `ANALYZING`(→`IN_ANALYSIS`) **ve `DONE`**(→`DELIVERED`), yani dört girişin ikisi. **Kapı kanıtlandı:** yeni test eski mapping ile düşüyor, yenisiyle geçiyor. **Platform borcu:** `results_service_impl.py:227` catch-all'u kanonik mapping'e daraltılmalı (P12 kabul kriteri) | MINOR | ✅ |
| ~~**C10-eski**~~ | ~~**`report_phase.x-derived-from.mapping`'i kalibrasyon-sonrasına aç.**~~ Bugün tam 4 giriş var (`ANALYZING/PENDING_REVIEW → PRELIMINARY`, `DONE → FULL`, `EXPERT_REJECTED → WITHDRAWN`); Y-D raporu **kalibrasyondan hemen sonra** gösteriliyor ve o an mission `UPLOADED` (`mission.py:84`) → **mapping'de karşılığı yok.** Bunun "çalışıyor" görünmesinin tek sebebi platform kodundaki catch-all `else PRELIMINARY` (`results_service_impl.py:227`) — yani platform **kanonikten geniş**. Ya `UPLOADED → PRELIMINARY` eklenir ya *"listelenmeyen statüler PRELIMINARY (fail-closed)"* yazılır. **Aynı turda:** mapping'deki **kanonik olmayan `ANALYZING`** adı `IN_ANALYSIS`'e çevrilir (`mission_status.enum.v1`'de `ANALYZING` yok; platform-içi ad — çeviri `mission.py:27`'de belgeli) | MINOR | 0.b-R, C9 |
| **C6** ⚠️ | **KOŞULLU AÇIK — "kapandı, iş yok" HÜKMÜ GERİ ALINDI (2026-07-31).** Enum kanonik olarak `ABSOLUTE / PANEL_ABSOLUTE / DLS2_RELATIVE / RELATIVE / NONE / AGNOSTIC` içeriyor ve `RELATIVE` = *"Saha-bazlı göreli kalibrasyon (ör. **DJI Mavic 3M çıktısı**)"*. **AMA** `x-context-subsets` ölçüldü: `edge/calibrated_dataset_manifest` alt kümesi **yalnız `["ABSOLUTE","RELATIVE"]`** — `DLS2_RELATIVE` **kabul edilmiyor** (buna karşılık `edge/intake_manifest` alt kümesi onu içeriyor). → **E13 kararı `DLS2_RELATIVE` çıkarsa contract değişikliği ZORUNLU** (alt küme + şema enum'u genişletilir; **MINOR, breaking değil**). `RELATIVE` çıkarsa iş yok. **Sıra düzeltmesi: E13 kararı C6'dan ÖNCE gelir** (planda ters yazılmıştı) | koşullu MINOR | **E13 kararı** |
| **C7** | `frame_analysis_job.v1` **yeni şema** — tekil kare analiz işi (doğrulandı: `schemas/worker/` altında **yok**) | MINOR | C1′, C3′ |
| **AL-C1** 🔴 | `expert_review_queue.v1` → `escalation_reason`'a **additive 7. değer `AUDIT_SAMPLE`**. Doğrulandı: kanonik **ve** worker vendored kopya **tam 6 değer**. Detay §11.2 | MINOR | — |
| **AL-C2** 🔴 | `expert_review_queue.v1` → `audit_sample: bool` + `audit_stratum: string` (platform-otoriter eksen: crop×layer×fenoloji). Detay §11.2 | MINOR | — |
| ✅ **C-SSOT** | **YAPILDI (2026-07-31) — iki SSOT kopyası hizalandı.** `docs/TARLAANALIZ_SSOT_v1_2_0.txt` contract kopyası platform kopyasıyla **bayt-özdeş** hâle getirildi (git'te ikisi de LF). **Ölçüm:** platform 4 KR fazla (**KR-088/091/092/093**), contract'ta **fazla KR yok**; 27 contract-only satırın tamamı bayat (eski başlık · **IL_OPERATOR** metni — contract'ın kendi `role.enum.v1`'i `DISTRICT_REP` kanonik/`IL_OPERATOR` DEPRECATED diyor · 2026-06-14 öncesi KR-024 tablosu) → **kaybedilen özgün içerik yok.** **Kapı:** `tests/test_kr_reference_integrity.py` (10 test) — her `x-kr-ref` KR'si iki kanonik kaynağın **birleşiminde** tanımlı olmalı; hizalama-öncesi durumda **düşüyor** (kanıtlandı). ⚠️ **Yan bulgu 1:** `ssot/kr_registry.md` yalnız **6 KR** tutuyor (088–093), tam korpus SSOT metninde (~49) — `CLAUDE.md`'nin *"kanonik kaynak kr_registry.md"* ifadesi **yanlıştı, düzeltildi.** ⚠️ **Yan bulgu 2:** KİRAZ çelişkisi üçüncü kaynağa yayıldı (bkz. KG-0.d-EK) | — | ✅ |
| ✅ **C-PARITE** | **YAPILDI (2026-07-31) — 9 yanlış parite iddiası düzeltildi.** Dokuz kanonik şema *"... interface/contracts/... ile **birebir uyumludur**"* diyordu; ölçüldü: **9/9'u bayt düzeyinde YANLIŞ**, ama **9/9'unun `properties` + `required` kümeleri birebir aynı**. Tek fark tutarlı bir idiom: kanonik `unevaluatedProperties: false` ↔ vendored `additionalProperties: false`. 9/9'da aynı olması bunun **çürüme değil bilinçli konvansiyon** olduğunu gösteriyor → **yanlış olan iddianın ifadesiydi.** Dokuz açıklama da gerçek sözleşmeyi anlatacak biçimde düzeltildi. **Kapı:** `tests/test_vendored_parity.py` (38 test) — parite + *"birebir uyumludur"* ifadesinin geri gelmesini yasaklayan sözcük kapısı (kanıtlandı: eski ifade dönünce düşüyor) + idiom farkının belgeli kalması. ⚠️ **Kapı kendi eksik düzeltmemi yakaladı:** ilk turda 6 şema bulmuştum, test kalan **3'ünü** (worker `calibration_metadata`/`expert_feedback`/`expert_review_queue`) gösterdi. **Not:** kardeş depo yoksa test **atlar** (skip), CI'da yeşil sanılmasın | — | ✅ |
| **C-VENDOR** ⬜ | **C8'de yapılacak vendored yayılımı:** ① worker `interface/contracts/analysis_type.enum.v1.json` **v1.4.1** → kanonik **v1.4.2** (C0'da bump edildi; enum dizisi aynı, yalnız `changeNote`) ② edge vendored `calibrated_dataset_manifest` + `intake_manifest` bu turun değişikliklerini almalı ③ dokuz şemanın düzeltilmiş açıklaması vendored kopyalara da yansır. **Bugün kırık yok:** worker/edge kendi hash kapılarını kullanır (I-4), ama sürüm dizesi hizası C8'in şartıdır (I-1) | — | C8 |
| **C-SSOT-2** ⬜ | **Kök neden açık:** `docs/TARLAANALIZ_SSOT_v1_2_0.txt` **hiçbir senkron aracının kapsamında değil** (`tools/sync_to_repos.sh` yalnız `schemas/`+`enums/`+`CONTRACTS_VERSION.md` taşıyor). Bu yüzden iki kopya sessizce ayrıştı. → Dosya, worker'daki gibi **salt-okunur drift dedektörüne** eklenmeli (kopyalama değil, uyarı). *Şimdi yapılmadı: rsync yolu burada test edilemez, körlemesine tooling değişikliği yapılmadı.* | tooling | — |
| **C8** | **Release töreni (I-1..I-5):** sürüm bump → **annotated `vX.Y.Z` tag** → `CONTRACTS_SHA256.txt` → platform submodule pin → worker vendor alt-kümesi → 3 repoda sürüm dizesi hizası. ⚠️ **Edge formuna dokunan her değişiklik** (C2′/C3′/C6) edge `interface/contracts/` vendored kopyası + **KR-041 hash** turunu da tetikler — şema açıklaması *"birebir uyumludur"* diyor | **zorunlu** | tur içeriği |

⚠️ **C8 her contract turunda tekrarlanır ve +1-2 gün maliyeti vardır.** İki tur:

> ### 🔒 TUR TANIMI — KANONİK (2026-07-31 denetimiyle yeniden tanımlandı)
>
> **TUR 1 = C0 + C1′ + C2′ + C2″ + C3′ + C9 + C10 + AL-C1 + AL-C2** *(+ C6 koşullu, E13 kararına bağlı)*
> **TUR 2 = C7** (tekil görüntü, demo sonrası)
>
> **📍 Tur 1 ilerleme (dal: `feat/contract-tur1`)** — ✅ C0 · ✅ C9 · ✅ C10 · ✅ C-SSOT · ✅ C-PARITE ·
> ✅ C2′ · ✅ C1′ · ✅ C3′ · ✅ **AL-C1** · ✅ **AL-C2** · ⬜ C6 *(E13 bekliyor)* ·
> ⬜ C2″ *(edge turu)* · ⬜ **C8 töreni**
> **⇒ Contract tarafı şema kalemleri TAMAM.** Kalan: C6 (E13'e bağlı) · edge turu · C8.
> *(demo kritik yolunun ⓪ adımı — P6/P12'nin ön koşulu — kapandı)*
>
> ⚠️ **Tur boyunca `pin_version.py --verify` KIRMIZIDIR** — agrega checksum bilerek re-pin
> edilmez; ara re-pin yayımlanmış `7.2.0` etiketinin checksum anlamını bozar. Tek re-pin noktası
> **C8**'dir. (`test_pin_version::test_real_repo_checksum_verifies` bu yüzden tur boyunca düşer;
> diğer 560 test yeşil kalmalıdır.)
>
> **Neden AL-C1/C2 Tur 1'de:** ikisi de saf **additive** (1 enum değeri + 2 opsiyonel alan) → aynı MINOR'a
> sığar; **[0] ölçüm temelinin tek açılabilir kilidi** (§11.5) ve C8 töreni tur başına +1-2 gün.
> Tur 2'ye ertelenirse dedup canlı bağlama + S2 bütçesi demo sonrasına kayar.
> *(Bu, §11.2'deki eski "C-Tur-2 ile birleştirilebilir" ifadesini **yürürlükten kaldırır**.)*
>
> **Neden C4 ve C5 listede yok:** C4 contract kalemi değil (edge'e taşındı) · C5 zaten yapılmış.

## 3.2 EDGE (`tarlaanaliz-edge`)

| # | İş | Dosya | Bağımlılık |
|---|---|---|---|
| **E1** | **Dev-station build profili** — M1+M2 rolü tek makinede; hangi gevşetmeler yapıldı, denetime yazılır | `config/build_profiles.yaml`, `src/infrastructure/platform/build_profile.py` | 0.e |
| **E2** | **S3/MinIO istemcisi** (bugün repo genelinde 0 eşleşme) | yeni: `src/infrastructure/network/object_store_client.py` | 0.a |
| **E3** | `cloud_client.submit_manifest()` **çağrılır hale gelsin**; `upload_chunk()` → **presigned PUT**'a çevrilsin (`octet-stream` + `X-Chunk-Index` kaldırılır) | `src/infrastructure/network/cloud_client.py:140,218,246-248` | E2, P1 |
| **E4** | Yükleme akışı: manifest → presigned PUT'lar → complete. `ingest_path` ile nesne ucu ayrıştırılır | `src/core/services/sync/uploader.py:180,289` | E3 |
| **E5** | `platform_ref` yalnız `complete` yanıtından yazılsın (SSOT §15 korunur) | `src/core/services/sync/upload_receipt_writer.py` | E4 |
| **E6** | **`CalibrationEngineRunner` protokolü** + **`TerraRunner`** (⚠️ **"Terra'nın CLI'si YOK" iddiası TEYİTLİ DEĞİL — bkz. 0.g ikinci açık kalem; DJI'dan yazılı cevap gelmeden kod yazılmaz.** Güvenli varsayım: runner = **çıktı klasörü izleyici**, süreç başlatıcı değil — CLI çıkarsa izleyici yine çalışır, tersi doğru değil) + **`OdmRunner`** (Docker CLI). Uydurma `--headless` argv'si kaldırılır. *(FAZ 1'de `MetashapeRunner`: doğru başsız komut **`metashape.sh -platform offscreen -r script.py`** — `-platform offscreen` olmadan sunucuda açılmaz; API referansı `metashape_python_api_2_3_0.pdf`)* | `src/core/services/calibration_gate/pix4d_runner.py` → yeniden adlandır | 0.d |
| **E7** | `_discover_output` dosya adları **config'den**. ⚠️ **DJI Terra çıktı adları resmi dokümanda tam yayınlanmamış** — yalnız `dsm.tif` / `gsddsm.tif` teyitli; DOM ve bant/indeks raster adları belirtilmemiş. **Tahminle yazılamaz, ilk koşumda ölçülecek** (ölçüm #2) | aynı dosya | E6, ölçüm #2 |
| **E8** | `ndvi_thresholds.yaml` + `phenology_calendar.yaml` → ⚠️ **KAPSAM DÜZELTİLDİ (0.d ek bulgusu):** sıra **① KİRAZ kararı** (bugün `bookable:True` ama hem wire-enum'da hem edge tablosunda YOK → sipariş edilebiliyor, iş iki yerden düşüyor; ya `bookable:False` ya enum+tablo) → **② WHEAT** (wire-enum'da var, tek eksik tablo) → **③ SUNFLOWER/OLIVE ertelenebilir** (`bookable:False`, sipariş edilemez → zararsız). Bugün edge'de 5 ürün (COTTON/CORN/PISTACHIO/GRAPE/RICE), contract'ta 8 | `config/processing/` · contract `crop_type.enum.v1` (① için) | ① ürün kararı |
| **E9** ⚠️ | **YENİDEN YAZILDI (2026-07-31) — gerekçe bayattı.** Eski metin *"`PRIORITIZATION_MIXED_CROP` **sessiz** çöküşü yerine açık hata"* diyordu; **çöküş zaten sesli:** `calibration_pipeline.py:207` yorumu *"instead of happening silently"*, `:230` olay yayılıyor, `custody_logger.py:93` kanonik denetim olayı, `:399` docstring *"audited rather than silent"*. → **Gerçek karar:** MIXED_CROP **denetim uyarısı mı, sert hata mı?** Öneri: **pilotta uyarı** (mixed-crop tarla uçuşu bloke etmesin), **üretimde sert hata**; `build_profiles.yaml` üzerinden profillenir → **E1 ile birleşir**. Ayrıca **eski C4'ün konusu (`sorties[].bbox` zorunlu mu)** buraya taşındı: bu **edge-yerel manifest kararıdır** (`aggregator.py:101,151`), contract turu gerektirmez | `src/core/services/pipeline/calibration_pipeline.py:207,230` · `config/build_profiles.yaml` | **E1** (C4 değil) |
| **E10** 🔴🔴 | **DEMO KRİTİK YOLU ②.** Yama görselleri → **nesne anahtarı** (göreli yol yerine) + presigned PUT ile yükleme. ⚠️ **Bugün `ndvi_overlay` yerel diske yazılıp manifeste göreli yol konuyor** → **kırmızı NDVI görseli merkeze hiç ulaşmıyor.** KG-0.b-R'nin göstermek istediği görsel tam olarak bu. Bu madde olmadan ÖN RAPOR'da poligon + NDVI değeri gelir, **görsel gelmez** | `src/core/services/pipeline/calibration_pipeline.py:332-336` | **C2′**, E2 |
| **E11** | **Kare seçici (frame selector)** — EXIF footprint (GPS+yaw+H+GSD) + ODM `shots.geojson` ile işaretli yamayı gören kareleri bul | yeni: `src/core/services/frames/frame_selector.py` | **C3′**, ölçüm #5 |
| **E12** 🔴 | `ENABLE_NDVI_PRIORITIZATION` bayrağını **AÇ** — ⚠️ **statü değişti (KG-0.b-R):** artık "ertelenebilir" değil, **ÖN RAPOR'un ön koşulu.** Bayrak kapalıyken `priority_zones` **hiç üretilmez** → `analysis_priority_zones` boş → P6/P12 gösterecek bir şey bulamaz → demo çöker. **P9 uyarısı hâlâ geçerli ama ölçek farklı:** kota sıçraması 28.000 dönüm/gün için hesaplanmıştı; **pilotta günde 3-5 tarla** olduğu için uzman yükü ihmal edilebilir. → **Pilotta AÇ**, üretim ölçeğine geçmeden önce kotayı yeniden ölç. 🔴 **ÖN KOŞUL EKLENDİ (2026-07-31): P9a olmadan AÇILMAZ.** §10.5/§11.5 kuralı *"E12, KİLİT-2 kapalıyken açılmaz; ya dedup bağlanır ya kota manuel sınırlanır"* diyordu ama **iki kaçış yolundan hiçbiri bir iş kalemine bağlı değildi** (tek kota kalemi P9, Dalga 4'te = demodan sonra). KİLİT-2 gerçekten kapalı: `should_send_to_expert` **çağrısız** (`prototype_manager.py:546`). → Kaçış yolu **P9a** olarak Dalga 2'ye alındı | `src/shared/config.py:160`, `.env.example:113` | E4 sonrası · **P9a** · **demo öncesi zorunlu** |
| **E13** ⚠️ | `calibrated_validator` → manifeste **motor adı** + **`calibration_result.calibration_type`** yazsın. **Alan adı düzeltmesi (2026-07-31):** planda geçen `calibration_tier` contract'ta **yok**; kanonik ad `calibration_result.calibration_type`. **Karar E13'te verilir ve C6'yı tetikler:** `RELATIVE` → contract işi yok · `DLS2_RELATIVE` (M3M'de dahili ışık sensörü var) → **C6 zorunlu**, çünkü `edge/calibrated_dataset_manifest` alt kümesi bugün yalnız `["ABSOLUTE","RELATIVE"]` | `src/core/services/calibration_gate/calibrated_validator.py` | C1′ · **C6'dan ÖNCE** |
| **E14** 🔴 | **KALİBRASYON KANITI ÜRETİCİSİ — EN ÖNCELİKLİ İŞ.** `calibration_result` ve `observed_footprint_wkt` **beş yerde tüketiliyor, sıfır yerde üretiliyor**: ① `sync.py:207-255` → `calibration_result.json` **dosyasını** ve **üst düzey** `observed_footprint_wkt`'i şart koşuyor, yoksa HC-05 upload kapısı `FAILED` ② `calibrated_validator.py:114-122` → **manifest alanı** `calibration_result`'ın 4 alt alanını şart koşuyor (`tool_name`, `tool_version`, `observed_footprint_wkt`, `calibration_type` — contract'ta hepsi **required**) ③ `qc_report_writer.py:245-256,341` → coverage'ı bundan hesaplıyor ④ `package_assembler.py:52` → dosyayı paketliyor ⑤ `dataset.py:123-125` → `calibration_result_ref` yoksa CALIBRATED geçişi `ValueError`. **`calibration_pipeline.run()` bunu `calibrated_manifest_path` olarak GİRDİ alıyor** ve docstring'i "upstream'de Pix4Dfields + `calibration_proof_checker` üretir" diyor — ama proof_checker yalnız **karşılaştırıyor**, üretmiyor. → **İki artefakt üretilmeli:** standalone `calibration_result.json` + manifest içi nested alan. `observed_footprint_wkt` ortho GeoTIFF extent'inden hesaplanır (KR-065 **ödeme** girdisi). ⚠️ **Bu iş C13'ten ÖNCE gelir:** boru bağlansa bile HC-05 **M1'in kendi içinde** takılır | yeni `src/core/services/calibration_gate/calibration_result_writer.py` | E6, E13 |

## 3.3 WORKER (`tarlaanaliz-worker`)

| # | İş | Dosya | Bağımlılık |
|---|---|---|---|
| **W1** | **M3M radyometrik zinciri — KAPSAM KÜÇÜLDÜ (2026-07-30 doğrulaması).** ✅ ODM resmi dokümanı: `--radiometric-calibration camera` **siyah seviye + vinyetleme + satır gradyanı/kazanç/pozlama** düzeltmelerini **zaten uyguluyor**; `camera+sun` buna **DLS spektral radyans + güneş açısı** ekliyor; çıktı **reflektans**. → **Ortomozaik yolunda 5 adımlı zinciri elle yazmaya gerek YOK.** İş yalnızca **tekil kare (İP-6) yolunda** gerekiyor — ve orada da ODM açık kaynak (AGPL) olduğu için **referans uygulama elinizde**, DJI PDF'inden sıfırdan türetmek zorunda değilsiniz. ⚠️ **Risk:** `camera+sun` resmî olarak **"deneysel"** — pilotta `camera` ile karşılaştırmalı ölçün | `src/preprocessing/radiometric/` (yalnız tekil kare yolu) | ölçüm #4 |
| **W2** | **Reflektans ölçeği motor başına** (ODM 0-1, Metashape 32768, Terra ölçülecek). Bugün ODM varsayımı gömülü | `scripts/orthomosaic_to_tiles.py:224,284` | E13 |
| **W3** | **ODM'yi M3M için uyarla.** Mevcut script MicaSense RedEdge 3'e ve sabit uçuş adlarına bağlı. Gerekli resmî bayraklar (doğrulandı): `--radiometric-calibration camera+sun` · `--primary-band <ad>` (varsayılan `auto`) · **`--skip-band-alignment`** (homography ile ön-hizalama yaptıysanız) · `--orthophoto-resolution <cm/px>` (varsayılan 5, GSD tahminiyle sınırlanır) · `--feature-quality medium` · `--skip-3dmodel` | `scripts/odm_run_botrytis.sh` → genelleştir `scripts/odm_run.sh` | ölçüm #5 |
| **W4** | **İkinci girdi tipi: `raw_frame`** — `pipeline.py` bugün **yalnız GeoTIFF** kabul ediyor (magic-byte guard, "inputs are GeoTIFF orthomosaics") | `src/core/services/inference/pipeline.py` | C7 |
| **W5** | **RGB↔ÇS eş-kayıt (co-registration)** — RGB, ÇS'den **1,71× daha ince** (GSD 37,2 vs 21,7) + M3M bant kayması | yeni modül | W1, W3 |
| **W6** | **Etiket şeması düzeltmesi** — "böcek türü/sayısı" → **"zararlı hasar izi sınıfı + şiddeti"**; `BENEFICIAL` ve `THERMAL_STRESS` üretilemez olarak işaretli kalır | eğitim etiket şeması + `sub_specialty_resolver.py` | 0.f, C5 |
| **W7** | **Veri seti boşluğu kararı** — COTTON, PISTACHIO, RICE, SUNFLOWER'ın eğitim veri seti yok. Karar: temin mi, erteleme mi? (Demo bunu ÖN RAPOR ile aşıyor — §2.1) | `config/*_datasets.yaml` | 0.d |

## 3.4 PLATFORM (`tarlaanaliz-platform`)

| # | İş | Dosya | Bağımlılık |
|---|---|---|---|
| **P1** | `POST /ingest/manifests` yanıtına **presigned PUT URL listesi** ekle (süre + bucket + anahtar kapsamı kısıtlı) | `src/presentation/api/v1/endpoints/ingest.py:363,371` | 0.a |
| **P2** | **Yeni uç `POST /ingest/complete`** — nesneler yüklendi, hash doğrula, Dataset `RAW_INGESTED` | aynı dosya | P1 |
| **P3** | Presigned üretimini **ingest anahtarlarına genişlet** + anahtar şeması `{tenant}/{dataset_id}/{raw\|layers\|patches}/{ad}`. ✅ `generate_presigned_url` **zaten var** (`patches.py:165`) → PUT yönü + kapsam kısıtı eklenecek. 🔴 **ANAHTARI PLATFORM ÜRETİR — edge'in verdiği yol ASLA imzalanmaz** (0.a ek şartı). "Edge'in anahtarını doğrula" biçiminde uygulamak YETERSİZDİR | `src/infrastructure/external/storage_adapter.py` | P1 |
| **P4** ⚠️ | `patches.py` → **object_key zorunlu**; yoksa **açık hata** (bugünkü sessiz 404 yerine). 🟠 **Güvenlik yarısı — 2026-07-31'de DÜZELTİLDİ:** eski metin *"anahtar DB'den okunur"* diyordu; **kod bunu zaten yapıyor** (`patches.py:151` → `viz_paths = patch_row.visualization_paths`; platformdaki **tüm** presign çağrıları `:165/:169/:173` oradan besleniyor, istekten anahtar alan **hiçbir** çağrı yok) → **kural işlevsizdi (no-op)** ve P4'ün güvenlik yarısını "yapılmış" gösteriyordu. **Doğru kural:** *anahtar DB'den okunur **VE DB'ye yalnız platformun ürettiği anahtar yazılır**; edge'in önerdiği yol hiçbir aşamada kalıcılaştırılmaz* → `ingest_service_impl.py:266`'daki `pz.visualizations.model_dump()` passthrough'u değişir. **Şiddet düzeltmesi:** anlık risk **çapraz-kiracı değil**; `patches.py:118-148`'de gerçek sahiplik kapısı var (`DatasetModel ⨝ ExpertReviewModel` → `403 PATCH.OWNERSHIP_DENIED`), sömürü **ele geçirilmiş edge + o mission'a atanmış uzman** ister. **Kabul testi iki koşullu kurulur** — tek koşullu test bugün de yeşil geçer, hiçbir şey kanıtlamaz | `patches.py:118-175` · `ingest_service_impl.py:258-266` | **C2′**, E10 |
| **P5** | **C15 (Y-C):** `DATASET.STATE_TRANSITION → CALIBRATED` üzerinden çiftçiye **durum bildirimi** ("uçuşunuz işlendi, analiz sürüyor"). ⚠️ `results_service_impl` ve `report_phase` **DEĞİŞMEZ** — ADR-007 korunur | `src/infrastructure/messaging/`, `farmer_notifier` | 0.b |
| **P6** 🔴 | **ÇİFTÇİ ÖN RAPOR UCU — yeniden tanımlandı (KG-0.b-R).** ~~layer_registry'ye yazmak~~ **değil**: `analysis_priority_zones`'u çiftçiye açan **okuma ucu**. Döndürür: `geom` (GeoJSON Polygon) + `ndvi_value` + `priority_level` + **presigned `ndvi_overlay` URL'i**. **Kapılar:** ① sahiplik (çiftçi yalnız kendi tarlası) ② **KR-033 ödeme** ③ `report_phase == PRELIMINARY` ④ **tespit/`findings` ASLA** ⑤ KR-071 PII yok. Bugün bu tabloyu `worker_dispatch_handler`, `expert_review_prioritization_service`, `worker_bridge_consumer.py:1088` (kota) ve `worker_job_publisher.py:115` okuyor — **çiftçi ucu yok** ✅ (2026-07-31 doğrulandı). ⚠️ **ÖN KOŞUL EKLENDİ: C9 + C10.** Kanonik tanım bugün PRELIMINARY içeriğini *"YALNIZ 4 kalem"* diye kapatıyor (öncelik bölgesi listede yok) ve `report_phase` mapping'inde **kalibrasyon-sonrası statü yok**; ikisi düzeltilmeden bu uç kanonik tanımın dışına çıkar | yeni uç (öneri `GET /missions/{id}/preliminary`) + `analysis_priority_zone_repository_impl` | 0.b-R · **C9 · C10** · C13 · E12 |
| **P12** 🔴 | **PRELIMINARY için ikinci içerik kaynağı.** `results_service_impl.py:227` fazı zaten `PRELIMINARY` veriyor ama içerik **worker sonucundan** geliyor; worker sonucu yokken ÖN RAPOR boş kalır. → Worker sonucu **YOKKEN** öncelik bölgelerinden sun; **geldiğinde** mevcut davranış aynen sürsün. `raw_findings` kırpması (`:247`) **değişmez** (satır 227/247 birebir doğrulandı). ⚠️ **Kabul kriteri eklendi (2026-07-31):** dönen `report_phase` değeri **C10'un kanonik mapping'ine karşı** test edilir. Bugün `:227` bir **catch-all** (`"FULL" if DONE else "PRELIMINARY"`) — yani platform kanonik mapping'den **geniş**; C10 bunu kanonikleştirmeden P12 doğrulanamaz | `src/application/services/results_service_impl.py` | 0.b-R · P6 · **C9 · C10** |
| **P7** | **TKGM feature flag'ini AÇ** — kod hazır (`tkgm_rest_adapter.py`, `tkgm_megsis_wfs_adapter.py`, idari cache, `GET /parcels/lookup|reverse-lookup|validate`, `settings.py:212`). **Yalnız kurumsal protokol geldikten sonra** | `src/infrastructure/config/settings.py:212` | TKGM protokolü |
| **P8** | `contracts` submodule pin + `CONTRACTS_SHA256.txt` güncelle (her contract turundan sonra) | repo kökü | C8 |
| **P9** | **Uzman kotası — ölçek-koşullu uyarı (KG-0.b-R ile revize).** `analysis_priority_zones` dolunca kota 1→N sıçrar. ⚠️ Eski hâli "E12 ile aynı sürümde açılmasın" idi; **E12 artık ÖN RAPOR için zorunlu.** Uzlaşma: **pilotta aç** (günde 3-5 tarla → yük ihmal edilebilir), **üretim ölçeğine geçmeden ÖNCE** gerçek uzman kapasitesini ölç ve kotayı sınırla. 🔴 **İKİYE BÖLÜNDÜ (2026-07-31)** — çünkü §10.5/§11.5'in tanıdığı iki kaçış yolundan **hiçbiri bir iş kalemine bağlı değildi** ve P9 demodan sonraydı | `worker_bridge_consumer.py:1085-1112` | ↓ |
| **P9a** 🔴 | **PİLOT KOTA TAVANI — Dalga 2, E12 ile AYNI sürümde.** `daily_image_capacity` için sabit üst sınır + aşımda kuyruğa alma. Bu, §10.5'in *"kota manuel sınırlanır"* kaçış yolunun uygulamasıdır ve **E12'nin ön koşuludur** (KİLİT-2 kapalı: `should_send_to_expert` çağrısız) | `worker_bridge_consumer.py:1085-1112` | **E12 ile aynı sürüm** |
| **P9b** | **Gerçek uzman kapasitesi ölçümü + kalıcı kota** (S2 bütçesi B girdisi) | aynı dosya | Dalga 4 · **üretim öncesi kapı** |
| **P10** | **POLİGON-KMZ çıktısı ekle.** Mevcut generator **waypoint** rotası üretiyor (docstring: "DJI Ground Station veya Litchi"). Haritalama görevinde Pilot 2'ye **waypoint değil poligon** verilmeli — Pilot 2 o zaman bindirme / gimbal −90° / shutter tetiklemesini **kendisi** kurar. Waypoint KMZ'de fotogrametri parametreleri kaybolur | `src/core/domain/services/flight_route_generator.py:331` (`flight_route_to_kmz`) | 0.d |
| **P13** ⬜ | **Doküman çelişkisi (2026-07-31 taraması):** `docs/architecture/end_to_end_workflow.md` **satır 30** *"C13/C15/C16/**C17** açık"* diyor, ama aynı dosyadaki **C17 satırı "ÇÖZÜLDÜ (2026-07-29, Faz 3)"**. Başlık özeti bayat → C17 listeden çıkarılmalı. Aynı turda C13/C15/C16 durum güncellemeleri de işlenir (metinler §9.1-B'de hazır) | `docs/architecture/end_to_end_workflow.md` | — |
| **P11** | *(uzun vade)* **WPML üretimi** — `.kmz` içinde `template.kml` + `waylines.wpml` (DJI Cloud API açık spesifikasyonu). Pilot cihaza dokunmadan görev gönderimi | aynı dosya | P10 |

## 3.5 WEB / ARAYÜZ (`tarlaanaliz-platform/web`) — 🆕 2026-07-31 denetiminde eklendi

> **Neden yoktu:** Planın §3 tabloları yalnız contract/edge/worker/platform-backend kapsıyordu.
> Demo kritik yolunun ①–⑥ adımlarının **hepsi** şema/edge/backend'de bitiyordu — çiftçinin
> **görmesi** için bir ekran yoktu. Plan geneli tarandı (`web|frontend|PWA|Next.js|arayüz|ekran|UI`):
> **sıfır** iş kalemi. Oysa `tarlaanaliz-platform/web/` (`web/package.json`) mevcut ve
> `docs/REPO_BOUNDARY_RULES.txt` `tarlaanaliz-web`'i **bağlayıcı** biçimde ayrı tüketici sayıyor.
> KG-0.b-R'nin direktifi *"çiftçi tarlasındaki sorunlu kırmızı NDVI bölgelerini **görsün**"*di.

| # | İş | Dosya/alan | Bağımlılık |
|---|---|---|---|
| **WEB1** 🔴🔴 | **DEMO KRİTİK YOLU ⑦ — ÖN RAPOR EKRANI.** Tarla haritası üzerinde `analysis_priority_zones` poligonları (`geom`), `ndvi_value`'ya göre renk skalası (kırmızı = sorunlu), poligona tıklayınca presigned **`ndvi_overlay`** görseli. Başlık: **"ÖN RAPOR"**. Kaynak: P6 ucu | `tarlaanaliz-platform/web/` | **P6** · P12 |
| **WEB2** 🟠 | **Kapı ve boş-durum mesajları:** ödeme kapılı (KR-033) · henüz bölge üretilmedi · `report_phase == FULL`'a geçince tam rapora yönlendirme · tespit **asla gösterilmez** (KR-019) | aynı | WEB1 |

⚠️ **Takvim etkisi:** Dalga 2 **+3-5 gün** uzar. WEB1 olmadan demo, API cevabında kalır.

---

# 4. İŞ AKIŞI (haftalık operasyonel döngü)

```
PAZARTESİ   Hava + güneş yüksekliği takvimi → haftanın uçuş günü/saati kesinleşir
            Kart hazırlığı (25 m'de kart başına 4-5 uçuş → kaç kart?)
                │
SALI        UÇUŞ GÜNÜ — 8-10 uçuş, tek irtifa (35 m), aynı KMZ'ler
            Her uçuş: panel öncesi + sonrası, gimbal −90°, güneş >30°
            Her sortie'ye bbox (aksi hâlde ürün tek ürüne çöker)
                │
SALI akşam  Kartlar → masaüstü. TERRA ile işle. Süre/RAM/boyut kaydet
                │
ÇARŞAMBA    Aynı veriyi ODM ile işle (çapraz kontrol)
            Terra-NDVI ↔ ODM-NDVI fark raporu
                │
PERŞEMBE    QC: kapsama oranı, bant tamlığı, CRS, bulanıklık
            Başarısız uçuşlar not edilir, tekrar penceresi belirlenir
                │
CUMA        Ölçüm tablosuna satır ekle; geçen haftayla NDVI farkı
            Zaman serisi grafiği güncellenir
                │
HAFTA SONU  SOP düzeltmeleri (irtifa/saat/panel yeri) + bir sonraki hafta planı
```

**Her uçuşta doldurulacak kayıt:** tarih/saat · tarla (ada/parsel) · ürün + fenolojik evre ·
güneş yüksekliği · hava · irtifa/bindirme · panel (öncesi ✓ sonrası ✓ gölgesiz ✓) ·
görüntü sayısı RGB/ÇS · Terra süresi · ODM süresi · tepe RAM · çıktı GB · kapsama oranı · not.

**Pilotta ölçülecek 4 metrik (demoda kullanılacak):**
1. **Verim:** dönüm/saat · 2. **Depolama:** GB/dönüm · 3. **Kalite:** kapsama oranı + QC geçme %
4. **Tutarlılık:** Terra-NDVI ↔ ODM-NDVI farkı ⟵ **en kritik.** Büyük fark, ileride motor
   değiştirmenin eğitim verinizi geçersiz kılacağı anlamına gelir.

---

# 5. SIRALAMA VE TAKVİM

## 5.1 Dalga şeması

```
ADIM 0  KARAR GÜNÜ (7 karar)                                    1 gün, kod yok
   │
   ├─ DALGA 1 — TEMEL (paralel yürür)
   │   ├─ E: 🔴 E14 KALİBRASYON KANITI ÜRETİCİSİ ⟵ İLK İŞ     3-4 gün
   │   │      (C13'ten ÖNCE — yoksa HC-05 M1'in içinde takılır)
   │   ├─ C: Tur 1 = C0+C1′+C2′+C2″+C3′+C9+C10+AL-C1+AL-C2    4-6 gün
   │   │      (+C6 koşullu · C4 düştü · C5 zaten yapılmış) + C8 töreni
   │   │      ⟵ C0 ve C9/C10 diğerlerinin ÖN KOŞULU
   │   ├─ E: E1 dev-station (+E9 profili) · E2 S3 · E8 YAML    4-6 gün
   │   ├─ P: P1,P2,P3 presigned + complete ucu                 4-6 gün
   │   └─ W: W3 ODM'yi M3M'e uyarla · W6 etiket şeması         3-5 gün
   │        ⟵ PİLOT BU DALGA SÜRERKEN BAŞLAR (kod beklemez)
   │
   ├─ DALGA 2 — HAT BAĞLANIR (Dalga 1 bitince)
   │   ├─ E: E3,E4,E5 (C13 kapanır) · E6,E7,E13 runner         6-9 gün
   │   ├─ P: P4 patches · P5 durum bildirimi                   4-6 gün
   │   │
   │   ├─ 🔴🔴 DEMO KRİTİK YOLU (KG-0.b-R) — sırayla, hepsi zorunlu:
   │   │   ⓪ C9+C10 kanonik ÖN RAPOR tanımı              (C-Tur-1'de)
   │   │        (içerik listesi "YALNIZ 4 kalem" + mapping'de
   │   │         kalibrasyon-sonrası statü YOK → ikisi de açılmalı)
   │   │   ① C2′ intake_manifest PlatformForm object_key  (C-Tur-1'de)
   │   │   ② E10 ndvi_overlay → GERÇEK nesne anahtarı      2-3 gün
   │   │        (bugün yerel göreli yol → görsel merkeze ULAŞMIYOR)
   │   │   ③ E12 ENABLE_NDVI_PRIORITIZATION = true         0,5 gün
   │   │        (kapalıyken priority_zones HİÇ üretilmiyor)
   │   │        ⚠️ ÖN KOŞUL: P9a kota tavanı (KİLİT-2 kapalı)
   │   │   ④ P4  patches object_key + anahtar sahipliği    1-2 gün
   │   │   ⑤ P6  çiftçi ÖN RAPOR okuma ucu                 2-3 gün
   │   │   ⑥ P12 PRELIMINARY ikinci içerik kaynağı         2-3 gün
   │   │   ⑦ WEB1 ÖN RAPOR EKRANI  🆕                      3-4 gün
   │   │        (⑥'ya kadar her şey API'de biter; ekran YOKTU)
   │   │   ───────────────────────────────────────────────────────
   │   │   ⚠️ Herhangi biri eksikse çiftçi KIRMIZI GÖRSELİ göremez:
   │   │      ⓪'sız kanonik dışı · ②'siz görsel yok · ③'süz bölge yok
   │   │      ⑤/⑥'sız veri yok · ⑦'siz EKRAN yok
   │   ├─ P: P9a pilot kota tavanı (E12 ile aynı sürüm)        1 gün
   │   ├─ WEB: WEB1 ÖN RAPOR ekranı · WEB2 kapı mesajları      4-5 gün
   │   ├─ W: W2 reflektans ölçeği                              2-3 gün
   │   └─ E: E10 yama nesne anahtarı (C16 kapanır)             2-3 gün
   │        ⟵ DEMO BU DALGA BİTİNCE MÜMKÜN
   │
   ├─ DALGA 3 — TEKİL GÖRÜNTÜ (demo sonrası)
   │   ├─ C: Tur 2 (C7) + C8 töreni                            2-3 gün
   │   ├─ W: W1 M3M radyometrik zinciri ⟵ EN BÜYÜK           8-12 gün
   │   ├─ E: E11 kare seçici                                   4-6 gün
   │   ├─ W: W4 raw_frame girdi tipi · W5 eş-kayıt             6-9 gün
   │   └─ W: W7 veri seti kararı                               karar
   │
   └─ DALGA 4 — AYRI SÜRÜM
       ├─ P9b uzman kapasitesi ölçümü + kalıcı kota           1 gün
       │     ⟵ ÜRETİM ölçeğine geçiş kapısı, pilot için değil
       │       (P9a pilot tavanı Dalga 2'ye alındı)
       └─ P7 TKGM flag (protokol gelince)                      1 gün
```

**Süre tahminleri %80 coverage kapısını (`--cov-fail-under=80`) ve contract törenini içerir.**
⚠️ **2026-07-31 revizyonu Dalga 2'yi +3-5 gün uzatır** (WEB1/WEB2 + P9a); Dalga 1 +1 gün (C9/C10).

## 5.2 Paralel iki hat — kod pilotu beklemez, pilot kodu beklemez

| Hat | Ne zaman | Kim |
|---|---|---|
| **SAHA HATTI** | 30 Tem'den itibaren **hemen** | Terra hediyesini masaüstüne aktive et → tarlaları seç (üzüm + fıstık) → poligonları bir kez çiz → panel teyit → SHGM kayıt + kurum uçuş izni → 3 Ağu'dan itibaren haftalık döngü |
| **KOD HATTI** | Adım 0'dan itibaren | Dalga 1 → Dalga 2 → demo → Dalga 3 |

**Buluşma noktası:** Dalga 2 bittiğinde pilotun 3 haftalık verisi de hazır olur → uçtan uca demo.

## 5.3 Hemen (bu hafta, 30 Tem – 2 Ağu) yapılacak 9 iş

| # | İş | Süre | Repo/alan |
|---|---|---|---|
| 1 | **Terra hediyesini RTX 3090'lı masaüstüne aktive et** — laptopa DEĞİL (ücretsiz lisans geri alınamaz) | 15 dk | saha |
| 2 | **Adım 0 karar günü** — 7 kararı yaz | 1 gün | governance |
| 3 | **DJI Mavic 3M Image Processing Guide'ı indir** ve W1 zincirini oku | 1 saat | worker |
| 4 | **TKGM'ye kurumsal protokol başvurusu** (cbs@tkgm.gov.tr · 0312 551 40 84) — kamu-kamu kanalı artık açık | 1 saat | governance |
| 5 | **Agisoft + Pix4D'ye eğitim/araştırma lisansı sorusu** + kamu satın alma prosedürünü başlat. ⚠️ **AYNI YAZIYA DJI'yı da ekleyin:** Terra'nın CLI/betik/toplu-iş arayüzü var mı · varsa hangi lisans seviyesinde (Agriculture $300/yıl dâhil mi) · çıktı dosya adları dokümante mi. **E6'nın tasarımı bu cevaba bağlı** (0.g ikinci açık kalem) — ek maliyeti yok | 1 saat | governance |
| 5b | **KİRAZ ürün kararı** (0.d ek bulgusu) — bugün `bookable:True` ama wire-enum'da ve edge tablosunda yok; çiftçi sipariş edebiliyor, iş sessizce düşüyor. Ya `bookable:False` (anında kapatır) ya enum+tablo. **Sipariş açık kaldıkça risk canlı** | 30 dk | ürün |
| 6 | **SHGM Kayıt Sistemi kaydı** (7 gün içinde) + kurum uçuş izin prosedürünü teyit | 2 saat | saha |
| 7 | **Pilot tarlaları seç** (üzüm birincil + fıstık), yazılı çiftçi rızası, poligonları **bir kez** çiz | 1 gün | saha |
| 8 | **Kalibrasyon paneli teyidi** — MicaSense/Sentera sınıfı, bant başına sertifikalı reflektans değeri. Panelsiz M3M'den reflektans çıkmaz | 30 dk | saha |
| 9 | **SD kart envanteri** — 35 m'de kart başına ~5 uçuş; günde 8-10 uçuş için kaç kart? | 30 dk | saha |

**Metashape 30 gün denemesini BAŞLATMA.** Demo tarihini belirleyip **3 hafta geri sayın**;
tek kullanımlık kaynak.

---

# 6. DEMODA SÖYLENECEKLER VE SÖYLENMEYECEKLER

**Söylenecek (pilottan gerçek ölçümle):**
- "X dönümü Y dakikada kalibre ediyoruz" · "kapsama oranı %Z" · "2 hafta arayla NDVI farkı şu"
- "İndeks katmanı 5 ürün için hazır; YZ tespiti ürün bazlı eğitim ister — üzüm ve mısır hazır,
  fıstık sırada" ⟵ **yol haritası olarak sunun**

**Söylenmeyecek:**
- ❌ "Tamamen otomatik" — ön raporun başında insan var (Terra'nın CLI'si yok)
- ❌ "Her drone ile çalışır" — Terra yalnız DJI multispektralini işler
- ❌ "Mutlak reflektans üretiyoruz" — M3M **hangi yazılımla olursa göreli**. Mutlak radyometri
  = 5 bantlı sensöre (RedEdge-P / Sentera 6X / Altum-PT) geçiş anı
- ❌ "Böcek türü ve sayısını tespit ediyoruz" — **fizik olarak imkânsız.** Kendi protokolünüz
  yazmış (satır 349-355): 20 m'de ÇS ~0,92 cm ≈ 9200 µm, tekil böcek tanıma eşiğinin (~80 µm)
  **~100 katı kaba** — "İHA böceği değil bıraktığı izi görür. Bu bir uçuş parametresi değil
  optik sınırdır." → **İz tespiti** deyin, böcek sayımı için **yer/tuzak sayımı (YS)**
- ⚠️ Abiyotik streste dikkat: M3M'de **termal yok, SWIR yok** → `NITROGEN_STRESS` (NDRE) ✅,
  genel vigor ✅, `WATER_STRESS` **zayıf** (CWSI termal ister), `THERMAL_STRESS` **hiç**

---

# 7. KARAR DAYANAKLARI — DOĞRULANMIŞ TEMEL BULGULAR

| # | Bulgu | Kaynak |
|---|---|---|
| 1 | **PIX4Dfields'in CLI/API/SDK'sı yok** — Pix4D'nin otomasyon ürünü ayrı SKU (PIX4Dengine) | Pix4D resmi dokümantasyon ağacı · ⚠️ **negatif iddia** — §8.5'teki 4 adımlı kanıt zinciri güçlü ama yokluk kanıtı değil |
| 2 | **DJI Terra multispektralde yalnız DJI kameraları** (P4M, M3M); üçüncü taraf adaptasyonu sadece RGB | DJI kılavuz v4.3 + destek |
| 3 | **DJI Terra tekil kalibre görüntü yazmıyor** — 2D MS çıktıları: tiles, DOM, DSM, tek-bant **stitched** görüntüler, 5 indeks | DJI resmi çıktı dokümanı |
| 3b | ⚠️ **"DJI Terra'nın CLI'si yok" — BAĞIMSIZ TEYİT EDİLEMEDİ (2026-07-30).** Arama iddiayı ne doğruladı ne çürüttü. **E6'nın tüm tasarımı buna dayanıyor** → DJI'dan yazılı cevap alınmadan E6 kodlanmaz (0.g ikinci açık kalem). Güvenli varsayım: klasör izleyici | doğrulama denemesi sonuçsuz |
| 3c | ✅ **ODM iddiaları resmî dokümanla doğrulandı (2026-07-30):** `--radiometric-calibration camera` = siyah seviye + vinyetleme + satır gradyanı/kazanç-pozlama; `camera+sun` = DLS spektral radyans + güneş açısı ve **resmen "experimental"**; kalibrasyonsuz çıktı **DN**, kalibrasyonlu **reflektans**; **M3M desteği v3.5.3'ten itibaren** | [ODM radiometric-calibration](https://docs.opendronemap.org/arguments/radiometric-calibration/) · [ODM multispectral](https://docs.opendronemap.org/multispectral/) |
| 3d | ✅ **M3M'de ışık (irradyans) sensörü VAR** — resmî specs: "Light Sensor: Built-in module". MS 1/2.8" 5 MP · RGB 4/3 20 MP. → **ölçüm #3'ün öncülü sağlam** (Terra bu sensörü kullanıyor mu, ayrı soru). ⚠️ GSD formülleri specs sayfasında **yayınlanmamış**; bağımsız hesapla doğrulandı (~H/37,5 ve ~H/20,1) | [DJI M3M specs](https://ag.dji.com/mavic-3-m/specs) |
| 4 | **M3M vinyetleme kamera tarafında UYGULANMIYOR** — parametreler her fotoğrafla geliyor; `SensorGain`/`ExposureTime`/`Irradiance` XMP'de | DJI Mavic 3M Image Processing Guide |
| 5 | **ODM M3M'i v3.5.3+ destekliyor**, `--radiometric-calibration camera\|camera+sun` → reflektans; ⚠️ bant hizalama kayması bilinen sorun | ODM resmi doküman + topluluk |
| 6 | **Metashape ağ işlemede HER düğüm ayrı lisans ister** (sunucu istemez, istemci ister) → 10 düğüm = $34.990. **ClusterODM bedava** | Agisoft helpdesk |
| 7 | **Metashape 30 gün denemesi tam işlevli** (export/kaydet açık), kredi kartı yok; süre sonu demo modu. **PIX4Dfields denemesi export ETMİYOR** | Agisoft + Pix4D resmi |
| 8 | **Kod ADR-007'ye sadık; çelişen taraf 2026-07-29 ürün direktifi.** ADR-007 §5: ön rapor **worker sonucu geldiğinde** üretilir | ADR-007 + `worker_bridge_consumer.py:1565` |
| 9 | **TKGM parsel geometrisi kodda hazır** — iki adaptör + idari cache + 3 uç + feature flag | platform kaynak kodu |
| 10 | **M3M GSD:** RGB = H/37,2 · ÇS = H/21,7 (H metre, GSD cm/px). RGB, ÇS'den **1,71× daha ince** | DJI resmi + protokol §2 |
| 11 | **Fiyatlar:** Terra Ag $300/yıl (3 cihaz) · PIX4Dfields $1.990/yıl · Metashape Pro $3.499 kalıcı · **Correlator3D $5.900 kalıcı** (script modu + multispektral, tüm modüller dahil) · ODM/ClusterODM **$0** | üretici fiyat sayfaları |
| 12 | **Ücretsiz agronomik yığın:** QGIS + **Precision Zones** eklentisi (PCA + K-Means++ + Elbow/Silhouette). ⚠️ **shapefile/ISOXML export YOK** — makine dosyası için Fields, GeoPard API veya kendi yazımı | plugins.qgis.org |
| 13 | **Sentinel-2 bedava:** 5 gün tekrar, 10 m NDVI, ayda 10.000 openEO kredisi → uçuş olmayan haftaları doldurur | Copernicus resmi |

---

---

# 8. TEKNİK EK — YAZILIM KARŞILAŞTIRMA REFERANSI

*(Karşılaştırma dosyası bu bölüme özetlendi ve silindi. Kamu araştırma projesi olması nedeniyle
anlamsızlaşan bölümler — servis-sağlayıcı lisans analizi ve 5/10 istasyonluk maliyet senaryoları —
bilinçli olarak alınmadı.)*

## 8.1 Sürüm ve platform (2026-07)

| | DJI Terra | PIX4Dfields | Metashape Pro | OpenDroneMap |
|---|---|---|---|---|
| Güncel sürüm | 5.3.0 (27 Tem 2026) | 2.13.2 (13 Tem 2026) | 2.3.1 (28 Nis 2026) | 3.6.x |
| İşletim sistemi | **Yalnızca Windows 10+** | Windows + macOS (**Linux yok**) | **Windows + macOS + Linux** | Linux/Docker |
| Tarım tarafı gelişimi | ⚠️ **Bakım modunda** — 5.3.0 sürüm notlarında multispektral/tarım yeniliği **yok**; bir yıllık yatırım 3D/inspection/termal'e gitti | Aktif (uydu, false-color, VRA cihazları, pansharpening) | Aktif (blending, LiDAR) | Aktif |

## 8.2 Sensör kapsaması — 5 bantlı sensöre geçiş için (bugün DJI-only, ama yol haritası)

| Sensör | DJI Terra | PIX4Dfields | Metashape Pro | ODM |
|---|---|---|---|---|
| DJI Mavic 3M | ✅ yerli | ⚠️ **göreli** | ⚠️ göreli | ✅ v3.5.3+ (⚠️ bant kayması) |
| Sentera 6X / 6X Thermal | ❌ | ✅ **tam radyometrik** | ✅ | ✅ v1.0.1+ |
| MicaSense RedEdge-P / Altum-PT | ❌ | ✅ **tam radyometrik** + pansharpening | ✅ | ✅ (RedEdge-MX, Altum) |
| Parrot Sequoia+ | ❌ | ✅ **tam radyometrik** (+termal profil) | ✅ | kısmen |
| P4 Multispectral | ✅ | ⚠️ göreli | ⚠️ göreli | ✅ v2.8.8+ |

> **Terra'nın kesin sınırı (DJI kılavuz v4.3 + destek):** multispektral rekonstrüksiyon **yalnız
> P4M ve M3M**; "Third-Party Camera Adaptation" **yalnız görünür ışık** içindir; LiDAR'da da
> "üçüncü taraf cihaz desteklenmez".
> **Sonuç:** 5 bantlı sensöre geçtiğiniz gün Terra kalibrasyon rolünden **tamamen** düşer.

## 8.3 Radyometrik mekanizmalar ve otomasyon riski

| | DJI Terra | PIX4Dfields | Metashape Pro | ODM |
|---|---|---|---|---|
| Panel | ✅ en fazla **3 yansıtkanlık**; bant başına 0–1 faktör | ✅ Airinov/Parrot/MicaSense/Sentera; **otomatik panel tespiti** | ✅ `locateReflectancePanels()` + sertifika elle | ✅ `--radiometric-calibration camera` |
| Işınım sensörü | ✅ "use sunlight sensor data" (**P4M dokümanında**; M3M'de teyit edilecek) | ✅ EXIF → sunshine sensor → panel → termal → hava | ✅ `use_sun_sensor=True` | ✅ `camera+sun` |
| Hava durumu düzeltmesi | — | ✅ açık/kapalı gökyüzü → güneş açısı | — | — |
| Reflektans ölçeği | reflektans haritası | reflektans faktörü | **32.768 = %100** | **float32 0–1** |
| ⚠️ Otomasyon riski | — | Otomatik tespit → manuel adım yok | ⚠️ **panel tespiti başarısız olursa her kalibrasyon görüntüsü ve her bant için ELLE maske** → kör otomasyonda sessiz kalite kaybı | ⚠️ parametre verilmezse sessizce **DN** üretir |

> **Motor değiştirme uyarısı (Pix4D'nin kendi dokümanından):** PIX4Dfields düzeltme tipini
> **otomatik seçer**, PIX4Dmapper elle seçtirir; Pix4D bunun "hesaplanan kamera yönelimi farkları
> nedeniyle biraz farklı reflektans değerleri" doğurabileceğini yazıyor. → **Motorlar arası mutlak
> reflektans bire bir aynı çıkmaz.** Tek motora sabitlenin ya da geçişte yeniden eğitin.
> (§4'teki 4. metrik tam bunu ölçüyor.)

## 8.4 İndeks, zonasyon ve çıktı formatları

| | DJI Terra | PIX4Dfields | Metashape Pro | QGIS+Precision Zones |
|---|---|---|---|---|
| Hazır indeks | NDVI, GNDVI, NDRE, LCI, OSAVI | geniş kütüphane | ❌ (formülle) | — |
| **Kullanıcı formülü** | ❌ **indeks hesaplayıcı YOK** | ✅ | ✅ `Set Raster Transform` | ✅ |
| Zonasyon | reçete haritası | ✅ + VRA + spot ilaçlama | ❌ | ✅ PCA + K-Means++ |
| **ISOXML/ISOBUS** | DJI/XAG ekosistemi | ✅ **var** (+John Deere/HORSCH/EAVision…) | ❌ | ❌ |
| PDF rapor | — | ✅ sigorta uyumlu | processing report | CSV/PNG |
| Ortho/DSM/indeks | GeoTIFF | GeoTIFF | GeoTIFF | — |
| Vektör | — | SHP/KML/GeoJSON | (GIS'e) | raster+CSV |
| Nokta bulutu | LAS/LAZ 1.4 + 5 format | — | LAS/LAZ + çok format | LAS |

⚠️ **Terra'nın indeks hesaplayıcısı yok** — 5 sabit indeksin dışına çıkamazsınız. Kendi indeksinizi
(ör. CIre, SAVI) istiyorsanız Terra ortosundan **kendiniz** hesaplamanız gerekir (rasterio ile zaten
yapıyorsunuz). **ISOXML üreten tek araç Fields** (ücretsizlerde yok, alternatif GeoPard API).

## 8.5 Otomasyon — ve PIX4Dfields boşluğunun kanıt zinciri

| | Terra | Fields | Metashape | ODM |
|---|---|---|---|---|
| CLI / headless | ❌ | ❌ | ✅ `metashape -r script.py` | ✅ |
| Python API | ❌ | ❌ | ✅ (+Java binding) | ✅ PyODM/NodeODM |
| Dağıtık işleme | ✅ Cluster (fiyat gizli) | ❌ **hiç yok** | ✅ ama **düğüm başına lisans** | ✅ **ClusterODM, bedava** |

**Fields'ın CLI'si olmadığının kanıt zinciri** (denetimde sorulursa):
1. `support.pix4d.com/hc/pix4dfields` dokümantasyon ağacının **hiçbir bölümünde** API/SDK/CLI başlığı yok
2. Pix4D'nin CLI dokümanları **PIX4Dmapper**'a ait (`pix4dmapper.exe -c -r "<proje>.p4d"`) ve
   **Enterprise Server** lisansı ister
3. Pix4D'nin resmi otomasyon yolu **PIX4Dengine SDK**: GUI'siz, Python, Windows+Linux, kendi
   altyapınızda, multispektral indeks destekli (`AlgoOption.Index.INDICES`), **tüketim bazlı fiyat**
4. Pix4D "Engine üzerine tamamen özelleştirilmiş arayüz geliştiren müşteriler"den bahsediyor →
   **ürüne gömme yolu Fields değil, Engine'dir**

## 8.6 Tam fiyat listesi (2026-07, resmi sayfalar)

| Ürün | Fiyat | Kapsam |
|---|---|---|
| **DJI Terra Agriculture** | **$300/yıl** | 3 cihaz |
| DJI Terra Standard | $1.790/yıl · **$5.080 kalıcı** | 1 hesap/1 bilgisayar |
| DJI Terra Flagship | $3.640/yıl · $10.450 kalıcı | 1 hesap/1 bilgisayar |
| DJI Terra Cluster | fiyat yayınlanmamış, yalnız yetkili satıcı | dağıtık |
| **PIX4Dfields** | ~$165/ay · **$1.990/yıl** · 3-yıl ~$111/ay | aynı anda tek bilgisayar (hesap-bağlı floating) |
| **Metashape Professional** | **$3.499 kalıcı** | 1 makine (node-locked) |
| Metashape Standard | $179 kalıcı | ⚠️ **tuzak** — Python API + network processing Pro'da |
| Metashape floating | teklifle (`sales@agisoft.com`) | ağ paylaşımlı |
| Metashape Service Provider | $6.736/yıl/makine · veya $0,973–1,559/makine-saati (min $155,90/ay) | ⚠️ kamu araştırma projesinde **muhtemelen gereksiz** |
| **Correlator3D Standard** | **$5.900 kalıcı** · $6.400 kalıcı floating · $2.950/yıl · $295/ay | 61 MP'e kadar, **sınırsız görüntü, tüm modüller**, script/batch modu |
| **OpenDroneMap / ClusterODM** | **$0** (AGPL-3.0) | sınırsız |
| **QGIS + Precision Zones / OTB** | **$0** | zonasyon (ISOXML yok) |

> **Fiyat doğruluk notu:** PIX4Dfields resmi fiyat sayfası bozuk render veriyor
> ("$4188$1990 / Save 53%"); $1.990/yıl iki ayrı Pix4D sayfasından tutarlı çıktı ama **sipariş
> öncesi yazılı teklif alın.** Pix4D "one-time charge (OTC)" lisanslarından söz ediyor, fiyat
> yayınlamıyor. **Kamu satın alması için hepsinde resmi teklif zorunlu.**
>
> **Türkiye temsilcileri (kamu satın alma için):** [Piri Reis Grup](https://www.pirireisgrup.com/agisoft-yazilim/) (Agisoft distribütörü) · [4B Harita](https://www.4bharita.com.tr/4b-harita/iha/agisoft-metashape.html) (Agisoft + Pix4D) · [Paksoy Teknik](https://paksoyteknik.com.tr/urun/agisoft-metashape/)

## 8.7 Air-gap uyumu — M1 için gizli kazanç

| | Değerlendirme |
|---|---|
| **Metashape** | ✅ **En iyi.** Node-locked için **tam offline aktivasyon**: `.actparam` → `.actreq` → `.actresp` dosyaları internetli başka makineden taşınır. → **M1'e hiç allowlist açmanız gerekmez.** Floating lisans sunucusu yerel servis olarak koşabilir |
| **ODM** | ✅ Lisans yok → aktivasyon sorunu yok |
| **PIX4Dfields** | ⚠️ İlk aktivasyon internet ister; sonra lisans yerelde saklanır ve **süresi bitene kadar** offline çalışır. Pix4D "ne kadar dayanır" sorusunu dokümante etmiyor. **Uzaktan cihaz deaktivasyonu YOK** → M1 diski arızalanırsa lisans için Pix4D desteğine başvurulur. Mevcut `pix4d_allowlist_domains.txt` **kasıtlı bir air-gap deliği** |
| **DJI Terra** | ⚠️ Offline lisans var ama **"donanım değişimi offline lisansı geçersiz kılar"** (resmi FAQ). 3-cihazlı yılda 2, 1-cihazlı yılda 1 kez çözülebilir |

> **Eyleme dönük sonuç:** Metashape'e geçilirse `config/processing/pix4d_allowlist_domains.txt` +
> `config/security/firewall_rules.conf` deliği **tamamen kapatılabilir** — güvenlik denetiminizde
> net kazanç. ODM'de bu delik hiç açılmaz.

## 8.8 Donanım gereksinimleri

| | DJI Terra | PIX4Dfields | Metashape Pro | ODM |
|---|---|---|---|---|
| Min RAM | **32 GB** | 8 GB | 16–32 GB | 16 GB (100–300 görüntü) |
| Önerilen RAM | 64 GB+ | (öncelik: CPU çekirdek > NVMe > RAM > GPU) | 32–128 GB, uçta 128+ | 64 GB (~1000 görüntü), **256 GB (~5000)** |
| GPU | ≥4 GB VRAM, Shader Model 6.1+, öneri RTX 2070+ | Vulkan 1.1 + 4 GB; ⚠️ **AMD hızlandırma YOK** | NVIDIA/AMD 1024+ shader; CUDA/OpenCL | CUDA opsiyonel |
| Ölçek kuralı | "+10 GB boş bellek ≈ +4000 foto" | görüntü/boyut **yazılım sınırı yok** (20.000+ test) | 1000+ foto @20–48 MP → 64–128 GB+ | ~1000 görüntü 64 GB'da **3,5–5,5 saat** |

⚠️ **Demo masaüstünüz (RTX 3090 24 GB / 32 GB RAM) Metashape ve ODM için sınırda.** 1000+
multispektral yakalamalı batch 32 GB'a sığmayabilir → **pilotta batch'i tarla başına bölün.**
Planlanan M1 (256 GB / RTX 5090) üçünün de tavsiye sınırının çok üstünde.

## 8.9 Bağımsız (akademik) doğrulama — elinizdeki tek üçüncü taraf kanıt

- **Sensors 2024, 24(1):286** — AgiSoft PhotoScan / PIX4Dmapper / DJI Terra, orman, 3 irtifa:
  işlem süresinde **AgiSoft ve Terra ≈ Pix4D'nin yarısı**; nokta bulutu yoğunluğunda **Pix4D ve
  AgiSoft, Terra'nın 2,5 katı**; DSM yüksekliklerinde **0,5–2,5 m** fark (Terra sistematik daha
  yüksek); ICP kalitesinde Terra daha az boşluk.
  ⚠️ **PIX4Dmapper** ile yapıldı (Fields değil) ve orman senaryosu → tarlaya birebir taşınamaz.
- **DergiPark (İHA yazılım karşılaştırması):** Agisoft **5,46 cm**, Pix4D **5,10 cm** konum
  doğruluğu → geometrik doğrulukta **pratikte fark yok**.
- **Remote Sensing 2024, 16(24):4633** (DJI P4MS + Metashape) — tam metne erişilemedi (HTTP 403);
  **sonuçlarına dayanılmadı.**
- **Üretici hız iddiaları kullanılamaz:** Pix4D vaka çalışmaları 50 ha MS'i "6 dk 54 sn", başka
  vakada 110 ha'yı "<2 saat" diyor — **10 kat fark.** Kapasite planlaması yalnız kendi ölçümünüzle.

## 8.10 Kaynak dizini (denetim/rapor için)

**DJI (resmi):** [Terra FAQ](https://enterprise.dji.com/dji-terra/faq) · [hangi drone'lar](https://support.dji.com/help/content?customId=en-us03400005023&spaceId=34&re=US&lang=en&documentType=artical&paperDocType=paper) · [multispektral görev gereksinimleri](https://repair.dji.com/help/content?customId=01700004678&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE) · [M3M radyometrik düzeltme](https://support.dji.com/help/content?customId=01700005126&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE) · [Terra kılavuz v4.3](https://dl.djicdn.com/downloads/dji-terra/20241024/DJI_Terra_User_Manual_v4.3_EN.pdf) · [Terra çıktı içerikleri](https://repair.dji.com/help/content?customId=01700004723&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE) · [**M3M Image Processing Guide**](https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/Mavic_3M_Image_Processing_Guide_EN.pdf) · [M3M specs](https://ag.dji.com/mavic-3-m/specs) · [M3M FAQ](https://ag.dji.com/mavic-3-m/faq) · [Terra store](https://store.dji.com/product/dji-terra) · [WPML spec](https://github.com/dji-sdk/Cloud-API-Doc/blob/master/docs/en/60.api-reference/00.dji-wpml/10.overview.md) · [SmartFarm kılavuz](https://support.dji.com/help/content?customId=01700009100&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE)

**Pix4D (resmi):** [Fields doküman ağacı](https://support.pix4d.com/hc/pix4dfields) · [radyometrik düzeltme](https://support.pix4d.com/hc/en-us/articles/360022919691) · [işleme seçenekleri](https://support.pix4d.com/hc/en-us/articles/360028421272) · [bilgisayar gereksinimleri](https://support.pix4d.com/hc/en-us/articles/360000889343) · [FAQ](https://support.pix4d.com/hc/en-us/articles/360042668212) · [cihaz deaktivasyonu](https://support.pix4d.com/hc/en-us/articles/18519039485853) · [girdi/çıktı](https://support.pix4d.com/hc/en-us/articles/360000897346) · [sürüm notları](https://support.pix4d.com/hc/en-us/articles/360001122223) · [fiyat](https://www.pix4d.com/pricing/pix4dfields/) · [deneme + export kısıtı](https://support.pix4d.com/hc/en-us/articles/360000831403) · [Engine FAQ](https://www.pix4d.com/enterprise/faq) · [Engine SDK API](https://developer.pix4d.com/server/1.4.2/api.html)

**Agisoft (resmi):** [Pro özellikleri](https://www.agisoft.com/features/professional-edition/) · [sistem gereksinimleri](https://www.agisoft.com/downloads/system-requirements/) · [mağaza/fiyat](https://www.agisoft.com/buy/online-store/) · [Service Provider](https://www.agisoft.com/buy/saas/service-provider-license/) · [eğitim lisansı](https://www.agisoft.com/buy/online-store/educational-license/) · [30 gün deneme](https://agisoft.freshdesk.com/support/solutions/articles/31000135259-how-to-try-full-metashape-functionality-before-buying) · [**offline aktivasyon**](https://agisoft.freshdesk.com/support/solutions/articles/31000169304--metashape-2-x-offline-activation-of-node-locked-license) · [ağ işleme lisans sayısı](https://agisoft.freshdesk.com/support/solutions/articles/31000145920-how-many-licenses-are-required-for-network-processing) · [ağ işleme kurulumu](https://agisoft.freshdesk.com/support/solutions/articles/31000145918-how-to-configure-the-network-processing) · [bellek gereksinimleri](https://agisoft.freshdesk.com/support/solutions/articles/31000157329-memory-requirements-for-processing-operations) · [MicaSense Altum iş akışı](https://agisoft.freshdesk.com/support/solutions/articles/31000148381-micasense-altum-processing-workflow-including-reflectance-calibration-in-agisoft-metashape-professi) · [2.3.x yenilikleri](https://agisoft.freshdesk.com/support/solutions/articles/31000177202-new-features-in-agisoft-metashape-2-3-x)

**ODM / ücretsiz yığın:** [multispektral (M3M v3.5.3+)](https://docs.opendronemap.org/multispectral/) · [`--radiometric-calibration`](https://docs.opendronemap.org/arguments/radiometric-calibration/) · [M3M bant hizalama](https://community.opendronemap.org/t/i-seek-wisedom-aligning-rgb-and-multispectral-imagery-from-dji-m3m/24501) · [ClusterODM](https://opendronemap.org/clusterodm/) · [büyük veri setleri](https://docs.opendronemap.org/large/) · [WebODM/ODM ayrışması Nis 2026](https://aerocartwright.com/library/webodm-odm-split/) · [Precision Zones](https://plugins.qgis.org/plugins/precision_zones/) · [MicaSense imageprocessing](https://github.com/micasense/imageprocessing) · [Copernicus openEO kredi](https://documentation.dataspace.copernicus.eu/APIs/openEO/credit_usage.html)

**Diğer ticari:** [Correlator3D fiyat](https://www.simactive.com/pricing) · [özellikler](https://www.simactive.com/correlator3d-mapping-software-features) · [GeoPard fiyat](https://geopard.tech/pricing/) · [Solvi fiyat](https://solvi.ag/pricing) · [UgCS Open sınırları](https://www.sphengineering.com/flight-planning/ugcs-open)

**Akademik:** [Sensors 2024 24(1):286](https://www.mdpi.com/1424-8220/24/1/286) · [özet (OUCI)](https://ouci.dntb.gov.ua/en/works/lDLGQrql/) · [DergiPark İHA yazılım karşılaştırması](https://dergipark.org.tr/tr/download/article-file/4723405)

**TKGM / ÇKS:** [MEGSİS](https://www.tkgm.gov.tr/projeler/mekansal-gayrimenkul-sistemi-megsis) · [Parsel Sorgu kullanım koşulları](https://parselsorgu.tkgm.gov.tr/app/documents/parsel-sorgu-kullanim-kosullari-v.1.0.pdf) · [CBS API](https://cbsapi.tkgm.gov.tr/megsiswebapi.v3.1/) · [ÇKS Yönetmeliği](https://www.turktob.org.tr/fs_/uploads/dosyalar/106-C%CC%A7iftc%CC%A7i%20Kay%C4%B1t%20Sistemi%20Yo%CC%88netmelig%CC%86i.pdf)

---

# 9. ADIM 0 — KARAR TASLAKLARI (imzaya hazır)

> ## ✅ YEDİ KARARIN TAMAMI ONAYLANDI — 2026-07-30, Proje Koordinatörü
>
> Bu bölüm artık **taslak değil, yürürlükteki karar kaydıdır.** Karar metinleri bağlayıcıdır;
> değişiklik yeni bir karar kaydı gerektirir.
>
> **Kalan yönetişim adımları (§9.1'de kopyala-yapıştır hazır):**
> ① `open_items_decisions_2026-06.md`'ye 7 kayıt satırı ② `end_to_end_workflow.md`'de C13/C15/C16
> durum güncellemesi ③ ★ işaretli üç karar için ADR/not (0.b → ADR-007 yorum notu ·
> 0.e → yeni ADR · 0.f → contract metadata notu).

---

## KARAR 0.a — Edge→Platform veri taşıma mimarisi (C13)

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** Edge→Platform veri aktarımı **iki fazlı, kontrol-düzlemi/veri-düzlemi ayrık** modelle
yapılacaktır: (1) M2, `POST /api/v1/ingest/manifests` ile **yalnız manifesti** (JSON) gönderir;
platform yanıtta her dosya için **süresi ve kapsamı sınırlı presigned PUT URL** döner. (2) M2
nesneleri **doğrudan nesne deposuna** yükler. (3) M2, `POST /api/v1/ingest/complete` ile bitişi
bildirir; platform hash doğrular ve Dataset'i `RAW_INGESTED`'a alır. Platform ikili veri gövdesi
kabul eden bir uç **açmayacaktır**.

**Önkoşul — E14 (kalibrasyon kanıtı üreticisi).** Bu karar **tek başına yeterli değildir.**
`calibration_result` ve `observed_footprint_wkt` bugün **beş yerde tüketiliyor, sıfır yerde
üretiliyor** (`sync.py:207-255` · `calibrated_validator.py:114-122` · `qc_report_writer.py:245-256`
· `package_assembler.py:52` · `dataset.py:123-125`); `calibration_pipeline.run()` bunları **girdi**
olarak alıyor ve docstring'i üretimi "upstream"e devrediyor — ama o upstream yazılmamış
(`calibration_proof_checker` yalnız **karşılaştırır**). Sonuç: **taşıma hattı bağlansa bile veri
M1'in kendi içinde HC-05 kapısında durur; ağa hiç çıkmaz.** Bu nedenle **E14, İP-1'den (C13) ÖNCE
tamamlanacaktır** ve Dalga 1'in ilk işidir. E14 tamamlanmadan 0.a'nın kabul testi
(`Dataset RAW_INGESTED`) koşulamaz.

**Gerekçe.** (a) Mevcut kod iki bağımsız kusurla kopuk: `cloud_client.submit_manifest()` repo
genelinde **çağrısız** ve Dataset satırını yalnız o üretiyor; parçalar `application/octet-stream` +
`X-Chunk-Index` ile **JSON ucuna** POST edildiği için her parça 422 dönüyor. (b) Presigned model
**C16'yı aynı işle** çözer (yama görselleri de aynı yolla gider). (c) Platform veri yolundan çıkar —
ölçek hedefi bunu zorunlu kılar. (d) Platformda `storage_adapter.py` zaten mevcut.

**Sonuçlar.** (+) Tek mekanizma üç kusuru kapatır (C13, C16, ham kare taşıma). (+) KR-070/071
tek-yön akışı ve outbound-443 kısıtı korunur. (−) **Edge'e S3/MinIO istemcisi eklenmesi gerekir**
(bugün repoda 0 eşleşme). (−) Presigned URL yeni bir güvenlik yüzeyidir: süre, bucket ve anahtar
kapsamı sıkı sınırlanmalı; ihlal `SECURITY.DENY` üretmeli.

**Reddedilen alternatif.** *Platformda parça-yükleme ucu:* `upload_chunk()` neredeyse hazır olduğu
için kısa vadede kolay; ancak platformu kalıcı olarak veri yoluna koyar ve C16'yı çözmez.

**EK ŞART — ANAHTAR SAHİPLİĞİ (2026-07-30 doğrulama turu; kararı değiştirmez, uygulamayı bağlar).**
Nesne anahtarını **platform ÜRETİR; edge'in verdiği hiçbir yol imzalanmaz.** Bu, "anahtar kapsamı
sınırlansın" ifadesinden daha güçlü ve daha dar bir yükümlülüktür — P3 aksi hâlde *"edge'in
anahtarını doğrula"* biçiminde de uygulanabilir ki bu yeterli DEĞİLDİR.

*Neden (bugünkü kod, ölçüldü):* `patches.py:165-175` edge'in manifeste yazdığı **göreli yolu**
(DB'ye `visualization_paths` olarak aynen kaydedilmiş hâlini) S3 anahtarı kabul edip
`settings.s3_default_bucket` ile imzalıyor. Yani anahtarı fiilen **edge belirliyor**.

> **🟠 ŞİDDET DÜZELTMESİ (2026-07-31 öz-denetim).** Burada önce *"çapraz-kiracı veri sızıntısı"*
> yazıyordu — **anlık risk olarak abartılıydı.** `patches.py:118-148`'de gerçek bir sahiplik kapısı
> var: `DatasetModel ⨝ ExpertReviewModel.expert_id`, eşleşmezse `403 PATCH.OWNERSHIP_DENIED`.
> Sömürü **iki koşul** ister: (1) hatalı/ele geçirilmiş edge **ve** (2) o dataset'in mission'ına
> **atanmış uzman** kimliği. Doğru ifade: *"ele geçirilmiş edge + atanmış uzman bileşiminde
> **çapraz-dataset okuma**"*. **Kararı değiştirmez** — anahtar sahipliği kuralı yine zorunlu,
> yalnız aciliyet etiketi 🔴→🟠 iner ve kabul testi **iki koşullu** kurulur.

*Bağlayıcı kural:*
1. Anahtar şeması yalnız platformda üretilir: `{tenant}/{dataset_id}/{raw|layers|patches}/{...}`.
   Manifestteki `object_key` alanı platformun **döndürdüğü** değerdir, edge'in önerdiği değil.
2. Presigned **PUT** URL'leri yalnız platformun ürettiği anahtarlar için verilir.
3. **⚠️ DÜZELTİLDİ (2026-07-31).** Eski metin: *"Presigned GET üretilirken anahtar DB'den okunur;
   istekten/manifestten gelen bir yol asla doğrudan imzalanmaz."* — **Bu kural işlevsizdi (no-op):**
   kod bunu **zaten** yapıyor (`patches.py:151` → `viz_paths = patch_row.visualization_paths`;
   platformdaki tüm presign çağrıları `:165/:169/:173` oradan besleniyor, istekten anahtar alan
   çağrı **yok**). Kural bu hâliyle P4'ün güvenlik yarısını "yapılmış" gösteriyordu.
   **Yürürlükteki kural:** *anahtar DB'den okunur **VE DB'ye yalnız platformun ürettiği anahtar
   yazılır**; edge'in önerdiği yol hiçbir aşamada kalıcılaştırılmaz* →
   `ingest_service_impl.py:266`'daki `pz.visualizations.model_dump()` passthrough'u değişmelidir.
4. Kapsam dışı anahtar talebi `SECURITY.DENY` üretir ve **sessiz düşmez**.
5. Kabul testi: sahte bir manifestle başka kiracının yolu istendiğinde uç **403/deny** dönmeli;
   bu test P4 ile aynı turda yazılır.

**Etkilenen:** E2, E3, E4, E5, E10 · P1, P2, P3, P4 · C1, C2, C3

---

## KARAR 0.b — ÖN RAPOR fazının kaynağı (C15) ★

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** ADR-007 **değiştirilmeyecektir.** `report_phase` mission.status'tan türetilmeye devam
eder ve PRELIMINARY fazı worker sonucundan sonra oluşur. 2026-07-29 ürün direktifi
("Pix4D değerleri çiftçiye ÖN RAPOR olarak gitsin, SONRA uzmanlara") **melez (Y-C) biçimde**
karşılanır: kalibrasyon tamamlandığında (`DATASET.STATE_TRANSITION → CALIBRATED`) çiftçiye
**rapor değil, işlem durumu bildirimi** gönderilir ("uçuşunuz işlendi, analiz sürüyor"), ve
kalibrasyon indeks katmanı `layer_registry`'ye **ham katman** olarak kaydedilir. `report_phase`,
`results_service_impl` ve KR-019 kapısı **dokunulmaz**.

**Gerekçe.** Kod bir hata yapmıyor — **ADR-007 §5'i birebir uyguluyor** ("Worker sonucu geldiğinde…
uzman kapısıyla PARALEL"). ADR-007 §2 ayrıca "yeni mission state EKLENMEZ" diyor. Direktifin
istediği YZ-öncesi *rapor* fazı, ADR-007'nin bilinçle yaratmadığı bir fazdır ve eklenmesi
**KR-019 (uzman kapısı), KR-025 (reçete içermez) ve KR-033 (ödeme kapısı)** eksenlerini yeniden
açar. Y-C, direktifin amacını (çiftçi uçuştan hemen sonra bir şey görsün) üç ADR'yi açmadan
karşılar.

**Sonuçlar.** (+) ADR-004/005/007 korunur; ödeme ve uzman kapıları etkilenmez. (+) En küçük kod
yüzeyi. (−) Çiftçi kalibrasyondan hemen sonra *rapor* değil *durum* görür — ürün beklentisi
kısmen karşılanır. (−) C15 "çözüldü" değil "kapsamı daraltılarak kapatıldı" olarak kaydedilir.

**Reddedilen alternatifler.** *Y-A (yeni faz + **ileride tahsis edilecek bir ADR numarası** — burada
önce "ADR-009" yazıyordu, ama ADR-009 dev-station'a ayrıldı; bkz. §9.1-C):* direktifi tam karşılar ama üç ADR ve
üç KR ekseni yeniden açılır; C13 kapanmadan zaten akmaz → **FAZ 1'e ertelendi.**
*Y-B (direktifi reddet):* sıfır kod, ama ürün beklentisi tamamen karşılanmaz.

**Not.** ADR-007'ye bu kararı işaret eden bir **yorum notu** eklenir; `end_to_end_workflow.md`
C15 maddesi "KARAR BEKLİYOR" → "Y-C ile kapatıldı" olarak güncellenir.

> ## 🔄 REVİZE — KG-0.b-R (2026-07-30, Proje Koordinatörü direktifi)
>
> **Direktif:** *"Uçuştan sonra hafıza kartı işlenip **ilk bulgular** çiftçiye gösterilsin —
> özellikle tarlasındaki **sorunlu, kırmızı NDVI bölgeleri**. Sonrasında bunlar **'ÖN RAPOR'**
> başlığı altında görünsün. Demoda bu kullanılacak."*
>
> **Karar: Y-C yerine → Y-D (öncelik-bölgesi kaynaklı ÖN RAPOR).** P6'nın FAZ 1'e ertelenmesi
> **GERİ ALINDI**; yeniden tanımlanarak FAZ 0 kapsamına alındı. Aşağıdaki (c) kararı yürürlükten
> kalktı, gerekçe kaydı olarak korunur.
>
> ### Neden önceki önerim (Y-C / ertele) fazla temkinliydi — düzeltme
> O öneriyi verirken tek gösterim yolu olarak `layer_registry`'yi görmüştüm ve haklı olarak
> "hiçbir şey teslim etmiyor" dedim. **Ama aradığım veri başka bir yerde ve hazır:**
>
> | Bulgu | Kanıt |
> |---|---|
> | **Sorunlu bölgeler zaten hesaplanıyor** (edge, YZ'den ÖNCE) | `ndvi_prioritizer.py` → `PRIORITIZATION.NDVI_PROCESSED`; `expert_image_renderer.py` → `ndvi_overlay.png` |
> | **Sözleşmesi var** | `ingest.py:71` `PriorityZoneEntry`: `patch_id` · **`geom` (GeoJSON Polygon, WGS84)** · `priority_level` (EXPRESS/NORMAL) · **`ndvi_value` (-1..1)** · `sampling_reason` · `visualizations{true_color, false_color, **ndvi_overlay**}` |
> | **Platform tablosu var** | `analysis_priority_zones` (`patch_id`, `dataset_id`, `geom` PostGIS, `priority_level`, `ndvi_value`, `visualization_paths` JSONB) |
> | **Yazan kod var** | `ingest_service_impl.py:266` |
> | **`report_phase` zaten PRELIMINARY veriyor** | `results_service_impl.py:227` → `"FULL" if mission_status == "DONE" else "PRELIMINARY"` — **yeni faz GEREKMİYOR** |
> | **Tespitler zaten kırpılıyor** | `results_service_impl.py:247` → `raw_findings = ... if report_phase == "FULL" else None` |
>
> **Yani istediğiniz ÖN RAPOR = `analysis_priority_zones`'un çiftçiye sunulması.**
> Eksik olan tek şey **okuma yolu** — bugün bu tabloyu `worker_dispatch_handler`
> (işlem sırası ipucu), `expert_review_prioritization_service` (uzman kuyruğu),
> `worker_bridge_consumer.py:1088` (kota sayımı) ve `worker_job_publisher.py:115` okuyor;
> **çiftçiye açan bir uç yok** ✅ *(2026-07-31'de dört okuyucu da doğrulandı)*.
>
> ⚠️ **2026-07-31 EKİ — "şema değişmez" kısmı düzeltildi.** Bu blok *"yeni faz gerekmiyor, şema
> değişmiyor"* diyor. **Faz kısmı doğru** (yeni mission state/faz eklenmiyor), **şema kısmı değil:**
> iki kanonik artefakt PRELIMINARY içeriğini **"YALNIZ/ONLY"** diyerek dört kaleme kapatıyor
> (`analysis_preliminary_ready.v1` + `report_phase.enum.v1`) ve öncelik bölgesi o listede **yok**;
> ayrıca `report_phase` statü eşlemesinde **kalibrasyon-sonrası statü bulunmuyor** (`UPLOADED` yok).
> → **C9 + C10** eklendi. Y-D kararı **değişmiyor**, yalnız kanonik tanım onu kapsayacak biçimde
> genişletiliyor.
>
> ### Üç eksen neden yeniden açılmıyor
> | Eksen | Durum |
> |---|---|
> | **KR-019** (uzman konsensüs kapısı) | ✅ Korunur — öncelik bölgeleri **tespit içermez**; yalnız NDVI değeri + poligon. ADR-007 §1'in "ön rapor tespit taşımaz" şartı sağlanıyor |
> | **KR-033** (ödeme kapısı) | ✅ Korunur — ÖN RAPOR **ödeme-kapılı kalır.** ADR-007 §4 zaten *"ön rapor ücretsiz teaser değildir; indeks katmanı gerçek üründür"* diyor |
> | **KR-025** (reçete yok) | ✅ Korunur — NDVI bölgesi bir **gözlem**, ilaçlama/tedavi kararı değil |
> | **ADR-007 §2** ("yeni mission state EKLENMEZ") | ✅ Korunur — **yeni state de yeni faz da eklenmiyor**; mevcut PRELIMINARY fazına **yeni bir içerik kaynağı** bağlanıyor |
>
> **Sonuç:** Bu, Y-A değil. ADR-007'yi değiştirmiyor, üç ADR'yi açmıyor. Bu yüzden ADR-007'ye
> yazılacak yorum notu **Y-D'yi** anlatacak biçimde güncellenir.
>
> **Yeni/değişen iş kalemleri:** **P6** (yeniden tanımlandı) · **P12** (yeni) · **E12** (sıra revize)
> · **E10/C16** (demo kritik yoluna alındı) — bkz. §3 tabloları ve Dalga 2 şeması.
>
> ### ⚠️ ÖNCEKİ ANALİZİMDEKİ HATANIN DÜZELTİLMESİ
>
> C15 çözümlemesinde şunu yazmıştım: *"**Pix4D çıktısını platforma taşıyan bir yol yok**
> (C13 ile aynı kök)"* — bu, `end_to_end_workflow.md`'nin C15 maddesinden alıntıydı ve
> **ben de doğrulamadan devraldım. İfade yanlıştır.**
>
> | | Doğru hâli |
> |---|---|
> | **Türetilmiş ürün** (öncelik bölgeleri + 3-katmanlı görseller) | ✅ **Yol TANIMLI** — `ingest.py:71` `PriorityZoneEntry` intake manifestinde taşınıyor, `ingest_service_impl.py:266` `analysis_priority_zones`'a yazıyor. ❌ **Ama BAĞLI DEĞİL** — `submit_manifest` çağrısız (C13). Yani **tesisat eksikliği**, tasarım boşluğu değil |
> | **Ham rasterlar** (ortho.tif / ndvi.tif tam çözünürlük) | ✅ İfade burada **doğru** — taşıma yolu gerçekten yok → C1 `index_layers[]` bu yüzden var |
>
> **Neden önemli:** "yol yok" demek problemi bir **tasarım boşluğu** gibi gösterdi ve beni
> "yeni faz gerekir, üç ADR açılır, ertele" sonucuna götürdü. Oysa gerçek "**yol var, fişi
> takılmamış**" — çözüm zaten planlanmış C13 tesisatının içinde. Bu fark, kararı **ertelemekten
> FAZ 0'da yapmaya** çevirdi.
>
> **Çelişmeyen kısım (her iki analizde de doğru):** `worker_bridge_consumer.py:1565`
> `_emit_preliminary_ready` **bildirimdir** ve worker sonucunda tetiklenir — ADR-007 §5'in birebir
> uygulaması. Y-D bunu **değiştirmiyor**; yanına kalibrasyon-sonrası bir okuma yolu ekliyor.
> Yani "ön rapor **bildirimi** YZ'den sonra çıkar" ifadesi doğruydu ve doğru kalıyor;
> yanlış olan "**içerik** için hiçbir taşıma yolu yok" ifadesiydi.

---

**Aşağıdaki (c) kararı 2026-07-30'da KG-0.b-R ile YÜRÜRLÜKTEN KALDIRILDI — gerekçe kaydı olarak korunur.**

~~**✅ KAPANDI — Y-C'nin ikinci yarısı FAZ 1'e ertelendi (seçenek (c) onaylandı).**~~
~~Katman gösterimi FAZ 0 kapsamından çıkarılmıştır; Y-C yalnız P5 durum bildirimi olarak uygulanır.~~

**Gerekçe kaydı — Y-C'nin ikinci yarısı neden tanımlı değildi (2026-07-30 doğrulama turu).**
Kararın *"kalibrasyon indeks katmanı `layer_registry`'ye ham katman olarak kaydedilir"* yarısı,
işaret ettiği dosyayla **hiçbir şey teslim etmiyor.** Ölçüldü: `layer_registry.py:109-113`
`GET /layers` yalnız **katman TANIMLARINI** döndürüyor (`color`, `pattern`, `priority`,
`requires_bands`) — göreve/tarlaya ait veri yok, çiftçi verisi yok. Yani P6 tek başına yalnız
bir tip kaydı ekler; çiftçi hiçbir şey görmez.

Katmanın gerçekten gösterilmesi bir **servis yolu** gerektirir ve bu bir ikilem doğurur:

| Seçenek | Sonuç |
|---|---|
| **(a)** Mevcut (kapılı) sonuç/tile yolundan sun | Faz türetmesine girer → *"rapor fazı dışında gösterim"* iddiası düşer; ADR-007 §4 ödeme kapısı korunur |
| **(b)** Kapısız yeni bir yol aç | KR-033 ödeme kapısı yeniden açılır — Y-C'nin tam kaçınmak istediği şey |
| **(c)** Yalnız durum bildirimi (P5), katman gösterimi FAZ 1'e ertelensin | Sıfır risk; Y-C "durum bildirimi" olarak dar ve dürüst kalır |

~~**SEÇİLEN: (c).**~~ ⟵ **YÜRÜRLÜKTEN KALKTI (KG-0.b-R).** O turda üç seçeneğin hepsi
`layer_registry` üzerinden düşünülmüştü; **dördüncü ve doğru yol (`analysis_priority_zones`)
o turda bulunamamıştı.** Tablo, teşhisin nasıl daraldığının kaydı olarak korunur.

--- *(yürürlükteki karar kaydının devamı)* ---

**YÜRÜRLÜKTEKİ SEÇİM: (d) — `analysis_priority_zones` kaynaklı ÖN RAPOR (Y-D).**
Çiftçi, kalibrasyondan sonra tarlasındaki **sorunlu kırmızı NDVI bölgelerini** "ÖN RAPOR"
başlığı altında görür. Yeni faz/mission state eklenmez; mevcut PRELIMINARY fazına ikinci bir
içerik kaynağı bağlanır. Ayrıntı ve kanıt: yukarıdaki **KG-0.b-R** bloğu.

**Etkilenen:** P5 · **P6 (yeniden tanım)** · **P12 (yeni)** · **E12 (aç)** ·
ADR-007 (yorum notu — Y-D'yi anlatır) · `end_to_end_workflow.md` C15

---

## KARAR 0.c — Ham görüntü (raw frame) taşıma politikası

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** Ham drone kareleri **bütün olarak merkeze aktarılmayacaktır.** Yalnızca NDVI/indeks
önceliklendirmesinin **işaretlediği yamaları gören** kareler seçilip yüklenir (`raw_frames[]`,
opsiyonel manifest bölümü). Seçim, kare seçici (EXIF footprint + ODM `shots.geojson`) tarafından
yapılır. Seçilmeyen kareler M1'de retention süresi boyunca kalır ve silinir.

**Gerekçe.** Üst-sınır hesabı: ÇS 2592×1944 16-bit ⇒ ~10,1 MB/bant × 4 + RGB ~11 MB ≈
**51 MB/tetik.** 25 m irtifada 30 dakikalık tek uçuş ~1.046 tetik ⇒ **~53 GB/uçuş**; günde 10 uçuş
⇒ **~533 GB/gün.** 1 TB disk **~2 gün** tutar. Tam aktarım ne bant genişliği ne depolama açısından
sürdürülebilir; üstelik YZ analizi zaten yalnız işaretli bölgeleri inceleyecek.

**Sonuçlar.** (+) Bant genişliği ve depolama yönetilebilir kalır. (+) 0.a'nın anahtar şeması
(`{kiosk}/{batch}/raw/…`) bunu doğal karşılar. (−) Kare seçici **yeni bir bileşendir** ve seçim
hatası "görülmeyen kanıt" doğurur → seçim kriteri ve kaçırma oranı denetime yazılmalı.
(−) Geriye dönük yeniden analiz, silinen kareler için mümkün olmaz.

**Reddedilen alternatifler.** *(i) Hiç gitmez:* tekil görüntü analizi (İP-6) ve YZ hedefleri
imkânsızlaşır. *(ii) Tamamı gider:* yukarıdaki hacim nedeniyle uygulanamaz.

**Doğrulama görevi.** 51 MB/tetik bir **üst sınırdır** (16-bit sıkıştırmasız TIFF varsayımı).
İlk uçuşta gerçek dosya boyutu ve EXIF `Bits Per Sample` ölçülüp bu karar **sayısal olarak
teyit edilecek.**

**Etkilenen:** C3 · E11 · P3 · retention politikası

---

## KARAR 0.d — Pilot ve demo ürünü

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** Pilot uçuşlarının **birincil ürünü ÜZÜM (GRAPE)**, demo ana hikâyesinin ürünü
**ANTEP FISTIĞI (PISTACHIO)** olacaktır. Demoda YZ tespit kalitesi **üzüm** üzerinden gösterilir.
Pamuk, çeltik, zeytin ve ayçiçeği pilot kapsamına **alınmaz.**

**Gerekçe.** Kanonik hazırlık kaynağı `crop_readiness.json` (2026-07-11):
ÜZÜM `pilot / strong / bookable:True` **ve** edge NDVI eşiği + fenoloji tablosu mevcut → tek
uçtan uca tam hazır çok yıllık ürün. ANTEP FISTIĞI `pilot / limited / bookable:True` **ve** edge
tablosu mevcut → ÖN RAPOR (indeks) sorunsuz üretilir, tespit kalitesi sınırlı olur; bahçe hikâyesi
korunur. ÇELTİK ve ZEYTİN `bookable:False`. AYÇİÇEĞİ hem `bookable:False` hem tablo yok.
PAMUK `bookable:True` ama `critical_gap` → tespit güvenilmez.

**Sonuçlar.** (+) Demoda hem bahçe hikâyesi hem doğrulanmış YZ çıktısı olur. (+) İki ürünün de
edge eşik tablosu hazır → `PRIORITIZATION_THRESHOLD_MISSING` riski yok. (−) Pamuk protokolün
(§10.1) referans ürünü olmasına rağmen pilot dışı kalır; pamuk verisi ayrı bir veri-toplama
kararı gerektirir. (−) İki ürün = iki fenolojik takvim, iki eşik seti.

**Yan karar (ücretsiz kazanç).** BUĞDAY `strong` + `bookable:True` ama edge eşik/fenoloji
tablosunda **yok**. İki YAML girdisi eklenerek güçlü verili üçüncü ürün açılacaktır (E8).

> ## ✅ KG-0.d-EK **KAPANDI — YANLIŞ BULGU** (2026-07-31, kod-teyitli)
>
> **Aşağıdaki "KİRAZ sipariş edilebiliyor" tespiti YANLIŞTIR.** Koordinatör (A) seçeneğini
> onayladı, ancak uygulamadan önce yapılan ölçüm gösterdi ki **kapatılacak bir risk yok** —
> ve `bookable: false` yazmak **yanlış** olurdu.
>
> **Neden yanlıştı:** `crop_readiness.bookable` **"çiftçi sipariş edebilir"** demek DEĞİLDİR.
> Sipariş yolunda **iki ayrı kapı** var ve ikisi de fail-closed uygulanıyor:
>
> | Kapı | Anlamı | Nerede uygulanıyor | CHERRY | RICE |
> |---|---|---|---|---|
> | **`is_gap_offered`** (KR-015 sunum kapsamı) | "bu sezon GAP'ta satılıyor mu" | `fields.py:273` · `change_crop_type.py:107` · missions · subscriptions | ❌ **`GAP_OFFERED_CROPS` = {COTTON, CORN, PISTACHIO, RICE, GRAPE}** → tarla bile açılamaz | ✅ |
> | **`is_bookable`** (teslim edilebilirlik) | "model bu ürün için sonuç üretebilir mi" | **`missions.py:293`** · **`subscriptions.py:170`** | — | ❌ `False` → **booking reddedilir** |
>
> ⇒ **CHERRY çift kapılı kapalı:** tarla oluşturulamaz, ürün değiştirilemez, booking'e hiç gelmez.
> ⇒ **RICE ters yönde de güvenli:** sunuluyor ama `is_bookable=False` → *"para alınıp teslim
> edilemeyen analiz"* riski de kapalı (VO docstring'inin tam olarak kaçındığı şey).
>
> **Dört küme BİLEREK farklıdır** — `crop_type.py:50-68`'de 2026-07 denetim kararı olarak yazılı:
> (1) `GAP_OFFERED_CROPS` (5, satılan) ⊂ (2) `_VALID_CODES` (7, VO-geçerli: +OLIVE +CHERRY) ·
> (3) wire `crop_type.enum.v1` (8) · (4) worker-internal (12). *"hiçbiri diğerinin yanlış kopyası
> değildir"*. Benim (ve önceki turun) hatası bu eksenleri **tek eksen sanmaktı**.
>
> **`bookable: false` yazmak ayrıca teknik olarak da yanlış olurdu:**
> `tests/unit/test_crop_readiness_manifest_sync.py:97-105` `bookable == (stage1 ∈ {production,
> pilot})` kuralını bağlıyor ve CHERRY'nin `stage1`'i gerçekten `pilot`. Elle düzenleme, tam da
> o testin yakalamak için var olduğu **"insan sync hatası"** olurdu.
>
> **Sonuç:** kod değişikliği **YAPILMADI**; KİRAZ'ı ticari olarak **açma** işi §13 birikmiş
> işler listesine (Ekim 2026+) alındı. **E8'in sıralaması da bu yüzden düzeltildi** (aşağıya bkz.).

**~~EK BULGU — KİRAZ: SİPARİŞ EDİLEBİLİR AMA İKİ YERDEN DÜŞÜYOR~~ (2026-07-30 doğrulama turu — YÜRÜRLÜKTEN KALKTI, gerekçe kaydı olarak korunur).**
Üç kaynak çapraz okundu (`crop_readiness.json` · `crop_type.enum.v1.json` · edge
`ndvi_thresholds.yaml`/`phenology_calendar.yaml`):

| Ürün | `bookable` | contract wire-enum | edge eşik tablosu | Sonuç |
|---|---|---|---|---|
| CORN · PISTACHIO · COTTON · GRAPE | True | ✅ | ✅ | sorunsuz |
| **WHEAT** | True | ✅ | ❌ | edge tablosu yok |
| **CHERRY** | **True** | **❌** | **❌** | **çift kopukluk** |
| SUNFLOWER · OLIVE | **False** | ✅ | ❌ | sipariş edilemez → zararsız |

KİRAZ bugün `bookable:True` — yani **çiftçi sipariş edebiliyor** — ama (1) `crop_type.enum.v1`
8 değerinde YOK → `analysis_job.v1` doğrulaması düşer, worker'a iş hiç gitmez; (2) edge eşik
tablosunda YOK → önceliklendirme eşiksiz kalır.

**E8'in ürün listesinde öncelik ters.** E8 bugün WHEAT + **SUNFLOWER + OLIVE** ekliyor; oysa
SUNFLOWER ve OLIVE `bookable:False`, yani sipariş edilemedikleri için eksiklikleri **zararsız**.
Sipariş edilebilen ve fiilen kırılan tek ürün olan KİRAZ ise listede yok.

**⚠️ EK KANIT (2026-07-31, SSOT hizalaması) — KİRAZ artık ÜÇÜNCÜ yerde de çelişiyor.**
Contract'ın `docs/TARLAANALIZ_SSOT_v1_2_0.txt` kopyası platform'unkiyle hizalandığında, platform'un
**2026-06-14 tarihli KR-024 tablosu** contract'a girdi ve o tablo **`| Kiraz | 14-21 |`** satırını
içeriyor. Yani artık contract deposunun **kendi normatif metni** kirazı desteklenen ürün sayıyor,
ama **kendi `crop_type.enum.v1`'i CHERRY'yi tanımıyor** (doğrulandı: `False`).
→ Tablo **bilerek olduğu gibi alındı** (kaynağa sadakat + bayt-özdeşlik korundu); çelişki
gizlenmedi, buraya yazıldı. **KG-0.d-EK kararı artık üç kaynağı birden bağlar:**
`crop_readiness.json` (bookable) · `crop_type.enum.v1` (wire) · SSOT KR-024 tablosu (normatif metin).

**~~Düzeltme (E8 kapsamı)~~ → YENİDEN DÜZELTİLDİ (2026-07-31): sıralamanın dayanağı çürüdü.**
Eski sıralama *"KİRAZ sipariş edilebilen ve fiilen kırılan tek ürün"* varsayımına dayanıyordu;
o varsayım **yanlış** (yukarıdaki kapanış kutusu). **Doğru ölçüt: `GAP_OFFERED_CROPS`** —
bu sezon fiilen satılan **5 ürün**: `COTTON, CORN, PISTACHIO, RICE, GRAPE`.

| Ürün | Satılıyor mu (`is_gap_offered`) | Wire enum | Edge tablosu | E8 önceliği |
|---|---|---|---|---|
| COTTON · CORN · PISTACHIO · GRAPE · RICE | ✅ | ✅ | ✅ | **iş yok** |
| WHEAT | ❌ satılmıyor | ✅ | ❌ | 🟡 **düşük** — satışa açılırsa gerekir |
| CHERRY | ❌ satılmıyor | ❌ | ❌ | 🟡 §13 (Ekim+) |
| SUNFLOWER · OLIVE | ❌ satılmıyor | ✅ | ❌ | 🟢 ertelenebilir |

⇒ **E8'de bugün ACİL İŞ YOK.** Satılan 5 ürünün beşinde de edge eşik + fenoloji tablosu **var**
(doğrulandı). WHEAT'in *"iki YAML girdisiyle güçlü verili ürün açılır"* kazancı gerçek ama
**satış kapsamına alınması ayrı bir ürün kararına bağlı** — o karar verilmeden tablo yazmak
kullanılmayan config üretir. → E8 **§13'e (Ekim+) taşındı.**

**Etkilenen:** E8 (kapsam düzeltmesi) · W7 · contract `crop_type.enum.v1` (KİRAZ kararına bağlı)
· pilot planı P-3 · demo tasarımı

---

## KARAR 0.e — Geliştirme istasyonu (dev-station) modu ★

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** M1/M2 donanımı temin edilene kadar, pilot ve demo için **tek makinede M1+M2 rollerini
birlikte çalıştıran ayrı bir build profili (`dev-station`)** tanımlanacaktır. Bu profilde
gevşetilen kontroller — air-gap ayrımı, fiziksel medya devri, ayrı mTLS istemci sertifikası,
chassis/boot attestation — **tek tek `build_profiles.yaml`'da adlandırılır** ve
`docs/security/open_items_decisions_2026-06.md`'ye gerekçesiyle kaydedilir. `dev-station`
profiliyle üretilen paketler **üretim kabul edilmez** ve manifestte açıkça etiketlenir.

**Gerekçe.** ADR-007'nin kendi ifadesiyle "makineler henüz alınmadı". Mevcut kod M2 rolünü
(air-gap + fiziksel medya + mTLS) varsayıyor; bu varsayımlar karşılanmadan pilot verisi platforma
**hiçbir yoldan** giremez ve "uçtan uca" demo iddiası dayanaksız kalır.

**Sonuçlar.** (+) Pilot verisi gerçek boru hattından geçer; demo iddiası doğrulanabilir olur.
(+) Gevşetmeler **açık ve sayılı** olduğu için M1/M2 gelince geri alınması izlenebilir.
(−) Güvenlik duruşu geçici olarak zayıflar — bu yüzden etiketleme ve denetim kaydı zorunludur.
(−) İki profil bakımı (dev-station + production) ek yük getirir.

**Kırmızı çizgi.** SHA-256 doğrulaması, WORM custody logu (HC-07), `correlation_id` zorunluluğu
(HC-01), PII yasağı (HC-02) ve CALIBRATED kanıtı olmadan upload yasağı (HC-05)
**dev-station'da da gevşetilmez.**

**Etkilenen:** E1 · `config/build_profiles.yaml` · `open_items_decisions_2026-06.md`

---

## KARAR 0.f — YZ etiket şeması ve üretilemez sınıflar ★

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** İHA görüntüsünden **böcek türü ve birey sayısı tespiti hedefi kaldırılmıştır.** Model
hedefi **"zararlı hasar izi sınıfı + şiddeti"** olarak tanımlanır (ballanma/is mantarı kaplaması,
defolyasyon, kanopi renk/stres anomalisi). Nicel eşikler ve yaşam evreleri (nimf, larva, yumurta)
**yer/tuzak sayımı (YS)** ile toplanır. `analysis_type.enum.v1`'de `BENEFICIAL` ve
`THERMAL_STRESS` değerleri **korunur ancak "üretilemez" olarak işaretlenir**; hiçbir model bu
sınıflarda çıktı vermeyecek şekilde eğitilmez.

**Gerekçe.** Optik sınır: `tarlaanaliz-edge/docs/operations/Tarama_Protokolu_v1.6_Birlesik.txt:349-355` — "20 m'de ÇS ~0,92 cm
≈ 9200 µm, tekil böcek tanıma eşiğinin (~80 µm) **~100 katı kaba** … İHA böceği değil bıraktığı
izi görür. Bu bir uçuş parametresi değil **optik sınırdır**." Bağımsız hesap aynı sonucu veriyor:
10 mm'lik bir böcekte tür ayrımı için ~0,1-0,2 mm/px, yani `H = GSD × 37,2` ile **37-74 cm
irtifa** gerekir — haritalama uçuşu değildir.
*(Düzeltme, 2026-07-30 doğrulama turu: burada önce "74 cm-1,5 m" yazıyordu. 0,1 mm/px →
H = 0,01 cm × 37,2 = **0,37 m**; 0,2 mm/px → **0,74 m**. Eski aralık 2× yüksekti (0,2-0,4 mm/px
ile hesaplanmış görünüyor). **Kararı değiştirmez, güçlendirir:** 37 cm, haritalama uçuşu için
74 cm'den bile daha imkânsızdır. GSD formülleri bağımsız doğrulandı — 20 MP 4/3 → ~H/37,5 ·
5 MP 1/2.8" → ~H/20,1, plandaki H/37,2 ve H/21,7 ile uyumlu.)*
`THERMAL_STRESS` için M3M'de **termal bant yok**;
gerçek `WATER_STRESS` için CWSI (termal) veya NDWI/NDMI (SWIR) gerekir, ikisi de yok.
Sözleşme tarafı bunu zaten kabul etmiş: `expert_review_queue.v1` şeması `BENEFICIAL` için
*"not yet emittable"* diyor.

**Sonuçlar.** (+) Pilot verisi **doğru hedefe** etiketlenir; yanlış etiketlenmiş 3 haftalık veri
riski ortadan kalkar. (+) Ürün iletişimi dürüst kalır. (−) "Böcek sayımı" beklentisi olan
paydaşlara bunun **optik sınır** olduğu açıklanmalıdır. (−) `WATER_STRESS` ve `THERMAL_STRESS`
ancak 5 bantlı + termal sensöre geçişte açılır — yol haritasına yazılır.

**Etkilenen:** C5 · W6 · eğitim etiket şeması · demo anlatısı (§6)

---

## KARAR 0.g — Yazılım lisans yolu ve satın alma

**Statü:** ☑ **ONAYLANDI** · **Tarih:** 2026-07-30 · **Karar veren:** Proje Koordinatörü

**Karar.** FAZ 0 (pilot + demo) **sıfır yazılım maliyetiyle** yürütülecektir: M3M ile gelen
**DJI Terra Full-Featured 3 ay** (RTX 3090'lı masaüstüne aktive edilir; ücretsiz lisans geri
alınamaz) + **OpenDroneMap** (ücretsiz, otomasyon motoru) + **QGIS/Precision Zones** +
**Sentinel-2/Copernicus**. Metashape 30 gün denemesi **demo tarihinden 3 hafta önce** başlatılır.
PIX4Dfields'e ödeme yapılmaz (deneme sürümü **çıktı export etmiyor**). Paralel olarak Agisoft ve
Pix4D'den **eğitim/araştırma lisansı** uygunluğu ve fiyatı yazılı sorulur; uygun çıkarsa **kamu
satın alma süreci hemen başlatılır.**

**Gerekçe.** Proje kamunun araştırma projesi olduğundan Agisoft'un Service Provider lisansı
($6.736/yıl/makine) **muhtemelen gereksizdir** — üçüncü taraf adına ticari işleme yapılmıyor.
Node-locked Professional ($3.499) veya akredite kuruluş şartı karşılanıyorsa **eğitim lisansı**
yeterli olabilir. Kamu satın alma prosedürü (doğrudan temin/ihale) **takvimi uzattığı** için sorgu
şimdi başlatılmalıdır. FAZ 0'da ücretli yazılıma ihtiyaç yoktur: Terra M3M'i yerli olarak işler,
ODM otomasyonu sağlar.

**Sonuçlar.** (+) İkna aşaması **0 TL**. (+) Motor kararı (FAZ 1) pilotun ölçtüğü
"Terra-NDVI ↔ ODM-NDVI farkı"na dayanır, tahmine değil. (−) Metashape 30 günü **tek kullanımlık**;
takvim hatası bu kaynağı yakar. (−) Eğitim lisansı uygunluğu **kurumun akreditasyon durumuna
bağlı** ve henüz teyitli değil.

**Açık kalem.** Agisoft eğitim lisansı "akredite eğitim kurumları, çalışanları ve öğrencileri"
ile sınırlıdır; kurumun bu tanıma girip girmediği **yazılı teyit gerektirir.**

**İKİNCİ AÇIK KALEM — "TERRA'NIN CLI'Sİ YOK" İDDİASI TEYİTLİ DEĞİL (2026-07-30 doğrulama turu).**
Bu iddia planın birçok yerinde **mimari dayanak** olarak kullanılıyor — en ağırı **E6**: Terra
runner'ı "süreç başlatıcı değil, **çıktı klasörü izleyici**" olarak tasarlanıyor. Yani yanlışsa
E6 baştan yazılır.

*Doğrulama denemesi:* bağımsız arama iddiayı **ne doğruladı ne çürüttü**; DJI'ın resmi
dokümantasyonunda Terra için CLI/API/batch başlığına rastlanmadı, ama **yokluk kanıtı da
bulunamadı**. Negatif iddialar doğası gereği aramayla kapatılamaz (bkz. bu turun dersi: *boş
arama sonucu bir şeyin YOK olduğunu kanıtlamaz*).

*Bağlayıcı adım:* **E6'ya kod yazılmadan önce** DJI'dan (kurumsal destek / yetkili satıcı)
**yazılı** cevap alınır: (a) Terra'nın komut satırı / betik / toplu-iş arayüzü var mı, (b) varsa
hangi lisans seviyesinde (Agriculture $300/yıl dâhil mi, yoksa Cluster mı), (c) çıktı dosya
adları dokümante mi. (c) zaten **ölçüm #2** ile sahada teyit edilecek; (a)-(b) satın alma
sorgusuyla (§5.3 madde 5) **aynı yazıda** sorulur — ek maliyeti yok.

*Risk kabulü:* cevap gelene kadar E6 **klasör izleyici** varsayımıyla tasarlanır (güvenli taraf:
CLI çıkarsa izleyici yine çalışır, tersi doğru değildir). Cevap "CLI var" gelirse E6 sadeleşir.

**Etkilenen:** §5.3 madde 1, 5 · E6 (tasarım varsayımı) · §7 bulgu 1-3 · FAZ 1 motor kararı ·
satın alma takvimi

---

## Karar özeti tablosu — hepsi ONAYLI (2026-07-30)

| # | Karar | Statü | Tip | ADR | Ana etkisi |
|---|---|---|---|---|---|
| 0.a | Manifest + presigned PUT (**önkoşul: E14**) | ☑ Onaylı | mimari | — | C13 + C16 + ham kare tek mekanizmada |
| 0.b | **Y-D** — öncelik bölgesi kaynaklı ÖN RAPOR *(~~Y-C~~ KG-0.b-R ile değiştirildi)* | ☑ Onaylı | governance | ★ ADR-007 yorum notu (**Y-D'yi** anlatır) | ADR-004/005/007 korunur · **C9+C10 ön koşul** |
| 0.c | Yalnız işaretli kareler | ☑ Onaylı | mimari | — | 533 GB/gün → yönetilebilir |
| 0.d | Üzüm pilot + fıstık demo | ☑ Onaylı | ürün | — | `bookable`+`strong` ürünle çalışma |
| 0.e | dev-station profili | ☑ Onaylı | güvenlik | ★ yeni ADR | Pilot verisi platforma girebilir |
| 0.f | Hasar izi sınıfı + şiddeti | ☑ Onaylı | ürün/YZ | ★ contract metadata notu | Yanlış etiketleme riski kapanır |
| 0.g | FAZ 0 sıfır maliyet | ☑ Onaylı | mali | — | İkna aşaması 0 TL |

**2026-07-30 doğrulama turu — kararlara EK (hiçbiri kararı geri almaz):**

| Kod | Ne | Statü | Neden önemli |
|---|---|---|---|
| **0.a-EK** | Anahtar sahipliği: **platform üretir**, edge'in yolu asla imzalanmaz | ☑ uygulamayı bağlar | `patches.py:165` bugün edge'in yolunu imzalıyor → çapraz-kiracı sızıntı riski |
| **0.b-R** 🔄 | **REVİZE:** ÖN RAPOR = `analysis_priority_zones`'un çiftçiye sunulması (**Y-D**). ~~Y-C/ertele~~ yürürlükten kalktı | ☑ **Onaylı 2026-07-30** (koordinatör direktifi) | Çiftçi kalibrasyondan sonra **sorunlu kırmızı NDVI bölgelerini** görür. Yeni faz/state **yok**; PRELIMINARY'ye yeni içerik kaynağı. KR-019/033/025 ve ADR-007 §2 **korunur**. Yeni: **P6** (yeniden tanım) + **P12** + **E12 açılır** |
| **0.d-EK** | **KİRAZ** sipariş edilebilir ama wire-enum + edge tablosunda yok | ⏳ **karar bekliyor** (ürün) | Sipariş açıkken risk canlı; E8 sırası düzeltildi |
| **0.g-EK** | "Terra'nın CLI'si yok" **teyitli değil** — E6'nın tasarımı buna dayanıyor | ⏳ açık kalem | DJI'dan yazılı cevap; satın alma yazısına eklenir (ek maliyet yok) |
| **0.f-düzeltme** | Optik sınır irtifası **37-74 cm** (önce "74 cm-1,5 m" yazıyordu, 2× yüksek) | ☑ düzeltildi | Kararı **güçlendirir**; GSD formülleri bağımsız doğrulandı |

### 🔬 2026-07-31 BAĞIMSIZ DENETİM TURU — plana işlenen düzeltmeler

**Yöntem:** İki turlu; her iddia bugünkü koda/şemaya karşı ölçüldü, sonra denetimin kendisi tersine
sınandı (1 iddia geri çekildi, 1 şiddet düşürüldü, 4 yeni bulgu). **Kanıt arşivi:**
`denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` (her satırın `dosya:satır` dayanağı orada).
**Hiçbir onaylı karar geri alınmadı** — düzeltmeler kalemlerin **hedefini, sırasını ve kapsamını** bağlar.

| Kod | Ne değişti | Etkilenen kalem |
|---|---|---|
| **D-1** | C1/C2/C3 **yanlış şemayı hedefliyordu.** İki `calibrated_dataset_manifest.v1` formu var (edge = kanıt manifesti · platform = paket agregası) ve **`patches` alanı contract'ın hiçbir şemasında yok**; göreli yol `intake_manifest.v1 EdgeForm.priority_zones[].visualizations`'ta | **C0** (yeni) · **C1′ C2′ C2″ C3′** |
| **D-2** | **`priority_zones` yalnız `EdgeForm`'da**, `PlatformForm`'da yok → 0.a-EK "anahtarı platform üretir" kuralıyla çelişiyordu | **C2′** |
| **D-3** | **C4 contract kalemi değil** — `sorties` contract'ta hiç yok, edge-yerel manifestte | C4 kapatıldı → **E9** |
| **D-4** | **C5 zaten yapılmış** (v1.4.1: `enum_valid_not_yet_emittable` + `requires_thermal_payload`/"Mavic 3M'de üretilemez") | C5 kapatıldı |
| **D-5** | **C6 "iş yok" yanlıştı** — `x-context-subsets['edge/calibrated_dataset_manifest']` yalnız `["ABSOLUTE","RELATIVE"]`; `DLS2_RELATIVE` kabul edilmiyor | **C6 koşullu açık** · **E13 önce** |
| **D-6** | **"Şema değişmez" iddiası kanonikle çelişiyor** — iki artefakt PRELIMINARY içeriğini "YALNIZ 4 kalem" diye kapatıyor **ve** `report_phase` mapping'inde kalibrasyon-sonrası statü yok | **C9 + C10** (yeni) · P6 · P12 |
| **D-7** | **KR-093 kanonik registry'de yok** (`ssot/kr_registry.md` KR-092'de bitiyor) ama contract artefaktları ona normatif atıf yapıyor | **C9 ön koşulu** |
| **D-8** | **Demo kritik yolunda ekran yoktu** — ①–⑥ hepsi API'de bitiyordu; `platform/web/` mevcut | **WEB1 + WEB2** (yeni) · adım **⑦** |
| **D-9** | **E12 ↔ KİLİT-2 kuralı hiçbir kaleme bağlı değildi**; tek kota kalemi demodan sonraydı | **P9a** (Dalga 2) · P9b (Dalga 4) |
| **D-10** | **0.a-EK Kural 3 işlevsizdi (no-op)** — kod zaten DB'den okuyor; kapatma yalnız "DB'ye platform anahtarı yazılır" ile olur. Şiddet 🔴→🟠 (sahiplik kapısı var) | Kural 3 · **P4** |
| **D-11** | **E9'un gerekçesi bayattı** — çöküş zaten sesli (`PRIORITIZATION.MIXED_CROP` denetim olayı); gerçek karar "uyarı mı sert hata mı" | **E9** yeniden yazıldı |
| **D-12** | **AL-C1/C2 tur çelişkisi** — §11.2 "Tur 2", devir notu "Tur 1" diyordu | **Tur 1** (bağlayıcı) |
| **D-13** | §9.1 kopyala-yapıştır blokları **yürürlükten kalkmış Y-C metnini** taşıyordu | §9 özet · §9.1-A · §9.1-C |
| **D-14** | **ADR-009 iki işe verilmişti**; platform ADR'leri 008'de bitiyor | ADR-009 = dev-station |
| **D-15** | `report_phase` mapping'i **kanonik olmayan `ANALYZING`** adını kullanıyor (`mission_status.enum.v1`'de `IN_ANALYSIS` var) | **C10** ile birlikte |
| **D-16** | Başlıkta **silinmiş dosyaya atıf** vardı (`fotogrametri_yazilim_karsilastirmasi_2026-07-29.md`) | başlık düzeltildi |

**Depo durumu (2026-07-31 ölçüldü):** contract **`7.2.0`** · checksum `5d3c204d…` · dört etiket de
**annotated** → **I-2 tutuyor** · platform **7.2.0** · worker **v7.2.0** · edge **1.3.0** (kendi şeması)
→ **I-1 tutuyor.** `pin_version.py --verify` ✅ · `validate.py` ✅ 89 dosya / 0 hata.
*(Devir notu §1 bunu `7.0.1` sanıyordu — iki sürüm bayattı, düzeltildi.)*

---

## 9.1 — Yönetişim kayıt satırları (kopyala-yapıştır)

### A) `tarlaanaliz-platform/docs/security/open_items_decisions_2026-06.md` → eklenecek

```markdown
## Karar Günü — 2026-07-30 (Proje Koordinatörü)

| Kod | Karar | Tip | Etkilenen | Statü |
|-----|-------|-----|-----------|-------|
| KG-0.a | Edge→Platform taşıma: manifest + presigned PUT; platform ikili gövde ucu AÇMAZ. **Önkoşul: E14 kalibrasyon kanıtı üreticisi (C13'ten önce).** | DECIDED | C13, C16 | Uygulama Dalga 1-2 |
| KG-0.b | ~~ÖN RAPOR: direktif **Y-C** (rapor değil durum bildirimi + ham katman) ile karşılanır.~~ ⟵ **KG-0.b-R (Y-D) ile DEĞİŞTİRİLDİ; yürürlükte değildir.** Tarihçe kaydı olarak korunur. | **SUPERSEDED** | C15 | Yürürlükteki karar: **KG-0.b-R** |
| KG-0.c | Ham kareler bütün olarak merkeze gitmez; yalnız işaretli yamaları gören kareler (`raw_frames[]`). | DECIDED | C3, E11 | Depolama üst sınırı ilk uçuşta teyit |
| KG-0.d | Pilot birincil ürün ÜZÜM; demo ana hikâyesi ANTEP FISTIĞI; YZ tespit vitrini ÜZÜM. Pamuk/çeltik/zeytin/ayçiçeği pilot dışı. Kaynak: `crop_readiness.json`. | DECIDED | E8, W7 | BUĞDAY için iki YAML girdisi açılacak |
| KG-0.e | `dev-station` build profili: M1+M2 tek makinede. Gevşetmeler `build_profiles.yaml`'da tek tek adlandırılır; paketler "üretim değil" etiketlenir. Kırmızı çizgi: HC-01/02/05/07 ve SHA-256 gevşetilmez. | DECIDED | E1 | Yeni ADR gerekir |
| KG-0.f | YZ hedefi "böcek türü+sayısı" DEĞİL, "zararlı hasar izi sınıfı + şiddeti". `BENEFICIAL` ve `THERMAL_STRESS` "üretilemez" işaretli. Gerekçe: optik sınır (protokol §10, ~100 kat kaba). | DECIDED | C5, W6 | Contract metadata notu |
| KG-0.g | FAZ 0 sıfır yazılım maliyeti (Terra hediye + ODM + QGIS + Sentinel-2). Metashape 30 gün demo−3 hafta. Eğitim/araştırma lisansı sorgusu + kamu satın alma başlatılır. | DECIDED | — | Akreditasyon teyidi açık kalem |

<!-- 2026-07-30 doğrulama turu — kararları DEĞİŞTİRMEZ, uygulamayı bağlar -->
| KG-0.a-EK | **Anahtar sahipliği:** nesne anahtarını **platform üretir**; edge'in verdiği yol ASLA imzalanmaz. GET presign'da anahtar DB'den okunur. Gerekçe: `patches.py:165` bugün edge'in göreli yolunu imzalıyor → **çapraz-kiracı sızıntı riski**. Kabul testi: sahte manifestle başka kiracı yolu → 403/deny. | DECIDED | P3, P4, E10 | Uygulama Dalga 1-2 |
| KG-0.b-R | **REVİZE (koordinatör direktifi):** ÖN RAPOR = **`analysis_priority_zones`'un çiftçiye sunulması** (Y-D). Çiftçi, kalibrasyondan sonra tarlasındaki **sorunlu kırmızı NDVI bölgelerini** (`geom` + `ndvi_value` + `ndvi_overlay`) "ÖN RAPOR" başlığı altında görür. **Yeni faz/mission state EKLENMEZ** — `results_service_impl.py:227` zaten `PRELIMINARY` türetiyor; eklenen yalnız **içerik kaynağı**. KR-019 (tespit yok), KR-033 (ödeme kapılı), KR-025 (reçete yok), ADR-007 §2 **korunur**. Önceki "FAZ 1'e ertele" kararı yürürlükten kalktı. | **DECIDED** | P6 (yeniden tanım), P12 (yeni), E12 (aç) | ADR-007 yorum notu Y-D'yi anlatacak; demo kritik yolu |
| KG-0.d-EK | **KİRAZ:** `bookable:True` ama contract wire-enum'da ve edge tablosunda YOK → sipariş edilebiliyor, iş iki yerden düşüyor. E8 sırası: ① KİRAZ kararı (bookable:False **veya** enum+tablo) ② WHEAT ③ SUNFLOWER/OLIVE ertelenebilir (`bookable:False` → zararsız). | **KARAR BEKLİYOR** (ürün) | E8, `crop_type.enum.v1` | Sipariş açıkken risk canlı |
| KG-0.g-EK | **"Terra'nın CLI'si yok" teyitli değil** — E6'nın tasarımı buna dayanıyor. DJI'dan yazılı cevap (CLI var mı · hangi lisansta · çıktı adları dokümante mi) satın alma sorgusuyla aynı yazıda istenir. Cevaba kadar E6 "klasör izleyici" varsayımıyla tasarlanır (güvenli taraf). | AÇIK KALEM | E6, §7 bulgu 1-3 | Cevap gelmeden E6 kodlanmaz |

<!-- 2026-07-31 bağımsız denetim turu — kararları DEĞİŞTİRMEZ, kalemlerin hedef/sıra/kapsamını bağlar -->
| KG-0.b-R2 | **ÖN RAPOR kanonik tanımı genişletilir.** `analysis_preliminary_ready.v1` ve `report_phase.enum.v1` PRELIMINARY içeriğini **"YALNIZ deterministik indeks katmanları + overall_health_index"** diye kapatıyor; öncelik bölgesi (poligon + `ndvi_value` + `ndvi_overlay`) listede YOK. Ayrıca `report_phase.x-derived-from.mapping`'de **kalibrasyon-sonrası statü yok** (`UPLOADED` eksik); "çalışıyor" görünmesinin sebebi platformun catch-all'u (`results_service_impl.py:227`). → **C9 + C10.** Ön koşul: **KR-093 kaydı contract `ssot/kr_registry.md`'ye taşınmalı** (bugün KR-092'de bitiyor). | DECIDED | C9, C10, P6, P12 | Y-D kararı değişmez; kanonik tanım onu kapsar |
| KG-0.a-EK2 | **Anahtar sahipliği kuralı 3 düzeltildi.** Eski hâli (*"GET presign'da anahtar DB'den okunur"*) **işlevsizdi** — kod bunu zaten yapıyor (`patches.py:151`). Yürürlükteki kural: *anahtar DB'den okunur **VE DB'ye yalnız platformun ürettiği anahtar yazılır**.* Şiddet 🔴→🟠: sahiplik kapısı var (`patches.py:118-148`), sömürü **ele geçirilmiş edge + atanmış uzman** ister. Kabul testi **iki koşullu** kurulur. | DECIDED | P4, `ingest_service_impl.py:266` | Tek koşullu test bugün de yeşil geçer |
| KG-0.b-WEB | **Demo kritik yoluna ⑦ ARAYÜZ adımı eklendi.** ①–⑥'nın hepsi API'de bitiyordu; `tarlaanaliz-platform/web/` mevcut ve `REPO_BOUNDARY_RULES.txt` web'i bağlayıcı biçimde ayrı tüketici sayıyor. → **WEB1** (ÖN RAPOR ekranı) + **WEB2** (kapı/boş-durum mesajları). Dalga 2 **+3-5 gün**. | DECIDED | WEB1, WEB2 | Ekransız demo API cevabında kalır |
| KG-0.e-E12 | **E12 ön koşulu bir kaleme bağlandı.** §10.5/§11.5 kuralı ("KİLİT-2 kapalıyken açılmaz; ya dedup ya kota") yazılıydı ama **hiçbir iş kalemi yoktu**; tek kota kalemi (P9) demodan sonraydı. → **P9a** (pilot kota tavanı, Dalga 2, E12 ile aynı sürüm) + **P9b** (kalıcı kota, Dalga 4). | DECIDED | E12, P9a, P9b | Aksi hâlde plan demo gecesi kendi kuralını ihlal eder |
| KG-C-TUR1 | **Contract Tur 1 yeniden tanımlandı:** `C0 + C1′ + C2′ + C2″ + C3′ + C9 + C10 + AL-C1 + AL-C2` (+C6 koşullu). **C4 düştü** (contract kalemi değil), **C5 düştü** (yapılmış). AL-C1/C2 Tur 2'den **Tur 1'e alındı** — [0] ölçüm temelinin tek açılabilir kilidi. | DECIDED | §3.1, §5.1, §11.2 | Kanıt: `denetim/…_2026-07-31_…md` |
```

### B) `tarlaanaliz-platform/docs/architecture/end_to_end_workflow.md` → durum güncellemesi

```markdown
| C13 | ... | **KARAR VERİLDİ (2026-07-30, KG-0.a):** manifest + presigned PUT modeli seçildi;
platformda ikili gövde ucu açılmayacak. ⚠️ Önkoşul: kalibrasyon kanıtı üreticisi (E14) —
`calibration_result`/`observed_footprint_wkt` beş yerde tüketiliyor, sıfır yerde üretiliyor;
o yazılmadan hat bağlansa bile HC-05 M1 içinde durur. |
| C15 | ... | **KAPATILDI (2026-07-30, KG-0.b-R) — Y-D ile.** ADR-007 §2/§5 korunur; kod zaten
ADR'ye sadıktı (`worker_bridge_consumer.py:1565` = **bildirim**, ADR-007 §5'in birebir uygulaması).
Direktif, ÖN RAPOR'un **`analysis_priority_zones`'tan** sunulmasıyla karşılanır: çiftçi
kalibrasyondan sonra sorunlu NDVI bölgelerini (`geom` + `ndvi_value` + `ndvi_overlay`) görür.
**Yeni faz/mission state eklenmez** — `results_service_impl.py:227` zaten `PRELIMINARY` türetiyor;
eklenen yalnız **içerik kaynağı** (P12) + **çiftçi okuma ucu** (P6). KR-019/033/025 korunur.
⚠️ **BU MADDENİN ESKİ METNİ DÜZELTİLMELİ:** *"Pix4D çıktısını platforma taşıyan bir yol yok"*
ifadesi **yanlıştır.** Doğrusu: **türetilmiş** ürün için yol **TANIMLI ama BAĞLI DEĞİL** —
`ingest.py:71` `PriorityZoneEntry` (geom + ndvi_value + visualizations) intake manifestinde
taşınıyor ve `ingest_service_impl.py:266` `analysis_priority_zones`'a yazıyor; eksik olan
`submit_manifest`'in çağrılması (C13). **Yol yokluğu değil, tesisat eksikliği.**
Tam çözünürlüklü ham rasterlar (ortho/ndvi .tif) için ise gerçekten yol yok → C1 `index_layers[]`. |
| C16 | ... | **KARAR VERİLDİ (2026-07-30, KG-0.a):** presigned mekanizmasıyla aynı işte çözülür;
yama görselleri `object_key` taşıyacak (C2 + E10 + P4). ⚠️ **Statü yükseldi:** KG-0.b-R ile
**demo kritik yoluna** girdi — `ndvi_overlay` bu madde olmadan merkeze ulaşmaz. |
```

### C) ★ ADR işleri

| Karar | Yapılacak | Dosya |
|---|---|---|
| 0.b | ADR-007'ye **yorum notu (Y-D metni — 2026-07-31'de düzeltildi):** *"2026-07-29 ürün direktifi **KG-0.b-R ile Y-D** biçiminde karşılandı: ÖN RAPOR içeriği `analysis_priority_zones`'tan sunulur. **Yeni mission state / yeni faz eklenmedi**; §2 ve §5 değişmedi. İçerik tanımı C9, statü eşlemesi C10 ile kanonikleştirildi."* ADR yeniden yazılmaz. ⚠️ Eski taslak metin "Y-C" diyordu — **yürürlükten kalkmış kararı** ADR'ye yazdıracaktı | `docs/adr/ADR-007-preliminary-farmer-view.md` |
| 0.e | **Yeni ADR — ADR-009 (numara doğrulandı 2026-07-31: platform ADR'leri ADR-008'de bitiyor, 009 boş):** dev-station profili, gevşetilen kontrollerin listesi, kırmızı çizgiler, geri alma koşulu (M1/M2 teslim). ⚠️ **ADR-009 bu işe tahsis edilmiştir**; Y-A ileride canlanırsa **başka numara** alır | `docs/adr/ADR-009-dev-station-profile.md` |
| **P-10 / C9** | **KR-093 kaydını kanonik registry'ye taşı** — bugün `ssot/kr_registry.md` **KR-092'de bitiyor** ve `ssot/contracts_ssot.md`'de de yok; oysa contract'ın kendi artefaktları (`report_phase.enum.v1`, `analysis_preliminary_ready.v1`) KR-093'e **normatif** atıf yapıyor → sarkan kanonik atıf. Tanımı olmayan KR değiştirilemez, **C9'un ön koşuludur** | `tarlaanaliz-contract/ssot/kr_registry.md` (kaynak: platform `docs/kr/kr_registry.md`) |
| 0.f | `analysis_type.enum.v1.json` **metadata notu**: `BENEFICIAL` ve `THERMAL_STRESS` için "not producible with current sensor/model set" + gerekçe | `tarlaanaliz-contract/enums/analysis_type.enum.v1.json` |

---

# 10. AKTİF ÖĞRENME DOSYALARIYLA ÇAPRAZ ANALİZ (2026-07-30)

**Karşılaştırılan kaynaklar:** `aktif_ogrenme_secim_tasarimi_S1_S2_dedup.md` (tasarım, 787 satır) +
`aktif_ogrenme_S1_S2_dedup_worker_uygulanabilirlik_denetimi_2026-07-18.md` (kod-doğrulamalı
denetim, 375 satır) ⟷ bu eylem planı.
**Yöntem:** Her iddia bugünkü kod/config ile teyit edildi; doküman değil **kod otoritatif** alındı.

## 10.1 🔴 BİRBİRİNİ YALANLAYAN — 1 kritik

### Ç-1 · KG-0.d "üzüm = YZ tespit vitrini" ↔ EK-A + üzüm veri setinin çekim alanı

**Çelişki.** KG-0.d, üzümü YZ tespit vitrini seçti (gerekçe: `crop_readiness` → GRAPE `strong`).
Ama üzümün `strong` verisi **Botrytis**tir ve üç kaynak birden bunun **nadir uçuşla
örtüşmediğini** söylüyor:

| Kaynak | Ne diyor |
|---|---|
| **EK-A tespit matrisi** | Üzümde **Botrytis** → "❌ Fiziksel olarak MS-görünmez (**salkımda, kanopi altında örtülü**)" |
| `config/grape_datasets.yaml` | `zenodo_botrytis_tomino_2022` → **altitude_m=30, gsd_cm=2.0, flight_angle=mixed** — "multi-angle (**nadir+30°+45°**)" |
| `scripts/odm_run_botrytis.sh:45` | `ALL_FLIGHTS=(0_V1 0_V2 30_V1 45_V1)` — üç ayrı **açı** |
| **Bu planın §2.3 uçuş kuralı** | Gimbal **−90° (saf nadir)**, sensör **M3M** |

**Sonuç:** Botrytis nadirden görünmediği için eğitim seti **eğik (oblik) açılarla** toplanmış.
Pilot protokolü saf nadir ve **M3M** (eğitim seti **MicaSense RedEdge 3**) olduğundan,
**pilot uçuşu Botrytis eğitim alanını üretmez.** "Üzümde YZ tespiti çalışıyor" demosu,
pilotun örneklemediği bir alana dayanır.

**Üç çözüm yolu:**
| # | Yol | Bedeli |
|---|---|---|
| **A (önerilen)** | **YZ vitrinini MISIR/OT'a çevir.** EK-A: Mısır → "✅ Karışık ot (**veri güçlü**)" ve ot **nadirden görünür**; `crop_readiness` CORN = `strong`+`bookable`. Nadir pilot ile **alan uyumlu** | Üzüm hikâyesi vitrinden düşer (pilot ürünü olarak kalabilir) |
| B | Üzüm uçuşlarına **eğik açı geçişi** ekle (nadir + 30°/45°) | Protokol + uçuş süresi artar; M3M↔RedEdge 3 sensör farkı yine kalır |
| C | Botrytis modelini **orijinal veri setinde** göster, pilot verisinde değil — ve bunu demoda açıkça söyle | Dürüst ama "kendi verimizde çalışıyor" iddiası zayıflar |

⚠️ **Yan bulgu (worker içi tutarsızlık):** `odm_run_botrytis.sh:6` "per **altitude** (0/30/45)" diyor,
`grape_datasets.yaml` ise aynı seti "multi-**angle** (nadir+30°+45°)" olarak tanımlıyor.
İkisi aynı şeyi farklı adlandırıyor → düzeltilmeli (yanlış olan script yorumu).

## 10.2 🟠 ÇAKIŞAN / KAPSAM DIŞI KALAN — 2

### Ç-2 · `encoder_version` tetikleyici listesinde **kalibrasyon motoru değişimi YOK**

Her iki dosyada da liste **birebir aynı** ve dört öğeli:
*"SSL yeniden-eğitim / omurga swap (takası) / kanal-transfer göçü / Faz-2 ViT LoRA'nın attention
`out_proj`'a ulaşması"* (denetim §G.5, §G.5.1; tasarım satır 537).

**Eksik olan:** **kalibrasyon motoru değişimi.** Oysa bu planın kendisi motor değişimi öngörüyor
(FAZ 0 Terra/ODM → FAZ 1 ODM veya Metashape) ve **W2** motorlar arası reflektans ölçeğinin
farklı olduğunu kayda geçiriyor (ODM 0-1 · Metashape 32768 · Terra ölçülecek). Reflektans ölçeği
değişince **encoder'a giren dağılım değişir** → saklı FAISS gömmeleri yeni gömmelerle
kıyaslanamaz hâle gelir. Bu, KİLİT-1'in tam olarak kapattığı hata sınıfıdır — ama tetikleyici
**model tarafında** değil **kalibrasyon tarafında** olduğu için guard bunu görmez.

**Yapılacak (yeni iş kalemi — W8):** `encoder_version` artırma tetikleyici listesine
**"kalibrasyon motoru veya reflektans ölçeği değişimi"** eklensin; tercihen
`model_registry.yaml`'a `calibration_engine` alanı konup değişimi runbook'ta zorunlu artırıma
bağlansın. **Maliyeti düşük, atlanması sessiz ve pahalı.**

### Ç-3 · Mahsul sayısı üç kaynakta üç farklı

| Kaynak | Mahsul sayısı |
|---|---|
| `crop_type.enum.v1.json` (contract) | **8** (COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, RICE) |
| `crop_readiness.json` (worker-kanonik) | **12** (+CHERRY, APPLE, PEACH, FIG) |
| **EK-A** tespit matrisi | **5** (pamuk, mısır, fıstık, çeltik, üzüm) |

Denetim raporu bunu **#4-kritik** olarak zaten işaretlemiş ("EK-A dışı 7 mahsulün duyusal-tavan
analizi eksik"). Bu plan ise **W7**'de aynı boşluğa veri-seti açısından bakıyor.
→ **Aynı boşluğun üç yüzü.** Birleşik iş: contract↔readiness enum hizası + EK-A'yı 8 contract
mahsulüne genişletme + veri seti kararı. **W7 kapsamı bu üçünü kapsayacak şekilde genişletilmeli.**

## 10.3 🟢 BİRBİRİNİ TAMAMLAYAN — 4

### T-1 · Pilot, S1 router'ın **kilidini açan** şeydir

Denetim G.4-[2]: S1 router kodu hazır, `router_density: null` × 8 → **veri-kapılı**
("ağırlıklar GAP saha verisini bekliyor; mahsullerin `pilot` olma sebebiyle aynı kök").
Bu planın pilotu (üzüm/fıstık, 3 hafta, haftalık döngü) **tam olarak o veriyi üretir.**
→ **Pilot ⇒ etiketli veri ⇒ LoRA adaptörü ⇒ yoğunluk artefaktı fit ⇒ shadow→pilot promosyon.**
Bu zincir hiçbir dokümanda yazılı değil; **pilotun ikinci gerekçesi** budur (birincisi demo).

### T-2 · EK-A, KG-0.f'in mahsul düzeyindeki karşılığıdır — ve **tam mutabık**

KG-0.f: "böcek türü/sayısı değil, **hasar izi sınıfı + şiddeti**".
EK-A bağımsız olarak aynı sonuca varmış:
- Pamuk ❌ "4 emici zararlının **tür ayrımı** → spektral olarak **tek** stres"
- Fıstık ✅ "Psillid — **ballıböcek/honeydew** NDWI+Green" ⟵ **böcek değil, izi**
- Mısır ❌ "koçankurdu (sap içi), tel kurdu (toprak)" · Üzüm ❌ "salkım güvesi larvası (tane içi)"

→ **Çelişki yok, güçlü teyit var.** EK-A pratikte **W6'nın etiket taksonomisi kaynağıdır** —
sıfırdan sınıf listesi yazmayın, EK-A'nın ✅/⚠️/❌ sütunlarını etiket şemasına çevirin.

### T-3 · E12 (NDVI önceliklendirme) ↔ KİLİT-2 (dedup ölü) — **tehlikeli etkileşim**

Bu plan **P9**'da uyarıyor: E12 bayrağı açılınca `analysis_priority_zones` dolar → uzman kotası
1→N sıçrar. Denetim raporu ise **KİLİT-2**'yi bildiriyor: `should_send_to_expert` çağrısız,
yani **uzman yükünü azaltacak dedup mekanizması ölü.**

→ **Birleşik sonuç (hiçbir dokümanda yok):** E12'yi KİLİT-2 kapalıyken açmak, uzman yükünü
**hem artırır hem de azaltıcıyı devre dışı bırakır** — en kötü kombinasyon.
**Sıralama kuralı:** E12 açılmadan önce ya dedup canlıya bağlanmalı (F1/F4/F5 ön-koşullarıyla)
ya da uzman kapasitesi ölçülüp kota manuel sınırlanmalı.

### T-4 · Aynı mühendislik disiplini iki yerde: "bağlamadan önce ön-koşul"

- **E14** (bu plan): kalibrasyon kanıtı üreticisi **C13'ten önce** — yoksa HC-05 M1'de takılır
- **F1/F4/F5** (denetim #2): saflık kapısı + nadir/karantina hariç + doğru uzay,
  **dedup canlıya bağlanmadan önce** — "sonradan eklenen yama değil"

→ Aynı kural, iki bağımsız yerde. **Genel ilke olarak yazılmalı:** *bir hattı canlıya bağlamadan
önce, o hattın sessizce bozacağı kanıt/kalite kapıları önce kurulur.*

## 10.4 ⚪ MUTABAKAT GEREKEN (çelişki değil, birim uyuşmazlığı)

**Ölçek varsayımları karşılaştırılamıyor.** Tasarım dokümanı: "2026 pilot — 6 hafta,
**100k–600k görüntü/gün**, 5 bitki × 6 katman · Uzman havuzu: **40 ziraat mühendisi**".
Bu plan: 1 drone, günde 8-12 uçuş → **~47-63 bin ham dosya/gün**, 3-5 tarla, 1-2 ürün.

⚠️ İki sayı **aynı birimde değil**: tasarımdaki "görüntü" büyük olasılıkla **tile** (ortodan
kesilen yama), buradaki ise **ham kare**. Bir ortomozaikten çıkan tile sayısı ham kare sayısından
çok daha fazladır. → **Çelişki ilan etmiyorum**; ama S2'nin bütün gerekçesi "uzman darboğazı"
olduğu için **pilot verisiyle tile/gün ve gerçek uzman sayısı ölçülüp bu varsayımlar
güncellenmelidir.** 40 uzman varsayımı da bu planda hiçbir yerde doğrulanmış değil.

## 10.5 Bu analizden doğan yeni iş kalemleri

| # | İş | Repo | Öncelik |
|---|---|---|---|
| **W8** | `encoder_version` tetikleyici listesine **kalibrasyon motoru/reflektans ölçeği değişimi** eklensin; `model_registry.yaml`'a `calibration_engine` alanı + runbook kuralı | worker + contract | 🔴 Yüksek (sessiz hata sınıfı) |
| **W7+** | W7 kapsamı genişletilsin: veri seti boşluğu **+** contract(8)↔readiness(12) enum hizası **+** EK-A'yı 8 mahsule genişletme | worker + contract | 🟠 Orta |
| **W9** | **W6 etiket şeması EK-A'dan türetilsin** — sıfırdan yazma; EK-A ✅/⚠️/❌ sütunları taksonomiye çevrilsin | worker | 🟠 Orta |
| **KG-0.d gözden geçirme** | YZ tespit vitrini: üzüm/Botrytis → **mısır/ot** (Ç-1 seçenek A) — **karar sizin** | — | 🔴 Demo öncesi |
| **E12 sıra kuralı** | E12, KİLİT-2 kapalıyken açılmaz; ya dedup bağlanır ya kota manuel sınırlanır. ✅ **2026-07-31: iş kalemine bağlandı** → **P9a** (pilot kota tavanı, Dalga 2, E12 ile aynı sürüm). Önceden kural yazılıydı ama **hiçbir kaleme bağlı değildi** | edge + platform | 🔴 **E12 ön koşulu** |
| **Ölçek mutabakatı** | Pilotta tile/gün ölçülsün; tasarımın 100k-600k ve 40-uzman varsayımları güncellensin | — | 🟡 Pilot çıktısı |
| **Küçük düzeltme** | `odm_run_botrytis.sh:6` yorumu "per altitude" → "per **angle**" | worker | 🟢 Düşük |

---

# 11. AKTİF ÖĞRENME HATTININ AÇIK İŞLERİ (konsolide)

**Kaynak:** `aktif_ogrenme_secim_tasarimi_S1_S2_dedup.md` + `..._uygulanabilirlik_denetimi_2026-07-18.md`
**Doğrulama:** Aşağıdaki her satır 2026-07-30'da **koddan/config'den bizzat teyit edildi.**
Artık yapılacak işler için **bu bölüm otoriterdir**; o iki dosya gerekçe/bilimsel dayanak arşividir.

## 11.1 Bağımlılık zinciri ve doğrulanmış durum

```
[0] ÖLÇÜM TEMELİ (i.i.d. denetim seti + propagation_precision)
    ✅ KOD VAR, UYKUDA — audit_set_sampler.py + propagation_metrics.py (43 test)
    🔒 KİLİT: (a) AL-C1/C2 contract kararı  (b) AL-P1 portal anti-anchoring  (c) GAP verisi
     │      ⟵ MUTLAK ÖN-KOŞUL: bu olmadan S1/S2/dedup'ın işe yarayıp yaramadığı ÖLÇÜLEMEZ
     ▼
[1] SÜRÜM DAMGASI  ✅ UYGULANDI (2026-07-19, memory + artefakt tarafı)
    Kalan: AL-W8 (legacy None→v1 damgalama) + W8 (kalibrasyon motoru tetikleyicisi, §10.2/Ç-2)
     │
     ▼
[2] S1 ROUTER  ✅ KOD VAR (shadow), OPERASYONEL UYKUDA
    Doğrulandı: `model_registry.yaml` → **8 kaydın 8'inde `router_density: null`**
    🔒 KİLİT: LoRA ağırlıkları (GAP saha verisi)  ⟵ **PİLOT BUNU ÜRETİYOR (§10.3/T-1)**
     │
     ▼
[3] DEDUP  — F1 (saflık) + F4 (nadir/karantina hariç) ✅ UYGULANDI 2026-07-19 (uykuda, 49 test)
    Doğrulandı: `should_send_to_expert(predicted_class, index_signature)` var ama **çağrısız (KİLİT-2)**
    🔒 KİLİT: canlıya bağlama + F7 propagation_precision kapısı ⟵ [0]'a bağımlı
     │
     ▼
[4] S2 BÜTÇE + CLUSTER-MARGIN  ⏸ KOD YOK (kasıtlı — spekülatif kod yazılmadı)
    Doğrulandı: `cluster_margin`/`supcon`/`diversity_select` → src/ içinde **0 eşleşme**
    🔒 KİLİT: ölçülmüş gerçek uzman hızı (B) + [0] + [5] uzayı
     │
     ▼
[5] SupCon TASK-UZAYI (EK-G/F5)  ⏸ KOD YOK (kasıtlı)
    🔒 KİLİT: grade-A/B etiket birikimi (tavuk-yumurta) → en son faz
     │
     ▼
[6] CONTINUAL / SEZON (S4) + sınıf-dengeli replay — lora_reversion_gate'i bağla
```

## 11.2 CONTRACT işleri

| # | İş | Doğrulama | Öncelik |
|---|---|---|---|
| **AL-C1** 🔴 | `expert_review_queue.v1` → `escalation_reason` enum'una **additive 7. değer `AUDIT_SAMPLE`**. Bugün i.i.d. denetim tile'ını taşıyacak bir neden **yok**; mevcut güven-temelli bir neden altında yollamak hem **yansızlığı bozar** hem `escalation_total{reason}` metriğini kirletir. Worker enum'a **tek taraflı ekleyemez** (§2.1 platform-otoriter) | ✅ Kanonik contract **ve** worker vendored kopya: tam **6 değer** (`LOW_CONFIDENCE, LOW_AGREEMENT, OOD_DETECTED, HIGH_EPISTEMIC, EXPERT_RE_TRIGGER, QUARANTINE_CAUTION`) — `AUDIT_SAMPLE` yok | 🔴 [0]'ın ön-koşulu |
| **AL-C2** 🔴 | `expert_review_queue.v1` → **denetim-modu alanları**: `audit_sample: bool` + `audit_stratum: string`. ⚠️ `audit_stratum` platform-otoriter eksende ifade edilmeli (`crop_type` × `analysis_type` × fenoloji-penceresi); eksen karışımı **şema hatasıdır** | Devir spesi §3-B: **bilimsel olarak A'dan üstün**; A+B **birlikte** önerilir (A metrik temizliği, B körlük) | 🔴 [0]'ın ön-koşulu |
| **AL-C3** 🟡 | **(YENİ, 2026-07-31)** `confidence_score`'u denetim satırında da tel üzerinden kaldır — tam anti-anchoring fail-closed. Bu turda YAPILMADI: alan `required` + `type: number`; nullable'a genişletmek `breaking_change_detector`'a göre **MAJOR** (ölçüldü) ve tur MINOR'du. Sınıf etiketleri (predicted_class/detection_type/sub_specialty) **zaten kaldırıldı**. Kalan risk yalnız skaler güvenin uzmana gösterilmesi → **AL-P1 portal yükümlülüğü** ile örtülüyor | Devir spesi §3-B; `x-anti-anchoring.residual_portal_obligation` | 🟡 v2/MAJOR |
| — | ⚠️ AL-C1/C2 **C8 sürüm törenine** dahildir (annotated tag + SHA256 + 3 repo pin). **TUR 1'e dâhildir** (2026-07-31 kararı — eski *"C-Tur-2 ile birleştirilebilir"* ifadesi **yürürlükten kalktı**; Tur 2 demo sonrası olduğu için [0] ölçüm temelini bloke ediyordu). Bkz. §3.1 "TUR TANIMI" | — | — |

**Kaynak devir spesi:** `tarlaanaliz-worker/denetim/audit_escalation_reason_devir_spec_2026_07_19.md`
— worker'ın karar-hazır devri; **platform seçer, worker uydurmaz.**

## 11.3 PLATFORM işleri

| # | İş | Neden | Öncelik |
|---|---|---|---|
| **AL-P1** 🔴 | **Uzman Portalı anti-anchoring:** denetim tile'ında uzmana `predicted_class` / `confidence` **GÖSTERİLMEZ** | Uzman modelin tahminini görürse "bağımsız" etiket modele **demirlenir (anchoring)** → yansızlık ölür → **tüm ölçüm temeli geçersiz olur.** Tek başına AL-C1 bunu çözmez | 🔴 [0]'ın ön-koşulu |
| **AL-P2** 🟠 | `escalation_total{reason}` metriği `AUDIT_SAMPLE` akınını **ayrı** saysın | Denetim akını gerçek eskalasyonla karışırsa "düşük güven akını" gibi görünür — sahte alarm | 🟠 AL-C1 ile birlikte |
| **AL-P3** 🟡 | KR-071 sözleşme testi denetim kanalını da kapsasın (`test_pii_isolation`) | Denetim kanalı PII kapısını **ATLAMAMALI**: yalnız `job_id + tile_coordinates + thumbnail`, **`field_id` YOK** | 🟡 AL-C2 ile |

## 11.4 WORKER işleri

| # | İş | Doğrulanmış durum | Kilit | Öncelik |
|---|---|---|---|---|
| **AL-W1** 🔴 | **Ölçüm temelini canlıya bağla:** `audit_set_sampler` rate tablosunu doldur (bugün boş/0.0 → hiçbir tile seçilmiyor) + uzman-kuyruğu yayıncısına bağla; dönen bağımsız etiketler `propagation_metrics`'i besler | Kod ✅ hazır, **dormant** | AL-C1+C2+P1 · GAP verisi | 🔴 |
| **AL-W2** 🟠 | **S1 router'ı uyandır:** `fit_s1_router_density.py` ile yoğunluk artefaktını fit et → `router_density` + `_sha256`'yı registry'ye yaz (KR-041 kapısı hazır) → `s1_router_ablation.py` ile **false-skip < 0.005** kanıtla → shadow→pilot yükselt | 8/8 kayıtta `router_density: null` | LoRA ağırlıkları ⟵ **pilot** | 🟠 |
| **AL-W3** 🔴 | **KİLİT-2: dedup canlı yolunu bağla** + F7 `propagation_precision(crop)` kapısını devreye al. F1/F4 kapıları **zaten hazır ve doğru yerde bekliyor** | `should_send_to_expert` src/ içinde **çağrısız** (3 eşleşme yorum) | AL-W1 ([0]) | 🔴 |
| **AL-W4** 🟠 | F2/F3 (temsilci seçim + soft-label cascade) + F6 (oto-eşik) | Ertelenmiş, kod yok | AL-W3 | 🟠 |
| **AL-W5** 🟠 | **S2 bütçe + cluster-margin seçici (EK-F):** bütçe (B) kavramı, cluster-margin seçici, crop×katman tahsisi, taşma kuyruğu | `cluster_margin`/`supcon`/`diversity_select` → **0 eşleşme** | B ölçümü + [0] + [5] | 🟠 |
| **AL-W6** 🟡 | **SupCon task-uzayı (EK-G / F5):** morfoloji-yanlı 1024-d uzayı görev-uzayıyla tamamla | Tek "contrastive" kod `ssl_pretrain.py` **BYOL/SimCLR SSL** — SupCon değil | grade-A/B etiket birikimi | 🟡 en son |
| **AL-W7** 🟠 | **EK-D sinyal bağımsızlığı — HÂLÂ AÇIK:** FAISS-cosine ↔ prototype-distance eskalasyonda **çift-sayım** | Denetim §2/EK-D: *"Sinyal-bağımsızlığı redundansı bu kalemde ÇÖZÜLMEDİ — ayrı iş kalemi olarak açık"* | — | 🟠 |
| **AL-W8** 🟡 | **Runbook:** ilk gerçek `encoder_version` artırımından **ÖNCE** legacy `None`-sürüm gömmeleri v1'e damgala (fail-open köprüyü kapat) | Aksi hâlde eski vektörler gerçek bir gömme-uzayı değişiminin ötesine "bedava" biner | — | 🟡 **W8 ile birlikte yapılmalı** |
| **AL-W9** 🟡 | **EK-A'yı 5 → 8 contract mahsulüne genişlet** (duyusal tavan analizi) | Denetim **#4-kritik**; §10.2/Ç-3 ile aynı boşluk | — | 🟡 **W7+ ile birleşik** |
| **AL-W10** 🟡 | **Mahalanobis deployment durumunu doğrula:** `activate_r2_mahalanobis.py` ile açılıyor — canlıda aktif mi, statik proxy'ye mi düşüyor? | Denetim §6-2 açık ucu | — | 🟡 AL-W2 öncesi |

## 11.5 Kilit haritası — neyin neyi beklediği

| Kilit | Ne bloke ediyor | Nasıl açılır |
|---|---|---|
| **KONTRAT kilidi** (AL-C1/C2 + AL-P1) | **[0] ölçüm temeli** → dolayısıyla [3] dedup canlı, [4] S2 | **Platform kararı.** Kod bekliyor, karar bekleniyor. **Tek gerçek "bugün alınabilir" kilit budur** |
| **VERİ kilidi** (GAP saha verisi / LoRA ağırlıkları) | [2] S1 router fit, [4] S2 B-ölçümü, [5] SupCon etiket birikimi | **Pilot** (§2, KG-0.d). Üzüm/fıstık uçuşları → etiket → ağırlık |
| **KİLİT-2** (dedup canlı yolu ölü) | [3] ve uzman yükü azaltımı | AL-W3 — ama önce [0] |
| **Tavuk-yumurta** (SupCon ↔ etiket) | [5] | Döngü çalışıp KR-029 A/B geri bildirimi üretince |

⚠️ **§10.3/T-3 hatırlatması:** **E12** (NDVI önceliklendirme bayrağı) **KİLİT-2 kapalıyken açılmamalı** —
uzman yükünü artırırken azaltıcıyı devre dışı bırakır.
✅ **2026-07-31 çözümü:** bu kural artık **P9a**'ya bağlıdır (pilot kota tavanı, Dalga 2, E12 ile aynı
sürüm). Önceki hâlinde kural yazılıydı ama **hiçbir iş kalemine bağlı değildi** ve tek kota kalemi
(P9) demodan sonraydı → demo gecesi plan kendi kuralını ihlal edecekti.

## 11.6 Bilinçli YAPILMAYACAKLAR (kapsam kayması önleyici)

Bu kalemler **eksik değil, kasıtlı olarak yazılmamış** — veri yokken parametre uydurmak
dürüstlük disiplinini bozar (kaynak dokümanın EK-C ilkesi):

- S2 bütçe ağırlığı / cluster-margin eşiği — **gerçek uzman hızı (B) ölçülmeden** yazılmaz
- SupCon geçiş eşiği (linear-probe acc / silhouette) — **yeterli etiket yokken** kalibre edilemez
- `escalation_reason`'a worker tarafından 7. değer eklemek — **§2.1 ihlali**
- `embedding_dim=1024` (K-4) — **sabit, değiştirilemez**

---

# 12. MOTOR KARARI — DEMO ve 1 AYLIK PİLOT İÇİN AYRI ÖNERİ (2026-07-30, derin tarama)

**Soru:** Metashape / DJI Terra / PIX4Dfields arasında hangisi?
**Yöntem:** Üreticilerin **resmi fiyat + lisans + destek** sayfaları ve **ölçülmüş vaka çalışması**.
**Bağlam değişkeni:** proje **kamu araştırma projesi** → eğitim/araştırma lisansları gündeme geldi.

## 12.1 Üç yeni belirleyici bulgu

### B-1 🔴 DJI Terra **Education sürümü 500 fotoğrafla sınırlı** — gerçek tarla için kullanılamaz

DJI resmi destek dokümanı, sürüm-işlev tablosunda net: Education sürümü için
**"The reconstruction of 500+ photos is not supported."** Bu sınır **yalnız Education
sürümünde** var (Agriculture/Pro/Electricity/Cluster'da yok).

**Neden öldürücü:** Aşağıdaki ölçülmüş vakada **50 hektarlık tek bir tarla 3.635 dosya**
üretti (727 RGB + 2.908 ÇS). 500 fotoğraf sınırı, **tek bir gerçek uçuşun bile** çok altında.
→ **Terra EDU (~€2.976, 10 cihaz, kalıcı) parası boşa gider.** Almayın.

**Buna karşılık Terra Agriculture:** 3 cihaz · 1 yıl · online yetkilendirme ·
**2D Multispectral Reconstruction dahil** · **fotoğraf sınırı YOK** · **$300/yıl.**

### B-2 🟢 Eğitim lisansları çok ucuz — **ama iki farklı uygunluk tanımı var**

| Ürün | Ticari fiyat | **Eğitim fiyatı** | Uygunluk tanımı (resmi) |
|---|---|---|---|
| **Metashape Professional** | $3.499 kalıcı | **$549 kalıcı** (node-locked, rehostable) | *"exclusively to **accredited educational institutions**, their employees and students"* — sayılanlar: üniversite, kolej, **bilimsel ve teknik okullar**, meslek okulları. ⚠️ **"araştırma enstitüsü" listede YOK**; "research staff" ancak *akredite eğitim kurumunun* personeli olarak geçiyor |
| **PIX4Dfields** | $1.990/yıl | **$650/yıl** · **$1.300 / 3 yıl** | *"universities, schools, **research institutes** and the like for educational research and teaching purposes"* — ⚠️ **araştırma enstitüsü AÇIKÇA sayılıyor.** Şart: **tanınmış eğitim alanlı e-posta** |
| DJI Terra EDU | — | ~€2.976 kalıcı (10 cihaz) | okul/üniversite/araştırma merkezi — **ama 500 foto sınırı (B-1)** |

→ **Kurumunuz için PIX4Dfields eğitim lisansı, Metashape'inkinden daha yüksek ihtimalle uygundur.**
Metashape "akredite **eğitim kurumu**" diyor; bakanlık/araştırma enstitüsü bu tanıma girmeyebilir.
**İkisinde de yazılı teyit alın** (Agisoft "written proof of eligibility" isteme hakkını saklı tutuyor).

### B-3 🔴 **Eğitim lisansı = ticari kullanım YASAK** — ve sizin faz planınızda gelir kapısı var

Agisoft EULA: *"the program, executed under educational license, including any materials created
with the help of it **shall not be used for commercial purposes**"* + *"does not allow to provide
access to the software to third parties... **service bureau**, or similar service."*
Pix4D: *"Educational licenses **will not be used for any commercial purposes** and will only be
used for scientific research and/or educational use."*

⚠️ **Tuzak:** Proje bugün kamu araştırması; ama faz planında **gelir kapısı** var. Eğitim lisansıyla
kurulan hattı ileride paraya dönüştürürseniz **lisans ihlaline** düşersiniz — ve bu, o güne kadar
üretilmiş çıktıları da kapsar ("materials created with the help of it").
→ **Eğitim lisansı yalnız gerçekten ticarileşmeyecek iş için.** Gelir kapısı açılacaksa ticari
lisans planlayın; ya da hattı **ODM** üstüne kurun (AGPL, ticari kullanım serbest).

## 12.2 Tek ölçülmüş gerçek veri noktası (Pix4D resmi vaka çalışması)

**PIX4Dfields + DJI Mavic 3M · 50 ha buğday · 90 m irtifa · Almanya, 26 Mart 2024:**

| Ölçüm | Değer |
|---|---|
| Girdi | **727 RGB (6,5 GB)** + **2.908 ÇS (27,6 GB)** = **34,1 GB** |
| Uçuş süresi | 32 dk |
| **İşleme** | **RGB 4 dk 30 sn · ÇS 6 dk 54 sn** |
| Uçtan uca | 51 dk 30 sn |
| GSD | 2,24 cm (RGB) · 3,73 cm (ÇS) |
| Çıktı | tarla sınırı, NDVI, değişken oranlı reçete haritası |

**Bu veri iki şeyi doğruluyor:**
1. **Depolama tahminim tutuyor.** Ölçülen: 34,1 GB / 727 tetik = **46,9 MB/tetik**.
   §2.2'deki üst sınır tahminim **51 MB/tetik** idi → **%9 sapma**. Tablolar güvenilir.
2. **Fields'in "fast" hattı gerçekten hızlı** — 50 ha multispektral **7 dakikanın altında**.

⚠️ Karşılaştırılabilir bir Terra veya Metashape ölçümü **hiçbir resmi kaynakta yayınlanmamış**.
Bu yüzden hız karşılaştırmasını **pilotta kendiniz ölçmelisiniz** (§12.5).

## 12.3 Karar çerçevesi — sizin durumunuzda gerçekten neyi ayırıyor

DJI-only olduğunuz için üç yazılımın **çoğu farkı bugün geçersiz.** Kalan gerçek eksenler:

| Eksen | Terra Agriculture | PIX4Dfields | Metashape Pro | ODM |
|---|---|---|---|---|
| M3M multispektral | ✅ yerli | ✅ (göreli kalib.) | ✅ (göreli) | ✅ v3.5.3+ |
| **Otomasyon (FAZ 8)** | ❌ CLI yok | ❌ CLI yok | ✅ Python API | ✅ CLI/Docker |
| Fotoğraf sınırı | yok | yok | yok (RAM) | yok (RAM) |
| GeoTIFF çıktı (rasterio uyumlu) | ✅ | ✅ | ✅ | ✅ |
| Zonasyon/VRA/ISOXML | reçete haritası | ✅ **tam** | ❌ | ❌ |
| **Yıllık maliyet (kamu araştırma)** | **$300** | $650 (EDU) / $1.990 | $549 (EDU, kalıcı) / $3.499 | **$0** |
| Ticarileşme riski | yok | ⚠️ EDU'da var | ⚠️ EDU'da var | yok (AGPL) |

**Kritik gözlem:** Demo ve pilotta **kırmızı NDVI bölgelerini üreten şey motor değil, sizin
`ndvi_prioritizer.py`'niz.** Motordan tek beklenen: **M3M'i işleyip georeferanslı çok-bantlı
GeoTIFF vermesi.** Dördü de bunu yapıyor. → **Bu aşamada agronomik UX (Fields) ve Python API
(Metashape) için para ödemenin karşılığı yok.**

## 12.4 ÖNERİ — DEMO (maliyet: **0 TL**)

| Rol | Araç | İspat |
|---|---|---|
| **Birincil motor** | **DJI Terra**, M3M ile gelen **Full-Featured 3 ay / 1 cihaz** hediyesi | Kutuyla geliyor; DJI FAQ: ücretsiz lisanslar **unbind edilemez** → RTX 3090'lı masaüstüne aktive edin. Fotoğraf sınırı **yok** (sınır yalnız EDU ve trial'da) |
| **İkinci görüş** | **ODM** (ücretsiz, AGPL) | Aynı veriyi ikinci motorla işleyip demoda **"tek yazılıma bağımlı değiliz"**i kanıtlar |
| **Görselleştirme** | QGIS + Precision Zones (ücretsiz) | Slayt görselleri |
| **Satın alınacak** | **HİÇBİR ŞEY** | — |

**Neden Fields veya Metashape değil:** Demo hikâyesi kalibrasyon → NDVI → **sizin ön rapor
ekranınız**. Fields'in zonasyon/PDF'i sizin platformunuzun ürettiğinin **kopyası** olurdu;
Metashape'in Python API'si demo için gereksiz (Terra'yı elle çalıştırıp klasörü izleyeceksiniz).
⚠️ **PIX4Dfields deneme sürümü çıktı export etmiyor** (Pix4D resmi) — demo için zaten kullanılamaz.

## 12.5 ÖNERİ — 1 AYLIK PİLOT (maliyet: **0 TL**, opsiyonel **$300**)

| Rol | Araç | Gerekçe |
|---|---|---|
| **Birincil motor** | **DJI Terra** (hediye 3 ay kapsıyor; bitince **Agriculture $300/yıl, 3 cihaz**) | 1 ay tamamen hediyenin içinde. Sonrasında $300/yıl, DJI-only bir operasyon için rakipsiz |
| **Otomasyon motoru** | **ODM** (ücretsiz) | FAZ 8'in gerçek headless kanıtı. Terra'nın CLI'si **yok** — otomasyon hikâyesi ODM ile kurulur |
| **Karşılaştırma** | Terra ↔ ODM her uçuşta | §4'teki 4. metrik: **motorlar arası NDVI farkı**. Üretim motoru kararı **bu ölçüme** dayanacak |
| **Satın alınabilir (opsiyonel)** | Terra Agriculture $300/yıl | Hediyeniz 3 ay; pilot 1 ay. **Şimdi gerekmiyor** |

### Pilotun **ölçmesi gereken** dört şey — üretim motoru kararı bunlara bağlı

| # | Ölçüm | Kararı nasıl belirler |
|---|---|---|
| 1 | **ODM M3M bant hizalaması** çalışıyor mu (topluluk kayması sizde de var mı) | ❌ ise otomasyon motoru olarak ODM düşer → **Metashape gerekli hale gelir** ($549 EDU / $3.499) |
| 2 | **Terra-NDVI ↔ ODM-NDVI farkı** (aynı tarla, aynı gün) | Büyükse motor değişimi eğitim verisini geçersiz kılar → tek motora sabitlenme + W8 (`encoder_version` tetikleyicisi) zorunlu |
| 3 | **dk/ha ve tepe RAM** (32 GB masaüstünde) | ODM ~1000 görüntüde 64 GB'da 3,5-5,5 saat; **32 GB'da batch bölmek gerekebilir** |
| 4 | **GB/dönüm gerçek değeri** | Ölçülen referans: 46,9 MB/tetik (Pix4D vakası). Sizinki sapıyorsa depolama planı revize |

### Ne zaman para ödemeye başlarsınız

```
PİLOT SONU
   │
   ├─ ODM M3M'de çalıştı + NDVI farkı kabul edilebilir
   │     → ÜCRETSİZ KAL. Terra $300/yıl (manuel/QC) + ODM (otomasyon). Yıllık ~$300
   │
   ├─ ODM M3M'de çalışmadı
   │     → Metashape gerekli. Kurum akredite eğitim kurumuysa $549 EDU (kalıcı),
   │       değilse $3.499 ticari. ⚠️ gelir kapısı açılacaksa EDU alma
   │
   └─ Zonasyon/VRA/ISOXML'i ÜRÜN olarak satacaksanız
         → PIX4Dfields. EDU $650/yıl (araştırma enstitüsü açıkça uygun),
           ticari $1.990/yıl. ⚠️ CLI yok — insan-döngüsünde kalır
```

## 12.6 Terra çıktılarında DJI logosu / filigran var mı? — **kanıt taraması**

**Kısa cevap: Raster çıktılarda (GeoTIFF ortho/DSM/indeks) filigran veya logo bildiren
hiçbir kaynak yok. Ama DJI'ın "filigran yoktur" diyen açık bir beyanı da yok.**
Aşağıda kanıtın tamamı — doğrudan teyit değil, **güçlü dolaylı kanıt.**

### Filigran OLMADIĞINA işaret eden 5 kanıt

| # | Kanıt | Kaynak |
|---|---|---|
| 1 | **DJI deneme sürümü kısıtlarını tek tek sayıyor** — 500 fotoğraf · LiDAR 8 GB · 1 ay · tek bilgisayar. **Filigran bu listede YOK.** DJI kısıtları açıkça saydığı için, olsaydı burada olurdu | DJI Terra FAQ (resmi) |
| 2 | **Resmi çıktı dokümanı** (dizin yapısı + format listesi: DOM/DSM GeoTIFF, tek-bant stitched, 5 indeks, LAS/LAZ, tiles) **filigran/marka hiç geçmiyor** | DJI "2D Maps & 3D Models Results and Contents" (resmi) |
| 3 | **DJI Kullanım Koşulları çıktı üzerinde marka/atıf ZORUNLULUĞU getirmiyor**; yerel üretilen çıktılar üzerinde DJI mülkiyet iddiası da yok | dji.com/terms |
| 4 | Çıktılar **standart GeoTIFF/LAS/DXF** — QGIS/ArcGIS'te analiz için tüketiliyor. Filigran bu analitik amacı bozardı | DJI + üçüncü taraf dokümanları |
| 5 | Kullanıcı forumlarında/topluluklarda **filigran şikâyeti bulunamadı** (arama yapıldı) | topluluk taraması |

### DJI markası taşıyan tek yer: **kalite raporu**

Terra bir **"Quality Report" PDF** üretiyor (görüntü sayısı, kamera kalibrasyon doğruluğu,
üretim süresi vb.). Bu **DJI'ın kendi ürettiği bir belge** — marka taşıması doğaldır.
⚠️ **Ama demonuz bu raporu göstermiyor.** Demo akışı: Terra GeoTIFF → sizin
`ndvi_prioritizer`'ınız → sizin ÖN RAPOR ekranınız. **Terra'nın raporu hiç görünmüyor.**

### ⚠️ Doğrulanamayan kısım — 10 dakikalık kesin test

DJI'ın "çıktılarda filigran yoktur" diyen **açık bir beyanı yok**; yukarıdaki kanıt
*yokluk kanıtı + dolaylı göstergeler*. Terra 3 ay ücretsiz elinizde olduğu için
**kesin testi kendiniz yapın (ölçüm #6, §2.4):**

1. Küçük bir set işleyin (ör. 60-100 görüntü)
2. Çıkan `.tif`'i **QGIS'te açın**, tam yakınlaştırın, köşeleri ve kenarları kontrol edin
3. `gdalinfo` ile metadata'ya bakın (marka/creator alanı var mı)
4. Kalite raporunu ayrıca açın — orada logo **beklenen** davranıştır, sorun değil

**Yedek garanti:** ODM açık kaynak; çıktısında marka **yapısal olarak yok.** Filigran
çıkarsa demo görselini ODM ortosundan üretirsiniz — zaten ikinci motor olarak koşacak.

## 12.7 Tek cümlelik cevap

**Demo ve 1 aylık pilot için üçünden hiçbirini satın almayın.** Elinizdeki **Terra hediyesi
(3 ay, sınırsız fotoğraf)** + **ODM (ücretsiz, CLI'li)** ikilisi her ikisini de tam karşılıyor
ve üretim motoru kararını **tahminle değil pilotun ölçümüyle** vermenizi sağlıyor.
Terra EDU'yu **almayın** (500 foto sınırı). Eğitim lisanslarını ancak gerçekten
ticarileşmeyecek bir hat için düşünün.

## 12.8 Kaynaklar (§12 için)

- [DJI Terra sürüm-işlev tablosu (resmi)](https://support.dji.com/help/content?customId=01700004862&spaceId=17&re=US&lang=en&documentType=&paperDocType=ARTICLE) — **"The reconstruction of 500+ photos is not supported"** (Education) · Agriculture = 3 cihaz, 2D Multispectral dahil
- [DJI Terra FAQ](https://enterprise.dji.com/dji-terra/faq) — ücretsiz lisanslar unbind edilemez
- [DJI Terra EDU fiyatı (Airclip)](https://www.airclip.de/DJI-Terra-EDU-perpetual-license-10-devices) — €2.975,63 + KDV, 10 cihaz, kalıcı
- [Agisoft eğitim lisansı (resmi)](https://www.agisoft.com/buy/online-store/educational-license/) — **Professional $549**, Standard $59, node-locked rehostable
- [Agisoft Metashape Pro EULA (PDF)](https://www.agisoft.com/pdf/metashape-pro_eula.pdf) — eğitim lisansında ticari kullanım + service bureau yasağı
- [PIX4Dfields eğitim fiyatı (resmi)](https://www.pix4d.com/pricing/pix4dfields-educational/) — **$650/yıl · $1.300/3 yıl**, floating (tek cihaz)
- [Pix4D eğitim çözümleri](https://www.pix4d.com/education) · [Pix4D lisans tipleri (PDF)](https://assets.ctfassets.net/go54bjdzbrgi/4dDSuOgf3K8HpcR8xOc7WK/470587180a30fb041af2aa2c5c45489e/Pix4D_-_Types_of_Licenses.pdf) — *"universities, schools, research institutes and the like"*
- [PIX4Dfields + M3M ölçülmüş vaka (Pix4D resmi blog)](https://www.pix4d.com/blog/input-savings-mavic-3-m) — 50 ha, 727 RGB + 2.908 ÇS, 34,1 GB, RGB 4:30 / ÇS 6:54, GSD 2,24/3,73 cm
- [PIX4Dfields deneme kısıtı](https://support.pix4d.com/hc/en-us/articles/360000831403) — deneme sürümünde **export yok**
- [ODM multispektral (M3M v3.5.3+)](https://docs.opendronemap.org/multispectral/) · [`--radiometric-calibration`](https://docs.opendronemap.org/arguments/radiometric-calibration/)


---

# 13. BİRİKMİŞ İŞLER — EKİM 2026 VE SONRASI

> **Ne zaman bakılır:** FAZ 0 (pilot + demo) kapandıktan sonra. Bu bölümdeki hiçbir kalem
> demo ya da pilot için gerekli DEĞİLDİR — buraya bilinçli olarak ertelendiler.
> **Kural:** bir kalem buradan yukarı (§3 iş tabloları) ancak **yazılı bir karar** ile çıkar.

## 13.1 Ürün kapsamı — yeni mahsul satışa açma

| # | İş | Neden ertelendi | Gerçek maliyeti |
|---|---|---|---|
| **B13-1** | **KİRAZ'ı ticari olarak aç** *(KG-0.d-EK "seçenek B")* | 2026-07-31'de ölçüldü: **kapatılacak risk yok** — CHERRY `GAP_OFFERED_CROPS`'ta değil, tarla bile açılamıyor. Açmak **yeni özellik**, hata düzeltme değil | **Dört yerde birden:** ① platform `GAP_OFFERED_CROPS`'a `CHERRY` ② contract `crop_type.enum.v1`'e `CHERRY` (**MINOR**, + C8 töreni) ③ edge `ndvi_thresholds.yaml` + `phenology_calendar.yaml` ④ fiyat/fenoloji kayıtları. ⚠️ `data_status: limited` → tespit kalitesi zayıf olur; **ÖN RAPOR (indeks) sorunsuz** çalışır |
| **B13-2** | **BUĞDAY'ı ticari olarak aç** | Wire enum'da **var**, edge tablosunda yok; ama `GAP_OFFERED_CROPS`'ta da yok → bugün satılmıyor. Tablo yazmak, satış kararı olmadan **kullanılmayan config** üretir | ① `GAP_OFFERED_CROPS`'a `WHEAT` ② edge iki YAML girdisi (**birkaç saat**) ③ fiyat kaydı. **Veri `strong`** → en ucuz gerçek kazanç, satış kararı verilirse ilk sıradaki |
| **B13-3** | SUNFLOWER / OLIVE tabloları | İkisi de satılmıyor **ve** `stage1: research` → `is_bookable` zaten reddediyor | Düşük; B13-2 ile aynı desen |

> ⚠️ **Dört eksen kuralı (2026-07 denetim kararı, `crop_type.py:50-68`):** bir mahsulü açmak
> **tek yerde** yapılmaz. `GAP_OFFERED_CROPS` (satılan) · VO `_VALID_CODES` (domain-geçerli) ·
> wire `crop_type.enum.v1` (mesaj) · worker-internal (12) **ayrı eksenlerdir**; biri diğerinin
> kopyası değildir. Yalnız birini değiştirmek sessiz kırık üretir.

## 13.2 Tesisat ve yönetişim

| # | İş | Neden ertelendi |
|---|---|---|
| **B13-4** | **C-SSOT-2** — `TARLAANALIZ_SSOT_v1_2_0.txt` senkron aracına **salt-okunur drift dedektörü** olarak eklensin | Kök neden kapatıldı ama tekrarı önleyen otomasyon yok; rsync yolu bu turda test edilemedi |
| **B13-5** | **C11** — `sorties[]` + `mission_date` AK-4 absorpsiyonu (edge vendored'da var, kanonikte yok) | I-5 gereği sapma geçici olmalı; ama demo yoluna girmiyor |
| **B13-6** | **P13** — platform `end_to_end_workflow.md:30` başlık özeti bayat (*"C17 açık"* ↔ C17 satırı *"ÇÖZÜLDÜ"*) | Doküman tutarlılığı; kod etkisi yok |
| **B13-7** | `## # [KR-033]` başlık yazım hatası (SSOT metni) | Bayt-özdeşlik korunsun diye bilerek düzeltilmedi; platform düzeltince aynı turda gelir |
| **B13-8** | **E8** — edge eşik/fenoloji tabloları (WHEAT/SUNFLOWER/OLIVE/CHERRY) | Satılan 5 ürünün **beşinde de** tablo mevcut → bugün acil iş yok; B13-1/B13-2'ye bağlı |

## 13.3 Ölçek ve model hattı *(zaten §11'de izleniyor, buraya yalnız takvim için)*

| # | İş | Tetikleyici |
|---|---|---|
| **B13-9** | **P9b** — gerçek uzman kapasitesi ölçümü + kalıcı kota | Üretim ölçeğine geçiş kapısı |
| **B13-10** | **P7** — TKGM feature flag | Kurumsal protokol gelince |
| **B13-11** | **AL-W4…AL-W10** — S2 bütçe, SupCon, Mahalanobis vb. | [0] ölçüm temeli + pilot verisi |
