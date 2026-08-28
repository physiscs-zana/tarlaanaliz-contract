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

⛔ **DÜZELTİLDİ (2026-08-11 — bu matris koddan SAPMIŞTI, üç üründe.)** Eski hâli tek bir
"kanonik kaynak" (`crop_readiness.json`) ve tek bir `bookable` sütunu gösteriyordu. Ölçüm
bunun yanlış olduğunu gösterdi: **iki ayrı kapı vardır ve `missions.py` İKİSİNİ DE koşar.**

| Kapı | Ne demek | Tek kaynağı | Kapıyı uygulayan |
|---|---|---|---|
| **SUNUM** (`is_gap_offered`) | ana sayfada gösterilir / seçilebilir mi | `tarlaanaliz-platform/web/src/lib/crops.ts` → `OFFERED_CROPS` (üreteç: `scripts/gen_offered_crops.py` → `config/offered_crops.generated.json`; FE+BE testleri pinler) | `fields.py` · `missions.py` · `subscriptions.py` · `change_crop_type.py` |
| **TESLİM** (`is_bookable`) | worker o ürün için model koşabilir mi | `tarlaanaliz-platform/data/crop_readiness.json` (üretildiği yer: `tarlaanaliz-worker/config/crop_readiness.yaml`) | `missions.py` · `subscriptions.py` (**`fields.py` DEĞİL**) |

**Değişmez:** SUNUM ⊆ TESLİM. Bir ürün sunuluyor ama readiness'te `bookable:false` ise
çiftçi ana sayfada görür, tarlasını açabilir, sipariş verince **409** alır — 2026-08-11'e
kadar ÇELTİK'te tam bu oluyordu. Değişmez artık testle kilitli:
`tests/unit/domain/value_objects/test_crop_type.py::test_every_offered_crop_is_bookable_in_readiness`.

⚠️ **`config/*_datasets.yaml` dosyasının varlığı hazırlık göstergesi DEĞİLDİR** — teslim
sinyali `crop_readiness.json`'dır (zeytin buna örnek: `olive_datasets.yaml` var ama `bookable: False`).

| Ürün | stage1 | data_status | SUNUM | TESLİM | Edge NDVI eşiği + fenoloji | Demo uygunluğu |
|---|---|---|---|---|---|---|
| **GRAPE (üzüm/bağ)** | pilot | **strong** | ✅ | ✅ | ✅ | ✅✅ **en iyi — tam** |
| **CORN (mısır)** | pilot | **strong** | ✅ | ✅ | ✅ | ✅✅ **tam** |
| **PISTACHIO (antep fıstığı)** | pilot | **limited** | ✅ | ✅ | ✅ | ✅ **yapılabilir** — tespit kalitesi zayıf olur, ÖN RAPOR sorunsuz |
| COTTON (pamuk) | pilot | critical_gap | ✅ | ✅ | ✅ | ⚠️ koşar ama tespit güvenilmez |
| RICE (çeltik) | research | critical_gap | ❌ **2026-08-11'de kaldırıldı** | ❌ | ✅ | ❌ — sunuluyordu ama TESLİM kapısı 409 veriyordu; kalibre veri gelince ikisi birlikte açılır |
| CHERRY (kiraz) | pilot | limited | ❌ **GAP dışı** | ✅ | ❌ | ❌ — readiness "hazır" diyor ama ürün GAP'ta sunulmuyor; eşik tablosu da yok |
| **WHEAT (buğday)** | pilot | **strong** | ❌ **sunulmuyor** | ✅ | ❌ **eksik** | ⚠️ veri güçlü ama **iki** engel var → aşağıdaki nota bak |
| OLIVE (zeytin) | research | critical_gap | ❌ | ❌ | ❌ | ❌ |
| SUNFLOWER (ayçiçeği) | research | critical_gap | ❌ | ❌ | ❌ | ❌ |

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

**En ucuz kazanç — DÜZELTİLDİ (2026-08-11):** BUĞDAY `data_status: strong` ve TESLİM kapısında
`bookable: True`, ama **iki** engeli var, bir değil:
1. **SUNUM kapısında yok** — `crops.ts::OFFERED_CROPS` buğday içermiyor, yani bugün ana sayfada
   seçilemiyor. (Eski metin *"`bookable: True`"* deyip bunu tek engel sanmıştı; ölçüm iki ayrı
   kapı olduğunu gösterdi — yukarıdaki kapı tablosuna bak.)
2. **Edge eşik/fenoloji tablosunda yok** — iki YAML girdisi (§3-E8).

Yani buğdayı açmak = `crops.ts`'e bir satır (+ üreteci koş) **ve** iki YAML girdisi. Kanonik
wire enum'da WHEAT zaten var, o yüzden contract turu GEREKMEZ. Sıra: önce edge eşikleri
(teslim gerçekten çalışsın), sonra sunum — tersi, satılan ama eşiksiz bir ürün üretir.

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
| **C2″** ⚠️ | **YENİDEN YAZILDI (2026-07-31, D10-E1).** ~~"`priority_zone.py:31,55` regex + `max_length=128` `object_key` için genişletilir"~~ hükmü **YANLIŞTI ve uygulanırsa edge'i kırardı:** edge **göreli yol** üretir, nesne anahtarını **platform** üretir (KG-0.a-EK kural 1) — regex `object_key` için genişletilseydi `ManifestWriter` kendi ürettiği manifesti reddederdi. **Doğru iş:** edge regex'i **DEĞİŞMEZ**; C8'de yapılacak tek şey vendored kopyayı kanonikle yeniden hizalamak (C-VENDOR kalemi kapsar) | — | C2′, **C8** |
| **C3′** | **`schemas/edge/calibrated_dataset_manifest.v1`** → `raw_frames[]` ekle (opsiyonel; yalnız seçilmiş kareler: `{object_key, frame_id, footprint_wkt, band}`). Kare seçimi kalibrasyon çıktısıdır → **edge formu** | MINOR | 0.c, C0 |
| **C4** ⚠️ | **İKİ KEZ DÜZELTİLDİ (2026-07-31).** ~~"contract kalemi değil"~~ hükmü de **eksikti.** Ölçüm: `sorties` **kanonik** contract'ta yok — ama **edge'in vendored interface sözleşmesinde VAR** (`tarlaanaliz-edge/interface/contracts/schemas/edge/intake_manifest.v1.schema.json`), üstelik `mission_date` ile birlikte. Yani bu bir **AK-4 edge-ileri sapmasıdır** (edge kanonikten önce re-pinlemiş), "yok" değil. **Ayrıca planın önermesi de yanlıştı:** *"bbox'ı zorunlu yapmak breaking"* — `bbox` o şemada **ZATEN `required`** (`sorties[].required = [sortie_id, field_id, crop_type, bbox]`). Yani karar verilecek bir şey kalmamış. **Gerçek durum:** `sorties` **dizisi** opsiyonel → hiç sortie yoksa bbox da yok → E9'un mixed-crop yolu. **Yapılacak → C11** | — | → **C11** |
| **C11** ⬜ | **AK-4 absorpsiyonu: `sorties[]` + `mission_date` kanoniğe alınsın.** Edge vendored sözleşmesinde canlı, kanonikte yok → I-5 gereği sapma **yalnız geçici** olabilir. `sorties[]`: `{sortie_id, field_id, field_name, crop_type, area_ha, planned_altitude_m, bbox}`, `required=[sortie_id, field_id, crop_type, bbox]`, dizi **opsiyonel** (geriye uyumlu) · `mission_date`: `["string","null"]`, `format: date`. Eklendiğinde `EdgeForm`'a girer (kaynak edge'dir) | MINOR | C0 |
| ~~**C5**~~ | ~~`analysis_type.enum.v1` → "üretilemez" notu~~ → **YAPILDI (v1.4.1'de mevcut, 2026-07-31 doğrulandı).** `BENEFICIAL → availability: enum_valid_not_yet_emittable` (*"model olgunluğuyla henüz emit edilemez"*) · `THERMAL_STRESS → requires_thermal_payload` (*"**Mavic 3M'de üretilemez**"*). İkisi de **makine-okunur**. Kalan tek delta: `changeNote`'a KG-0.f çapraz atfı → **C0 ile aynı commit** | — | — |
| ✅ **C9** | **YAPILDI (2026-07-31).** KR-093 kanonik registry'ye taşındı (`ssot/kr_registry.md`, 8 bölümlü format, platform normatif metninden; **KG-0.b-R eklentisi işaretli** + AK-4 çapraz-repo notu). `report_phase.enum.v1`'e **`x-preliminary-content`** kapalı listesi eklendi: **Aşama A** (kalibrasyon sonrası — `geom`/`ndvi_value`/`priority_level`/`ndvi_overlay`) · **Aşama B** (worker sonrası — ortho + HEALTH/NITROGEN_STRESS/WATER_STRESS + `overall_health_index`, **özgün tanım değişmedi**) · **`never`** (findings/detections/prescription…). `analysis_preliminary_ready.v1`'in faz-düzeyi *"ONLY"* iddiası **olayın kendi payload'ına daraltıldı**. ⚠️ **Ek bulgu:** contract'ın kendi `docs/TARLAANALIZ_SSOT_v1_2_0.txt` kopyası **KR-084'te bitiyor**, platform kopyası KR-093'e gidiyor — aynı adlı iki SSOT metni **ayrışmış** (hizalama ayrı kalem). **Platform borcu:** iki kopyanın aynalanması | MINOR | ✅ |
| ~~**C9-eski**~~ | ~~**KR-093 içerik tanımını genişlet (2026-07-31 denetimi).**~~ Bugün iki kanonik artefakt PRELIMINARY içeriğini **"YALNIZ/ONLY"** diyerek kapatıyor: `analysis_preliminary_ready.v1` (*"carries **ONLY** deterministic index layers (HEALTH/NITROGEN_STRESS/WATER_STRESS) + overall_health_index"*) ve `report_phase.enum.v1` (*"**Yalnız** deterministik indeks katmanları… sunulur"*). Y-D'nin göstereceği **öncelik bölgesi (poligon + `ndvi_value` + `ndvi_overlay`)** bu listede **YOK** → liste genişletilir. **Ön koşul: KR-093 kaydı `ssot/kr_registry.md`'ye taşınmalı (bugün KR-092'de bitiyor)** | MINOR | 0.b-R |
| ✅ **C10** | **YAPILDI (2026-07-31).** Mapping **kanonik adlarla** yeniden yazıldı ve Y-D anı eklendi: `UPLOADED`/`IN_ANALYSIS`/`PENDING_REVIEW` → `PRELIMINARY` · `DELIVERED` → `FULL` · `EXPERT_REJECTED` → WITHDRAWN(409). **`unlisted_status_behavior: FAIL-CLOSED`** eklendi — *"listelenmeyen = PRELIMINARY"* yasaklandı (aksi hâlde `DRAFT`/`PLANNED` ön rapor üretirdi). **`platform_internal_aliases`** ile platform çevrimi belgelendi. ⚠️ **Denetimde sanılandan büyük çıktı:** kanonik-dışı ad **iki taneydi** — `ANALYZING`(→`IN_ANALYSIS`) **ve `DONE`**(→`DELIVERED`), yani dört girişin ikisi. **Kapı kanıtlandı:** yeni test eski mapping ile düşüyor, yenisiyle geçiyor. **Platform borcu:** `results_service_impl.py:227` catch-all'u kanonik mapping'e daraltılmalı (P12 kabul kriteri) | MINOR | ✅ |
| ~~**C10-eski**~~ | ~~**`report_phase.x-derived-from.mapping`'i kalibrasyon-sonrasına aç.**~~ Bugün tam 4 giriş var (`ANALYZING/PENDING_REVIEW → PRELIMINARY`, `DONE → FULL`, `EXPERT_REJECTED → WITHDRAWN`); Y-D raporu **kalibrasyondan hemen sonra** gösteriliyor ve o an mission `UPLOADED` (`mission.py:84`) → **mapping'de karşılığı yok.** Bunun "çalışıyor" görünmesinin tek sebebi platform kodundaki catch-all `else PRELIMINARY` (`results_service_impl.py:227`) — yani platform **kanonikten geniş**. Ya `UPLOADED → PRELIMINARY` eklenir ya *"listelenmeyen statüler PRELIMINARY (fail-closed)"* yazılır. **Aynı turda:** mapping'deki **kanonik olmayan `ANALYZING`** adı `IN_ANALYSIS`'e çevrilir (`mission_status.enum.v1`'de `ANALYZING` yok; platform-içi ad — çeviri `mission.py:27`'de belgeli) | MINOR | 0.b-R, C9 |
| ✅ **C6** | **KAPANDI — İŞ YOK (2026-08-01, E13 = `ABSOLUTE`).** Koşul gerçekleşmedi: karar `DLS2_RELATIVE` çıkmadı, dolayısıyla alt küme genişletmesi ve MINOR bump **iptal**. Gerekçe §14.7 kalem 6'da; kapı `tests/test_calibration_type_axis.py`. ⬇️ Aşağıdaki eski değerlendirme **tarihsel kayıt** olarak duruyor. **KOŞULLU AÇIK — "kapandı, iş yok" HÜKMÜ GERİ ALINDI (2026-07-31).** Enum kanonik olarak `ABSOLUTE / PANEL_ABSOLUTE / DLS2_RELATIVE / RELATIVE / NONE / AGNOSTIC` içeriyor ve `RELATIVE` = *"Saha-bazlı göreli kalibrasyon (ör. **DJI Mavic 3M çıktısı**)"*. **AMA** `x-context-subsets` ölçüldü: `edge/calibrated_dataset_manifest` alt kümesi **yalnız `["ABSOLUTE","RELATIVE"]`** — `DLS2_RELATIVE` **kabul edilmiyor** (buna karşılık `edge/intake_manifest` alt kümesi onu içeriyor). → **E13 kararı `DLS2_RELATIVE` çıkarsa contract değişikliği ZORUNLU** (alt küme + şema enum'u genişletilir; **MINOR, breaking değil**). `RELATIVE` çıkarsa iş yok. **Sıra düzeltmesi: E13 kararı C6'dan ÖNCE gelir** (planda ters yazılmıştı) | koşullu MINOR | **E13 kararı** |
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
| **E13** ✅→⬜ | **KARAR VERİLDİ (2026-08-01): yazılacak değer `ABSOLUTE`** (gerekçe §14.7 kalem 6 · kapı `contract/tests/test_calibration_type_axis.py`). ⇒ **C6 iş yok.** ⬜ **Kalan iş edge'de, UYGULAMA:** `calibrated_validator` bugün `calibration_type`'ı yalnız **varlık** olarak doğruluyor (`calibrated_validator.py:120` required-field listesi), **değer üretmiyor** — ölçüldü: `pix4d_runner.py` ortho/NDVI/NDRE/NDWI üretiyor, kalibrasyon tipi yazmıyor. Yazılacak: `tool_name`=Pix4Dfields + `tool_version` + `calibration_type="ABSOLUTE"`. ⚠️ Panel kanıtı yoksa değer **uydurulmaz** — enum `x-normalization.missing` **FAIL-CLOSED** diyor: tip bildirilmemişse hiçbir bağlamda varsayılmaz. ⬇️ Eski tanım: `calibrated_validator` → manifeste **motor adı** + **`calibration_result.calibration_type`** yazsın. **Alan adı düzeltmesi (2026-07-31):** planda geçen `calibration_tier` contract'ta **yok**; kanonik ad `calibration_result.calibration_type`. **Karar E13'te verilir ve C6'yı tetikler:** `RELATIVE` → contract işi yok · `DLS2_RELATIVE` (M3M'de dahili ışık sensörü var) → **C6 zorunlu**, çünkü `edge/calibrated_dataset_manifest` alt kümesi bugün yalnız `["ABSOLUTE","RELATIVE"]` | `src/core/services/calibration_gate/calibrated_validator.py` | C1′ · **C6'dan ÖNCE** |
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

## 3.6 DEMO GÖRÜNTÜLEME HATTI — kuyruk (`DK`) — 🆕 2026-08-05 dört-disiplinli denetimden

> **Nereden geldi:** 2026-08-05'te çiftçi sonuç akışı ilk kez uçtan uca çalıştırıldı
> (DJI Terra çıktısı → COG → MinIO → tile ucu → çiftçi haritası) ve tur **dört bağımsız
> denetçiye** (Kıdemli SWE · QA · Pentest · SDLC) verildi. Demo-öncesi 6 kritik aynı turda
> kapatıldı (platform PR **#381**, `f761c317`, CI 18/18). Aşağıdakiler **bilerek ertelendi**.
>
> 🔴 **Kod ailesi neden `DK`:** `D-1…D-16` ve `W1…W15` bu planda **zaten dolu**
> (ölçüldü 2026-08-05). Kalemler yerel `SONRAKI_OTURUM_PLANI.txt`'de `D-1…D-13` diye
> yazılmıştı; **kanonik kod burada `DK-`'dır**, o yerel dosya git ile taşınmaz.

| # | İş | Depo / dosya | Ne zaman |
|---|---|---|---|
| **DK-1** 🟠 | **Worker'a GNDVI hizalaması.** Platform `HEALTH`'i `("gndvi","ndvi")` tercih sırasıyla besliyor; worker gndvi COG'unu **hiç üretmiyor** (`_MAPS_BY_RESULT_MODE`'da hiçbir modda yok, `gndvi_url` ataması 0). Demo yolunda manifest **elle** yazıldığı için GNDVI **canlı çalışıyor** — ayrışma yalnız üretim worker yolunda. Kayıt: `open_items_decisions_2026-06.md` **COORDINATE**. Yapılacak: (a) `reporting_agent._MAPS_BY_RESULT_MODE` (b) `map_renderer.RAMP_REGISTRY` renk rampası (c) `IndexMaps.gndvi_url`. **Ardından** platformda tercih sırası **davranış** testi | worker: `reporting_agent.py` · `map_renderer.py` → sonra platform `tile_service_impl.py` | 🔴 **Ekim 2026 sonrası** (kullanıcı kararı) |
| **DK-2** 🔴 | **`list_summaries` sessiz sonuç kaybı.** SQL `LIMIT` **satır** üzerine (`limit*3`); tekilleştirme + ödeme elemesi o kırpılmış pencerenin İÇİNDE yapılıyor. İki bağımsız kayıp yolu ölçüldü: (a) görev başına >3 sonuç → 60 görev/4 sonuçta 50 yerine **38** (b) düşük ödeme yoğunluğu → 200 görev/1-5 ödenmişte 40 yerine **30**. Çözüm: tekilleştirmeyi SQL'e taşı (`DISTINCT ON`/`row_number()=1`), `LIMIT`'i **görev** üzerine uygula, keyset sayfalama. ⚠️ Düzeltmeyle **aynı turda** (a) ve (b) testleri gelmeli | platform `results_service_impl.py` | demo sonrası ilk sprint |
| **DK-3** 🟠 | **`sameOriginContract` sunucu-taban bloğu METİN araması.** M-F13 (sessiz varsayılan `?? 'http://backend:8000'`) ve M-F22 (dış alan string birleştirmeyle gizlenir) 325 testlik suite'ten **yeşil geçiyor**. Çözüm: `resolveRequestBase`'i **üretim yolundan** çağır (`@jest-environment node`) — env silinmişken `rejects.toThrow`, env varken fetch'in aldığı URL **literal** doğrulansın. Metin taraması yalnız ikincil lint kalsın | platform `web/src/lib/__tests__/sameOriginContract.test.ts` | demo sonrası ilk sprint |
| **DK-4** 🟠 | **N+1 sorgu + sıralı S3.** 50 sonuç → **101 DB sorgusu + 50 SIRALI S3 GET** (ölçüldü). Çözüm: `dataset.result_uri`'leri tek `IN(...)` ile çek · boto3 client'ı örnek düzeyinde tembel-önbellekle (emsal: worker `S3ResultArtifactSink._get_client`) · manifest okumalarını `asyncio.gather` ile sınırlı eşzamanlılıkta koştur · `limit`'i query parametresi yap | platform `results_service_impl.py` | demo sonrası |
| **DK-5** 🟠 | **`get_tile` manifest'i aday başına yeniden çözüyor** — tile başına 4 DB + 2 S3 (gndvi yoksa). Manifest **bir kez** çözülüp adaylar bellekteki `maps` sözlüğünden seçilmeli | platform `tile_service_impl.py` | demo sonrası |
| **DK-6** 🟠 | **`assert_called_once()` argümansız** — `test_get_tile_success_renders_png:124` argümanları denetlemiyor; rescale tablosunun kullanıldığı ve fallback döngüsünün çalıştığı **ölçülmüyor**. Tek satır: `assert_called_once_with(..., "rdylgn", (0.0, 0.8))` | platform testleri | demo sonrası |
| **DK-7** 🟠 | **Yutulan `except Exception` + `exc_info` eksikliği.** `tile_service_impl` 363/437/462 · `results_service_impl` 497. Bu turun teşhisi *"except'ler hatayı yuttu"* idi; **yutucu aynen duruyor**. En az `type(err).__name__ + str(err)` loglanmalı | platform | demo sonrası |
| **DK-8** 🟠 | **`layer_refs` mükerrer kolonu.** Göç sonrası tabloda kalıyor ama ORM ne yazıyor ne okuyor → ölü ikinci kaynak, `available_layers` ile sessizce ayrışır. Çözüm: `COMMENT ON COLUMN` ile **DEPRECATED** işaretle; **düşürme AYRI göç** (geri dönüşü zor — onay gerekir) | platform `alembic/` | demo sonrası |
| **DK-9** 🟠 | **SSR için `X-Forwarded-For` iletimi.** `INTERNAL_API_ORIGIN` üretime taşındı (2026-08-05) → SSR artık nginx'i atlayıp backend'e **doğrudan** gidiyor; istemci IP'si iletilmediği için tüm SSR istekleri **tek hız-sınırı kovasında** toplanıyor (tek kullanıcı diğerlerini 429'a düşürebilir). Demo tek kullanıcılı olduğu için ertelendi | platform `web` + `nginx` | üretim öncesi **kapı** |
| **DK-10** 🟠 | **`contracts` deposunda `.gitattributes`.** Bugün bu makinede disk=blob **bayt-özdeş** (ölçüldü: CRLF=0, LF=348) ve KR-042 kapısı 96/96 geçiyor. AMA taze bir klonda sistem `core.autocrlf` devreye girip CRLF üretebilir → kapı orada patlar. Kalıcı çözüm **contract deposunda**: `* text=auto eol=lf` | **contract** (bu depo) | ikinci makine kurulumundan **önce** |
| **DK-11** 🟠 | **Süreç kapıları kendi kuralını denetlemiyor.** (a) BOUND kapısı yalnız `src/` tarıyor, `alembic/` görmüyor → 2 migration hâlâ BOUND'suz (`2026_07_27`, `2026_07_29`) (b) `CLAUDE.md` pytest komutu CI ile hizalı **değil**: ortam değişkenleri eksik → `exit 2` (13 collection hatası); CI'da `TARLA_ENVIRONMENT=development APP_ENV=development` var (c) `audit_v322_tree.py` kapı değil, drift yalnız raporlanıyor ve yalnız **izlenen** dosyaları tarıyor → yeni dosya hakkında sıfır sinyal (d) I-3 doğrulama komutu **kör**: `git submodule status` alt-modül çalışma ağacı kirliliğini göremez → `git -C contracts diff --quiet` eklenmeli | platform `CLAUDE.md` · `ci.yml` · kök `CLAUDE.md` §3 | demo sonrası |
| **DK-12** ⬜ | **Ölü kod temizliği (ONAY GEREKİR).** `web/src/components/features/map/MapLayerViewer.tsx` — 60 satır, **0 import**. Mükerrer **DEĞİL** (farklı arayüz, kanonik ağaçta ikisi de onaylı, aynı commit `b565a78a` 2026-02-08). Silmek geri dönüşü zor işlem | platform `web` | onay sonrası |
| **DK-13** ⬜ | **Yeni `CLAUDE.md` test kuralı önerisi (#12):** *"Faz/rol kapılı bir DTO'ya yeni alan eklerken fixture değeri, alanın GERÇEK üreticisinin çıktı biçimini taşır; nötr yer tutucu kullanılmaz ve kapının her dalında o alana ayrı bir iddia yazılır."* Gerekçe: 2026-08-05'te `summary` sızıntısı **tam da bu boşluktan** geçti | platform `CLAUDE.md` | demo sonrası |
| **DK-14** 🟠 | **Migration birim testi.** Son iki migration'ın **ikisi de** kendi testiyle gelmişti; bu üçüncüsü gelmedi. Emsal: `tests/unit/test_payment_intent_target_unique_migration.py`. (CI zaten upgrade→downgrade→upgrade zincirini koşuyor) | platform `tests/unit/` | demo sonrası |

> 🟢 **DK-1 BAĞLAMI DEĞİŞTİ (2026-08-05 akşamı, üçüncü tur):** worker artık **ayakta ve GPU
> çalışıyor** (`tarlaanaliz-worker:gpu`, RTX 3090 Ti, `analysis_jobs` kuyruğunu tüketiyor).
> Yani DK-1'in "worker devre dışı, demoyu iyileştirmiyor" gerekçesi **artık geçerli değil**;
> kalemi bloke eden şey yalnızca ekim-sonrası önceliklendirme kararıdır. Aynı turda worker'a
> **tarla geneli NDVI ölçümü** eklendi (`health_distribution.py` → `metrics.health_distribution`
> + `custom_metrics.mean_ndvi`) ve platform `overall_health_index`'i o kaynaktan türetiyor
> (worker PR #197 · platform PR #387). GNDVI **raster üretimi** hâlâ eksik — DK-1 duruyor.
>
> 🆕 **DK-15 (yeni, 2026-08-05):** worker uçtan uca **çıkarım denenmedi**. Konteyner kuyruğu
> tüketiyor ama gerçek bir `analysis_job` mesajıyla akış koşturulmadı. Ayrıca antep fıstığı
> için eğitim veri seti yok (`crop_readiness: pistachio → limited`) — model koşsa bile tespit
> güvenilirliği demo için yeterli olmayabilir. NDVI **ölçümü** veri setinden bağımsızdır.
>
> > 🟡 **DK-15 YARI KAPANDI (2026-08-05 akşamı).** Worker **ilk kez gerçek bir iş mesajı
> > işledi** (`job_id=568d8786-c4e7-4c88-97a8-44f26f8af8db`): gerçek DJI/Terra ortomozaiğinden
> > yığılmış 4-bantlı COG (G/R/RE/NIR, 8558×7638, 618 MB) MinIO'ya yüklendi ve iş kuyruğa
> > basıldı. Ölçülen zincir: mesaj tüketildi → şema doğrulandı → **KR-018 kapısı çalıştı**
> > (`"KR-018: Calibration NONE — job rejected"`) → `analysis_results`'a **REJECTED** gövdesi
> > yayınlandı → `expert_review_queue`'ya eskalasyon yayınlandı → platform köprüsü ikisini de
> > aldı (`WORKER_BRIDGE.RESULT_RECEIVED status=REJECTED`, `ANALYSIS_FAILED`).
> > **AÇIK KALAN:** çıkarım (inference) hâlâ koşmadı — girdi ham DN olduğu için kapı
> > (doğru biçimde) reddetti. Bkz. **DK-21** (Terra radyometrik düzeltme).
> > ⚠️ Platform tarafında `analysis_results` **satırı yazılmadı**: doğrudan kuyruğa basılan
> > iş için `analysis_jobs` satırı yoktu → FK ihlali. Bu **koşum düzeneğinin** eksiği,
> > üretim yolunun değil (üretimde satırı platform kendi açar). Demo satırının üzerine
> > yazmamak için DB'ye elle kayıt **açılmadı**.
>
> ✅ **DK-17 KAPANDI (2026-08-05 akşamı — bağımsız denetim + kalıcı çözüm).**
> İddia **doğrulandı ve KAPSAMI GENİŞLEDİ.** Ölçüm: `git grep s3_endpoint` `src/` içinde
> yalnız `src/shared/config.py:81`'i buluyordu; üç `boto3.client("s3")` çağrısı
> (`result_artifact_sink.py` · `s3_export_sink.py` · `adapter_registry.py`) `endpoint_url`
> **geçmiyordu**. 🔴 **Denetimde çıkan ikinci yol — ilk kalemde YOKTU:** GDAL/rasterio
> `s3://` **OKUMA** yolu da endpoint'siz kalıyordu ve GDAL 3.12.1 `AWS_ENDPOINT_URL`
> değişkenini **okumuyor** → istek **gerçek AWS'ye** çıkıyordu. Ölçüm imzası: MinIO
> *"The Access Key Id ..."*, AWS *"The **AWS** Access Key Id ..."* der; endpoint'siz
> koşuda dönen mesaj **AWS'ninkiydi** (yani yerel kimlikle imzalanmış bir istek internete
> gidiyordu). **Çözüm:** eşleme tek kaynağa alındı — `src/shared/s3_endpoint.py`; boto3
> `endpoint_url` + path-style adresleme alır, GDAL `AWS_S3_ENDPOINT` + `AWS_HTTPS` +
> `AWS_VIRTUAL_HOSTING` alır; ortam değişkeni adı `WorkerConfig`'ten **türetilir**
> (elle yazılmaz). Üretim yolundan doğrulandı (konteyner içinde, `AWS_S3_ENDPOINT`
> ortamda **YOKken**): okuma `8558x7638 EPSG:4326` döndü, yazma MinIO'ya gerçekten
> düştü. 14 test + **5 mutasyon** (hepsi öldürdü).
>
> ✅ **DK-18 KAPANDI (2026-08-05 akşamı).** İddia doğrulandı: `boto3` hiçbir lock'ta
> yoktu ve konteynerde `import boto3` → `ModuleNotFoundError`. **Kök sorun tek bir ürün
> kararının İKİ kapıya bağlanmasıydı** — çalışma-zamanı bayrağı *ve* görünmez bir imaj
> içeriği önkoşulu. **Çözüm:** `requirements-s3.in` + `requirements-s3.lock`
> (`pip-compile --generate-hashes`, 7 paket tam geçişli) + `Dockerfile.gpu`'da **ayrı
> katmanda** `--require-hashes` kurulum (torch katmanının build cache'i korunsun diye).
> Artık bayrak **tek kapıdır**; compose'ta `TARLAANALIZ_ENABLE_RESULT_ARTIFACT_UPLOAD`
> açıldı. İmaj 13.7 → **13.8 GB**. Drift kilidi: `tests/unit/test_s3_lock_matches_pyproject.py`
> (kopyalanan lock kümesi == hash-kurulan küme) + **4 mutasyon** (hepsi öldürdü).
>
> 🆕 **DK-19 (yeni, 2026-08-05 — İLK GERÇEK İŞ MESAJININ ORTAYA ÇIKARDIĞI) — ✅ KAPANDI.**
> `asdict(EscalationRequest)` set edilmemiş alanları **açık `null`** olarak yazıyordu;
> `expert_review_queue.v1`'de `audit_bucket`/`audit_rotation_key`/`audit_selection_rate`
> **opsiyoneldir ama tipleri `integer`/`string`/`number`'dır** — JSON Schema'da "opsiyonel"
> = "olmayabilir", "null olabilir" **değil**. Sonuç: iş denetim örneğine seçilmediğinde
> (yaygın durum) worker **kendi vendored şemasını ihlal eden** bir mesaj yayınlıyordu.
> Şema `additionalProperties: false` taşıdığı için platform aynası kapıyı sıktığı anda
> uzman o tile'ı **hiç görmezdi**. Birim testler göremedi çünkü fixture'lar alanları
> **dolu** veriyordu — **DK-13'ün tarif ettiği boşluğun ta kendisi**. Çözüm:
> `omit_nulls_schema_disallows()` — hangi alanın düşeceği **şemadan türetilir**, elle
> liste tutulmaz. 10 test + 5 mutasyon; ilk turda **M13 hayatta kaldı** (worker'daki
> tesisat test edilmiyordu) → üretim-yolu testi eklenip öldürüldü.
>
> ✅ **DK-20 KAPANDI (2026-08-05 akşamı).** `jsonschema>=4.20,<5` + `referencing>=0.30,<1`
> `dev` grubundan **ana `[project].dependencies`'e taşındı**, `requirements.lock` yeniden
> üretildi (`uv pip compile --universal --generate-hashes`; +4 paket: jsonschema ·
> jsonschema-specifications · referencing · rpds-py — **0 paket düştü**), backend imajı
> kuruldu. Üretim yolundan **iki yönlü** doğrulandı:
> ```
> gecerli mesaj : SCHEMA_VALIDATE_BROKEN 0 · SCHEMA_VALIDATE_SKIPPED 0   (kapi kostu)
> POZITIF KONTROL — kasten bozuk mesaj (confidence_score: "bu-bir-sayi-degil"):
>   WORKER_BRIDGE.SCHEMA_INVALID ... "'bu-bir-sayi-degil' is not of type 'number'"
>   WORKER_BRIDGE.RESULT_ERROR ... ValueError: KR-081 contract validation failed -> DLX
>   analysis_results tablosu: 1 satir (yalniz demo) — bozuk mesaj DB'ye DEGMEDI
> ```
> **Düzeltmeden önce aynı mesaj** `SCHEMA_VALIDATE_BROKEN` yazıp **işlenmeye devam
> ederdi.** Kapı `worker_result_schema_enforce=True` ile fail-closed çalışıyor.
> Kilit: `tests/unit/test_requirements_lock_consistency.py` (pyproject runtime ⊆ lock).
>
> <details><summary>Özgün kalem metni (kayıt için)</summary></details>
>
> 🔴 **DK-20 (yeni, 2026-08-05 — AYNI KOŞUDA ÖLÇÜLDÜ) — AÇIK, YÜKSEK ÖNCELİK.**
> **Platform üretim imajında `jsonschema` KURULU DEĞİL** → KR-081 sözleşme kapısı
> worker'dan gelen **her mesaj için fail-open**. Platform kendi logunda söylüyor:
> `WORKER_BRIDGE.SCHEMA_VALIDATE_BROKEN ... KR-081 kapısı bu mesaj için ETKİSİZ`
> (iki kuyrukta da: `analysis_results` ve `expert_review_queue`). Ölçüm:
> `docker exec tarlaanaliz-backend python -c "import jsonschema"` → yok ·
> `pyproject.toml:110` `jsonschema>=4.20,<5` **yalnız `[project.optional-dependencies].dev`
> grubunda** · `requirements.lock`'ta **hiç yok** · üretim kodu onu çalışma-zamanında
> import ediyor (`src/application/services/contract_validator_service.py:82`, ImportError
> dalı `# pragma: no cover`). **DK-18'in platform tarafındaki ikizi:** çalışma-zamanı
> bağımlılığı test grubunda beyan edilmiş. Çözüm: `jsonschema` + `referencing` ana
> bağımlılıklara taşınsın, `requirements.lock` yeniden üretilsin, imaj kurulsun.
>
> 🔴 **DK-21 (yeni, 2026-08-05) — ÖN RAPOR'U BLOKE EDER.** Elimizdeki tek işlenmiş Terra
> çıktısı **radyometrik düzeltme KAPALI** koşuldu — ölçüldü (Terra iş kaydı
> `records/94280574-*.json`): `use_reflectance_calibration=False` ·
> `use_sun_sensor_per_image=False` · `radiometricCorrectionSet=False`. Yani çıktı **ham
> DN**'dir; kanonik KR-018/082: *"Worker ham DN veya kalibrasyonu belirsiz veriyi kabul
> etmez."* Dürüst bir işte `calibration_type: NONE` yazılır ve iş **reddedilir**
> (koşuldu — DK-15'e bakınız).
>
> > ⛔ **2026-08-06 DÜZELTMESİ.** Bu kalem önce *"aynı 670 fotoğrafla Terra'yı Radiometric
> > Correction AÇIK yeniden koş, güneş sensörü yeter, panel şart değil (~10-15 dk)"* diyordu.
> > **YANLIŞTI.** Terra 5.3.0'ın "Radiometric Correction" ekranı (kullanıcının ekran
> > görüntüsüyle ölçüldü) yalnızca **kalibrasyon paneli** içindir: *Camera Reflectance
> > Factor* · 3 × *Calibration Board* sekmesi · 5 bant yansıma kutusu · *Import Calibration
> > Photo*. Ekranda **"Sun sensor" seçeneği YOK**. 29-07 uçuşunda panel fotoğrafı
> > çekilmediği için bu yol **geriye dönük tamamlanamaz** — panel sonradan eklenemez.
> >
> > **Ama güneş sensörü verisi ELİMİZDE** (ham karelerin XMP'sinde ölçüldü): aynı karede
> > `Irradiance` G 16077.6 · R 13096.1 · RE 10038.8 · NIR 9741.7 (+ `SensorGain`,
> > `ExposureTime`, `BlackLevel=3200`, `VignettingData`); uçuş boyunca %1.5 değişiyor.
> > Bantlar arası **%65** irradyans farkı, ham DN'de bant oranlarını sistematik kaydıran
> > şeyin ta kendisi.
> >
> > **Üç gerçek seçenek** (ayrıntı: `docs/TERRA_RADYOMETRIK_YENIDEN_KOSUM.md`):
> > **A)** Terra + panel → **yeni uçuş** gerekir · **B)** ⭐ **Pix4Dfields ile aynı
> > fotoğrafları işle** → uçuş gerekmez; `TARLAANALIZ_SSOT_v1_2_0.txt:79` Pix4Dfields'in
> > M3M için **panelsiz göreli kalibrasyon** ürettiğini yazıyor (bu makinede kurulu değil,
> > ölçüldü) · **C)** Terra'da güneş-sensörü anahtarı gerçekten yok mu — 1 dakikalık
> > kontrol (`use_sun_sensor_per_image` parametresi Terra'nın iş kaydında **var**).
> >
> > 🔴 **Motor seçimine etkisi:** KR-034 motorları agnostik sayar ama **eşdeğer değiller** —
> > aynı panelsiz uçuşta Pix4Dfields kurtarabiliyor, Terra kurtaramıyor. Bu, **Ç-2 / W8**
> > (motor değişimi `encoder_version` tetikleyicisi olsun) kalemini güçlendirir.
>
> 🟠 **DK-22 (yeni, 2026-08-05) — GİZLİ RİSK, bugün canlı DEĞİL.** `health_distribution.py`
> geçerli-piksel filtresi olarak **yalnız `np.isfinite`** kullanıyor; bir raster'ın
> **beyan edilmiş `nodata`** değerini dikkate almıyor. Terra'nın `index_map/NDVI.tif`'i
> `nodata=0.0` (sonlu bir nöbetçi değer) taşıyor → o pikseller "NDVI=0 ölçümü" sayılıyor.
> Büyüklük ölçüldü: aynı raster için `mean_ndvi` **0.1525** (isfinite) ↔ **0.264**
> (nodata-duyarlı) = **%42 hata**; dağılımda `critical` %64.6 ↔ %38.8. Bugün canlı
> DEĞİL çünkü üretim çağrısı raster değil **süreç-içi hesaplanmış** diziyi besliyor
> (`reporting_agent._compute_field_metrics` → `message.index_maps_raw["ndvi"]`, NaN-güvenli).
> AMA fonksiyonun kendi docstring'i girdi olarak *"ortomozaik"* diyor — davet açık.
>
> ✅ **DK-24 (yeni, 2026-08-06) — AÇILDI ve AYNI TURDA KAPANDI: göreli (yüzdelik) katman.**
> **Karar:** mutlak eşik iddiası yerine **sıralama** iddiası — yalnız demo için değil
> **genel yaklaşım** olarak (kullanıcı kararı, 2026-08-06).
>
> **Gerekçe ölçüldü** (Dicle Ü. 29-07 uçuşu, 3.000.000 piksel): bant kazancı değiştiğinde
> mutlak sayılar oynuyor ama sıralama **hiç** bozulmuyor —
> ```
> kazanç NIR/R   mean_ndvi   "zayıf" %      Spearman sıra korelasyonu
> 1.00 / 1.00      0.264       85.0                1.000000
> 1.35 / 1.00      0.394       61.8                1.000000   <- eksik düzeltme ~BU
> 1.00 / 1.35      0.124       91.7                1.000000
> 0.60 / 1.90     -0.280       99.2                1.000000
> ```
> Matematiksel sebebi var: NDVI, NIR/R oranının **monoton** fonksiyonudur; bant kazancı o
> oranı yalnız ölçekler. Yani *"tarlanın hangi bölgesi daha kötü"* **ham DN'de bile TAM
> doğrudur** — ÖN RAPOR kararının (KG-0.b-R / Y-D) istediği tam olarak budur.
>
> | Katman | Ne yapıldı |
> |---|---|
> | worker | `compute_relative_distribution()` — %5/20/50/80/95 kesim noktaları. **Kalibrasyon kapısına TABİ DEĞİL** (bilinçli); istatistik kapısı (min geçerli piksel) korunur |
> | worker | `_compute_field_metrics` yeniden kuruldu: eskiden `dagilim is None` **metrics'in TAMAMINI** düşürüyordu → kalibre olmayan işte geçerli ölçüm de kayboluyordu. Artık mutlak kısım fail-closed kalır, göreli kısım yayınlanır |
> | worker | Yük **daima** iki bayrak taşır: `ordering_calibration_invariant: true` · `values_calibration_dependent: true` (KR-025: worker yorumlamaz, geçerlilik bağlamını bildirir) |
> | platform | `_percentile_rescale()` — renk ölçeği artık **COG'un kendi %2–%98 dilimlerinden**; `_INDEX_RESCALE` yalnız geri düşüş. Veri seti başına bir kez hesaplanıp önbelleğe alınır |
>
> 🔴 **Neden sabit tablo yanlıştı:** `_INDEX_RESCALE` değerleri **tek bir uçuşun** (Dicle Ü.)
> %5–%95 dilimlerinden elle alınmış ve global sabit gibi yazılmıştı. Başka tarlada harita
> soluklaşır/doyar; kalibre olmayan girdide ise sabit aralık **mutlak bir iddiadır**.
>
> **Sözleşme değişmedi** — `Metrics.custom_metrics` zaten `additionalProperties: true`
> ("Analysis-specific custom metrics"). Sürüm yükseltmesi / yeniden pinleme **gerekmedi**.
> Testler: worker 14 + platform 11 = **25 test**, **13 mutasyon** (biri ilk turda hayatta
> kaldı → test ayrıştırıcı hâle getirildi). Platform coverage %83.54, mypy 461 dosya temiz.
>
> 📄 **İndeks sayısı ve radyometri araştırması** (2026-08-06, kaynaklı):
> `docs/M3M_INDEKS_VE_RADYOMETRI_ARASTIRMASI.md` — 4 bantla **58 vejetasyon indeksi**
> (hesaplandı, alıntılanmadı) · M3M kırmızı kenarı **RE2 (730nm)**, literatürdeki NDRE ise
> **RE1 (705nm)** için tanımlı → Terra'nın NDRE'si bir **ikame** · DJI'ın kendi kılavuzu
> **panelsiz** yolu tarif ediyor · üçüncü motor **ODM** ($0, `camera+sun`).
>
> ✅ **DK-21 KAPANDI (2026-08-06) — ODM ile kalibrasyon KOŞTU.**
> `opendronemap/odm` (0.63 GB) çekildi, 670 fotoğraf `--radiometric-calibration camera+sun`
> ile işlendi ve **14 dakikada** bitti (RTX 3090 Ti makinesi, GPU gerekmedi). ODM kendi
> `log.json`'ında `"radiometric_calibration": "camera+sun"` yazıyor. Çıktı:
> **5 bantlı float32 ortofoto** (`Red, Green, NIR, RedEdge` + alpha), değerler **0–0.20**
> — yani **reflektans** (Terra'nın ham DN'i 36–4044'tü). Panel gerekmedi, ücret ödenmedi.
>
> 🔴 **ÖNGÖRÜM YANLIŞ ÇIKTI — kayda geçiriyorum.** 2026-08-06 sabahı, tek karede ölçülen
> R/NIR irradyans oranından (1.3443) yola çıkıp *"kalibrasyon uygulanınca '%85 zayıf'
> ~%62'ye iner"* demiştim. Ölçüm bunu **çürüttü**:
> ```
> Terra (ham DN, kalibresiz) : mean_ndvi 0.264   · critical+poor %85.0
> ODM  (camera+sun, RELATIVE): mean_ndvi 0.2657  · critical+poor %87.8
> ```
> Fark **%0.6**. Tek-kare irradyans oranından tarla geneline yapılan çıkarım tutmadı —
> muhtemelen Terra'nın zaten uyguladığı kazanç/pozlama normalizasyonu farkın çoğunu
> soğuruyor. **Ders:** bu büyüklük hesapla kestirilemiyor, koşturmak gerekiyordu.
> ⚠️ Bu bir **toplam** (motor + kalibrasyon) ve **toplu** karşılaştırmadır; iki raster
> farklı ızgarada ve farklı geçerlilik maskesinde (Terra %50.7 ↔ ODM %57.0). Piksel-piksel
> sıra korelasyonu **hâlâ ölçülmedi** (ortak ızgaraya getirme gerekir).
>
> 🟡 **DK-15 İLERLEDİ, KAPANMADI — çıkarım İLK KEZ koştu.** Kalibre COG (`G,R,RE,NIR`,
> reflektans, NaN maskeli) MinIO'ya kondu ve `calibration_type: RELATIVE` +
> `calibration_method: DLS_IRRADIANCE` + `scale: reflectance_0_1` ile iş basıldı.
> **KR-018 kapısı İLK KEZ GEÇTİ.** Boru hattının tamamı koştu: tile → çıkarım →
> AL paketleme → rapor → yayın. **AMA sonuç `NO_RESULT`** (bkz. DK-25).
>
> 🔴 **DK-25 (yeni, 2026-08-06) — AÇIK, YÜKSEK ÖNCELİK. Çıkarım hiçbir tile'ı analiz etmedi.**
> Ölçüldü: `T3.1 NaN-resilience: 16/16 tiles skipped` + `4/4 tiles skipped` → **20/20**.
> Kök neden: gerçek bir ortomozaiğin uçuş ayak izi **dikdörtgen değildir**; dışarısı
> `NaN`'dır (bu koşuda raster'ın **%43'ü**). `pipeline._process_batch` NaN taşıyan tile'da
> hata alıp **tile'ın TAMAMINI** atıyor (T3.1 dayanıklılık kalkanı). Sonuç zinciri:
> 0 tile → `confidence 0.0` → `result_mode: NO_RESULT` → `_compute_field_metrics`
> K-10 gereği `None` döner → **`metrics` hiç gitmez**, dolayısıyla DK-24'ün göreli
> dağılımı da üretilmez.
> **Yani bugün gerçek bir orto ile çıkarım pratikte HİÇBİR ŞEY analiz edemiyor.**
> Bu bir politika kararı ister (tek başıma almadım): kısmen geçerli tile ne olacak —
> (a) geçerli piksel oranı eşiği + NaN doldurma (`REFLY_RECOMMENDED.VALID_PIXEL_LOW`
> zaten 0.85 eşiğini tanımlıyor), (b) NaN-duyarlı havuzlama, (c) ayak izine kırpma.
> Seçim modelin gördüğü dağılımı değiştirir → ML incelemesi gerekir.
>
> ✅ **DK-25 KAPANDI (2026-08-06) — kısmen geçerli tile politikası, literatür dayanaklı.**
> **Eşik:** `config.tile_min_valid_ratio = 0.20`. Dayanak: Raster Vision'ın `nodata_threshold`
> **varsayılanı 1.0** (chip yalnız %100 nodata ise atılır — üretimdeki en müsamahakâr uç) ·
> uydu iş akışlarında yaygın öneri *"geçerli kaplama %20'nin altındaki sahneyi at"*.
> 🔴 **0.85 KULLANILMADI:** `REFLY_RECOMMENDED.VALID_PIXEL_LOW` uçuş düzeyinde bir
> *yeniden-uç* sinyalidir; tile'a uygulamak ayak izi sınırındaki her tile'ı atardı —
> eşiği yanlış bağlamdan kopyalamak olurdu.
> **Doldurma:** yalnız **model tensörü** için, o tile'ın **bant ortalaması**. 0 ile doldurmak
> fiziksel olarak "siyah cisim" demektir ve modele yanlış sinyal verir; bant ortalaması
> tile'ın kendi dağılımına göre en az bilgi taşıyan değerdir.
> 🔴 **ÖLÇÜME DOLDURMA GİRMEZ:** `ndvi_mean`/`ndre_mean` orijinal (NaN'lı) bantlardan
> `np.nanmean` ile hesaplanır.
>
> 🔴 **DK-25 ALT-BULGUSU — `safe_divide` "bölen sıfır" ile "girdi bilinmiyor"u karıştırıyordu.**
> NaN girdi sessizce **0.0**'a dönüyordu; %50 geçerli bir tile'da gerçek NDVI ortalaması 0.5
> iken **0.25** çıkıyordu (**%50 hata**, sessiz). DK-22'nin hesap düzeyindeki ikizi. Artık
> bilinmeyen NaN olarak yayılır; gerçek sıfır-bölen davranışı **değişmedi**.
>
> 🔴 **DK-27 (yeni, 2026-08-06) — ASIL BLOKÖR BUYMUŞ: MC-Dropout çıkarımı HİÇ koşamıyordu.**
> DK-25 düzeltmesinden sonra tile'lar hâlâ atlanıyordu. Sebep NaN **değildi**:
> ```
> RuntimeError: P1-C1: norm layer 'input_proj.spectral_spatial.norm' (GroupNorm)
> is in train mode during MC-Dropout — would corrupt epistemic uncertainty…
> ```
> `encode_with_mc_dropout` modeli MC geçişlerinden **önce** `.eval()` yapmıyordu; tek
> `self.eval()` çağrısı geçişlerden **sonraydı** ve kapı ondan önce patlıyordu. `nn.Module`
> varsayılanı **train** olduğu için kapı **her tile'da** fırlıyordu. Kapı 2026-05-17'de
> eklenmiş; gerçek bir iş hiç koşulmadığı için **o günden beri çıkarım hiç çalışmamış**.
> Düzeltme tek satır: `self.eval()` → `_enable_dropout_only()` → invariant kontrolü.
>
> 🔴 **DK-27 ALT-BULGUSU — hata SEBEBİ DOĞRULANMADAN isimlendiriliyordu.** Genel `except`
> her `ValueError/RuntimeError`'ı yakalayıp *"skipping tile due to **non-finite data**"*
> diye logluyordu. Encoder invariant hatası "NaN sorunu" diye raporlandı ve teşhis saatlerce
> yanlış yöne gitti. Üstelik gerçek sebep (`reason`) yalnız `extra`daydı ve **JSON
> biçimlendirici onu düşürüyordu** — operatör sebebi hiç göremiyordu. Mesaj artık
> `type(exc).__name__` + metni **taşıyor**.
>
> 🟠 **DK-26 (yeni, 2026-08-06) — ✅ KAPANDI 2026-08-07, ama MEKANİZMA İDDİASI ÇÜRÜDÜ.**
> Platform `worker_bridge` tüketicisi **düşmüş durumda** — platformun kendi sağlık kontrolü
> söylüyor: `health-degraded: worker_bridge unreachable`. Kuyruklar dolu bekliyor
> (`analysis_results 1 · expert_review_queue 1`, tüketici 0).
>
> ⛔ **"aio_pika tüketici görevini KALICI OLARAK öldürüyor, yeniden bağlanma yok" iddiası
> ÖLÇÜMLE ÇÜRÜTÜLDÜ (2026-08-07).** İki bağımsız ölçüm:
> * `aio_pika 9.6.2` + `aiormq`: teslim görevi `Channel.create_task(consumer(message))` ile
>   açılır; `FutureStore.add`'in done-callback'i **yalnızca görevi kümeden çıkaran bir
>   `remover`**'dır — istisnayı kanala YAYMAZ, kanalı kapatmaz.
> * `get_async_session` hatada `rollback()` + `close()` yapıyor → bağlantı havuzu da
>   zehirlenmiyor ("failed transaction" hipotezi de düşüyor).
>
> Yani tüketici **ölmüyordu**. Gözlenen "unreachable" durumu, aynı oturumda Docker
> Desktop'ın kapanmış olmasıyla açıklanır (yığın komple aşağıdaydı).
>
> ✅ **AMA ALTINDAKİ KUSUR GERÇEKTİ ve kapatıldı.** `expert_reviews.result_id`,
> `analysis_results.result_id`'ye FK'dir (`expert_review_model.py:52`). Eskalasyon
> işleyicisi ana satırı **yalnız koşullu** yaratıyordu (job_id VE mission_id dolu VE
> mission kaydı var VE `mission.field_id` dolu). Koşul tutmazsa
> `_build_expert_review_rows` (`worker_bridge_consumer.py:219`) `result_id`'yi
> `UUID(job_id)` — job_id yoksa **rastgele `uuid4()`** — yapıp satırı yine üretiyordu;
> rastgele UUID `analysis_results`'ta asla bulunmaz → commit **kesin** FK ihlali.
> Gerçek zarar tüketicinin ölmesi değil: **eskalasyon her seferinde sessizce DLX'e
> gidiyordu** (uzman incelemesi hiç yaratılmıyor → KR-019 zinciri kopuyor) ve operatör
> Postgres'in FK metnini görüyordu, EKSİK OLANIN adını değil.
> Çözüm: saf `escalation_precondition_error()` kapısı + `EscalationPreconditionUnmet`
> istisnası — DB'ye hiç dokunmadan, eksik alanın adıyla fail-closed.
> Test: `tests/unit/infrastructure/messaging/test_escalation_fk_precondition.py`
> (3 mutasyon öldürüldü + pozitif kontrol).
>
> 🟠 **DK-23 (yeni, 2026-08-05) — ✅ KAPANDI 2026-08-07.** `_overall_health_from_body`
> değeri **`round(raw, 2)`** ile 2 ondalığa indiriyor; `analysis_results.overall_health_index`
> kolonu gerçekte **`numeric(4,3)`** (ölçüldü: `information_schema`; kaynak göç
> `alembic/versions/20260103_007_analysis_jobs.py:147`), ORM'de ise `Numeric(3, 2)` yazıyor.
> `2026_08_04_analysis_results_model_align.py:40` daraltmayı **bilinçli olarak ayrı bir
> karara bırakmış** — ama `round(..., 2)` o kararı **sessizce zaten almış** durumda:
> demo satırındaki `0.264` kod yoluyla **asla** üretilemez, `0.26` olur.
>
> Üç katman ayrı ayrı yanlıştı, üçü birden hizalandı (göç GEREKMEDİ — daraltan taraf koddu):
> tüketici `round(raw, 3)` · ORM `Numeric(4, 3)` · ölçüm-yok dalı `Decimal("0.000")`.
> ORM sapması ayrıca **testleri üretimden farklı bir şemada koşturuyordu** (`create_all`
> ORM'i kullanır) — dar kolonda yeşil geçen test üretimi temsil etmez.
> Gerçek ÖN RAPOR ölçüsüyle kanıt: `mean_ndvi = 0.2657` → eski kod `0.27`, yeni kod
> **`0.266`**. Mevcut testlerden **ikisi kusuru kilitliyordu** (`0.264 → Decimal("0.26")`
> bekliyorlardı); ölçülüp güncellendiler. 3 mutasyon öldürüldü + pozitif kontrol.
> Sınır değerleri üretim yolundan ölçüldü: `0.0 · 1.0 · 1.5 · -0.5 · 0.9995` — hepsi
> `[0,1]` değişmezini koruyor ve `numeric(4,3)`'e sığıyor (`1.000` = 4 basamak, tam sınır).
>
> ⚠️ **AŞAĞI AKIŞTA ÖLÇÜLEN YAN ETKİ (öz-denetimde bulundu, gizlenmiyor):**
> `retention_service.py:257` → `health_score=int(ar.overall_health_index * 100)`.
> `int()` **aşağı keser**, yuvarlamaz. Aynı ölçüm (0.2657) için: eski zincir
> `0.27 → 27`, yeni zincir `0.266 → **26**`. Gerçek değer %26.57 olduğuna göre yeni
> sayı doğru tarafta (eski 27, çift-yuvarlamanın artığıydı) — ama bu **bir davranış
> değişimidir** ve `field_index_timeseries.health_score` ile `avg_health_score`
> toplulaştırmasına yansır. `int()` → `round()` düzeltmesi BU PR'A ALINMADI: ayrı bir
> karar (retention davranışını tek başına değiştirir) ve kapsam dışı.
>
> ✅ **DK-28 KAPANDI (2026-08-08, altıncı oturum) — zincir motor çıktısından tile'a kadar CANLI.**
> Kapanış **gerçek veriyle** doğrulandı, kod okumasıyla değil:
>
> ```
> layers            3 katman (HEALTH/ndvi · ndre · stress_ratio) -> /api/v1/tiles/...
> has_basemap       True
> tile render       HEALTH 115 KB · NITROGEN 127 KB · WATER 123 KB · BASEMAP 1.7 KB PNG
> ```
>
> Kapatan halkalar (hepsi merge edildi):
> | Halka | Nerede | PR |
> |---|---|---|
> | M1 ÜRETİCİSİ (motor dizini → 3 kanıt dosyası) | edge `package_builder.py` + `POST /calibration-gate/build` | edge #62 |
> | Adres kancası (yerel yol → nesne deposu URI'si) | edge `uri_resolver.py` | edge #62 |
> | Ayak izi ÖLÇÜMÜ (kutu değil, geçerli-piksel maskesi) | edge `RasterioFootprintReader` | edge #62 |
> | Artefakt yükleme kapsamı + tam adres | platform `X-Artifact-Name` + `assembled_uri` | platform #399 |
> | Kalibre manifest ingest ucu | platform `POST /ingest/datasets/{id}/calibrated-manifest` | platform #398 |
>
> 🔴 **Kalan üretici boşluğu YOK ama iki DAĞITIM kapısı var** (kusur değil, donanım/provizyon):
> mTLS istemci sertifikası (M2→platform yükleme) ve AV2 servisi (`is_ready_for_analysis`).
> Ayrıntı: `docs/SESSION_HANDOFF.md` §0.A.
>
> 🟡 **GÜNCELLEME (2026-08-08 denetim turu) — mTLS'in SERTİFİKA ayağı kapandı.** Özel CA +
> istemci sertifikası üretildi (`openssl verify` → OK, `clientAuth` uzantılı,
> `C:\ProgramData\TarlaAnaliz\certs\`); edge HC-03 kapısı artık `CertificateNotFoundError`
> **fırlatmıyor** (ölçüldü). Bu sertifika **satın alınmaz** — halka açık CA'lar istemci
> kimliği için sertifika vermez; güven kaynağı platformun `API_MTLS_REGISTERED_FINGERPRINTS`
> listesi, yani **kendi özel CA'mız**. Maliyet sıfır. **Kalan üç adım** (parmak izini env'e
> kaydet · mTLS-sonlandıran ters vekil `X-Client-Cert`+`X-Client-Cert-Verify: SUCCESS`
> başlıklarını set etsin · platform ayağa kaldırılsın): `docs/SESSION_HANDOFF.md` §0.A-mtls.
>
> ---
>
> ✅ **DK-34 (2026-08-08) — dashboard boş kalıyordu. KAPANDI** (platform #401).
> `/api/v1/results` `overall_health_index=0.151` dönerken `/api/v1/dashboard/farmer`
> `avg_health_score=null` gösteriyordu: `_insert_timeseries` yalnız `summary.*` yolunu
> okuyor, worker ise ÖN RAPOR'da `summary`yi KR-019 gereği boş gönderiyordu. Artık aynı
> kanonik türetme (`_overall_health_from_body`) kullanılıyor; fail-closed korundu.
> Ölçüm: dashboard `avg_health_score` **null → 15.0**.
>
> ✅ **DK-35 (2026-08-08) — kalibrasyon tipi HİÇ taşınmıyordu. KAPANDI** (platform #401).
> Edge manifesti `calibration_result.calibration_type = RELATIVE` taşıyor ama kalibre
> manifest ingest'i yalnız iki URI kolonunu yazıyordu; tüketici tipi `dataset.manifest`ten
> okuduğu için daima `NONE` görüyor ve **worker HER işi KR-018 sert kapısıyla reddediyordu**.
> Bu, DK-28 zincirinin uçtan uca kapanmasını engelleyen halkaydı. Ölçüm: düzeltme sonrası
> worker gerçek ODM ortomozaiğini işledi (36 tile).
>
> ✅ **DK-41 (2026-08-08) — taban görüntü paketleme anında COG'a çevrilir. KAPANDI** (edge #64).
> Terra RGB ortomozaiği 14527×12966 / 276 MB **düz** GeoTIFF; iç karolama ve overview
> olmadan tile sunucusu her karo için dosyanın büyük bölümünü tarıyordu. Artık M1
> paketleme adımında otomatik çevriliyor — **her uçuşta**, elle iş yok. Çözünürlük
> değişmez; fail-soft (çevrilemezse orijinal kullanılır, COG sunum optimizasyonudur).
>
> ✅ **DK-42 (2026-08-08) — nginx `upstream` IP'yi dondurup 502 üretiyordu. KAPANDI** (platform #402).
> Konteyner yeniden oluşturulunca IP değişiyor, nginx eski adreste kalıyordu
> (`upstream: http://172.18.0.2:3000` · gerçek IP `172.18.0.9` · web doğrudan 200).
> Belirti aldatıcı: **servis çalışıyor ama site 502**. Çözüm: `resolver 127.0.0.11` +
> değişkenli `proxy_pass $upstream$request_uri`. Ayırt edici testle doğrulandı (IP zorla
> değiştirildi, nginx'e dokunulmadan 3/3 HTTP 200).
>
> ✅ **DK-38 (2026-08-08) — SESSİZ YANLIŞ SAYI: `mean_ndvi` geçersiz pikselleri sayıyordu. KAPANDI** (worker #207).
> Çiftçiye gösterilen "sağlık 15/100" **yanlıştı**; doğrusu **27**. Düzeltme sonrası
> üretimde ölçüldü: `Valid-pixel mask applied (alpha_band_5): 43.0%` →
> `overall_health_index` **0.151 → 0.266** → dashboard **15 → 27**.
> ⚠️ İki kaynak gerekti: `dataset_mask()` ODM'de *all_valid* döndüğü için tek başına
> YETMEDİ; `colorinterp`'teki **alfa bandı** ikinci kaynak olarak eklendi (ölçüldü —
> ilk yazımda bu dal yoktu ve düzeltme üretimde sessizce etkisiz kaldı).
> Özgün ölçüm (aynı raster, `src.read(band_index)` — maske OKUNMUYORDU):
>
> | Hesap | NDVI ort | std |
> |---|---|---|
> | maskesiz (boş pikseller 0 sayılıyor) | **0.1515** | 0.1674 |
> | alfa bandı maskeli (doğru) | **0.2657** | 0.1372 |
> | DJI Terra, kendi bant rasterleri (`nodata=nan`) | **0.2639** | 0.1551 |
>
> Worker'ın raporladığı `0.151` maskesiz değerle **birebir** aynı. Kök neden: ODM
> ortomozaiğinde `nodata=None`, uçuş alanı dışı pikseller **0** taşıyor ve 5. bant (alfa)
> yok sayılıyor; ortomozaik köşe kutusunun yalnız **%57**'sini kaplıyor → %43 boş alan
> ortalamayı aşağı çekiyor. `compute_mean_ndvi` doğru yazılmış (NaN'ları hariç tutuyor) —
> eksik olan **maskenin pipeline'da hiç okunmaması**. Düzeltme dikkat ister: NaN'lar model
> tensörüne sızmamalı (`_build_tensor`), bu yüzden ayrı bir kalem olarak açıldı.
> **Yan bulgu (olumlu):** Terra ↔ ODM `camera` farkı **<%1** — iki motorun radyometrik
> işlemesi tutarlı, yani sorun motorda değil tüketicide.
>
> ✅ **DK-39 (2026-08-08) — "Gerçek Görünüm" GRİ KARE gösteriyordu. KAPANDI** (platform #401).
> Taban görüntü olarak yazılan ODM ortomozaiği multispektral (5 bant `float32`,
> `('Red','Green','NIR','RedEdge',None)`, 0–0.1); `indexes=(1,2,3)` 3. kanalda mavi yerine
> **NIR** okuyor ve ölçekleme olmadığı için tile düz gri çıkıyordu. Artık fail-honest:
> kaynak görünür ışık taşımıyorsa `has_basemap=False` + tile 404, düğme hiç açılmaz.
> **Mavic 3M'in mavi bandı yoktur** → o pakette gerçek renkli görünüm üretilemez; gerçek
> RGB kaynak Terra'nın `map/result.tif`'idir (ölçüldü: 4 bant `uint8`, R/G/B + alfa).
>
> 🟠 **DK-36 (yeni, 2026-08-08) — meşru dispatch yolu hâlâ kapalı.**
> `dispatch_to_worker` ön koşulları ölçüldü: `av1_report_uri=NULL` · `av2_report_uri=NULL` ·
> `calibration_records=0`. Uçtan uca koşumda bu kapı **bilinçli atlandı** ve sahte AV raporu /
> sahte kalibrasyon kaydı **YAZILMADI**. Kalem açık: AV1/AV2 üreticisi + `CalibrationRecord`
> üreticisi bağlanmalı (P19 ile aynı aile: alan var, üretici yok).
>
> 🔴 **DK-31 (yeni, 2026-08-08) — AK-4: kanonik `analysis_job.v1` bant sözlüğünü ZORLAMIYOR.**
> Worker `available_bands`'i kanonik `GREEN/RED/RED_EDGE/NIR/BLUE/LWIR` sözlüğüyle
> **vendored şemasında** daralttı (worker #206) çünkü kanonik şema alanı serbest string
> bırakıyor:
>
> ```json
> "available_bands": { "type": "array", "items": { "type": "string" } }
> ```
>
> Sözlük **başka bir kanonik şemada** (`edge/intake_manifest.v1`) tanımlı ama iş mesajında
> zorlanmıyordu — uyuşmazlığın sessiz kalmasının sebebi tam olarak bu: telin **iki ucunda
> da kapı yoktu**. Ölçülen sonuç: platformdan gelen her iş `capability_detector` sert
> kapısında düşüyordu, ve düşmese bile bantlar **konuma göre** yanlış eşlenip NDVI'yi
> sessizce bozuyordu (ort +0.3381→+0.3910, std 0.1866→0.0695).
>
> **İstek:** kanonik `schemas/worker/analysis_job.v1.schema.json` →
> `drone_metadata.available_bands.items` alanına `intake_manifest.v1` ile **aynı enum**.
> Daraltma güvenli: tek üretici (platform `build_analysis_job_v1`) zaten kanonik gönderiyor.
> Tam gerekçe: `tarlaanaliz-worker/denetim/birlesik_devir_spec_arsivi_2026.md` §1
> (2026-08-11'e kadar ayrı dosya: `band_sozlugu_devir_spec_2026_08_08` §3).
> Kanonik ayna inince worker'ın I-5 sapması kapanır.
>
> ---
>
> 🟠 **DK-32 (yeni, 2026-08-08) — `/calibration-gate/build` üzeri-yazma muhafızı taşımıyor.**
> Aynı `batch_id` ile ikinci çağrı mevcut kanıt setini **sessizce eziyor** (koşum 6'da
> ölçüldü: iki kol aynı batch'e yazdı, ikincisi kaldı). Yeniden kalibrasyon meşru bir
> operatör işlemidir, ama `/validate`'ten geçmiş bir paketi ezmek değildir. **Karar
> gerekiyor:** (a) idempotent üzerine-yaz (bugünkü), (b) mevcut paket varsa 409,
> (c) `force=true` bayrağı. Kapsam dışı bırakıldı, uydurulmadı.
>
> ---
>
> 🟠 **DK-33 (yeni, 2026-08-08) — `OSAVI` kanonik `layer_type` kümesinde yok.**
> DJI Terra gerçekten üretiyor (koşum 5: Terra 10 çıktı verdi, biri `OSAVI.tif`).
> Yazıcı uydurma enum değeri yazmıyor → giriş yazılıyor ama `layer_type` alanı
> KONULMUYOR (tasarım gereği). Kanonik kümeye eklenmeli mi, ayrı sözleşme kalemi.
>
> ---
>
> 🔴 **DK-28 (yeni, 2026-08-07) — "Gerçek Görünüm" düğmesi ÜRETİMDE HİÇ GÖRÜNMEZ.**
> Kalem aslında "düğmenin görsel doğrulaması" idi; doğrulama **yapılamadı, çünkü
> doğrulanacak bir şey yok** — özellik uçtan uca ölü. Zincir komutla ölçüldü:
>
> | Halka | Ölçüm | Sonuç |
> |---|---|---|
> | Arayüz | `MapLayerViewer.test.tsx` 6 test (yerleşim sırası, varsayılan kapalı, örtme hatası, pozitif kontrol) | ✅ doğru ve test edilmiş |
> | Platform kapısı | `tile_service_impl.py:130` `_BASEMAP_INDEX = "rgb"` · `:351` `has_basemap = _resolve_cog_uri(result_id, "rgb") is not None` | manifestte `maps.rgb.geotiff` arıyor |
> | Manifest kaynağı | `_resolve_manifest_uri` → `DatasetModel.result_uri` = **worker'ın sonuç manifesti** | worker üretiyor |
> | Worker üretimi | `reporting_agent.py:52-57` `_MAPS_BY_RESULT_MODE` = `ndvi, ndre, stress_ratio` — **`rgb` HİÇBİR result_mode'da yok** | ❌ |
>
> Anahtar zinciri **tek yönlü ve kapalı**: `_build_manifest` → `"maps": index_maps`
> (birebir) ← `sink.upload(artifacts)` ← `render_index_maps` yalnız `allowed` içinde
> dönüyor ← `allowed = _MAPS_BY_RESULT_MODE[result_mode]`. Yani `maps.rgb` **üretilemez**.
>
> ⚠️ **İlk kanıtım zayıftı, öz-denetimde düzeltildi.** `grep -rn '"rgb"' worker/src` → 0
> eşleşme yazmıştım; **pozitif kontrolle** sınayınca (`"ndvi"` 17 · `"stress_ratio"` 14
> eşleşme veriyor, yani araç çalışıyor) geniş tarama `grep -rin "\brgb\b"` **114 eşleşme**
> buldu. Hepsi incelendi: SSL eğitimi / augmentation / encoder / renderer **iç değişkenleri**
> — hiçbiri artefakt anahtarı değil. Tek gerçek-renk çıktısı `true_color.png`, yalnız
> `expert_bundle_persistence.py` üzerinden **yerel uzman paketi dizinine** yazılıyor
> (`<output_dir>/<job_id>/true_color.png` + kendi manifesti) ve **PNG**'dir; tile servisi
> ise açıkça GeoTIFF ister (*"GeoTIFF (COG) tercih; yoksa tile render edilemez"*).
> Sonuç değişmedi ama artık kanıtlı: **dar grep'in "0 eşleşme"si tek başına kanıt değildi.**
>
> Yani `has_basemap` **yapısal olarak daima False**; düğme hiç render edilmez. Arayüz
> testleri `has_basemap: true`'yu **kendileri enjekte ettiği** için yeşil — bu tam olarak
> "alan-kapısı ≠ bilgi-kapısı" tuzağı: tüketici doğru, ÜRETİCİ yok.
>
> ⚠️ **Tek satırlık düzeltmesi YOK, mimari karar gerektiriyor.** `render_true_color_composite`
> mevcut ama yalnız `expert_bundle_producer.py:320`'ye bağlı (uzman paketi, çiftçi haritası
> değil). Üstelik Mavic 3M'in **mavi bandı yok** (G/R/RE/NIR) — gerçek renkli ortofoto
> worker'ın hesapladığı bir indeks değil, drone'un ayrı 20MP RGB kamerasının Terra/ODM
> ile işlenmiş **girdi artefaktıdır**. Doğru akış: ingest → dataset manifesti →
> `maps.rgb.geotiff`. Karar sahibinin: (a) RGB ortofotoyu ingest hattına ekle,
> (b) düğmeyi kaldır, (c) olduğu gibi bırak ve belgele.
>
> ### ✅ KARAR: (a) — 2026-08-07, sahip kararı. Platform yarısı UYGULANDI.
>
> **Sözleşme değişikliği GEREKMEDİ.** Kanonik şema bunu zaten modelliyordu:
> `schemas/platform/calibrated_dataset_manifest.v1` → `outputs[].layer_type` enum'unda
> **`ORTHO`** var (*"ORTHO/DSM raster ürünleridir"*). Yani eksik olan sözleşme değil,
> **kablolamaydı**.
>
> **Zincirin ölçülmüş hâli (2026-08-07) — üç depoda:**
>
> | Halka | Durum | Kanıt |
> |---|---|---|
> | Motorlar RGB ortomozaik üretiyor | ✅ | Terra `map/result.tif` = *"the RGB 2D orthographic map"* |
> | Edge motor çıktısını buluyor | ✅ | `calibration_gate/engine_adapter.py` → `ortho_path` (Terra/ODM/Pix4D üçü için) |
> | Edge onu kullanıyor | ⚠️ **yalnız yerel** | `expert_image_renderer.py` — uzman görseli; platforma gitmiyor |
> | Edge manifeste `outputs[ORTHO]` yazıyor | ❌ | `manifest_writer.py`'de `outputs`/`layer_type`/`ORTHO` → **0 eşleşme** |
> | Platform kalibre manifesti kabul ediyor | ❌ | `calibrated_dataset_manifest` platform kodunda **yalnız 1 yorum satırı**; OpenAPI'da uç **yok** |
> | Platform adresi saklıyor | ✅ **YENİ** | `datasets.rgb_ortho_uri` (göç `2026_08_07_dataset_rgb_ortho_uri.py`) |
> | Tile servisi sunuyor | ✅ **YENİ** | `_resolve_basemap_uri()` — ingest kanonik, worker manifesti geriye dönük yedek |
> | Arayüz düğmesi | ✅ | `MapLayerViewer` 6 test |
>
> **Bu turda yapılan (platform, PR ile):** `datasets.rgb_ortho_uri` kolonu (additive,
> nullable, `varchar(500)` — `av2_report_uri` ile aynı şekil) + domain entity + repository
> iki-yön eşlemesi + `_resolve_basemap_uri()`. `has_basemap` ve `/tiles/{id}/basemap/...`
> artık **ingest tarafına** bakıyor. Fail-honest davranış korundu: adres yoksa `None` →
> uç 404 → düğme gizli. 4 mutasyon öldürüldü + pozitif kontrol.
>
> **Neden JSONB `manifest` içine değil:** `datasets.manifest` **ham intake** manifestini
> tutuyor (`ingest_service_impl.py:201` — batch_id, kiosk_id, dosya sayısı), kalibre
> çıktıları değil. Ayrıca tile servisi bunu tile başına okur; ayrı kolon JSONB
> ayrıştırması gerektirmez.
>
> **KALAN — edge yarısı (donanım-kapılı, M1/M2 istasyonu henüz yok):**
> 1. `manifest_writer` → `outputs[]`'a `{layer_type: "ORTHO", uri, sha256, reflectance_scale}` yaz,
> 2. ortomozaiği yükleme kümesine ekle (bugün yalnız yerelde duruyor),
> 3. platform: kalibre manifesti kabul eden uç + `rgb_ortho_uri`'yi yazan adım
>    (OpenAPI'da uç **hiç tanımlı değil** — bu bir sözleşme işi, KR-081 contract-first).
>
> ✅ **DK-29 (2026-08-07) — KAPANDI (platform PR #395 → `02be248`): `av2_report_uri` iki farklı şeydi.**
> DK-28'in edge yarısını bağlarken çıktı. Aynı kolon iki yerde çelişik tanımlanmış:
> * `src/core/domain/entities/dataset.py:58,75` → *"Merkez **AV2 raporu** URI"*,
>   `CALIBRATED_SCANNED_CENTER_OK` için zorunlu;
> * `src/application/services/av2_orchestrator.py:151` → `av2_report_uri=report.report_uri`
>   (antivirüs **tarama raporu**, KR-073);
> * `src/infrastructure/messaging/worker_job_publisher.py:11,145,159-169` → aynı alanı
>   **`image_urls[0]`** yapıyor ve *"av2 kalibre **ortomozaik**"* diye adlandırıyor;
>   doğrulaması yalnız `s3://|https://` şema kontrolü — içeriğin raster olduğunu **hiç
>   denetlemiyor**.
>
> **Kanıtın desteklediği:** iki tanım çelişiyor, biri yanlış. **Desteklemediği:** üretimde
> kolonda fiilen ne durduğu — onu görmek için canlı satır gerekir ve o satırı yazacak
> ingest yolu donanım-kapılı. Worker bu oturumda gerçek rasteri **harness ile doğrudan
> URL** verilerek okudu, bu yoldan değil. RGB ortomozaiği bu alana bindirmeden önce
> ayrıştırılmalı: AV raporu ile raster adresi **ayrı kolonlar** olmalı.
>
> **ÇÖZÜM:** yeni kolon `datasets.calibrated_ortho_uri` (additive, nullable,
> `varchar(500)`); `av2_report_uri` **değiştirilmedi** (AV zinciri KR-072 9-durum
> geçişleri ona bağlı). Yayıncı artık yeni alanı okuyor ve eksikse **iki alanın
> farkını adıyla açıklayan** bir hatayla fail-closed reddediyor.
>
> **Kodda yedek YOK, veride taşıma VAR.** *"ortho yoksa av2'ye düş"* fallback'i
> bilerek yazılmadı — düzeltilen belirsizliği kalıcılaştırırdı. Göç,
> `av2_report_uri` fiilen `.tif`/`.tiff` ise değeri taşır. Mantık **canlı
> Postgres'te** sınandı (işlem `ROLLBACK`'li): `s3://b/ORTO.TIF` taşındı (büyük
> harf de yakalandı), `s3://b/av2_report.json` NULL kaldı.
>
> ⚠️ **BİLİNÇLİ SONUÇ — dağıtım artık her iş için fail-closed.**
> `calibrated_ortho_uri`'nin ÜRETİCİSİ henüz yok (ölçüldü) — kalibre-ingest yolu
> DK-28 ile **aynı donanım-kapılı yol**. Önceki davranış *sessizce yanlıştı*
> (worker'a denetim belgesi gidiyordu) ve worker platform-dağıtımlı bir işi zaten
> hiç başarıyla tüketmemişti. 4 mutasyon öldürüldü + pozitif kontrol.
>
> ✅ **DK-30 (2026-08-07) — KAPANDI (aynı PR): yerel `DATABASE_URL` göçü engelliyordu.** DK-28 göçünü
> gerçek DB'de doğrularken çıktı. `backend` konteynerinde:
> * `DATABASE_URL=postgresql+asyncpg://…@**localhost**:5432/tarlaanaliz`
> * ama `TARLA_DB_HOST=**postgres**` (doğru servis adı)
>
> `alembic/env.py:54` **önce `DATABASE_URL`'e bakıyor**, parçalı `TARLA_DB_*`
> değişkenlerine (satır 62-64) ancak o yoksa düşüyor. Sonuç: konteyner içinde
> `alembic upgrade head` → `Connection refused (localhost:5432)`. Göç yalnız
> `-e DATABASE_URL=…@postgres:5432/…` ile elle ezilerek koşuyor.
>
> Bu, "göç koştu sandım ama koşmadı" sınıfının aynısıdır (2026-08-06'da `migrate`
> servisi `alembic/`'i mount etmediği için sessizce `exit 0` dönmüştü). Düzeltme:
> compose'daki `DATABASE_URL` host'u `postgres` olmalı **ya da** env.py'nin öncelik
> sırası belgelenip compose ondan türetilmeli. **Ölçüm komutu:**
> `docker compose exec -T backend printenv | grep -E "DATABASE_URL|TARLA_DB_HOST"`
>
> ⛔ **İLK ÇERÇEVELEMEM EKSİKTİ, düzeltiyorum:** "göçü engelliyor" dedim ama
> **tasarlanan yol `migrate` servisidir ve o DOĞRU** — tuzağı 2026-07-21
> denetiminde üç bağımsız BLOCKER olarak bulup çözmüşler (compose:231-246).
> Gerçek boşluk şuydu: göç **yazan** kişi için doğal yer `backend`'dir, çünkü
> `migrate`in aksine `./alembic`i **mount eder** (compose:349) — yeni göç anında
> oradadır; `migrate` imajı bayattır ve `build` ister. Ama `backend`'de aynı
> override yoktu.
>
> **ÇÖZÜM:** aynı açık `DATABASE_URL` override'ı `backend`'e de eklendi.
> Ezmek güvenli: uygulama `DATABASE_URL`'i **okumaz** (`grep -rn DATABASE_URL src/`
> → tek eşleşme `cli/commands/migrate.py`); runtime `TARLA_DB_*` üzerinden bağlanır.
> Üretim yolundan doğrulandı (elle override VERMEDEN): `alembic current` → head ·
> `downgrade -1`/`upgrade head` → kolon 1→0→1 · `GET /health` → **HTTP 200**.
>
> 🆕 **DK-16 (yeni, 2026-08-05):** `metrics` zinciri **uçtan uca canlı mesajla** doğrulanmadı.
> Her halka ayrı ayrı mutasyonla test edildi (worker üretim · to_dict serileştirme · platform
> üç kademeli türetme) ama tek bir gerçek iş mesajıyla baştan sona akış görülmedi.
>
> 🔴 **DK-1 için QA kararı (2026-08-05):** tercih sırası davranış testi **şimdi yazılmadı** —
> üretimde koşmayan bir dala test yazmak **sahte güven** üretir. Test, worker hizalamasıyla
> **birlikte** gelir.

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

**Karşılaştırılan kaynaklar:** `tarlaanaliz-worker/denetim/aktif_ogrenme_secim_tasarimi_S1_S2_dedup.md`
⟷ bu eylem planı. (2026-08-11'de o dosya İKİ kaynağın birleşimi hâline geldi: **BÖLÜM A** =
tasarım, 787 satır · **BÖLÜM B** = kod-doğrulamalı denetim, 375 satır — eskiden ayrı dosyaydı,
adı `aktif_ogrenme_S1_S2_dedup_worker_uygulanabilirlik_denetimi_2026-07-18`. Çelişkide
**BÖLÜM B otoriterdir**.)
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

✅ **W8 / Ç-2 KAPANDI (2026-08-07).** Liste artık **yorum değil, KAPI**:

* `src/shared/encoder_version.py` → `EMBEDDING_SPACE_DRIFT_TRIGGERS` (kapalı küme):
  `SSL_RETRAIN · BACKBONE_SWAP · CHANNEL_TRANSFER · VIT_LORA_ATTENTION ·`
  **`CALIBRATION_SCALE_CHANGE`** (+ `INITIAL`, yalnız sürüm 1 için).
* `config/model_registry.yaml` → yeni kardeş alan `encoder_version_reason`.
  Öneriden farkı: `calibration_engine` **motorun adını** tutardı (Terra/ODM), oysa
  guard'ın ihtiyacı "gömme uzayı kaydı mı?" sorusunun cevabı. Gerekçe alanı hem
  kalibrasyon hem de diğer dört tetikleyiciyi **tek eksende** taşır; motor adı zaten
  `calibration_metadata` sözleşmesinde iş mesajıyla geliyor (mükerrer kaynak açılmadı).
* `scripts/validate_model_registry.py` → `find_encoder_version_violations()`:
  eksik / uydurma / sürüme uymayan gerekçe = **BUILD FAIL** (contracts_gate.yml:79'da
  zaten koşuyor). Sürüm 1 ⇒ `INITIAL`; her artırım ⇒ bir tetikleyici adı.
* Sürüklenme kapıları: kanonik küme ile **docstring** ve **operatörün gerçekten baktığı**
  `model_registry.yaml` metni ayrık düşerse test kırmızıya döner.
* 4 mutasyon öldürüldü (tetikleyiciyi sil · doğrulayıcıyı hep-geçer yap · `main`'den
  kontrolü çıkar · canlı registry'ye uydurma gerekçe yaz) + pozitif kontrol; gerçek kapı
  uydurma gerekçede `exit=1` verdi.

**Ölçülmüş gerekçe (kanıt):** ODM `none → camera`, aynı tarla + aynı 670 fotoğraf →
ortalama NDVI 0.182 → 0.267 (**+%47**), "en zayıf %20" IoU **0.355**; Terra ↔ ODM piksel
sıra korelasyonu **0.299** (`docs/TERRA_ODM_KARSILASTIRMA_2026-08-06.md`).

⚠️ **AL-W8 hâlâ açık ve W8'in yanında durmalı:** ilk gerçek artırımdan ÖNCE legacy
`None`-sürüm gömmeleri v1'e damgalanmalı (fail-open köprü kapansın), aksi hâlde eski
vektörler gerçek bir gömme-uzayı değişiminin ötesine "bedava" biner.

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

**Kaynak devir spesi:** `tarlaanaliz-worker/denetim/birlesik_devir_spec_arsivi_2026.md` §9
(2026-08-11'e kadar ayrı dosya: `audit_escalation_reason_devir_spec_2026_07_19`)
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
| **B13-1** | **KİRAZ'ı ticari olarak aç** *(KG-0.d-EK "seçenek B")* — ⭐ **kiraz kararının KANONİK adresi budur** (§14.17 ÖNCELİK 2 buraya işaret eder) | 2026-07-31'de ölçüldü: **kapatılacak risk yok** — CHERRY `GAP_OFFERED_CROPS`'ta değil, tarla bile açılamıyor. Açmak **yeni özellik**, hata düzeltme değil. **2026-08-24'te ürün sahibi yeniden erteledi** ve ölçüm **hâlâ geçerli** (aşağıya bkz.) | **Dört yerde birden:** ① platform `GAP_OFFERED_CROPS`'a `CHERRY` ② contract `crop_type.enum.v1`'e `CHERRY` (**MINOR**, + C8 töreni) ③ edge `ndvi_thresholds.yaml` + `phenology_calendar.yaml` ④ fiyat/fenoloji kayıtları. ⚠️ `data_status: limited` → tespit kalitesi zayıf olur; **ÖN RAPOR (indeks) sorunsuz** çalışır. 🔴 **+ BEŞİNCİ yer (2026-08-21'de ortaya çıktı):** `model_registry`'de `cherry_*` **tek giriş yok** → dört katman da `MODEL_YOK` ile fail-closed kesilir. Yani kirazı açmak artık **model eğitimi** de gerektiriyor; "iki YAML girdisi" sanılmasın |
| **B13-2** | **BUĞDAY'ı ticari olarak aç** | Wire enum'da **var**, edge tablosunda yok; ama `GAP_OFFERED_CROPS`'ta da yok → bugün satılmıyor. Tablo yazmak, satış kararı olmadan **kullanılmayan config** üretir | ① `GAP_OFFERED_CROPS`'a `WHEAT` ② edge iki YAML girdisi (**birkaç saat**) ③ fiyat kaydı. **Veri `strong`** → en ucuz gerçek kazanç, satış kararı verilirse ilk sıradaki |
| **B13-3** | SUNFLOWER / OLIVE tabloları | İkisi de satılmıyor **ve** `stage1: research` → `is_bookable` zaten reddediyor | Düşük; B13-2 ile aynı desen |

> ⚠️ **Dört eksen kuralı (2026-07 denetim kararı, `crop_type.py:50-68`):** bir mahsulü açmak
> **tek yerde** yapılmaz. `GAP_OFFERED_CROPS` (satılan) · VO `_VALID_CODES` (domain-geçerli) ·
> wire `crop_type.enum.v1` (mesaj) · worker-internal (12) **ayrı eksenlerdir**; biri diğerinin
> kopyası değildir. Yalnız birini değiştirmek sessiz kırık üretir.

### 🍒 KİRAZ — ertelemenin bedelsiz olduğunun kanıtı (ölçüldü 2026-08-24)

Ekim'de bu satırı okuyan kişi bugünkü tartışmayı bilmeyecek; kanıt burada duruyor.
**Soru:** kiraz kararını ertelemek canlı bir risk bırakıyor mu? **Cevap: hayır.**

| Kaynak | Bugünkü değer | Anlamı |
|---|---|---|
| `crop_type.py:81` → `GAP_OFFERED_CROPS` | `{COTTON, CORN, PISTACHIO, GRAPE}` | **CHERRY YOK** → tarla açılamaz, sipariş **SUNUM** kapısında kesilir |
| `data/crop_readiness.json` → `CHERRY` | `{stage1: pilot, data_status: limited, bookable: true}` | **TESLİM** kapısı "evet" der |

İki değer çelişmiyor, **ayrı eksenden** okuyor (SUNUM ⟂ TESLİM). Çiftçi kirazı
**sipariş edemiyor bile** — dolayısıyla *"sipariş fail-closed kesiliyor"* durumu
pratikte hiç oluşmuyor. ⚠️ `bookable: false` yazarak "temizlemek" **yanlıştır**:
`tests/unit/test_crop_readiness_manifest_sync.py` `bookable == (stage1 ∈
{production, pilot})` kuralını bağlar, CHERRY'nin `stage1`'i `pilot`'tur — elle
düzenleme tam da o testin yakalamak için var olduğu insan-senkron hatası olur.

⏳ **Yeniden gündeme gelme tetikleyicisi:** kirazı **satışa açma** kararı verilirse
(yukarıdaki beş yer + model eğitimi). Kendiliğinden bozulan bir şey yok; kalem
**takvimle değil kararla** açılır.

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


---

# 14. TUR 1 DENETİM SONRASI — ÇÖZÜM SIRASI (2026-07-31)

> **Kaynak:** 10 disiplinli bağımsız denetim → ajanlar arası tartışma → senkronizasyon çatışma
> matrisi → ana ajanın kanıta karşı kendi ölçümü. **146 bulgu** (14 KRİTİK / 45 YÜKSEK).
> **Kanıt arşivi:** `denetim/denetim_raporu_2026-07-31_10disiplin.md` — o dosya iş listesi DEĞİLDİR.
> ⛔ = **C8 release töreninden ÖNCE zorunlu.**
>
> ### 📍 İlerleme
> **KADEME 0 ✅ TAMAM (2026-07-31)** — D1…D6 + plan dışı D3-b · CI'da **9/9 yeşil** (PR #21,
> `headRefOid` doğrulandı) · kanıt: `denetim/denetim_raporu_2026-07-31_kademe0_kapi_mutasyonlari.md`.
> **KADEME 1 ✅ contract yarısı TAMAM** — D7 · D8 · D9 + plan dışı D3-c. Maliyet pencereleri
> **kapatıldı** (D7 `footprint_wkt` kaldırma · D9② yeniden adlandırma — ikisi de bu turda bedavaydı).
> **KADEME 2 ✅ iş kalemleri TAMAM** — C11 absorpsiyonu (D10-E2) · C2″ hükmü düzeltildi (E1) ·
> `$ref` kararı yazıldı (E3 → §14.2.1, **onay bekliyor**) · `relative_path` deseni gerçek çıktıyı
> kabul ediyor (E5) · `maxItems` 8000 (E6). **Aktif kilit:** E11 **C8'den önce merge edilmez** (E4).
> **KADEME 3 ✅ TAMAM** — D12…D15 + plan dışı D3-d (bileşim körlüğü). Denetim satırı artık
> ölçtüğü sistemi değiştiremiyor: konsensüs dışı · JOIN anahtarlı · gruba bağlanamaz ·
> seçim kanıtı (π_h) taşır · model güveni kapalı.
> **KADEME 4 ⚠️ kısmen TAMAM** — D17 (WATER_STRESS `proxy_only` + ön fazdan çıktı) ve D18
> (`api/` PII taraması + kapsam-duyarlı `phone`) bitti; D16'nın kapı/tanım/doküman parçaları
> yapıldı, **GÖÇ parçası (D16-b) koordinatör kararına bırakıldı** — hangi kaynak normatif
> kalacak? Karar verilmeden gövde taşımak normatif içerik kaybı riski taşıyor.
> **Sıradaki: KADEME 5 (§14.5) ve C8 ön koşulları** — ⛔ kalemler: D16-b · §14.2.1 `$ref` onayı.
> **Açık kalan kararlar:** **§14.2.1 `$ref` onayı** · **D4-b** (parite kapısı CI'da) · **D4-c**
> (matris sürümleme kapsamı) · **SD8** (etiketsiz 16 sürüm) · **C6b/E13** · **AK-1** CHLOROPHYLL_A.
> **Başka depoya düşen iş:** **E15** (edge fail-loud) · **P14** (platform fail-open adımı) ·
> **E16** (edge ürün adı biçimi + vendored yenileme).
> **Turda doğan açık kalemlerin TAMAMI:** §14.5.1 tablosu (AK-1…AK-7).

**Öncelik hiyerarşisi (çatışma çözerken kullanılan ölçüt sırası):**
① fiziksel/ölçüm geçerliliği → ② geri alınamazlık → ③ güvenlik değişmezi → ④ istatistiksel
geçerlilik → ⑤ kanıt/kapı bütünlüğü → ⑥ mimari tutarlılık → ⑦ süreç kolaylığı.
Anahtar ilke: **"Yeşil ama yalan bir kapı, kırmızı bir kapıdan tehlikelidir."**

> ## 🧭 TEK YETKİLİ GİRİŞ NOKTASI — bunu okumadan §14'e dalma
>
> **Sorun (ölçüldü 2026-08-11):** bu dosyada *“sonraki oturum buradan başla”* iddiası
> taşıyan **beş** bölüm vardı (§14.7 · §14.9 · ▶️ GİRİŞ NOKTASI · tarihsel kayıt · §14.8)
> ve bölümler **sıra dışıydı** (14.7 → 14.6 → 14.9 → başlıksız ▶️ → 14.8 → 14.10).
> Hangisinin canlı olduğu okurun tahminine kalıyordu.
>
> **2026-08-24'te sadeleştirildi:** süperseded bölümlerin **gövdeleri** arşive
> taşındı, **açık kalemleri** §14.A'da canlı tabloya çıkarıldı. Plan 3993 → ~3330 satır.
>
> | Bölüm | Statü | Nerede |
> |---|---|---|
> | **§14.17 (2026-08-21)** | 🟢 **CANLI GİRİŞ NOKTASI** | **planda** — beş öncelik (② kiraz **§13.1 B13-1**'e taşındı) + 2026-08-24 durum güncellemesi |
> | **§14.A (2026-08-24)** | 🟢 **canlı açık borç** | **planda** — arşive taşınanların **tüm** açık kalemleri (14 + uzman ekranı 8 + Ö1) |
> | **§14.10 (2026-08-10)** | 🟢 **canlı tablo** | **planda** — `AL-K1…AL-K20`, **19'u açık** (kart/indeks/termal borçları) |
> | **§14.5 · §14.7 · §3.6** | 🟢 canlı | **planda** — kendi açık kalemlerini taşırlar |
> | §14.16 (2026-08-21) | 🟠 süperseded | **planda** — ① ve ②'nin uygulama kaydı + 5 kalemlik *"açıkça yapılmayanlar"* |
> | §14.9 · §14.8 · §14.11 · §14.12 · §14.14 · ▶️ GİRİŞ NOKTASI · ▶️ v8.0.0 | 📦 **arşiv** | `EYLEM_PLANI_ARSIV_2026-08.md` — gövde + kanıt |
> | §14.15 (2026-08-20) | ⛔ **KALDIRILDI (2026-08-21)** | Mezar taşı planda; açık kalemleri §14.17'ye taşınmıştı |
>
> ⚠️ **Hiçbir açık iş arşive gömülmedi** — taşımadan önce her bölüm `⬜` **ve**
> `🔴/🟠/🟡` ile birlikte tarandı, açık kalemler §14.A'ya çıkarıldı, sonra gövde taşındı.
> Kanıt: plandan çıkan 650 satırın 643'ü arşivde **bayt-özdeş**, kalan 7'si bilinçli
> yeniden yazılan kiraz bloğu.
>
> 🔬 **Yöntem uyarısı (kendi kusurum, kayda geçiyor):** bölümlerin açık iş taşıyıp
> taşımadığını ölçmek için ilk turda yalnız **⬜** saydım. Bu **yanıltıcıdır** —
> ▶️ GİRİŞ NOKTASI bölümü 0 ⬜ gösteriyordu ama açık kalemlerini **🔴** ile işaretliyor.
> Bir bölümü silmeden önce **⬜ ve 🔴 birlikte** sayılmalı, üstelik kalem kimliklerinin
> başka yerde izlendiği de doğrulanmalı (`kimlik ∈ blok − blok_dışı` = 0 olmalı).


## 14.0 KADEME 0 — Kapılar dürüst hale gelsin (her şeyden ÖNCE) — ✅ **TAMAMLANDI (2026-07-31)**

> **Durum:** D1…D6 **altısı da yapıldı** · süit **735 geçti / 2 beyanlı xfail / 0 skip** ·
> her kapı **mutasyonla** doğrulandı (kanıt: `denetim/denetim_raporu_2026-07-31_kademe0_kapi_mutasyonlari.md`).
> Turda **beyan edilmemiş breaking yok** — ve bu artık *ölçülmüş* bir sıfır, kör bir sıfır değil.

| # | İş | Durum | Kapatır | Dosya |
|---|---|---|---|---|
| ✅ **D1** | `verify-checksums` → `summary.needs` **ve** fail koşuluna girdi · breaking adımından `continue-on-error: true` kaldırıldı · *"Don't fail - just warn"* yerine **beyan kapısı**: breaking **yasak değil, BEYAN EDİLMEMİŞ olması yasak** (`CONTRACTS_VERSION.md` → `**Breaking Change:** YES`) · dedektör çıkış kodu sözleşmesi **0/1/≥2** ve `≥2 = kapı KÖR` ayrı hata · `detect-breaking-changes` da `summary` fail koşuluna eklendi (push'ta `skipped` kabul) | ✅ | SD3, SD5 | `.github/workflows/contract_validation.yml` |
| ✅ **D2** | Çıkarıcı **her başlık düzeyinde 4 biçimi** tanıyor. ⚠️ **Ölçüm plandan büyük çıktı:** registry `^## ` regex'iyle **54 tanımın 6'sını** görüyordu (%89 kör, Q6 doğrulandı) ve SSOT metnindeki 3 köşeli-parantezsiz başlık da kaçıyordu. **Q5 de kapatıldı:** `test_data_layer_kr_present_in_ssot_text` alt-dize kontrolüydü → KR-088/091 için **tamamen boştu** (o ikisi metinde yalnız çapraz-atıf satırında geçiyor, gövdeleri registry'de); artık **tanım başlığı** şartı var. `CLAUDE.md`'nin KR tablosu ölçülen sayılarla düzeltildi (birleşim 55 · kesişim 50 → AR3 doğrulandı, iki kaynak **iç içe**) | ✅ | Q6, **Q5**, AR3 | `tests/test_kr_reference_integrity.py`, `CLAUDE.md` |
| ✅ **D3** | `compare_schemas` **özyinelemeli** (`properties`/`patternProperties`/`$defs`/`items`/`contains`/`if-then-else`/`not`/`propertyNames`/`allOf`/`anyOf`/`oneOf`/`prefixItems`) + **25 testlik regresyon süiti**. **Plan dışı 3 ek bulgu bu turda kapatıldı:** ① `x-context-subsets` (bağlam-bazlı KABUL listeleri, `calibration_type.enum`) enum ekseni gibi karşılaştırılıyor — değer düşmesi MAJOR ② okunamayan şema artık **exit 2** (eskiden sessizce `{}` dönüyordu = kapı kör) ③ **Windows'ta araç HİÇ koşmuyordu** (cp1254 emoji çökmesi) → `validate.py`'deki kalıcı UTF-8 düzeltmesi buraya da alındı, yani SDLC_GATES §1C maddesi ilk kez uygulanabilir | ✅ | SD1, SD2, Y5 | `tools/breaking_change_detector.py`, `tests/test_breaking_detector_recursion.py` |
| ✅ **D3-b** 🆕 | **BU OTURUMDA BULUNAN DÖRDÜNCÜ YALAN:** dedektör ilerleme başlığını **stdout**'a basıyordu; CI `--json > breaking_changes.json` yönlendirmesi geçersiz JSON üretiyor, `json.load` patlıyor ve CI'ın `if` bloğu **else** dalına düşerek `has_breaking=false` yazıyordu. ⇒ `continue-on-error` hiç olmasaydı bile kapı **daima "breaking yok"** derdi. Banner `stderr`'e alındı + CI'ya *"bozuk JSON asla breaking-yok diye okunamaz"* adımı + `test_cli_json_output_is_parseable` regresyonu | ✅ | (denetimde yoktu) | aynı |
| ✅ **D4** | CI bağımlılıkları **tek kaynağa** indi (`requirements-dev.txt`; `pyyaml` + `pytest-cov` eklendi → Q2'nin 18 sessiz atlaması bitti) · `paths:` filtresi testlerin **ölçülen** okuma yollarından türetildi (`ssot/**`, `docs/**`, `drone_capability_matrix.yaml`, `pyproject.toml`, `requirements-dev.txt`) · `pytest -rs` + **`tests/conftest.py` atlama kapısı**: beyan edilmemiş her skip gerekçesi oturumu düşürür, CI özetine skip bütçesi yazılır | ✅ | SD6, Q2, Q3, Q7 | CI, `requirements-dev.txt`, `tests/conftest.py` |
| ✅ **D4-b** | **KARAR VERİLDİ (2026-08-01): kapı KARŞI TARAFTA koşar — PAT YOK.** Ölçüm sayısı da düzeltildi: 45 değil **47** (CI logu: `972 passed, 47 skipped, 2 xfailed`; hepsi tek gerekçe — `test_vendored_parity.py:88` *"kardeş depo yok"*). **Kararı belirleyen ölçüm:** bu depo **PUBLIC**, kardeşlerin üçü de PRIVATE (`tarlaanaliz-platform`, `tarlaanaliz_worker`, `tarlaanaliz_edgekiosk`). ⇒ **PAT seçeneği reddedildi:** private depo anahtarını **public** bir deponun Actions ortamına koymak sır yüzeyini yanlış yöne açar (fork PR/`pull_request_target` yapılandırma hatası tek adım uzakta). **Ters yön bedava:** kardeş CI'ı bu public depoyu `GITHUB_TOKEN` ile ek sır olmadan çeker. Yön ayrıca **daha doğru** — vendored kopyayı değiştiren PR kardeş depoda açılır, sapma orada ve *üretildiği anda* yakalanır; buradan bakınca yalnız kardeş `main`'i görünür, açık PR'daki sapma zaten görünmez. **Test ikinci kez yazılmaz:** kardeş depo `tests/test_vendored_parity.py`'yi **olduğu gibi** koşar (kopyalanan kapı, D16'nın kapattığı ikili-gövde hatasının test hâli olurdu) | ✅ | AR4, Y3, E14 | `tests/conftest.py` beyanı + `test_vendored_parity.py` docstring'i güncellendi · uygulama: **E17/W10** |
| ⬜ **D4-b2** 🟡 | **Kararın kalan boşluğu (yazılı kabul):** kapı kardeş tarafa taşınınca *"kanonik değişti ama tüketici hiç PR açmadı"* hâli hiçbir CI'da görünmez — kardeş CI'ı ancak kardeş depoda bir PR açılınca koşar. İki kapatma yolu: (i) kardeş `contracts_gate.yml`'lara `schedule: cron` (haftalık) eklemek, (ii) C8 öncesi yerel koşumu zorunlu tutmak (bugünkü hâl, `SDLC_GATES §3C`). **Bugün (ii) yürürlükte**; (i) E17/W10 ile birlikte değerlendirilir | Bu boşluk PAT seçeneğinde de vardı (checkout kardeş `main`'i görürdü) — yani karar bir gerileme değil | plan §14.7 |
| ✅ **D5** | `test_real_repo_checksum_verifies` → `release_gate` + `xfail(strict=True)`; koşul **makine-okunur beyandan** okunuyor: `CONTRACTS_VERSION.md` → `**Checksum State:** PENDING_REPIN`. Aynı beyanı **üç kapı** okuyor (CI checksum işi · pin testi · `PENDING_PROPAGATION` testi) ve `pin_version.py` dosyayı baştan ürettiği için **C8'de kendini siler** → üç kapı aynı anda sertleşir. `-m "not release_gate"` `tests/conftest.py` tarafından **reddediliyor** (exit 4) | ✅ | Q1, Ç6, SD4 | `tests/release_state.py`, `tests/test_pin_version.py`, `pyproject.toml`, `CONTRACTS_VERSION.md` |
| ✅ **D6** | SDLC_GATES §3A'ya *"PENDING_REPIN kalkmış olmalı"* · §3C'ye **`PENDING_PROPAGATION` boş** kapısı (checklist maddesi değil **test**: `test_pending_propagation_is_empty`, tur içi xfail → release'de gerçek kırmızı) + *"parite CI'da koşmaz, C8'de yerel koş"* · §3E'ye `-rs`/skip-0/xfail-0/deselect-yok + dedektör çıkış kodu sözleşmesi · **yeni §3G: annotated tag töreni** (`git tag -a` + `%(objecttype)`=`tag` doğrulaması + `git describe` + push) | ✅ | SD7, SD8 | `docs/checklists/SDLC_GATES.md`, `tests/test_vendored_parity.py` |

**Kapıların mutasyon kanıtı (hepsi bu oturumda koşuldu):** ① `escalation_reason`'dan `QUARANTINE_CAUTION`
silindi → dedektör **BREAKING** dedi, CI kapısı *"beyan edilmemiş breaking"* ile düşürdü (eskiden 0 breaking)
② eski dedektörle yeni süit **21/25 düşüyor** ③ `PENDING_REPIN` beyanı silindi → pin + propagation testleri
**gerçek kırmızı** ④ beyansız `pytest.skip("pyyaml yok")` → oturum **RC=1** ⑤ `-m "not release_gate"` → **RC=4**
⑥ KR-093 tanımı iki kaynaktan silindi → **3 test kırmızı**; `## KR-093`→`### KR-093` biçim değişimi ise
**yanlış alarm üretmedi**.

## 14.1 KADEME 1 — Geri alınamaz + maliyet penceresi kapanıyor — ✅ **contract yarısı TAMAM (2026-07-31)**

> **Durum:** D7/D8/D9'un **contract** kalemleri yapıldı · süit **790 geçti / 2 beyanlı xfail / 0 skip** ·
> dedektör **0 breaking** · her kapı mutasyonla doğrulandı (kanıt aynı denetim dosyasına eklendi).
> ⚠️ **D7'nin EDGE KODU yarısı açık** (aşağıda **E15**) — ayrı depo, ayrı PR.

| # | İş | Durum | Kapatır |
|---|---|---|---|
| ✅ **D7** | **Ç7 tek hamle — contract yarısı.** `raw_frames[].footprint_wkt` **KALDIRILDI** → **`sees_patch_ids[]`** (`minItems:1`, `maxItems:500`, `^[a-f0-9]{32}$` — desen `priority_zones.patch_id` ile **test tarafından bağlandı**) ve **`required`'a girdi**: KG-0.c gereği bir karenin listede olmasının tek meşru gerekçesi budur · `observed_footprint_wkt` **KALDI** + `maxLength:4096` + **desen** (EWKT RED · `POLYGON/MULTIPOLYGON` şart · tam kısmı 4+ basamaklı koordinat RED = *"\|koordinat\|>180 ⇒ derece değil"* ayırıcısı; ondalık hassasiyet serbest — 8 vakayla doğrulandı) · **`footprint_crs`** (`const: EPSG:4326`) eklendi · **`crs_mismatch` bağlandı:** `qc_report.flags[]` serbest dizeden **kapalı vocabulary'ye** çevrildi (5 değer; kaynak: üreticinin fiilen yazdığı bayraklar, `qc_report_writer.py:157-165`) · `raw_frames.maxItems` 5000→**8000** (D11/E6 buraya alındı: 25 m uçuş 5.229 kare) | ✅ | E7, G2, K7, P3, **G1**, Y2, (E6) |
| ⬜ **E15** 🔴 | **D7'nin EDGE KODU yarısı (bu depoda YAPILAMAZ):** `qc_report_writer._geometric_coverage` → `min(...,1.0)` kırpması **kaldırılır** (oran ≫1 = CRS uyuşmazlığı; kırpma onu *"kusursuz kapsama"* yalanına çeviriyor) · iki `except → 0.0`/`pass` yolu **fail-loud** olur · `footprint_crs` okunur, uyuşmazlıkta `crs_mismatch` bayrağı yazılır. **Kanıt:** `qc_report_writer.py:245-289` · **KR-065 ödeme** kararı bu değere bağlı | ⬜ | G1 (kod yarısı) |
| ✅ **D8** | **C6a — fail-open kapatıldı.** Enum'un global *"eksikse PANEL_ABSOLUTE varsay"* güvenlik-ağı **kaldırıldı**, yerine **bağlam-bazlı `missing: {policy: FAIL-CLOSED}`** kondu (5 bağlam ayrı ayrı yazılı) · `platform/calibrated_dataset_manifest` alt-kümesine **`NONE`** eklendi (dürüst değer yazılabilsin diye) · `hard_reject: [NONE]` korundu. ⚠️ **Ölçümle çözülen çelişki:** C1′ turunda yazılan `test_none_is_excluded` **tam tersini** iddia ediyordu; ölçüm kuralın **canlı kodda** olduğunu gösterdi (`worker_job_publisher.py:80-84` → *"status CALIBRATED → PANEL_ABSOLUTE (güvenlik-ağı)"*) ve aynı fonksiyonun 4. adımının **zaten NONE ürettiğini** — yani NONE sistemde akıyordu, yalnız kalibre manifestte yazılamıyordu. Test gerekçesiyle **tersine çevrildi**. **Edge alt-kümesi bilerek DAR bırakıldı** (edge kalibrasyon başarısızsa manifest üretmez — `calibrated_validator` CHECK 2) → bileşim kararı **C6b/E13**'te | ✅ | S1 |
| ⬜ **P14** 🔴 | **D8'in PLATFORM yarısı:** `worker_job_publisher.py:80-84` üçüncü adım (`status CALIBRATED → PANEL_ABSOLUTE`) **kaldırılmalı**, tip yoksa **`NONE`** yazılmalı. Contract artık bunu normatif olarak söylüyor (`x-normalization.missing.policy = FAIL-CLOSED` + `x-superseded-2026-07-31.consumer_obligation`) | ⬜ | S1 (kod yarısı) |
| ✅ **D9** | **Ç5 zinciri tamam.** ① **`x-layer-classes`** eklendi (`raster_product` / `index` / `composite` / `derived_metric` + 13 değerin haritası) ② **`IRRIGATION_EFFICIENCY` → `CANOPY_TEMP_UNIFORMITY`** (şema enum'u **ve** matris; ölçüldü: kardeş depoların hiçbirinde geçmiyor → **bedava**; termal kamera sulama *verimliliğini* ölçemez — uygulanan su + bitki su tüketimi gerekir, ikisi de sistemde yok) ③ **`index_requirements`** matrise eklendi — ⚠️ **bant gereksinimleri uydurulmadı, worker'ın FİİLİ formüllerinden ölçüldü** (`feature_extraction.py:207-222`): SAVI **Blue GEREKTİRMEZ**, EVI **gerektirir** (kod: B yoksa EVI sıfırlanır) · `CHLOROPHYLL_A` **`null` bırakıldı** (formülü depoda tanımlı değil; worker'daki `LCI` **aynı ad değil**) → §14.5'e açık kalem ④ **14 testlik kapı**: her `layer_type`'ın sınıfı var · matris↔şema vocabulary'si bağlı · **listelenen her indeks üretilebilir** (mutasyon: 4 bantlı Mavic'e EVI eklenince kırmızı) · eski ad **değer olarak** geri gelemez (tarihsel not korunur) | ✅ | A8, A10, S10, S11, Y4 |
| ✅ **D3-c** 🆕 | **KADEME 1'de doğan dedektör boşlukları (aynı sınıf, bu turda kapatıldı):** ① serbest bir alana **`enum` EKLEMEK** daraltmadır ama hiç görünmüyordu (`ENUM_CONSTRAINT_ADDED`) ② **`x-normalization` gibi normatif `x-` blokları** doğrulamayı değiştirmez ama tüketici KODUNU değiştirir — D8'in fail-open→FAIL-CLOSED çevirisi klasik şema diff'inde **görünmezdi** → `NORMATIVE_ANNOTATION_CHANGED` (*manual review required*; `x-updated` bilerek kapsam dışı) ③ yeni bağlam alt-kümesi eklemesi raporlanmıyordu. **Ayrıca `x-compat-accepted`:** biçimsel daraltmayı **beyanla** NON_BREAKING'e indirir (gerekçe raporda yankılanır) — kapsam DAR: alan silme · enum değeri silme · `required` genişletme · tip daraltma **asla** indirilemez (5 test) | ✅ | (denetimde yoktu) |
| ⬜ **D4-c** 🆕 | **Kapı kapsamı boşluğu:** `drone_capability_matrix.yaml` **normatiftir** (KR-018/030 bant kapısı) ama ne checksum ağacında (`schemas/`+`enums/`+`api/`) ne de breaking dedektöründe (`schemas/`+`enums/`) — yani sürüm bump'ı olmadan sessizce değişebilir. C-SSOT-2 ile **aynı sınıf** (SSOT metni de kapsam dışı). D9'un testi matris↔şema vocabulary'sini bağladı, ama sürümleme boşluğu duruyor → checksum ağacına mı alınacak, salt-okunur drift dedektörüne mi? | ⬜ | (denetimde yoktu) |

## 14.2 KADEME 2 — C8 sıralama kilitleri — ✅ **iş kalemleri TAMAM (2026-07-31)**

| # | Kilit / iş | Durum |
|---|---|---|
| ✅ **D10-E2** | **C11 yapıldı: `sorties[]` + `mission_date` kanoniğe absorbe edildi.** ⚠️ **Ölçüm iddiayı doğruladı:** edge'in `intake_manifest_valid.json` fixture'ı kanoniğe karşı **2 hata** veriyordu ve ikisinin de tek sebebi bu ikisiydi (`oneOf` hiçbir dala uymuyor → `unevaluatedProperties: false` her alanı reddediyor). Yani edge'in **gerçek çıktısı** kanonik sözleşmeye göre geçersizdi. Absorpsiyondan sonra fixture (ürün adları kanonikleştirilerek) **hatasız geçiyor** — test bunu kardeş depo varken fiilen doğruluyor. Dizi opsiyonel (MINOR), sortie varsa `bbox` zorunlu (eski C4'ün cevabı) | ✅ |
| ⬜ **E16** 🔴 | **Edge ürün sözlüğü hizalaması — KAPSAM GENİŞLEDİ (AK-7 ile).** Edge üç yerde küçük harf yazıyor: ① `sorties[].crop_type` (C11 absorpsiyonu kanonik biçimle yapıldı) ② vendored `worker_result.v1.crop_type` enum'u (`cotton…`, 5 değer) ③ fixture'lar (`worker_result_valid.json:6` → `"cotton"`). Kanonik taraf artık **beş alanda da** BÜYÜK harf zorluyor. **Ölçülen kalan fark tam olarak budur:** edge fixture'ı bugün tek ve net bir hata veriyor — `'cotton' is not one of ['COTTON', …]`. Edge C8'de: üretici eşlemesi + vendored yenileme + fixture güncellemesi. ⚠️ **SIRA KİLİDİ:** platform `worker_result_schema_enforce` (P1) **edge hizalanmadan AÇILMAZ** — açılırsa edge çıktısı runtime'da reddedilir | ⬜ |
| ✅ **D10-E1** | **C2″ hükmü DÜZELTİLDİ** — §3.1'deki satır yeniden yazıldı: *edge regex DEĞİŞMEZ.* Eski hüküm (`priority_zone.py:31,55` regex'ini `object_key` için genişlet) uygulansaydı **`ManifestWriter` kendi ürettiği manifesti reddederdi** (edge göreli yol üretir, anahtarı platform üretir — KG-0.a-EK kural 1) | ✅ |
| ⬜ **D10-E4** | **KİLİT (iş değil, SIRA): E11 C8'den ÖNCE merge EDİLMEZ.** Gerekçe: `additionalProperties:false` → edge CHECK 1 → `REJECTED_QUARANTINE` ve **geri dönüşü yok**. E11 (kare seçici) yazıldığında C8 tamamlanmış olmalı | ⬜ *(kilit aktif)* |
| ✅ **D10-E3** | **`$ref` kararı YAZILDI** → §14.2.1. Ölçüm: kanonik `intake_manifest` **3 harici `$ref`** taşıyor (`drone_type`, `threat_type`, `dataset_status`), vendored kopyalarda **0** (satır içi) → air-gap M1'de `Unresolvable`. Karar taslağı + gerekçe aşağıda; **uygulama C8'de** | ✅ *(karar)* |
| ✅ **D11-E5** | **`relative_path` deseni gerçek çıktıyı kabul ediyor.** Eski desen ölçümden ÖNCE dondurulmuştu ve M1'in **fiilen ürettiği** dosyaları reddediyordu: `odm_orthophoto.original.tif` (ODM'nin gerçek adı), `layers/ndvi.tif.aux.xml` (GDAL yan dosyası), boşluklu (`Tarla Verileri/…`) ve Türkçe (`kırmızı/…`) klasörler. Yeni desen bunları kabul ederken **traversal korumasını korur** (mutlak yol · `..`/`.` segmenti · boş segment · `\` · `:` · kontrol/glob karakterleri) — **13 vakayla** doğrulandı | ✅ |
| ✅ **D11-E6** | `raw_frames.maxItems` **5000 → 8000** (25 m uçuş 5.229 kare + pay). **D7 commit'inde** yapıldı | ✅ |

### 14.2.1 🔒 KARAR TASLAĞI — E3: harici `$ref`'ler C8'de ne olacak? *(onay bekliyor)*

**Ölçüm.** Kanonik `schemas/edge/intake_manifest.v1.schema.json` üç harici referans taşıyor:
`../../enums/drone_type.enum.v1.json` (satır 56) · `../../enums/threat_type.enum.v1.json` (183) ·
`../../enums/dataset_status.enum.v1.json` (197). Edge/worker'ın **vendored kopyalarında bu
referanslar YOK** — değerler satır içi. Yani sözleşme iki biçimde yaşıyor ve M1 (hava-boşluklu,
internet yok) kanonik biçimi **çözemiyor** (`Unresolvable`).

**Seçenekler.**
| | Yaklaşım | Artı | Eksi |
|---|---|---|---|
| **A** | **Yayında `$ref`'leri INLINE et** (C8 çıktısı tek-dosya şema) | M1'de ek altyapı gerekmez · vendored kopyalarla **aynı biçim** (parite kapısı gerçek parite ölçer) · air-gap sorunu tamamen biter | Enum değişince şema da yeniden yayımlanmalı (C8 zaten tören) · dosya büyür |
| **B** | **Yerel Registry** (tüketici enum dosyalarını yanında taşır, `$ref` korunur) | Tek kaynak korunur, kopya yok | Her tüketicide çözücü kurulumu · M1'de dosya yerleşimi kırılırsa **sessiz** `Unresolvable` · bugünkü sapmayı sürdürür |

**ÖNERİ: (A) inline** — çünkü ① vendored kopyalar zaten inline, yani (A) sapmayı **kapatır**,
(B) ise iki biçimi kalıcılaştırır ② air-gap M1'de en az hareketli parça ③ enum'ların kendisi
`enums/` altında **kanonik kaynak olarak kalmaya devam eder** (inline yalnız YAYIN biçimidir).

**Şartlar (uygulama C8'de):** ① inline üretim **araçla** yapılır (elle kopyala-yapıştır YASAK)
② üretilen dosyada `x-inlined-from` izi bulunur ③ bir test inline değerlerin kanonik enum'la
**birebir** olduğunu zorlar (C-PARİTE deseninin aynısı) ④ enum değişince yeniden üretim
release checklist'ine (§3G) girer.

**Onay:** ✅ **KOORDİNATÖR ONAYLADI ve UYGULANDI (2026-07-31).**
⚠️ **Ölçüm E3'ü düzeltti:** sorun 3 referans değil, **38 harici `$ref` / 23 dosya / 13 enum** (E3 yalnız `intake_manifest`e bakmıştı). **Uygulama:** `tools/inline_refs.py` — kaynak DRY kalır (`$ref` korunur), `dist/schemas/` **kendi kendine yeten yayın biçimini** üretir (68 dosya, harici ref **0**, 38 düğümde `x-inlined-from` izi). Satır içi alınan anahtarlar bilerek DAR: yalnız doğrulama anahtarları (`$id`/`metadata` taşınmaz — `$id` kopyalamak aynı kimliği iki yerde tanımlardı). **Kapılar:** 7 test — harici ref kalmadı · her düğümde iz var · satır içi ≡ kanonik enum · bayat `dist/` kırmızı. Mutasyon: enum'dan değer silinince üretilen düğüm değişiyor; `dist/` elle bozulunca `--check` RC=1. `.gitignore`'a **bilinçli istisna** (`dist/schemas/` izlenir — izlenmezse C8'de gönderilecek artefakt olmaz).

## 14.3 KADEME 3 — Denetim aletini onar — ✅ **TAMAM (2026-07-31)**

> **Tema:** ölçüm aracı, ölçtüğü sistemi DEĞİŞTİRMEMELİ. Dördü de aynı şemada
> (`schemas/worker/expert_review_queue.v1.schema.json`), tek `allOf` bloğunda ve
> **28 davranış testiyle** (`tests/test_audit_measurement_integrity.py`) bağlandı.
> Dedektör: 0 breaking (bileşim eklemesi **beyanlı**).

| # | İş | Durum |
|---|---|---|
| ✅ **D12** | **M2:** yeni `consensus_participation` alanı — denetim satırında **`EXCLUDED` zorunlu** (kör uzmanın etiketi yayın kapısını bloke edemez; denetim etiketi denetlediği kararın parçası olamaz) · **M3:** `tile_id` denetim satırında **zorunlu ve null olamaz** — `analysis_result.detections` bir DİZİ olduğu için `job_id` JOIN'i hangi tile'ın denetlendiğini söylemiyordu, yani `propagation_precision` hesaplanamıyordu · **M4:** denetim satırında `tile_group_id: const null` + `tile_group_size: const 1` — toplu onay yayılımı, denetim etiketini kendi ölçtüğü yayılıma besliyor ve isabeti **yapısal olarak 1'e** çekiyordu | ✅ |
| ✅ **D13** | **M1/Y1:** `audit_selection_rate` (π_h, `0 < x ≤ 1`) + `audit_rotation_key` + `audit_bucket` — üçü de denetim satırında **zorunlu**. Tabaka etiketi tek başına yansız kestirim vermez; Horvitz-Thompson her gözlemi `1/π_h` ile ağırlıklar. ⚠️ **BİLİNÇLİ SAPMA:** plan *"`audit_stratum` opak dize kalsın"* diyordu; **yapı KORUNDU** çünkü ölçüldü — `crop_type`/`analysis_type` eksenleri kanonik enum'larla birebir eşleşiyor, onları dizeye çevirmek bilgi kaybı olurdu. Tartışmalı olan tek eksen **fenoloji** (A5/A6: contract enum'u 8 ürünün 3'ünü kapsıyor, edge takvimi ayrı sözlük) → **opsiyonel kaldı ve zorunlu yapılması test ile YASAKLANDI** (`test_phenology_axis_is_not_required`) | ✅ |
| ✅ **D14** | **Ç1:** öncelik kuralı sözleşmeye normatif olarak yazıldı — *"denetim çekilişi ÖNCE ve modelden bağımsız; çakışmada `audit_sample` kazanır"* + yeni `spot_check_suppressed` bayrağı + denetim satırında `required_reviewers: const 1` (inceleme yükü tabakalar arasında değişip ölçümü kirletmesin) | ✅ |
| ✅ **D15** | **Ç4 adım 1:** denetim satırında `confidence_score: const 0` (anti-anchoring — model güveni tel üzerinde bilgi taşımaz) + **`x-deprecated-in-context`** beyanı (bağlam · tarih · politika · **2-MINOR penceresi** · gerekçe · M2/M3 bağımlılığı). Alan `required` olduğu için KALDIRILAMAZ (o MAJOR olurdu) → bağlam-bazlı sabitlendi | ✅ |
| ✅ **D3-d** 🆕 | **KADEME 3'te doğan dedektör körlüğü:** *hiç yokken* bileşim kısıtı eklemek (`allOf`/`oneOf`/`anyOf`/`prefixItems`) **raporlanmıyordu** — iki tarafta da liste şartı arandığı için `expert_review_queue`'ya eklenen **5 blok** "0 değişiklik" görünüyordu. `ENUM_CONSTRAINT_ADDED` ile aynı sınıf. Kapatıldı + 5 test. Bu turun bloklarına beyan yazıldı: ölçüldü, **5 bloğun 5'i de** `audit_sample`/`AUDIT_SAMPLE` koşullu ve o alanlar aynı yayımlanmamış turda eklendi ⇒ eski belgelerde `if` hiç ateşlenmez | ✅ |
| ⬜ **W8** 🔴 | **KADEME 3'ün worker yarısı:** `audit_set_sampler` π_h/bucket'ı **zaten hesaplıyor** ama emisyon kodu yazılmadı (M1/P4: *"kayıp değil, hiç bağlanmamış"*). Worker denetim satırını üretirken artık zorunlu olan altı alanı (`tile_id`, `consensus_participation`, π_h, rotation, bucket, `confidence_score: 0`) yazmalı; platform konsensüs yolu da `EXCLUDED` satırı saymamalı (**P16**) | ⬜ |

## 14.4 KADEME 4 — Normatif kaynak tekilliği — ⚠️ **kısmen TAMAM (2026-07-31)**

| # | İş | Durum | Kapatır |
|---|---|---|---|
| ⚠️ **D16** | **Ç8 paketi — üç parçası yapıldı, GÖÇ parçası koordinatör kararına bırakıldı.** ✅ **Tekil-gövde kapısı** kuruldu (`tests/test_single_normative_body.py`): ölçüldü — **50 KR'nin gövdesi İKİ kaynakta birden** (SSOT metni 51 · registry 54 · birleşim 55). "İkili gövde yasak" diyen bir test 50 yerde düşer ve ilk işi devre dışı bırakılmak olurdu; bu yüzden borç **donduruldu** — liste yalnız KÜÇÜLEBİLİR, yeni ikili gövde kırmızı verir. ✅ **`stress_ratio`** artık **beyanlı** (`analysis_type → metadata.indexDefinitions`): durum `UNDEFINED_PENDING_DECISION` + neden tahmin edilmediği + neyin beklendiği yazılı (A3: 3 atıf / 0 tanım doğrulandı). ✅ **CLAUDE.md "sayı değil üretici"**: sabit sayılar yerine **çalışan komut** kondu (aynı bölüm iki kez bayat sayı yüzünden yanlış teşhise yol açmıştı). ⬜ **KALAN:** KR-093'ün 10 satırlık (SSOT metni) ve 98 satırlık (registry) **iki gövdesinin birleştirilmesi** + `kr_registry.md`'nin türetilmiş dizine indirilmesi | ⚠️ kısmi | AR1, AR3, **A3**, Q5 |
| ✅ **D16-b** | **KARAR VERİLDİ ve UYGULANDI (2026-07-31): normatif gövde = SSOT metni; registry işaretçi tutar.** ⚠️ **İlk gerekçem ÖLÇÜM HATASIYDI** — *"registry yalnız contract'ta yaşar"* demiştim; sığ bir `ls` yüzünden yanlış. Gerçek: registry'nin platform (`docs/kr/`, `contracts/ssot/`) ve worker (`docs/reference/`) kopyaları VAR. **Ama asıl ölçüm kararı yine aynı yöne çıkardı:** o üç kopyanın **hiçbirinde KR-093 başlığı yok** (1211/1242/936 satır), SSOT metninin platform kopyası da farklı (1906 ↔ 1895) — yani **her iki dosyanın da alt-akış kopyaları bayat**. Belirleyici fark **senkron MEKANİZMASI**: SSOT metni C-SSOT'ta bayt-özdeş hâle getirildi + kapısı var; `kr_registry.md` **hiçbir senkron aracının kapsamında değil** (C-SSOT-2). Tutulamayan kaynağı normatif ilan etmek çürümeyi kurala çevirir. **Uygulama:** KR-093'ün registry gövdesi (99 satır) → 24 satırlık işaretçi; registry'ye özgü iki MUST (*Aşama A tespit değildir* · *yeni faz eklenmez*) + Aşama A içerik listesi SSOT metnine **taşındı** (kayıpsızlık testle zorlanıyor). Borç **50 → 49** | ✅ | AR1, AR2 |
| ⬜ **D16-b2** 🔴 | ~~KOORDİNATÖR KARARI — hangi kaynak normatif kalacak?~~ **Kalan 49 KR'nin göçü.** SSOT metni **çapraz-repo** artefakttır (platform kopyasıyla bayt-özdeş, C-SSOT); registry yalnız contract'ta yaşar ama **8 bölümlü tam gövdeleri** o taşıyor (KR-093: 98 satır vs 10 satır). Karar verilmeden gövde taşımak **normatif içerik kaybı** riski taşır — bu yüzden bu turda YAPILMADI. Karar sonrası: göç + `kr_registry.md` → türetilmiş dizin + üretici araç + `KNOWN_DUAL_BODY_COUNT` düşürülür | ⬜ | AR1, AR2 |
| ⬜ **D16-c** | **K3/K5 — saklama ve rıza MUST'ları** KR-093 gövdesine eklenecek (üç yeni veri kategorisi KR-090 saklama politikasının dışında). **Bilerek ertelendi:** yeni normatif içeriği ŞİMDİ eklemek, birleştirilecek iki gövdeden hangisine yazılacağı belirsiz olduğu için göçü zorlaştırır → **D16-b'den SONRA** | ⬜ | K3, K5, Y6 |
| ✅ **D17** | **A1 zinciri — üç kaynağın çeliştiği ölçülerek doğrulandı:** plan **KG-0.f** *"gerçek WATER_STRESS için CWSI (termal) veya NDWI/NDMI (SWIR) gerekir, **ikisi de yok**"* diyor ↔ `analysis_type` `availability: available` diyordu (yalnız 4 bantla) ↔ `report_phase.stage_b` katmanı **uzman kapısı ÖNCESİNDE** çiftçiye teslim ediyordu. **Yapılan:** `WATER_STRESS.availability` → **`proxy_only`** (yeni, additive değer + `proxy_basis`: doğrudan ölçüm LWIR/SWIR ister, 4 bantla hesaplanan "NDWI" McFeeters **su kütlesi** formudur, Gao bitki-suyu formu değil) · **`stage_b`'den çıkarıldı** · **A2:** changeNote KG-0.f'i artık **eksiksiz** alıntılıyor (eski not BENEFICIAL + THERMAL_STRESS'i sayıp WATER_STRESS'i atlıyordu — seçici alıntı). **Sınıf kapısı:** `proxy_only` işaretli HİÇBİR katman ön fazda sunulamaz (tek katman değil, kural). ⚠️ C9'un *"stage_b değişmez"* testi gerekçesiyle daraltıldı: §14'ün öncelik sırasında **① fiziksel/ölçüm geçerliliği**, ⑥ mimari tutarlılığı yener | ✅ | A1, A2 |
| ✅ **D18** | **K4 — `api/` ağacı artık taranıyor.** Ölçüldü: `validate.py` yalnız `schemas/`+`enums/`, CI grep'i yalnız `schemas/` tarıyordu ⇒ **kimlik yüzeyini tanımlayan `api/` hiçbir PII kapısından geçmiyordu** — oysa `SDLC_GATES §1B` *"hiçbir şema/enum/**API alanında**"* diyordu (sözleşme kendi iddiasının gerisindeydi). **İlk taramada gerçek isabet:** `api/platform_public.v1.yaml → $.info.contact.email`. **Kapsam-duyarlılık:** `phone` yasak değil (kimlik modelinin kendisi) ama yeri belli — `user_pii.v1` + auth yüzeyi dışında **hata**; `phone_verified` gibi türev adlar etkilenmez (tam ad eşleşmesi). `pyproject.toml` yasak listesi **3 → 6** değere hizalandı (araçla ayrışmıştı) ve ayrışma testle yasaklandı | ✅ | K4 |
| ✅ **D18-b** | **UYGULANDI: adres SİLİNDİ, kapı İSTİSNASIZ.** Gerekçe ölçümle: diğer iki spec'te künye bloğu **hiç yok** (0 eşleşme) · OpenAPI 3.1'de `info.contact` **opsiyonel** · adres depoda **başka hiçbir yerde** geçmiyordu · kimlik modeli telefon+PIN. `METADATA_EXCEPTIONS` **boşaldı** ve testi *"liste BOŞ olmalı"* biçiminde sertleştirildi + adresin geri gelmesini yasaklayan regresyon kapısı. Mutasyonla kanıtlandı: adres geri konunca hem `validate.py` hem testler düşüyor | ✅ | — |

## 14.5 KADEME 5 — SONRAYA (karar bu tur, uygulama sonraki)

> ### 📍 KADEME 5 ilerleme (2026-07-31)
> **Bu depoda yapılabilir olan iki kalem YAPILDI** (aşağıda ✅); kalanların hepsi ya
> **başka depoya** ya **E13/motor kararına** ya **agronomi kararına** bağlı — bilerek
> açık bırakıldı, her biri için engelin NE olduğu yazıldı.

| # | Kalem | Durum | Engel / gerekçe |
|---|---|---|---|
| ✅ **G3/G4** | **`priority_zones[].geom` koordinat sınırları.** Ölçüldü: şema UTM METRE (`[500000, 4000000]`), enlem 91 ve boylam −181'i **kabul ediyordu** → yanlış CRS'teki poligon sözleşmeden geçip `ST_SetSRID(…,4326)` ile **yanlış damgalanıyordu** (G4). Artık `prefixItems` ile `[boylam ±180, enlem ±90]` zorlanıyor — D7'deki WKT derece ayırıcısının GeoJSON karşılığı (aynı kural, iki gösterim). EdgeForm master'da var olduğu için daraltma **beyanlı** (`x-compat-accepted`). ⚠️ **Şemanın zorlayamadıkları AÇIKÇA yazıldı** (halka kapanışı · papyon · halka yönü — JSON Schema bunları ifade edemez) ve iki test bu sınırı **regresyon kaydı** olarak tutuyor: kapı gördüğünü iddia etmiyor | ✅ | — |
| ✅ **K2** | **Veri yönetişimi kararı (yeni 0.h)** — taslak §9'a değil buraya, karar tablosuna yazıldı (aşağıda) | ✅ taslak | Onay bekliyor |
| ✅ **S5** | **CONTRACT YARISI YAPILDI (2026-08-01, TUR 2).** Teşhis ölçümle netleşti: alan **yalnız platform** şemalarındaydı; worker'ın vendor'ladığı 8 sözleşmenin ve kanonik `schemas/worker/*`'ın **hiçbirinde** yoktu → worker ölçeği **tüm filo için tek global env**'den okuyor (`src/shared/config.py:236` = `10000.0`). 🔴 **Worker kodu bunu zaten biliyor ve düzeltmeyi kendisi tarif ediyor:** *"The canonical fix is a per-job scale field in the calibration contract"* (`config.py:230-234`) · *"Kalıcı çözüm: per-job reflectance_scale'i calibration_metadata sözleşmesine ekleyip okumak"* (`pipeline.py:2358`). Yapılan: `worker/calibration_metadata.v1`'e opsiyonel `scale` bloğu (`reflectance_scale` enum + `scale_factor`), **platform'daki tanımla birebir aynı adlar** (yeni ad icat edilmedi) + `scaled_int` için `if/then` bölen zorunluluğu + `x-normalization.scale.missing` = `DECLARED_FALLBACK` (I-5: geçici; üretici yazınca `FAIL_CLOSED`). Kapı: `tests/test_reflectance_scale_contract.py` (11 test, **5/5 mutasyon** kırmızı) | ⬜→✅ | Yeni tur açıldı: `PENDING_REPIN` + `PENDING_PROPAGATION[calibration_metadata]` |
| ⬜ **W12** 🟠 | **S5'in WORKER yarısı — okuma kodu.** Sözleşme alanı eklendi ama worker hâlâ global env okuyor. Yapılacak: `calibration_metadata.scale`'i job başına oku, yoksa `settings.reflectance_scale`'e düş **ve bunu logla** (beyan `DECLARED_FALLBACK` diyor). ⚠️ Yayılım (vendored kopyaya alan taşıma) **okuma kodu hazır olmadan yapılmamalı** — alan ölü taşınır. Bugünkü tek savunma doyum alarmı (`pipeline.py:2364`), bir kapı değil. İlgili: **W2** (ölçek motor başına — E13 ile motor artık belli: Pix4Dfields) | Worker deposu | S5 · `PENDING_PROPAGATION` beyanı |
| ~~⬜ S5 (eski tanım)~~ | ~~`scale_factor` — reflektans ölçeği taşınmıyor; **EVI/SAVI'yi sessizce bozar, NDVI gizler**~~ (NDVI orandır → ölçekten bağımsız; EVI'nin `+1`/`6R−7.5B` ve SAVI'nin `+L` toplama sabitleri ölçeğe DUYARLIDIR). Ölçüldü: alan yalnız `schemas/platform/calibration_result.v1.schema.json:69`'da var, indeks üretim yoluna **bağlı değil** | ⬜ | **E13** (hangi motor → hangi ölçek) kararına bağlı; plan bunu "E13'ün hemen ardından ilk sırada" diye işaretlemiş |
| ✅ **C6b/S2 · S4 · S6** | **YAPILDI (2026-08-01, TUR 2 — hepsi MINOR).** **C6b/S2:** `edge/calibrated_dataset_manifest` alt-kümesine `PANEL_ABSOLUTE` eklendi — intake dört değer kabul ederken kalibre manifest ikisini kabul ediyordu, yani paket intake'te panel bildirip **aynı istasyonun ikinci belgesinde** yazamıyordu. 🔴 **İlk deneme tam hizalama yaptı ve kendi E13 kapım (`test_calibration_type_axis.py`) onu kırmızıya çevirdi** — aynı gün verilen iki kararın çelişmesini kapı engelledi; hizalama kısmi yapıldı (`DLS2_RELATIVE` E13 gereği dışarıda, `NONE` D8 gereği). **S4:** `calibration_method` platform/edge/datasets/events'te vardı ama **worker'ın yüzeyinde yoktu** (S5 ile birebir aynı desen) → `worker/calibration_metadata.v1`'e eklendi, sözlük `calibration_certificate`/`edge/calibration_result` ile aynı. **S6:** `outputs[]` heterojen (DSM metre · CWSI birimsiz · 8-bit ORTHO), tek paket-ölçeği yetmiyordu → `file_artifact.reflectance_scale` eklendi, paket düzeyi **varsayılan** oldu | ⬜→✅ | dedektör: 6 değişiklik, **0 breaking** · 1048 test yeşil |
| ⚠️ **S7** | **YARIM YAPILDI (MINOR yarısı).** `raw_frames[].band` enum'una **`RGB`** eklendi → kompozit kare artık AÇIKÇA işaretlenebilir. Önceden bunu ifade etmenin tek yolu alanı boş bırakmaktı; yokluk **iki şeyi** kodluyordu (RGB kompozit / bant bilinmiyor). ⚠️ `RGB` kanonik `available_bands`'e **sızdırılmadı** (kare türü, bant değil — yoksa KR-018 bant kapısı 4-bant minimumunu RGB ile sağlanmış sanardı) | ⬜→⚠️ | `test_raw_frame_band_matches_canonical` genişletildi |
| ⬜ **S7-b** 🟡 | **S7'nin MAJOR yarısı:** `band` hâlâ **opsiyonel** → yokluk hâlâ belirsiz. Zorunlu kılmak `FIELD_MADE_REQUIRED` = MAJOR. Üretici yok (ölçüldü: `raw_frames` için üç depoda 0 eşleşme; E11 yazılmadı) yani pratikte kimseyi kırmaz — ama **beyanla geçirilemedi**, bkz. AK-11 | **MAJOR penceresi** — S3 ve K1 ile aynı tur | S7 |
| ⬜ **AK-11** 🟡 | **Dedektör beyan desteği TUTARSIZ (ölçüldü 2026-08-01).** `tools/breaking_change_detector.py` `x-compat-accepted` beyanını kısıt daraltmalarında (pattern/maxLength/enum) tanıyor ve `ACCEPTED TIGHTENING (declared)` olarak indiriyor; ama **`FIELD_MADE_REQUIRED` yolunda beyanı hiç kontrol etmiyor** (satır 615-630). Sonuç: "üretici yok, ölçüldü" gerekçesi bu değişiklik tipinde işlemiyor ve S7-b MINOR turunda yapılamadı. Ya beyan desteği bu tipe genişletilir, ya "required daraltması beyanla geçilemez" **yazılı** kural olur | AK-2/AK-3 ailesi (dedektör sınırları) | S7-b'nin doğrudan engeli |
| ⬜ **S3** 🔴 | **`DLS2_RELATIVE` satıcıya özgü ürün adı** — DLS2 bir **MicaSense** parçasıdır (SSOT KR-018: *"MicaSense RedEdge-P/Altum-PT: DLS2 + reflectance panel"*); M3M'de güneş sensörü var ama **DLS2 değil**. E13 kararı bu değeri kalibre paket yüzeyinden zaten reddetti, ama enum'dan **kaldırmak/yeniden adlandırmak** ayrı iş: enum değeri yeniden adlandırma = **MAJOR** + migration guide + üç tüketici re-pin | **MAJOR penceresi** — K1 `{tenant}` ve S7-b ile aynı tur | E13 · denetim §Sensör |
| ⬜ **K1** | `{tenant}` opaklaştırma | ⬜ | **MAJOR** — bu tur MINOR; sürüm penceresi kararı |
| ✅ **K3** | Saklama politikası MUST'ları | ✅ | **KAPANDI (2026-08-01, 0.h ile).** D16-c beklenmedi: KR-090 gövdesi zaten registry'de yaşıyor (D16-b2 ölçümü — SSOT metninde 0 kez geçiyor), MUST 9-12 oraya yazıldı ve `test_data_governance.py` ile zorlandı |
| ⬜ **P1** | Çalışma zamanı zorlaması (Pydantic + `enforce=True`) | ⬜ | **platform deposu** · ⚠️ **SIRA KİLİDİ:** edge ürün sözlüğü hizalanmadan (E16) açılırsa edge çıktısı runtime'da reddedilir |
| ⬜ **A5/A6 · A7** | Fenoloji eşlemesi · kanopi maskesi | ⬜ | **Agronomi kararı** — kaynak Bakanlık/TAGEM/dergipark düzeyinde teyit ister |
| ⬜ **Ç2 · Ç4 adım 2-3 · S12** | Yayın politikası `n≥5` · portal/v2 · `DTM`/`POINT_CLOUD` | ⬜ | Ç4 → v2 penceresi · S12 → §12 motor kararı |

> ### 🔒 KARAR TASLAĞI — **0.h Veri Yönetişimi** (K2, onay bekliyor)
> **Sorun (K2):** plan §0 *"kamu araştırma projesi → veri yönetim planı, çiftçi rızası,
> yayın/veri paylaşım politikası"* yükümlülüğünü **tanıyor** ama bu, listedeki **tek
> eyleme dönüşmemiş** satırdı. Bu turda üç yeni veri kategorisi (öncelik bölgesi
> poligonları + NDVI görselleri · seçilmiş ham kareler · denetim örneklemi etiketleri)
> sözleşmeye girdi ve **hiçbiri** KR-090 saklama politikasında tanımlı değil (K3).
>
> **Taslak karar:**
> 1. **Veri kategorisi kaydı zorunlu:** contract'a giren her yeni kişisel/konumsal veri
>    kategorisi, aynı turda KR-090 saklama tablosuna bir satır ekler (süre + silme yolu +
>    hukuki sebep). Kayıt yoksa kalem C8'e giremez.
> 2. **Rıza metni ürün kararıdır, ama KAPSAMI sözleşmeden türetilir:** çiftçiye
>    gösterilen rıza metni, `x-preliminary-content` + `raw_frames` + denetim kanalının
>    kapsadığı veri kategorilerini eksiksiz saymalıdır.
> 3. **Yayın/paylaşım politikası:** toplulaştırılmış çıktılarda **n≥5** eşiği (Ç2
>    kalıntısı) — tek çiftçinin tarlası toplulaştırma içinde tanınamamalı.
> 4. **Üçüncü kişi verisi:** komşu parsele taşan görüntü/izdüşüm **taşınmaz** (Ç7/D7 ile
>    kare izdüşümü zaten kaldırıldı; kural genel hâle getirilir).
>
> **Onay:** ✅ **ONAYLANDI (2026-08-01)** — dört madde de kabul, **ikisi düzeltilerek.**
> Uygulama D16-c'yi beklemedi: KR-090 gövdesi zaten registry'de yaşıyor (D16-b2'de
> ölçüldü — SSOT metninde **0** kez geçiyor), yani satırlar bugün yazılabilirdi.
>
> **Madde 1 — kabul, UYGULANDI.** Üç kategorinin sözleşmede taşındığı doğrulandı ve
> KR-090'a **madde 9/10/11** olarak süre + silme yolu + gerekçe ile yazıldı:
> öncelik bölgesi/ön faz görselleri → **730 gün** (analiz sonucuyla aynı; ayrı ömür
> verilseydi silinmiş bir analizin konumsal izi geride kalırdı) · seçilmiş ham kareler →
> **180 gün** (en kısa kademe; ham kare en yüksek çözünürlüklü ve en kolay yeniden
> kimliklendirilebilir veridir, KR-050 minimizasyonu gereği şüphede az sakla — süre
> KVKK aydınlatma metniyle kesinleşir) · denetim örneklemi → **ASLA silinmez**, ama
> ölçüm dışı içerik 730 günde budanır (satır bir ölçüm kaydıdır; silinirse geçmiş model
> kalite iddiaları doğrulanamaz hâle gelir). Kural artık **zorlanıyor**:
> `tests/test_data_governance.py` (11 test).
>
> **Madde 2 — kabul, değişiklik yok.** Rıza metni ürün kararıdır; kapsamı KR-090'daki
> kategori listesinden türetilir. Contract'ta doğrudan zorlanamaz, kaynak olarak durur.
>
> **🔴 Madde 3 (n≥5) — kabul ama DURUMU DÜZELTİLDİ: bugün uygulanamaz.** Ölçüldü:
> `n>=5` / `k_anonym` / `aggregation_threshold` benzeri hiçbir ifade `enums/`,
> `schemas/`, `ssot/` ya da SSOT metninde **yok (0 eşleşme)** — çünkü toplulaştırma
> yüzeyi henüz sözleşmede yok. Onaylanmış ama hiçbir yere yazılamayan bir kural, D16'da
> kapatılan *"prose var, zorlanabilirlik yok"* sınıfının aynısı olurdu. ⇒ Madde 3
> **ileriye dönük taahhüt** olarak kabul edildi ve **Ç2**'ye bağlı kaldı: toplulaştırma
> yüzeyi doğduğu turda `n≥5` aynı turda yazılır.
>
> **Madde 4 — kabul, UYGULANDI + bir boşluk ADIYLA açıldı.** Ölçüldü: tekil kare
> izdüşümü sözleşmede **yok** (C7 Tur 2'ye ertelendi), yani kural bugün ihlal
> edilmiyor. Ama `raw_frames` seçilmiş kareleri listeler ve bir kare **komşu parseli
> görebilir**: `sees_patch_ids` yalnız hedef yamaları işaretler, kare **kırpma (crop)
> garantisi sözleşmede yoktur**. Kural KR-090 madde 12 olarak yazıldı, boşluk **0.h-a**
> adıyla açıldı — adsız boşluk, kapanmış boşluktan ayırt edilemez.
>
> **⚠️ Kapı bir mutasyonda KÖR bulundu ve düzeltildi.** İlk sürüm üç kategoriyi de aynı
> sanıp `key in json.dumps(şema)` diyordu. `raw_frames` property'si şemadan silindiğinde
> kapı **yeşil kaldı**. İki kök neden, ikisi de gerçek kusur: ① `raw_frames` edge
> şemasında iki kez geçiyor (biri property, biri alan-sahipliği listesi elemanı) ②
> platform `calibrated_dataset_manifest` `raw_frames`'i **taşımıyor**, yalnız
> açıklamasında ondan bahsediyor — taşıyıcı listesi yanlıştı. Kapı artık `properties`/
> `$defs` **anahtarlarına** bakıyor; 5/5 mutasyon kırmızı döndü.


P1 çalışma zamanı zorlaması (platform: Pydantic + `enforce=True`) · K1 `{tenant}` opaklaştırma (**MAJOR**) ·
K2 plan §0 veri yönetişimi kararı (**yeni 0.h**) · K3 saklama politikası · **C6b + S3/S4/S6/S7** (E13 sonrası) ·
**S5 `scale_factor`** — E13'ün **hemen ardından ilk sırada** (EVI/SAVI'yi sessizce bozuyor, NDVI gizliyor) ·
G3/G4/G5 geometri geçerliliği · Ç4 adım 2-3 (AL-P1 portal, v2 null) · Ç2 kalıntısı (yayın politikasına `n≥5`) ·
A7 kanopi maskesi · A5/A6 fenoloji eşlemesi · §12 motor kararı sonrası `DTM`/`POINT_CLOUD` (S12)

### 🧭 STANDART KURALI (kullanıcı direktifi, 2026-07-31 — DAİMA)

> **contract · edge · worker · platform AYNI standardı kullanır.** Bir ad, bir sözlük, bir
> sürüm, bir biçim. Bir depoda farklı yazılan şey "yerel tercih" değil **sapmadır** (I-5) ve
> geçici olabilir; kalıcı divergence yasaktır. Bu tur bunun üç örneğini kapattı: ürün sözlüğü
> (AK-7), indeks adı (AK-1), test aracı sürümü (AK-4). **Yeni bir ad/sözlük icat etmeden önce
> diğer üç depoda karşılığı var mı diye ÖLÇ.**

### 14.5.1 🆕 2026-07-31 (KADEME 0+1+2) turunda DOĞAN açık kalemler

> Bu tabloyu turun içinde bulduğum her şey için tutuyorum; başka hiçbir dosyada ikinci bir
> liste yok (handoff yalnız buraya işaret eder). ✅ = aynı turda kapatıldı.

| # | Açık kalem | Neden şimdi kapatılmadı | Nerede duruyor |
|---|---|---|---|
| ✅ **AK-1** | ~~`CHLOROPHYLL_A` bant gereksinimi TANIMSIZ~~ → **KAPANDI: `CHLOROPHYLL_A` → `LCI`.** Ad, worker'da **gerçekten uygulanan** indeksle birleştirildi (`src/indices/lci.py`: `LCI = (NIR−RedEdge)/(NIR+RedEdge)`) → gereksinim tahmin değil **ölçüm**: `[RED_EDGE, NIR]`. ⚠️ **LCI ≡ NDRE formülü** (worker `LCICalculator(NDRECalculator)`, H9/MD-9 kararı); ikisi bilerek ayrı: NDRE genel canlılık, LCI klorofil bozulması (fıstık psillid tespitinde NDWI+Green ile). ⇒ 4 bantlı drone da üretebilir; matriste `extended` altında kalması **ürün kararıdır**. Artık `index_requirements`'ta `null` girdi YOK | — | matris `index_requirements.LCI` · `x-layer-classes.map` · 3 yeni test (`TestCrossRepoNamesAreUnified`) |
| ⬜ **P15** 🔴 | **AK-1'in platform yarısı:** `tarlaanaliz-platform/src/core/domain/value_objects/spectral_tier.py:51` → `EXTENDED_INDICES = ("EVI","SAVI","CHLOROPHYLL_A")` sabiti **`LCI`** olmalı. Ad birleştirmesinin tek canlı tüketicisi budur (ölçüldü: worker/edge'de eşleşme yok) | Ayrı depo, ayrı PR | plan §14.5.1 (bu satır) |
| **AK-2** | **Dedektör `$ref` hedeflerini ÇÖZMEZ.** Retarget `REF_CHANGED` (NON_BREAKING) olarak görünür kılınır ama sınıflandırılmaz — bir `$ref`'i tamamen farklı bir şemaya çevirmek sessizce MINOR görünür | Çözüm, çapraz-dosya referans grafiği + döngü koruması ister; KADEME 0'ın kapsamı "kapılar dürüst olsun"du, "kapılar tam olsun" değil. **E3 kararı (C8'de `$ref` inline)** bu riski zaten büyük ölçüde ortadan kaldırır | `tools/breaking_change_detector.py` docstring "BİLİNEN SINIRLAR" + `docs/checklists/SDLC_GATES.md` §3E (elle inceleme maddesi) |
| **AK-3** | **`NORMATIVE_ANNOTATION_KEYS` elle tutulan bir listedir** (5 anahtar). Yeni bir normatif `x-` bloğu eklenirse otomatik kapsanmaz | Otomatik kapsama, "hangi `x-` normatiftir" sorusunu çözmeyi gerektirir; `x-updated` gibi gürültü alanlarını da içine alırdı | `tools/breaking_change_detector.py` sabiti — yeni normatif blok eklerken listeye yazılmalı |
| ✅ **AK-4** | ~~pytest sürüm sapması (yerel 9.0.2 / CI 8.4.2)~~ → **KAPANDI: her yerde pytest 9.x.** `requirements-dev.txt` `>=9.0.0,<10` · `pyproject.toml` `^9.0.0`; `pytest-cov` da hizalandı (`^7.0.0` — yerelde koşan sürüm). Kapının yerelde geçip CI'da farklı davranması, kapıya olan güveni yok eder — **sürüm sapması da bir sapmadır** | — | `requirements-dev.txt` · `pyproject.toml` · yerel doğrulama: pytest 9.0.2 + pytest-cov 7.0.0 ile kapsamlı koşum yeşil |
| **AK-5** | **`x-compat-accepted` beyanları BAYATLAYABİLİR.** Bugün gerekçe *"üretici yok"* (ölçüldü). Üretici yazıldığında beyan hâlâ orada durur ve daraltmayı indirmeye devam eder | Beyanın "ne zaman geçersizleşeceğini" makine-okunur yazmak yeni bir alan (`valid_until` / `revisit_when`) ister — tasarım kararı | `schemas/edge/calibrated_dataset_manifest.v1.schema.json` (2 beyan) · testler yalnız beyanın **eksiksizliğini** zorluyor, tazeliğini değil |
| **AK-6** | **E15/P14/E16 kardeş depo işleri** — D7/D8'in kod yarıları (edge `qc_report_writer` fail-loud · platform `worker_job_publisher` fail-open adımı) + C11'in edge yarısı (**E16** ürün adı biçimi + vendored yenileme) | Ayrı depo, ayrı CI, ayrı PR; bu oturum contract deposunda çalıştı | §14.1 (**E15**, **P14**) ve §14.2 (**E16**) satırları |
| ✅ **AK-7** | ~~İki ürün vocabulary'sinin kök nedeni~~ → **KAPANDI: beş serbest metin alanının HEPSİ kanonik sözlüğe bağlandı.** ⚠️ **Sınıf taraması tek örneği değil BEŞİNİ buldu:** `edge/worker_result.v1.crop_type` (*"e.g. cotton, wheat"* — küçük harf örneği, edge sözlüğünün kaynağı) + **dört olay şeması** (`analysis_completed`, `analysis_review_requested`, `field_created`, `field_health_changed`) — dördü de açıklamasında *"reference: crop_type.enum.v1"* diyordu ama şema **hiçbir şeyi zorlamıyordu** (C0'ın manifestlerde kapattığı "prose var, zorlanabilirlik yok" sınıfı). **Daraltma güvenli mi? ÖLÇÜLDÜ:** platform ürünleri zaten BÜYÜK harf üretiyor (`crop_type.py:113,130`) · `worker_result.v1`'in **kod üreticisi yok** · platform şema zorlaması varsayılan **KAPALI** (`settings.py:190`). Beş alan da `x-compat-accepted` ile beyanlı; yeni **sınıf kapısı** (`test_crop_vocabulary_single_standard.py`, 8 test) serbest metin ürün alanının geri gelmesini yasaklıyor | — | 5 şema + kanonik enum · dedektör: 5× `ENUM_CONSTRAINT_ADDED` **ACCEPTED** |
| ✅ **AK-10** | **ÇÖZÜLDÜ (araç + kapı): `tools/sync_kr_corpus.py`.** Ölçüm doğrulandı ve artık ÖLÇÜLEBİLİR: `--check` bugün **4/4 hedefte sapma** raporluyor (platform SSOT metni STALE · worker SSOT metni **MISSING** · her iki registry kopyası STALE). Araç bilerek iki kipli: `--check` ölçer (kapı), `--apply` yalnız operatör çalıştırır ve sonucu **kardeş depoda AYRI PR** olur — sessiz kopyalama C8'in görünmez yan etkisi olurdu. CRLF farkı sapma sayılmaz (normalize hash). Kapı SDLC_GATES §3C'ye eklendi + 9 test (kardeş depo gerektirmeyen, geçici dizinli davranış testleri). **Kalan iş operatörde:** `--apply` + iki kardeş depoda commit/PR | ⬜→✅ | **eski metin:** `kr_registry.md`: platform `docs/kr/` **1211 satır**, platform `contracts/ssot/` **1242**, worker `docs/reference/` **936** — üçünde de **KR-093 başlığı YOK**; contract'ta 1267. SSOT metni: contract **1906** ↔ platform **1895**, worker'da **hiç yok**. Yani hem registry hem SSOT metni alt-akışta bayat ve worker KR korpusunun yeni yarısını hiç görmüyor | Senkron aracı yok (C-SSOT-2 kökü): `tools/sync_to_repos.sh` yalnız `schemas/`+`enums/`+`CONTRACTS_VERSION.md` taşıyor. Çözüm bir araç kararı: salt-okunur drift dedektörü mü, gerçek dağıtım mı? | plan §14.5.1 · ölçüm bu turda |
| ⬜ **P17** 🔴 | **SSOT metni senkronu BOZULDU (bu turda, bilinçli):** D17'nin KR-093 gövde düzeltmesi `docs/TARLAANALIZ_SSOT_v1_2_0.txt`'i değiştirdi → contract kopyası artık platform kopyalarından FARKLI (ölçüldü: contract `41e152a3…` · platform/docs `78a4f557…` · platform/contracts/docs `d525671f…`). C-SSOT'un kurduğu bayt-özdeşlik yeniden kurulmalı | Platform deposunda yapılır (ayrı PR); C8'in parçası. ⚠️ Not: platform'un İKİ kopyası var (`docs/` ve submodule `contracts/docs/`) ve bunlar **birbirinden de farklı** — yani senkron zaten kırıktı, bu tur onu görünür kıldı | plan §14.5.1 |
| ✅ **AK-9** | **KAPANDI (2026-08-11 · D12, contract 7.6.1 → PR #62).** ⛔ Aşağıdaki *"ad var, üretim yok"* iddiası **ÖLÇÜMLE ÇÜRÜTÜLDÜ**: iddia tek bir dosyaya (`feature_extraction.compute_indices_v2`) bakıp "yok" demişti; üretici worker'ın **çıkarım hattındadır** (`inference/pipeline.py:141 · :902 · :2144 · :1904/:1995`) ve çıktı `reporting_agent.py:55-56` ile rasterlanıp nesne deposuna yüklenip `manifest.json`'da listeleniyor. Formül **tahminle değil, koddan okunarak** tanımlandı: `stress_ratio = NDRE / NDVI`, NDVI ≤ 0 piksellerinde nötr `1.0` (`src/indices/stress_ratio.py:59-60`). Teslimat kuralı DEĞİŞMEDİ ama artık **makine-okunur**: `delivery_rule.preliminary = false` — katman `proxy_only`, uzman kapısı öncesinde çiftçiye sunulmaz. **Tanımlılık ≠ geçerlilik.** Kapı: `test_single_normative_body.py::TestDerivedQuantitiesAreDefined` (9 mutasyon) + kardeş-CI `TestVendoredMetadataDoesNotContradict` (6 mutasyon). Ayrıntı: **§14.11**. **Aşağıdaki özgün kayıt tarihsel bağlam için bırakıldı** ⬇️<br>~~`stress_ratio` TANIMSIZ~~ — KR-093'ün `WATER_STRESS` kaleminin kaynağı olarak **3 yerde** anılıyor, **0 yerde** tanımlı (A3 doğrulandı). Worker `channel_spec.py` adı `derived_indices` listesinde taşıyor ama `compute_indices_v2` çıktısında hesap YOK: ad var, üretim yok | Formülü tahminle yazmak doğrulanamaz kapı üretir (`CHLOROPHYLL_A` dersi). WATER_STRESS artık `proxy_only` ve ön fazdan çıktığı için bugün **zorunlu teslimat değil** → tanım, termal/SWIR donanım kararıyla birlikte verilir | `analysis_type → metadata.indexDefinitions.stress_ratio` (`UNDEFINED_PENDING_DECISION` + gerekçe) · kapı: `test_single_normative_body.py` |
| ⬜ **AK-8** | **`expert_labeling_card.calendar_risk_by_crop` FARKLI EKSEN kullanıyor:** anahtarları `^[a-z_]+$` ve örnekleri *"cereals, fruit_trees, cotton"* — yani mahsul **GRUBU** ile mahsul **ADI** aynı sözlükte karışıyor. Ürün sözlüğü kapısı bunu bilerek kapsam dışı bıraktı (farklı eksen) | Grup ekseninin kanonik bir sözlüğü YOK; tanımlamak agronomi kararıdır (hangi gruplar, hangi mahsul hangi gruba?) | `schemas/worker/expert_labeling_card.v1.schema.json` → `calendar_risk_by_crop.patternProperties` |

## 14.7 ✅ TUR 1 KAPANIŞI (2026-07-31) — **2026-08-11'de depoda yeniden ölçüldü**

> **Bu bölüm 104 satırdı; kalemlerin başındaki işaretlere GÜVENİLMEDİ, hepsi kodda/CI'da/git'te
> yeniden ölçüldü.** Sonuç: **14 kalem bitmiş**, **7 kalem gerçekten açık**. Kapananlar tek
> satıra indirildi (kanıtı korunarak); açık olanlar tam gövdesiyle aşağıda.
>
> ⚠️ **Kalem numaraları KORUNDU** — `CHANGELOG.md:435` ve dört denetim raporu bu bölüme
> *“kalem 4 / kalem 6 / kalem 7 / E17-W10 satırları”* diye atıf yapıyor.

### ✅ KAPANDI — ölçümle doğrulandı (2026-08-11)

| # | Kalem | Bugünkü ölçüm (kanıt) |
|---|---|---|
| **1a · 1b · 2 · 2a** | SSOT metni senkronu · registry sınıflandırma · ikili gövde 49→0 · KR-092 clamp→fail-closed | `sync_kr_corpus.py --check` → **IN_SYNC 4/4** · `KNOWN_DUAL_BODY_COUNT = 0` (forbid kipi) |
| **1c** | `sync_kr_corpus --apply` + kardeş PR'lar | **2026-08-11'de yapıldı**: contract PR #59 · platform PR #405 · worker PR #213. Worker kopyası KR-034 ODM bloğunu hiç taşımıyordu, o da kapandı |
| **3** | D4-b — parite kapısı karşı tarafta koşar (PAT yok) | **E17 + W10 uygulandı**: `edge/.github/workflows/contracts_gate.yml` ve `worker/…/contracts_gate.yml` ikisinde de `test_vendored_parity` **2 atıf** |
| **4** | SD8 — 14 retro-tag + kayıt notu | ⛔ *“push onay bekliyor”* ifadesi **BAYATTI**: ölçüm **25 yerel = 25 uzak tag**, fark 0. (Aynı bayatlık 6-lens denetiminde bulgu #33 olarak da yakalanmıştı.) `2.0.2` bilinçli etiketsiz — sürüm kilidi yok |
| **5** | 0.h veri yönetişimi + K3 saklama MUST'ları | `tests/test_data_governance.py` yürürlükte |
| **6** | E13 = `ABSOLUTE` ⇒ C6 iş yok | `tests/test_calibration_type_axis.py` (7 test) kararı koruyor |
| **7** | C8 töreni — `v7.3.0` yayımlandı | tag annotated, `git describe` temiz |
| **W11** | Worker'da kodlamasız `open()` (5 üye) | **Beşi de kapandı** — `safe_path.py:19` artık `open(safe, encoding="utf-8")` ve satırda `# W11: kodlama DAİMA açık` notu var; diğer üç dosyada kodlamasız `open(` **0** |
| **C8-a** | Kalıcı `propagate_vendored.py` aracı | **Araç VAR** — `tools/propagate_vendored.py`, ilk commit **2026-08-02** |
| **E15** | edge `qc_report_writer` clamp + fail-loud + `crs_mismatch` | Dosya başlığı: *“E15 (2026-08-02) — İKİ SESSİZ YOL KAPATILDI”*; ham oran WORM'a yazılıyor, `flags.append("crs_mismatch")` :190 |
| **E16 / E16-b** | edge ürün sözlüğü BÜYÜK harfe | edge `*.json` içinde küçük harf `"cotton"` → **0 eşleşme** |
| **P14** | platform fail-open `PANEL_ABSOLUTE` adımı | `worker_job_publisher.py:82`: *“🔴 P14 (2026-08-01) — ESKİ 3. ADIM KALDIRILDI”* |
| **P15** | `CHLOROPHYLL_A` → `LCI` | `spectral_tier.py:51` P15/AK-1 notu · `EXTENDED_INDICES = ("EVI", "SAVI", "LCI")` |
| **P17** | bayat sürüm sabiti logları | `main.py:182` *“P17 (2026-08-01): sürüm dizesi TEK YERDEN okunur”* → `pinned=_contracts_pin.semver` |
| **P1** | platform şema zorlaması (`enforce=True`) | **AÇILMIŞ** — `settings.py:214-215` `worker_result_schema_enforce: bool = True` + `edge_manifest_schema_enforce: bool = True`. Sıra kilidi (E16 önce) **sağlandı** |
| **W8** | Denetim satırı emisyonu (π_h · bucket · rotation) | `agent_messages.py:209-211` üç alanı da taşıyor |
| **W13** | worker vendored `analysis_job.v1` → `scale` + `calibration_method` | Dosyada **5 eşleşme** |

### ⬜ GERÇEKTEN AÇIK — 7 kalem (2026-08-11 ölçümü)

| # | Kalem | Bugünkü ölçüm | Engel |
|---|---|---|---|
| **P16** 🟠 | Platform konsensüs yolu `consensus_participation: EXCLUDED` satırını **saymamalı** | platform `src/` içinde `consensus_participation` → **0 eşleşme** | Alan hiç kalıcılaştırılmadı (eski **P21** ile aynı yüzey); dışlanacak veri henüz yok |
| **0.h-a** 🟡 | `raw_frames` **kırpma (crop) garantisi** yok — seçilmiş ham kare komşu parseli görebilir | contract `intake_manifest.v1` içinde `cropped_to_parcel` → **0** | Kare seçici **E11** ile aynı yüzey; E11 C8'den önce merge edilmez (D10-E4 kilidi) |
| **2b** 🟡 | Normatif metindeki sayısal eşiklerin worker YAML'ı ile hizasını doğrulayan kapı | contract `tests/` içinde eşik-hizası testi **YOK** | Kardeş depo dosyası okunmadan yazılamaz; D4-b artık uygulandı → **engel kalktı, yazılabilir** |
| **2c** 🟡 | Ürün sözlüğü **eksen farkı** yazılı değil | worker `dynamic_thresholds.yaml` anahtarları küçük harf (`grape:`, `disease:`), kanonik tel BÜYÜK harf | Eksen farkı ya kanonik olarak beyan edilir ya anahtarlar hizalanır (worker kararı) |
| **2d** 🟡 | `sync_kr_corpus.py` *“kaybolacak içerik”* ile *“üzerine yazılacak eski sürüm”* ayrımını yapmıyor | **2026-08-11'de bizzat yaşandı:** araç `DIVERGENT` deyip yazmayı reddetti; 8 satırın tamamı süperseded çıktı, elle birleştirildi | Ayrım satır-bazlı değil **blok-bazlı** eşleştirme ister (tasarım kararı) |
| **AK-5** 🟡 | `x-compat-accepted` beyanlarına `revisit_when` alanı | **8 dosyada** beyan var, `revisit_when` → **0** | Gerekçe *“üretici yok”*; üretici yazılınca beyan sessizce bayatlar |
| ✅ **AK-9** | ~~`stress_ratio` tanımsız~~ → **KAPANDI 2026-08-11** | `analysis_type.enum.v1` v1.4.4 → `status: DEFINED`, `formula: "stress_ratio = NDRE / NDVI"`, makine-okunur `domain_guard` + `delivery_rule.preliminary=false` | *"üretim yok"* iddiası ⛔ çürütüldü (ölçüm yanlış dosyaya bakmış); kısıt SUNUM katmanında uygulanıyor — bkz. §14.11 |

**Diğer kapı borçları (durum değişmedi):** **AK-2** dedektör `$ref` hedeflerini çözmez —
E3 inline'ı riski büyük ölçüde kaldırdı · **AK-3** `NORMATIVE_ANNOTATION_KEYS` elle tutulan
5 anahtar · **AK-8** `calendar_risk_by_crop` mahsul GRUBU ile ADINI karıştırıyor (grup
sözlüğü agronomi kararı).

### 🔶 MAJOR TURU — `v8.0.0` (hâlâ AÇILMADI)

> Üçü de `versioning_policy.md`'ye göre breaking; tek turda toplamak üç ayrı MAJOR + üç
> migration guide + üç kez üç-depo re-pin turunu **bire** indirir.
> Ön koşul: MINOR turu C8 ile kapatılır (yapıldı, `v7.3.0`).

| # | Kalem | Neden MAJOR | Bugünkü durum |
|---|---|---|---|
| **S3** | `DLS2_RELATIVE` → satıcıdan bağımsız ad (ör. `IRRADIANCE_RELATIVE`) ya da tamamen kaldırma | enum değeri yeniden adlandırma | Karar **ölçümle çözüldü**: `x-derivation.map` iki anahtar taşıyor ⇒ `DLS2_RELATIVE` matristeki hiçbir drone için türetilemez. Uygulama MAJOR turu bekliyor |
| **S7-b** | `raw_frames[].band` → `required` | `FIELD_MADE_REQUIRED` | **AK-11 kapandı** ⇒ beyanlı MINOR'da da yapılabilir; v8.0.0'ı beklemek ZORUNDA değil |
| **K1** | `{tenant}` opaklaştırma | alan biçimi değişimi | §14.5'te MAJOR penceresi olarak izleniyor |
| **DEP-1** | Penceresi dolmuş 2 ödeme nesnesi (`payment_status.enum.v1` · `payment_intent.v1`) | silme = MAJOR | `since: 6.2.0`'dan beri 7.0→7.4 geçti; tüketiciler v2'ye pinli. MAJOR açılırsa aynı turda silinmeli |

**Tur açılış sırası:** ① AK-11 ✅ zaten kapalı ② S3 kararı uygulanır ③ `docs/migration_guides/`
altına **tek** rehber ④ `pin_version.py --major --breaking` ⑤ annotated tag + push
⑥ `propagate_vendored.py --check` → `--apply` (artık **araç var**, elle yapılmaz)
⑦ üç depo re-pin → I-1/I-3/I-4 ölçülür.
**Kapsam kilidi:** MINOR yapılabilen hiçbir şey MAJOR tura eklenmez.

---
## 14.6 Şüpheli bulgular — kapatılmadan önce ölçülecek

`M2` platform konsensüs yolu · `M4` worker bulk_approval yolu · `M1/P4` emisyon kodu yazılırken ·
`Q21` `pytest -q` ×5 ardışık · `SD8` retro-tag koordinatör kararı · `A7` TAGEM/Bakanlık literatür teyidi

---

## 14.A 📦 ARŞİVE TAŞINAN TURLAR + DEVRALINAN AÇIK KALEMLER (2026-08-24)

> **756 satır** `docs/EYLEM_PLANI_ARSIV_2026-08.md`'ye **bayt-özdeş taşındı.**
> Gerekçe: bu dosya dört ayrı *"SONRAKİ OTURUM — BURADAN BAŞLA"* iddiası
> taşıyordu (§14.9 · GİRİŞ NOKTASI · §14.8 · §14.17) ve okuyan kişi hangisinin
> canlı olduğunu bilemiyordu. **Tek canlı giriş: §14.17.**
> Emsal: v8.0.0 turu 2026-08-11'de aynı ölçütle kaldırılmıştı.
>
> 🔴 **Kayıp YOK — ölçüldü:** taşınan gövde arşivde bayt-özdeş duruyor
> (`git diff --stat` ile doğrulanabilir) ve **açık kalemlerin tamamı aşağıda
> canlı listede.** Kapalı kalemlerin gerekçesi arşivdedir.

| Taşınan bölüm | Neydi | Neden arşiv |
|---|---|---|
| **§14.9** (179 st.) | *"DEVAM ET" girişi* (2026-08-01) | §14.17 ile süperseded |
| **▶️ GİRİŞ NOKTASI** (200 st.) | Motor-agnostik kalibrasyon + v7.5.0 turu (2026-08-02) | Araştırma sonucu **KR-034/ODM ile kanonikleşti**; gövde `M3M_INDEKS_VE_RADYOMETRI_ARASTIRMASI.md` + `TERRA_ODM_KARSILASTIRMA_2026-08-06.md` ile örtüşüyor |
| **▶️ v8.0.0 TURU** (18 st.) | Zaten kaldırılmış turun devir tablosu | İkinci dereceden tarihsel kayıt |
| **§14.8** (57 st.) | Öz-denetim sıralı listesi (2026-08-01) | §14.17 ile süperseded |
| **§14.11** (50 st.) | D12/D13 turu (2026-08-11) | Gövdesi kapandı; **açık kalanları** aşağıda |
| **§14.12** (51 st.) | Cerrahi kalite turu (2026-08-11) | Gövdesi kapandı; **açık kalanları** aşağıda |

> 🔴 **§14.10 TAŞINMADI — planda kaldı (hemen aşağıda).** İlk taramamda *"kapandı"*
> diye işaretlemiştim; **yanlıştı ve ölçümle yakalandı.** Sebep: tarayıcım açık kalemi
> yalnız `⬜` / `[ ]` ile arıyordu, §14.10 ise **🔴/🟠/🟡 önem rozeti** kullanıyor →
> 20 kalemlik canlı tabloyu *"0 açık"* saydı. Canlı iş tablosunu arşive gömmek,
> tam da bu taşımanın önlemeye çalıştığı kaybı üretecekti.
> **Ders (hafızada da kayıtlı): tarayıcını önce kendi üzerinde sına.**
| **§14.14** (201 st.) | Uzman ekranı zinciri turu (2026-08-19/20) | Kendi başlığı *"süperseded: canlı giriş §14.17"* diyordu |

### ⬜ Devralınan AÇIK kalemler — **arşive taşınan bölümlerden: 14**

> ⚠️ **Bu 14, dosyanın tüm açık borcu DEĞİLDİR** — yalnız *arşive taşınan* bölümlerden
> devralınandır. Ayrıca **§14.10'da 19 açık `AL-K` kalemi** (planda, hemen aşağıda) ·
> **§14.5 KADEME 5** · **§3.6 DK kuyruğu** kendi kalemlerini taşır. Toplam borcu tek
> sayıya indirmek için bunları toplayın — **buradaki 14'ü toplam sanmayın.**

| # | Kalem | Depo | Durum / neden açık |
|---|---|---|---|
| **Ö7** | `KNOWN_VENDORED_AHEAD` W14'ün *kalıcı* beyanını taşıyor ama yapı *"kalıcı olamaz"* diyor | contract | Bugün delik değil (6/6 dolu); sayaç 0'a inemez, **metin yanlış** |
| **P21** | `consensus_participation` kalıcılaştırılsın (`ExpertReviewModel` kolonu + worker mesajından okuma) | platform | **P16'nın eksik ortası** |
| **P16** | Konsensüs yolu `EXCLUDED` satırı saymamalı | platform | 🔒 **W8-b + P21'e bağlı** |
| **W8-c** | `AuditSetSampler` oran tablosu boş → hiçbir tile seçilmiyor | worker | AL-W1; aktivasyon **bilinçli ops kararı**, kod hazır |
| **W13** (ÖD-2) | `analysis_job.v1` `CalibrationMetadata` — S5 + W12 tel üstünde ölü | worker | contract tarafı ✅, worker tarafı ⬜ |
| **P17** (ÖD-14) | `main.py` sürüm sabiti sınıfı yarım süpürülmüş (log satırlarında `7.2.0` kalıntısı) | platform | Ölçüldü, **gerçek ama küçük** |
| **SD11** | Kanonik şema/enum üst düzey `notes`/`metadata` anahtarları OpenAPI `struct` ihlali | contract | **23 ihlal / 12 dosya** (`notes` ×16 · `metadata` ×7) |
| **AL-K18** | Ön faz kapısı **canlı trafikte** doğrulanmadı | platform | Ayakta yığın yoktu; kabul ölçütü `SESSION_HANDOFF.md` §0.A/D-2'de |
| **AL-K19** | Yeni parite kapısı **yalnız worker CI'ında** koşar | contract | D4-b tasarımı gereği bilinçli |
| **AL-K23** | `Detection.bbox` parite-kilitli istisna | contract | Kapatma denendi, **ölçümle geri alındı**. Çıkış sırası: önce vendored kopyayı kapat, sonra istisnayı sil |
| **AL-K24** | `paths:` filtresi tümden kaldırılsın mı? | contract | **Karar sahibinin.** Her filtre bir fail-open yüzeyi; karşı ağırlık CI maliyeti |
| **AL-K27** | `payment_target_type` bağlanmadı — bilerek ertelendi | contract | Ölçüldü ve **güvenli**; **bir sonraki MINOR turunun ilk kalemi** |
| **AL-K28** | `field_created` değer kısıtı kuralının **kapısı yok** | contract | Kural yalnız düzyazıda yaşıyor |
| **AL-K29** | `tools/sync_to_repos.py` ölü — **silme kararı kullanıcının** | contract | Gerçek çağıran **0**, kapsam **%0** |

> ⚠️ **P-1…P-6 (motor adaptörü) donanım-kapılıdır** ve arşivdeki GİRİŞ NOKTASI
> bölümünde ölçümleriyle durur: `P-2` (`CalibratedManifestWriter`, bugün **0 yazıcı**)
> ve `P-6` (M3M sıfır-Blue etkisi) pilotu açan yoldur. Donanım geldiğinde
> **§3.6'dan önce** gelirler.

### ⬜ §14.14'ten devralınan **uzman ekranı zinciri** — 8 kalem

> 🔬 **Bu tablo ikinci turda eklendi.** İlk hâlim buradan yalnız *"1 ürün sorusu"*
> yazmıştı; çürütme turu ölçtü ki **DK-49/50/51/53/54/55 planda HİÇ geçmiyordu**
> (yalnız arşivde). Sekizi de aşağıda.

| # | Kalem | Nerede |
|---|---|---|
| **DK-48** 🔴 | Bastırılan tespitler uzman kanalına açılmalı. **Kod tarafı kapandı** (plat #450 · work #242) ama **dağıtılmadı** → canlıda hâlâ boş | worker + platform |
| **DK-49** 🟠 | `trigger_confidence` uzmana gösterilmiyor (yalnız ADMIN). Değer **zaten kayıtlı**; iş onu uzman ucuna taşımak. ⚠️ KR-025: *tanı* değil **modelin belirsizliği** olarak sunulmalı | platform + web |
| **DK-50** 🔴 | **Sunucu CPU borcu** — `numpy<2` pini kalıcı değil. #446 ile döşeme servisi kurtarıldı ama **asıl çözüm sunucuda**: VM işlemci modeli `host-passthrough` yapılmalı. Kod bunu çözemez, etrafından dolaşır | **altyapı** |
| **DK-51** 🟠 | *"Gerçek Görünüm"* taban görüntüsü boş — `rgb_ortho_uri` ile `calibrated_ortho_uri` **aynı 5 bantlı dosyayı** gösteriyor. Tile servisi dürüstçe boş dönüyor; kusur **ingest tarafında** | edge/ingest |
| **DK-52** 🟠 | Yama (`priority_zones`) üretimi üretimde **bağlı değil**: 0 satır, log 0 kez, bayrak `False`. Eşik tablosu da *"literatür ortalaması, kalibre edilmeli"* diyor | edge |
| **DK-53** 🟡 | **Faydalı böcek kartı YOK** (210 kartın 0'ı `beneficial`). Koruma #447'de bağlandı → kart yazıldığı gün görünür. *Ölü koruma bağlama* örneği | worker kart kataloğu |
| **DK-54** 🟡 | Kanonik bağ mandalında **2 kalem** kaldı (5 → 2). Mandal iki yönlü, sessizce unutulamaz | platform |
| **DK-55** 🟡 | `lock-install-smoke` bütçesi kapağı aşıyor: kapak 20 dk, gerçek **28,5 dk** → kapak **yanlış güven** veriyor | platform `ci.yml` |
| **DK-56** 🔴 | **Eskalasyon döngüsü — inceleme HİÇ kapanmıyor.** `expert_reviews.escalation_round = **26**` (satır `e8c513ed…`/`dbdfb37a…`, 08-19'da doğdu, 08-26 03:30'da yine atandı) ve `escalated_to_expert_id` **atanan uzmanın kendisi**. Sonuç: `has_open_reviewer()` yüzünden KR-019 kapısı **hiç değerlendirilmiyor** → görev `PENDING_REVIEW`da kilitli kalıyor, iki inceleme ZATEN `rejected` olsa bile. Rapor çiftçiye **hiç** ulaşmaz | platform `expert_reassignment_service` |
| **DK-57** 🔴 | **Uzman, GÖREMEYECEĞİ kanıta atanıyor** — aşağıdaki açık ürün sorusunun ilk somut ölçümü. `4d1ab823…`: `predicted_sub_specialty=DISEASE` → hastalık uzmanı atandı (atama **doğru** çalıştı), ama `predicted_detection_type` **BOŞ** (koşum `INDICES_ONLY`, %31 güvenle bulgu bastırıldı) → alt-uzmanlık `evidence_hint`'ten türetildi (`worker.py:1455-1458`). Gerçekte üretilen katman **Azot Stresi** ve arayüz onu bu uzmandan **bilerek gizliyor**. Uzmandan kanıtsız karar isteniyor | worker + platform |
| **DK-58** 🟠 | **Uzmana tüm tarlanın tek görüntüsü gidiyor.** `ReviewImagesResponse` iki kaynak döner: `patches` (Edge'in 3 katmanlı yamaları, **birincil**) yalnız NDVI önceliklendirme + Pix4D varsa dolar — üretimde **donanım-kapılı**, yani boş; herkes `tile_layers` **geri düşüşüne**, yani tarla geneli COG'a düşüyor. Alt-uzmanlık ayrımı görüntü katmanında hiç oluşmuyor. DK-52 ile aynı kök | edge → platform |
| **DK-59** 🟡 | **Kartlar alt-uzmanlığa göre GİZLENMİYOR** — kusur değil **ürün kararı çatışması**. Ayrım mantığı ÇALIŞIYOR (ölçüldü: zararlı uzmanı `{BENEFICIAL,PEST}` ↔ su/azot uzmanı `{HEALTH,NITROGEN_STRESS,WATER_STRESS}`, ayrık). Backend kart **silmez**, `relevant` etiketi koyar; arayüz ilgisizleri **özet olarak altta** tutar — gerekçesi kodda: *"hastalık/zararlı ayrımı komşu kart okunarak yapılır"*. Ürün sahibi 2026-08-26'da **süzme** istedi. ⚠️ `_caller_specialization_codes` **fail-OPEN**: DB hatasında tüm kartlar `relevant:True` — süzme eklenirken bu dal ele alınmazsa arıza anında uzman **hiç kart göremez** | web + platform |
| **DK-60** 🟠 | **Çerez 24 saat, JWT 30 dakika.** `AUTH_TOKEN_TTL_MS = 24 saat` (`web/src/lib/constants.ts:6`) ↔ `jwt_access_token_expire_minutes = 30` (`settings.py:171`). Sunucu kapısı yalnız çerezin **varlığına** bakıyor (`(admin)/layout.tsx:41`), geçerliliğine değil → sayfa açılıyor, ilk API çağrısı 401 alıyor, refresh düşerse `clearAuthStorage()` **oturumu siliyor**. Belirti: panelde 30 dk bekleyip bir butona basınca **çıkış**; geri dönünce sayfa açık (istemci önbelleği). Canlı gözlendi 2026-08-26 | web |
| **DK-61** 🟠 | **Abonelik zamanlayıcısı sonsuz döngüde — abonelik bir daha görev ÜRETEMEZ.** Ölçüldü 2026-08-26: son 24 saatte **51 koşumun 51'i** de `UniqueViolation (uq_mission_field_planned_active)` ile düştü. Üç katman: ① `session.commit()` **döngünün dışında** (`fastapi_scheduler_integration.py:204`) → tek çakışma **tüm partiyi** düşürür, ikinci abonelik aktif olunca o da bloke olur ② rollback `next_due_at`'i de geri alıyor → tarih hiç ilerlemiyor, **kendiliğinden iyileşme yok** ③ 🔴 commit geri alındığı hâlde `RUN_COMPLETE **created=1**` yazılıyor — *yanlış başarı raporu*. ⚠️ Kısıt kısmi (`CANCELLED/FAILED/REJECTED` hariç), yani görev `DONE` olsa bile etkin kalır → sahte mükerrer görev doğmaz **ama** döngü de bitmez. Bugün zararı dar (tek ACTIVE abonelik, görevi zaten var, gerçek uçuş sağlam); **uçuştan sonra o müşteri hiç yeni görev almaz**. ⓘ Yan not: backend Sentry DSN'i **`javascript-react`** projesine bakıyor — backend hataları arayüz projesinde birikiyor, bildirim yanlış ekibe gidiyor | platform scheduler |
| **DK-62** 🟡 | **Gozkurdu karti UAV ile gorulemeyecek bir yapiyi “YUKSEK gorunurlukte” ilan ediyor — uzman olmayan seyi arıyor.** `config/expert_labeling_cards/pistachio_cards.yaml` → `thaumetopoea_solitaria`: `uav_detectability: DIRECT`, `uav_detection_reliability: HIGH`, `pattern: defoliation_patchy_with_nests`; `distinguishing` *“Dallarda ipeksi KESE (silk nest) — belirgin beyaz yapi”*; `ground_verification` *“ipeksi kese…”*. ⚠️ Literatur bunu **curutuyor**: kalici ipeksi kese **T. pityocampa**’nin (cam kese bocegi) ozelligidir; Simonato ve ark. 2013 *T. solitaria*’yi **“patch-restricted forager”** — gecici cadir ya da **hic cadir yok** — diye siniflandirir; TAGEM teknik talimati larvalarin **gunduz govde/kalin dallarda golgede dinlenip GECE beslendigini** soyler ve mucadelede **kese toplamayi HIC anmaz** (oysa T. pityocampa icin anar). Kart ayrica **“kislayan larvalar”** diyor; tur **YUMURTA halinde kislar**, larva tomurcuk patlamasiyla cikar — yani `calendar_months [3,4,5]` bas tarafi erken, asil pencere **Nisan–Mayis**. 💥 Zarar: uzman ~1 cm GSD’de **var olmayan** beyaz yapiyi arar, bulamaz, **“yok” der** — %100’e varan defolyasyon yapabilen bir zararlida yanlis negatif; etiket havuzuna da sizar. ✅ Onerilen duzeltme: kanit **keseden → agac-olcekli, ANI/ikili defolyasyona** cevrilir; `pattern` → `defoliation_abrupt_tree_scale`; `multi_temporal_required: true` (mantari `defoliation_progressive` olan karazenk/septoria’dan ayiran sey **hiz**, doku degil); guven `HIGH` → `MEDIUM`. Katalog **worker=SSOT**, platform kopyasi bayt-ozdes (`sha256 de41d6f8…`) — duzeltme **iki depoya da ayni sekilde** gitmeli. ℹ️ Kanit sinifi: kartin metni **bizzat okundu**; curutme **arastirma ajani raporundandir**, birincil kaynaklar (Simonato 2013 + TAGEM talimati) **tarafimdan okunmadi** — duzeltmeden once dogrulanmali. Katalogdaki tek **DIRECT+HIGH** kart bu; digerlerinin hepsi kanopi-olcekli sinyale dayaniyor (23 kart tarandi). | worker + platform (kart YAML, bayt-ozdes) |

**+ Açık ürün sorusu:** uzmanın **hangi alana yönlendirileceğine** bugün *kalibre
edilmemiş bir NDVI/fenoloji sezgisi* karar veriyor (`classify_from_evidence`). İfade
PR **#448**'de düzeltildi (alan *"modelin tanısı değil, yönlendirme ipucu"*), ama
**kalibrasyon sorusu açık** — DK-52'deki eşik kalibrasyonuyla aynı kökten.
**İlk gerçek uçuş verisiyle birlikte değerlendirilmeli.**
>
> 🔴 **2026-08-26 — bu soru artık teorik değil, ÖLÇÜLDÜ (DK-57).** Canlı bir incelemede
> tespit hiç üretilmediği hâlde (`predicted_detection_type` BOŞ) yönlendirme
> `evidence_hint`'ten **DISEASE** dedi; sistem hastalık uzmanı atadı; gerçekte üretilen
> tek katman **Azot Stresi**ydi ve arayüz onu o uzmandan gizledi. Yani kalibrasyonsuz
> sezgi yalnız *"yanlış alana yönlendirme"* değil, **kanıtsız karar isteme** üretiyor.

### 🔴 Ö1 — CI bu depoda **otoriter değildir** (§14.9'dan, planda hiç geçmiyordu)

CI, yerelde kırmızı olan `ee4aed7`'i **yeşil geçirdi**: kırılan test, contract CI'ında
**atlanan 134 testin** içindeydi (kardeş depo okuyanlar). ⇒ Kardeş-bağımlı kapılar için
CI **süitin ~%11'ini koşmaz**. Yerelde 20 sn'de yeniden üretilir:

```bash
git clone --local . <bos-dizin> && cd <bos-dizin> && pytest    # CI çıktısı birebir
```

⚠️ *"CI yeşil"* bu depoda **"tam süit geçti" demek değildir** — kardeş depo gerektiren
kapılar sessizce atlanır.

---


## 14.10 🔬 DK-43…DK-47 TURU (2026-08-10) — sessiz kusurlar · indeks gerçeği · kart SSOT

> **Bu turda UYGULANANLAR** worker/platform CHANGELOG'larında (DK-43…DK-47).
> Aşağıdakiler **bilerek uygulanmayan** kalemlerdir: karar, veri ya da ayrı bir tur ister.
> Her satırın dayanağı ölçülmüştür; ölçüm komutu/kanıtı ilgili CHANGELOG girdisindedir.

| Kod | Repo | Kalem ve ölçülmüş dayanağı | Neden şimdi değil |
|---|---|---|---|
| **AL-K1** 🟠 | worker | **Aşama-1 eşikleri config'siz, mahsul- ve fenoloji-körü.** `_anomaly_filter` varsayılanları (NDVI<0.55 · stress<0.85 · NDRE<0.15) hiçbir YAML'da yok, üretim çağrısı parametresiz. Kartlar evre-bazlı NDVI aralığı taşıyor (`grape_cards` LEAF_DEVELOPMENT [0.35,0.55]). **Seçicilik-güvenlik cephesi:** görülebilir en küçük lezyon oranı `f* = (h−τ)/(h−l)`; h=0.75, l=0.30, τ=0.55 → **%44**. | Önce gerçek ortomozaikte NDVI/stress histogramı ölçülmeli; eşik değiştirmek ablasyon ister |
| **AL-K2** 🟠 | worker | **Karo içi dağılım atılıyor** (yalnız ortalama). Alt-kantil (p5/p10) + bağlantılı-bileşen sayısı, **sabit donanımda gerçek bilgi kazancı** olan iki eksenden biri (diğeri zaman). | AL-K1 ölçümüne bağlı; yanlış-pozitif bütçesi hesaplanmalı |
| **AL-K3** 🔴 | worker | **Eskalasyon bağımsızlığı ~2 etkin sinyal.** `enable_dualhead=False` → agreement bellek-benzerlik vekili; agreement(<0.6) ve OOD(cosine<0.3) **aynı ölçünün iki eşiği**; belleği boş mahsulde (fıstık) ikisi de susar. Gerçekten bağımsız sinyal (U1 çelişkisi · kart `pattern` uyumu · izole-pozitif komşuluk) eklenmeli. | Yeni tetikleyici = **sözleşme değişikliği** (enum parity + KR-041 hash + kanonik ayna + CHANGELOG ≈ 12 dosya) |
| **AL-K4** 🔴 | worker | **Uzman kuyruğu bütçesi tasarıma girmemiş.** 1M karo/gün'e karşı 40 uzman ≈ 8-20K etiket/gün → toplam eskalasyon bütçesi **~%1-2** ve TÜM tetikleyiciler bu tek havuzu paylaşıyor. Tek yeni tetikleyici bütçeyi tek başına yiyebilir. | AL-K3'ten ÖNCE gelmeli: aile-başı kantil-bütçe tahsisi tasarlanmadan tetikleyici eklenmemeli |
| **AL-K5** 🟠 | worker | **Küre yoğunlaşma kriteri ölçülmüyor.** S^(d−1)'de N kayıt arasında beklenen şans-kosinüsü `≈ sqrt(2·lnN/d_eff)` → τ=0.3 ve N=50K için **d_eff ≥ 240** gerekir. BYOL boyut çöküşü d_eff'i düşürürse OOD dedektörü **sessizce ölür**. Ölçüm ucuz (tek SVD → katılım oranı), encoder terfi kapısına bağlanabilir. | Ağırlık yok (`lora_adapter=null`); ölçülecek embedding GAP saha verisine bağlı |
| **AL-K6** 🟡 | worker | **Hebbian sönümü örtük bir tasarım sabiti.** ×0.95/30 gün → yarı-ömür ≈ **405 gün**; 12 ay sonra ağırlık ≈0.54. Yıllık fenoloji döngüsüne isabetli ama hiçbir yerde "böyle seçildi" yazmıyor. | Örtük sabiti açık parametre yapmak ürün kararı |
| **AL-K7** 🟠 | worker | **Denetim seti hattı hâlâ uykuda** — engel-1 kapandı (`AUDIT_SAMPLE` enum'da, 2026-08-02); kalan engel GAP saha verisi + canlı dedup yayılım yolu. `propagation_metrics.bulk_approval_allowed` toplu-onay amplifikasyonunun **hazır** kontrolüdür. Bağlama noktaları: kurulum `worker.py:476-482`, emisyon `:1274` paraleli. | Veri-kapılı |
| **AL-K8** 🔴 | worker + contract | **Kart ↔ boru hattı termal çelişkisi KALICI hâle geldi.** 9 kart dosyası CWSI istiyor, 3 kart `THERMAL_REQUIRED` şart koşuyor; CWSI hesaplayıcısı **yok**, `THERMAL_AUX_SPEC` hiç seçilmiyor, kanonik `thermal_analysis_result.cwsi` **required**. Kullanıcı kararı (2026-08-10): **yalnız M3M** → çelişki kendiliğinden kapanmayacak. | Ürün kararı; DK-45'te yeni kart bilerek `BASIC_4BAND` yapıldı ki çelişkiye **yeni örnek eklenmesin** |
| **AL-K9** 🟠 | worker + contract | **Üç üretici-ölü özellik.** `economic_impact.estimate_yield_loss` (17 kayıt) · `yield_forecast/` (KR-089) · `index_averages` (KR-088) — üçünün de `src/` içinde çağıranı YOK (ölçüldü, pozitif kontrollü). DK-47'de tanıtım metni gerçeğe hizalandı; **bağlama kararı verilmedi**. `index_averages` için worker üreticisi + `analysis_result` alanı gerekir (contract-first, KR-081). | Ayrı karar: bağlanacak mı, düşülecek mi |
| **AL-K10** 🟡 | worker | **Aynı indeksin iki matematiksel tanımı üretimde.** `feature_extraction.py` NDVI'yi `+eps` ile, `src/indices` `safe_divide` ile hesaplıyor; ikisi de üretim yolunda (A.2 LR yolu). Bilinçli/belgeli (K-6) ama **NaN semantiği DK-38 sonrası ayrıştı**: biri NaN yayar, diğeri eps ile yutar. | Yeniden değerlendirme; DK-43 düzeltmesiyle birlikte tutarlılık kontrolü |
| **AL-K11** 🔴 | worker + platform | **Kart kataloglarında ALAN-DÜZEYİ parite kapısı YOK.** DK-46 sınıf kimliği + içerik özetini kilitledi, ama iki katalog **farklı şema kuşağındaydı** (platformdaki 132 kartın hiçbirinde v2.x alanı yoktu). Bugün bayt-özdeşler; platform ileride kendi alanını eklerse kapı bunu içerik farkı olarak yakalar ama **nedenini** söylemez. | Şema-kuşağı paritesi ayrı iş kalemi |
| **AL-K12** 🟡 | worker | **`confused_with` sarkan referansları izlenmiyor.** Tüm kart dosyalarında **33 ayrı ad / 65 geçiş** hedefsiz. Şema bunu bilerek serbest bırakıyor ("veya genel kavram adı") ve çoğu meşru (`dogal_olgunlasma`, `besin_klorozu`, `maturity`). **Sert kapı YANLIŞ olur** — doğru çözüm ratchet baseline. | Hangi 33'ün meşru kavram, hangisinin yazım hatası olduğu agronomik ayrım ister |
| **AL-K13** 🔴 | worker + platform | **Kart katalog ratchet'i CI'da ZORLANMIYOR.** `scripts/check_card_catalog_drift.py` yalnız iki depo yan yana checkout edilmişse çalışır; worker CI'ında **atlar ve bunu söyler**. Kalıcı çözüm **E17 deseni**: `contracts_gate.yml`'a karşı deponun checkout adımı. Bu yazılmadan kapı "geliştirici-zamanı"dır. | E17 ile aynı mekanizma; birlikte yapılmalı |
| **AL-K14** 🟡 | worker | **HEALTH referans kartı adlandırması tekdüze değil:** 11 dosya `healthy_<crop>`, `rice_cards` **`rice_crop_healthy`**. DK-45'in çözdüğü ad-ekseni sorununun aynısı, küçük ölçekte. Testler bu yüzden ada değil `sub_specialty: HEALTH` alanına bakıyor. | Tek satırlık düzeltme ama DK-45 töreninin aynısını ister (baseline + drift senkronu) |
| **AL-K15** 🟠 | worker | **`spectral_signatures.yaml` iddia edilenin çok altında:** tanıtım 64 kayıt/12 bitki diyordu, ölçüm **9 kayıt / 6 bitki** (wheat, corn, grape, apple, olive, peach). **Pamuk, fıstık ve ayçiçeği atlası BOŞ** — bu üçü L1 atlas isabetinden hiç yararlanamıyor. Platformdaki 13 `spectral_signatures_ref` işaretçisinin 9'u bu yüzden bayattı. | Kalibre saha verisine bağlı (aynı kök: GAP verisi) |
| **AL-K16** 🟡 | platform | **`barley_cards` / `potato_cards` öksüz.** BARLEY/POTATO iki deponun da crop enum'unda yok (platformda yorum satırında, "ARŞİV"). Kartlar silinmedi (ürün açılırsa hazır), worker'a taşınmadı (enum ihlali olurdu). Katalog drift baseline'ındaki **kalan 2 sapma** bunlar. | Ürün kararı: bu iki ürün açılacak mı |
| **AL-K17** 🟠 | worker + contract + platform | **`tile_counts` muhasebesi artık kapanmıyor.** DK-43 üçüncü bir kova (hariç tutulan) yarattı: `_anomaly_filter` düşük kaplamalı karoyu `continue` ile atlıyor (`pipeline.py:2337`), ama `tile_count_total` hâlâ `len(tiles)`. **Ölçüldü:** 3 karo → total=3 · anomaly=1 · healthy=0 → **2 karo hiçbir alanda yok**. Pozitif kontrol: DK-43 öncesi aynı fonksiyonda `continue` **yok** (0 adet) → `total == healthy + anomaly` değişmezi tutuyordu; DK-43 onu kırdı. Kanonik şema (`analysis_result.v1.schema.json:221`) hâlâ **ikili** çerçeve tanımlıyor (*"green-vs-problem"*, `total` = *"tiles scanned"*) — üçüncü kovanın sözleşmede adı yok. **Bugün canlı yanlış rapor YOK** (ölçüldü: platform `src/` **ve** `web/src` bu üçlüyü yalnız saklıyor/taşıyor, türetme yapmıyor — pozitif kontrollü). Risk: `healthy = total − anomaly` diyen herhangi bir tüketici DK-43'ün sildiği hatayı yeniden doğurur. | Kalıcı çözüm **contract-first** (KR-081): şema alanı → worker `PipelineResponse` taşıma → platform sütunu + tüketici → test; MINOR sürüm + üç depo turu. **W8-b ile komşu ama aynı değil** (**§14.9** *Turdan BAĞIMSIZ kuyruk* tablosundaki, `tile_count_total/healthy/anomaly` üçlüsünü açıkça anan kalem): o, denetim çekilişinin popülasyonu; bu, muhasebenin kapanışı — birlikte tasarlanmalı |
| **AL-K18** 🟡 | worker | **`np.errstate(invalid="ignore")` amaçladığı uyarıyı bastırmıyor.** `pipeline.py:2348`: `np.nanmean`'in *"Mean of empty slice"* uyarısı kayan-nokta hata durumundan (`errstate`'in kapsamı) değil `warnings` modülünden gelir. **Ölçüldü:** `pytest tests/unit/test_pipeline_helpers.py -W error::RuntimeWarning` → `test_non_finite_mean_is_never_healthy` **FAILED**; aynı dosya uyarısız **96 passed**. DK-43 bu dosyaya **4 yeni** `np.nanmean` ekledi (diff +4 / −0; 7→11). **Şiddet dürüstçe daraltıldı:** bu yol bugün üretimde **ULAŞILAMAZ** — testin kendi docstring'i söylüyor (`safe_divide` + `_valid_pixel_ratio` + `clip_index` birlikte kapatıyor); uyarı yalnız testin `monkeypatch`'lediği sahte hesaplayıcıyla üretiliyor. Gerçek etki: (a) `filterwarnings = error` açılırsa test kırılır ve `errstate` kurtarmaz; (b) kod niyetini yanlış ifade ediyor — okuyan "bastırılıyor" sanır. | Doğru düzeltme bir davranış kararı ister: uyarıyı `warnings.catch_warnings()` ile hedefli susturmak mı, boş dilimi `nanmean`'den önce elemek mi. Tek satırlık yama yerine, testin öngördüğü gün (kırpma yapmayan yeni indeks, ör. CWSI) ile birlikte ele alınmalı |
| **AL-K19** 🟡 | contract | **Bayt-kilitli şema, silinmiş bir worker dosyasını kaynak gösteriyor.** `schemas/worker/expert_review_queue.v1.schema.json:463` → `"source"` alani `worker denetim/audit_escalation_reason_devir_spec_2026_07_19` §3-B/§4 diyor (gercek dizede `.md` uzantisi VAR; burada kapiyi gevsetmemek icin yazilmadi); o dosya 2026-08-11'de `birlesik_devir_spec_arsivi_2026.md` §9'da birleşti ve **dört deponun hiçbirinde yok** (ölçüldü: `git ls-tree -r` × 4 → 0 isabet). Aynı dize `dist/` kopyasında da var. **Bu turda BİLEREK düzeltilmedi:** `schemas/` checksum kapsamındadır (`tools/pin_version.py:94` `schemas_dir.rglob('*.json')`) → tek karakterlik açıklama değişikliği agrega checksum'ı değiştirir, yeniden pin + platform submodule + worker KR-041 öz-hash'i, yani **tam üç-depo sürüm töreni** ister. Bugün zarar YOK: arşivin §-tablosu eski adı satır başında taşıyor, arayan bulur. | Bir sonraki PATCH/MINOR sürüm törenine **bindirilmeli** — tek başına sürüm yükseltmeyi hak etmiyor. Aynı turda `dist/` kopyası da yeniden üretilmeli |
| **AL-K20** 🔴 | dört depo | **"Sarkan atıf bırakma" kuralının KAPISI YOK — kural bir dilek.** Kök `CLAUDE.md` *"diff olmadan iş yapmak"* diyor ve `tarlaanaliz-docs-cleanup` reçetesi sarkan-atıf taramasını *"en yüksek sinyalli mekanik kontrol"* sayıyor, ama **hiçbir depoda bunu koşturan bir CI adımı ya da test yok** (ölçüldü: `git grep -l "docs/architecture\|docs/README\|DIRECTORY_TREE" -- tests scripts .github` → platformda yalnız `scripts/gen_directory_tree.py`, o da üreteç). Sonuç ampirik: 2026-08-11 turu 83 dosya sildi ve **12 sarkan atıf** hayatta kaldı — 9'u tek bir canlı mimari belgede (`end_to_end_workflow.md`), biri **açık bir DEFER kaleminin** hedefiydi (`open_items_decisions_2026-06.md` #4). Elle tarama üç turda üç kez kaçırdı; sorun dikkat değil **kapı yokluğu**. | ✅ **KURULDU (2026-08-11, DÖRT DEPODA):** `check_doc_links` + ratchet baseline + CI adımı; dört kopya **bayt-özdeş** (blob `91dc7d71…` — yollar `__file__`'dan türetiliyor, elle yazılmıyor). Baseline: contract 99 · platform 96 · worker 185 · edge 24. **SINIR ① 2026-08-11'de KAPATILDI (kısmen — kapsamı ölçüldü):** worker ve edge'in `contracts_gate.yml` içindeki `sibling-parity` işi contract'ı zaten yan yana checkout ediyor (E17); kapı oraya bağlandı + *contract'a ait atlama = 0* ölçümü eklendi. **Nerede bağlanamaz, ölçüldü:** contract→worker/edge ve platform→worker atıfları için hedef depolar **PRIVATE** (`gh repo view --json visibility`: worker/edge/platform PRIVATE, contract PUBLIC) → çapraz-repo token'ı olmadan checkout edilemez; o ayak hâlâ geliştirici-zamanı. **SINIR ② AÇIK.** Eski kayıt: ① **çapraz-repo atıfı CI'da denetlenmiyor** — mutasyonla gösterildi: contract'ın 7 bulgusunun sınıfı (`tarlaanaliz-worker/denetim/…`) kardeş depo checkout DEĞİLKEN atlanıyor (kapı yeşil kalır), kardeş depolar VARKEN kırmızıya döner. Yani bu ayak bugün **geliştirici-zamanı**; CI'da bağlayıcı kılmak **E17 deseni** (karşı depo checkout + token) ister — **AL-K13 ile aynı aile, birlikte yapılmalı**. Atlanan sayı ekrana basılır → sessiz fail-open yok. ② **kısaltılmış ad** yakalanmıyor (`DENETIM_2026-05-31` vs tam kök `..._pentest_ve_kurulum`); önek taraması dört depoda **933 yanlış pozitif** üretiyor (veri seti kimlikleri önek paylaşıyor) → kapıya konulamaz, elle taramayla kapatılır |

> **AL-K17/AL-K18'in kaynağı farklıdır:** bu iki kalem turun kendi öz-denetiminde değil,
> **sonraki oturumun bağımsız denetiminde** bulundu (2026-08-10). İkisi de öz-denetimin
> yapısal kör noktasındaydı — kendi kurduğu çerçevenin *dışını* denetlemek, o çerçeveyi
> kuran gözden beklenemez. Turun kendi öz-denetimi ayrıca **doğrulandı**: DK-43/DK-44
> mutasyon iddiaları bağımsız yeniden koşuldu (3 mutasyon → 2 · 1 · **5** test kırmızı;
> CHANGELOG sonuncusu için 4 diyor, ölçüm 5 — eksik değil fazla) ve 13 kart dosyasının
> bayt-özdeşliği `cmp` ile teyit edildi.

### 📌 Bu turda ölçülüp ÇÜRÜTÜLEN iddialar (tekrar gündeme gelmesin)

| İddia | Neden çürüdü |
|---|---|
| "Platform kart kopyası **bayat**" | Bayat değil, **farklı şema kuşağı** + çift yönlü ayrışma. Ortak 125 kartın 125'inin de içeriği farklıydı; platformda korunacak benzersiz veri **bulunamadı** (5 özel alanın tamamının worker'da karşılığı vardı — değerler birebir aynı ya da worker'da daha zengin; 13 spektral işaretçinin 9'u bayattı) |
| "`healthy_rice` yok" | **VAR** — adı `rice_crop_healthy`. `startswith("healthy")` filtresi kaçırdı. 12 mahsulün 12'sinde de HEALTH referansı mevcut |
| "Aşama-1 fail-open'ı **veri kaybı** üretiyor" | Bu konfigürasyonda **üretmiyordu**: kaçan 11 karonun hepsi `tile_min_valid_ratio=0.20` altındaydı, Aşama-2 zaten atardı. Kusur **muhasebede** (`tile_count_healthy` 11 hiç ölçülmemiş karo sayıyordu) ve **kırılganlıkta** (koruma tek bir belgelenmemiş yan etkiye bağlıydı) |
| "DK-44 `stress_ratio` düzeltmesi platform `WATER_STRESS` katmanını besliyor" | **Beslemiyor.** O katman **tam-görüntü** yolundan besleniyor ve zaten çalışıyordu; tile düzeyindeki `stress_ratio`'nun bugün tüketicisi yok |

---

## 14.13 ⬜ UZMAN EKRANI — REFERANS KARTLARI DAHA DETAYLI OLSUN (2026-08-19, kullanıcı isteği)

**Durum: AÇIK.** Sonraki oturumda ele alınacak; bu turda ölçüm yapıldı, uygulama yapılmadı.

### İstek (kullanıcının kendi ifadesi)

> *"Referans Kartları (Antep Fıstığı — 23 kart)" altındakiler için daha detaylı
> bilgilerin yazılması"*

Uzman, karar ekranında (`/expert-portal/reviews/{id}`) mahsule göre referans
kartlarını görüyor. Antep fıstığında **23 kart** listeleniyor: hastalık, zararlı,
abiyotik stres ve yabancı ot.

### Bugün ekranda ÖLÇÜLEN kart içeriği (gerçek çıktı)

Her kart şu alanları taşıyor: **ad · sınıf** (Hastalık/Zararlı/Abiyotik Stres/Yabancı
Ot) **· etmen (latin adı) · kısa açıklama · Eşik (bazılarında) · Karıştırma**
(ayırıcı tanı adayları).

Örnek — *Fıstık Psillidi*: `Agonoscena pistaciae` · eşik *"bileşik yaprak başına
25-30 nimf (TAGEM EZE)"* · karıştırma `water_stress, alternaria_blight`.

**Yani iskelet iyi; eksik olan derinlik.** Kartların bir kısmında eşik yok
(ör. *Verticillium Solgunluğu*, *Septoria*), bazılarında izleme penceresi metin
içine gömülü (*"Ergin uçuşu Nisan-Mayıs ortasında"*) ve yapısal bir alanı yok.

### 🔴 ÖNCE ÖLÇÜLECEK — kart kataloğunun SSOT'u worker'dadır

`kart-katalogu-worker-ssot` (2026-08-10, DK-46): **platform kartların bayt-özdeş
kopyasını tutar, ikinci değer üretmez.** Dolayısıyla:

* İçerik zenginleştirmesi **worker'daki kanonik katalogda** yapılır, platformda DEĞİL.
* Platform tarafı yalnızca **sunum** (hangi alan gösteriliyor, nasıl yerleşiyor).
* Ratchet kapısı **geliştirici-zamanı**; CI'da zorlanmıyor (AL-K13) → senkronu elle ölç.

Uygulamadan önce şu üçü ölçülmeli:
1. Kanonik kart şeması hangi alanları **zaten** destekliyor (eklemeye gerek var mı)?
2. Ekran hangi alanları **gösteriyor**, hangileri şemada var ama sunulmuyor?
   (Bu oturumda üç kez çıkan sınıf: *"alan var, tüketici yok"*.)
3. Kart sayısı ve içerik platform ↔ worker arasında bayt-özdeş mi?

### Kapsam sınırı (KR-025)

Kartlar **tanı desteği**dir. İlaçlama/müdahale önerisi **eklenmez** — yapay zekâ
analiz yapar, müdahale kararı vermez. Derinleştirme; etiyoloji, fenoloji, ayırıcı
tanı, izleme yöntemi ve eşik yönünde olur.

### Bu isteğin çıktığı bağlam

Uzman ekranı gerçek bir incelemede açıldı (`548673e0`, Ferda Yarpuzlu) ve ekran
**fail-honest davrandı**: *"Bu inceleme için görüntü bulunamadı … Görüntüyü
görmeden karar vermeyin"*. Ölçüldü: `analysis_priority_zones` **0 kayıt**,
`layer` tablosu **0 kayıt** — çünkü o analiz sonucu (`08b3cac3`) **gerçek worker
koşmadan** üretilmişti. Kartlar o yüzden ekranın tek içeriğiydi; istek oradan doğdu.

---

## 14.14 → 📦 ARŞİVDE

> Uzman ekranı zinciri turu (2026-08-19/20, 201 satır) `EYLEM_PLANI_ARSIV_2026-08.md`'ye
> taşındı; kendi başlığı zaten *"süperseded: canlı giriş §14.17"* diyordu.
> Tek açık kalemi (**uzman yönlendirmesinin kalibrasyonu**) §14.A'da canlı listede.

---


## 14.17 ▶️ SONRAKİ OTURUM — **BURADAN BAŞLA** (2026-08-21 kapanışında yazıldı)

> Her satır bu turda **ölçüldü**. Tahmin yok; ölçülemeyen "ölçülmedi" diye yazılı.
> Önceki tur §14.16'da anlatılıyor, oradaki 5 kalem hâlâ geçerli.

### Bugün nerede duruyoruz — üç ayrı cümle

| Cümle | Durum | Kanıt |
|---|---|---|
| **Merge edildi** | ✅ Dört depo `7.8.0` hizalı, temiz, CI yeşil | `gh pr list --state merged --search "merged:2026-08-21"` |
| **Dağıtıldı** | ❌ **HAYIR.** Üretim `7.7.2` kodunu koşuyor | prod backend içinde `analysis_job_started` grep → **0**; `contracts/CONTRACTS_VERSION.md` → `7.7.2` |
| **Çalışıyor** | 🟡 Worker **bağlı**, iş **akmıyor** | `analysis_jobs` → tüketici **1**, mesaj **0**; 3 iş hâlâ PENDING, `started_at` NULL |

### 🔄 DURUM GÜNCELLEMESİ — 2026-08-24 (ölçüldü; §14.17 gövdesi bu tarihte bayatladı)

> ⚠️ **Y-1 ve Y-2 ARTIK AÇIK DEĞİL.** §14.17 aşağıda ikisini *"yeni kusur"* diye anlatır;
> o metin **2026-08-21'in fotoğrafıdır** ve tarihsel kayıt olarak duruyor. Bugünün
> doğrusu bu tablodur.

| §14.17'de yazan | 2026-08-24 ölçümü |
|---|---|
| **Y-1** `IDEMPOTENT_SKIP` işi PROCESSING'de bırakıyor | ✅ **KAPANDI** — platform **#458** (`RK-1`): SKIP dalı ikinci işin (REFLY) sonucunu da kalıcılaştırır; iş-eksenli ve idempotent, NORMAL dal dokunulmadı. + **AST mandalı** (RK-3) |
| **Y-2** yayıncı bayat bağlantıda ölüyor | ✅ **KAPANDI** — worker **#248**: bir kez yeniden bağlan + dene |
| **Ö-1** üretim kimlikleri korumasız | ✅ **KAPANDI** — contract **#114** (+5 yerel `settings.json`): deny şablonuna `.sim-worker-prod.env` |

**Aynı turda kapanan, §14.17'nin hiç bilmediği kök nedenler** (17-ajanlı bağımsız
denetimden çıktı — 31 kritik+yüksek bulgu → 13 kök neden):
platform **#459** `RK-2` K2+K3 (durum-makinesi eksen-çaprazı, **pre-existing KRİTİK**) ·
platform **#460** `RK-11` (Ö-3 fail-open) + `RK-4` (eskalasyon dedup) + `RK-10` (git-izli dev
config) · platform **#461** `B05-K1`/`B06-K1` · worker **#250** `RK-5` (kök
`sim-worker-baglan.sh` **silindi**, ürün sahibi onayıyla) + `RK-13` conftest DLL guard ·
worker **#251**/**#252**.

🔴 **`RK-11`'in TEK ZAYIF HALKASI de kapandı — `T02` (platform `a6791019`).** Bağımsız
denetim ölçtü, paralel oturum doğruladı: **`APP_ENV=prod` (yazım hatası) sessizce
geçiyordu** → `get_current_environment("")` = `'prod'` → `in ("production","staging")`
**False** → RK-11 dâhil **tüm strict boot kapıları fail-OPEN**. Asimetri ölçüldü:
`TARLA_ENVIRONMENT=prod` boot'u çökertiyor, `APP_ENV=prod` çökertmiyordu. Ayrıca
`mtls_verifier.py` ve `ingest.py` bu helper'ı **hiç kullanmıyordu** → yalnız
`TARLA_ENVIRONMENT=production` verildiğinde ortamı `development` sanıyor, kayıtsız cihaz
sertifikasını kabul ediyorlardı. Kanıt: `src/infrastructure/config/env_helper.py:24`
(kusuru **kendi docstring'inde** belgeliyor) + `settings.py:150`.
⇒ *"Kapı kuruldu"* ile *"kapı gerçekten kapanıyor"* ayrı cümlelerdir; RK-11 **iki adımda**
kapandı.

#### 🔀 Paralel oturum — şerit ayrımı (çakışma YOK)

Bu tur **iki oturum aynı çalışma ağacında** yürüdü. Ayrım ölçüldü ve karşılıklı korundu:
diğer oturum `SESSION_HANDOFF.md` + kod düzeltmelerini aldı, **bu dosyaya (eylem planı)
hiç dokunmadı** (`git diff --stat f65aafe..ef2bc38` → yalnız handoff + settings şablonu).
Kendi devir notlarına da yazdılar: *"contract EYLEM_PLANI working tree'de başka aktörün
commit'lenmemiş kiraz-doküman değişikliği vardı — **dokunulmadı**."*
Hafıza kaydı: `tarlaanaliz-paralel-oturum-riski`.

⚠️ **Devir notunun "kalan açık kök nedenler" listesi RK-4/RK-10/RK-11'i bir süre AÇIK
saydı — oysa kapalılardı.** Hata değil, **zaman sırası**: not `12:24`'te yazıldı, #460
`13:13`'te, #461 `17:43`'te merge edildi. Not **aynı gün #116 ile düzeltildi** (liste
artık KAPANDI/AÇIK olarak ayrılıyor ve her kapanış **PR numarasına** bağlı); gerçek
ayrıca buraya da yazıldı — **iki dosya artık hemfikir**. *Sayıyı komuttan al:*
`gh pr list --repo physiscs-zana/tarlaanaliz-platform --state merged --search "merged:>=2026-08-21"`

#### Bugün ne AÇIK kaldı

| Durum | Kanıt |
|---|---|
| **Açık PR: SIFIR** (dört depo) | `gh pr list --repo <depo> --state open --json number --jq 'length'` → `0 0 0 0` |
| ✅ **Dağıtım YAPILDI** (`RK-9` kapandı) — 2026-08-24, ürün sahibi | Üretim `a2af40ec` → `65c4880a`. Canlıda: #455 · #456 · #458 · #459 · #460 · #461 · #462. Dağıtım kapıları kanıt üretti: `contracts=6569144342da (v7.8.0)` (submodule DOLU) · `CONFIG_OK` · `RASTER_OK 1.26.4 1.4.4` · tazelik `geride=0 önde=0`. ⚠️ **İkinci el kanıt** — dağıtım çıktısından okundu; bu oturum üretimi **bağımsız doğrulayamadı** (dışarıdan her uç `401` döner ve `401` sürüm kanıtı DEĞİLDİR) |
| ✅ **Zincir TAM BAĞLI (2026-08-24)** | Üretim kuyrukları: `analysis_job_started` **2** · `analysis_results` **2** · `expert_review_queue` **2** · `analysis_jobs` **1** (worker bağlandı; önceki ölçümde 0 idi ve ondan önce kuyruk **404**'tü). Köprü SSH tünelidir ve kalıcı değildir; **tünel gözetmeni** (worker #255) oturum açılışında tüneli kendi kurar — canlılığı TCP ile değil **broker cevabıyla** ölçer, yarı-açık oturumu kapatıp yeniden kurar. 🔴 **Hâlâ ölçülmemiş:** gerçek bir işin uçtan uca akması (kuyruklarda 0 mesaj). *"Bağlı" ≠ "akıyor".* |
| ✅ **`SENTRY_DSN` DOLDURULDU (2026-08-24)** | AB bölgesi (`ingest.de.sentry.io`) — veri Avrupa'da kalır, KVKK açısından doğru. Kanıt zinciri: ön-uçuş uyarısı **11→10** · `sentry_initialized` loglandı · test olayı Sentry'ye **ulaştı**. `SENTRY_TRACES_SAMPLE_RATE=0.1` (kod varsayılanı 0.0'dır, yani bu değer olmadan HTTP izleme kapalı kalırdı). Kod `send_default_pii=False` ile koşuyor (KR-050) |
| Kalan kök nedenler (beyan) | `RK-6` sır yönetimi (kabul edildi: tek koruma dosyanın yokluğu) · `RK-7` mahsul seti tek SSOT'tan okumuyor · `RK-8` fıstıkta eğitimsiz model + kalibre olmayan güven |

🔴 **Dağıtım YAPILDI, davranış hâlâ ölçülmedi.** #458/#459/#460 üçü de *"iş asılı
kalıyor / sonuç kayboluyor"* sınıfındandır; artık canlıdalar ama **görüldükleri**
anlamına gelmez — mandalların bir kısmı **AST**'tir ve yalnız YAPIYI doğrular.
Sıradaki iş kod değil **ölçüm**: kuyruk + tüketici + durum geçişi.

⚠️ **Bir dağıtım REDDEDİLDİ ve bu ARIZA DEĞİL, kapının çalışmasıdır.** plat #463
merge olunca sunucudaki checkout 1 commit geriye düştü ve `deploy_prod.sh` 0c tazelik
kapısı **fail-closed** durdu — PR #449 tam bunun için yazılmıştı. Ölçüldü: #463
**yalnız test** (1 dosya, `test_mtls_verifier_dev_bypass.py`) → üretimde
çalışma-zamanı eksiği **yok**. Hizalama: `git pull --ff-only origin main` ve
`git submodule update --init --recursive`, sonra yeniden dağıtım.

⚠️ **Kısayol uyarısı:** dağıtım bir kez reçetenin dışında, tek başına
`git pull origin main` ile (submodule güncellemesi olmadan) koşuldu. Bu sefer zararsız
kaldı çünkü submodule zaten v7.8.0'daydı. Ama **RK-11 artık boş `contracts/` ile boot'u
REDDEDİYOR** → aynı kısayol bir dahakine doğrudan kesinti üretir.

##### Bu turun kendi ölçüm dersi (kayda geçiyor)

Bu bölümün **ilk hâli** *"Y-1 push bile edilmemiş, Y-2'nin PR'ı yok, 08-22'den beri sıfır
merge"* diyordu. **O ölçüm yapıldığı anda DOĞRUYDU** (`origin/main` = `0982887e`), ama
paralel oturum aynı gün içinde ikisini de kapattı. Ders: *"ölçtüm"* ile *"hâlâ geçerli"*
ayrı cümlelerdir — **çok aktörlü çalışmada ölçümün raf ömrü saatlerdir**; yazmadan önce
`git fetch` tekrarlanır.

### 🔴 ÖNCELİK 1 — Zinciri GERÇEKTEN akıt (tek turda kanıtlanabilir)

Bugün zincirin **her halkası kodda hazır** ama uçtan uca **bir kez bile
akmadı**. Sıra önemlidir; her adım bir öncekini kanıtlar:

- [ ] **1a. Platformu üretime dağıt.** Bu yapılmadan `analysis_job_started`
      tüketicisi üretimde YOK; worker sinyali yayınlar, **kimse dinlemez** ve
      `analysis_jobs.status` yine ilerlemez. Ölçüldü: prod backend'de o kuyruk
      adı **hiç geçmiyor**.

      🔴 **ELLE `git pull && docker compose build/up` ZİNCİRİ KOŞMAYIN.**
      `git pull` **submodule'ü güncellemez** → `contracts/` boş/bayat kalır.
      Bu, 2026-08-17 ve 2026-08-18 kesintilerinin sınıfıdır; **bu kez daha
      sert**: `RK-11` artık fail-closed olduğu için boş `contracts/` **boot'u
      doğrudan reddeder** — eskiden sessiz olan hata şimdi görünür kesinti.
      Tek doğru yol:

      ```bash
      git submodule update --init --recursive && bash scripts/deploy_prod.sh
      ```

      `deploy_prod.sh` bunu **kendisi de denetler** (`scripts/deploy_prod.sh:82-92`,
      submodule `-`/`+` durumunda fail-closed durur) ve adım **0c** ile bayat
      checkout'ta *"DAĞITIM TAMAM"* demeyi engeller.
      ⚠️ Dağıtımdan **önce** yerelde davranışsal koşum yapın: #458/#459/#460
      üçü de *"iş asılı kalıyor / sonuç kayboluyor"* sınıfıdır ve **AST
      mandalları yalnız YAPIYI doğrular**, davranışı değil.
- [ ] **1b. Worker'ı bağla** — `bash tarlaanaliz-worker/scripts/sim-worker-baglan.sh`
      (tünel + konteyner + doğrulama tek komutta). Bugün çalıştı; **tünel makine
      yeniden başlayınca gelmez**, o yüzden her oturumda yeniden koşulur.
- [ ] **1c. BİR iş sevk et.** Üretimdeki 3 PENDING işin **mesajı kayıp**
      (ölçüldü: `event_outbox` `published_at` DOLU ama kuyrukta 0 mesaj ve broker
      2026-08-18'den beri yeniden başlamamış). Worker'ın sonradan bağlanması o
      mesajları geri getirmez → **yeni bir sevk şart**.
      ⚠️ Bu üretim verisine yazar; **ürün sahibinin onayıyla** yapılmalı.
- [ ] **1d. Ölç:** `analysis_jobs.status` PENDING → PROCESSING → COMPLETED,
      `started_at`/`completed_at`/`duration_ms`/`output_manifest` dolu mu?
      `input_manifest` satılan/sevk edilen/teslim edilemeyen üçlüsünü taşıyor mu?

### 🔴 ÖNCELİK 2 — ⬜ İNSANA ait karar 5 *(kiraz buradan ÇIKTI → §13.1 **B13-1**)*

> **Kiraz kararı 2026-08-24'te ürün sahibi tarafından ERTELENDİ.** Gövde artık
> §13 *"BİRİKMİŞ İŞLER — EKİM 2026 VE SONRASI"* içindeki **B13-1**'de yaşıyor;
> buraya ikinci kopya yazılmaz. **Slot silinmedi**, çünkü §14.15 tablosu buraya
> iki yerden atıf yapıyor ve taşıdığı **insan kararı 5** kirazdan bağımsızdır
> (aşağıda duruyor). Silseydim iki sarkan atıf üretecekti.

🔴 **Bu slot zaten bir kez YANLIŞ açılmıştı.** Kiraz **2026-07-31'de** ölçülüp
kapatılmış ve §13'e alınmıştı — KG-0.d-EK: *"kod değişikliği **YAPILMADI**;
KİRAZ'ı ticari olarak açma işi §13 birikmiş işler listesine (Ekim 2026+) alındı."*
§14.17 onu 2026-08-21'de **yeniden "ürün kararı bekliyor"** diye açtı ve o
kapanışa hiç atıf yapmadı. Yani bugünkü erteleme yeni bir karar değil, **2026-07-31
kararının geri getirilmesidir**.

**Ertelemenin bedelsiz olduğu ÖLÇÜLDÜ (2026-08-24):**

| Kaynak | Bugünkü değer | Anlamı |
|---|---|---|
| `crop_type.py:81` → `GAP_OFFERED_CROPS` | `{COTTON, CORN, PISTACHIO, GRAPE}` | **CHERRY YOK** → tarla bile açılamaz; sipariş **SUNUM** kapısında kesilir |
| `data/crop_readiness.json` → `CHERRY` | `{stage1: pilot, data_status: limited, bookable: true}` | **TESLİM** kapısı "evet" der |

İkisi **ayrı eksendir** (SUNUM ⟂ TESLİM, `crop_type.py:50-68`). §14.17'nin
*"kiraz siparişi fail-closed kesiliyor"* cümlesi **doğru ama eksik**: sipariş o
kapıya hiç ulaşmaz, daha önce SUNUM kapısında düşer. ⇒ **bugün canlı risk yok**,
erteleme bedelsizdir.
⚠️ `bookable: false` yazmak ayrıca **teknik olarak yanlış** olurdu:
`tests/unit/test_crop_readiness_manifest_sync.py` `bookable == (stage1 ∈
{production, pilot})` kuralını bağlar ve CHERRY'nin `stage1`'i gerçekten `pilot`.

#### ⬜ Devralınan insan kararı 5 — **HÂLÂ AÇIK** (kirazdan bağımsız)

*Uzmanı (KR-019 inceleyicisi) olmayan bir katman sevk edilebilir mi?*
§14.15'ten devralındı; kiraz kalemine yalnızca *"ikisi de satılabilirlik ↔ teslim
edilebilirlik ekseninde"* diye **iliştirilmişti**. Kiraz taşındı, bu karar kaldı.
Bugünkü pratik etkisi **hâlâ ölçülmedi** (2026-08-21 beyanı bugün de geçerli).

### 🟠 ÖNCELİK 3 — Worker kurulumunun 5 kırılganlığı

Ayrıntı ve kanıt `SESSION_HANDOFF.md` §0.A tablosunda. Özet:
tünelin **otomatik başlatması yok** (yeniden başlatmada ~6 dk'lık sonsuz çökme
döngüsü) · üretimde **tüketicisiz kuyruk** riski · üç kuyrukta **DLQ yok** ·
**imaj 7 gün bayat** (tazelik yalnız bind-mount'tan) · kapsayıcı kökte
**ayrışmış ikizler** (silme **onay** bekliyor).

### 🟠 ÖNCELİK 4 — §14.16'nın 5 açık kalemi

fan-out · `analysis_type` adının 7 anlamı · SSOT metni ↔ enum çelişkisi (8 mi 11
mi — **kırıcı**, insan kararı) · eski geri düşüş yolu · ölü `check_ssot_compliance`.

### 🟡 ÖNCELİK 5 — Kapı asimetrisi (kural↔kapı envanterinden)

`check_doc_facts.py` **yalnız worker'da**. Bu turda platform `CLAUDE.md`'de
**5 bayat satır atfı** ve contract'ta **11 koşmayan yayımlanmış komut** bulundu —
ikisi de tam o kapının sınıfı. Platform + edge'e taşımak, sınıfın tekrarını
engelleyen **tek yapısal önlemdir**.

### 🟢 YEREL UÇTAN UCA KOŞUM (2026-08-21) — zincir **İLK KEZ AKTI**

> Ürün sahibinin kararı: *"önce yerelde kanıtla"*. Gerekçe ölçülmüştü — üretimde
> `analysis_job_started` kuyruğu **YOK** (`404 NOT_FOUND`), yani üretim 7.8.0 öncesi
> kodu koşuyor ve durum zinciri orada **görünemezdi**. Bağımsız kanıt: 7.8.0
> tüketicisi açılışta o kuyruğu *declare eder*; kuyruk hiç doğmamış.

**Yerel yığın önce ONARILDI (Ö-2):** backend 381 başarısız sağlık kontrolüyle ölüydü.
Kök neden ölçüldü ve **teşhis bir kez düzeltildi**: kapı `/app/contracts/…` değil
**`/app/CONTRACTS_VERSION.md`** okuyor (`main.py:117` → `contracts_base.parent` = `/app`).
`src/` mount'lu (taze), platformun kök dosyaları imaja gömülü (2026-08-13, `7.7.2`).
Çözüm yama değil, **tazelik simetrisi**: üç mount birlikte
(`contracts/` + `CONTRACTS_SHA256.txt` + `CONTRACTS_VERSION.md`).
Sonuç: `contracts_integrity_verified checked=98` · `contract_orchestration_guard_wired
pinned='7.8.0'` · nginx `200` · login ucu `422` (uç VAR kanıtı).

**Kanıtlanan halkalar** (iki koşum, `analysis_jobs` kuyruğuna kanonik
`build_analysis_job_v1` + `publish_analysis_job` ile — elle alan uydurulmadı):

| Halka | Kanıt |
|---|---|
| ① Katmanlar **`GENERAL` değil** | `ANALIZ_PAKETI.TESLIM_EDILEMEYEN crop=PISTACHIO satilan=[HEALTH,DISEASE,PEST,FUNGUS] sevk=[DISEASE] edilemeyen=3×MODEL_YOK` → mesajda `analysis_types: ['DISEASE']` |
| ② PENDING → **PROCESSING** | iş `ab990df4`: worker `analysis_job_started` yayınladı → `WORKER_BRIDGE.JOB_STARTED` → `started_at=14:34:28` **ilk kez doldu** |
| ② → **COMPLETED** | iş `01d6f7fc`: `completed_at` dolu, `duration_ms=36103`, `output_manifest` yazıldı |
| Bilinçli `PENDING→COMPLETED` düşüşü + uyarısı | `ANALYSIS_JOB.BASLADI_SINYALI_KAYIP … started_at BOŞ kaldı (kanıt kaydın kendisinde)` — tasarlandığı gibi |
| Worker hattı | `pipeline_completed duration_ms=30447 result_mode=INDICES_ONLY confidence=0.311`, 4 katman + **karo kırpıntıları** S3'e |

#### 🔴 Bu koşumun ÇIKARDIĞI İKİ YENİ KUSUR

| # | Kusur | Kanıt ve neden önemli |
|---|---|---|
| **Y-1** 🔴 | **`IDEMPOTENT_SKIP` işin COMPLETED geçişini ATLIYOR.** `worker_bridge_consumer.py:1618` çıplak `return`; COMPLETED geçişi `:1782`, yani **sonra**. Görev `PENDING_REVIEW`/`DONE`/`EXPERT_REJECTED` ise sonuç mesajı tümden atlanır ve **iş sonsuza kadar PROCESSING'de kalır**. | Canlıda ölçüldü: iş `ab990df4` analizi 30 sn'de BİTTİ, sonuç S3'e yazıldı ve **`analysis_results` satırı veritabanında MEVCUT** (`result_id=fcb65f99…`) — buna rağmen iş hâlâ `PROCESSING`. Çürütme turu iddiayı **güçlendirdi**: `analysis_jobs.status`'u COMPLETED'a çeken **tek** üretici `:1785`'tir (ölçüldü, alternatif yol yok), o da atlanan dalın içindedir. Yani bu, ②'nin kapattığı *"sonuç var ama iş PENDING"* hâlinin birebir tekrarıdır — yalnızca bir adım sonrasında. **Tasarımla erişilebilir:** admin sevk ucu *"ikinci veri seti bir arıza DEĞİL, meşru bir iş durumudur"* diyor (REFLY/yeniden kalibrasyon) ve KR-019 reddi görevi yeniden analize yollar. Aynı görevin İKİNCİ işi bu delikten düşer. ⚠️ Bu, ②'nin kapattığı kusurun **bir adım sonraki** hâlidir. |
| **Y-2** 🟠 | **"İş başladı" sinyali BOŞTA KALMIŞ bağlantıda ölüyor.** `publisher.publish()` → `queue_declare` → `StreamLostError: Connection reset by peer`. Best-effort tasarım işi kurtardı (doğru), ama PROCESSING sinyali kayboldu. | 2 sevkin **1'inde** oldu (14:38:11). Worker'ın normal hâli *boşta beklemek* olduğu için bu, istisna değil **olağan** yol. Yani yeni kurulan sinyal üretimde sık sık kayıp olacak ve *"kuyrukta mı, koşuyor mu"* ayrımı yine bulanıklaşacak. Sonraki yayınlar başarılı → bağlantı kendini toparlıyor, eksik olan **ilk çağrıda yeniden deneme**. |

#### Bu koşumun KANITLAMADIĞI (sessiz borç değil, beyan)

* **Ingest → AV1 → AV2 → sevk** üst zinciri koşulmadı. Sevk kapısı yalnız
  `CALIBRATED_SCANNED_CENTER_OK` kabul ediyor (doğru davranış); yereldeki iki veri seti
  **analiz sonrası** durumda. Taze veri seti yerel ingest ister ve o **üç ayrı
  yapılandırma** ister: yerel nginx'te 8443/istemci-sertifikası sonlandırması yok ·
  `client.pem` parmak izi (`7cccee5c…`) backend'de kayıtlı olanla (`3bb10fc6…`)
  **uyuşmuyor** · mTLS başlıklarını vekil üretmeli.
* **Üretim ölçümleri yapılmadı** (SSH bu oturumda kesildi). Üretim hakkındaki tek
  ölçüm kuyruk sondasıdır: `analysis_jobs` tüketici 1 → 0 (tünel düştü),
  `analysis_job_started` **yok**.
* **Yerel veri değişti (beyan):** pozitif kontrol için görev `591ba3da` elle
  `DONE → ANALYZING` yapıldı; zincir onu kanonik olarak `PENDING_REVIEW`'a taşıdı.
  Yalnız YEREL veritabanı; üretim verisine dokunulmadı.
* **Tünel düştü:** oturum başında ayaktaydı (`ssh -f -N`, 12:20), sonra kayboldu ve
  worker **32 kez** yeniden başladı — devir notundaki *kırılganlık #1*'in canlı
  gerçekleşmesi.

---

### 🔬 ÖZ-DENETİM (2026-08-21, kapanıştan 22 dk sonra) — 5 bulgu, hepsi ÖLÇÜLDÜ

> Ürün sahibi kapanıştan hemen sonra §14.16/§14.17 turunun öz-denetimini istedi.
> **Önce doğrulananlar** (önceki oturum bunları DOĞRU söylemiş): 11 PR merge
> (`gh pr list … merged:>=2026-08-21` → 4+3+3+1) · dört depo temiz ve `7.8.0` hizalı ·
> I-3 submodule bayt-özdeş · zincirin üç halkası da kodda · **KESTİRME kapısı
> mutasyonla sınandı** (blok bozulunca `exit=1`, geri alınca `exit=0`) · **worker
> "iş başladı" sıra testi mutasyonla sınandı** (çağrı silinince kırmızı) · 35 test yeşil.
>
> Aşağıdaki 5 bulgu **beyan edilmemişti**.

| # | Bulgu | Kanıt (bu turda ölçüldü) |
|---|---|---|
| **Ö-1** 🔴 | **Üretim kimlikleri düz metin, korumasız, kapsayıcı kökte.** `.sim-worker-prod.env` üretim RabbitMQ **ve** MinIO parolalarını taşıyor. Betiğin kendi belgesi `rm -f .sim-worker-prod.env  # kimlikleri sil` diyor — **silinmedi**. | Beş `settings.json`'ın `permissions.deny` listesinde `git_token` **3/3** var, `sim-worker-prod` **0/5**. Hiçbir devir belgesinde geçmiyor (`grep -rn "sim-worker-prod.env" docs/` → 0). |
| **Ö-2** 🔴 | **Yerel platform yığını ÖLÜ ve bunu bu turun kendi değişikliği öldürdü.** backend 381 başarısız sağlık kontrolü, nginx **502**. Oturum *"worker healthy"* diye kapandı; **platformun öldüğü hiç ölçülmedi**. | Kök neden: `main.py:187` pin `7.8.0` (mount'lu `src` → taze) ↔ `/app/contracts/CONTRACTS_VERSION.md` **`7.7.2`** (imaja gömülü, imaj **2026-08-13**). backend compose YALNIZ `./src:/app/src:ro` mount ediyor — `contracts/` mount **YOK**. Konteyner 12:11'de başlatıldı, pin 11:30'da merge edildi → 85 dk boyunca oturum içinde ölüydü. |
| **Ö-3** 🔴 | **Sürüm kapısı YANLIŞ YÖNE fail-closed.** Sürüm *eskiyse* keser; dosya *hiç yoksa* **geçirir**. Daha az tehlikeli hâli kesip daha tehlikelisini geçiriyor. | `contract_orchestration_guard.py:123-129` → `if not cv_path.exists(): logger.warning(...); return`. Canlı ölçüm (backend konteynerinde koşuldu): **(A)** sürüm ESKİ → `ContractsVersionError` ✅ · **(B)** dosya YOK → **geçirdi** ❌. (B) tam olarak 2026-08-18 üretim senaryosudur (**boş submodule** → çiftçi ekranı kararır). |
| **Ö-4** 🟠 | **Kural gövdesindeki I-2 komutu yanlış beyan ediyor.** *"temiz `vX.Y.Z` dönmeli"* diyor; bugün `v7.8.0-3-g1b8b93c` dönüyor. Değişmez KIRIK DEĞİL (etiket release commit'inde, sonraki 3 commit yalnız `docs/`) — **komutun beklentisi** yanlış. | `git -C tarlaanaliz-contract describe --tags HEAD` → `v7.8.0-3-g1b8b93c`. Sınıf: *"yayımlanmış ama koşmayan komut"* — önceki oturumun contract'ta **11 örneğini** kapattığı sınıfın kendisi, kendi taşıdığı dosyada (`docs/workspace/calisma-alani-kurallari.md`). |
| **Ö-5** 🟠 | **Kökte ayrışmış ikizler + hiç beyan edilmemiş bir artefakt.** Kök `sim-worker-baglan.sh` **242** satır, git'teki **301** — kök kopya eski atası. `sim-worker-prod.yml` de ayrışmış. **Ek:** boş `tarlaanaliz-platform;C` dizini (PowerShell artefaktı, 2026-08-19) — hiçbir belgede geçmiyor. | `diff <(tr -d '
' < sim-worker-baglan.sh) …/scripts/sim-worker-baglan.sh` → `_koku_bul()` fail-closed kök çözümü kök kopyada **YOK**. İkizler §14.15 kalem 11'de beyan edilmişti (silme onay bekliyor); `;C` dizini edilmemişti. |

**Ö-2 + Ö-3 birlikte okunmalı:** aynı mekanizmanın iki yüzü. Yerel yığın bugün
Ö-2'nin *fail-closed* yüzünü yaşıyor (gürültülü, görünür, zararsız). Üretim
2026-08-18'de Ö-3'ün *fail-open* yüzünü yaşadı (sessiz, görünmez, çiftçi ekranı
karardı). **Kapıyı düzeltmeden yapılacak bir üretim dağıtımı ikinci yüzü tekrar riske atar.**

⬜ **Ö-1 · Ö-3 · Ö-4 · Ö-5 bu turda AÇIK bırakıldı** (ürün sahibi öz-denetim istedi,
uygulama istemedi). Ö-2 dağıtım/imaj tazeleme işidir, ÖNCELİK 1a ile aynı turda kapanır.

---

### 🟠 ÖNCELİK 5-B — §14.15'ten DEVRALINAN açık borç (11 kalem)

> Bu tablo 2026-08-20'de §14.15'te ölçüldü. §14.15 gövdesi 2026-08-21'de daraltılırken
> tablo **buraya taşındı** — §14.17 onu tek satırlık *"kapı asimetrisi"* özetine
> indirmişti ve 11 kalemin **10'u** o özette görünmüyordu. Taşıma, silmeden ÖNCE yapıldı.

#### Kalemler (ölçüldü 2026-08-20, §14.15'ten devralındı)

| # | Kalem | Neden bu turda kapanmadı |
|---|---|---|
| 1 | `check_ssot_compliance.py` ölü (platform) | Bağlanması **ürün kararı**: BOUND'un 3. kopyası, yığın limiti `CLAUDE.md` ile çelişiyor (40/50/80/100 ↔ 50). Silmek **onay** ister. |
| 2 | Kapı betiğinin kendi testi **1/4 depoda** | Yalnız platform'da `test_kestirme_yok_kapisi.py` var (bu turda 2 test eklendi). contract/worker/edge'de yok. |
| 3 | "Belge ↔ kapı paritesi" kapısı **1/4 depoda** | `check_doc_facts.py` yalnız worker'da. Bu turdaki 2 ve 3 numaralı kusuru yakalayacak kapı platform ve edge'de **yok**. |
| 4 | platform `crop_readiness` worker-paritesi CI'da **skip** | Kardeş depo checkout edilmiyor (3 skip). Worker'ın `contracts_gate.yml`'i bunu yapabildiğini kanıtlıyor. |
| 5 | worker kart kataloğu ratchet'i CI'da **skip** (8 test) | Aynı sebep; `check_card_catalog_drift.py` hiçbir workflow'da çağrılmıyor. |
| 6 | ADR-002 (worker `drone_registry.yaml`'a erişemez) **tamamen kapısız** | Tek zorlama bir PR şablonu onay kutusu. Ayrıca ADR-002 kimliği bu depoda **iki ayrı şeye** işaret ediyor → kimlik-grep'i yanlış güven veriyor. |
| 7 | KR-025+ "kart YAML'ında ilaç adı/marka yasak" **kartları görmüyor** | `validate_expert_labeling_card` yalnız şema doğruluyor; gövde tarayıcı yalnız `ipm_corpus`'ta koşuyor. Ham tarayıcı doğrudan kapı yapılamaz: 13 karta uygulandı → 3 isabet, **üçü de meşru** (direnç ekolojisi + kaynak atfı) → **taban listesi (ratchet) gerekir**. |
| 8 | Test kabul ölçütlerinin (11 madde) **hiçbiri** CI'da zorlanmıyor | Mutasyon koşucusu platform'da **var** ama hiçbir workflow çağırmıyor; worker'da hiç yok. |
| ~~9~~ ✅ | ~~Oturum kancası **iki gövde**~~ — **KAPANDI 2026-08-20** | Kök `settings.json` git'teki kanonik dosyayı, dört depo `settings.json` **makine-yerel** kopyayı gösteriyordu. İçerik özdeşti (ölçüldü, fark yalnız satır sonu) ama sapmayı engelleyen hiçbir şey yoktu; üstelik kural *"depo içinden başlat"* dediği için **pratikte koşan makine-yerel kopyaydı** → `KURULUM.md`'nin *"git pull kancayı da günceller"* vaadi o yolda geçersizdi. **Düzeltildi:** dördü de kanonik gövdeyi gösteriyor; kanca yeni yoldan koşturularak doğrulandı (EXIT=0, Türkçe çıktı sağlam). `KURULUM.md` §3/§4 de düzeltildi — dört deponun kanca taşıdığını hiç yazmıyordu. |
| 10 | worker'da `CLAUDE.md`'nin ikinci, mükerrer kopyası | 2026-03 tarihli, kendini "ESKİ KOPYA — OTORİTER DEĞİL" diye işaretliyor (dürüst) ama `check_claude_md_refs.py` yalnız kök `CLAUDE.md`'ye bakıyor → içindeki bayat yollar kapsam dışı. Silme **onay** ister. |
| 11 | `sim-worker-baglan.sh` kapsayıcı kökte **mükerrer** | Betik bu oturumda worker deposuna alındı; kapsayıcıdaki kopya artık fazlalık. Silme **onay** ister. |

#### ⬜ Bir sonraki turda ilk yapılacak (kural tarafında)

- [ ] Kalem 3'ü kapat: worker'daki belge↔kapı parite kapısını platform ve edge'e taşı.
      **Bu, 2 ve 3 numaralı kusurun bir daha oluşmasını engelleyen tek yapısal önlemdir.**
- [ ] Kalem 2'yi kapat: kapı betiğinin testini contract/worker/edge'e taşı (üç kopya
      yerine tek kanonik test + üç ince sarmalayıcı düşünülebilir).
- [ ] Kalem 1, 10, 11 için **ürün sahibinden silme onayı** iste.



---

### Sonraki oturumun İLK komutu

```bash
gh pr list --repo physiscs-zana/tarlaanaliz-platform --state merged --search "merged:>=2026-08-21"
```

Sonra `SESSION_HANDOFF.md` §0.A. **Hafızadan değil, depodan oku.**

---

## 14.16 ✅ ① ve ② UYGULANDI (2026-08-21) — *"sonraki oturum yerine bu oturumda"*

> Ürün sahibi §14.15'i okuyup **"sonraki oturum yerine bu oturumda yapmaya ne dersin?"**
> dedi ve dört kararı verdi. İkisi de aynı oturumda uçtan uca uygulandı, merge edildi.
> §14.15 aşağıda **tarihsel kayıt** olarak duruyor (ölçümleri hâlâ geçerli).

### Ürün sahibinin dört kararı

| Soru | Karar |
|---|---|
| Fıstıkta hangi katmanlar satılıyor? | **Sözleşme örneğindeki 4 katman** (HEALTH, DISEASE, PEST, FUNGUS) |
| `analysis_types` kaynağı? | **Kaynak = paket, KAPI = üretilebilirlik** (fark "teslim edilemedi" yazılır) |
| Tekil mi dizi mi? | **Diziye geç** |
| PROCESSING'e nasıl geçilecek? | **Worker "iş başladı" olayı yayınlasın** |
| Diğer 6 mahsul? | **Hepsine fıstıkla aynı 4 katman** |

### Merge edilen PR'lar (ölçüm: `gh pr list --state merged`)

| Depo | PR | Ne |
|---|---|---|
| contract | #109 | **v7.8.0** — `analysis_job_started.v1` şeması · OpenAPI `AnalysisType` 7→11 · boşta koşan kapı gerçek kapıya · **yayımlanan komut sınıfı** (11 örnek daha bulundu) |
| worker | #245 | "iş başladı" yayını · sonuç artık **koşan** türleri beyan ediyor · pin v7.8.0 |
| edge | #81 | pin 7.8.0 (saf pin; edge şema baytları değişmedi — ölçüldü) |
| platform | #455 | `analysis_jobs.status` **gerçekten ilerliyor** · contract v7.8.0 pini |
| platform | #456 | sevk edilen katmanlar **artık GENERAL değil** — paket ∩ üretilebilirlik |
| contract | #110 | devir notu + bu bölüm |
| worker | #246 | **worker üretime bağlanabiliyor** — eksik override dosyası git'e alındı + kapısı |
| worker | #247 | öz-denetim: yanlış ölçüme dayanan gerekçe + kapının 4 kaçış yolu kapatıldı |
| platform | #457 | CLAUDE.md'deki satır numaralı atıflar kaldırıldı (5'i zaten bayattı) |

⚠️ Bu tablo bir kez **"6 PR"** diye yazıldı ve altında 5 satır vardı; çürütme turu
ölçüp düzeltti. **Sayıyı komuttan alın**, elle saymayın.

### 🔴 "Merge edildi" ≠ "dağıtıldı" ≠ "çalışıyor"

**Hiçbiri üretime dağıtılmadı.** Üretim hâlâ eski kodu koşuyor: `analysis_jobs`
satırları PENDING'de duruyor ve sevkler `GENERAL` göndermeye devam ediyor.
Ayrıca **worker hiçbir yerde koşmuyor**, yani "iş başladı" sinyali bugün
üretilmiyor bile. Zincir ancak (a) dağıtım ve (b) worker'ın ayağa kalkmasıyla
canlıda doğrulanabilir.

### Ölçülmüş ürün bulguları (kod değil, VERİ çelişkileri)

1. 🔴 **KİRAZ sipariş edilebilir ama hiçbir modeli yok.** `crop_readiness.json`
   `bookable: true` diyor; model kaydında `cherry_*` **tek giriş yok**. Yeni kapı
   bunu görünür kılıyor: kiraz için sevk **fail-closed** kesiliyor ve dört katmanın
   dördü de `MODEL_YOK` gerekçesiyle kaydediliyor. **Ürün kararı bekliyor.**
2. **WHEAT çelişkili:** modeli VAR ve `bookable: true` ama canlı fiyat kapsamında
   **yok** (KR-015 ile Tarla kapsamı dışına alınmış). Çözücü üretilebilirliğe
   düşüyor ve `PAKET_TANIMSIZ_URETILEBILIRLIGE_DUSULDU` yazıyor — kullanılabilirlik
   korunuyor, çelişki kayda geçiyor.
   ⛔ **SUNFLOWER bu cümleye YANLIŞ eklenmişti.** Ölçüldü: `bookable: false`
   (`stage1: research`). Sipariş alınmıyor, çelişki yok. İki mahsulü tek cümlede
   birleştirmek ölçülmemiş bir genellemeydi.
3. **Satılan ≠ koşturulabilen, artık ölçülü:** fıstıkta 4 satılıyor, **1** koşuyor.

### Bu turda AÇIKÇA yapılmayanlar (sessiz borç değil)

| # | Kalem | Neden |
|---|---|---|
| 1 | **Dağıtım** | Yapılmadı. `deploy-staging.yml` elle tetiklenir; üretim dağıtımı ayrı bir karardır. 🟢 **Worker AYRI**: dağıtılmadı ama **üretim broker'ına tünelle bağlandı** (PR #246) — `analysis_jobs` tüketici 0→1. Üretim sunucusunda worker KOŞAMAZ (ölçüldü: `sse4_2`/`avx` yok, GPU yok). |
| 2 | **Fan-out** (tür başına ayrı çıkarım) | Birleştirme semantiği (tespit harmanı, `confidence` indirgemesi, çelişen `result_mode`) **kodda yok** ve tasarlanması bir ÜRÜN kararı. Bugün etkisi 0: platform tek üretilebilir tür sevk ediyor. Kırpma artık `ANALYSIS_TYPE_NOT_RUN` koduyla **görünür**. |
| 3 | **`analysis_type` adının 7 anlamı** | Ölçüldü: platform'da 7 ayrı şeye işaret ediyor (4 DB kolonu, 6 farklı sabit). Bu turda **katman ekseni** ayrıldı (`analysis_types`), ama `analysis_jobs.analysis_type` → `processing_depth` ve `missions.analysis_type` yeniden adlandırmaları **yapılmadı** — göç + ORM + arayüz işi, ayrı tur. |
| 4 | **SSOT metni ↔ enum çelişkisi** | "Kaç katman?" sorusuna depo **dört** ayrı cevap veriyor (11 enum · 10 iç eşleme · 8 SSOT metni · 7 eski OpenAPI kesiti). Bu turda OpenAPI 11'e çekildi; **SSOT metnini değiştirmek KIRICI bir karardır** ve insan kararı bekliyor. |
| 5 | **`_map_analysis_types` geri düşüşü** | Katman taşımayan bir iş gelirse eski yola düşülüyor — ama artık **UYARIYLA**. Tümden silmek, eski kuyrukta bekleyen işleri düşürürdü. |

---

## 14.15 ⛔ KALDIRILDI (2026-08-21, öz-denetim turu) — *"İSPATLI PLAN" (2026-08-20 kapanışında yazılmıştı)*

> **Bu bölüm 255 satırdı.** §14.16 onu daha 2026-08-21'de *"tarihsel kayıt"* ilan
> etmişti ama başlığı hâlâ **"SONRAKİ OTURUM"** diyordu ve dosyada beşinci bir
> "buradan başla" iddiası olarak duruyordu.
>
> **Hiçbir açık kalem kaybolmadı — ölçüldü ve TAŞINDI (silmeden ÖNCE):**
>
> | §14.15'te olan | Bugün nerede |
> |---|---|
> | **ÖNCELİK ①** (her sevk `GENERAL`'e düşüyor) — ölçülmüş zincir + çerçeve düzeltmesi | **UYGULANDI**: §14.16 (platform #456 · worker #245 · contract #109). Ölçülmüş sonuç tablosu `SESSION_HANDOFF.md` §0.A'da |
> | **ÖNCELİK ②** (`analysis_jobs.status` ilerlemiyor) — ölçülmüş kanıt | **UYGULANDI**: §14.16 (platform #455 · contract v7.8.0 `analysis_job_started.v1`) |
> | **⬜ İNSANA ait kararlar 1·2·3·6·7** | **CEVAPLANDI**: §14.16 *"Ürün sahibinin beş kararı"* tablosu |
> | **⬜ İNSANA ait karar 4** (`GENERAL` jokeri kalsın mı) | **ÇÖZÜLDÜ**: platform #456 ile sevk artık `GENERAL` göndermiyor |
> | 🔴 **⬜ İNSANA ait karar 5** (*uzmanı olmayan bir katman sevk edilebilir mi? — KR-019*) | **HÂLÂ AÇIK** → §14.17 ÖNCELİK 2'nin yanına alındı, aşağıda |
> | **ÖNCELİK ③ · 11 kalemlik AÇIK KALEMLER tablosu** | **TAŞINDI** → §14.17 **ÖNCELİK 5-B** (birebir, 9 numaralı kapanmış kalem dahil) |
> | *"Sonraki oturumda İLK yapılacak"* — `pistachio_general_v1` ölçümü | **YAPILDI**: `model_registry.yaml` 9 giriş, fıstıkta yalnız `pistachio_disease_v1`, `pistachio_general_v1` **yok** |
> | *"`analysis_type` adının 5 ayrı anlamı"* | **ÖLÇÜLDÜ ve SAYI DÜZELDİ: 5 değil 7** → §14.16 tablosu kalem 3 |
>
> ⬜ **Devralınan tek insan kararı:** *uzmanı (KR-019 inceleyicisi) olmayan bir katman
> sevk edilebilir mi?* Bugün pratik etkisi ölçülmedi; §14.17 ÖNCELİK 2 (kiraz kararı)
> ile aynı oturumda sorulmalı çünkü ikisi de **satılabilirlik ↔ teslim edilebilirlik**
> ekseninde.

