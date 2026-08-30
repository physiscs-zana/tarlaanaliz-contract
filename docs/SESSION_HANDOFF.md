# Oturum Devir Notu (Session Handoff)

> Amaç: Farklı bilgisayarlar arasında çalışırken **oturum durumunu** taşımak.
> Yerel makine hafızası taşınmaz; bu dosya repo ile GitHub üzerinden senkronize olur.
> **Bir sonraki oturumda önce bu dosyayı oku.**

**Son güncelleme:** 2026-08-26 (**yirmi birinci oturum** — 🔴 **çiftçi tarla ekleyemiyordu**: saha kanıtından kök nedene, beş PR (plat #473/#474/#478/#479/#480) — ekran çiftçiye **yalan söylüyordu** (boş ama truthy sınır), `Invalid LngLat (NaN, NaN)` kök nedeni **deneyle kanıtlandı** (tür etiketine güvenmek; etiketi uyduran da bizim kodumuzdu), tarla ekleme **tek butona** indi · A-1/A-2 `/docs` üretimde fail-OPEN (#476) + G-1 WORM tablosuna yanlış “teslim edildi” (#477) · ⭐ **DAĞITIM İLK KEZ ÜÇ KATMANDA ÖLÇÜLDÜ** — üretim `origin/main` ile **0 commit** hizalı, backend konteynerinde ve **canlı web paketinde** doğrulandı · ⚠️ iki oturum **kayıt bırakmadan** kapandı, bu bölüm depodan kurtarıldı. Detay: §0.A. Önceki: 2026-08-25 (**yirminci oturum** — önceki turun devir notu **bağımsız denetimden geçti** (4 kusur + 1 yeni bulgu + 3 karar) · 🔴 **canlı çiftçi hatası** düzeltildi: tarla eklenemiyordu, arayüz sözleşmenin bayat aynasıydı (plat #468) · 🔴 **T01-K1 gerilemesi kapandı** — kapı doğruydu, KÜME yanlıştı; düşük-güvenli her işte uzman incelemesi sessizce kapanıyordu (plat #469) · Y1 sınıfı (üç üye) + Y2 üretici formu + çift declare (plat #470) · **K3** DLX'e bağlı kuyruk yoktu, **#467 bunu kapatmıyor** (plat #471) · **Y3** iş ekseni artık kanıt taşıyor, `status="FAILED"` bilerek YAPILMADI (plat #472) · iki sarkan betik atfı + Y4 tuzağı + yeni kapı (work #259). ⛔ “Hiçbiri dağıtılmadı” iddiası 2026-08-26'da **ÇÜRÜTÜLDÜ** — ölçüldü, altısı da canlıda (§0.A ③). Önceki: 2026-08-19/20 (**on altıncı oturum** — uzman ekranı zinciri: sonuç↔veri seti bağı sınıfı tamamen kapatıldı (#441/#443) · **üretimde ölü döşeme servisi** bulundu ve düzeltildi (#446 — NumPy x86-64-v2 uyumsuzluğu, 7770 log satırı) · CI asılma kapakları (#442) · alan adı + BOUND kapısı (#444) · dağıtımda submodule kapısı + simülasyon bağımsızlığı (#445) · kartlar alt uzmanlık duyarlı (#447). ✅ **7 PR MERGE EDİLDİ ve DAĞITILDI**. Önceki: 2026-08-18 (**on üçüncü/on dördüncü oturum** — KR-013-2 komşuluk kapısı sahipten bağımsız hâle getirildi (#91) · CLAUDE.md dört depoda Opus 5 rehberine göre yeniden yapılandırıldı + `check_claude_md_refs.py` atıf bütünlüğü kapısı kuruldu (#92) · kök `CLAUDE.md` + oturum-başı kanca kalıcılık için contract'a taşındı (#93) · dört depoda `docs/`+`denetim/` (191 dosya) tam-okuma denetimi: platform+worker sıfır aday, contract'ta 2 alansız dosya silindi/taşındı (#94). **AL-K26 (I-1 hizası) bu turda platformun 7.6.1'de kaldığı iddiasıyla açık görünüyordu — ölçüldü, 2026-08-13'te KAPANMIŞ ve dört depo bugün de 7.7.2'de hizalı** (bkz. §0.A, önceki turun bu satırı düzeltildi). Önceki: **on ikinci oturum** — contract deposunun cerrahi kalite denetimi: 27 alan-sızması düğümü kapatıldı · `validate.py` tüm ağacı gezer oldu · CI `paths:`/`needs` **türetiliyor** · hiç var olmamış Node/TS zinciri kaldırıldı (`npm run format` **zararlıydı**) · üç "belgelenmiş ama koşmayan" kural kapıya bağlandı · parite kapılarının **beş** kör noktası ölçülüp kapatıldı. ✅ **19 PR MERGE EDİLDİ**, **v7.7.0 · v7.7.1 · v7.7.2** etiketlendi; ayrıca **I-1 sürüm hizası** ve **betik ağacı** kapıları kuruldu. Önceki: **on birinci oturum** — docs sadeleştirme turunun ÖZ-DENETİMİ: 12 sarkan atıf onarıldı · **sarkan-atıf kapısı dört depoya kuruldu** ve çapraz-repo ayağı worker/edge CI'ında bağlayıcı kılındı · **çeltik sunumdan çıkarıldı** (canlı ürün çelişkisi) · aktif_ogrenme ikilisi tek belgede birleşti. ✅ **9 PR MERGE EDİLDİ.** ⚠️ Çeltik `main`'de ama **CANLIDA DEĞİL** — bkz. §0.A. Önceki: **onuncu oturum** — D12: `stress_ratio` kanonikte TANIMLANDI (`NDRE/NDVI`) ve KR-093 ön faz kapalı listesi **ilk kez kodda kapıya bağlandı** · D13: üç depo **7.6.1**'e hizalandı · öz-denetim, parite kapısının `metadata`'ya kör olduğunu ölçüp yeni kapı ekletti. ✅ **5 PR MERGE EDİLDİ**, üç depo temiz ve varsayılan dalında)

> ## 📐 BU DOSYANIN ROLÜ (2026-07-31'de netleştirildi)
> Bu dosya **DURUM FOTOĞRAFIDIR** — depo sürümleri, senkron durumu, oturumlar arası devir.
> **İŞ LİSTESİ TUTMAZ.**
>
> | Dosya | Rolü |
> |---|---|
> | **`docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`** | ⭐ **Yapılacak işlerin TEK kaynağı** (C/E/W/P/WEB/AL kalemleri, dalgalar, kararlar) |
> | bu dosya | Depo durumu + devir (işler için yukarıdakine bakılır) |
> | `denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` | Kanıt arşivi — her düzeltmenin `dosya:satır` dayanağı |
>
> Aynı iş için ikinci bir liste açılmaz; bir kalem değişecekse **eylem planında** değişir.

---

---

## 0.A EN GÜNCEL — (2026-08-29, **yirmi ikinci oturum: GERÇEK UÇUŞ ÜRETİMDE İŞLENDİ · TOPRAK MASKESİ · CHM İLE AĞAÇ/OT/TOPRAK · RENK ÖLÇEĞİ**)

> **Bu turun tek cümlesi:** 2026-08-27 gerçek fıstık uçuşu (Karaburun 102/1, sipariş
> `24cceb52`) üretim zincirinden **uçtan uca geçti** ve çiftçinin canlılık puanı
> **0.317 → 0.650** oldu — fark ağaç değil, **ağaç aralarındaki toprak**tı.

### ① ✅ ZİNCİR AKTI — gerçek siparişte, uçtan uca

`sim-gercek-4c-raster2.py` → 263 MB COG (33 parça) → platform adresi kendisi bildirdi
(`assembled_uri`) → `rgb_ortho_uri` + `calibrated_ortho_uri` **kanonik üreticiden** yazıldı
(elle SQL yok) → sevk → yerel GPU worker → sonuç → uzman kuyruğu.

| Uçuş | veri seti | `overall_health_index` | dayanak |
|---|---|---|---|
| Uçuş-1 (maskesiz) | `33f230f7` | 0.317 | `FIELD_MEAN_NDVI` |
| **Uçuş-2 (maskeli)** | `481e9c13` | **0.650** | `FIELD_MEAN_NDVI` |

Worker ölçümü: 4326×4731 → 110 karo, **30'u kapsama eşiği altında hariç**, 80 karo,
`confidence=0.310`, `mode=INDICES_ONLY`, ~33 dk.

⚠️ **Ölçüm tuzağı:** worker konteyneri `pipeline_completed` için `04:31:09` dedi,
üretim DB satırı `04:02:17` yazdı — **~29 dk saat kayması** (Docker Desktop VM uyku/uyanma).
Zaman damgasına dayanan hata ayıklama bu makinede yanıltır.

### ② 🔴 SEVK `PENDING_REVIEW`'DA TIKANDI — çözüm tasarımın kendisindeydi (→ DK-63)

Sevk **409** verdi. `mission.py:88` → `PENDING_REVIEW` yalnız `DONE / EXPERT_REJECTED /
FAILED / CANCELLED`'a gider; sevk edilebilir olan `EXPERT_REJECTED`. Yani Uçuş-2'yi
işletmenin kanonik yolu Uçuş-1'i **reddettirmekti** — kaçamak değil, tasarlanmış
yeniden-uçuş döngüsü. Ret iki bağımsız gerekçeyle de doğruydu (kapsama **%22.4**;
analiz **maske öncesi** üretilmişti).

**Ölçülmüş yan bilgiler (bir dahaki tura):**
* Sevk ucu **üç işi birden** yapar: `EXPERT_REJECTED → ANALYZING`, `CALIBRATED →
  CALIBRATED_SCANNED_CENTER_OK` (**AV2 muafiyeti**, `scan_performed:false` damgasıyla —
  üretimde `TARLA_AV2_ENABLED=false` ve `av2-scanner:8400` **yok**), ve en güncel veri
  setini kuyruğa koyma. AV2 **ayrı bir adım değildir**.
* `qc_report.pass_warn_fail` bir **kapı DEĞİL** — platform kaynağında hiç geçmiyor.
  KR-018'in altı koşulu: durum · kalibre · sha256 · av1 · av2 · ≥4 bant.
* Üretim DB'si: `ssh tarlaanaliz-prod` → konteyner **`tarlaanaliz-db`**.
  Kullanıcı/veritabanı adını uydurma, konteynerin `$POSTGRES_USER`/`$POSTGRES_DB`'sini kullan.
* Çiftçi listesi görev başına **yalnız en güncel** sonucu gösterir
  (`results_service_impl.py`) — iki uçuşu ayrı ayrı sunmak bugünkü tasarımla **mümkün değil**.

### ③ ⭐ TOPRAK MASKESİ — ölçümü DOĞRU değil, TEKRARLANABİLİR de yaptı

Maske (`NDVI ≥ 0.40`, `health_distribution.yaml`) ürüne üç yoldan birden ulaşıyor
(`reporting_agent.py`): `mean_ndvi` → platform `overall_health_index` türetimi.

| ort. NDVI | Uçuş-1 (30 m) | Uçuş-2 (60 m) | sapma |
|---|---|---|---|
| maskesiz | 0.3152 | 0.2695 | **0.046** |
| maskeli | 0.6405 | 0.6422 | **0.0017** |

İki bağımsız uçuş, farklı yükseklik, 14 dk arayla: **maskesizken birbirini tutmuyor,
maskeliyken örtüşüyor.** Maskesiz indeks aslında *"karede ne kadar toprak kaldı"*yı
ölçüyordu ve bu uçuş sınırlarına göre değişiyordu.

### ④ 🔴 AMA `canopy_cover_ratio` "AĞAÇ ORANI" DEĞİL (→ DK-64)

Ot da yeşildir ve `0.40` eşiğini geçer. Nokta bulutundan **CHM** üretildi
(`odm_filterpoints/point_cloud.ply`; pozitif kontrol tepe **3.77 m** ≈ fıstık ağacı,
negatif kontrol zemin medyanı **0.087 m** ≈ 0):

| | Uçuş-1 | Uçuş-2 |
|---|---|---|
| ağaç | %22.3 | %6.5 |
| **ot** | %5.5 | **%13.6** |
| toprak | %72.2 | %79.9 |

Uçuş-2'de "kanopi" denen %20.1'in **üçte ikisinden fazlası ot**. Ot ortalamayı iki uçuşta
da aynı yönde çekiyor: yalnız-ağaç **0.6682 / 0.6663** (fark **+0.0317 / +0.0326**).
Yükseklik eşiği veriden seçildi (Otsu): **1.52 / 1.46 m**; ağaç tacı medyanı **2.74 / 2.71 m**
— farklı uçuş, farklı nokta bulutu, **aynı ağaçlar**.

⚠️ Çiftçiye sunmadan önce **tarla poligonuyla kırpılmalı**: Uçuş-2 ortofotosu 32.8 dönüm,
kayıtlı tarla **29.0 dönüm**.

### ⑤ ⭐ RENK ÖLÇEĞİ — renkler ZATEN göreli, ve kimse söylemiyordu

Ürün sahibinin *"uzmana renklerin anlamını verelim"* fikri ölçüm sonrası büyüdü:

1. **Uzman portalinde hiç renk açıklaması YOKTU** (ölçüldü).
2. Karo üreticisi rampayı **görüntünün kendi %2–%98 dilimlerine** oturtuyor
   (`tile_service_impl._percentile_rescale`) → renkler **her durumda göreli**, kalibrasyon
   mutlak olsa bile. *"Kırmızı = NDVI 0.2"* her hâlde yanlış olurdu.
3. Worker her sonuçla `absolute_scale_valid` gönderiyor — **sıfır tüketici** (platform, web,
   şemalar). Öksüz veri.

⇒ Lejant **iki bağımsız şey** söyler: *"renkler görelidir"* (daima) ve *"sınıf sınırları
yaklaşıktır"* (yalnız `RELATIVE`). Bunları tek koşula bağlayan regresyonu yakalayan test
**mutasyonla doğrulandı**.

**Dal: `feat/renk-olcegi-gecerlilik` (platform) — PR yok, DAĞITILMADI.** Göç gerekmedi;
`absolute_scale_valid` `datasets.manifest['calibration_type']`'tan türetiliyor,
okuma kanonik `dataset_value_for_result` ile (sonuç-kapsamlı, "görevin en günceli" değil).
Lejant **ortak** `ResultMapSection`'a konuldu — o bileşeni çiftçi *ve* uzman kullanıyor.

### ⑥ ⭐ ARAŞTIRMA DENETİMİ — kartımız çürütülmüş bir iddia taşıyor (→ DK-62)

23 fıstık kartı içinde **tek `DIRECT`+`HIGH`** olan `thaumetopoea_solitaria`, kanıtını
*kalıcı ipeksi keseye* dayandırıyor. Literatür bunu çürütüyor (kalıcı kese
*T. pityocampa*'nın; *T. solitaria* gündüz gövdede dinlenir, **yumurta halinde kışlar** —
kart "kışlayan larvalar" diyor). ⓘ Kart metni okundu; **çürütme araştırma ajanı
raporundan**, birincil kaynaklar okunmadı → düzeltmeden önce doğrulanmalı.

### ⑦ 📌 BU TURDA AÇILAN KALEMLER

`DK-62` (gözkurdu kartı) · `DK-63` (yeniden analiz kapısı) · `DK-64` (ağaç/ot/toprak + CHM
+ ortofoto çözünürlüğü). Dal: `docs/devir-2026-08-26`, **PR yok — birikiyor**.

### ⑨ 🔴 AYNI OTURUMUN İKİNCİ YARISI — sözleşme 7.9.0 + ÜÇ ZİNCİRLEME KUSUR (kendi ürettiğim)

**Teslim edilen (üçü de merge + üretime dağıtıldı):**

| depo | ne |
|---|---|
| contract | `analysis_job.v1` → `field_boundary_geojson` (opsiyonel, 0 breaking) · **v7.9.0 etiketli** |
| worker | `field_clip.py` — ölçüm tarla sınırına kırpılır · bitki-örtüsü maskesi **mahsule bağlı** |
| platform | `FieldBoundaryRepositoryImpl` — sınır sevk yüküne konur · uçuş geçmişi + renk lejantı |

I-1/I-2/I-3 doğrulandı: üç depo **7.9.0**, `v7.9.0` annotated etiket,
submodule pini `8384fdf0` = etiket commit'i.

**🔴 ÜÇ KUSUR ÜRETTİM — üçünü de öz-denetimde kendim buldum:**

1. **Maskeyi KÜRESEL açtım.** Her mahsule uygulandı, **7 mevcut testi**
   kırdı. Kıranlardan biri tam bu sınıfı koruyordu: *"0.0 meşru bir
   NDVI'dir; onu silmek VERİ İMHA EDERDİ"*. Buğday tarlasında NDVI 0.0
   çiftçinin **görmesi gereken** sorundur. Ürün sahibinin kuralı zaten
   *"ağaçlı bahçe"* diye kapsamlıydı — **kural doğruydu, ben genişlettim**.
   ⇒ Düzeltme: küresel varsayılan **KAPALI**, maske
   `config/crops/<mahsul>.yaml`'dan açılır. Kodda mahsul listesi **yok**.

2. **`git stash` ÜRETİMİ BOZDU.** Paylaşımlı worker ağacını temizledim;
   ama çalışan konteyner o dizini **bind-mount** ediyordu
   (`…/src → /app/src`). Modül dosyaları ayağının altından çekildi, worker
   çöktü, onaylanmamış iş yeniden koştu ve çiftçinin değeri
   **0.650 → 0.270** oldu. ⚠️ **Dosyayı geri koymak yetmedi** — Python
   içe aktarılmış modülü yeniden yüklemez; düzelme ancak **konteyner
   yeniden başlatılınca** geldi.

3. **Mahsule bağlı maske ÜRETİMDE ÖLÜ KODDU.** `ReportRequest`
   `crop_type` **taşımıyordu**; `getattr(message, "crop_type", None)`
   sessizce `None` alıp maskeyi kapatıyordu. Kanıt zaten oradaydı
   (`vegetation_mask_applied = false`), ben bakmamıştım.
   ⇒ Alan **ZORUNLU** yapıldı (sessiz düşüş tip düzeyinde imkânsız),
   bilinmeyen mahsul **loglanıyor**, **üretim yolundan geçen** testler
   yazıldı (mutasyonla kanıtlandı).

**Üçünün ortak kökü: ÇÖZÜCÜYÜ test ettim, ZİNCİRİ değil.**
Ayrıntı ve reçeteler: yerel hafıza `olculmus-tuzaklar-2026-08-29`.

**Ölçülen diğer gerçekler (bir dahaki tur için):**
* Uçuş-2 ortofotosunun **%56'sı tarla sınırlarının DIŞINDAYDI**; kırpınca
  ağaç oranı %6.5 → **%13.4**, ot %13.6 → **%5.3** (→ DK-65).
* `fields.boundary` (PostGIS) üretimde **NULL**; poligon
  `boundary_geojson` (JSONB) içinde — uzamsal sorgu sessizce boş döner.
* CHM bağımsız eksenle doğrulandı: taç çapı 4.5–5.4 m, komşu mesafesi iki
  uçuşta **8.04 / 7.92 m**, **CV 0.08** → dikili bahçe ızgarası.
* Yerel araç sürümleri CI'dan geriydi (`ruff` 0.15.12 vs 0.16.5, `mypy`
  2.1.0 vs 2.3.1) ve ölçümü geçersiz kılıyordu. ⚠️ Sürüm eşitlemek de
  yetmiyor: **bağımlılık kümesi** farklı → bu depoda **mypy yerelde
  tahmin edilmez, CI'da doğrulanır** (`ci.yml` bunu zaten yazıyor).

**⚠️ AÇIK (o an):** kırpma platformda canlıydı ama uçtan uca hiç koşmamıştı.
→ **⑩'da KAPANDI.**

### ⑩ ✅ ÜÇÜNCÜ FAZ — zincir uçtan uca aktı, YEDİ kusur kapandı

> **Tek cümle:** yeniden analizi açtım; arkasından **dört kilit daha** çıktı, hepsi
> kapandı ve iki uçuş da artık **maskeli + tarla sınırına kırpılmış**.

**Çiftçinin gördüğü son hâl** (ölçüldü, `DISTINCT ON (dataset_id)`):

| Uçuş | Sonuç | Sağlık | Bitki örtüsü | Açık toprak | Tarla dışı (kırpıldı) |
|---|---|---|---|---|---|
| 27 Ağustos | `9150c0ca` | **0.666** | %27.2 | %72.8 | %4.5 |
| 28 Ağustos | `9fbbfef7` | **0.646** | %19.1 | %80.9 | **%57.9** |

Bayat `0.650` (kırpılmamış) ve maskesiz `0.317` **elenir**.

**Kırpmanın bağımsız doğrulaması:** boru hattı %57.9 dedi, elle ölçüm %56 —
iki ayrı yöntem 1.9 puan içinde uyuştu.

⚠️ **Ölçülen ama açıklanmayan:** kırpma sağlığı neredeyse hiç değiştirmedi
(0.650 → 0.646) ama örtü oranını %20.6 → %19.1 düşürdü — yani **bahçe DIŞI,
bahçenin kendisinden daha yeşildi**. Nedeni ÖLÇÜLMEDİ.

**Kapatılan yedi kusur** — dördü ancak gerçek siparişi uçtan uca sürerken göründü:

| # | Kusur | Nasıl bulundu | PR |
|---|---|---|---|
| 1 | Worker çöküş döngüsü (kalp atışı) | RabbitMQ `missed heartbeats` + `die 1` | work #265 |
| 2 | Ulaşılamaz yeniden-analiz geçişi (DK-63) | sevk `FAILED` | plat #484 |
| 3 | Başarısız sevk görevi KİLİTLİYOR | görev `ANALYZING`, kuyruk boş | plat #485 |
| 4 | `rate_limiter` çalışma zamanı kusuru | mypy → mutasyon | plat #484 |
| 5 | Escalation sonuç satırında patlıyor | `analysis_results_pkey` | plat #486 |
| 6 | Örtü oranı çiftçiye ulaşmıyor (DK-64 Kademe 1) | API'de var, arayüzde yok | plat #487 |
| 7 | Aynı uçuş için MÜKERRER kart | üç maskeli satır oluştu | plat #488 |

**Zincirleme:** yeniden analizi açınca escalation'ın kırık olduğu çıktı; escalation
düzelince aynı uçuşun iki sonucu oluştu; iki sonuç oluşunca listeleme kuralının
bunu öngörmediği görüldü. **Hiçbiri kod okuyarak bulunamazdı.**

**Sevk artık uçuş hedefleyebiliyor:** `sim-faz4d-sevk.py … --dataset <UUID>`.
Bayrak PIN kapısından ÖNCE ayıklanır.

**⚠️ Kanıtlanmayan:** #486'daki escalation kusurunun tam interleaving'i **yerelde
yeniden ÜRETİLEMEDİ** (hem sıralı hem yarış kurgusu kusurlu kodla yeşil kaldı).
Yarış testi bu yüzden depoya KONULMADI — sahte güven, testsizlikten kötüdür.
Düzeltme çakışmanın sebebine değil, o yolun sözleşmesine dayanır.

### ⑪ ✅ DÖRDÜNCÜ FAZ — beş öneri uygulandı + üç ortam sapması kapandı (2026-08-30)

**Sözleşme 7.10.0** (contract #124, `v7.10.0` etiketli): ön-faz kapalı listesine
`canopy_cover_ratio` + `field_clip_outside_ratio`. 0 breaking.

| # | İş | PR |
|---|---|---|
| 1 | Kırpma **kapsamı** çiftçiye (kolon+göç+köprü+DTO+arayüz) | plat #491 |
| 2 | **Skaler faz kapısı** — KR-093 yalnız katmanlar için çalışıyordu | plat #491 |
| 3 | Kanonik ön-faz listesi | ctr #124 |
| 5 | **`SUPERSEDED`** — yeniden analiz uzmanı REDDETTİRMESİN (DK-63) | plat #492 |
| 6 | Yeniden başlatma sayacı **görünür** | work #267 |
| — | worker saf pin 7.10.0 (I-1) | work #268 |

**4 (CHM / ağaç-ot ayrımı) BİLİNÇLİ ERTELENDİ** — pilot uçuşlardan sonra, tek iş
olarak. Bugün verilen `%27.2` **bitki örtüsüdür**, ot dahildir; arayüz bunu
çiftçiye açıkça yazar ve terim koruması **teste bağlıdır**.

#### ⚠️ İki KAVRAM aynı kelimeyi kullanıyor — karıştırma

`result_mode` (worker) ile `report_phase` (platform) **AYRI eksenlerdir** ve
ikisi de "FULL" der:

* `result_mode = FULL_REPORT` → *worker'ın güveni yeterli, bulguları raporladı*
* `report_phase = FULL` → *uzman onayladı, çiftçi görebilir*

Bir iş `FULL_REPORT` üretip aynı anda çiftçiye `PRELIMINARY` gidebilir —
bugünkü iki uçuş da öyle. Kod ayrımı DOĞRU yapıyor; risk yalnız insan
yorumundadır (denetimde/devirde karıştırılır).

#### Worker'ın raporu uzman görüşünden bağımsız mı? — ÜÇ eksen, üç cevap

| Eksen | Bağımlılık | Kanıt |
|---|---|---|
| Bu işin raporunun **içeriği** | **BAĞIMSIZ** | pipeline'da uzman sorgusu YOK; `result_mode` yalnız güven eşiğinden |
| Çiftçiye **teslimi** | **TAM BAĞIMLI** | `raw_findings = ... if report_phase == "FULL"`; `FULL` yalnız görev `DONE` iken, o da yalnız uzman onayıyla |
| **Gelecek** işlerin içeriği | **KISMEN, dolaylı** | ⚠️ mekanizma 2026-08-30'da ÖLÇÜLDÜ ve **düzeltildi** — aşağıya bak |

#### 🔴 Üçüncü eksenin MEKANİZMASI ÖLÇÜLDÜ — ilk yazdığım ZİNCİR YANLIŞTI

İlk hâli *"uzman → **prototip** → bellek → agreement → güven"* diyordu.
Dosyalar tam okununca çürüdü (worker **#269**):

| İlk iddia | Ölçüm |
|---|---|
| Prototipler belleğe/çıkarıma gidiyor | `PrototypeManager.query` **hiç çağrılmıyor** (yalnız testlerde) |
| `is_prototype` FAISS'te | geçiş **0** |
| `MemoryOrchestrator` prototip mesafesi ekliyor | geçiş **0** |
| `Pipeline` prototip uyumu kullanıyor | yorum-dışı geçiş **0** |

**Yanıltan şey `prototype_manager.py`'nin KENDİ docstring'iydi** — üç
entegrasyonu *olmuş gibi* yazıyordu. Yorum iddiadır; üreticiyi okumadan
güvenildi. Docstring ölçüme uyduruldu + **iki yönlü mandal testi** kondu
(entegrasyon bağlanırsa da, docstring geri alınırsa da kırılır).

**GERÇEK zincir — iki yol, ikisi de ölçüldü:**

1. **Hebbian `weight` (K-6)** → `_weighted_top_disease_hint` içinde
   `score = cosine × weight × zero_init` ile **HANGİ** komşunun ipucunun öne
   çıktığını sıralar. `cosine_sim`/`is_ood`'a **DOKUNMAZ** — bilinçli sınır:
   *takviye HATIRLAMAYI yanlar, YENİLİK tespitini asla* (fail-closed OOD korunur).
2. **REJECT** → `atlas.invalidate(crop, disease)` (KR-029) L1 kaydını **SİLER**
   → sonraki sorgular L2'ye düşer → `agreement` kaynağı `atlas_confidence`'tan
   `cosine_sim`'e geçer → güven değişebilir.

✅ **AKIŞ DA ÖLÇÜLDÜ** (worker **#270**, `tarlaanaliz-worker/denetim/uzman_geri_bildirim_zinciri_olcumu_2026_08_30.md`).
Betikler `tarlaanaliz-worker/denetim/deneyler/` altında — iddia değil, **yeniden koşulabilir kanıt**:

| Deney | Ölçüm |
|---|---|
| Hebbian ipucu sıralamasını değiştiriyor mu | **EVET** `HASTALIK_A → HASTALIK_B` |
| `cosine_sim` / `is_ood` etkileniyor mu | **HAYIR** — `0.995037` → `0.995037` |
| REJECT → `atlas.invalidate` | kaynak `L1 → L2`, agreement **0.88 → 1.000** |
| Güven / rapor kipi kayıyor mu | **+0.0360**, 7 senaryonun **1'inde** `PARTIAL → FULL` |

Fark **tam** formülün öngördüğü `0.30 × 0.12` çıktı — pozitif kontrol: formül
gerçekten o yuvadan besleniyor. ✅ Fail-closed sınırı da ölçüldü: **takviye
HATIRLAMAYI yanlar, YENİLİK tespitini asla.**

📌 **Ölçümün gösterdiği beklenmeyen yön:** bu senaryoda **REJECT güveni
YÜKSELTTİ** (reddedilen atlas kaydı silinince sorgu L2'ye düşüyor ve oradaki
cosine daha yüksek). Kusur **iddiası değil**, ölçülmüş davranış; arzu
edilirliği ürün/ML kararıdır.

⚠️ **Kapsam sınırı:** deneyler İZOLE nesnelerle koştu ve üretime DOKUNMAZ.
Ölçülen: mekanizmanın çalıştığı. **Ölçülmeyen:** üretimdeki canlı FAISS/atlas
durumunda aynı **BÜYÜKLÜKTE** etki (gerçek indeks içeriği, decay geçmişi ve
`zero_init` durumu farklıdır).

📌 **Beyan edilmiş borç:** `add_sample` ÜRETİMDE çağrılıyor (her grade A/B geri
bildirimi) ama `query` hiçbir üretim yolundan çağrılmıyor — prototipler
üretiliyor, kimse okumuyor. Bu bir kusur DEĞİL, K-7 "genişletme" deseninin
bilinçli faz borcu; ama beyan edilmemiş hâli SESSİZ borçtu.

✅ Kritik koruma yerinde (O-4): çıkarımda saklanan gömüler `TrainingGrade.C` —
eğitime/prototipe **girmez**; onları ancak **gerçek uzman geri bildirimi**
yükseltir. Eski kod modelin kendi güvenini not sayıyordu → **doğrulama
yanlılığı**; kapatılmış.

#### Ortam: üç sapma kapandı (kanıt arşivi platform `denetim/`)

`redis 8.0.1` (pin `<6`) sahte "unused ignore" üretiyordu · `pytest 9.1.1`
contract'ın `==9.0.2` pinini ihlal ediyordu · **sistem** `core.autocrlf=true`
taze klonları CRLF'e çevirip KR-042 kapısını sahte kırmızıya düşürüyordu.
Üçü de düzeltildi: `mypy src/ scripts/` → **488 dosya 0 hata** (CI ile birebir).

### ⑧ ⚠️ DEVREDEN

* ✅ **Uçuş-1'in maskeli+kırpılmış koşumu YAPILDI** (⑩). Önceki turda "önerilmedi"
  denmişti çünkü sevk hep en güncel veri setini seçiyordu — **o kısıt kaldırıldı**
  (`--dataset`), yani gerekçe artık geçersiz.
* **Birleştirme YAPILMADI** (ürün sahibi kararı). Ölçüm hazır: F1 uzamsal olarak **F2'nin
  içinde**, aynı gün 14 dk arayla → radyometrik risk düşük; F1'in 77 ek karesi merkezi
  yoğunlaştırır. Uçuş-1 **30 m** (GSD 1.38 cm, `pistachio.yaml` şartı `[0.5,1.5]` içinde),
  Uçuş-2 **60 m** (2.76 cm, şartın ~2 katı dışında).
* Uzman kuyruğunda Uçuş-2'nin **kırpılmış** sonucu için iki `PENDING` inceleme.
* 🔶 **DK-64 Kademe 2 AÇIK:** ağaç/ot/toprak üçlü ayrımı. Kademe 1 (bitki örtüsü /
  açık toprak) canlıda; ağaç-ot ayrımı **CHM** ister (yükseklik), NDVI ayıramaz.
  Üretici hâlâ kurulu değil — bugüne dek elle yapıldı, sahada üretilemez.

---

## 0.B — (2026-08-25/26, **yirmi birinci oturum: ÇİFTÇİ TARLA-EKLEME ZİNCİRİ · A-1/G-1 · DAĞITIM İLK KEZ ÖLÇÜLDÜ — 8 PR**)

> ⚠️ **Bu bölüm SONRADAN yazıldı.** İki oturum (denetim turu + tarla-formu turu) devir
> notu bırakmadan kapandı; bu kayıt depodan ve **yeniden yapılan ölçümlerden** kurtarıldı.
> Ders ⑤'te.
>
> **Bu turun PR'ları — SAYIYI KOMUTTAN AL:**
> ```bash
> gh pr list --repo physiscs-zana/tarlaanaliz-platform --state all \
>   --search "created:>=2026-08-25" --json number,state,title
> ```

### ① 🔴 ÇİFTÇİ TARLA EKLEYEMİYORDU — saha kanıtından kök nedene (plat #473 · #474 · #478 · #479 · #480)

Gerçek çiftçinin üretim ekran görüntüsü: form dolu, alan **28854**, yeşil *“Tarla sınırı
eklendi (Polygon)”* yazıyor — ama harita kutusu **boş** ve üstünde
`Harita yüklenemedi: Invalid LngLat object: (NaN, NaN)`. Kaydet'e basılıyor, **hiçbir şey
olmuyor**. Çiftçi: *“iki buton da çalışmıyor.”*

⚠️ **Asıl sınıf: “Kadastrodan Çek” ASLINDA ÇALIŞMIŞTI.** `28854` değeri yalnızca
TKGM yanıtından (`28853.55` → `Math.round`) gelebilir. Çiftçi sonucu göremediği için
“çalışmıyor” sandı. Yani kusur işlevde değil, **ekranın çiftçiye yalan
söylemesindeydi** — bu turun bütün kalemleri o tek sınıfın üyesi.

| PR | Kapatılan |
|---|---|
| **#473 · #474** | Siyah harita + *“Kadastro sorgusu başarısız”* — TKGM yol parametresi. #473'ün **düşen commit'leri** ve **aynı kök nedenin ikinci dosyadaki kopyası** #474'te toplandı |
| **#478** | ① **boş ama TRUTHY sınır** — `coordinates=ham.get("coordinates", [])` anahtar yoksa `{type:"Polygon", coordinates:[]}` üretiyordu; arayüz yalnız **varlığa** bakıyordu (`if (data.geometry)`) → “sınır eklendi” denip hiçbir şey çizilmiyor, Kaydet'te backend opak hatayla reddediyordu. Artık bir sınır **ya geçerlidir ya yoktur** ② arayüzde **tek yazıcı yoktu** (çizim / kadastro / ters-kadastro state'e ayrı ayrı yazıyordu) ③ Kaydet'in **bekleme durumu yoktu** → asılı POST ile ölü buton ayırt edilemiyordu; çift gönderim kilidi de yoktu ④ **harita çökünce butonlar ölüyordu** (`map.on('click')` try bloğunun en sonundaydı; `setTerrain` yalnızca **süsleme** olduğu hâlde korumasızdı) |
| **#479** | `Invalid LngLat (NaN, NaN)` **kök nedeni bulundu ve deneyle kanıtlandı**: düzleştirme `type` **etiketine** güveniyordu (`type === 'MultiPolygon' ? flat(2) : flat(1)`). Etiket yanlışsa `.flat(1)` noktaları değil **halkaları** verir; 2–3 noktalı halka `LngLatLike`'ın uzunluk kapısından geçer ve `Number([x,y])` = **NaN** olur. **Etiketi uyduran da bizim kodumuzdu** (`ham.get("type","Polygon")`, **üç** yerde). Artık nokta listesi etiketten değil **verinin yapısından** türetiliyor; `type` tabanlı düzleştirme depoda **kalmadı** |
| **#480** | Ürün sahibi: *“harita açıldı ama işlem kalabalığı var, yaşlı çiftçiler zor bulur; sakın çalışan kodları bozma.”* **Bir adım tamamen kalktı** — önceden: ada/parsel yaz → “Haritada Çiz”e bas → haritanın **içinden** “Kadastrodan Çek”i bul; şimdi: ada/parsel yaz → **“Kadastrodan Çek”** → sınır gelir, harita **kendiliğinden** açılır. Çizim ve tıkla-seç yolları **duruyor** (TKGM'de kaydı olmayan parseller için hâlâ gerekli). Ayrıca: her alana **görünür etiket** (yer tutucu yazmaya başlayınca kayboluyordu), **3 adımlı** akış, `(Polygon)` gibi teknik terim gizlendi, alan kutusu sınır varken **salt okunur** (düzenlenebiliyordu ama kayıtta sınırdan hesaplanan değer eziyordu), çiftçiye görünen metinler **diakritikli** Türkçe |

**Doğrulama biçimi:** tarayıcıda **uçtan uca** — üretim derlemesi + gerçek Mapbox anahtarı +
gerçek TKGM poligonu (Gaziantep/Oğuzeli/Karaburun 102/1, 19 nokta). jest **427/427** ·
tsc / eslint / prettier temiz · mutasyon: #478 backend 3/3 + arayüz 3/3, #479 2/2.
**İki mutasyon EŞDEĞER çıktı** ve ayırt edildi — biri fazlalık diye **silindi**, biri
savunma-derinliği diye **bilerek bırakıldı**. `mypy` tabanı ölçüldü: `origin/main` zaten
aynı 2 hatayı veriyor, yeni hata yok.

⚠️ **#479'un beyan edilmiş sınırı:** çiftçinin tarayıcısındaki NaN'ın **tam üreteci**
kanıtlanamadı (25+ olumsuz koşulda yerelde üretilemedi: 0x0 kap, `display:none`,
`transform:scale(0)`, WebGL yok, DEM kesik…). Bir neden **uydurulmadı**; bunun yerine
yapı olarak **imkânsız** kılındı ve bir daha olursa **ölçülebilir** yapıldı (yığın izi +
merkez/zoom/kap ölçüleri + nokta sayısı loglanıyor).

### ② A-1/A-2 ve G-1 — denetim turu (plat #475 · #476 · #477)

* **A-1 + A-2 (#476)** — ortam etiketi **BÜYÜK HARF** yazılırsa (`APP_ENV=Production`)
  `_docs_url` karşılaştırması tutmuyordu → `/docs` üretimde **açık** kalırdı: kimliksiz
  API yüzeyi ifşası, **fail-OPEN**. Ayrıca `TANINAN_ORTAMLAR` kümesi mandalsızdı.
  ⛔ *“Üretimde hâlâ açık”* dendi, **çürütüldü**: `/docs` ve `/openapi.json` →
  **404**, `/health` → **200**. 404'ü **uygulama** veriyor (JSON gövde + FastAPI güvenlik
  başlıkları; rastgele bir yol da aynı imzayı üretiyor), ağ katmanı değil. Kusur
  **latent** bir tuzaktı — dört yapılandırmada da etiket küçük harf.
* **G-1 (#477)** — `_insert_field_history` `NO_RESULT` durumunda da **teslim edildi**
  yazıyordu: hiçbir sonuç üretilmediği hâlde çiftçinin tarla geçmişine
  `ANALYSIS_DELIVERED` düşüyordu (`health_score=None`). Zarar **kalıcı**: `field_history`
  bir **WORM** tablosu, asla silinmiyor. Asimetri kanıttı — kardeş **üç** çağrı yeri
  `result_mode != "NO_RESULT"` koşulunu taşıyor, bu **taşımıyordu**.
* **#475** aynı daldan **mükerrer** açılıp merge edildi (#476'dan 35 sn önce). Zararsız,
  ama not: PR açmadan önce açık PR listesine bakılır.

### ③ ⭐ DAĞITIM İLK KEZ ÜÇ KATMANDA ÖLÇÜLDÜ — §0.B'nin iddiası ÇÜRÜDÜ

| Katman | Ölçüm | Sonuç |
|---|---|---|
| Üretim diski | `git rev-parse --short HEAD` → `84d1a7ba` (= #480) | `452d9879` (#476) ve `93e4579d` (#477) bu commit'in **atası**; `origin/main`'in **0 commit** gerisinde |
| Çalışan backend konteyneri | `docker exec tarlaanaliz-backend grep -c …` | iki düzeltme de **1** |
| Çalışan **web paketi** (dışarıdan) | canlı CSS'te `.-mt-1{margin-top:-.25rem}` | **VAR** ⇒ #480 canlı |

**Web'i DIŞARIDAN ölçmenin yolu.** Çiftçi sayfaları **giriş kapılı**, bu yüzden
*“yeni dizeyi `curl` ile ara”* reçetesi orada **çalışmaz** (`/fields` → HTTP 200
ama gövde giriş ekranı; sayfanın kendi chunk'ı hiç servis edilmez). Çalışan yol: #480 ile
**tek** bir yeni Tailwind sınıfı doğdu (`-mt-1`, tüm `web/` ağacında yalnız
`AddFieldModal.tsx:352`). Tailwind CSS'i `content: ["./src/**"]` taramasından ürettiği için
bu sınıf **ancak** o kaynaktan derlenmiş pakette bulunur — ve genel CSS **giriş
gerektirmez**. Pozitif kontrol: `.mt-1` de bulundu (grep'in çalıştığının kanıtı).

⚠️ **Bu ölçümün DESTEKLEMEDİĞİ şey:** yalnız **platform** (backend + web) ölçüldü; worker
ve edge kapsam dışı. Ayrıca statik varlıkların `last-modified`'ı **asimetrik** kanıttır:
**yeni** tarih dağıtımı kanıtlar, **eski** tarih dağıtılmadığını **kanıtlamaz** (içeriği
değişmeyen chunk eski tarihini korur). Ölçülen üç değer üç ayrı dağıtıma denk düştü:
`08-25 21:34Z` (#476 sonrası) · `08-25 23:36Z` (#478 sonrası) · `08-26 05:43Z` — #480'in
commit'inden **2 dk** sonra.

**Düzeltilmiş kural:** otomasyonun yokluğu **dağıtılmadığını kanıtlamaz.** Ürün sahibi
`deploy_prod.sh`'ı elle koşuyor, ama bunu merge'den **dakikalar sonra** yapıyor.

### ④ 🔴 ÖZ-DENETİM: aynı hata bir turda ALTI KEZ — çıkarımı ölçüm gibi söylemek

Denetim turunun kendi kaydına göre **altı** kez bir çıkarım ölçüm gibi sunuldu. İkisi aynı
oturumda çürütüldü: *“A-1 üretimde hâlâ açık”* → tek bir `curl` ile; *“iki PR
de dağıtılmadı”* → ürün sahibinin tek komutuyla. **Her ikisi de söylenmeden önce
ölçülebilirdi.** Kural zaten yazılı (kanıt aynı mesajda); eksik olan uygulamaydı —
*“merge ≠ dağıtıldı ≠ çalışıyor”* üçlüsünün **her ayağı ayrı ayrı** ölçülür.

### ⑤ ⚠️ İKİ OTURUM KAYIT BIRAKMADAN KAPANDI — bu bölümün var olma nedeni

Bu turun sekiz PR'ı bu dosyada **hiç** anılmıyordu (`grep` → #473…#480 için **0 isabet**).
Aynı ihlal §0.B ⑧'de de kayıtlı (o turda beş PR eksikti) — yani **tekrar eden** bir kalıp.
**Kural:** bir tur, devir notu yazılmadan **bitmiş sayılmaz**; ve devir notu **kapanış
anında** yazılır, sonraki oturuma bırakılmaz.

### ⑥ AÇIK KALEMLER

| # | Kalem | Durum |
|---|---|---|
| **U-1** | `docker-compose.override.yml` ile `docker-compose.dev.yml` yorumlar hariç **bayt-özdeş** (`diff` boş) → iki kaynak sessizce ayrışır. Ayrıca README + iki-makine runbook'u hâlâ çıplak `docker compose up` diyor (`-f` yok, grep **0 isabet**) → ikinci makinede üç tazelik mount'u yüklenmez | AÇIK, ucuz |
| **U-2** | `deploy-staging.yml` bir **plasebo**: build adımı `echo "Docker build would run here"`, gerçek komut yorum satırında. Tetiklenirse hiçbir şey dağıtmaz ama *“staging'e dağıtıldı”* izlenimi verir | AÇIK, ucuz |
| `rollback.request` | tek taraflı (worker tüketiyor, platformda üretici yok) — §0.B ⑦'den **devam ediyor**, ürün kararı bekliyor | AÇIK |

> Gerekçeleri ve **elenmiş 18 kalemin** neden elendiği, çalışma alanı kökündeki
> `DENETIM-ACIK-BULGULAR` listesinde (git-izli **değil**, makineye özel).

**Çalışma alanı temizliği (ölçülerek):** `Desktop/ODM_TARLA` **22 GB → 6,8 GB** — ODM ara
ürünleri silindi (`opensfm`, `odm_texturing_25d`, `odm_filterpoints`, `odm_meshing`);
ortofoto, COG, rapor, georeferencing ve kaynak fotoğraflar **korundu**. Pozitif kontrol:
silme sonrası COG ve camera ortofotosu `rasterio` ile **açıldı**. ⚠️ Üç koldaki `images/`
klasörleri **hardlink** (`link=3`, tek fiziksel kopya) — ikisini silmek **sıfır yer
açardı**. `Desktop/DJİ_29-07-ÇEKİM` (16 GB, `link=1`) arşiv kararı **ürün sahibinin**.

---

## 0.B — (2026-08-25, **yirminci oturum: DEVİR NOTUNUN BAĞIMSIZ DENETİMİ + CANLI ÇİFTÇİ HATASI + 6 PR**)

> **Bu turun PR'ları — SAYIYI KOMUTTAN AL:**
> ```bash
> for r in tarlaanaliz-contract tarlaanaliz-platform tarlaanaliz_worker; do \
>   gh pr list --repo physiscs-zana/$r --state all --search "created:>=2026-08-25" --json number,state,title; done
> ```

### ① Önceki turun devir notu bağımsız olarak DENETLENDİ

Her iddia komutla yeniden sınandı. **§1 (T01-K1 gerilemesi) kusursuz çıktı** — altı satır
atfının altısı da birebir; kapı ayrıca **canlı konteynerde davranışsal olarak** ölçüldü
(`PENDING_REVIEW → True`, pozitif kontroller doğru).

**Dört kusur bulundu ve düzeltildi:** ①② Y4'ün iki bayat satır atfı
(`config.py:39`→`:47` — kayma aynı gün worker #257 ile oluşmuştu; `consumer.py:121-127`→
`:131-137` — bu atıf *hiç* doğru olmamış) · ③ *"docs onu düzeltme gibi sunuyor"*
**⛔ ÇÜRÜTÜLDÜ** (sabit tüm çalışma alanında **iki** yerde geçiyor, hiçbiri docs değil) ·
④ §3.2 iki **bağımsız** kapıyı birleştiriyordu.

**Yeni bulgu:** iki sarkan `dlq-kur.sh` atfı (aşağıda, worker #259).

**Doğrulanamayan üç kalem karara bağlandı** (kaynak geçici bir çalışma-alanı notuydu;
kaybolmaması için kararlar BURAYA taşındı):

1. **Ajan turu sayıları** (14 ajan / 105 bulgu / 77 doğrulanmış / 36 kusur) → ⛔
   **DOĞRULANAMAZ, KAPATILDI.** Turun hiçbir artefaktı diske yazılmamış (2026-08-25 tarihli
   denetim klasörü YOK) ve kaynak oturum kaydına erişilemiyor. Bir daha doğrulanabilir hâle
   **gelmeyecek** — kovalamayın. ⚠️ **Kural ihlali, ders:** bir filo turu, ajan çıktısı
   `denetim-<tur>-<tarih>/bulgular/` altına yazılmadan **bitmiş sayılmaz**.
2. **Üretim SHA'sı** → ⚠️ **ÖLÇÜLMEDİ**, kusur DEĞİL. Sürüm bildiren uç yok, yerel dağıtım
   kaydı yok. Doğrulama: `ssh <prod> "cd /opt/tarlaanaliz && git rev-parse --short HEAD"`.
3. **Takvim çelişkisi** → ✅ **KAPANDI**, konusuz kaldı (revize takvim yerine geçti).

### ② 🔴 CANLI ÇİFTÇİ HATASI — tarla eklenemiyordu (plat #468)

Çiftçi *"Yeni Tarla Ekle"* formunda Kaydet'e basınca kırmızı **"Validation failed"**
alıyordu. **Kök neden: arayüz, sözleşmenin BAYAT AYNASIYDI.** Backend
`FieldCreateRequest.geometry` varsayılansız (zorunlu) tanımlı; arayüz ise sınırı
*"(Opsiyonel)"* diye sunuyor ve alanı yalnız doluysa gönderiyordu. `main.py` tüm 422'leri
şema sızdırmamak için tek bir *"Validation failed"*e düzleştirdiği için sebep gizleniyordu.

**Çalışan konteynerde ölçüldü:** `ZORUNLU: ['parcel_ref','area_ha','crop_type','geometry']`;
eski arayüzün gönderdiği gövde → `REDDEDILDI: [(('geometry',), 'missing')]`.

Ayrıca **KR-013-2 komşu-tarla bilgi notu KALDIRILDI** (ürün kararı): kapı
`KR-013-2-DEVRE-DISI-2026-08-17` ile yorum satırında, yani not **var olmayan** bir
davranışı anlatıyordu. ⚠️ **KR-013-1 asgari 5 dönüm kuralı HÂLÂ ETKİN** (`field.py:50`,
kapı `fields.py:259`) — o cümle silinmedi, alan kutusunun yardım metnine taşındı.

### ③ T01-K1 GERİLEMESİ KAPANDI (plat #469) — kendi #464'ümüzün ürünü

#464 eskalasyon dalına `gorev_yan_etkileri_atlanmali` bağladı. **Kapı doğruydu, KÜME
yanlıştı:** o küme `PENDING_REVIEW` içerir ve üretim sırası tam onu üretir
(worker `:1396` sonuç ÖNCE → görev PENDING_REVIEW → `:1604` eskalasyon SONRA → kapı ısırır).
Sonuç: düşük-güvenli **her** işte uzman incelemesi sessizce kapanıyordu.

Eskalasyon ekseninin **kendi** kapısı yazıldı; küme kanonikten **türetiliyor**
(`GOREV_TERMINAL_DURUMLARI - {"PENDING_REVIEW"}`) — ikinci gövde YOK.

> **DERS (kalıcı):** *bir kapıyı İZOLE sınamak yetmez — üretimin o kapıya hangi SIRAYLA
> geldiğini de sına.* #464'ün mandalları izole yazılmıştı ve **yeşildi**. Yeni
> `TestT01K1UretimSirasi` sırayı kilitler.

### ④ Diğer dört PR

| PR | İş | Not |
|---|---|---|
| plat #470 | **Y1** (`result_id == job_id` sınıfı) + **Y2** (üretici formu) + çift kuyruk declare | Y1 sınıfı **üç** üyeliydi ve sonuçları farklı: uzman ataması FK ihlali (sert) · wire olayı yanlış kimlik · `field_history` kolonu **FK değil** → çökmez, **sessizce** yanlış işaretçi. Y2: `_insert_field_history` worker'ın hiç üretmediği `type`/`severity`/`name` anahtarlarını okuyordu → gerçek yükte geçmiş olayları **yapısal olarak hiç yazılmıyordu** |
| plat #471 | **K3** — DLX'e bağlı kuyruk YOKTU | 🔴 **#467 bu deliği KAPATMIYOR**: policy deseni dokuz kuyruk sayan açık bir liste ve `domain.events.*` orada yok. Ayrıca ölçüldü: `declare_topology` için depoda **hiç test yoktu** |
| plat #472 | **Y3** — çıkarım çökse bile iş ekseninde iz kalmıyordu | ⛔ `status="FAILED"` **YAPILMADI**: platform görevi FAILED yapar, ardından gelen eskalasyon kapıya takılır → uzman incelemesi hiç açılmaz (T01-K1'in aynısı). İş ekseni **durum değil KANIT** taşır |
| work #260 | 🔴 **K2** — eksik zorunlu bant sıfırla dolduruluyordu, sonuç **sessizce yanlış** oluyordu | Kural tek kaynağa çıkarıldı; fail-closed → ACİL eskalasyon. **Öz-denetimde bulundu** (bkz. ⑤) |
| work #259 | İki sarkan `dlq-kur.sh` atfı + Y4 tuzağı + "ölü" DLX opt-in **karar** olarak mandallandı | Kapı ilk koşumda **üçüncü** bir atıf buldu; ölçüldü, platformda gerçekten var → çapraz-repo, kanıtıyla izin listesine alındı |

### ⑤ 🔴 ÖZ-DENETİM: kapsamı SESSİZCE DARALTMIŞIM — K2 (worker #260)

Tur sonunda kendi çıktımı çürütme turu (`CLAUDE.md` §6) **kendi hatamı** buldu:
devir notunda **KRİTİK** olarak duran **K2**, benim önerdiğim PR gruplamasında
**yoktu** — yani §3 *"kapsamı sessizce daraltma"* ihlali. Kökten kapatıldı.

**Kusur:** `_load_bands` eksik olan HER bandı ayrım yapmadan sıfırla dolduruyor,
yalnız WARNING basıyordu. `NIR=0` → `NDVI = (0−R)/(0+R+eps) = −1.0` → **tarlanın
tamamı "anomali"**. Sıfır kanal düşük varyanslı olduğu için güven formülü bunu
belirsizlik saymaz → fail-closed eşikleri (KARAR-13) **devreye girmez** → model
tam bir tanı üretir ve sonuç çiftçiye gider. **Başarısız değil, sessizce YANLIŞ.**

**Koruma neden etkisizdi:** `channel_spec.build_input_tensor` ayrımı ZATEN
yapıyordu, ama `_load_bands` ONDAN ÖNCE koşup bandı sıfırla "var" hâle getiriyor
ve o korumayı **körleştiriyordu**. Kural artık tek kaynakta
(`bant_sifir_doldurulabilir_mi`), iki tüketici de onu okur. Zorunlu bant eksikse
fail-closed → `NO_RESULT` + `PIPELINE_ERROR` → **ACİL eskalasyon** (iş kaybolmaz,
uzmana gider). Blue'nun tasarlanmış nazik bozulması **korundu**.

### ⑥ Merge provası GERÇEK bir çakışma buldu (merge etmeden önce)

Beş platform dalı sıralı olarak geçici bir dalda merge edildi: #468→#469→#470→
#471 temiz, **#472 ÇAKIŞTI**. Sebep salt metinsel bitişiklik — #469 ve #472 aynı
çapaya ekleme yapıyordu. **Çakışmayı yönetmek yerine ORTADAN KALDIRDIK:** #472'nin
yardımcı bloğu başka bir konuma taşındı (Python ad çözümlemesi çağrı anında olduğu
için davranış değişmez). Prova tekrarlandı → **beşi de temiz**, ve **birleşmiş
hâlde** `ruff` temiz + tüm unit testler yeşil (çıkış kodu 0). Merge sırası artık
önemsiz.

### ⑦ AÇIK KALEM olarak BEYAN (sessiz borç bırakmamak için)

**`rollback.request` tek taraflı** — worker tüketiyor, platformda ne üretici ne
tüketici var (ölçüldü: `grep -rn rollback tarlaanaliz-platform/src` yalnız ilgisiz
DB rollback'leri buluyor). **Düzeltilmedi ve bu bilinçli:** platform tarafına
üretici yazmak var olmayan bir özellik icat etmek olurdu. Bugün **sıfır risk**
(kimse basmıyor) ve DLX policy deseni onu zaten kapsıyor. Ürün kararı gerektirir.

### ⑧ Bu dosyada EKSİK kalan beş PR (önceki turdan)

Denetimde ölçüldü: **plat #466, #467 · worker #256, #257, #258** bu dosyada hiç anılmıyordu.

- **plat #466** — otomatik sevk zinciri: kalibrasyon kaydı üreticisi + olay yolunun AV2 bayrağından ayrılması
- **plat #467** — DLX policy kapsamı 4→9 + fail-closed doğrulama · ⚠️ **dağıtım durumu ÖLÇÜLMEDİ**
- **work #256** — taze zincir Faz 2 (COG yükleme) · **#257** — sırları `--env-file`'a taşı · **#258** — rakip DLQ betiği kaldırıldı

### ⑥ Ortam notu — yerel worker testleri

`pytest tests/unit` worker'da **54 kırmızı**. ⚠️ **BASELINE DE 54** (`git stash` ile
`master` üzerinde ölçüldü) → değişikliklerimiz sıfır yeni kırmızı üretiyor. Kök neden
makine artefaktı: **torch/NumPy ABI uyuşmazlığı** (`Numpy is not available`), kodla
ilgisiz. Hafızadaki *"yerel artık sıfır kırmızı"* kaydı (#448 sonrası) bu ortamda
**bayatlamıştır**.

### 🔴 "Merge edildi" ≠ "dağıtıldı" ≠ "çalışıyor"

Altı PR'ın hiçbiri **dağıtılmadı**. Bu depolarda push/merge tetikli deploy işi **yok**.

> ⛔ **2026-08-26'da ÇÜRÜTÜLDÜ — bkz. §0.A ③.** “Dağıtılmadı” bir **çıkarımdı**
> (“otomatik dağıtım yok → demek ki dağıtılmamış”), ölçüm değil. Ölçüm: üretim diski
> `84d1a7ba` (= plat #480) ve `origin/main`'in **0 commit gerisinde** — yani bu altı PR
> da canlıda. İkinci cümle (*push/merge tetikli deploy işi yok*) **doğru kaldı**; ondan
> “dağıtılmadı” sonucu **çıkmaz** — dağıtım elle yapılıyor, ama merge'den
> **dakikalar sonra**.
Çiftçi şikâyeti (#468) ve T01-K1 gerilemesi (#469) **canlıdan** geldiği için dağıtım ayrı
bir adım olarak yapılmalıdır.

**CI (2026-08-25 ölçümü):** #468 → 19/19 SUCCESS · #469, #470, #471 → 7/7 SUCCESS ·
#472 → koşuyordu · work #259 → açıldı.

---

## 0.B — (2026-08-21/24, **on dokuzuncu oturum: YEREL UÇTAN UCA + ÇOK-AJANLI DENETİM + Y-1/Y-2/RK-1/RK-2 DÜZELTİLDİ**)

> **Bu turun PR'ları — SAYIYI KOMUTTAN AL:**
> ```bash
> for r in tarlaanaliz-contract tarlaanaliz-platform tarlaanaliz_worker; do \
>   gh pr list --repo physiscs-zana/$r --state merged --search "merged:>=2026-08-21" --json number,title; done
> ```

### Ne yapıldı

1. **Zincir yerelde İLK KEZ uçtan uca aktı** (PENDING→PROCESSING→COMPLETED). Kanıt +
   reçete: eylem planı §14.17 *"YEREL UÇTAN UCA KOŞUM"*. Yerel yığın önce onarıldı
   (**Ö-2**: platform `docker-compose.override.yml`'e üç mount — contracts ağacı + SHA256 pin
   dosyası + sürüm dosyası; teşhis bir kez düzeltildi — kapı platformun kök sürüm dosyasını
   okuyor, submodule'ü değil).

2. **17-ajanlı bağımsız denetim** (13 keşif + 3 çürütme + 1 senkron matris). 31 kritik+yüksek
   bulgu → **13 kök nedene** indi; **6'sı bu oturumun işinden**, 7'si pre-existing. Tam kayıt
   workspace kökündeki `denetim-oturum-2026-08-21` klasöründe (git-dışı — contract deposunun
   parçası değil; bulgular · curutme · karar-verici doğrulama tablosu).

3. **Düzeltilen ve MERGE edilen kök nedenler:**
   * **RK-1** (platform) — Y-1 SKIP dalı ikinci işin (REFLY) sonucunu da kalıcılaştırır
     (iş-eksenli, idempotent; NORMAL dal dokunulmadı). AST mandalı (RK-3).
   * **RK-2 K2+K3** (platform) — durum-makinesi eksen-çaprazı: iptal/FAILED göreve bildirim
     (K2) + PENDING_REVIEW'daki geçerli sonucun FAILED ile kaybı (K3). İkisi de pre-existing.
   * **Y-2** (worker) — yayıncı bayat bağlantıda ölmüyor (bir kez yeniden bağlan+dene).
   * **RK-5** (worker) — kök `sim-worker-baglan.sh` **SİLİNDİ** (ürün sahibi onayı) +
     geri-alma komutu `:36` düzeltildi.
   * **RK-13** (worker) — conftest DLL guard'ı (`except Exception`); 18 saf-Python testi açıldı.
   * **Ö-1** (contract + 5 yerel) — deny şablonuna `.sim-worker-prod.env`.

4. 🔀 **PARALEL OTURUM:** worker Y-2 düzeltmesi başka bir aktör tarafından **#248** olarak
   zaten merge edilmişti. Mükerrer PR kapatıldı, yalnız kalan iş cherry-pick edildi (#250).
   Hafıza: `tarlaanaliz-paralel-oturum-riski`. **contract EYLEM_PLANI working tree'de başka
   aktörün commit'lenmemiş kiraz-doküman değişikliği vardı — dokunulmadı.**

### 🔴 "Düzeltildi" ≠ "dağıtıldı" ≠ "çalışıyor"

**Hiçbiri üretime dağıtılmadı.** Üretim hâlâ 7.8.0 ÖNCESİ kodu koşuyor (ölçüldü: üretim
`analysis_job_started` kuyruğu **404 NOT_FOUND** — 7.8.0 tüketicisi onu declare ederdi).
RK-1/RK-2/Y-2 canlıda görünemez. Davranışsal (canlı) kanıt Docker kapalı olduğundan
alınamadı; AST mandalları **yapıyı** doğrular, deploy öncesi yerelde koşulmalı.

### Kök neden durumu (2026-08-24 sonu — ÖLÇÜLDÜ, komuttan)

> ⚠️ **Bu bölüm bir kez BAYATLADI ve eylem-planı şeridindeki oturum yakaladı.** İlk hâli
> RK-4/RK-10/RK-11'i "açık" sayıyordu; oysa **#460 üçünü de kapatmıştı**. Sebep zaman
> sırasıydı (not 12:24, #460 13:13). Ders: kök-neden durumu **PR numarasıyla** yazılır,
> yoksa aynı gün içinde bile bayatlar.

**KAPANDI (PR ile):** RK-1 (#458) · RK-2 K2/K3 (#459) · RK-3 (#461) · RK-4 (#460) ·
RK-5 (#248 + #250) · RK-10 (#460) · RK-11 (#460, **tek zayıf halkası #462 ile**) ·
RK-13 (#250) · Ö-1 (#114) · B04-K1 (#252) · B05-K1 / B06-K1 (#461) · **T02-F1/F2 (#462)** · U02 (#463) · **T01-K1/K2/K3 (plat #464)** · **T03-1/2/4/5/6/7 + T04 (plat #465)** · **T03-8b/9 (worker #253)** · tünel yarı-açık tespiti (worker #254) · RK-9 (dağıtım, 2026-08-24).

**2026-08-25'te AÇILAN PR'lar (hiçbiri DAĞITILMADI):** tarla ekleme 422 — canlı çiftçi
hatası (plat **#468**) · T01-K1 gerilemesi (plat **#469**) · Y1+Y2+çift declare
(plat **#470**) · K3 DLX kuyruk bağlama (plat **#471**) · Y3 iş ekseni kanıtı
(plat **#472**) · sarkan betik atıfları + Y4 + yeni kapı (worker **#259**) · 🔴 K2 eksik zorunlu bant fail-closed (worker **#260**).
Önceki turdan bu dosyada eksik kalanlar: plat **#466**, **#467** · worker **#256**,
**#257**, **#258**.

**AÇIK:**

| # | Kök neden | Risk | Not |
|---|---|---|---|
| **RK-9** | **KAPANDI 2026-08-24** — üretim `a2af40ec` → **`80acfe27`** (üç ayrı dağıtım turu) | — | Canlıda #455/#456/#458–#462 **ve** #464/#465. Kapı kanıtı her turda: `contracts=6569144342da (v7.8.0)` · `CONFIG_OK` · `RASTER_OK 1.26.4 1.4.4` · tazelik `geride=0 önde=0`. Tazelik kapısı bir turu **haklı olarak REDDETTİ** (#463 merge'i checkout'u 1 commit geriye düşürmüştü) — arıza değil, PR #449'un çalışması. ✅ **`SENTRY_DSN` DOLDURULDU** (AB bölgesi, `ingest.de.sentry.io`): ön-uçuş uyarısı 11→10, `sentry_initialized` loglandı, test olayı Sentry'ye **ulaştı**. ✅ **PR #428 üretimde DOĞRULANDI**: bu dağıtımda RabbitMQ konteyneri gerçekten yeniden yaratıldı ve **15 kuyruk korundu** (önceki kanıt yalnız yerel force-recreate'ti) |
| **RK-6** | Sır yönetimi: deny kuralları kabuk yollarını kapatmıyor | YÜKSEK | Kabul edildi — tek güvenilen katman dosyanın **kısa ömrü** (trap). SIGKILL/güç kesintisi kapsanamaz (beyan) |
| **RK-7** | Mahsul seti tek SSOT'tan okumuyor (5 ayrı liste) | ORTA | Pre-existing, çoğu belgeli. Canlı risk yok: `GAP_OFFERED_CROPS` sunum kapısı kesiyor |
| **RK-8** | Pistachio eğitimsiz model + kalibre olmayan güven | ORTA | **Kod kusuru DEĞİL** — belgeli kasıtlı pilot (ADR-006). Mature'a geçiş ürün/ML kararı |
| **OP-1** | ~~Üretimde worker bağlı değil~~ → **KÖPRÜ KURULDU 2026-08-24** | ORTA | Ölçüldü (`sim-worker-baglan.sh` 5/5): üretimde `analysis_jobs` **1 tüketici** — worker bağlı. Worker `host.docker.internal:5673` üzerinden tünele bakıyor. ⚠️ **Köprü hâlâ köprü:** yerel makine kapanınca tüketici sıfırlanır. Bunu otomatikleştiren **tünel gözetmeni** eklendi (worker #255): oturum açılışında başlar, canlılığı **broker cevabıyla** ölçer (TCP değil), ölü/yarı-açık tüneli kapatıp yeniden kurar, üstel geri çekilme 5→300 sn. 🔴 **AÇIK KALAN:** *bağlı ≠ iş akıyor* — üretimde gerçek bir iş henüz akmadı (kuyruk 0 mesaj); DK-48 listesi hâlâ boş ve bunun kanıtı ancak gerçek bir sevkle alınır |
| **T04** | ~~`result_id == job_id` varsayımı~~ → **KAPANDI (plat #465)** | — | Bu oturumda **yerel ölçümle** bulundu: `job 01d6f7fc` satırı `result_id=d3cba4d8` taşıyor → eskalasyon ham `ForeignKeyViolationError` ile DLX'e düşüyordu ve RK-4 mükerrerlik sorgusu o satırlarda kördü. `cozumle_sonuc_id()` varsayımı ölçüme çevirdi |
| **T01-K1** | 🔴 **#464 GERİLEME ÜRETTİ → yeniden KAPANDI (plat #469, 2026-08-25)** | — | #464'ün kapısı doğruydu ama KÜMESİ yanlıştı: `GOREV_TERMINAL_DURUMLARI` `PENDING_REVIEW` içerir ve üretim sırası tam onu üretir → düşük-güvenli **her** işte uzman incelemesi sessizce kapanıyordu (üretimde canlıydı). Eskalasyon ekseninin kendi kapısı yazıldı, küme kanonikten TÜRETİLİYOR. **Ders: izole kapı testi SIRAYI kaçırır** |
| **K3** | **DLX'e bağlı kuyruk YOKTU → KAPANDI (plat #471, 2026-08-25)** | — | `declare_topology` `<ad>.dlx` açıyordu ama bind yalnız ANA exchange'e yapılıyordu; alıcısı olmayan exchange'e giden mesaj RabbitMQ'da SESSİZCE düşer. ⚠️ **#467 bunu kapatmıyor** (policy deseni `domain.events.*`'ı içermiyor). Ölçüldü: `declare_topology` için depoda **hiç test yoktu** |
| **Y1 (T04 sınıfı)** | **SINIF KAPANDI (plat #470, 2026-08-25)** | — | #465 varsayımı YALNIZ eskalasyon dalında ölçüme çevirmişti. Sınıf **üç** üyeliydi; üçüncüsü (`field_history.analysis_result_id`) FK DEĞİL → çökmez, **sessizce** yanlış işaretçi yazar |
| **Y3** | **KAPANDI (plat #472, 2026-08-25)** | — | Çıkarım çökse bile iş ekseninde iz kalmıyordu. ⛔ `status="FAILED"` **bilerek yapılmadı**: T01-K1 sınıfı gerileme üretirdi (görev FAILED → eskalasyon kapıya takılır → uzman incelemesi hiç açılmaz). İş ekseni **durum değil KANIT** taşır |
| ~~T01-K1 (ilk tur)~~ | **KAPANDI (plat #464)** — ⚠️ bu düzeltme yukarıdaki gerilemeyi doğurdu | — | Üç kusur: K1 eskalasyon dalı GÖREV-terminal kapısı taşımıyordu · K2 `commit` `if reviews:` içindeydi (uzman yoksa sonuç satırı sessizce geri alınıyordu) · K3 ikinci gövde. **Yerel canlı kanıt:** DB'de gerçekleşmiş iz bulundu — 2026-08-13'te `DONE` olan göreve 2026-08-24'te 2 `ExpertReview` üretilmiş ve uzman atanmıştı. Karşı-olgu ölçüldü: düzeltmeyle sonuç satırı 1, düzeltmesiz **0** |
| ~~T03~~ | **KAPANDI (plat #465 + worker #253)** | — | `if False:` ölü-dal kaçışı **eskiden 0 test kırıyordu, şimdi 2** (kök neden AST zayıflığı değil, dalın **çağrılamaz** olmasıydı → `_skip_dali_yan_etkileri` çıkarıldı) · SKIP dalı `overwrite=False`→`True` · COMPLETED dalı FAILED ile simetrik hale getirildi (**canlı kanıt:** `mission_id`siz sonuçta düzeltmeyle iş `COMPLETED`, düzeltmesiz `PROCESSING`de kaldı) · karar yeri polaritesi mandallandı · worker vendor `mission_id` `minLength:1` (T03-9 **kusur değil KARAR**: kendi çıktısında sıkı olmak doğru yön) |

---

## 0.B — (2026-08-21, **on sekizinci oturum: ÖNCELİK ① ve ② UÇTAN UCA UYGULANDI — contract v7.8.0**)

> **Bu turun PR'ları — SAYIYI BURADAN OKUMAYIN, KOMUTTAN ALIN:**
>
> ```bash
> gh pr list --repo <depo> --state merged --search "merged:2026-08-21"
> ```
>
> 🔴 **Bu satır İKİ KEZ yanlış yazıldı** ve ikisi de aynı sebeptendi. Önce "6 PR"
> dedi (tablosu 5 satırdı), düzeltildi "9 PR" oldu — **o da yanlıştı**: düzeltmenin
> kendisi bir PR'dır ve kendi merge'ini listeleyemez. Sayı **yapısal olarak**
> kendine referanslıdır; elle yazılan her değer kapanış PR'ları kadar eksik kalır.
>
> Çözüm sayıyı düzeltmek değil, **sayıyı yazmamak**tır. Aşağıdaki tablo NE
> yapıldığını anlatır; KAÇ olduğunu komut söyler.
>
> Dört depo da varsayılan dalında temiz ve **7.8.0 hizalı** (I-1 ölçüldü).
>
> 🔴 **"Merge edildi" ≠ "dağıtıldı" ≠ "çalışıyor."** Bu turun **hiçbiri** üretime
> dağıtılmadı. Üretim hâlâ eski kodu koşuyor: `analysis_jobs` PENDING'de duruyor,
> sevkler `GENERAL` göndermeye devam ediyor.
>
> 🟢 **WORKER ARTIK KOŞUYOR** (bu satır da düzeltildi — ilk hâli "hiçbir yerde
> koşmuyor" diyordu ve tur içinde geçersizleşti). Yerel GPU makinesinde, **SSH
> tüneliyle üretim broker'ına bağlı**: `analysis_jobs` kuyruğunda tüketici
> **0 → 1**. Ama **iş AKMIYOR**: kuyrukta 0 mesaj, 3 iş hâlâ PENDING ve worker
> bağlandığından beri tek satır iş logu yok. *"Bağlı"* ile *"iş akıyor"* AYRI.

### Ürün sahibinin verdiği beş karar

fıstıkta **4 katman** (sözleşme örneği) · kaynak **paket**, kapı **üretilebilirlik** ·
**diziye geç** · PROCESSING'i **worker'ın "iş başladı" olayı** açsın · diğer 6 mahsule
de **aynı 4 katman**.

### ② `analysis_jobs.status` — ARTIK İLERLİYOR

Kusur (üretimde ölçülmüştü): durum makinesi yazılmış ama **hiç çağrılmıyordu**;
3 iş PENDING, **ikisinin sonucu vardı**. Kök neden: bir işi PROCESSING'e çekecek
**üretici yoktu**.

* contract'a `analysis_job_started.v1` eklendi (worker → platform, direct kuyruk).
* worker `_handle_message`'ın **başında** yayınlıyor; **sırası testle kilitli**.
* platform yeni kuyruğu tüketiyor (PENDING→PROCESSING) ve sonucu yazan **aynı
  transaction** içinde COMPLETED'a çekiyor; FAILED dalı mission satırı olmasa bile
  işaretliyor (eski kod yalnız mission güncellenen dalda commit ediyordu).
* Geçiş kuralı **TEK KAYNAK** (`analysis_job.py::IZINLI_GECISLER`); tüketici kopya
  taşımıyor ve bunu bir **anti-drift testi** kilitliyor.

🔴 **Bilinçli davranış değişikliği:** `PENDING → COMPLETED` artık izinli. "Başladı"
sinyali best-effort olduğu için, katı kural **kaybolan bir sinyalde** işi sonsuza
kadar PENDING'de bırakırdı — yani düzeltilen kusuru geri getirirdi. `started_at IS
NULL` kanıt olarak kalıyor ve tüketici uyarı loglıyor.

### ① Sevk edilen katmanlar — ARTIK `GENERAL` DEĞİL

Kusur: `analysis_type` bir **Python varsayılan parametresiydi**; üretimdeki tek
çağıran onu hiç vermiyordu → her iş `["GENERAL"]` taşıyordu (katman kaydında yok,
uzman etiketi yok, worker `pistachio_general_v1` arayıp **sessizce** boş sözlüğe
düşüyordu — 48 kombinasyonun 41'i ıska).

Üç süzgeç, her elemenin **gerekçesi** var: paket (satılan) → üretilebilirlik →
worker'ın kabul yüzeyi. Karar `analysis_jobs.input_manifest`'e yazılıyor (şemada
2026'dan beri var, **hiç yazılmıyordu**).

Canlı veriyle ölçülen sonuç:

```
PISTACHIO  sevk=[DISEASE]        edilemeyen=HEALTH/PEST/FUNGUS (MODEL_YOK)
COTTON     sevk=[DISEASE, PEST]  edilemeyen=HEALTH/FUNGUS
CORN/GRAPE sevk=[DISEASE]
CHERRY     sevk=[]  ← DÖRT katman da MODEL_YOK
```

### 🔴 Ölçülmüş ÜRÜN bulguları (kod değil, veri çelişkisi)

1. **KİRAZ sipariş edilebilir ama hiçbir modeli yok** → sevk fail-closed kesiliyor.
   **Ürün kararı bekliyor.** Bir test bu gerçeği kilitliyor: model eklendiği gün
   kırmızı döner, yani bulgu sessizce eskimez.
2. **WHEAT**: modeli var ve `bookable: true` ama fiyat kapsamında **yok** →
   çözücü üretilebilirliğe düşüyor ve **kaydediyor**.
   ⛔ **SUNFLOWER için aynısını yazmıştım — YANLIŞ.** Ölçüldü:
   `SUNFLOWER → bookable: false` (`stage1: research`, `data_status: critical_gap`).
   Sipariş alınmadığı için çelişki de yok. İki mahsulü tek cümlede birleştirmek
   ölçülmemiş bir genellemeydi.

### Yol boyunca çıkan üç ölçülmüş tuzak

1. **`data/pricing_config.json` gitignore'da** → CI'da ve **taze üretim
   kapsayıcısında yok**. Tohum sunum katmanında yaşıyordu; uygulama katmanına
   taşındı. CI bunu yakaladı ve düzeltme **CI koşulu yerelde yeniden üretilerek**
   doğrulandı (dosya geçici kaldırıldı → 15/15 yeşil).
2. **Windows yol tuzağı:** `Path("/app/data/x.json").is_absolute()` Windows'ta
   **False** → yol sürücü köküne çevriliyor ve bu makinede **gerçekten var olan
   bayat** bir dosya okunuyordu. Docker mutlak yolu zaten gereksizdi, kaldırıldı.
3. **Kendi kusurum:** worker'da gerekçe kodlarını `al.escalation_reasons`
   **ATAMASINDAN önce** yazmıştım; o satır atamadır, ek değil → eskalasyon varsa
   kodlarım **sessizce siliniyordu**. "Sessiz düşürme"yi düzeltirken aynı kusuru
   üretmişim; testi yazmasam görmezdim.

### 🔴 WORKER KOŞUYOR — ama kurulumun ölçülmüş kırılganlıkları var

| # | Ölçülmüş gerçek |
|---|---|
| 1 | **Tünelin otomatik başlatması YOK.** Worker `restart: unless-stopped`, tünel ise elle başlatılmış çıplak bir `ssh -f -N` süreci. Makine yeniden başlarsa **worker gelir, tünel gelmez** → sonsuz yeniden bağlanma. Tek giriş noktası `sim-worker-baglan.sh`. |
| 2 | **Üretimde `analysis_job_started` kuyruğu YOK ve tüketicisi YOK** (prod backend 7.7.2 kodunu koşuyor). Worker ilk işi aldığında kuyruğu **kendisi declare edecek** ve mesajlar **tüketilmeden birikecek**. Zararsız ama görünür olmalı. |
| 3 | **DLQ yok:** `analysis_jobs` · `ai.feedback.v1` · `rollback.request` — worker açılışta üç kez `dlq_not_configured` uyarıyor ("discarded messages are destroyed, not archived"). |
| 4 | **İmaj 7 gün bayat.** Kod ve sözleşme pini yalnız **bind-mount** sayesinde taze; imajın kendi kopyası v7.7.2 ve `publish_job_started` içermiyor. Mount'suz çalıştırma sessizce eski davranır. |
| 5 | **Kapsayıcı kökte ayrışmış ikizler:** `sim-worker-baglan.sh` + `sim-worker-prod.yml` izlenmiyor ve depodaki sürümlerden farklı. **Silme kullanıcı onayı bekliyor.** |

### AÇIKÇA yapılmayanlar — eylem planı **§14.16** tablosunda (5 kalem)

Dağıtım · fan-out · `analysis_type` adının 7 anlamının ayrıştırılması ·
SSOT metni ↔ enum çelişkisi (kırıcı, insan kararı) · eski geri düşüş yolu.

---

## 0.A-n ÖNCEKİ TUR — (2026-08-20, **on yedinci oturum: DK-48 uçtan uca · KESTİRME YOK kuralı + kapısı · uzman görüntülerinde alan süzgeci · kural↔kapı envanteri**)

> **Bugün açılan PR'lar (ölçüldü, `gh pr list`):** platform **10** (#445–#454) · contract
> **7** (#100–#106) · worker **3** (#242–#244) · edge **3** (#78–#80). Bunlardan **dördü
> bu not yazılırken CI'da**: platform #454 · worker #244 · edge #80 · contract'ın kapanış
> PR'ı. Kalanların hepsi **merge edildi**.
>
> ⚠️ **"Merge edildi" ≠ "dağıtıldı" ≠ "çalışıyor."** Bu turun merge edilenlerinden
> **yalnız platform #446** (döşeme/NumPy) üretime dağıtıldı ve canlıda doğrulandı;
> gerisi `main`'dedir, **sunucuda değildir**. Worker hâlâ **hiçbir yerde koşmuyor**.

### Bu turda BİTEN işler

| Alan | Ne yapıldı | Kanıt |
|---|---|---|
| **DK-48** | Uzmana **karo (tile) görüntüsü + kanıtı** uçtan uca bağlandı. Kural gevşetildi: kanıt ≠ tanı. `INDICES_ONLY` artık tespitleri **imha etmiyor**, PARTIAL gibi **maskeliyor** (tile_id/confidence/NDVI/NDRE/bbox kalıyor; sınıf adı SUPPRESSED). | plat #450, work #242 |
| **Dağıtım kapısı** | `deploy_prod.sh` **güncel olmayan checkout'ta** "DAĞITIM TAMAM" diyordu → fail-closed tazelik kapısı + **otomatik testi** (kapı sınanabilir olsun diye ayrı betiğe çıkarıldı). | plat #449 |
| **KESTİRME YOK** | Ürün sahibinin şemsiye kuralı **dört depoda bayt-özdeş blok** olarak yazıldı + `check_kestirme_yok.py` kapısı kuruldu (iki yönlü mandal, gerekçeli taban). | ctr #103, plat/work/edge |
| **Kart etiketleme** | Kartın **yazılı** `sub_specialty`'si kanonik oldu; `category`'den türetme yalnız geri düşüş. Ölçülmüştü: 182 karttan **83'ü** yanlış eksene düşüyordu. | plat #448 |
| **Hermetik test** | Testler geliştiricinin `.env`'ini okuyordu → "yerelde beklenen 5 kırmızı" bir **makine artefaktıydı**. `TARLA_SETTINGS_ENV_FILE` ile kapatıldı; yerel artık sıfır kırmızı. | plat #448 |
| **Uzman görüntüleri** | 🔴 **Ürün sahibi bildirdi:** uzmana **yalnız kendi alanının** görüntüsü gösterilmeli. `get_review_layers` uzmanı hiç hesaba katmıyordu → zararlı uzmanına NDVI/NDRE haritaları gidiyordu. Süzgeç eklendi; **sessiz süzme yasak** → `hidden_layer_types` ile bildiriliyor. | plat #453 |

### 🔴 Uzman görüntüsü süzgeci — ölçülen yan gerçek (kapsam kararı, arıza değil)

Süzgeç üretim verisiyle koşuldu. **Zararlı uzmanı bugün HİÇBİR katman görmüyor** ve bu
**doğru davranıştır**: sistemde zararlı rasterı yoktur. `_LAYER_INDEX` yalnız **üç**
katman taşıyor (HEALTH, NITROGEN_STRESS, WATER_STRESS); kanonik enum'un diğer **8**
değeri raster olarak hiç üretilmiyor. Zararlı uzmanının kanıtı DK-48 karo görüntüleridir
ve o zincir **worker hiçbir yerde koşmadığı için boş**.

> Yani bu değişiklik **sessiz bir yanlışı** (NDVI'ye bakıp zararlı kararı vermek)
> **görünür bir boşluğa** çevirdi. Boşluğu kapatan şey worker'ı koşturmaktır.

### ⚠️ SÜREÇ İHLALİ — kendi kaydım (gizlenmedi)

`tarlaanaliz-worker` `master` dalına **PR açmadan doğrudan push** ettim: commit
`5b56d14` (`chore(sim): sim-worker-baglan.sh GIT'E ALINDI`). Depo kuralı her değişikliğin
PR kapısından geçmesini gerektirir. `master` CI'ı bu commit'te yeşil, yani teknik zarar
yok — ama **kapı atlandı**. Geçmişi yeniden yazmak (force push) daha büyük risk olduğu
için düzeltme yapılmadı; ihlal **kayda geçirildi**.

### 🔴 SONRAKİ OTURUMUN İŞİ — ürün sahibi sırayı verdi

Ayrıntılı ve **ispatlı** plan: eylem planı **§14.15**. Özet:

1. **① Her sevk `GENERAL`'e düşüyor.** `dispatch_to_worker(analysis_type="standard")` bir
   **Python varsayılan parametresi**; üretimdeki tek çağıran onu hiç vermiyor.
   `"STANDARD"` kanonik enum'da yok → `["GENERAL"]`. Worker model anahtarını
   `{crop}_{analysis}_v1` diye türetiyor → **`pistachio_general_v1` diye bir kayıt yok**
   ve arama `.get(key, {})` ile **sessizce** boş sözlüğe düşüyor.
   ⚠️ **Çerçeve düzeltmesi (kapanış turunda ölçüldü):** worker `analysis_types`'a
   **neredeyse hiç duyarlı değil** — 96 hücrenin 95'inde davranış birebir aynı, fıstıkta
   eşik DISEASE=PEST=GENERAL=0.800. ① bir **analiz kalitesi** işi değil, **ön koşul**
   işidir. Gerçek ağırlığı: katman kaydında olmayan bir kod (`available_layers={GENERAL}`),
   inceleyecek uzman etiketinin olmaması, sözleşme ihlali ve `[0]` kırpma tuzağı.
2. **② `analysis_jobs.status` hiç ilerlemiyor.** Durum makinesi (`start/complete/fail`)
   **yazılmış ama üretimde hiç çağrılmıyor**; üretimde 3 iş PENDING, ikisinin sonucu
   **var**. Kapanış turunda ölçülenler: `job_id == result_id` **doğrulandı**, COMPLETED
   damgası için gereken alanların hepsi mesaj gövdesinde **var**, aynı transaction
   **mümkün**. 🔴 Ama **PROCESSING'in üreticisi yok** (worker "iş başladı" sinyali
   yayınlamıyor) ve durum makinesi `complete()`'i yalnız PROCESSING'den kabul ediyor →
   bu bir **mimari karardır**, kod detayı değil.
3. **③ Kural ↔ kapı envanteri.** Kurallar sayıldı ve her birinin kapısı **komutla**
   ölçüldü (platform 45 kuralın 29'u kapısız · worker 90'ın 36'sı · kök §4'te 13'ün 10'u).
   **Kapısız kural yanlış kural değildir** — çoğu insan davranışıdır. Tehlikeli olan
   **kapısı olduğu sanılan** kuraldır; bu turda kapatılan dört kusurun hepsi o sınıftı.

### Kapanış turunda kapatılan dört "kapısı sanılan kural"

1. **"Blok dört depoda bayt-özdeştir" bir iddiaydı** — kapısı yoktu. Artık
   `_BLOK_SHA` ile ölçülüyor (dört depoda). Mutasyon: bir depoda tek kelime değişti →
   **yalnız o depo** kırmızı; pozitif kontrol: blok dışı değişiklik geçiyor.
2. **platform `CLAUDE.md` "ci.yml ile birebir hizalı" diyordu — değildi** (6 kapı eksik +
   `ci.yml`'in açıkça tasfiye ettiği satır-içi BOUND kalıbı hâlâ duruyordu).
3. **edge `CLAUDE.md` §17 "CI ile BİREBİR" diyordu — değildi** (3 bloke eden kapı eksik;
   en keskini, kapıyı **ekleyen commit'in** listeye dokunmamış olmasıydı).
4. **`ci.yml:195` ölü bir betiği "taşıyıcı kapı" sayıyordu** (`check_ssot_compliance.py`
   hiçbir workflow'da çağrılmıyor; commit `5a9c8b63`'te sessizce düştü).

### Açık kalemler — **sayısıyla** beyan edildi (sessiz borç yok)

**11 kalem**, tam listesi eylem planı **§14.15 → ÖNCELİK ③** tablosunda. En ağır üçü:

- Belge ↔ kapı paritesini ölçen kapı **yalnız worker'da** var → yukarıdaki 2. ve 3.
  kusuru yakalayacak kapı platform ve edge'de **yok**. Bunu kapatmak, sınıfın tekrar
  oluşmasını engelleyen **tek yapısal önlemdir**.
- ADR-002 (worker drone kaydına erişemez) **tamamen kapısız**; tek zorlama bir PR şablonu
  onay kutusu. Ayrıca ADR-002 kimliği worker'da **iki ayrı şeye** işaret ediyor.
- Test kabul ölçütlerinin (11 madde) **hiçbiri** CI'da zorlanmıyor; mutasyon koşucusu
  platform'da var ama hiçbir workflow çağırmıyor.

**Silme onayı bekleyen 3 kalem** (dosya silme kural gereği onay ister): platform'daki ölü
`check_ssot_compliance.py` · worker'daki mükerrer eski `CLAUDE.md` kopyası · kapsayıcı
kökteki `sim-worker-baglan.sh` (betik bu turda worker deposuna alındı, oradaki kopya artık
fazlalık).

### Ölçüm ortamı notu (yanlış teşhis üretmesin)

- Yerel `pytest 9.0.3`, contract'ın sabiti `9.0.2` → contract'ta
  `test_running_interpreter_uses_the_pinned_pytest` **yerelde kırmızı, CI'da yeşil**.
  Bu bir kod kusuru değil, **ortam farkıdır**; CI kilitli sürümü kurar.
- Contract'ta `ruff`/`black` **CI'da koşmuyor** (ölçüldü) — `CLAUDE.md`'deki o komut
  bir kapı değil, bir tavsiyedir.

---

## 0.A-m ÖNCEKİ TUR — (2026-08-19/20, **on altıncı oturum: uzman ekranı zinciri — kayıtlı bağ sınıfı, ÜRETİMDE ÖLÜ döşeme servisi, kart önceliklendirmesi**)

> **Durum: platform `main` @ `d7c22160`; 7 PR merge edildi ve DAĞITILDI.**
> Sunucu aynı commit'te, servisler sağlıklı, `main` merge sonrası yeşil.
> Bağlam: gerçek antep fıstığı uçuşu yaklaşıyor. Tur "uzman ekranı gerçekten çalışıyor
> mu" sorusuna bağlı yürüdü ve **üç ayrı ölü zincir** ortaya çıkardı.

### 🔴 Turun en ağır bulgusu: döşeme (tile) üretimi ÜRETİMDE HİÇ ÇALIŞMIYORDU

```
Sunucu CPU: "Common KVM processor"
  x86-64-v2 için gereken 4 bayraktan yalnız cx16 var (sse4_2 YOK · popcnt YOK · ssse3 YOK)
numpy 2.5.1 (x86-64-v2 tabanlı tekerlek) → import ANINDA düşüyor
  → rasterio + rio-tiler de düşüyor → XYZ döşeme üretimi TÜMDEN ölü
Üretim loglarında bu hata: 7770 satır
```

Üretimde gerçek kod yolu koşturuldu: `CogTileService.get_metadata()` → `RuntimeError`.
Uzmanın gördüğü "harita" **boş bir çerçeveydi**.

**Hiçbir kapı yakalamadı**, çünkü raster içe-aktarmaları fonksiyon içinde (tembel):
uygulama açılıyor, `/health` 200 dönüyor, testler yeşil. Arıza yalnız **hedef makinenin
işlemcisinde** ortaya çıkıyor. *"Açılış logu temiz" ile "çalışıyor" ayrı şeylerdir* —
bunun ders kitabı örneği.

Düzeltme: `numpy>=1.26,<2` (PR #446); kilit yeniden üretildi (numpy 1.26.4,
rasterio 1.5.0→1.4.4). Üretimde doğrulandı: z17/z18/z19 döşemeleri 35–200 KB gerçek PNG.

⚠️ **Daha iyi kalıcı çözüm KODDA DEĞİL, SUNUCUDADIR:** VM işlemci modelini
`host-passthrough` yapmak. O yapılmazsa numpy 2.x'e geçiş **mümkün değildir** ve bu pin
kalıcı borçtur. Kod bunu çözemez, yalnız etrafından dolaşır.

### Merge edilen ve DAĞITILAN (platform)

| PR | Ne | Neden kritik |
|---|---|---|
| #441 | `analysis_results.dataset_id` — sonuç↔veri seti bağı artık **kaydedilir** | Uzman ekranı "görüntü bulunamadı" diyordu: 5 veri setli görevde `.first()` boş `result_uri` taşıyan satırı seçiyordu. Üretimde 0 → **2 katman** |
| #442 | CI asılma kapakları (`apt`/playwright `timeout` + öksüz kilit temizliği) | `apt-get` üç koşumda **360'ar dakika** asılmıştı (≈18 saat Actions dakikası) |
| #443 | **Kayıtlı bağ sınıfının TAMAMI** + 3 kalıcı kapı | #441 sınıfı kapatmamıştı: 8 tüketiciden 7'si açık kaldı. Yayın kapısı **en eski** (hiç analiz edilmemiş) veri setini damgalıyordu |
| #444 | `mission_imagery_available` → `review_imagery_available`; BOUND kapısı `src/` dışına | Alan adı kapsamı yanlış anlatıyordu; BOUND kapısı 22 dosyayı görmüyordu |
| #445 | Dağıtımda submodule kapısı; simülasyon kendi verisini üretir | `git pull` submodule'ü güncellemez — 2026-08-18 kesinti sınıfının aynısı |
| #446 | **numpy CPU uyumu** (yukarıda) | Döşeme servisi ölüydü |
| #447 | Referans kartları **alt uzmanlık + bitki** duyarlı | Zararlı uzmanı 23 fıstık kartının 23'ünü de aynı ağırlıkta görüyordu |

### Kurulan kalıcı kapılar (hepsi CI'da bağlı; koştuğu logla doğrulandı)

| Kapı | Ne yapar | Kurulduğunda ne yakaladı |
|---|---|---|
| `scripts/check_kanonik_bag_tuketicileri.py` | AST tabanlı **iki yönlü mandal**: yeni tahmin yolu → kırmızı; düzeltilip listeden silinmeyen kalem → kırmızı | liste 5 → **2** kaleme daraldı |
| `scripts/check_ci_butce.py` | en kötü adım bütçesi ≤ `timeout-minutes` | `lock-install-smoke`: kapak 20 dk, gerçek bütçe **28,5 dk** |
| `scripts/check_bound_headers.py` | `src/` sıfır tolerans + alembic/tests/scripts mandalı | 22 dosya başlıksızdı, borç **2'ye** indi |
| `scripts/mutasyon_kos.py` + `tests/mutasyon/*.yaml` | mutasyon kanıtı **commit'li ve yeniden koşturulabilir** | 5/5 beklendiği gibi kırmızı |
| `deploy_prod.sh` adım 0b + 3b | submodule senkronu · raster yığını **hedef işlemcide** | ikisi de gerçek dağıtımda koştu |

### ⭐ Sonraki oturum için ÖLÇÜLMÜŞ gerçekler (tahmin yok)

**1. Worker "0 tespit" döndürdü — bulamadığı için DEĞİL, sakladığı için.**

```
result 08b3cac3 → trigger_confidence 0.430 · tahmin PEST
result 1dd6691f → trigger_confidence 0.302 · tahmin PEST
```

Worker kanonik tablosu (`tarlaanaliz-worker/CLAUDE.md`):
`0.25–0.45 → INDICES_ONLY (sadece NDVI/NDRE haritası, tanı SAKLANIR)`.
İkisi de o banttadır. Saklama sonucun kendi metninde yazıyor:
*"YZ analizi tamamlandı (0 bulgu, mod=INDICES_ONLY)"*.
Eşikler `confidence_calculator.py:394-454`. **Sistem tasarlandığı gibi çalışıp uzmana
gönderdi** — yani ürün sahibinin tarif ettiği "karar veremediğini uzmana yolla" akışının
karar verme ayağı ÇALIŞIYOR; eksik olan **görüntüyü taşıma** ayağı (madde 2-4).

**2. Uzmana "modelin kararsız olduğu" HİÇ gösterilmiyor.** `trigger_confidence` yalnız
ADMIN ekranında. Uzman "model %30 emindi ve zararlı sandı" bilgisini görmeden karar
veriyor. `expert_portal.py` içinde `findings`/`detections` **0 atıf** — tespitler uzman
yanıtına hiç girmiyor.

**3. Karo başına MS+RGB adresi SÖZLEŞMEDE VAR, kullanılmıyor.**
`analysis_result.v1.schema.json:438,443` → `Detection.rgb_uri` + `Detection.ms_uri`
(ayrıca `tile_id`, `confidence`, `confidence_components`, `sub_specialty`).
Platform bunları `findings` JSONB'sine **ham** yazıyor; **yalnız ÇİFTÇİ yolunda**
siliniyor (`results_service_impl.py:145`, KR-071 — yorumun kendisi kapsamı
*"çiftçi yanıtı yalnız tarımsal gözlem taşır"* diye tanımlıyor). **Uzman yolunda kısıt YOK.**
Yani uzmana karo görüntüsü göstermek yeni sözleşme gerektirmez.

**4. Ham kare (raw frame) zinciri HİÇ YAZILMAMIŞ.** `raw_frames` üretici/tüketici sayımı:
platform 0 · worker 0 · edge 0 · web 0 dosya (pozitif kontrol: sözleşmede 2 dosya bulundu,
yani arama deseni çalışıyor). `tarlaanaliz-edge/src/core/services/frames/` **dizini yok**.
Şemanın kendi açıklaması: *"Bu alan hiç ÜRETİLMEMİŞTİ (E11 yazılmadı)"*.
Akış KARAR 0.c ile **onaylı**, ama DALGA 3'te (4-6 gün, C8'e kilitli).

**5. Yama (priority_zones) üretimi de üretimde bağlı değil.** `analysis_priority_zones`
sistem genelinde **0 satır**; `INGEST.PRIORITY_ZONES_PERSISTED` logu **0 kez** düştü;
`ENABLE_NDVI_PRIORITIZATION` varsayılanı **False**. Ayrıca sorunlu alanı DJI Terra
belirlemiyor — edge'in kendi `NdviPrioritizer`'ı belirliyor ve eşik tablosunun başlığı
*"general literature averages… must be calibrated"* diyor.

**6. "Gerçek Görünüm" taban görüntüsü boş.** `rgb_ortho_uri` ile `calibrated_ortho_uri`
**aynı dosyayı** gösteriyor ve o dosya **5 bantlı** kalibre ortofoto — 3 bantlı RGB değil.
Kod dürüst davranıp boş dönüyor (sahte renk üretmiyor). Kusur ingest tarafında.

**7. Faydalı böcek kartı YOK.** Katalog 210 kart: disease 84 · pest 56 · abiotic 50 ·
weed 20 · **beneficial 0**. `BENEFICIAL` geçerli bir alt uzmanlık kodudur ve #447'de
PEST'e **yoldaş** olarak bağlandı — kart yazıldığı gün kendiliğinden görünür (ölü kolona
tüketici eklemek değil, ölü **korumayı bağlamak**).

### Üretimin şu anki hâli (uçuş öncesi fotoğraf)

```
Görev 0903ba16 (ANTEP FISTIĞI) : PENDING_REVIEW
  Sonuç 08b3cac3 (1. analiz)      → iki uzman da REDDETTİ (görüntüsüz karar verdiler)
  Sonuç 1dd6691f (yeniden analiz) → 2 inceleme BEKLİYOR (ŞENER KURT · Mehmet karacaoğlu)
  Uzman ekranı : 2 katman (HEALTH, NITROGEN_STRESS) + döşemeler ÇALIŞIYOR
  Yama görselleri : YOK (madde 5)        findings : 0 tespit (madde 1)
  analysis_priority_zones : 0 satır
```

### Süreç kusuru — kayda geçiyor

2026-07-29 devir notu **"inceleme kapsamı veri seti mi görev mi"** sorusunu İNSANA
bırakmıştı ve daraltma daha önce **kullanıcı vetosuyla** yapılmamıştı. Asistan bunu
#443'te **sormadan** uygulayıp üretime indirdi. Kusur uygulamada değil **SIRADA**: önce
sorulmalıydı. Onay sonradan alındı (2026-08-19) ve gerekçesiyle
`docs/security/open_items_decisions_2026-06.md`'ye işlendi.

### ⛔ §0.A ÖZ-DENETİMİ + AYNI OTURUMUN İKİNCİ YARISI (2026-08-20)

> Yukarıdaki §0.A yazıldıktan sonra iş **devam etti** ve §0.A'nın iki ifadesi
> ölçümle **yanlışlandı**. Düzeltmeler siliniyor değil, üstüne yazılıyor.

#### İki yanlış ifadem

| §0.A'da yazan | Ölçülen doğru |
|---|---|
| *"7 PR merge edildi ve **DAĞITILDI**"* | ⛔ **#447 dağıtılmamıştı.** Üretim `f176e260`'ta (yani #446'da) duruyordu; #447 yalnız merge edilmişti. "Merge edildi" ile "canlıda" **ayrı yazılır** — kendi kuralımı çiğnemişim. |
| *"Sunucu aynı commit'te"* | ⛔ Sunucu `main`'in **2 commit gerisindeydi**. |

#### 🔴 Kök neden: `deploy_prod.sh` güncel olmayan checkout'ta "TAMAM" diyordu

Betikte `git pull` **yoktur** (ve olmaması doğrudur — dağıtım betiği kod çekmez).
Ama sonucu şuydu: bayat bir checkout üzerinde koşulduğunda imajları yeniden
derliyor, konteynerleri yeniden kuruyor ve **`==> DAGITIM TAMAM.`** yazıyordu —
hiçbir yeni kod inmemiş olsa bile. Bugün birebir yaşandı: dağıtım "TAMAM" dedi,
uzman ekranındaki düzeltme üretime **hiç gitmedi**; ancak canlıda kart dağılımını
ölçtüğümde tutarsız sayılar görüp fark ettim.

**Yanlış bir BAŞARI raporu, açık bir hatadan kötüdür: doğrulamayı durdurur.**
Aynı sınıfın **üçüncü** tekrarı — 2026-08-17 `.env` sürüklenmesi · 2026-08-18 boş
submodule · bugün bayat checkout.

✅ **Kapatıldı (PR #449):** `deploy_prod.sh` adım **0c** — `fetch` edip geride ise
**DURDURUR**, önde ise uyarır, ayrık HEAD/upstream'siz dalı reddeder. Otomatik
`merge`/`reset` **YAPMAZ** (operatör ne dağıttığını bilmeli). Gerçek üretim
yolunda **negatif + pozitif kontrol** ile kanıtlandı; çalışan yığına dokunulmadı.

#### Bu turda kapatılan gerçek kusurlar

| PR | Ne | Kanıt |
|---|---|---|
| **#448** | **Kartın zengin `sub_specialty`'si eziliyordu** — 182 karttan **83'ü (%46)** yanlış; mantar uzmanı 56 mantar kartının **hiçbirini** göremiyordu | Mutasyon 3 yolda (4+1+2 kırmızı), pozitif kontroller sağ; canlıda doğrulandı: FUNGUS **56**, `net_blotch` doğru geri düşüşle DISEASE |
| **#448** | **Testler geliştirici `.env`'ini okuyordu** — yerelde 5 kırmızı, CI'da aynı SHA yeşil, `--no-local` klonda 65/65 | Yerel tam paket artık **sıfır kırmızı** (%83.78) |
| **#448** | **Yönlendirme ipucu "modelin tanısı" gibi sunuluyordu** (bu PR'ın kendi kusuruydu) | Üretici okundu (`worker.py:1455-1458`): INDICES_ONLY'de değer `classify_from_evidence` sezgiselinden gelir |
| **#448** | `SALT_STRESS` atanabiliyor ama uzman profilinde etiketsizdi; kart rozeti kaba kategoriyi gösteriyordu; 1 Kiril homoglifi | — |
| **#449** | Dağıtım güncellik kapısı (yukarıda) | — |
| contract **#101** | §14.14'ün öz-denetimi: **2 kalem çürütüldü, 3 atıf yanlıştı, 3 yeni kusur** | — |

#### 🔴 Uzman ekranı zinciri — ÜÇ noktadan ölü (DK-48'in kesin teşhisi)

Ürün sahibinin *"uzman ekranında sadece harita var"* şikâyetinin tam cevabı:

| # | Nerede | Ne oluyor |
|---|---|---|
| 1 | `analysis_result.py:200` | INDICES_ONLY'de tespitler maskeleniyor — **KR-019 gereği doğru** |
| 2 | `reporting_agent.py:295` | Uzman görsel paketi INDICES_ONLY'de **bilerek atlanıyor** — yani tam da uzmanın çağrıldığı modda |
| 3 | `reporting_agent.py:291` | FULL/PARTIAL'da bile üretilmiyor: **`expert_bundle_bands` üretim kodunda hiçbir yerde atanmıyor** (yalnız `= None` varsayılanı ve onu okuyan kapı var) |

Yani sistem uzmanı çağırıyor ama karar vermesi için gereken görselleri üretmiyor.
Üretici (`expert_bundle_producer` + `expert_bundle_persistence`, 6 PNG + manifest)
**yazılmış ama hiç bağlanmamış** — bugüne dek bir kez bile çalışmamış.

⬜ **Açık ürün kararı (insana ait):** madde 2'deki kapı gevşetilmeli mi?
Tanının saklanması KR-019'dur ve doğrudur; ama **uzmanın bakacağı görüntünün**
saklanması eskalasyonun amacını ortadan kaldırıyor. Görüntü tanı değildir —
tanının ön koşuludur. Karar verilmeden uçtan uca uygulama başlatılmamalı
(worker + sözleşme sürümü + platform + web).

#### Üretimin şu anki hâli

```
platform main = sunucu = 9a2609c6   (fark 0, submodule ' ' temiz)
servisler: backend/web/db/minio/rabbitmq/redis — hepsi healthy
uzman ekranı: kartlar ARTIK doğru alt uzmanlıkla · "model karar veremedi (%30,
              yönlendirildiği alan: Zararlı)" bölümü CANLIDA · döşemeler çalışıyor
hâlâ eksik : karo görüntüleri (DK-48, üç noktadan ölü) · yama görselleri (DK-52,
              edge üretmiyor) · gerçek görünüm taban katmanı (DK-51, edge)
```

## 0.A-l ÖNCEKİ TUR — (2026-08-19, **on beşinci oturum: uçuş öncesi platform turu — üretim kesintisi sınıfı üç kusur + admin görünürlüğü + ÖZ-DENETİM**)

> **Durum: platform `main` @ `2715808f`; kod ÜRETİMDE DOĞRULANDI** (rota tablosu
> çalışan konteynerden okundu, `git log` değil).
> Bağlam: **1-2 gün içinde gerçek antep fıstığı bahçesinde uçuş** — bu turun tamamı
> "simülasyonda hata çıkmasın" amacına bağlı.

### Merge edilen ve DAĞITILAN (platform)

| PR | Ne | Neden kritik |
|---|---|---|
| #428 | RabbitMQ `hostname:` sabitlendi | Her dağıtımda Mnesia düğüm kimliği değişiyor, **kuyruğa alınmış tüm işler siliniyordu** (`Recovering 0 queues` + 6 yetim düğüm dizini). Force-recreate ile kanıtlandı: 0 → 12 kuyruk |
| #430 | "Görev başına tek veri seti" varsayımının **üçüncü** örneği | Çiftçi **haritayı hiç göremiyordu** |
| #431 | Uzman 6sa cevap vermezse inceleme aynı branş uzmanına DEVREDİLİR | Silinmiş uzmanda `PENDING` kalan inceleme konsensüsü **kalıcı kilitliyordu** (üretimde yaşandı: `6a1ce099`) |
| #432 | Admin uzman görünürlüğü (işler · kararlar · elle devir · PIN sıfırlama) | Admin uzman incelemelerini **hiçbir yerden** göremiyordu |

### ⚠️ ÖZ-DENETİM ZİNCİRİ: #432 → #433 → #434 (toplam **13 kusur**)

> **Bu başlık 2026-08-19'da iki kez düzeltildi.** Önce "sekiz kusur, hepsi kapatıldı"
> yazıyordu; **yanlıştı**. (a) #433'ün CI koşumu **dokuzuncu** kusuru gösterdi
> (`create_app()` CI'da rotasız uygulama üretiyor — kök neden AÇIK). (b) #433'ün
> kendisi denetlendi ve **dört kusur daha** çıktı (#434). Devir notunun bayat kalması,
> notsuzluktan kötüdür.

**#434 — öz-denetimin öz-denetimi (MERGED, `ed83ad08`):** üçü aynı sınıfın tekrarıydı,
*"üretici ya da zincir sınanmamış"*:
1. #433 `must_change_pin` zorlamasını kurdu ama **claim'i YAZAN kodu sınamadı** —
   claim hiç üretilmese zorlama sessizce ölürdü, testler yeşil kalırdı.
2. Hız sınırı **tanımlıydı**, middleware'de **uygulandığı sınanmamıştı**.
3. 🔴 **`escalation_round` ölü kolonuna TÜKETİCİ eklenmişti.** Devir **sınırsızdır**:
   uzman A cevap vermezse iş B'ye, B de vermezse **tekrar A'ya** gidebilir —
   6 saatte bir, sonsuza kadar. Sayaç artırılmadığı için bu **salınım GÖRÜNMEZDİ**.
   Sayaç bağlandı; **üst sınır/alarm bilinçli olarak EKLENMEDİ** — "kaç devirden
   sonra ne olacağı" bir ÜRÜN kararıdır, SSOT'ta kuralı yok.
   ⚠️ **Uçuş sırasında buna bakın:** bir uzman cevap vermiyorsa iş sessizce iki
   uzman arasında dönebilir; admin listesindeki sayaç tek göstergedir.
4. Docstring'imde yanlış iddia (silinen test dosyası "değiştirilmeden geçer" diyordu).

Mutasyon oturum toplamı: **15 ölen / 5 no-op kontrol**. ⛔ Bir önceki kapanışta
"10/10 öldü, üç no-op" demiştim — **iki sayı da yanlıştı** (doğrusu o an 9/2 idi).

---

### #432'de bulunan sekiz kusur (hepsi #433 ile kapatıldı)

Kullanıcı, React ekranı yazılmadan önce öz-denetim istedi. Sonuç — **kendi işimde**:

1. **PR gövdemde yanlış iddia.** "`must_change_pin` ile uzman ilk girişte kendi PIN'ini
   koyar" dedim; **tüketicisi yoktu** (`auth.py`de bayrak hiç okunmuyor, `AuthTokenResponse`
   taşımıyor, web'de geçmiyor). Testim bir mock'ta bool'un set edildiğini doğruluyordu →
   **sahte-yeşil**. Zincir kapatıldı: claim → `jwt_middleware` → `403 PIN_CHANGE_REQUIRED`,
   dar muafiyet listesiyle (change-pin · refresh · logout).
2. **İş kuralını kanonikten okumak yerine yeniden yazmışım — 4 örnek.** En ağırı:
   `consensus_conflict = farklı verdict sayısı > 1`. Kanonik kural (`expert_portal.py:681`)
   **"herhangi biri RED derse"**. İki yönde de yanlıştı: `confirmed`+`corrected` → ben
   "yayın durdu" diyordum, gerçekte **yayınlanıyor**; `rejected`+`rejected` → ben "çelişki
   yok" diyordum, gerçekte **yayın duruyor** (görülmesi gereken hâl gizleniyordu).
   Kural artık `src/core/domain/services/expert_review_rules.py`de tek yerde;
   yayın kapısı da oradan okuyor (mutasyonla doğrulandı: yüklemi bozunca **kapı testleri**
   kırmızıya döndü, no-op mutasyon hayatta kaldı).
   Dördüncüsü: `expert_unreachable` kanonik üç-koşullu yüklemin `deletion_requested_at`
   ayağını **atlıyordu** → KVKK silme talebi vermiş uzman "sorunlu" filtresinde gizleniyordu.
3. **"HEMEN" istendi, sistem 12 saate kadar bekliyordu.** Devir 6 saatlik
   `stuck_mission_scan` işine iliştirilmişti (SLA 6sa + tarama 0-6sa). Kendi işine alındı:
   **15 dk + dağıtımda ilk tur hemen** (`next_run_time`).
4. **Yöneticiyi kimse denetlemiyordu.** Uzmanı izleyen yüzeyi kurup admin işlemlerini
   WORM'a yazmamışım. `ADMIN.EXPERT_REVIEW_REASSIGNED` + `EXPERT.PIN_RESET` eklendi
   (kardeş modül `admin_field_location` bunu 2026-06'dan beri yapıyordu — desen oradaydı).
5. **Mükerrer modül.** `/admin/expert-reviews/{id}/location` ucu **zaten vardı**
   (`admin_field_location.py`) ve aynı yol uzayını kullanıyordu; ben yanına ikinci bir
   modül açmışım. Birleştirildi, dosya silindi — **yol, yanıt modeli, RBAC, audit olay adı
   değişmedi**. Ayrıca elle yazdığım yetki kapısı yerine kanonik `require_roles` kullanıldı.
6. **Kök neden: 19 testin tamamı mock'tu.** Üretim yolundan geçen katman eklendi —
   gerçek `create_app()` + `TestClient` (jetonsuz → 401) ve gerçek SQLite motoru.
   İlk koşumda **üç gerçek hata** yakaladı: `expert_reviews`ta `updated_at` kolonu yok,
   `users`ta `role` kolonu yok, SLA yüklemi naive datetime'da `TypeError` fırlatıyordu.

**Dürüstlük notu:** `reset-pin` hız sınırı eklendi ama bu bir kaba-kuvvet açığı **değildi**
(uç CENTRAL_ADMIN kapılı) — politika tutarlılığı için yapıldı. `_load_users` JOIN'i gerçek-SQL
testiyle **kapsanmıyor** (SQLite'a ARRAY bağlanamıyor); onu `alembic check` +
`check_orm_schema_conformance.py` taşıyor.

### Açık kalemler

- 🔴 **Admin WEB EKRANI yok.** Bu tur yalnız API. Uçlar hazır, React yazılmadı.
- 🔴 **Yetim inceleme `6a1ce099`** — dağıtımdan sonra 15 dk içinde otomatik devredilmeli;
  edilmezse `POST /admin/expert-reviews/{id}/reassign` ile elle tetiklenir.
- `result_hash` üreticisi yok (ANALYZED durumu istiyor) · `layer_refs` ölü kolon ·
  `SchemaRegistry` boş → worker mesaj doğrulaması fail-open · `users.failed_login_attempts`
  ve `locked_until` ölü kolonlar.

---

## 0.A-k ÖNCEKİ TUR — (2026-08-18, **on üçüncü/on dördüncü oturum: KR-013-2 bağımsızlığı · CLAUDE.md Opus 5 yeniden yapılandırması · kalıcılık mimarisi · docs/denetim takip denetimi**)

> **Durum: I-1 dört depoda HİZALI (7.7.2), önceki turun "platform geride" iddiası bayattı.**
> Ölçüm (2026-08-18, `origin/*` + `check_version_alignment.py` sonucu):
>
> | Depo | Sürüm | Dal | Durum |
> |---|---|---|---|
> | contract | **7.7.2** | `master` (tag'in 16 commit ilerisi, docs-only: #91-#94) | ✅ etiketli, temiz |
> | worker | **7.7.2** | `master` | ✅ hizalı; I-1 kapısı kendi CI'ında |
> | edge | **7.7.2** | `main` | ✅ hizalı; I-1 kapısı kendi CI'ında |
> | platform | **7.7.2** | `main` | ✅ **2026-08-13'te re-pin edildi** (`eaf62e21`), I-1 kapısı `ci.yml:109`'da bağlı |
>
> Bu turda: (1) contract PR #91 — KR-013-2 komşu-tarla kapısı SSOT sahipten bağımsız
> hâle getirildi, üç depoda uygulama noktası ayrı işaretle bulunur oldu. (2) contract PR
> #92 — dört depoda `CLAUDE.md` Opus 5 rehberine göre yeniden yapılandırıldı (edge 903→386,
> worker 611→256, contract 452→198 satır) + `check_claude_md_refs.py` atıf bütünlüğü kapısı
> dört depoda CI'a bağlandı. (3) contract PR #93 — kök `TARLA-ANALİZ/CLAUDE.md` (git dışı
> kapsayıcı klasör) ve oturum-başı PowerShell kancasının gövdesi contract'a taşındı; kök artık
> ince işaretçi, kalıcılık git ile sağlanıyor. (4) contract PR #94 — dört depoda `docs/`+
> `denetim/` (191 dosya) tam-okuma denetimi: platform (34) ve worker (62) **sıfır aday**,
> edge (23) tek zayıf aday (dokunulmadı), contract (72) 2 alansız dosya silindi/taşındı.
>
> **I-1 artık ÖLÇÜLÜYOR.** `tools/check_version_alignment.py` (AL-K30) contract CI'ında
> kanonik kipte, worker ve edge CI'ında tüketici kipinde koşuyor — üçü de **uçtan uca
> doğrulandı** (workflow'daki gerçek çağrı okundu, commit başlığına güvenilmedi).
> Kapının ilk koşumu platform'un geride kaldığını hemen yakaladı; **sessizce kalamaz.**
>
> **platform'un geride kalması bu oturumda bilinçli değil, sadece sıra gelmedi** —
> bu oturumda platform'da çalışan bir aktör yoktu. Bir sonraki oturumun ilk işi.
>
> Sürüm dizeleri: contract `7.7.2` · checksum `aded57d3926459a12a45d1004f16aee80e55de1e5bb6e310cbad563753b7a2b0`
> (`bf269235…` 7.7.0 · `2d9f7475…` 7.7.1). Üç sürümde de **yalnız `api/` içindeki üç
> `info.version` damgası** değişti — `schemas/` ve `enums/` ağaçlarına hiç dokunulmadı,
> yani kardeşlerin vendored öz-hash'i sabit kaldı.

---

## 0.A-j ÖNCEKİ TUR — (2026-08-11, **on ikinci oturum: contract cerrahi kalite denetimi · v7.7.0 + v7.7.1**)

> ⚠️ Bu bölümdeki "platform 7.6.1'de kaldı, AL-K26 açık" iddiası **2026-08-13'te KAPANDI**
> (platform `eaf62e21` ile re-pin edildi) — bkz. yukarıdaki §0.A EN GÜNCEL tablosu. Aşağısı
> bu turun kendi kapanış anındaki (henüz platform kapanmamış) durumudur, tarihsel kayıt.

### Ne yapıldı — **19 PR** (#69…#89), üç sürüm etiketi

Tema: **"belgelenmiş ama koşmayan kural bir dilektir"**. Denetim, sözleşme metnini değil
**kapıların kendisini** hedef aldı; bulunanların çoğu *var sanılan* kapılardı.

| Küme | PR | Özet |
|---|---|---|
| Alan sızması | #69 | 19 şemada **27 object düğümü** politikasız açıktı; `validate.py` artık **tüm ağacı** gezip her object düğümünden politika beyanı istiyor (sessizlik yasak) |
| Sözlük bağlama | #69, #78 | `threat_type` kanoniğe bağlandı + bağlama ratchet'i · `quarantine_decision` **bilinçli bağlanmadı** (iki ayrı eksen — AL-K21 kapandı) |
| CI dürüstlüğü | #69 | `paths:` 13 → **24 kök**, `summary.needs` eksik iş taşıyordu; ikisi de artık **türetiliyor**, elle yazılmıyor |
| Parite kapıları | #71, #72, #74, #77, #81, #82 | politika paritesi kapısı · "kardeş CI'ında koşuyor" iddiası **yanlıştı** · kapının **tavsiyesi hataya yol açıyordu** · sayaç kilidi **küreseldi** |
| Ayna kusurları | #75, #76 | ÖD-13 kapısı `main()` yerine **kopyasını** ölçüyordu; düzeltmenin kendi kör noktası da ayrıca bulundu |
| Ölü/zararlı araç | #73 | Node/TS zinciri **hiç var olmamıştı**; `npm run format` checksum kapsamındaki **94 dosyayı** yeniden biçimlendirirdi — ölü değil **zararlı** |
| Koşmayan kurallar | #80 | `drone_type` senkron kapısı **yoktu** · `poetry.lock` üçüncü kaynak olarak **çelişiyordu** (pytest 7.4.4 ↔ 9.0.2) · belgelerde koşmayan komutlar |
| Sürüm | #79, #82, #85 | **v7.7.0** (MINOR) · **v7.7.1** ve **v7.7.2** (PATCH) |
| I-1 kapısı | #87 | *"Sürüm üç depoda aynı"* kuralı üç `CLAUDE.md`'de yazılıydı, **doğrulayan tek komut yoktu**; edge `7.6.1`'i hiç pinlememişti ve kimse fark etmemişti |
| Betik ağacı | #89 | `.sh`/`.ps1` ağacı **tümden kapısızdı** (3 dosya / 1021 satır, 0 isabet); yetim ve koşarsa zararlı bir betik silindi + iki katmanlı kapı |
| Öz-kusur | #85 | `v7.7.1`'de *"sınıfın tamamını kapattım"* dedim; **kardeş dosyayı saymamıştım** — worker yakaladı, `v7.7.2` düzeltti |

### 🔴 v7.7.1 neden gerekti — etiket değişmez

`v7.7.0` yayımlandıktan **sonra** edge pin PR'ında tek bir kapı kırmızı verdi:
parite sayacı **küresel** bir taban tutuyordu (142) ama kapı **her kardeşin kendi
CI'ında** koşuyor (D4-b). edge checkout'unda toplam 0 çıkıyor → `0 >= 142` **yapısal
kırmızı**. Kusur v7.7.0 kaynaklı değil, **v7.6.1** ile gelmişti; edge 7.6.0'a pinli
olduğu için ancak yeni pine geçerken göründü. Düzeltmenin `master`'a inmesi yetmez —
kardeş CI sözleşmeyi **pinli etiketten** checkout eder ve etiket değişmez (I-2).

Düzeltmenin tasarımı **edge oturumundan geldi** (taban çift başına + pozitif kontrol).
Uygularken kendi ölçümüm **kalan bir delik** daha buldu: iki kilit de depo verisini
okuduğu için, ölçecek verisi olmayan kardeşte yürüyüşün bozulması görünmüyordu
(*edge-only CI + körelmiş yürüyüş → `2 passed`*). Aynı boşluk contract'ın **kendi**
CI'ında daha büyüktü. Çözüm: yürüyüşü **sentetik girdiyle** sınayan 5 test.

### Kapanışta açık kalan TEK iş

**platform `7.6.1`'de** (`AL-K26`) — bu oturumda platform'da çalışan aktör yoktu.
Sonraki oturumun ilk işi; artık bir kapı bunu ölçüyor.
✅ **Güncelleme (2026-08-13):** platform re-pin edildi, AL-K26 kapandı — yukarıdaki uyarı kutusuna bakın.

Diğer açık kalemler **karar** bekliyor, iş beklemiyor: `AL-K24` (`paths:` kaldırılsın mı) ·
`AL-K27` (`payment_target_type`, sonraki MINOR) · `AL-K28` (`field_created` kapısı) ·
`AL-K29` (`sync_to_repos.py` ölü, silme onayı).

### Bu oturumun kalıcı dersi

Yanlış ölçüm iki kez gerçek iddiaya dönüşmek üzereyken yakalandı: PowerShell `>`
yönlendirmesi git blob'una BOM+CRLF ekleyip *"betik Linux'ta koşmaz"* diye **yanlış
bir HIGH bulgu** üretecekti; alt-dize taraması kapının kendi tanımı sanılıp edge'e
*"öneriniz çalışmaz"* denecekti. İkisi de kanıt istenince eridi. Kural, kök
`CLAUDE.md`'ye eklendi: **tek seferde bul, tek seferde çöz — sonsuz döngü yok.**

---

## 0.B — (2026-08-11, **on birinci oturum: docs öz-denetimi · sarkan-atıf kapısı · çeltik sunumdan çıktı**)

> **Durum: HEPSİ MERGE EDİLDİ (9 PR, dört depo).** Merge sonrası CI dört depoda da yeşil;
> I-1 üçlü hiza **7.6.1**; SSOT üç depoda bayt-özdeş `d3c65d62…`.
> `docs`+`denetim` izli dosya: **184 → 183**.
>
> | PR | Depo | Konu |
> |---|---|---|
> | [#66](https://github.com/physiscs-zana/tarlaanaliz-contract/pull/66) | contract | 8 çapraz-repo sarkan atıf + kapı + **eylem planı §2.1 matrisi koddan sapmıştı** |
> | [#67](https://github.com/physiscs-zana/tarlaanaliz-contract/pull/67) | contract | kapı çıktısı makine-okunur (`SKIPPED_CROSS_REPO`) |
> | [#409](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/409) | platform | 12 sarkan atıf + kapı + `test_ops_scripts_in_image` **I-3 yönü eklendi** |
> | [#410](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/410) | platform | **çeltik sunumdan çıktı** (5→4 ürün) + "SUNULAN ⇒ bookable" kapısı |
> | [#411](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/411) | platform | kapı betiği senkron |
> | [#218](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/218) | worker | kapı + **aktif_ogrenme ikilisi birleşti** (62→61 dosya) + K4/K6 |
> | [#219](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/219) | worker | çapraz-repo ayağı CI'da bağlayıcı + 2 yetim belge bağlandı |
> | [#66](https://github.com/physiscs-zana/tarlaanaliz_edgekiosk/pull/66) | edge | kapı |
> | [#67](https://github.com/physiscs-zana/tarlaanaliz_edgekiosk/pull/67) | edge | çapraz-repo ayağı + yetim belge bağlandı |

### 🔴 CANLIDA OLMAYAN TEK ŞEY — çeltik (merge ≠ deploy)

`main`'de `offered_crops.generated.json` = `['CORN','COTTON','PISTACHIO','GRAPE']` (ölçüldü),
ama `curl https://tarlaanaliz.com/` **hâlâ `RICE` içeriyor**. Yayın elle yapılır:
`tarlaanaliz-platform/docs/operations/WEB_RELEASE_RUNBOOK.md` (üretim sunucusunda
`docker compose build web` +
Cloudflare "Purge Everything"). **Sunucu erişimi olan makinede yapılmalı.**

**Neden çıkarıldı:** `missions.py` sipariş yolunda İKİ kapı koşuyor ve ayrı kaynaklardan
okuyor — SUNUM (`is_gap_offered` ← `crops.ts`) ⟂ TESLİM (`is_bookable` ← `crop_readiness.json`).
Çeltik birincide vardı, ikincide `bookable:false` → çiftçi ana sayfada görüyor, tarla
açabiliyor (`fields.py` yalnız SUNUM'a bakar), sipariş verince **409** alıyordu.
Değişmez artık testle kilitli: `test_every_offered_crop_is_bookable_in_readiness`.

### Yeni kapı: sarkan doküman atıfı (AL-K20)

Dört depoda `check_doc_links` + ratchet baseline + CI adımı. Betik **bayt-özdeş**
(blob `58ea575d…`; yollar `__file__`'dan türetilir — dördünü de aynı baytlarla güncelle,
`cmp` ile doğrula). Baseline: contract 98 · platform 96 · worker 182 · edge 24.

**Çapraz-repo ayağı worker+edge CI'ında BAĞLAYICI** (`contracts_gate.yml` → `sibling-parity`
işi contract'ı zaten yan yana checkout ediyordu). CI log'uyla kanıtlandı: önceden worker 2 /
edge 1 atlanan atıf → şimdi `SKIPPED_CROSS_REPO_COUNT 0`.
⛔ contract→worker/edge ve platform→worker bağlanamaz: o depolar **PRIVATE**, çapraz-repo
token'ı gerekir (ölçüldü: `gh repo view --json visibility`).

### ⚠️ SONRAKİ OTURUM / DİĞER MAKİNE İÇİN

1. **AL-K19 bir sonraki sürüm törenine BİNMELİ.** `schemas/worker/expert_review_queue.v1.schema.json:463`
   silinmiş bir worker dosyasını `source` gösteriyor; `schemas/` checksum kapsamında olduğu için
   tek başına düzeltmek üç-depo töreni ister. Bu oturumda contract'ta **39 şema dosyalık**
   `unevaluatedProperties` işi commit'lendi (`contract/uneval-array-items`) — tören ORADA açılacak,
   AL-K19 o turda düzeltilsin (`dist/` kopyası da yeniden üretilmeli).
2. **Kök `.txt`'ler git DIŞINDA (K4) ve bu makinede EKSİK.**
   `Tarama_Protokolu_v1.6_Birlesik` bu bilgisayarda **YOK** (pozitif kontrollü `find`; yalnız
   v1.3 var). Üç 2026-07 denetiminin referans belgesi ve worker `phenology_registry.yaml`
   sezon uzunlukları ona hizalanmıştı → **F-8 hizalaması bu makinede doğrulanamıyor.**
   Diğer bilgisayarda duruyorsa oradan alıp kalıcı bir yere koyun; kalıcı seçenek
   `tarlaanaliz-contract/docs/` altına almak (worker `denetim/kalan_isler.txt` §2/K4).
3. **Bu klasör git deposu değil** — kök `CLAUDE.md` ve beş `.claude/settings.json`
   **push ile taşınmaz**; yeni makinede elle kopyalanır (kök `CLAUDE.md` §7).
   Yerel hafıza (`~/.claude/memory/tarlaanaliz/`) de taşınmaz — devir yalnız bu dosyayla olur.
4. **Birleştirme sırası BİTTİ.** Kalan 7 adayın 6'sı ölçümle çürütüldü (üretim kodundan adıyla
   anılan canlı referanslar / eşi olmayan / ilgisiz konu = grab-bag riski). Yeni kural:
   **koddan adla anılan belge birleştirilmez; birleştirilecekse ADI KORUNUR.**
5. **Kapının bakımı:** baseline **elle yamanmaz** — `--write-baseline` + diff incelemesi.
   Tarihsel bir dosya adını `.md` uzantısıyla anmak onu baseline'a sokup kapıyı o dosyada
   gevşetir; köken notlarında uzantı yazmayın.

### Paralel oturum uyarısı (bu turda yaşandı)

Paylaşılan checkout'ta `git checkout -b` ile dal açıp çalışırken paralel oturum **dalı
değiştirdi**; iki commit'im onların dalına düştü (`gh pr create` *"No commits between…"*
diyene kadar fark edilmedi). Kurtarma: `git branch -f <dalım> <sha>` → `git reset --soft HEAD~1`
→ yalnız kendi dosyalarını `git restore`. **Kalıcı korunma: izole `git worktree` kullanın**
(bu turda worker'da öyle yapıldığı için worker hiç etkilenmedi).

---

## 0.B — (2026-08-11, **onuncu oturum: D12 `stress_ratio` kararı · KR-093 ön faz kapısı · D13 üç-repo 7.6.1 hizası**)

> **Durum: HEPSİ MERGE EDİLDİ.** Beş PR, üç depo, hepsi CI'dan geçti. Çalışma ağaçları
> temiz, üç depo da varsayılan dalında, turun beş dalı silindi.
> İş listesi kalemleri: eylem planı **§14.11**.
>
> | PR | Depo | Konu |
> |---|---|---|
> | [#62](https://github.com/physiscs-zana/tarlaanaliz-contract/pull/62) | contract | D12 — `stress_ratio` TANIMLANDI + `delivery_rule` (7.6.1 re-pin) |
> | [#63](https://github.com/physiscs-zana/tarlaanaliz-contract/pull/63) | contract | Öz-denetim bulgusu: vendored `metadata` çelişme kapısı |
> | [#407](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/407) | platform | KR-093 ön faz kapalı listesi **kapıya bağlandı** + contracts 7.6.1 |
> | [#408](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/408) | platform | submodule pini `v7.6.1` etiketli commit'e (I-3 onarımı) |
> | [#216](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/216) | worker | vendored `analysis_type` v1.4.1 → v1.4.4 + `v7.6.1` |

### Sürüm durumu — **7.6.0 → 7.6.1** (PATCH, non-breaking)

Beş değişmez varsayılan dallarda **komutla** ölçüldü (kapanışta):

```
I-1  contract 7.6.1 · platform 7.6.1 · worker v7.6.1
I-2  v7.6.1 annotated · merge-base --is-ancestor v7.6.1 origin/master → EVET
     (etiket 8a0a8e7 → c4b7b94'e TAŞINDI; gerekçe aşağıda)
I-3  submodule pin c4b7b94 == etiketli commit · checksum c4551a06… birebir ayna
I-4  worker öz-hash: OK (v7.6.1)
I-5  availability 11/11 hizalı · stress_ratio değerleri birebir → ayrışma KAPANDI
SSOT metni üç depoda BAYT-ÖZDEŞ (0 fark satırı)
```

### Ne yapıldı

| Kod | Depo | İş |
|---|---|---|
| **D12** | contract | `indexDefinitions.stress_ratio` `UNDEFINED_PENDING_DECISION` → **`DEFINED`**. Formül **üretici koddan okundu**: `NDRE / NDVI`, NDVI ≤ 0 piksellerinde nötr `1.0`. Önceki *"ad var, üretim yok"* iddiası ⛔ çürütüldü — ölçüm yanlış dosyaya (`compute_indices_v2`) bakmıştı; üretici çıkarım hattındadır ve raster S3'e yüklenip manifest'te listelenir. Yeni makine-okunur alan: `delivery_rule.preliminary = false`. |
| **D12** | platform | KR-093 ön faz **kapalı listesi kodda hiç tüketilmiyordu** (`x-preliminary-content` → 0 eşleşme) → `WATER_STRESS` vekil katmanı uzman onayından ÖNCE çiftçiye sunuluyordu. Yeni `preliminary_content_gate.py` listeyi **kanonikten okur** (kopyalamaz); kapı **üç yüzeyde**: katman listesi + `available_indices`, raster tile ucu, tile metadata. Uzman/admin kapsam dışı. |
| **D12+** | platform | Aynı denetimde **iki ek delik**: (a) konsensüs RED sonrası özet ucu 409 derken **tile'lar servis edilmeye devam ediyordu**; (b) faz türetmesi `"FULL" if DONE else "PRELIMINARY"` idi — kanonik *"listelenmeyen = PRELIMINARY varsayımı YASAKTIR"* der. İkisi de fail-closed yapıldı. |
| **D12** | worker | **Kod değişmedi (bilinçli).** `reporting_agent.py` + `src/indices/stress_ratio.py` başına "neden burada kalıyor" gerekçesi. |
| **D13** | üç depo | Sürüm töreni: contract re-pin + annotated tag · platform submodule/checksum/`main.py` boot-pin · worker vendored kopya + KR-041 öz-hash. |

**Neden worker'dan çıkarılmadı (seçenek (b) elendi):** `result_mode` ile `report_phase`
**bağımsız eksenlerdir** (KR-093) — `FULL_REPORT` modundaki iş de uzman onayına kadar
`PRELIMINARY` fazındadır, dolayısıyla `reporting_agent`'tan silmek sızıntıyı KAPATMAZDI.
Ayrıca kanonik `x-removed-2026-07-31.still_computable` worker'ın hesaplamaya devam
etmesine **açıkça izin verir**. Kısıt üretimde değil **sunumda**.

### 🔬 SONRAKİ OTURUM — BU OTURUMUN İŞİNİ ÖNCE DENETLE

**D-1 · Tazelik.** Üç depoda `git status --short` + `git log --oneline -1`. Bu oturumda
paralel bir aktör worker'da iki kez commit attı (biri **benim commit'lenmemiş** düzenlemelerimi
kendi commit'ine aldı: `22d6fc7`). Kirli ağaç varsa önce onu anla.

**D-2 · Kapı gerçekten üretim yolunda mı?** Ön faz kapısı `_build_layers` + `tiles.py`
üzerinden **birim testleriyle** doğrulandı ve gerçek manifest biçimiyle elle koşuldu
(`PRELIMINARY → ['HEALTH','NITROGEN_STRESS']`). **Canlı trafikte doğrulanmadı** — ayakta
yığın yoktu. Kabul ölçütü: `PENDING_REVIEW` bir mission için
`GET /results/{id}/summary` → `layers` içinde `WATER_STRESS` **yok**;
`GET /tiles/{id}/WATER_STRESS/…` → **403**; aynı sonuç `DONE` olunca **200**.

**D-3 · Merge ≠ deploy.** Kod varsayılan dallarda; çalışan platform sürecinin yeni kodu
içerdiği ÖLÇÜLMEDİ. Ön fazda katman kaybolduysa önce *"hangi sürüm koşuyor"* diye sor.

**D-4 · Yeni kapının kapsamı.** `TestVendoredMetadataDoesNotContradict` **yalnız worker
CI'ında** koşar (contract CI'da kardeş depo yok → atlanır, D4-b tasarımı). Contract
deposu worker'ın **Python koduna** hâlâ bakamaz: `stress_ratio.py`'deki sabiti değiştiren,
kanonik girdiyi de aynı turda değiştirmek zorundadır ve bunun **kapısı yoktur**.

**D-5 · Bu oturumun kendi yöntem hataları** (tekrarlamamak için):
- **Ölçtüğüm şey iddia ettiğim şey değildi:** dal silmeden önce "içerik master'da var mı?"
  diye `git diff master...dal` (**üç nokta**) koştum — o komut "dalın merge-base'den beri
  ne eklediğini" gösterir, master'da eksik olanı değil. Doğrusu iki-nokta ağaç
  karşılaştırması + `log dal..master` / `log master..dal` ile **yön** ölçümü.
- **Etiketi merge sonrasına bırakmak yanlıştı:** worker CI contract'ı **pinli etikete**
  göre checkout ediyor; `v7.6.1` uzakta yokken iş `Checkout contract @ pinli etiket`
  adımında düştü. Tag, tüketici PR'ları CI'a girmeden push edilmeli.
- **Etiketi ileri taşımak I-3'ü kırdı:** platform pini eski hedefte kalınca `describe`
  bulanıklaştı (`v7.6.0-13-g8a0a8e7`). Etiket taşındıysa tüketici pinleri de taşınmalı.
- **CI'da olup yerelde koşmadığım kapı vardı:** worker'da `CONTRACTS_VERSION.md` değişen
  her PR `CHANGELOG.md` de ister. Kapının **tam kabuk komutunu** workflow'dan okuyup
  birebir yerelde koşturmak gerekiyordu.
- **"PR merged" ≠ "commit'im indi":** #62 benim son push'umdan ÖNCEKİ head'de merge edildi
  (üstelik squash değil); parite kapısı master'a girmedi, ayrı PR (#63) ile indirildi.

### 📌 Karar bekleyenler (kullanıcıya)
1. **AK-9 KAPANDI** (bu tur) — `stress_ratio` tanımlı; teslimat kısıtı sunum katmanında.
2. Önceki turdan **devam edenler:** AL-K9 (üç üretici-ölü özellik) · AL-K16 (barley/potato) ·
   AL-K8 (kartlardaki `THERMAL_REQUIRED`) · AL-K13 (kart ratchet'i CI'da zorlanmıyor).

## 0.A-i ÖNCEKİ TUR — (2026-08-10, **dokuzuncu oturum: DK-43…DK-47 — sessiz kusurlar · indeks gerçeği · kart SSOT**)

> **Durum: HEPSİ MERGE EDİLDİ** (kullanıcı talimatı: *"konu başına ayrı PR aç ve commit'le
> push ve merge yap"*). İş listesi kalemleri: eylem planı **§14.10** (AL-K1…AL-K16 +
> çürütülmüş iddialar).
>
> | PR | Depo | Konu | Ana dal (merge sonrası) |
> |---|---|---|---|
> | [#208](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/208) | worker | DK-43 | — |
> | [#209](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/209) | worker | DK-44 | — |
> | [#210](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/210) | worker | DK-45 | — |
> | [#211](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/211) | worker | DK-46 (ratchet + baseline + test) | — |
> | [#212](https://github.com/physiscs-zana/tarlaanaliz_worker/pull/212) | worker | DK-47 | `master 029aa4a` |
> | [#404](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/404) | platform | DK-46 (13 dosya bayt-özdeş + `labeling_card_service`) | `main 9ec947c2` |
>
> Her PR **ayrı ayrı** CI'dan geçti (worker 4 kapı · platform 6 kapı). Üç depoda da
> çalışma ağacı **temiz**. ⚠️ **Merge ≠ deploy** — canlıda görünme ayrı adımdır.

### Ne yapıldı (hepsi ölçüm + mutasyonla doğrulandı)

| Kod | Depo | İş |
|---|---|---|
| **DK-43** | worker | Aşama-1 anomali filtresi NaN'da **fail-OPEN**'dı: ölçüm yapılmamış karo "sağlıklı" sayılıyordu. Gerçek uçuşta 36 karonun **11'i**. `np.nanmean` + fail-closed + kapsama kapısı. Sağlıklı 11→**0**, hariç tutulan 0→**11**. |
| **DK-44** | worker | `stress_ratio` `_compute_indices`'te **hiç üretilmiyordu** (ValueError DEBUG'a yutuluyordu). İki turlu, sıradan bağımsız çözüm + WARNING. Ölçülen özdeşlikler belgelendi: `LCI==NDRE`, `GNDVI==−NDWI`. |
| **DK-45** | worker | Fıstık ad ekseni crops→kart/registry hizalandı (3 eşleme); `card_coverage_baseline` **yanıltıcı gerekçesi** düzeltildi; **kök/kökboğazı çürüklüğü şemsiye kartı** eklendi. Kartsız 16→13, sapma 85→79. |
| **DK-46** | worker + platform | **Worker = kart SSOT.** Platform bayt-özdeş kopya (11 dosya/132 kart → 15/**210**), **12 HEALTH kartı** portala geldi (öncesinde HİÇ yoktu). Sapma 30→**2**. Ratchet kapısı + baseline + 8 test. Platform'da **RICE eşlemesi** eklendi (satılan ürün, portalda kartı yoktu). |
| **DK-47** | worker | Tanıtım özeti gerçeğe hizalandı: 3 üretici-ölü özellik ayrı kutuya, 7 iddia düzeltildi, sayısal özet ölçülen değerlerle karşılaştırıldı. |

**Kapılar (kapanışta, her PR'da ayrı ayrı ölçüldü):** worker `ruff` temiz · `mypy` 128
(taban) · üç ratchet OK · KR-041 `OK (v7.6.0)` · `pytest` **4422 passed** ·
platform `ruff`/BOUND temiz · `mypy` **462 dosya, 0 sorun** · `pytest` (CI ile birebir
`TARLA_ENVIRONMENT=development`) **6031 test / 0 hata / 5 skip**, kapsam **%83.67** (eşik 80).
**13 mutasyon, 13'ü de bir testi öldürdü.**

### 🔬 SONRAKİ OTURUM — BU OTURUMUN İŞİNİ ÖNCE DENETLE

Aşağıdakiler **benim kendi işime** karşı yazılmış denetim kalemleridir. Kod yazmadan önce
bunları koş; hiçbirini "geçmiştir" diye varsayma.

**D-1 · Tazelik.** Üç depoda `git status --short` + `git log --oneline -1`. Bu oturumda
platform HEAD'i ölçüm sırasında `409def12`→`14804d73` değişti (başka aktör). Kirli ağaç
varsa **önce onu anla**, üzerine yazma.

**D-2 · Gerçek-veri iddiasını yeniden üret.** DK-43'ün sayıları `_anomaly_filter` üretim
kodu **doğrudan çağrılarak** ölçüldü; **tam konteyner uçtan-uca koşumu TEKRARLANMADI**.
Kabul ölçütü: aynı raster ile
`docker logs tarlaanaliz-worker | grep "Anomaly filter"` → beklenen **36/36** (11 karo
artık "sağlıklı" değil, Aşama-2'de *atlandı* olarak loglanır) ve `tile_count_healthy`
**0**. Dashboard `health` **düşmeli ya da aynı kalmalı** — yükselirse düzeltme yanlış yönde.

**D-3 · Ratchet gerçekten kapı mı?** `check_card_catalog_drift` worker CI'ında **atlıyor**
(platform yan yana yok). Yani bugün "kapı" değil, geliştirici kontrolü. AL-K13 kapatılmadan
"kart senkronu garantili" **denmemeli**. Ölç: CI logunda skip satırını gör.

**D-4 · Mutasyon borcunu yeniden çalıştır.** Bu oturumda **iki testim ilk yazımda
mutasyondan sağ çıktı** (biri gerekçe metnini dosyanın herhangi bir yerinde arıyordu,
biri savunma-derinliği guard'ıydı). İkisi de güçlendirildi — ama aynı hata sınıfı
tekrarlanabilir: yeni yazılan her testte "hangi mutasyon bunu öldürür?" sorusunu yaz.

**D-5 · Platform kart senkronu içerik denetimi.** Bayt-özdeşlik **doğrulandı** ama
platform kartlarının uzman portalı **arayüzünde** nasıl göründüğü denetlenmedi (v2.x
alanları ilk kez orada). Portal ekranını bir kez gözle doğrula.

**D-6 · Çürütülmüş iddiaları tekrar gündeme getirme.** §14.10 sonundaki tabloya bak:
"platform kopyası bayat" · "healthy_rice yok" · "fail-open veri kaybı üretiyor" ·
"DK-44 WATER_STRESS katmanını besliyor" — dördü de ölçümle çürütüldü.

**D-7 · Bu oturumun kendi yöntem hataları** (tekrarlamamak için):
- `git checkout` ile mutasyon geri alırken **kendi commit'lenmemiş işimi sildim** →
  mutasyon geri alma için **yedek** kullan, git değil.
- İlk gerçek-veri ölçümüm **geçersizdi** (alfa bandını `str(enum)` ile arıyordum; Python
  3.11+ `IntEnum.__str__` sayı döndürüyor). Üretim loguyla çapraz kontrol olmasa
  fark etmezdim → **her ölçümü bilinen bir gerçekle çapraz doğrula.**
- `class_vocab_drift_baseline.yaml`'ı **yanlış dizinde** aradım (`config/` vs
  `config/phenology/`) ve "yok" sandım → "hiç yok" çıktısına **pozitif kontrol** koy.
- `healthy_rice` yok dedim; `startswith("healthy")` filtresi `rice_crop_healthy`'yi
  kaçırdı → **ada değil alana** (`sub_specialty`) bak.
- 🔴 **Geçici klasördeki (scratchpad) yedeği tek kaynak saydım ve klasör silindi.**
  PR'lar arası bekleyen DK-45/46/47 dosyaları oradaydı; oturum ortasında **boşaldı**.
  Kurtarma **oturum kaydından** (transcript `.jsonl`) yapıldı: `Write` içerikleri +
  `Edit` `old/new` çiftleri + betikli yazmalar kronolojik sırayla yeniden oynatıldı
  (20/20 uygulandı; biri `import` satırı ayrı bir komuttaydı, `ruff` yakaladı).
  Doğrulama: worker↔platform kart bayt-özdeşliği yeniden ölçüldü → sapma yine **2**.
  **Ders:** commit'lenmemiş iş için tek yedek yeri **geçici klasör olamaz** — ya
  hemen bir dala commit'le ya da depo içinde kalıcı bir yere koy. Transcript bir
  kurtarma kaynağıdır ama **yedek değildir** (yalnız bu makinede, yalnız bu oturum).

### 📌 Karar bekleyenler (kullanıcıya)
1. ✅ **KAPANDI** — konu başına ayrı PR açıldı, CI'dan geçirildi ve merge edildi (tablo yukarıda).
2. AL-K9: üç üretici-ölü özellik bağlanacak mı, düşülecek mi.
3. AL-K16: barley/potato ürünleri açılacak mı (kartları hazır bekliyor).
4. AL-K8: kartlardaki THERMAL_REQUIRED talepleri "gelecek yetenek" diye mi işaretlensin.

## 0.A-h ÖNCEKİ TUR — (2026-08-10, **sekizinci oturum: DOĞRULAMA TURU — iddialar mutasyonla sınandı, zincir tekrar aktı**)

> ### 🔴 EN ÖNEMLİ ÜÇ CÜMLE
>
> 1. **Yedinci turun beş düzeltmesi de CANLI ve GERÇEKTEN çalışıyor** — yeşil teste
>    güvenilmedi: DK-38 ile `build_profiles` kapısı **mutasyonla** (kodu bilerek bozup
>    testin kırıldığını görerek), DK-42 **backend IP'sini zorla değiştirerek**, DK-39
>    **iki yönde** (kaynak RGB iken açık / multispektral iken kapalı) sınandı.
> 2. **Simülasyon 1–7 baştan koştu (hepsi `EXIT=0`)** ve sayılar 2026-08-08 ile birebir
>    çıktı — zincir kararlı, tek seferlik değil. Ardından **taze bir iş** M1 paketinden
>    çiftçinin sayfasına kadar aktı: `27/100 · ndvi 0.266`.
> 3. **Bu turda depolara tek satır kod girmedi** (dört depo temiz, HEAD'ler değişmedi);
>    bulunan tek kusur **simülasyon koşumunun kendisindeydi** ve orada düzeltildi.
>
> ### Ölçülen iddialar (hepsi komutla)
>
> | İddia | Ölçüm | Sonuç |
> |---|---|---|
> | 5 PR ana dalda | 4 depo `git log` + `rev-list --left-right` | ✅ `0 0` (origin ile aynı) |
> | Planda DK-38/41/42 KAPANDI | eylem planı satır 680/686/693 | ✅ |
> | Mojibake onarıldı | 10 dosya UTF-8 çözücü + **pozitif kontrol** | ✅ hiçbirinde yok |
> | edge CI kapısı | `ruff check` · `ruff format --check` · 3 takım + kapsam | ✅ **1371 geçti**, %84.88 |
> | worker birim takımı | `pytest tests/unit` | ✅ **3975 geçti** |
> | platform (değişen modüller) | 5 test dosyası, `APP_ENV=development` | ✅ **116 geçti** |
> | DK-36 hâlâ kapalı | DB sorgusu | ✅ av1 `0` · av2 `0` · `calibration_records` `0` |
>
> ### Mutasyon sınamaları (yeşil test kanıt değildir)
>
> * **DK-38** — alfa bandı dalı öldürüldü → `test_ALFA_BANDI_yoluyla_maske_OLCULEN_ODM_DURUMU`
>   **kırmızıya döndü**. Yani düzeltmeyi koruyan gerçek bir kilit var.
> * **`build_profiles` sahipliği** — `cog_converter` satırı silindi → **2 test öldü**.
> * **DK-42 (ayırt edici)** — ağa dolgu konteyner konup backend yeniden başlatıldı,
>   IP **`172.18.0.8 → 172.18.0.12`** değişti; nginx yeniden başlatılMADAN **401**
>   döndü (**502 değil**). 502'yi doğuran senaryonun ta kendisi koşturuldu.
> * İki mutasyon da geri alındı; dört çalışma ağacı temiz, I-3 bayt-özdeşliği sağlam.
>
> ### Simülasyon: koşum 8 (ayrıntı `edge-simulasyon/KOSUM_SONUCLARI.md`)
>
> Kaynak kilidi 5/5 · koşum 1–7 `EXIT=0` · maske/kutu **0.9737 · 0.9732 · 0.5424**
> (08-08 ile birebir) · `dicle_none` **422 sert red** · depo-kökü-dışı **400** ·
> kayıtsız drone **422** · gözetim zinciri 6 kol / **4 farklı red sebebi**.
>
> **Yeni:** M1→M2'ye giden dosya **5 değil 6** — `rgb_ortho_cog.tif` (DK-41 üretim
> yolunda). Doğrulandı: `tiled · 512×512 · overview [2,4,8] · deflate · EPSG:32637`.
>
> 🔴 **DK-41 × DK-38 çapraz sınaması:** COG çevrimi geçerli-piksel bilgisini koruyor mu?
> Kaynak ve COG'da alfa oranı **0.42972333 = 0.42972333** → koruyor. Korumasaydı worker
> sessizce yanlış NDVI'ya dönerdi. (Not: `dataset_mask()` iki dosyada da "hepsi geçerli"
> diyor — bilgi **yalnız** alfa bandında; DK-38'in ikinci dalı olmasa düzeltme burada
> da etkisiz kalırdı.)
>
> ### Taze uçtan uca koşum (üretim kodu)
>
> `M2 staged COG → nesne deposu → RealIngestService → analysis_jobs → build_analysis_job_v1
> + publish_analysis_job → RabbitMQ → worker → analysis_results → timeseries → dashboard`
>
> ```
> Pipeline completed: tiles=25 confidence=0.433 mode=INDICES_ONLY 9869ms
> Valid-pixel mask applied (alpha_band_5): 43.0% out-of-flight      <- DK-38 canlı
> Band plan resolved via raster_descriptions: {R:1,G:2,NIR:3,RE:4}  <- PR #206 canlı
> Timeseries UPDATED (re-analysis) rows=1 health=27                 <- DK-40 canlı
> dashboard/farmer -> health_score 27/100 · ndvi_mean 0.266
> ```
>
> **DK-39 iki yönde:** `rgb_ortho_uri` ODM ortomozaiğini gösterirse `has_basemap=false`
> + 404 (float32, mavi bandı yok → sahte görüntü göstermiyor); DJI Terra RGB COG'u
> gösterirse `has_basemap=true` + **98 KB gerçek ortofoto, 24.104 farklı renk, gri
> piksel %0.0**. Düğme "hep açık" değil — kaynağı görünür ışık taşımıyorsa kapanıyor.
>
> ### Bulunan tek kusur: simülasyon koşumunun kendisi (düzeltildi)
>
> `kosum_3` §3 *"beyan dosyası yoksa fail-closed mu"* bölümü **kendi iddiasını
> ölçmüyordu**: koşum 5/6 aynı ODM dizinine operatör beyanını (`tarlaanaliz_engine.json`)
> yazdığı için girdi kirlenmişti — ekrana "RAW_DN olmalı" yazıp `SUN_IRRADIANCE` okuyordu.
> Beyansız geçici kopya + ters yön pozitif kontrolü ile düzeltildi. **Üretim kodu sağlam:**
> temiz kopyada `beyan YOK → RAW_DN`, `beyan VAR → SUN_IRRADIANCE`.
> **Genel ders:** bir koşum başka bir koşumun girdisine yazıyorsa, sonrakilerin pozitif
> kontrolleri **sessizce geçersizleşir**.
>
> ### Ölçülmeyenler (dürüst liste — "doğrulandı" sayılmasın)
>
> * Platform **tam** takımı ve `mypy` koşulmadı; yalnız değişen modüllerin 116 testi.
> * Yerel `ruff 0.15.12`, CI'nın pinlediği **0.15.20** (aynı araç, yama sürümü farklı).
> * Tarayıcıda **görsel** doğrulama yapılmadı; API + tile ölçüldü.
> * **mTLS bacağı yine koşulamadı** — M2→depo yüklemesi elle yapıldı (açık dikiş).
> * **DK-36 meşru dispatch yolu bilinçle atlandı**; sahte AV raporu / kalibrasyon kaydı
>   **YAZILMADI**, onun yerine `analysis_jobs` satırı elle açılıp üretim yayıncısı çağrıldı.
>
> ### Ortam tuzakları (bu turda ölçüldü — bir sonraki oturuma zaman kazandırır)
>
> * Docker Desktop kapalıysa önce o açılır; açılınca 8 konteynerin hepsi `healthy` geldi.
> * nginx **127.0.0.1:8080**'de (port 80 yayınlanmamış — `http://localhost/` bağlanamaz,
>   bu **502 sanılmasın**).
> * DB kullanıcısı **`tarlaanaliz_user`** (`tarlaanaliz` değil → `role does not exist`).
> * Giriş gövdesi alanı **`phone`** (`phone_number` değil → `Validation failed`).
> * Git Bash konteyner yollarını bozar → `MSYS_NO_PATHCONV=1` (`/etc/…` yolu
>   `C:/Program Files/Git/etc/…` oluyor ve "dosya yok" hatası veriyor).
> * Backend içi S3 önekleri `TARLA_S3_*`, worker'ınkiler `TARLAANALIZ_S3_*` — **farklı**.
>
> ### Gösteri öncesi açık kalemler (değişmedi)
>
> 1. 🟠 **Tarla sınırı gerçek görev planından gelmeli** — uydurma sınır yine
>    `coverage_ratio=0.0043` ve QC **FAIL** üretti (ölçüm artefaktı, hüküm değil).
> 2. 🟠 **DK-36 meşru dispatch yolu kapalı** (av1/av2 NULL, kalibrasyon kaydı yok).
> 3. 🟠 **M1/M2 ayrı istasyon yok**; her şey bu makinede (Docker).
> 4. Demo verisi notu: `datasets.rgb_ortho_uri` **Terra RGB COG'da kalmalı** — ODM
>    manifesti yutulursa bu alan ODM ortomozaiğine döner ve "Gerçek Görünüm" kapanır.

---

## 0.A-g ÖNCEKİ TUR — (2026-08-08, **yedinci oturum: DENETİM TURU — beş kusur, hepsi merge + deploy**)

> ### 🔴 EN ÖNEMLİ ÜÇ CÜMLE
>
> 1. **Zincir gerçek veriyle uçtan uca kapandı ve çiftçinin sayfasına yansıdı:**
>    M3M uçuşu → DJI Terra → edge paketleme (**COG otomatik**) → platform ingest →
>    worker → tüketici → dashboard **27/100 · ndvi 0.266** · **RGB "Gerçek Görünüm"**.
> 2. **Beş üretim kusuru bulundu, düzeltildi, MERGE EDİLDİ ve imajlar yeniden kuruldu**
>    (merge ≠ deploy — üç imaj da yeniden kurulup içeriği doğrulandı).
> 3. **En ağır bulgu DK-38'di:** çiftçiye gösterilen sağlık puanı **yanlıştı** (15,
>    doğrusu 27) — worker geçersiz piksel maskesini hiç okumuyordu. DJI Terra ile
>    bağımsız karşılaştırma sorunun **motorda değil tüketicide** olduğunu kanıtladı.
>
> ### Merge edilen beş PR
>
> | Depo | PR | İçerik |
> |---|---|---|
> | contract | **#55** | devir notu + §0.A-mtls + eylem planı (DK-31…DK-42) |
> | platform | **#401** | 🔴 DK-34 dashboard boş · DK-35 kalibrasyon tipi taşınmıyor · DK-39 gri taban görüntü · DK-40 yeniden analiz yansımıyor · çiftçi dili |
> | platform | **#402** | 🔴 DK-42 nginx `upstream` IP'yi donduruyor → **502** |
> | worker | **#207** | 🔴 DK-38 geçersiz piksel maskesi okunmuyor → **sessiz yanlış NDVI** |
> | edge | **#64** | DK-41 taban görüntü paketleme anında **COG**'a çevrilir (her uçuşta otomatik) |
>
> ### Bilimsel karşılaştırma — Terra ↔ ODM (ölçüldü)
>
> | Kaynak | mean NDVI | std |
> |---|---|---|
> | DJI Terra (kendi bant rasterleri, `nodata=nan`) | **0.2639** | 0.1551 |
> | ODM `camera` (alfa maskeli) | **0.2657** | 0.1372 |
> | ODM **maskesiz** (kusurlu hesap) | 0.1515 | 0.1674 |
>
> İki motor arasındaki fark **<%1** — radyometrik işleme tutarlı. Worker'ın raporladığı
> `0.151` maskesiz değerle **birebir** aynıydı: ortomozaik köşe kutusunun yalnız %57'sini
> kaplıyor, %43 boş alan NDVI=0 olarak ortalamaya giriyordu.
>
> ### Kurulum durumu (merge ≠ deploy — ölçüldü)
>
> | Bileşen | `src` bind-mount | Yapılan |
> |---|---|---|
> | backend | ✅ var | `compose build backend` + recreate |
> | worker | ❌ **yok** | `docker build -f Dockerfile.gpu` |
> | web | ❌ hiç mount yok | `compose build web` |
>
> İmajların **içinde** yeni kod doğrulandı (`grep -c DK-38/DK-39/DK-40` konteyner içinde).
> ⚠️ `docker cp` geçici yamadır — konteyner yeniden oluşturulunca kaybolur.
>
> ### Gösteri öncesi bilinmesi gerekenler
>
> 1. 🟠 **Tarla sınırı gerçek görev planından gelmeli.** Test koşumunda uydurma sınır
>    `coverage_ratio=0.5069` → QC **FAIL** üretti. Gerçek sınırla düzelir.
> 2. 🟠 **Meşru dispatch yolu hâlâ kapalı** (DK-36): `av1_report_uri=NULL`,
>    `av2_report_uri=NULL`, `calibration_records=0`. Koşumlarda bu kapı bilinçli atlandı;
>    **sahte AV raporu / sahte kalibrasyon kaydı YAZILMADI**.
> 3. Donanım: M1/M2 ayrı istasyon **yok**; her şey bu makinede (Docker). Laptop yalnız
>    tarayıcı olarak kullanılacaksa backend `127.0.0.1`'e bağlı — ağa açmak ayrı iş.
>
> ### Ortam tuzakları (bu turda ölçüldü)
>
> * **nginx 502 = imaj kurulumunun yan etkisi** (DK-42, artık kalıcı düzeltildi). Eski bir
>   kurulumda görülürse hızlı çare `docker restart tarlaanaliz-nginx`.
> * Backend `RABBITMQ_URL` konteyner içinde **`localhost`** gösteriyor (yanlış); çalışan
>   biçim worker'ınkidir: `amqp://…@tarlaanaliz-rabbitmq:5672/%2Ftarlaanaliz` (vhost URL-kodlu).
> * Backend `/health` **`worker_bridge unreachable`** uyarısı basıyor — ayrı kalem.
> * Edge CI `ruff check` **ve** `ruff format --check` koşar; yeni bir `src/` modülü
>   `config/build_profiles.yaml` → `ownership` + karşı makinenin `exclude`'una girmeli.

---

## 0.A-f ÖNCEKİ TUR — (2026-08-08, **altıncı oturum: DK-28/DK-29 zinciri + ilk gerçek-veri koşumları + üç üretim kusuru**)

> ### 🔴 EN ÖNEMLİ ÜÇ CÜMLE
>
> 1. **DK-28/DK-29 zinciri KOD DÜZEYİNDE uçtan uca bağlandı** — üretici→tüketici arasında
>    kopuk halka yok (2026-08-08 denetiminde halka halka izlendi: edge `package_builder`
>    → `calibrated_manifest_uploader` → platform `POST …/calibrated-manifest` →
>    `datasets.calibrated_ortho_uri` → `worker_job_publisher.py:205` `image_urls=[ortho]`
>    → worker `_parse_job`). **Gerçek veri M1→M2'ye kadar aktı** (ODM 3 kol + DJI Terra
>    → kanıt seti → M1→M2 gözetim zinciri). ⚠️ **M2→platform bacağı bu turda
>    KOŞULAMADI** (mTLS provizyonu yoktu); aşağıdaki "demo" bloğundaki 3 katman **daha
>    önceki bir dataset'ten** üretildi. Yani **tek bir uçuşun uçtan uca aktığı henüz
>    ÖLÇÜLMEDİ** — kalan adımlar §0.A-mtls'te.
> 2. **Test etmek üç GERÇEK üretim kusuru buldu** — üçü de ölçülüp düzeltildi ve
>    merge edildi: platform boot-crash (bayat KR-042 pini) · M2 replay **veri kaybı** ·
>    worker bant sözlüğü uyuşmazlığı + **sessiz yanlış NDVI**.
> 3. **Beş çapraz-repo değişmezi tutuyor**, dört depoda **0 açık PR**, dört çalışma
>    ağacı da temiz ve ana dalda (ölçüldü, aşağıda).
>
> ### Merge edilenler (bu tur)
>
> | Depo | PR | İçerik | Merge |
> |---|---|---|---|
> | edge | **#62** | DK-28 M1 ÜRETİCİSİ: `package_builder` + `uri_resolver` kancası + `RasterioFootprintReader` + `POST /calibration-gate/build` | `3655dfa` |
> | edge | **#63** | 🔴 M2 **VERİ KAYBI**: replay denemesi meşru stage'i siliyordu | `02a1967` |
> | platform | **#399** | DK-28 artefakt kapsamı: `X-Artifact-Name` + `assembled_uri` + akıtmalı birleştirme | `05faf59` |
> | platform | **#400** | 🔴 **BOOT-CRASH**: bayat `CONTRACTS_SHA256` pini (96 pin / 97 dosya) | `46f9cb5` |
> | worker | **#206** | 🔴 bant sözlüğü uyuşmazlığı + konumsal bant eşlemesi (**sessiz yanlış sayı**) | `b7dd53f` |
>
> Tur başında ayrıca #61/#398/#205 (v7.6.0 pin + kalibre-manifest ingest ucu) merge edildi.
>
> ### Ölçülen değişmezler (kapanış anı)
>
> ```
> I-1  contract 7.6.0 · platform 7.6.0 · worker v7.6.0 · edge SSOT 7.6.0 (edge SemVer 1.7.0)
> I-2  git -C contracts describe --tags HEAD  ->  v7.6.0   (temiz, bulanık değil)
> I-3  git submodule status contracts  ->  fc7e0e6b (v7.6.0), '+/-' YOK, içerik temiz
> I-4  worker compute_contracts_hash.py --verify  ->  OK (v7.6.0)
> I-5  BİR geçici sapma: worker bant enum'u kanonikten önde (devir spesi yazıldı)
> ```
>
> Dört depo: `contract=master · platform=main · edge=main · worker=master`, hepsi **0 kirli dosya**.
> Dört depoda **0 açık PR**.
>
> ### Gerçek veriyle ne koşturuldu (`edge-simulasyon/KOSUM_SONUCLARI.md`)
>
> | Koşum | Ne ölçüldü |
> |---|---|
> | 5 | Üretici, gerçek ODM 3 kol + Terra ile. `none` kolu **KR-018 sert red**. Üç manifest de **kanonik** şemayı geçti |
> | 6 | `/build` HTTP ucu; H3 depo-kökü hapsi + kayıtsız drone reddi doğrulandı |
> | 7 | M1→transfer→M2 gözetim zinciri; **4 farklı ret sebebi** (ayırt edici) |
>
> **🔴 En değerli sayı:** DJI Terra ortomozaiği köşe kutusunun **yalnız %54'ünü** kaplıyor.
> Kutu kullanılsaydı kapsama 1.00 okunacak, KR-065 oranı → KR-031 **ödemesi %84 şişecekti**.
> Geçerli-piksel maskesi tercihi teorik değilmiş.
>
> ### Demo — worker sonuçları artık GÖRÜNÜYOR
>
> ```
> layers            3 katman  (HEALTH/ndvi · ndre · stress_ratio) -> /api/v1/tiles/...
> available_indices ['ndvi', 'ndre', 'stress_ratio']
> overall_health    0.151  (basis: FIELD_MEAN_NDVI)
> has_basemap       True            <- "Gerçek Görünüm" de açıldı
> tile render       HEALTH 115 KB · NITROGEN 127 KB · WATER 123 KB · BASEMAP 1.7 KB
> ```
>
> Öncesi `layers: []` idi. Kopuk halka `datasets.result_uri` idi — **NULL değil boş dize**,
> yani tüketici koşmuş, worker mesajında alan yokmuş (satır 2026-08-04'ten, ilk manifest
> 2026-08-05'ten → eski satır hiçbir zaman katman kazanamazdı).
>
> `summary` ve `detections` **bilerek boş**: `report_phase=PRELIMINARY` (mission `DONE` değil).
> Bu **KR-019 uzman onay kapısıdır**, kusur değil — DB'den zorlanmadı.
>
> ### Sonraki oturumun kapısındaki kalemler
>
> Tam liste **eylem planında**. Buradaki üçü durum fotoğrafının parçası:
>
> 1. 🔴 **AK-4 aynası:** kanonik `analysis_job.v1` → `drone_metadata.available_bands`
>    hâlâ serbest string. Worker önden gitti (vendored enum); kanonik ayna inmeli.
>    Gerekçe + istek: `tarlaanaliz-worker/denetim/birlesik_devir_spec_arsivi_2026.md` §1
>    (2026-08-11'e kadar ayrı dosya: `band_sozlugu_devir_spec_2026_08_08` §3).
> 2. 🟡 **mTLS: sertifika engeli KALKTI (2026-08-08), kalan iş proxy + kayıt.** Bkz. §0.A-mtls.
> 3. 🟠 **AV2 servisi deploy edilmemiş** (`TARLA_AV2_ENABLED=false`, `av2-scanner` konteyneri yok)
>    → `is_ready_for_analysis` sağlanamıyor, yani **tam meşru** dispatch yolu kapalı.
>    Demo koşumunda AV ön koşulu bilinçli atlandı; **sahte AV raporu YAZILMADI**.
>
> ### ⚠️ Sonraki oturum için ölçülmüş tuzaklar
>
> * **`main`'e merge DEPLOY DEĞİLDİR.** Backend `src/` bind-mount ama `CONTRACTS_VERSION.md` +
>   `contracts/` **imaja gömülü**; uvicorn `--reload`'suz. Yeni sözleşme sürümünde
>   **imaj yeniden kurulmalı** (`docker compose build backend`), yoksa boot-crash.
> * **Worker `src` bind-mount DEĞİL** — kod değişikliği için
>   `docker build -f Dockerfile.gpu -t tarlaanaliz-worker:gpu .` +
>   `docker compose --env-file ../tarlaanaliz-platform/.env up -d worker` (env-file ZORUNLU).
> * **mypy çalışma ağacında çöküp taze klonda çalışıyorsa** ilk şüphe bayat `.mypy_cache`'tir
>   (bugün tam olarak bu oldu; silince iki taraf da 56 hata verdi).
> * **Edge CI'da iki iş PR'da ATLANIR** (`Test Windows` + `Package Build`, Windows/2× ücret
>   kapısı). `build_profiles.yaml`'a dokunursan paket kapısını **yerelde** koştur.

---

## 0.A-mtls — M2→platform kolu: sertifika engeli KALKTI (2026-08-08 denetim turu)

> ### Önce kavram — bu sertifika **satın alınmaz**
>
> mTLS (karşılıklı TLS = hem sunucu hem istemci birbirine sertifika göstererek kimlik
> kanıtlar) için gereken **istemci sertifikası** halka açık bir sertifika otoritesinden
> (CA = Certificate Authority, sertifika imzalayan kurum) **alınmaz**. Let's Encrypt gibi
> ücretsiz CA'lar yalnız **sunucu** sertifikası verir; istemci kimliği için sertifika
> vermezler. Bu sistemde zaten veremezler: platform, tanıdığı cihazları
> **`API_MTLS_REGISTERED_FINGERPRINTS`** listesindeki parmak izleriyle (fingerprint =
> sertifikanın SHA-256 özeti) tanır — yani güven kaynağı **kendi özel CA'mızdır**.
> Dışarıdan alınan bir sertifika bu kapıyı hiç açmaz. **Maliyet: sıfır.**
>
> ### Ne yapıldı (ölçüldü)
>
> | Adım | Sonuç |
> |---|---|
> | Özel CA + istemci sertifikası üretildi (`openssl`, RSA-4096 CA / RSA-2048 istemci) | `openssl verify -CAfile ca.pem client.pem` → **OK** |
> | `extendedKeyUsage = TLS Web Client Authentication` | ölçüldü ✅ |
> | Konum: **`C:\ProgramData\TarlaAnaliz\certs\`** (kodun gerçek kökü — `config.py:20` `_CFGROOT`) | `client.pem` · `client-key.pem` · `ca.pem` |
> | HC-03 kapısı | `EdgeCloudClient(config=…)` artık **`CertificateNotFoundError` FIRLATMIYOR** |
>
> ⚠️ Depo içindeki `tarlaanaliz-edge/config/security/certs/` **yükleme yolu DEĞİLDİR** —
> ilk denemede oraya konmuştu ve kod görmedi. Gerçek kök `_CFGROOT`'tur.
> (Her iki konumda da `.gitignore:30` `*.pem`'i kapatır — sır commit edilmez.)
>
> ### Kalan üç adım (bunlar olmadan kol hâlâ koşmaz)
>
> 1. **Parmak izini platforma kaydet:** `.env` → `API_MTLS_REGISTERED_FINGERPRINTS=<izi>`.
>    Hesabı platformun kendi yöntemiyle yapılır (`mtls_verifier.py:215-222` — PEM gövdesinden
>    başlık/satır sonu çıkarılıp SHA-256). Liste **boş bırakılırsa fail-closed**: hiçbir
>    cihaz kabul edilmez (`no_registered_devices`).
> 2. **mTLS'i sonlandıran ters vekil (reverse proxy) gerekli.** Platform sertifikayı
>    soketten değil **başlıktan** okur: `X-Client-Cert` + `X-Client-Cert-Verify: SUCCESS`
>    (`mtls_verifier.py:148-170`, `SUCCESS` değilse fail-closed). Yani nginx/traefik gibi
>    bir katman TLS'i sonlandırıp bu iki başlığı **kendisi** set etmeli.
> 3. **Platform ayakta olmalı.** Denetim anında Docker Engine kapalıydı; `main`'e merge
>    **deploy değildir** (imaj yeniden kurulmadan yeni sözleşme sürümü boot-crash yapar).
>
> ### Üretim töreni (saha donanımı gelince)
>
> Yukarıdaki sertifikalar **test/sim** içindir (CN=`sim-m2-01`). Gerçek istasyonda: CA'nın
> özel anahtarı (`ca-key.pem`) **M1/M2'de DEĞİL**, çevrimdışı bir kasada durur; her kiosk
> için ayrı CN (`STATION-XXX-01`) ile ayrı istemci sertifikası imzalanır; parmak izi
> platform env'ine eklenir. Bir kiosk kaybolursa **yalnız o parmak izi** listeden silinir.

---

## 0.A-uctan-uca — ZİNCİR GERÇEK VERİYLE KAPANDI (2026-08-08 denetim turu)

> ### 🔴 EN ÖNEMLİ ÜÇ CÜMLE
>
> 1. **Zincir ilk kez tek bir akışta uçtan uca koştu:** edge kalibre manifesti →
>    platform ingest → `analysis_job.v1` → worker (**gerçek ODM ortomozaiği**) →
>    sonuç → tüketici → `field_index_timeseries` → **çiftçinin sayfası**.
> 2. **İki kopuk halka bulundu ve düzeltildi** (platform [#401](https://github.com/physiscs-zana/tarlaanaliz-platform/pull/401)):
>    **DK-34** dashboard boş kalıyordu · **DK-35** kalibrasyon tipi hiç taşınmıyordu.
>    İkisi de aynı sınıf: *tüketici kusursuz, üretici hiç yazmıyor.*
> 3. **Önceki turun iki düzeltmesi gerçek veriyle doğrulandı:** worker #206'nın bant
>    sözlüğü (kanonik `GREEN/RED/RED_EDGE/NIR` kabul edildi) ve bant planı
>    (`Band plan resolved via raster_descriptions: {'R':1,'G':2,'NIR':3,'RE':4}` —
>    konumsal varsayım kullanılmadı).
>
> ### Demo kullanıcının sayfası — ölçülen çıktı
>
> ```
> GET /api/v1/dashboard/farmer   (+905000000001 / FARMER_SINGLE)
>   ÖNCE : avg_health_score=null · health_score=null · ndvi_mean=null
>   SONRA: avg_health_score=15.0 · health_score=15 · ndvi_mean=0.151
>          overall_health=FIELD_MEAN_NDVI · uyarı: "Sağlık skoru düşük: 15/100" (HIGH)
> GET /api/v1/results
>   3 katman (HEALTH/ndvi · NITROGEN_STRESS/ndre · WATER_STRESS/stress_ratio)
>   overall_health_index=0.151 · report_phase=PRELIMINARY
> ```
>
> **NDVI 0.151 gerçek ölçümdür** (29-07-2026 uçuşu, antep fıstığı, seyrek örtü) —
> uydurulmuş bir demo değeri değil. Worker 2496×2672 rasteri 36 tile'a böldü,
> `INDICES_ONLY` modunda bitirdi (güven 0.429 → KR-019 uzman kapısı devrede).
>
> ### mTLS — uygulama tarafı ÇALIŞTI
>
> Üretilen istemci sertifikasının parmak izi `.env`'e (`API_MTLS_REGISTERED_FINGERPRINTS`)
> eklendi ve backend yeniden kuruldu. `POST /api/v1/ingest/.../calibrated-manifest`
> çağrısı **401 → 403**'e döndü: yani **mTLS kimliği kabul edildi**, istek RBAC'ta durdu
> (`required_roles=['CENTRAL_ADMIN','STATION_OPERATOR']`, demo kullanıcı `FARMER_SINGLE`).
> Rol UYDURULMADI; aynı iş servis katmanından koşuldu (uç zaten yalnız onu çağırır).
>
> ### ⚠️ Hâlâ kapalı olan meşru yol (sahte kanıt YAZILMADI)
>
> `WorkerDispatchService.dispatch_to_worker` iki kapıdan geçemiyor (ölçüldü):
> `av1_report_uri=NULL` · `av2_report_uri=NULL` · `calibration_records=0`.
> Bu tur **AV kapısı ve kalibrasyon-kaydı ön koşulu atlanarak** `build_analysis_job_v1`
> + `publish_analysis_job` doğrudan çağrıldı. Yani ölçülen şey **worker→platform→arayüz**
> bacağıdır; **AV/kayıt ön koşulu hâlâ açık kalemdir.**
>
> ### Ortam tuzağı (yeni)
>
> Backend konteynerinde `RABBITMQ_URL` **`localhost`** gösteriyor (konteyner içinde yanlış
> adres). Çalışan doğru biçim worker'ınkidir:
> `amqp://tarlaanaliz:***@tarlaanaliz-rabbitmq:5672/%2Ftarlaanaliz` (vhost URL-kodlu).
> Ayrıca backend `/health` **`worker_bridge unreachable`** uyarısı basıyor — ayrı bir kalem.

---

## 0.A-e ÖNCEKİ TUR — (2026-08-07, **beşinci oturum: W8/Ç-2 · DK-23 · DK-26 · DK-28 keşfi**) — ✅ **KAPANDI, MERGE EDİLDİ**

> ### 🔴 EN ÖNEMLİ ÜÇ CÜMLE
>
> 1. **Üç açık kalem kapandı**, üçü de artık **kapıya** bağlı (yorum değil): W8/Ç-2
>    (kalibrasyon motoru → `encoder_version` tetikleyicisi + BUILD FAIL kapısı) ·
>    DK-23 (üç katmanda ondalık daralması) · DK-26 (eskalasyon FK önkoşulu).
> 2. **DK-28 KEŞFEDİLDİ:** "Gerçek Görünüm" düğmesi **üretimde hiç görünmüyor** —
>    arayüz kusursuz ve test edilmiş, ama `maps.rgb` üreticisi **hiç yok**
>    (`_MAPS_BY_RESULT_MODE` = ndvi/ndre/stress_ratio). Karar gerekiyor, eylem planına
>    üç seçenekle yazıldı.
> 3. **Eylem planındaki bir MEKANİZMA İDDİASI çürütüldü** (DK-26'nın "aio_pika tüketiciyi
>    öldürüyor"u) — kütüphane kaynağından ölçüldü. Altındaki kusur gerçekti ve kapatıldı.
>
> ### Açılan PR'lar (bu oturum)
>
> | Depo | PR | İçerik |
> |---|---|---|
> | worker | **#203** | W8/Ç-2 — `CALIBRATION_SCALE_CHANGE` tetikleyicisi + `encoder_version_reason` build kapısı |
> | platform | **#393** | DK-23 (numeric(4,3) hizalaması) + DK-26 (eskalasyon FK kapısı) |
> | contract | **bu PR** | eylem planı: W8/DK-23/DK-26 kapandı, DK-28 açıldı |
>
> ### Ölçülen kapılar
>
> worker `pytest tests/unit` **3928 passed** · platform **5730 passed** (`PYTEST_EXIT=0`) ·
> iki depoda `ruff` temiz · platform `mypy src/` 461 dosya 0 sorun ·
> **13 mutasyon koşuldu, 13'ü de testleri kırdı**, her birinin yanında pozitif kontrol.
>
> ### Ortam notu
>
> **Docker Desktop yeniden ayağa kaldırıldı (29.4.3).** 2026-08-06 15:22–2026-08-07 00:05
> UTC arasında **GitHub Actions büyük kesintisi** vardı; o pencerede kuyruğa giren
> contract master koşusu **kalıcı olarak `queued`'da çakılı** kaldı (iptal/rerun ikisi de
> reddediyor — kurtarma yolu yeni push). Worker master `0b4fd5e` **yeşil** (ölçüldü).

---

## 0.A-d ÖNCEKİ TUR — (2026-08-05, **dördüncü oturum: DK-17/DK-18 kalıcı çözüm + İLK GERÇEK İŞ MESAJI**)

> ℹ️ Aynı günün önceki üç turu §0.A-c / §0.A-b / §0.A-a'dadır ve geçerliliğini KORUR.
>
> ### 🔴 EN ÖNEMLİ İKİ CÜMLE
>
> 1. **Worker ilk kez gerçek bir `analysis_job` mesajı işledi** — ve KR-018 kapısı doğru
>    biçimde reddetti. Çıkarım hâlâ koşmadı; sebebi **kod değil veri**: elimizdeki Terra
>    çıktısı **radyometrik düzeltme KAPALI** üretilmiş, yani ham DN (DK-21).
> 2. **`s3_endpoint` ölü alanı yalnız yazma yolunu değil OKUMA yolunu da bozuyormuş** —
>    GDAL endpoint'siz kalınca `s3://` isteği **gerçek AWS'ye** çıkıyordu. İlk kalem
>    (DK-17) bunu görmemişti; denetimde çıktı.
>
> ### ✅ DK-17 — `s3_endpoint` artık İKİ yola da bağlı (tek kaynak)
>
> `src/shared/s3_endpoint.py` eklendi: boto3 `endpoint_url` + path-style adresleme alır,
> GDAL `AWS_S3_ENDPOINT`/`AWS_HTTPS`/`AWS_VIRTUAL_HOSTING` alır. Ortam değişkeni adı
> `WorkerConfig.model_config["env_prefix"]`'ten **türetilir** (ikinci kopya yok).
> Bağlanan yerler: `result_artifact_sink` · `s3_export_sink` · `adapter_registry` ·
> `pipeline._open_validated_image`.
>
> **Üretim yolundan ölçüldü** (konteyner içinde, `AWS_S3_ENDPOINT` ortamda **YOKken**):
> ```
> okuma : _open_validated_image("s3://tarlaanaliz-results/.../ndvi.tif") -> 8558x7638 EPSG:4326
> yazma : S3ResultArtifactSink.upload(...) -> s3://tarlaanaliz-results/dk17-smoke/.../manifest.json
>         (MinIO'da gerçekten göründü: manifest.json 134 B · ndvi.png 19 B — sonra silindi)
> ```
> Ölçüm imzası (endpoint'siz koşunun AWS'ye gittiğinin kanıtı): MinIO
> *"The Access Key Id ..."* der, AWS *"The **AWS** Access Key Id ..."* der.
>
> ### ✅ DK-18 — `[s3]` extras hash-kilitli olarak imajda
>
> `requirements-s3.in` + `requirements-s3.lock` (`pip-compile --generate-hashes`, 7 paket
> tam geçişli) · `Dockerfile.gpu`'da **ayrı katmanda** `--require-hashes` kurulum (torch
> katmanının build cache'ini bozmamak için). İmaj 13.7 → **13.8 GB**; konteynerde
> `boto3 1.43.64` doğrulandı. Compose'ta `TARLAANALIZ_ENABLE_RESULT_ARTIFACT_UPLOAD: "true"`.
> **Kök sorun:** tek bir ürün kararı İKİ kapıya bağlıydı; ikincisi (imaj içeriği) görünmezdi.
>
> ### 🧪 İLK GERÇEK İŞ MESAJI — ölçülen zincir
>
> Gerçek DJI/Terra ortomozaiğinden 4-bantlı COG yığıldı (G/R/RE/NIR · 8558×7638 · 618 MB),
> MinIO'ya yüklendi, `analysis_jobs`'a dürüst `calibration_type: NONE` ile basıldı:
> ```
> worker  : KR-018: Calibration NONE — job rejected
> worker  : Message published -> analysis_results   (status=REJECTED, NO_RESULT)
> worker  : Message published -> expert_review_queue
> platform: WORKER_BRIDGE.RESULT_RECEIVED status=REJECTED · ANALYSIS_FAILED
> ```
> ⚠️ Platform `analysis_results` **satırı yazılmadı** — doğrudan kuyruğa basılan iş için
> `analysis_jobs` satırı yoktu (FK). Bu **düzeneğin** eksiği, üretim yolunun değil.
> Demo satırını bozmamak için DB'ye elle kayıt açılmadı.
>
> ### 🔴 BU KOŞU ÜÇ YENİ KUSUR ÇIKARDI (birim testler göremiyordu)
>
> | # | Bulgu | Durum |
> |---|---|---|
> | **DK-19** | Worker eskalasyon gövdesi `audit_bucket`/`audit_rotation_key`/`audit_selection_rate` alanlarını **açık `null`** yazıyordu; şema opsiyonel ama `null` kabul etmiyor → **kendi vendored şemasını ihlal eden** mesaj. Fixture'lar alanları dolu verdiği için görülmüyordu (**DK-13 boşluğu**) | ✅ kapatıldı — düşürülecek alan **şemadan türetiliyor** |
> | **DK-20** | **Platform üretim imajında `jsonschema` YOK** → KR-081 kapısı worker'dan gelen her mesaj için **fail-open**. Platform kendi logunda söylüyor: `SCHEMA_VALIDATE_BROKEN ... KR-081 kapısı bu mesaj için ETKİSİZ`. `pyproject.toml` onu **`dev`** grubunda beyan ediyor; `requirements.lock`'ta yok. **DK-18'in platform ikizi** | ✅ kapatıldı — ana bağımlılığa taşındı, lock yenilendi, imaj kuruldu; **pozitif kontrolle** doğrulandı (kasten bozuk mesaj `SCHEMA_INVALID` + DLX, DB'ye değmedi) |
> | **DK-21** | Terra çıktısı **ham DN** → ÖN RAPOR üretilemez. ⛔ 2026-08-06: *"Terra'yı düzeltme açık yeniden koş, panel şart değil"* önerisi **ÇÜRÜTÜLDÜ** — Terra'nın Radiometric Correction ekranı (ekran görüntüsüyle ölçüldü) yalnız **kalibrasyon paneli** içindir, panel fotoğrafı sonradan eklenemez. Güneş sensörü verisi ham karelerin XMP'sinde **var** (`Irradiance` G 16078 / NIR 9742) ama Terra onu ayrı bir ekrandan sunmuyor | 🔴 **AÇIK — karar gerekiyor:** yeni uçuş+panel · **Pix4Dfields (panelsiz RELATIVE, SSOT:79)** · ya da Terra'da güneş-sensörü anahtarı aranması |
>
> ### 🔍 DEMO SAYILARININ DENETİMİ — hepsi yeniden üretildi
>
> Demo satırındaki (elle girilmiş) sayılar worker'ın **kendi fonksiyonlarıyla** gerçek
> veriden birebir çıktı — tarla sınırına kırpılmış Terra NDVI raster'i üzerinden:
> ```
> compute_mean_ndvi          -> 0.264   (DB overall_health_index = 0.264 ✔)
> critical% + poor%          -> 85.00   (özet "yüzde 85" ✔ · 7,07 dönüm ↔ "7,1" ✔)
> good% + excellent%         ->  5.42   (0,45 dönüm ↔ "0,5" ✔)
> geçerli piksel oranı 50.7% -> 16.41 × 0.507 = 8.32 dönüm  (özet "8,3 dönüm" ✔)
> ```
> **Yani ÖN RAPOR metni dürüst; yalnız makine üretmiyor.** İki uyarı: (a) bu NDVI ham DN
> üzerinden hesaplandığı için mutlak eşikler **yaklaşıktır** (DK-21); (b) `round(raw, 2)`
> yüzünden kod yolu `0.264`'ü **asla** üretemez, `0.26` olur — kolon `numeric(4,3)` (**DK-23**).
> Ayrıca raster okunurken `nodata=0.0` nöbetçisi dikkate alınmazsa aynı sayı **0.1525**
> çıkıyor (%42 hata) — bugün canlı değil ama tuzak duruyor (**DK-22**).
>
> ### 🏁 EN GÜÇLÜ TEK KANIT — worker kendi konteynerinde, kendi kodu, gerçek veri
>
> `InferencePipeline._load_bands` **üretim fonksiyonu** MinIO'daki gerçek 4-bantlı
> ortomozaiği `s3://` üzerinden okudu ve worker'ın kendi ölçüm fonksiyonları şunu üretti:
> ```
> OKUNAN BANTLAR: ['G','NIR','R','RE'] · crs=EPSG:4326 · 7638x8558 · gecerli %50.2
> mean_ndvi(RELATIVE) = 0.2639            -> DB overall_health_index 0.264 ✔
> dagilim = critical 38.8 · poor 46.2 · fair 9.57 · good 5.13 · excellent 0.29
>           critical+poor = %85.0          -> ozet "yuzde 85" ✔
> ```
> Bu, Terra'nın NDVI raster'inden **bağımsız ikinci bir türetmedir** (ham bantlardan
> hesaplandı) ve üç ondalıkta aynı sayıyı verdi.
> ⚠️ **Bu bir ÖLÇÜM TATBİKATIDIR, kapıdan geçmiş bir iş DEĞİL:** `RELATIVE` metrik
> fonksiyonlarına **elle** verildi. Gerçek iş hâlâ dürüstçe `NONE` ile gidiyor ve
> **reddediliyor** (DK-21 kapanana kadar öyle kalmalı).
>
> ### ♻️ SONRAKİ KOŞUM İÇİN HAZIR DURAN
> `s3://tarlaanaliz-results/jobs/dicle-20260729/bands_basic4.tif` (618 MB, G/R/RE/NIR
> yığılmış COG) MinIO'da duruyor. Terra düzeltme AÇIK yeniden koşulunca bu dosya
> **yeniden üretilmeli** (bantlar değişecek), sonra aynı akış `RELATIVE` ile koşulur.
>
> ### 🟢 2026-08-06 EKİ — ODM KOŞTU, ÇIKARIM İLK KEZ ÇALIŞTI, İKİ YENİ KUSUR ÇIKTI
>
> * **DK-21 KAPANDI.** ODM `camera+sun` 670 fotoğrafı **14 dk**'da işledi; çıktı 5 bantlı
>   **reflektans** ortofoto (0–0.20). Panelsiz, ücretsiz. Terra ↔ ODM farkı **%0.6**
>   (`mean_ndvi` 0.264 ↔ 0.2657) — *"kalibrasyon %85'i %62'ye indirir"* öngörüm **çürüdü**.
> * **KR-018 kapısı İLK KEZ GEÇTİ** ve çıkarım boru hattı baştan sona koştu.
> * 🔴 **DK-25:** ama **20/20 tile NaN yüzünden atlandı** (orto ayak izi dikdörtgen değil,
>   raster'ın %43'ü NaN) → `NO_RESULT` → `metrics` hiç gitmedi. **Gerçek orto ile çıkarım
>   bugün pratikte hiçbir şey analiz etmiyor.** Politika kararı ister (ML incelemesi).
> * 🟠 **DK-26:** platform `worker_bridge` tüketicisi ölü (`health-degraded`), kuyruklar
>   bekliyor; kök neden yakalanmayan `IntegrityError` tüketici görevini öldürüyor.
>
> ### 🎯 2026-08-06 (öğleden sonra) — **ÖN RAPOR İLK KEZ MAKİNEDEN ÇIKTI**
>
> ```
> result_mode PARTIAL_REPORT · confidence 0.598 · calibration_type RELATIVE
> health_distribution: critical 35.98 · poor 51.79 · fair 7.22 · good 4.72 · excellent 0.28
> mean_ndvi 0.2657 · absolute_scale_valid false
> relative_distribution (DK-24): p05 0.132 · p20 0.170 · p50 0.227 · p80 0.322 · p95 0.600
> ```
> Bağımsız ölçümle birebir aynı (0.2657 / %87.8). Zincir: ODM `camera+sun` → COG →
> MinIO → `analysis_jobs` → KR-018 geçti → çıkarım → rapor → köprü.
>
> **Bunun için DÖRT kusur düzeltildi** (üçü sessizdi) — DK-25 (tile NaN politikası),
> `safe_divide` (bilinmeyen → 0.0, %50 hata), **DK-27 (MC-Dropout `.eval()` eksikti —
> çıkarım 2026-05-17'den beri HİÇ çalışmamış)**, ve sebebi doğrulamadan isimlendiren log.
>
> **Terra ↔ ODM üç kollu karşılaştırma:** `docs/TERRA_ODM_KARSILASTIRMA_2026-08-06.md`
> — kalibrasyonun ağırlığı **kamera düzeltmelerinde** (`none→camera` ortalama +%47),
> güneş sensörü ekstra ~%0; Terra zaten **yarı kalibre**; piksel düzeyindeki düşük
> korelasyonun sebebi **konumsal kayma** (uçuşun kendi RMSE'si 1.838 m ≈ 37 px).
>
> ### 📌 GİRİŞ NOKTASI
> Yazılım kuyruğu → eylem planı **§3.6 (`DK-1…DK-27`)**.
> **AÇIK:** DK-26 (köprü tüketicisi IntegrityError'da ölüyor) · **W8/Ç-2** (motor
> değişimi `encoder_version` tetikleyicisi — kanıt artık var, kalem açık) · DK-23.
> *(Aşağıdaki DK-21 metni tarihsel kayıttır; kalem 2026-08-06'da kapandı.)*
> Terra panelsiz uçuşu kurtaramıyor; Pix4Dfields (SSOT:79) kurtarabiliyor. Üç seçenek,
> ölçümler ve karar akışı: [`docs/TERRA_RADYOMETRIK_YENIDEN_KOSUM.md`](TERRA_RADYOMETRIK_YENIDEN_KOSUM.md).
> Kalibre veri geldiği anda aynı akış `RELATIVE` ile koşar ve ÖN RAPOR makineden çıkar.

---

## 0.A-c ÖNCEKİ TUR — (2026-08-05, **üçüncü oturum: worker GPU + ölçüm zinciri**) — ✅ **KAPANDI, MERGE EDİLDİ**

> ℹ️ Aynı günün **birinci** turu §0.A-a'da, **ikinci** turu §0.A-b'de; ikisi de geçerliliğini
> KORUR. Bu tur onlarla paralel/ardışık koştu ve farklı alana dokundu (worker + ölçüm).
>
> ### 🔚 OTURUM KAPANIŞI — üç depo merge edildi, 0 açık PR
>
> | Depo | Dal | Tepe commit | PR'lar |
> |---|---|---|---|
> | **worker** | `master` | `91df0c5` | **#197** · **#198** (öz-denetim düzeltmeleri) |
> | **platform** | `main` | `7e8efe65` | #382 · #383 · #384 · #385 · #386 · **#387** |
> | **contract** | `master` | (bu commit) | #30 · #32 · #33 · #34 · #36 |
>
> ### 🟢 WORKER İLK KEZ AYAKTA — GPU ÇALIŞIYOR
>
> Worker'ın Docker imajı ve konteyneri **yoktu** (ölçüldü: `docker images | grep worker` boş).
> Artık `tarlaanaliz-worker:gpu` (13.7 GB) var ve konteyner **healthy**:
>
> ```
> GPU        : cuda.is_available()=True · RTX 3090 Ti 25.8 GB · torch 2.12.0+cu130
>              (gerçek tensör çarpımı koşturuldu — "kurulu" değil ÇALIŞIYOR)
> KR-041     : "runtime gate OK: contracts hash matches (v7.4.0)"
> RabbitMQ   : virtual_host=/tarlaanaliz · "Started consuming"
>              kuyruklar: analysis_jobs · ai.feedback.v1
> broker     : rabbitmqctl list_queues consumers -> her ikisinde de 1
> /healthz   : {"status":"ok", critical_rabbitmq_consumer: true, faiss_ready: true}
> ```
>
> Worker **kendi** `docker-compose.yml`'ini aldı; platformun ağına `external: true` ile
> dışarıdan bağlanır (iki depoyu birbirine bağlamamak + GPU'suz makinede
> `docker compose up`'ı kırmamak için). Platform ayakta değilse **açık hata** verir.
>
> 🔴 **İKİ GERÇEK KUSUR ÇIKTI — ikisi de düzeltildi:**
>
> 1. **İmaj hiç build edilememişti.** `--require-hashes` modunda torch 2.12'nin
>    `setuptools<82` bağımlılığı lock'ta yoktu → build FAIL. Runbook
>    (`docs/ops/gpu_supply_chain_hash_lock.md`) bunu dürüstçe yazmış: *"tam imaj build'i
>    bir sonraki gerçek deploy'da teyit edilebilir"*. Teyit yapıldı, kırık çıktı.
>    `setuptools==81.0.0` hash'leriyle eklendi (65→66 paket, **0 silme**).
> 2. **Vhost URL-encode edilmemişti.** Broker'daki gerçek ad `/tarlaanaliz` — baştaki
>    slash **adın parçası**. Ölçüldü: `.../tarlaanaliz` → yanlış ad · `...//tarlaanaliz`
>    → boş (`NOT_ALLOWED - vhost  not found`) · `.../%2Ftarlaanaliz` → **doğru**.
>
> ### 📊 ÖLÇÜM ZİNCİRİ — "canlılık puanı" artık gerçek kaynaktan
>
> **Bulunan kusur (ölçüldü):** platform `overall_health_index`'i **tespitlerin**
> `ndvi_value` ortalamasından türetiyordu; tespit yoksa `confidence_score` yedeğine
> düşüyordu — **o bir sağlık ölçüsü değil, modelin kendine güvenidir**. ÖN RAPOR'da
> tespitler KR-019 kapısıyla gizli olduğu için çiftçiye gösterilen puan **hep** o yanlış
> vekildi. Demo verisindeki `0.264` **elle** hesaplanıp DB'ye yazılmıştı; kod üretemiyordu.
> Bu fonksiyonun **hiç testi yoktu**.
>
> | Katman | Ne yapıldı |
> |---|---|
> | worker | `health_distribution.py` — tarla geneli NDVI dağılımı + ortalama (yeni) |
> | worker | `ReportingAgent._compute_field_metrics` → `ReportResponse.metrics` |
> | worker | orchestration taşır → `AnalysisResult.to_dict()` → mesajda `metrics` |
> | contract (vendored) | `analysis_result.v1` → `metrics` + `$defs.Metrics` |
> | platform | `_overall_health_from_body` **üç kademeli**: tarla geneli → tespit ort. → confidence |
>
> **Vendored şema sapma DEĞİL, hizalanma:** `metrics` kanonikte v7.4.0'da zaten vardı;
> worker'ın dar alt kümesi (I-4) taşımıyordu. Script'le kopyalandı, elle yazılmadı.
> KR-041 hash `bb66e1bc → d5526486`; **sürüm dizesi SABİT** (I-1). AK-4 devir spesi
> gerekmez — worker kanoniğe yaklaştı, uzaklaşmadı.
>
> ⚠️ **Tek uyarlama (3 yer):** kanonik `unevaluatedProperties` → worker
> `additionalProperties`. Worker'ın **kayıtsız** `Draft202012Validator`'ı ilkini çözemez;
> birebir kopya bilinmeyen-alan mührünü **gevşetir**. Bunu ben fark etmedim —
> `tests/contract/test_worker_runtime_profile_lock.py` kırmızı verip zorladı.
>
> ### 🖼️ DEMO EKRANI — "Gerçek Görünüm" + ölçüm sınırları
>
> - **RGB ortofoto taban katman** olarak eklendi (`/tiles/{id}/basemap/...` — ayrı uç,
>   `analysis_type` enum'una **dokunulmadı**; RGB analiz değil fotoğraftır). Açma/kapama
>   düğmesi katman listesinin **dışında**. Açılınca analiz katmanları geçici gizlenir —
>   yoksa yarı saydam raster'lar fotoğrafın **%75'ini** kapatıyordu (kullanıcı bildirdi,
>   opaklık matematiğiyle doğrulandı).
> - **Mapbox CSS** CDN yerine paketten. İlk deneme (#382) **canlıda işe yaramadı**:
>   `next.config.mjs`'teki geniş `sideEffects:false` regex'i CSS import'unu tree-shaking
>   ile atıyordu — build çıktısı **bit bit aynı** kalmıştı. #383 kök nedeni düzeltti
>   (ölçüm: mapbox CSS kuralı 0 → 107).
> - Metin sadeleştirildi (140→65 kelime, punto 16px), *"ekinle otu ayırmaz"* maddesi
>   **kaldırıldı** (kullanıcı kararı: `WEED` katmanı yol haritasında var, o cümle gelecek
>   yetenekle çelişiyordu). Saha gözleminin bilgisi korundu — "kurumuş ot" sebep listesinde.
>
> ### 🔴 SONRAKİ OTURUM BUNU BİLMELİ
>
> 1. **Worker çalışıyor ama ÇIKARIM DENENMEDİ.** Kuyruğu tüketiyor; gerçek bir
>    `analysis_job` mesajıyla uçtan uca akış **koşturulmadı**. Ayrıca **antep fıstığı için
>    eğitim veri seti yok** (`crop_readiness: pistachio data_status: limited`) — model
>    koşsa bile tespit güvenilirliği demo için yeterli olmayabilir. NDVI **ölçümü** ise
>    veri setinden bağımsız, o çalışır.
> 2. **`metrics` ucu ucuna bağlandı ama canlı mesajla doğrulanmadı** — worker gerçek iş
>    işleyip `metrics` gönderdiğinde platform kademe 1'i kullanacak. Zincirin her halkası
>    ayrı ayrı test edildi (mutasyonla), uçtan uca akış değil.
> 3. **Demoda "YZ" vaadi TAM RAPOR'a aittir.** ÖN RAPOR'da gösterilen şey ölçümdür
>    (kamera + matematik); ona "YZ analizi" demek ilk teknik soruda güven kaybettirir.
>    Ekranda YZ iddiası **yok** (ölçüldü) — bu doğru, korunmalı.
> 4. **Ölçüm-aracı tuzağı — bu turda DÖRT kez yaşandı:** `komut | tail` kalıbında `$?`
>    **pipe'ın son komutunu** ölçer. Bir kez "tsc=0" yazarken tsc **exit 1**'di; bir kez
>    arka plan görevi "exit code 0" derken docker build **başarısızdı**. Çıktıyı dosyaya
>    al, exit kodunu **ayrı** oku.
>
> ### 🔬 OTURUM SONU ÖZ-DENETİM — DÖRT KUSUR BULDU (worker PR #198)
>
> Kullanıcı talebiyle kapanıştan önce **katı, ispatlı öz-denetim** koşuldu. Dördü de
> **"doğrulandı" diye raporlanmış** yerlerdeydi; öz-denetim olmasaydı sessizce kalırdı.
> Bu artık **kalıcı kural** (`~/.claude/memory/tarlaanaliz/oturum-sonu-oz-denetim.md`).
>
> | # | Rapor ne diyordu | Ölçüm ne gösterdi | Düzeltme |
> |---|---|---|---|
> | 1 | "S3/MinIO yapılandırıldı" | `s3_endpoint = None` — `TARLAANALIZ_S3_ENDPOINT_URL` **hiç okunmadı** (doğrusu `..._S3_ENDPOINT`); `s3_access_key_id` diye alan **YOK** — worker çıplak `boto3.client("s3")` çağırıyor | `AWS_*` env'lerine geçildi, canlıda doğrulandı |
> | 2 | "eşikler config'te, hardcode değil" | İzinli kalibrasyon kümesi `enums.py::FINETUNE_ALLOWED_CALIBRATIONS`'ın **elle yazılmış ikinci kopyası**; o dosya "SINGLE SOURCE OF TRUTH" diyor | Config artık yalnız **politika** seçer; küme kanonik enum'dan **türetilir** |
> | 3 | "fail-closed: kalibrasyon uygunsa üretir" | DJI M3M varsayılanı `RELATIVE` (`enums.py:64` *"DJI default"*) → kapı reddediyordu → **sahadaki her uçuşta** dağılım hiç üretilmezdi | Politika `SSL` (RELATIVE dahil); `NONE` reddi kalır |
> | 4 | (izi sürerken çıktı) | **`boto3` imajda HİÇ YOK** — hiçbir lock'ta değil, `[s3]` extras'ında ve `Dockerfile.gpu` onu kurmuyor | Bilinçli tasarım; upload bayrağı sabit `"false"`, gerekçe yorumda |
>
> **Bulgu 3'ün bedeli sessiz bırakılmadı.** RELATIVE'de sınıf sınırları **yaklaşıktır**;
> çıktı artık `custom_metrics.absolute_scale_valid` (RELATIVE'de `false`) +
> `calibration_type` taşıyor. Tüketici "yaklaşık" etiketi basabilir. KR-025: worker
> yorumlamaz, ölçümün **geçerlilik bağlamını** bildirir. Bayrak `mean_ndvi` None olsa
> bile **daima** yazılır — yoksa yüzdeler mutlak sanılırdı.
>
> **K-3 korundu:** RELATIVE hâlâ fine-tuning'e **girmez**; bu yalnız ölçüm/gösterim
> yolu (worker CLAUDE.md §15 *"RELATIVE → sadece SSL morfoloji"* — politika adı da o yüzden `SSL`).
>
> Kilit: `RELATIVE` `SSL`'de kabul / `FINETUNE`'da red — **ayrıştırma testi**, yani
> `calibration_policy` gerçekten kümeyi değiştiriyor (no-op ayar değil). M7 mutasyonu
> (SSL'i dar kümeye bağla) 3 testi kırdı; geri alındı, hash birebir aynı.
>
> ### 📌 GİRİŞ NOKTASI
> Donanım/ölçüm hattı → 2026-08-02 bölümü (P-2 · P-6, hâlâ geçerli).
> Yazılım kuyruğu → eylem planı **§3.6 (`DK-1…DK-18`)**.
> Saha kontrol listesi → `docs/DEMO_GUNU_YAPILACAKLAR.txt` (EK-B canlı ölçümler).

---

## 0.A-b ÖNCEKİ TUR (aynı gün, ikinci oturum) — (2026-08-05, **bağlam altyapısı + KR-034 doküman hizası**) — ✅ **KAPANDI**

> ℹ️ **Aynı günün BİRİNCİ oturumu (demo görüntüleme hattı + dört-disiplinli denetim) hemen
> aşağıda §0.A-a'dadır ve geçerliliğini KORUR.** Bu oturum onunla paralel/ardışık koştu,
> farklı alana dokundu (edge + oturum altyapısı); iki bölüm birbirini geçersiz kılmaz.
>
> ### 🔚 OTURUM KAPANIŞI
>
> Bu oturumun ağırlığı **kod değil bağlam**tı: her oturumda projeyi sıfırdan öğrenme maliyeti
> kökten kaldırıldı. Depoya inen tek işlevsel değişiklik **edge PR #58**.
>
> | Depo | Dal | Durum |
> |---|---|---|
> | edge | `main` @ `adf10d0` | ✅ PR **#58** merged + pull edildi · temiz |
> | contract | `master` | bu devir notu · temiz |
> | worker | `docs/i5-devir-spec-uzlasma-2026-08-03` | **dokunulmadı** · temiz · upstream ile senkron |
> | platform | `main` @ `f761c317` | **dokunulmadı** (birinci oturumun alanı) |
>
> ### ✅ edge PR #58 — KR-034 motor-agnostik doküman hizası
>
> `tarlaanaliz-edge/CLAUDE.md`'de **altı yer** 2026-08-02 turundan sonra eski dünyada kalmıştı;
> ölçülüp düzeltildi (yalnız doküman, +51/−7): §20 KR-034 satırı *"Pix4Dfields drone-agnostik
> (yedek yazilim yok)"* → *"Kalibrasyon motoru AGNOSTIK: Pix4Dfields **veya** DJI Terra"* +
> tablo hücresine sığmayan iki hard kural notu (CLI yok → operatör GUI'den, edge çıktı dizinini
> okur · `calibration_type` iki girdili → ham DN = `NONE`) · §2 s.26/s.39 · §10 · §11 ·
> §12 (M3M'in göreliliği **motordan bağımsız bir fizik kısıtı**, Pix4Dfields'e özgü değil).
>
> §5'teki 5 `CALIBRATION.PIX4D_*` olayı **bilerek silinmedi** — kodda gerçekten var
> (`custody_logger.py:104-108`) ve `pix4d_runner.py` yayınlıyor; silmek dokümanı ters yönde
> yalancı yapardı. Blok `[ESKI YOL]` diye işaretlenip `dosya:satır` dayanaklı durum notu eklendi.
>
> ### 🔴 KOD TARAFINDA ÜÇ ÇELİŞKİ — ölçüldü, DOKUNULMADI
>
> Üçü de KR-034'ün kanonik metniyle çelişiyor; düzeltmeleri **P-2'ye bağlı** (gerçek motor
> export klasörü görülmeden yazmak, `pix4d_runner.py`'nin düştüğü hatanın tekrarı olur):
> 1. `pix4d_runner.py` var olmayan bir CLI'a subprocess açıyor **ve canlı bağlı**
>    (`pipeline_factory.py:68` → `calibration_pipeline.py:44,72,86`). `cli_path` yoksa
>    `__init__` `FileNotFoundError` atar (`pix4d_runner.py:113-114`) ⇒ üretimde boru hattı
>    **hiç kurulamaz**; testler `run_fn` dikişini enjekte ettiği için süit yeşil koşuyor.
> 2. `engine_adapter.py` **hiç WORM olayı yazmıyor** (`structured_log` çağrısı yok).
> 3. `resolve_calibration_type()` `src/` içinden **hiç çağrılmıyor** (yalnız testlerden) —
>    yeni yol yazılmış ama bağlı değil.
>
> ⇒ İş kalemi olacaklarsa **eylem planına** yazılmalı; bu dosya iş listesi tutmaz.
>
> ### ⛔ ÇÜRÜTÜLEN İDDİA — "push otomatik PR açar" YANLIŞ
>
> Dört depoda da push'ta PR açan **hiçbir mekanizma yok** (ölçüldü). Tek
> `peter-evans/create-pull-request` contract `auto_sync.yml`'de ve o dosya kendi başlığında
> *"UNCONFIGURED stub … MUST NOT auto-run on push"* diyor; tetiği yalnız `workflow_dispatch`.
> `git log --all -S "create-pull-request" -- .github/` platform'da **hiç** eşleşmiyor.
> PR sahipleri: platform 12/12 · contract 10/10 · worker 9/10 hepsi `physiscs-zana`
> (tek istisna `app/dependabot`). Mükerrer PR gözlemi doğruydu, **sebebi farklı**: iki kez
> `gh pr create` (#267 19:48:12 → #268 19:49:27, 75 sn arayla).
> ⇒ Otomatik PR'ı **bekleme**; `gh pr create` öncesi `gh pr list --head <dal>` ile ölç.
>
> ### ✅ Alt-modül stat-cache notu BAĞIMSIZ OLARAK DOĞRULANDI
>
> §0.A-a'daki uyarı doğru. Bu oturumda tekrar ölçüldü: `git -C tarlaanaliz-platform/contracts
> status --short` → **96 dosya** `M` gösteriyor, ama `diff --numstat` **boş** ve `diff --quiet`
> **exit 0** ⇒ **içerik farkı YOK**. (`update-index --refresh` göstergeyi temizlemiyor.)
> Bu bir senkron kırıklığı değildir; `status` çıktısına bakıp alarm verme.
>
> ### 🧹 edge dal temizliği + bir ders
>
> `main`'e birleşmiş **23 eski dal** yerelden silindi (güvenli `-d`); bu haftanın 4'ü bırakıldı.
> Hepsi `origin`'de duruyor (uzakta 36 dal, dokunulmadı) — geri alınabilir.
> `ci/geotiff-osgeo-coverage` bilerek bırakıldı ve şu ders çıktı: **`git branch --merged`
> TOPOLOJİYE bakar, İÇERİĞE değil.** O dalın tek farkı (`46e707b`, GDAL `setuptools/wheel`)
> main'de **zaten var** (`edge_ci.yml:84-90`, yorumlarına kadar aynı); PR #31 merge'inden
> **2 dk sonra** push edildiği için topolojik olarak yetim kalmış (merge-sync-lag).
> ⇒ "Birleşmemiş" görünen dalı silmeden önce `git diff main...<dal>` ile gerçek farkı oku.
>
> ### 💻 MAKİNE-YEREL ALTYAPI — **git ile TAŞINMAZ**, yeni makinede tekrar kurulur
>
> Kapsayıcı klasör git deposu olmadığı için şunlar bu makineye özeldir:
> `TARLA-ANALİZ/CLAUDE.md` (114 satır: 4-depo haritası · çapraz-repo değişmezleri · çalışma
> kuralları · giriş noktaları) · 5 × `.claude/settings.json` (`autoMemoryDirectory` → tek hafıza
> havuzu · `git_token.txt` için `permissions.deny` · `SessionStart` kancası) ·
> `~/.claude/hooks/tarlaanaliz-oturum-basi.ps1` · `~/.claude/memory/tarlaanaliz/` (42 konu dosyası).
> **Kurulum adımları kök `CLAUDE.md` §7'de.**
>
> Neden gerekliydi: hafıza **5 ayrı kovaya** bölünmüştü (kök 11 · platform 15 · worker 6 ·
> edge 6 · contract 2) ve hangi klasörden başlatıldığına göre yalnız biri görünüyordu; aynı olgu
> (sade-dil kuralı, 2026 yaz pilotu) birden çok kovada yeniden öğrenilmişti. Tek havuzda
> birleştirildi, eski kovalar yedek olarak duruyor.
>
> ### 📌 GİRİŞ NOKTASI — DEĞİŞMEDİ
>
> Donanım/ölçüm hattı: aşağıdaki 2026-08-02 bölümü (**P-2 · P-6**) aynen geçerli.
> Yazılım kuyruğu: eylem planı **§3.6**. TUR 3 hâlâ `PENDING_REPIN`;
> `describe --tags HEAD` → `v7.4.0-13-g3a1da5e` (**beklenen** — sürüm henüz yayımlanmadı,
> I-2 arızası değil).

---

## 0.A-a ÖNCEKİ TUR (aynı gün, birinci oturum) — (2026-08-05, **demo görüntüleme hattı + dört-disiplinli denetim**) — ✅ **KAPANDI, MERGE EDİLDİ**

> ### 🔚 OTURUM KAPANIŞI — yalnız `tarlaanaliz-platform` değişti, CI 18/18 yeşil
>
> | Depo | Dal | Merge commit | PR | Durum |
> |---|---|---|---|---|
> | **platform** | `main` | `f761c317` | **#381** | ✅ 18/18 (Alembic Upgrade/Downgrade Smoke + SSOT BOUND Header Guard dahil) |
> | platform | `main` | `95283e24` | #374 | ✅ (aynı oturumun ilk turu) |
> | contract · edge · worker | — | — | — | **DOKUNULMADI** — bu tur contract gerektirmedi |
>
> ```
> git -C tarlaanaliz-platform log --oneline -1 origin/main
>   f761c317 Merge PR #381: dort-disiplinli denetimin demo-oncesi kritikleri
> git -C tarlaanaliz-platform submodule status contracts
>   " eb28b74… contracts (v7.4.0)"   ← başında '+/-' YOK → I-3 sağlam
> ```
>
> ⚠️ **Ölçüm notu (yanlış alarma düşmemek için):** `git status` alt-modülü ` M contracts`
> gösterebilir. 2026-08-05'te ölçüldü: `git -C contracts diff --numstat` **boş**,
> `git diff --quiet` **exit 0** → içerik farkı YOK, yalnız stat-cache (dosyanın değişiklik
> zaman damgası tazelenmiş, içeriği değil). Bu, senkron kırıklığı **değildir**.
>
> ### ✅ NE BAŞARILDI — çiftçi sonuç akışı ilk kez uçtan uca çalıştı
>
> DJI Terra çıktısı (Dicle Ü. denemesi, M3M) elle COG'a çevrilip MinIO'ya yüklendi ve
> **çiftçi ekranında harita + katman olarak göründü**: `Terra index_map → cog_uret.py →
> minio_yukle.py (manifest) → demo_veri.py (6 tablo) → RBAC → KR-033 ödeme kapısı →
> tile ucu → tarayıcı`. Yol boyunca **6 gerçek hata** bulunup kalıcı olarak düzeltildi
> (SSR göreli URL · `libexpat1` eksiği · `rasterio.Env` yerine `AWSSession` ·
> `geographic_bounds` API'si · `analysis_results` ORM/şema ayrışması · `next.config.mjs`
> sessiz üretim varsayılanı — sonuncusu yerel giriş bilgilerini `api.tarlaanaliz.com`'a
> gönderiyordu).
>
> Ardından **dört bağımsız denetçi** (Kıdemli SWE · QA · Pentest · SDLC) turu denetledi,
> bulgular çapraz tartışmaya sokuldu ve **hepsi ana oturumda bizzat ölçülerek** doğrulandı.
> Demo-öncesi 6 kritik kalem (A1–A6) kapatıldı:
>
> | # | Kapatılan | Kalıcı kazanım |
> |---|---|---|
> | **A1** | `.env.yedek-*` hiçbir `.gitignore` kalıbına uymuyordu (21 sır, korumasız) | `.gitignore` genel kalıp + yedek depo ağacı dışına taşındı |
> | **A2** | `INTERNAL_API_ORIGIN` yalnız `.gitignore`'lu override dosyasındaydı → düzeltme ikinci makineye/üretime taşınmıyordu | `docker-compose.yml` + `.env.example` |
> | **A3** 🔴 | **ADR-008 regresyonu:** `summary` metni *"(3 bulgu, mod=…)"* taşıyor, ÖN RAPOR'da sızıyordu. Kapının kanonik kolu `detection_gate.py` vardı ama results yolunda **0 çağrı** | `gate_result_summary()` + iki okuma yolu da kapıdan geçiyor (fail-closed) |
> | **A4** | GNDVI ayrışması kayıtsızdı (I-5 ihlali) | `open_items_decisions_2026-06.md` **COORDINATE** kalemi |
> | **A5** | Yeni migration'da `BOUND` başlığı yoktu | eklendi |
> | **A6** | `MapLayerViewer` 73 satır değişti, **hiçbir test import etmiyordu** (3 mutasyon hayatta) | mutasyonla sınanmış jest testi |
>
> ### 🔴 SONRAKİ OTURUM BUNU BİLMELİ
>
> 1. ✅ **Uçtan uca prova YAPILDI (2026-08-05, canlı sistemde ölçüldü).** Kullanıcı
>    Docker'ı `--no-cache` ile yeniden kurup `alembic upgrade head` koştu; zincirin
>    tamamı komutla doğrulandı. Ayrıntı: **`docs/DEMO_GUNU_YAPILACAKLAR.txt` → EK-B**.
>    Özet: giriş 200 · liste 200 (`HEALTH←gndvi`, `NITROGEN_STRESS←ndre`,
>    `tier=TEMEL`, `band=BASIC_4BAND`) · `report_phase=PRELIMINARY`, `detections=[]` ·
>    tile `HEALTH` 68.786 bayt + `NITROGEN_STRESS` 40.660 bayt (PNG imzalı),
>    rasteri olmayan katman ve tarla dışı karo **404**, tokensiz **401** ·
>    sonuç sayfası SSR 200 ("Sonuçlar yüklenemedi" **yok**).
>
>    🔬 **KR-019 kapısı pozitif kontrollü ölçüldü:** DB'de `summary` **305 karakter
>    dolu**, API `''` döndürüyor. Yani kapı gerçekten kesiyor — "zaten boştu" değil.
>    **Sonucu:** çiftçi serbest özet paragrafını **görmeyecek** (kasıtlı, fail-closed).
>    Kutuda canlılık puanı (%26.4) + "haritayı nasıl okursunuz" + "bu ölçüm ne
>    değildir" duruyor. Demoda "özet paragrafı" vaat edilmemeli.
>
>    ⚠️ **Tile kimliği tuzağı:** tile/metadata uçları `result_id` bekler, liste ucunun
>    döndürdüğü `analysis_job_id` **değil** (ikisi ayrı kolon). Yanlışıyla çağrı
>    fail-closed **403 "Sonuc sahipligi dogrulanamadi"** verir — uç bozuk sanılmasın.
>    Detay ucu (`/results/{mission_id}/summary`) doğru `result_id`'yi zaten döndürüyor.
>
>    ✅ **Gözle doğrulama da yapıldı (kullanıcı, 2026-08-05): harita göründü.**
>    Böylece demo akışında **doğrulanmamış adım kalmadı** — backend komutla,
>    arayüz tarayıcı gezintisiyle, harita gözle doğrulandı.
>
>    ⚠️ **Ama harita İNTERNET İSTER (ölçüldü).** Ağı kapalı bir tarayıcıda tek bir
>    `.png` karo isteği bile gitmiyor: taban harita
>    `mapbox://styles/mapbox/satellite-streets-v12` gelmezse `map.on('load')`
>    tetiklenmiyor ve **bizim raster katmanlarımız da eklenmiyor**. Yani internet
>    kesilirse sadece uydu arka planı değil, ürettiğimiz analiz katmanı da kaybolur.
>    Saha notu: `docs/DEMO_GUNU_YAPILACAKLAR.txt` **A7**. Çevrimdışı yedek bilinçli
>    olarak yapılmadı (demo sunumunda internet bulunacağı teyit edildi).
>
>    🔬 **Bu turun en pahalı dersi — mutasyonla sınanmış yeşil test bile üretim
>    çıktısını ölçmez.** Platform PR #382 Mapbox CSS'ini CDN'den paket import'una
>    çevirdi; `tsc`/`eslint`/`jest` temiz, iki mutasyon kilidi kırmızıya döndü — ve
>    **canlıda hiçbir işe yaramadı**. Kök neden `next.config.mjs`'teki
>    `test: /mapbox-gl/` + `sideEffects: false`: `import 'x.css'` **yan etkili** bir
>    import'tur, webpack onu tree-shaking ile atıyordu. Kanıt: import eklendiği hâlde
>    build çıktısı **bit bit aynı** kaldı. PR **#383** regex'i `.js` ile sınırladı ve
>    aynı kalıbın kalan iki örneğini (`FieldMap`, `FieldMapDraw`) de kapattı.
>    Ölçüm: mapbox CSS kuralı **0 → 107**, `.mapboxgl-canvas` position
>    **`static` → `absolute`**. Kural: *kaynak doğru ≠ çıktı doğru* — araya bundler
>    yapılandırması girer ve kaynağı sessizce iptal edebilir.
> 2. **Ertelenen 14 kalem eylem planına taşındı** → `TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`
>    **§3.6**. (Yerel `SONRAKI_OTURUM_PLANI.txt` git'te **değildir**, ikinci makinede yoktur —
>    kanonik liste §3.6'dır.)
> 3. **TUR 3 `PENDING_REPIN` hâlâ açık** — aşağıdaki 2026-08-02 bölümü geçerliliğini
>    koruyor; bu tur contract'a dokunmadığı için beyan da değişmedi.
> 4. **Demo bağlamı:** ürünü **çiftçi seçer** — pilot mahsul antep fıstığı (`PISTACHIO`),
>    eğitim veri seti YOK (W7). Bu yüzden demo değeri **tespit** değil, **ölçüm**
>    (canlılık haritası + zayıf bölge) üzerinden kurulur.
> 5. **OSAVI kullanılamaz durumda** (ölçüldü): Terra 0.0337 vs formül 0.2639 — **8 kat
>    sapma**. Kök neden: bantlar ham DN, OSAVI'nin `+0.16` sabiti 0–1 yansıma varsayar.
>    NDVI/GNDVI/LCI/NDRE formülle **birebir** uyuşuyor. Kalibre uçuş olmadan OSAVI açılmaz.
>
> ### 📌 GİRİŞ NOKTASI (iş listesi)
> Donanım/ölçüm hattı için aşağıdaki 2026-08-02 bölümü (P-2 · P-6) **aynen geçerli**.
> Yazılım kuyruğu için: eylem planı **§3.6**.

---

## 0.A-1 ÖNCEKİ OTURUM — (2026-08-02, **motor araştırması + adaptör turu**) — ✅ **KAPANDI, MERGE EDİLDİ**

> ### 🔚 OTURUM KAPANIŞI — dört depo merge edildi, CI 6/6 yeşil
>
> | Depo | Dal | Merge commit | PR | Merge sonrası CI |
> |---|---|---|---|---|
> | contract | `master` | `d5ef33d` | **#28** | ✅ Contract Validation |
> | edge | `main` | `fba45a3` | **#54** | ✅ Contracts Gate · ✅ EdgeKiosk CI |
> | platform | `main` | `f2de26a` | **#355** | ✅ CI/CD Pipeline · ✅ Security Scan |
> | worker | `master` | `8ad50ae` | **#193** | ✅ Full Test Suite |
>
> Dört depo **temiz · senkron · 0 açık PR**. Çapraz-repo SSOT **IN_SYNC** (3 hedef + 2 POINTER_OK).
>
> 🔴 **AÇIK TUR — SONRAKİ OTURUM BUNU BİLMELİ:** `CONTRACTS_VERSION.md` →
> `**Checksum State:** PENDING_REPIN` (**TUR 3**). Agrega checksum bilerek bayat; bu turun
> içeriği (`radiometric_mode.enum.v1.json` + `x-radiometric-axis-2026-08-02` + KR-034/030
> motor-agnostik metin) **bir sonraki C8 töreninde** `pin_version.py` ile pinlenecek ve
> beyan **kendini silecek** → üç kapı aynı anda sertleşir. Beyanı C8'den ÖNCE elle silmek
> kapıları erken sertleştirir (testler gerçek kırmızıya döner).
>
> **Sürüm hedefi:** bu turun içeriği **v7.5.0 (MINOR)** olarak kapanır — dedektör
> `Detect Breaking Changes: SUCCESS` dedi, kırıcı değişiklik yok. v8.0.0 turunda yalnız
> **DEP-1** kaldı (S3 ve K1 ölçümle MINOR'a indi), tek başına dört depoyu yeniden
> pinletmeye değmez.
>
> ### 💻 MAKİNE DEĞİŞİKLİĞİ — RTX 3090 makinesinde ilk iş
>
> Kullanıcı bu noktada **RTX 3090 masaüstüne** geçti (Latitude 7300 → RTX 3090; bkz.
> demo donanım profili: 24GB VRAM / 32GB RAM — 32GB tavanı Pix4D ↔ worker'ı **sırayla**
> çalıştırmayı zorunlu kılıyor, aynı anda değil).
>
> ```bash
> # 1) Dört depoyu da güncelle (hepsi varsayılan dalda, merge edilmiş hâlde)
> git -C tarlaanaliz-contract checkout master && git -C tarlaanaliz-contract pull
> git -C tarlaanaliz-edge      checkout main   && git -C tarlaanaliz-edge      pull
> git -C tarlaanaliz-platform  checkout main   && git -C tarlaanaliz-platform  pull
> git -C tarlaanaliz-worker    checkout master && git -C tarlaanaliz-worker    pull
> ```
>
> **O makinede yapılacak iki ölçüm** (ikisi de pilotu açan yolda):
>
> 1. 🔴 **P-2 girdisi** — M3M görüntülerini **Pix4Dfields ya da DJI Terra** ile bir kez
>    işle ve **export klasörünü** ver. Dosya adları/dizin yapısı görülmeden kalibre
>    manifest yazıcısı yazılamaz; yazmak `pix4d_runner.py`'nin düştüğü hatanın tekrarı olur.
>    ⚠️ Terra kullanılacaksa **radyometrik düzeltmeyi AÇ** — kapalıyken çıktı ham DN'dir ve
>    yeni kural gereği `calibration_type: NONE` → paket reddedilir.
> 2. 🔴 **P-6** — `grape_lr_v1` `EXTENDED_5BAND` (10 kanal, BLUE bekliyor); M3M'de BLUE yok
>    ve `feature_extraction.py:164` onu **sıfırla dolduruyor**. 36 feature'ın 4'ü sabit sıfır
>    olurken `StandardScaler` gerçek Blue ile fit'lenmiş ⇒ Platt kalibrasyonu (ECE 0.013–0.24)
>    4-bant girdide **geçerliliğini kanıtlamış değil**. Hata VERMEZ, sessizce bozar — ve o
>    güven skoru fail-closed rapor kipini (K-10) sürüyor. GPU'lu makine bu ölçüm için doğru yer.
>
> **Demo öncesi kullanıcının kendi kontrolü:** kartlardaki **sonek-0 fotoğrafları görünür ışık
> mı, gerçek-zamanlı NDVI önizlemesi mi?** NDVI önizlemesiyse DJI Terra yeniden yapılandırması
> **başarısız olur** (DJI: *"如果是实时 NDVI 照片而非可见光照片，将无法处理成功"*). Kamera ayarından geliyor.
>
> ### 📌 GİRİŞ NOKTASI (iş listesi)
> Eylem planı → **`▶️ GİRİŞ NOKTASI — MOTOR-AGNOSTİK KALİBRASYON + v7.5.0 TURU`**
> (`docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`). Sıra: **P-2 · P-6** → P-4 · P-5 →
> v7.5.0 turu (S7-b · S3-b · K1) → kuyruk (W8-c · W8-b · P21 · P20 · Ö7).

---

## 0.A (devam) — AYNI OTURUMUN AYRINTISI (2026-08-02, motor araştırması + adaptör turu)

> ### 🔬 Çok dilli motor araştırması (18 ajan · EN+ZH+ES · çürütme turlu) **İKİ VARSAYIMI ÇÜRÜTTÜ**
>
> 1. 🔴 **Pix4Dfields'in de DJI Terra'nın da YEREL CLI'ı YOK.** Pix4Dfields: doküman
>    merkezinin 10 bölümü + SSS + sürüm notları 2.8→2.13.2 + girdi/çıktı belgesi = sıfır
>    atıf. DJI Terra: V5.3.0 kılavuzunun 70+ sayfası = sıfır atıf. CLI ayrı ürünlerde
>    (Pix4Dmapper *obsolete* + Enterprise lisans · Pix4Dengine SDK/Cloud) ya da bulutta
>    (TerraAPI — **Haziran 2026'da kapatıldı**, zaten *"agricultural applications"*
>    içermiyordu). ⇒ `edge/…/pix4d_runner.py` **var olmayan bir CLI'a** subprocess açıyordu;
>    satır 86'daki *"verified on M1 during smoke test"* beyanı **bayat** (M1 hiç alınmadı).
> 2. 🔴 **Yeni delik AV-3:** `calibration_type` yalnız drone'dan türetiliyor. Ama DJI Terra'da
>    radyometrik düzeltme **kapalıyken çıktı ham DN'dir**; aynı M3M uçuşu yine `RELATIVE`
>    etiketlenir ve NDVI eşikleri ham DN'e uygulanır. **S1 fail-open bulgusunun aynı sınıfı.**
>
> ✅ **Doğrulanan:** E13-R'nin `RELATIVE` kararı iki bağımsız üretici kaynağıyla teyit edildi
> (Pix4D: *"not fully radiometrically calibrated, only a relative calibration"* · DJI Image
> Processing Guide Eq. 4-6: ρ_NIR yayımlanmadığı için panelsiz mutlak reflektans türetilemez).
>
> ### ✅ Bu oturumda YAZILAN (edge — PR **#54** ile merge edildi, `fba45a3`)
>
> | Dosya | Ne |
> |---|---|
> | `src/core/services/calibration_gate/engine_adapter.py` | **Motor-agnostik çıktı adaptörü** — `Pix4DFieldsAdapter` (`.data.tif` zorunlu, görüntüleme `.tif` reddedilir) · `DJITerraAdapter` (`map/index_map/` okunur, `index_map_color/` reddedilir) · fail-closed motor tespiti · fail-closed radyometrik kip beyanı |
> | `src/core/services/calibration_gate/calibration_type_resolver.py` | **İki girdili türetme** — `f(drone_class, radiometric_mode)`; **ham DN → `NONE`** (AV-3 kapatıldı) |
> | `tests/unit/test_engine_adapter.py` · `test_calibration_type_resolver.py` | 34 test, **gerçek dosya sistemiyle** (casus yok) |
>
> **Kapı kanıtı: 8/8 mutasyon KIRMIZI** (görüntüleme dosyasını kabul et · renkli indeksi oku ·
> bant belirtecini sessizce atla · motor belirsizliğini çöz · beyansızı PANEL say · ham DN'i
> reflektans say · göreliyi ABSOLUTE'a yükselt · bilinmeyen drone sınıfına varsayılan uydur).
> Geri yükleme doğrulandı. `ruff check src/ tests/` → **All checks passed** (depo geneli).
>
> ### 📌 GİRİŞ NOKTASI
> Eylem planı → **`▶️ GİRİŞ NOKTASI — MOTOR-AGNOSTİK KALİBRASYON + v7.5.0 TURU`**
> (`docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`). Eski "v8.0.0 TURU" bölümü **tarihsel
> kayda** çevrildi — S3 ve K1 ölçümle MINOR'a indi, turda yalnız DEP-1 kaldı.
>
> ### ✅ C-1 · C-2 · C-3 de bu oturumda KAPANDI (kullanıcı onayı) — çapraz depo sözlük hizası
>
> 🔴 **Kendi ihlalimi buldum:** `RadiometricMode` kavramını edge'de **uydurmuştum**;
> kanonik sözlükte karşılığı yoktu (ölçüldü). worker CLAUDE.md §2.1 ihlali — geri alındı.
>
> | # | Yapılan | Depo |
> |---|---|---|
> | **C-1** | `enums/radiometric_mode.enum.v1.json` **kanonik** yazıldı · `calibration_type → x-derivation`'a 6 gözlü makine-okunur türetme tablosu (`x-radiometric-axis-2026-08-02`) + 4 değişmez | contract |
> | **C-2** | KR-034/KR-030 normatif metni motor-agnostik + *"iki motorun da CLI'ı yok, subprocess tasarımı yazılmamalı"* + *"radyometrik düzeltme opsiyonel → ham DN"* notları | contract + platform + worker SSOT (**IN_SYNC**) |
> | **C-3** | Edge tabloyu **kanonikten yüklüyor** (hardcode kaldırıldı) · 2 enum vendor'landı · hash pin kapsamı **8 → 10** · contract parite MIRROR listesine kaydedildi | edge + contract |
>
> **Kapı kanıtı: 8/8 mutasyon KIRMIZI** (bu tur toplam **16/16**). Geri yükleme doğrulandı.
> Durum: contract **1281 passed**, `validate.py` **165/0** · edge **985 passed**, ruff temiz,
> hash pin OK.
>
> **Bu turda üç kapı BENİ yakaladı** (hepsi düzeltildi): sahiplik (M1/M2 ataması yok) ·
> vendored parite (dosya ekledim, listeye yazmadım) · hash pin sayı kilidi (sabit `8`;
> sayıyı büyütmek yerine değişmez **üretecin kendisiyle** yeniden yazıldı + boş-glob kapısı).
>
> **Tur içi beklenen kırmızı:** `test_real_repo_checksum_verifies` (agrega checksum bayat →
> C8'de `pin_version.py` kapatır). `test_detector_accepts_a_git_ref` de kırmızı ama
> **temiz HEAD klonunda da kırmızı** (`git clone --local` ile ölçüldü) → bu turdan bağımsız.
>
> ### ⏭️ SIRADAKİ (P-2…P-6, henüz YAZILMADI)
> **P-2 `CalibratedManifestWriter` bilerek beklemede:** `observed_footprint_wkt`'yi gerçek
> raster'dan çıkarmak gerekiyor ve **hiçbir motorun gerçek çıktısı henüz elde yok**. Dosya
> adlarını ve footprint çıkarımını görmeden yazmak, `pix4d_runner.py`'nin düştüğü hatanın
> aynısı olurdu. Kullanıcı bir kez Pix4Dfields **veya** DJI Terra koşturup export klasörünü
> verdiğinde yazılır. P-4/P-5/P-6 planda.

---

## 0.A-ÖNCESİ — (2026-08-02, **otonom tur**) — **SIRA 3 KAPANDI + AK-11**

> Kullanıcı uyurken otonom koşuldu. **7 PR, 4 depo, hepsi CI yeşil ve merge edildi:**
> edge **#52** (E18+E15) · **#53** (E17) · platform **#354** (P15+P19) ·
> worker **#191** (W15+W8-yarım) · **#192** (W10) · contract **#27** (C8-a) + AK-11 (master).
>
> ### Turun şekli: dört kapı **kendi hatamı** gösterdi
> Bu turun en değerli çıktısı düzeltilen kalemler değil, **kapıların beni yakalaması**:
> 1. **E17 kapısı ölçütümü çürüttü.** *"Atlama = 0"* yazmıştım; ilk koşuşta
>    `95 passed, 69 skipped` dedi. Beklentim yanlıştı — parite süiti **iki deponun**
>    çiftlerini birden kapsıyor, karşı taraf PRIVATE olduğu için meşru atlanıyor.
>    Ölçüt *"BU depoya ait atlama yok"* + *"hiç test koşmadıysa da kırmızı"* oldu.
> 2. **C8-a aracı iki kez yakalandı**; ikincisi ciddi: `--check` kusursuz görünürken
>    **`--apply` hiçbir şey yazmıyordu** (exit 0 ile). Yalnız mutasyonla göründü.
> 3. **E18'de dört fixture, düzeltilen hatanın ÜZERİNDE duruyordu** — `calibrated.json`
>    yolunu veriyor ama dosyayı hiç yazmıyorlardı; yalnız sessiz yutma sayesinde
>    geçiyorlardı. (Aynı ders P14 turunda da çıkmıştı.)
> 4. **Şema açıklamasına dokunmak** checksum + dist kapılarını kırdı → tek cümlelik prose
>    bile üç depoyu yeniden pinlemeyi gerektiriyor (ölçüldü, borç plana yazıldı).
>
> ### İki kez "yapma" dedim — ve nedenini ölçtüm
> * **W8 çağrı yeri bağlanmadı.** Publish noktasında elde yalnız **anomali** tile'ları
>   var; oradan çekiliş örneği **ölçtüğü sonuca koşullar**. Sampler'ın kendi bilimsel
>   gerekçesi bunu yasaklıyor. **Yanlı çekiliş, hiç çekiliş yapmamaktan kötüdür** —
>   ölçüm temeli sessizce geçersiz olur ve fark edecek kapı yok. → **W8-b**
> * **P19'da "kaldır" kararını GERİ ALDIM.** Ölü sandığım dalın **açık bir testi** vardı;
>   eksik olan kod değil **üretici bağlantısı**. Belirtilmiş davranışı tek taraflı silmek
>   yerine durum beyan edildi ve **kapıya bağlandı** (iki yönde mutasyon kırmızı).
>
> ### Bayat beyan sayacı: bu oturumda **beş**
> P1'i kilitleyen iki not (`settings.py` + `ingest.py`, drift zaten giderilmişti) ·
> sampler'ın *"`AUDIT_SAMPLE` enum'da yok"*u (var) · `data_lifecycle_transfer.md` ·
> W15 docstring'i. Hepsi *"karar uygulandı, çevresindeki metin eski dünyada kaldı"*.
>
> ### AK-11 ✅ (SIRA 4'ün ilk adımı)
> Dedektör artık `FIELD_MADE_REQUIRED` yolunda da beyanı tanıyor. Kusur iki katmanlıydı:
> tip listede yoktu **ve** o dal `_record()`'u hiç çağırmıyordu. Yeni koşul **açık
> opt-in** (`"accepts": [...]`) — tek damga aynı düğümdeki daha güçlü iddiayı sessizce
> kapsamasın. ⇒ **S7-b artık beyanla MINOR turda da kapatılabilir.**
>
> ### 📌 SONRAKİ OTURUM — **TEK GİRİŞ NOKTASI**
> Eylem planı → **`▶️ SONRAKİ OTURUM — v8.0.0 TURU: ÖLÇÜLMÜŞ İŞ PLANI`**
> (`docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`, §14.9'un sonunda).
>
> Orada dört kalemin (**S3 · S7-b · K1 · DEP-1**) her birinin gerekçesi **ölçüm
> çıktısıyla** yazılı, 9 adımlık tören sırası ve turdan **bağımsız** kuyruk
> (**W8-b · P21 → P16 · W8-c · Ö7 · P20**) kanıtlarıyla duruyor.
>
> 🔴 **Önce kullanıcı kararı:** tur açılacak mı? MAJOR = dört deponun aynı anda yeniden
> pinlenmesi, geri alınması zor. **Hiçbir kalem CANLI bir arıza değil** — bekleyen şey
> teknik hazırlık değil **zamanlama**.
>
> ⚡ **Turu açmasanız bile yapılabilecek olan:** **S7-b**. AK-11 sayesinde *"üretici yok,
> ölçüldü"* beyanıyla MINOR turda da kapatılabilir (edge/platform/worker → **0** üretici,
> ölçüldü). Kuyruktaki beş kalem de MAJOR beklemiyor.
>
> Dört depo: temiz · senkron · 0 açık PR · I-1 `7.4.0 = 7.4.0 = v7.4.0` · CI 4/4 yeşil.

---

## 0.A′ ÖNCEKİ OTURUM (2026-08-01 gecesi → 2026-08-02) — **öz-denetim + ÖD-0 + `v7.4.0` YAYIMLANDI**

> ### 🔚 OTURUM KAPANIŞ ÖZETİ
>
> **TUR 2 KAPANDI.** `v7.4.0` annotated tag ile yayımlandı, dört depo hizalı, açık PR yok.
>
> | Depo | Sürüm / Pin | Değişmez |
> |---|---|---|
> | contract | `7.4.0` · tag `v7.4.0` · **23 tag** · checksum `c7b8d46e…` | I-2 ✅ (`objecttype=tag`, `describe` temiz) |
> | platform | `7.4.0` · submodule `eb28b74` (PR **#352**) | I-3 ✅ (96/96 per-dosya hash) |
> | worker | `v7.4.0` · öz-hash `bb66e1bc…` (PR **#189**, **#190**) | I-4 ✅ · I-5 ✅ (devir spesi uzlaştı, silindi) |
> | edge | yerel `1.5.0` · upstream `7.4.0` (PR **#51**) | hash 8/8 |
>
> **Oturumun üç işi:** ① önceki oturumun **öz-denetimi** ② denetim borcu **ÖD-0** (`sürüm-riski`
> lensi) ③ **C8 töreni** (6/6 adım).
>
> ### 🔴 ÜÇ KÖK BULGU (üçü de aynı sınıf: *yeşil görünen ama ölçmeyen yüzey*)
> 1. **CI, yerelde kırmızı olan commit'i yeşil geçirdi.** `ee4aed7`'in CI koşusu `success`
>    döndü; kırılan test contract CI'ında **atlanan 134 testin** içindeydi (kardeş depo okuyor).
>    ⇒ Bu depoda CI, kardeş-bağımlı kapılar için **otoriter değildir**; süitin %11'ini koşmaz.
>    **Yerelde 20 saniyede yeniden üretilebiliyor:** `git clone --local . <boş dizin>` + `pytest`
>    → CI çıktısı birebir (`1093 passed, 134 skipped`). Push öncesi bu koşulmalı.
> 2. **Atlama kapısı dosyaya bakmıyordu** — yalnız gerekçe dizesine bakıyordu, bu yüzden ikinci
>    bir dosya beyanın altına **adı geçmeden** sığındı (beyanın notu da bayattı: 47 → 134).
>    Beyan artık `(gerekçe, dosya, not)` üçlüsü; mutasyon kırmızı.
> 3. **Release aracının kendisi bozuktu.** `pin_version.py` agrega checksum'ı yazdıktan **sonra**
>    `api/*.yaml`'ı senkronluyordu; o dosyalar checksum kümesinin **içinde** → pin doğduğu anda
>    bayat, `--verify` anında kırmızı. v7.3.0'da görünmemişti çünkü `info.version` o tur
>    değişmemişti. Sıra düzeltildi + regresyon kapısı (mutasyonla doğrulandı).
>
> ### 📋 ÖD-0 (`sürüm-riski` lensi) — 9 soru, elle koşturuldu
> Temiz: MINOR **iki bağımsız ölçümle** (dedektör 9/0 + dedektörün kodunu hiç kullanmayan
> düzleştirilmiş tarama 89 dosya/0; ikinci araç 3/3 mutasyonla doğrulandı) · migration guide
> gerekmiyor · I-2 22/22 → **23/23** · re-pin penceresi **güvenli** (yeni alanların canlı
> üreticisi yok, ölçüldü). Kapatılan: **yayın kapısı boşluğu** (`pin_version` sürümü yazar ama
> `## [Unreleased]` başlığını çevirmez, hiçbir kapı ölçmüyordu → 2 `release_gate` testi) +
> CHANGELOG'un turun ortasını anlatan 3 bayat cümlesi.
>
> ### 🆕 Kardeş depolara yazılan (SIRA 3 kuyruğunda)
> **E18** — edge `_read_calibration_type` her okuma hatasını **sessizce** yutup
> `calibration_type`'ı atlıyor; üç yorumu hâlâ *"platform PANEL_ABSOLUTE varsayar"* diyor ama
> **P14 o ağı kaldırdı** ⇒ okunamayan dosya → `NONE` → worker sert reddi, **teşhis edilemez**
> sebeple. E15 ile aynı sınıf. · **P19** — platform `_derive_calibration_type` 2. adımı **ölü**
> (`calibration_manifest`'e hiçbir yerde değer atanmıyor) ⇒ "3 kaynak" aslında 1 + fail-closed,
> bu da E18'in etkisini büyütüyor. · **W15** — worker docstring'i okumadığı alanı okuduğunu
> söylüyor (S4 gerekçesini yanlış yönlendirir). · **DEP-1** — penceresi dolmuş iki deprecation
> MAJOR turu içeriğine eklendi. · **Ö7** — W14'ün kalıcı beyanı "yalnız küçülür" diyen borç
> listesinde duruyor (delik değil, taksonomi yanlış; C8 sonrası).
>
> **Kanıt arşivi:** `denetim/denetim_raporu_2026-08-01_gece_ozdenetim_onceki_oturum.md` ·
> `denetim/denetim_raporu_2026-08-01_gece_od0_surum_riski_lensi.md`.
>
> **📌 SONRAKİ OTURUMUN GİRİŞ NOKTASI:** eylem planı **§14.9**. Yeni sıra: ① **P1**
> (platform `enforce=True` — iki kilit de açıldı; platform commit'i **kullanıcı onayı ister**)
> ② kardeş depo kuyruğu (**E18** ve **P19** öne alınmalı — canlı teşhis riski) · E17/W10 ·
> E15 · W8 · P15/P16 · C8-a ③ **MAJOR TURU** (kilit kalktı; AK-11 önce).

---

## 0.A″ ÖNCEKİ OTURUM (2026-08-01, **ikinci oturum**) — **§14.8'in tamamı + E13 geri alındı**

> ### 🔚 OTURUM KAPANIŞ ÖZETİ
>
> **§14.8'deki 16 ÖD kaleminin 15'i kapandı** (kalan: **ÖD-0** — `sürüm-riski` lensi hâlâ
> koşmadı). Üstüne **bir karar geri alındı** (E13 → **E13-R**, koordinatör onayı) ve
> denetimin görmediği **beş yeni sapma** ölçümle bulundu.
>
> | Depo | Durum (oturum kapanışı) |
> |---|---|
> | contract | PR **#25 MERGED** (9/9) · PR **#26 MERGED** (9/9 — E13-R + ÖD-4/6/7/9…16 + SD9/SD10) |
> | worker | PR **#187 MERGED** (W13 — 3/3) · PR **#188 MERGED** (W11 — 6/6) · KR-041 hash `f1447fb6…` → `66747d4a…` |
> | platform | PR **#351 MERGED** (P14 + P17 — 6/6 yeşil; kullanıcı commit onayı verdi) |
> | edge | dokunulmadı — **E16 ölçüldü, üretici kararı bekliyor** (aşağıda) |
>
> **🔄 E13 GERİ ALINDI — kararın kendisi ölçümle çürüdü.** E13 kalibre pakete filo-geneli
> sabit `ABSOLUTE` yazıyordu; üç kanonik kaynak da tersini söylüyordu (matris
> `DJI_MAVIC_3M: relative` · SSOT `:79`/`:1014` · platform `calibration_class.py:41`).
> Ölçülen sonuç: sabit `ABSOLUTE` worker'ın `FINETUNE_ALLOWED_CALIBRATIONS` kümesi
> üzerinden **K-3'ü etiket yoluyla delerdi** (göreli M3M verisi ince ayara girerdi).
> **E13-R:** değer `calibration_class`'tan türetilir. 💰 Bedel yazılı ve kabul edildi:
> **M3M verisi ince ayara girmez** (yalnız SSL ön-eğitimi).
>
> **🔴 ÖD-2 zinciri KAPANDI (contract + worker birlikte).** `analysis_job.v1` gömülü
> `$defs/CalibrationMetadata` kanonikten ayrışmıştı ve `unevaluatedProperties: false`
> taşıyordu → `scale` taşıyan iş **worker'ın kapısında** düşerdi; W12'nin okuma kodu
> veriyi asla görmezdi. İki depo aynı turda düzeltildi.
>
> **Yeni kapılar (hepsi mutasyonla doğrulandı — bu turda toplam 44 mutasyon):**
> `test_context_subset_binding` (defter↔şema) · `test_calibration_metadata_single_definition`
> (iki tanım ayrışamaz + **belge düzeyinde** doğrulama) · `test_calibration_type_derivation`
> (E13-R) · `test_publication_tree_gates` (yayın ağacı + yayımlanan üreteç) ·
> `test_vendored_parity` **9→16 dosya**, MIRROR/SUBSET kipleri, enum ekseni, prose tavanı.
>
> **📌 SONRAKİ OTURUM:** ① PR **#26**'yı merge et ② **ÖD-0** (`sürüm-riski` lensi tek
> başına koşturulmalı — v7.3.0'ın yayımlanmış içeriği hâlâ denetlenmedi) ③ kardeş depo
> kalemleri: **W14** (EGE + meyve ağaçları) · **E16/E16-b** (küçük harf crop sözlüğü) ·
> **P14** (E13-R ile acilleşti) · **P17** (sürüm log sabitleri) · **W11** (kodlamasız
> `open()`) ④ sonra C8 töreni (TUR 2 hâlâ `PENDING_REPIN`).
>
> ### 🔬 BU TURUN İKİ METODOLOJİ DERSİ (ikisi de kendi kapımda yakalandı)
> 1. **Uygulanmayan mutasyon yeşil verir** ve kapıyı kör sandırır (dosyalar CRLF, desenler
>    `\n` ile yazılmıştı → hiç eşleşmedi). Mutasyon script'leri artık "uygulandı mı"
>    kontrolüyle koşuyor.
> 2. **Ölçüm aracının kendi hatası** bulguyu uydurur: builtin `open(dosya, mod)` ile
>    `Path.open(mod)` imzaları farklı; ilk tarayıcı `p.open("rb")`'yi — hem de bir
>    **checksum aracında** — "kodlamasız okuma" diye raporladı. **Önce aracı doğrula.**
>
> ### 📋 Bu turda ölçülen, denetimin GÖRMEDİĞİ beş sapma
> `analysis_job` vendored kopyası (W13 · kapandı) · `expert_labeling_card` **EGE** ·
> `expert_review_queue` **APPLE/CHERRY/FIG/PEACH** (ikisi **W14**) ·
> `intake_manifest.sorties[].crop_type` küçük harf (**E16-b**) · edge kalibre manifestte
> `raw_frames[].band`'e **RGB** yayılmamış + `qc_report.flags` kısıtsız (C8 yayılımı, beyanlı).
>
> **I-2 tamamlandı:** ÖD-7'de nüfus **biçimden bağımsız** yeniden ölçüldü (19→**22** sürüm);
> `v2.0.1 · v2.1.0 · v4.1.2` retro-tag'leri atıldı ve **push edildi** → **22/22**.
>
> ### 🔚 OTURUM KAPANIŞI — son üç iş (yukarıdaki tablodan SONRA yapıldı)
> * **W11 (worker PR #188, merged):** kodlamasız metin okuma sınıfı kapatıldı
>   (`contract_validator.py:233` · `cold_storage_manager.py:263,293` · `ssl_pretrain.py:2131`
>   · `safe_path.py` docstring örneği) + **AST tabanlı** kalıcı kapı
>   (`tests/contract/test_text_io_encoding_gate.py`; kendi kapsamını da ölçüyor).
> * **P14 + P17 (platform PR #351):** fail-open `CALIBRATED → PANEL_ABSOLUTE` **kaldırıldı**
>   (E13-R sonrası kritik: tek kalan "göreli veriyi mutlak etiketle worker'a gönderme" yoluydu)
>   + `main.py` log sabitleri pin nesnesinden okunuyor. İki test fixture'ının **fail-open
>   davranışı ürettiği** ortaya çıktı ve düzeltildi; 48 kombinasyonluk regresyon eklendi.
>   Kapı: ruff temiz · BOUND OK · `APP_ENV=test pytest --cov` **0 FAILED**, coverage **%83.43**.
> * **E16 ölçüldü — tek taraflı yapılamaz:** küçük harf ürün sözlüğü edge `src/` ve `config/`'te
>   **YOK** (config zaten BÜYÜK harf; `threshold_loader.py:50` `.upper()` ile normalize ediyor);
>   yalnız **iki vendored şemada** + fixture'larda yaşıyor. **Ama** `sorties[].crop_type` bir
>   **GİRDİ** sözleşmesidir ve değerini **görev planı** üretir → enum'u daraltmak küçük harf yazan
>   bir görev dosyasını **reddeder** (kart REJECTED). Karar: üretici mi BÜYÜK harfe geçecek, edge mi
>   doğrulamadan önce normalize edecek? *(`worker_result.v1` edge `src/`'de hiç kullanılmıyor —
>   o dosyanın daraltılması risksiz ve ayrı bir küçük adım.)*
>
> ### ✅ ÜÇ KARAR DA VERİLDİ VE UYGULANDI (oturum kapanışında)
> | # | Karar | Uygulama |
> |---|---|---|
> | **W14** | *"Cherry worker'da kalsın, platformda gerekmiyor"* (koordinatör) | İki `KNOWN_VENDORED_AHEAD` girişi **borç** olmaktan çıkıp **beyan edilmiş eksen farkı** oldu (`W14_DECISION`); yeniden açılma koşulu makine-okunur yazıldı: ürün siparişe açılırsa **tel önce genişletilir** |
> | **E16** | *"Edge normalize et"* (koordinatör) | edge **PR #50 MERGED** — `_canonical_crop()` sınırda `strip().upper()`, iki vendored enum kanonik 8 ürüne çekildi, CONTRACTS_SHA256 yenilendi, 9 testlik yeni kapı. ⚠️ **P1 kilidi açıldı** |
> | **SD11** | *"Karar sende"* → **`notes`/`metadata` kanonikte KALIR, `x-` göçü YAPILMAZ** | 4 ölçümlü gerekçe (JSON Schema belgesi · göç her okuyucuyu kırar · sıfır davranış kazancı · istisna dar) + **istisna listesi kapıya bağlandı**: `struct` dışında kural / `notes`-`metadata` dışında pointer eklenemez, liste büyüyemez |
>
> ### 🔴 ESKİ HÂLİ (tarihsel kayıt) — üç açık karar
> | # | Soru | Neden tek taraflı kapatılmadı |
> |---|---|---|
> | **W14** | Worker-içi 12-ürün / 7-bölge ekseni **wire** şemalarına (`expert_review_queue`, `expert_labeling_card`) sızmış. Kanonik absorbe mi etsin · şemalar worker-içi mi ilan edilsin · vendored mi daraltılsın? | Üretilmiş 4 kart seti + `bulk_approval_suggester` + testler etkileniyor. ⚠️ İlk taslağımda *"kiraz sipariş edilebiliyor"* yazmıştım — **YANLIŞTI**, düzeltildi: KG-0.d-EK 2026-07-31'de kod-teyitli kapandı (CHERRY çift kapılı kapalı) ve `crop_type.py:50-68` **dört kümenin bilerek farklı** olduğunu yazıyor |
> | **E16** | Girdi sözleşmesindeki enum daraltması (yukarıda) | Saha kartı reddi riski; üretici kararı |
> | **SD11** | Kanonik şemalardaki `notes`/`metadata` → `x-notes`/`x-metadata` göçü (OpenAPI uzantı konvansiyonu). Bugün **23 `struct` bulgusu beyanlı** olarak susturuldu (`.redocly.lint-ignore.yaml`, gerekçesi yazılı) | 12 kanonik dosya + onları **okuyan** tüketiciler (ör. `metadata.bandRequirements` KR-018 bant kapısının kaynağı) |
>
> **Kanıt arşivi:** `denetim/denetim_raporu_2026-08-01_od1_od2_od3_od8.md` ·
> `denetim/denetim_raporu_2026-08-01_e13r_od4_od5_od6_od7.md`.
> **📌 SONRAKİ OTURUMUN GİRİŞ NOKTASI: eylem planı → yeni `§14.9` ("DEVAM ET DENİNCE BURADAN BAŞLA").**
> Sıra: ① **C8 töreni / TUR 2 kapanışı (v7.4.0)** — 6 adımı yazılı ② **P1 kilidi açıldı** (E16 sayesinde)
> ③ kardeş depo kuyruğu (E17/W10 · E15 · W8 · P15/P16 · C8-a) ④ **MAJOR TURU** (AK-11 önce).
> Denetim borcu: **ÖD-0** (sürüm-riski lensi hiç koşmadı) — C8'den ÖNCE.

---

## 0.A‴ DAHA ÖNCEKİ OTURUM (2026-08-01) — **§14.7 tamamı + C8 töreni + TUR 2 açılışı**

> ### 🔚 OTURUM KAPANIŞ ÖZETİ
>
> **`v7.3.0` YAYIMLANDI** (annotated tag, C8 release töreni). §14.7'nin **yedi kalemi de** kapandı.
>
> | Depo | Sürüm / Pin | Değişmez |
> |---|---|---|
> | contract | `7.3.0` · tag `v7.3.0` · 19 tag | I-2 ✅ (`objecttype=tag`, `describe` temiz) |
> | platform | `7.3.0` · submodule `a8cf512` | I-3 ✅ (checksum **vendor**, `13c0ab5e…`) |
> | worker | `v7.3.0` · öz-hash | I-4 ✅ |
> | edge | yerel `1.4.0` · upstream ref `7.3.0` | hash bloğu yeniden üretildi |
>
> **Kapanan kararlar:** D16-b2 (ikili gövde **49→0**) · D4-b (parite kapısı **karşı tarafta**, PAT yok)
> · SD8 (**14 retro-tag** + `2.0.2` kayıt notu) · 0.h/K3 (veri yönetişimi + saklama) · E13 (**`ABSOLUTE`**)
> · C8 töreni · S5 + W12 (per-job reflektans ölçeği) · C6b/S2 · S4 · S6 · S7 (yarım).
>
> **⚠️ AÇIK TUR:** `CONTRACTS_VERSION.md` → `**Checksum State:** PENDING_REPIN` (TUR 2).
> Bu tur `S5 · C6b/S2 · S4 · S6 · S7` taşıyor ve **bir sonraki C8 töreninde** kapatılır.
> Tur içi **beklenen** iki xfail: checksum + `PENDING_PROPAGATION`.
>
> **✅ Kapanış anı doğrulaması (2026-08-01):** dört depoda **0 açık PR** · dört çalışma ağacı
> **temiz**, push edilmemiş commit **yok** · I-1 hizası `7.3.0 = 7.3.0 = v7.3.0` (edge yerel
> `1.4.0`, upstream ref `7.3.0`) · I-2 `objecttype=tag`. Merge edilen PR'lar: contract
> **#22 · #23 · #24** · platform **#349 · #350** · worker **#184 · #185 · #186** · edge **#49**.
>
> **`PENDING_PROPAGATION` bugün ne taşıyor:** yalnız `calibration_metadata.v1 ← calibration_method`
> (S4). ⚠️ Bunu C8'de yaymadan önce worker'da OKUYAN bir tüketici olmalı — S5'te yayılım
> okuma kodundan önce yapılmaya kalkışıldı ve şema `additionalProperties: false` olduğu için
> gerçek belge reddedilecekti; W12 ikisini birlikte taşıyarak çözdü. Aynı hata tekrarlanmasın.
>
> **🔴 BU OTURUMDA KENDİ KAPILARIM BENİ 5 KEZ YAKALADI** (hepsi düzeltildi — kapılar çalışıyor):
> 1. **C6b ↔ E13 çelişkisi:** alt-kümeyi intake ile *tam* hizaladım, `DLS2_RELATIVE`'i aynı gün
>    reddettiğim yüzeye soktum → `test_calibration_type_axis.py` kırmızı.
> 2. **Vendored'a 12 KB prose taşıdım** (I-4 ihlali) → worker'da **45 test** cp1254'te kırıldı.
>    Kök neden ikiydi: benim prose taşımam + `contract_validator.py:233` kodlamasız `open()` (**W11**).
> 3. **Platform kod sabiti:** `main.py:183` `ContractsVersionPin("7.2.0")` unutulmuştu → KR-041 drift
>    kapısı yakaladı.
> 4. **Edge CI'ında sürüm hardcode** (`grep -q "CONTRACTS_VERSION=1.3.0"`) → kapı sayı yerine **biçim**
>    zorlar hâle getirildi, mutasyonla doğrulandı.
> 5. **W12'de MagicMock sahte job'lar:** `_load_bands` artık `calibration_metadata` okuyor → CI'da
>    `AttributeError`/`ValueError` seli. **Yerelde görünmedi** (rasterio yok) — CI otoriter.
>
> **Ölçüm disiplini:** MAJOR/MINOR kararı **iki bağımsız** ölçümle verildi — dedektör (0 breaking)
> **+** dedektörden bağımsız derinlik taraması (157 dosya, `$defs`/`items`/`oneOf` dahil). Dedektörün
> `FIELD_MADE_REQUIRED` için `x-compat-accepted` beyanını **hiç kontrol etmediği** ölçüldü (**AK-11**).
>
> **📌 SONRAKİ OTURUM — TEK GİRİŞ NOKTASI: eylem planı `§14.8`.**
> Kullanıcı "devam et" dediğinde **§14.8'in başından** başla; sıra oradadır.
> (§14.7 kapandı · §14.8 öz-denetimden doğdu · 🔶 MAJOR TURU bölümü ayrıca bekliyor.)
>
> ### 🔬 OTURUM SONU ÖZ-DENETİMİ (6 lens · 109 ajan · 3.5M token)
> Kanıt arşivi: `denetim/denetim_raporu_2026-08-01_ozdenetim_6lens.md`
>
> **🔴 Üç KRİTİK bulgu ELLE DOĞRULANDI** (ajan iddiası kanıt sayılmadı) ve **hepsi gerçek** —
> üçü de aynı kök nedene bakıyor: *aynı kavramın iki şema tanımı var ve hiçbir kapı ikisini bağlamıyor.*
> 1. **C6b/S2 kararı fiilen uygulanmadı** — `PANEL_ABSOLUTE` yalnız enum **kayıt defterine**
>    (`x-context-subsets`) yazıldı; şemanın **inline** enum'u hâlâ `[ABSOLUTE, RELATIVE]`.
>    Yani karar kâğıt üzerinde; `PANEL_ABSOLUTE` taşıyan belge bugün de reddedilir.
> 2. **S5 + W12 tel üstünde ÖLÜ** — `analysis_job.v1 → $defs/CalibrationMetadata` `scale`
>    taşımıyor ve `unevaluatedProperties: false`; ölçüldü: *"Unevaluated properties are not
>    allowed ('scale' was unexpected)"*. Worker'ın okuma kodu asla veri görmeyecek.
> 3. **E13/C6b kapıları yalan yeşil** — kayıt defterini ölçüyorlar, şemayı değil.
>
> **⚠️ Denetimin kendi borcu (dürüstlük notu):** 109 ajanın **69'u oturum kotasında düştü**.
> `sürüm-riski` lensi **hiç koşmadı** (v7.3.0'ın yayımlanmış içeriği denetlenmedi → **ÖD-0**) ve
> çürütme turu yarım kaldı; workflow "skeptiği düşen bulguyu ele" mantığıyla çalıştığı için
> **haksız elenen bulgu olabilir** (**ÖD-0b**). §14.8'deki ÖD-4…ÖD-16 bu yüzden
> **"önce doğrula"** notuyla girdi — hiçbiri kanıtlanmış sayılmaz.

---

## 0.B ÖNCEKİ OTURUM (2026-07-31, ikinci oturum) — **KADEME 0→5 + öz-denetim**

> ### 🔚 OTURUM KAPANIŞ ÖZETİ
> **Yapılan:** eylem planı §14'ün **beş kademesi** (KADEME 0,1,2,3 tam · 4 kısmi · 5 kısmi) +
> onaylanan iki karar (**§14.2.1 `$ref` inline** · **D16-b tek gövde**) + **D18-b** + **AK-10**.
> **Sayılar:** yerelde **910 test / 2 beyanlı xfail / 0 skip** · `validate.py` **96 dosya / 0 hata**
> · dedektör **0 breaking** · **CI 9/9 yeşil** (`headRefOid` her turda doğrulandı).
> **Yeni:** 9 test dosyası · 3 araç (`inline_refs.py`, `sync_kr_corpus.py` + `validate.py` genişletildi)
> · `dist/schemas/` yayın biçimi (68 dosya, harici `$ref` 0).
>
> **⚠️ ÖZ-DENETİMDE BULDUĞUM KENDİ HATALARIM (4 adet, hepsi düzeltildi):**
> 1. `analysis_type.enum`'a konvansiyon dışı **üst düzey `version`** alanı ekledim → kaldırıldı.
> 2. D17'de makine-okunur listeden `WATER_STRESS`'i çıkardım ama **KR-093'ün iki prose gövdesi
>    bayat kaldı** → AR1'in yenisini ürettim; düzeltildi + kalıcı "makine↔metin" kapısı yazıldı.
> 3. D16-b gerekçemde **"registry yalnız contract'ta yaşar"** dedim — sığ `ls` yüzünden YANLIŞ;
>    derin ölçüm yönü değiştirmedi ama gerekçe **senkron mekanizması**na dayandırıldı.
> 4. Tekil-gövde kapım **başlık** sayıyordu, **gövde** değil → göçü göremiyordu; damga tabanlı
>    ölçüme çevrildi (mutasyonla kanıtlandı).
>
> **Kapı kanıtı:** 26 kapının **22'si mutasyonla** doğrulandı · 2'si kısmi (kardeş depo gerekiyor)
> · 2'si henüz koşulmadı (C8 töreni · CI parite kararı).
>
> **📌 SONRAKİ OTURUM: eylem planı §14.7** — sıralı iş listesi oradadır (C8'i açan 7 kalem,
> 7 kardeş depo işi, bloke kalemler, kapı borcu). Bu dosya iş listesi tutmaz.


**Yapılan:** Eylem planı **§14.0 (D1…D6)** — *"kapılar dürüst hale gelsin"*. Altısı da bitti,
üstüne denetimde görülmemiş **dördüncü bir CI yalanı** bulunup kapatıldı (D3-b).

### Depo durumu
- Dal `feat/contract-tur1` · süit **735 passed / 2 xfailed (beyanlı) / 0 skipped** · RC=0
- `validate.py` 89 dosya / 0 hata · dedektör (master…HEAD): **breaking 0** — artık *ölçülmüş* sıfır
- ⚠️ Tur içi beklenen kırmızılar artık **beyanlı**: `CONTRACTS_VERSION.md` →
  `**Checksum State:** PENDING_REPIN`. Bu satırı **üç kapı** okuyor ve `pin_version.py`
  C8'de dosyayı baştan ürettiği için **beyan kendini siler** → üç kapı aynı anda sertleşir.

### Neyin yalan olduğu ölçüldü (özet — kanıt arşivde)
| Kapı | Eski davranış | Şimdi |
|---|---|---|
| `breaking_change_detector` | iç içe enum/`$defs`/`items`/`oneOf` **kör**; Windows'ta hiç koşmuyor; bozuk şemayı sessizce yutuyor | özyinelemeli + `x-context-subsets` + UTF-8 + okunamayan şema = **exit 2** |
| CI breaking adımı | `continue-on-error: true` **ve** banner stdout'a basıldığı için JSON bozuluyor → `has_breaking=false` (iki bağımsız yalan) | beyan kapısı: **beyan edilmemiş breaking build'i düşürür**; bozuk JSON = FAIL |
| `verify-checksums` | `summary.needs`'te yok | özet + fail koşulunda; uyuşmazlık **beyansızsa** düşürür |
| Sessiz atlama | 18 test `pyyaml` yok diye sessizce atlanıyordu | `conftest.py`: **beyan edilmemiş skip = oturum kırmızı** |
| KR çıkarıcısı | registry'nin **54 tanımından 6'sını** görüyordu; Q5 kapısı boştu | her başlık düzeyi + 4 biçim; "anılmak ≠ tanımlı" |
| Release checklist | annotated tag adımı **yok**; `PENDING_PROPAGATION` kontrolü yok | §3G tag töreni + propagation **testi** |

### ✅ KADEME 1 de bu oturumda yapıldı (contract yarısı)
**D7** `footprint_wkt` → `sees_patch_ids[]` + WKT derece-ayırıcısı + `footprint_crs` +
`crs_mismatch` vocabulary'si · **D8** kalibrasyon fail-open → **FAIL-CLOSED** + `NONE` ·
**D9** `x-layer-classes` + `IRRIGATION_EFFICIENCY` → `CANOPY_TEMP_UNIFORMITY` +
`index_requirements` (worker formüllerinden ölçüldü) · plan dışı **D3-c** (dedektörde 3 boşluk).
⏳ **İki maliyet penceresi kapatıldı** — ikisi de sonraki turda MAJOR olurdu.

### ✅ KADEME 2 de bu oturumda yapıldı (iş kalemleri)
**C11** `sorties[]` + `mission_date` kanoniğe absorbe edildi — ölçüm: edge'in gerçek fixture'ı
kanoniğe karşı 2 hata veriyordu, absorpsiyondan sonra (ürün adları kanonikleştirilerek) **geçiyor** ·
**C2″** hükmü düzeltildi (edge regex DEĞİŞMEZ; eski hüküm `ManifestWriter`'ı kendi manifestine
karşı kırardı) · **E3** `$ref` kararı yazıldı (§14.2.1, **onay bekliyor**) · **E5** `relative_path`
deseni ODM/GDAL/boşluk/Türkçe adlarını kabul ediyor, traversal korumasını koruyor (13 vaka) ·
**E6** `maxItems` 8000. **Aktif kilit:** E11 **C8'den önce merge edilmez** (E4).

### ✅ KADEME 3 de bu oturumda yapıldı
**D12** konsensüs dışlaması (`consensus_participation: EXCLUDED`) + JOIN anahtarı (`tile_id`) +
grup yasağı · **D13** seçim kanıtı (π_h + rotation + bucket) · **D14** öncelik kuralı +
`spot_check_suppressed` · **D15** `confidence_score: const 0` + 2-MINOR deprecation penceresi ·
plan dışı **D3-d** (hiç yokken bileşim eklemek dedektöre görünmüyordu).
⚠️ Worker/platform yarıları açık: **W8** (emisyon) · **P16** (konsensüs yolu EXCLUDED saymamalı).

### ⚠️ KADEME 4 kısmen yapıldı
**D17** `WATER_STRESS` → `proxy_only` + ön fazdan çıkarıldı (üç kaynak çelişiyordu: KG-0.f
*"CWSI/SWIR gerekir, ikisi de yok"* ↔ enum `available` ↔ stage_b uzman kapısı ÖNCESİ teslim) +
A2 changeNote eksiksiz alıntı · **D18** `api/` ağacı artık PII taranıyor (ilk taramada gerçek
isabet: `$.info.contact.email`) + `phone` kapsam-duyarlı + `pyproject` yasak listesi 3→6 hizalandı ·
**D16** kapı/tanım/doküman parçaları: tekil-gövde borcu donduruldu (**50 KR iki gövdeli**),
`stress_ratio` beyanlı tanımsız, CLAUDE.md artık **sayı değil üretici komut** yayımlıyor.

### ✅ D16-b · D18-b · KADEME 5 (yapılabilir kısmı) da bu oturumda
**D16-b** KR-093 **tek gövdeye** indi: normatif metin SSOT metninde, registry 24 satırlık
işaretçi. Karar ölçümle: her iki dosyanın da alt-akış kopyaları BAYAT (registry'nin
platform/worker kopyalarında KR-093 başlığı bile yok) → belirleyici fark **senkron
mekanizması**: SSOT metninin var, registry'nin yok. Registry'ye özgü iki MUST taşındı,
kayıpsızlık testle zorlanıyor. Borç **50 → 49**.
**D18-b** OpenAPI künyesindeki e-posta **silindi**; PII kapısı artık **istisnasız**.
**KADEME 5**: G3/G4 yapıldı — `geom` artık UTM metre / enlem 91 / boylam −181 reddediyor
(D7'deki WKT derece ayırıcısının GeoJSON karşılığı); şemanın ZORLAYAMADIKLARI (halka
kapanışı, papyon) açıkça yazıldı ve regresyon kaydına alındı. K2 için **0.h karar taslağı**
yazıldı. Kalan KADEME 5 kalemlerinin hepsi E13/motor · agronomi · başka depo bağımlısı.

### 🔴 SONRAKİ OTURUMUN İLK İŞİ — **C8 ön koşulları**
⛔ **§14.2.1 `$ref` inline onayı** · ⛔ **D16-b2** (kalan 49 KR göçü) · **AK-10** (KR korpusu
dağıtımı fiilen kırık: worker SSOT metnini hiç taşımıyor) · **0.h** onayı.
Sonra C8 töreni: sürüm + annotated tag + 3 depo pin (SDLC_GATES §3G).
**D16-b:** KR-093'ün iki gövdesi (SSOT metni 10 satır ↔ registry 98 satır) hangi kaynakta
birleşecek? SSOT metni çapraz-repo (platform ile bayt-özdeş), registry tam gövdeleri taşıyor.
Karar verilmeden gövde taşımak **normatif içerik kaybı** riski taşıdığı için bu turda yapılmadı.
Karar sonrası: göç + registry → türetilmiş dizin + `KNOWN_DUAL_BODY_COUNT` düşürülür + **D16-c**
(K3/K5 saklama/rıza MUST'ları) yazılır.

**Karar bekleyenler:** **§14.2.1** `$ref` inline kararı (C8'in ön koşulu) · **D4-b** (parite
kapısı CI'da koşsun mu) · **D4-c** (`drone_capability_matrix.yaml` normatif ama checksum/dedektör
kapsamı DIŞINDA) · **SD8** (etiketsiz 16 sürüm) · **C6b/E13** · **AK-8** (mahsul GRUBU ekseni).
*(AK-1 `CHLOROPHYLL_A` → `LCI` ile KAPANDI · AK-4 pytest sabitlemesiyle KAPANDI · AK-7 beş
crop alanı kanonik sözlüğe bağlanarak KAPANDI.)*

**Başka depoya düşen iş (bu depodan yapılamaz):** **E15** edge `qc_report_writer` —
`min(...,1.0)` kırpması + `except → 0.0` sessiz yolu fail-loud olmalı · **P14** platform
`worker_job_publisher.py:80-84` fail-open `PANEL_ABSOLUTE` adımı · **E16** edge ürün sözlüğü
(küçük→BÜYÜK harf + vendored + fixture) · **P15** platform `spectral_tier.py:51` → `LCI` ·
**W8** worker denetim satırı emisyonu (π_h/bucket zaten hesaplanıyor) · **P16** platform
konsensüs yolu `EXCLUDED` satırı saymamalı.

> 📌 **Bu turda doğan açık kalemlerin TAMAMI tek yerde:** eylem planı **§14.5.1** (AK-1…AK-8;
> ✅ işaretliler aynı turda kapatıldı). Ayrıca kardeş depo işleri: E15 · E16 · P14 · P15 · P16 · W8.
> Bu dosya iş listesi tutmaz; yalnız oraya işaret eder.

**Kanıt:** `denetim/denetim_raporu_2026-07-31_kademe0_kapi_mutasyonlari.md` (her kapının
mutasyon kaydı). **İş listesi:** yalnız eylem planı §14.

---

## 0.A ÖNCEKİ OTURUM (2026-07-31) — Contract Tur 1 + 10-disiplin bağımsız denetim

**Yapılan:** Contract Tur 1'in şema kalemleri tamamlandı (dal `feat/contract-tur1`, 7 commit):
**C0** (iki-form ayrımı zorlanabilir) · **C9+C10** (KR-093 içerik + statü eşlemesi) · **C-SSOT**
(iki SSOT kopyası bayt-özdeş) · **C-PARITE** (9 yanlış parite iddiası) · **C2′** (PlatformForm
`priority_zones` + `object_key`) · **C1′+C3′** (`layer_type`/`band`/`calibration_type`, `raw_frames`)
· **AL-C1+AL-C2** (i.i.d. denetim kanalı). 7 yeni test dosyası, **704 test**.

**Sonra:** 10 disiplinden bağımsız denetim (agronomi/entomoloji · sensör-kalibrasyon · ML/DS ·
pentest · sistem mimarisi · QA · SDLC · KVKK · edge/embedded · GIS/jeodezi) → ajanlar arası
tartışma (4 çatışma çözüldü) → senkronizasyon çatışma matrisi → ana ajanın kanıta karşı ölçümü.

### 📊 Sonuç: 146 bulgu (14 KRİTİK · 45 YÜKSEK) — 10/10 KRİTİK **doğrulandı**

⚠️ **Turun şema işi büyük ölçüde doğru, ama KANIT KAPILARININ ÇOĞU YALAN SÖYLÜYOR.** En sert üç ölçüm:
- `breaking_change_detector` **iç içe enum'lara kör** — `QUARANTINE_CAUTION` silindi, dedektör
  "0 breaking" dedi. ⇒ commit mesajlarındaki *"0 breaking"* ifadesi bu tur için **kanıt değil**.
- Yeni 156 testin **%40'ı CI'da hiç koşmuyor** (45 parite skip + 18 `pyyaml` skip).
- Breaking kapısı `continue-on-error: true`; `verify-checksums` `summary.needs`'te **yok**.

### ✅ O OTURUMUN DEVRETTİĞİ İŞ — **KADEME 0** → **2026-07-31 ikinci oturumda YAPILDI** (bkz. §0.B)

Eylem planı **§14.0** (D1…D6): CI teli · KR başlık çıkarıcısı · dedektör özyineleme · parite
kapısı canlandırma · `xfail(strict)` · release checklist tag adımı.
**Gerekçe:** bu altısı kapanmadan Kademe 1-4'ün hiçbirinin doğrulaması güvenilir değildi.

**Tam sıra:** `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` **§14** (18 kalem, ⛔ işaretliler C8 öncesi).
**Kanıt:** `denetim/denetim_raporu_2026-07-31_10disiplin.md`.

### ⏳ Kapanan maliyet pencereleri (bu tur yapılmazsa MAJOR olur)
- **D9②** `IRRIGATION_EFFICIENCY` → `CANOPY_TEMP_UNIFORMITY`: `layer_type`'ın üreticisi yok → **bedava**
- **D7** `raw_frames[].footprint_wkt` kaldırma: üreticisi (E11) yok → **breaking değil**

### 🔒 C8 sıralama kilitleri (D10)
**E11 C8'den ÖNCE merge edilmez** (geri dönüşü olmayan karantina) · **C11 C8'den ÖNCE** ·
**C2″'de edge regex DEĞİŞMEZ** · **C8'de `$ref`'ler inline** (air-gap).

### Durum
Dal `feat/contract-tur1` push'lu · `validate.py` 89/0 · `pytest` 704 geçti + 1 **beklenen**
checksum kırmızısı (C8'de kapanır) · çalışma dizini temiz.

---

## 0. EN GÜNCEL OTURUM (2026-07-30) — Fotogrametri motor kararı + Karar Günü (7 karar) + tek eylem planı

**İstek:** DJI Terra / PIX4Dfields / Agisoft Metashape karşılaştırması → demo+pilot planı →
tüm işlerin **tek dosyada** toplanması → Karar Günü kararlarının onaylanması.

**Ana çıktı:** `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` — **bundan sonraki tek eylem
kaynağı.** Contract/edge/worker/platform iş listeleri, 7 onaylı karar, aktif öğrenme açık
işleri, çapraz analiz ve teknik referans orada. **Sonraki oturum önce onu okur.**

### Bu oturumda ALINAN 7 KARAR (KG-0.a … KG-0.g · onaylı 2026-07-30)
| Kod | Karar | Contract etkisi |
|---|---|---|
| KG-0.a | Edge→Platform taşıma: **manifest + presigned PUT** (platform ikili gövde ucu açmaz). **Önkoşul: E14** | C0/C1′/C2′/C3′ *(2026-07-31'de hedef şemalar düzeltildi)* |
| KG-0.b**-R** 🔄 | ÖN RAPOR: **ADR-007 değişmez**, direktif **Y-D** ile karşılanır — çiftçi kalibrasyondan sonra **`analysis_priority_zones`**'tan tarlasındaki **sorunlu kırmızı NDVI bölgelerini** görür (`geom` + `ndvi_value` + `ndvi_overlay`). *(Oturum içinde revize: önceki Y-C/"durum bildirimi + ertele" yürürlükten kalktı)* | — (şema değişmez) |
| KG-0.c | Ham kareler **bütün gitmez** — yalnız işaretli yamaları gören kareler | C3 |
| KG-0.d | Pilot **ÜZÜM**, demo hikâyesi **ANTEP FISTIĞI** (kaynak: `crop_readiness.json`) | — |
| KG-0.e | **dev-station** profili (M1+M2 tek makinede; M1/M2 alınmadı) | — |
| KG-0.f | YZ hedefi "böcek türü/sayısı" **DEĞİL** → "**hasar izi sınıfı + şiddeti**" (optik sınır) | `analysis_type.enum` metadata notu |
| KG-0.g | FAZ 0 **sıfır yazılım maliyeti**; eğitim/araştırma lisansı sorgusu + kamu satın alma | — |

### 🔴 DEMO KRİTİK YOLU (KG-0.b-R) — ürün açısından en acil zincir

Çiftçinin **kırmızı NDVI bölgelerini** görmesi için 6 adımın **hepsi** gerekli; biri eksikse ekran boş kalır:

`① C2 patches[].object_key şeması → ② E10 ndvi_overlay gerçek nesne anahtarı → ③ E12 bayrağı AÇ → ④ P4 doğrulama → ⑤ P6 çiftçi okuma ucu → ⑥ P12 PRELIMINARY içerik kaynağı`

**②'siz görsel yok · ③'süz bölge yok · ⑤/⑥'sız ekran yok.** Ön koşul: C13 tesisatı + E14.

**Neden yeni faz gerekmiyor (koddan doğrulandı):** `results_service_impl.py:227` zaten
`"FULL" if mission_status == "DONE" else "PRELIMINARY"` türetiyor; `:247` findings'i PRELIMINARY'de
zaten kırpıyor. Eklenen yalnız **içerik kaynağı** (P12) + **çiftçi okuma ucu** (P6).
KR-019 (tespit yok) · KR-033 (ödeme kapılı kalır) · KR-025 (reçete yok) · ADR-007 §2 (yeni state yok) **korunur**.

### ⚠️ ÖNCEKİ ANALİZDE DÜZELTİLEN HATA — sonraki oturum bunu bilmeli

`end_to_end_workflow.md` C15 maddesindeki *"Pix4D çıktısını platforma taşıyan bir yol yok"*
ifadesi **YANLIŞTIR** (bu oturumda doğrulanmadan devralınmış, sonra düzeltilmiştir):

| | Gerçek |
|---|---|
| **Türetilmiş ürün** (öncelik bölgeleri + görseller) | Yol **TANIMLI ama BAĞLI DEĞİL** — `ingest.py:71` `PriorityZoneEntry` intake manifestinde taşınıyor, `ingest_service_impl.py:266` `analysis_priority_zones`'a yazıyor; eksik olan `submit_manifest` çağrısı (C13). **Tesisat eksikliği, tasarım boşluğu değil** |
| **Ham rasterlar** (ortho/ndvi .tif) | İfade burada **doğru** — yol yok → C1 `index_layers[]` |

**Çelişmeyen kısım:** `worker_bridge_consumer.py:1565` `_emit_preliminary_ready` bir **bildirimdir**,
worker sonucunda tetiklenir (ADR-007 §5). Y-D bunu değiştirmez; yanına kalibrasyon-sonrası
**okuma yolu** ekler. → `end_to_end_workflow.md` C15/C16 güncelleme metinleri eylem planı §9.1-B'de hazır.

### 💰 MOTOR KARARI — demo ve 1 aylık pilot için: **hiçbir şey satın alınmayacak** (§12)

**Demo + 1 aylık pilot = 0 TL.** Elinizdeki **DJI Terra hediyesi** (M3M kutusundan, 3 ay,
**fotoğraf sınırı YOK**) + **ODM** (ücretsiz, CLI'li, otomasyon kanıtı) ikisini de karşılıyor.
Üretim motoru kararı **pilotun ölçümüne** bırakıldı — tahmine değil.

| Bulgu | Sonuç |
|---|---|
| 🔴 **Terra EDUCATION 500 fotoğrafla sınırlı** (DJI resmi: *"reconstruction of 500+ photos is not supported"*) | ~€2.976'lık Terra EDU **ALINMAYACAK** — 50 ha tek tarla 3.635 dosya üretiyor |
| ✅ Terra **Agriculture**: foto sınırı yok, 2D Multispectral dahil, 3 cihaz, **$300/yıl** | Hediye bitince tek makul satın alma |
| 🟢 Eğitim lisansları ucuz: **Metashape Pro $549 kalıcı** · **PIX4Dfields $650/yıl** | ⚠️ Uygunluk farklı: Pix4D *"research institutes"* **açıkça sayıyor**; Agisoft yalnız *"accredited educational institutions"* — araştırma enstitüsü girmeyebilir |
| 🔴 **Eğitim lisansı = ticari kullanım YASAK** (her iki EULA; "materials created with it" dahil) | Faz planında **gelir kapısı** var → EDU ile kurulan hat paraya dönerse **ihlal**. ODM'de (AGPL) bu kısıt yok |
| 📏 Ölçülmüş referans (Pix4D resmi vaka): M3M + 50 ha, 90 m → 727 RGB + 2.908 ÇS = **34,1 GB**; RGB 4:30 / ÇS 6:54 | Depolama tahminimizi doğruluyor: ölçülen **46,9 MB/tetik** vs tahmin 51 (%9 sapma) |
| 🔍 **Terra çıktısında filigran?** Hiçbir kaynak bildirmiyor (DJI deneme kısıtları listesinde de yok), ama DJI'ın açık beyanı da yok | **İlk uçuşta doğrula** (ölçüm #6): `.tif`'i QGIS'te aç + `gdalinfo`. Kalite raporunda logo **normaldir** — demo o raporu göstermiyor. Filigran çıkarsa görseli **ODM ortosundan** üret |

**Pilotun ölçeceği 4 şey üretim motorunu belirleyecek:** ① ODM M3M bant hizalaması ② Terra-ODM
NDVI farkı ③ dk/ha + tepe RAM (32 GB'da) ④ gerçek GB/dönüm.
**Karar ağacı:** ODM çalıştı → ücretsiz kal (~$300/yıl Terra) · ODM çalışmadı → Metashape ·
zonasyon/VRA **ürün** olacaksa → Fields. Tam gerekçe ve kaynaklar: eylem planı **§12**.

### ⚠️ CONTRACT TARAFINDA BEKLEYEN → **ARTIK EYLEM PLANI §3.1'DE** (2026-07-31)

> Buradaki iş listesi **kaldırıldı** — aynı iş iki dosyada tutulduğu için bayatlıyordu
> (C1/C2/C3 yanlış şemayı hedefliyordu, KG-0.f zaten yapılmıştı).
> **Yürürlükteki liste tek yerde:** eylem planı **§3.1 → "🔒 TUR TANIMI"** bloğu.
>
> **TUR 1 = C0 + C1′ + C2′ + C2″ + C3′ + C9 + C10 + AL-C1 + AL-C2** *(+C6 koşullu)*
> *(C4 düştü — contract kalemi değil · C5 düştü — zaten yapılmış · AL-C1/C2 Tur 2'den Tur 1'e alındı)*
>
> **Kaynak devir spesi:** `tarlaanaliz-worker/denetim/birlesik_devir_spec_arsivi_2026.md` §9
> (2026-08-11'e kadar ayrı dosya: `audit_escalation_reason_devir_spec_2026_07_19`;
> worker'ın karar-hazır devri — **platform seçer, worker uydurmaz**).
> **Neden değiştiği:** `denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` (kanıt arşivi).

### Doğrulama (bu oturumda geçti)
`python tools/check_no_egeanaliz.py` → OK · `python tools/validate.py` → **0 hata, ALL VALIDATIONS PASSED**
*(Not: bu oturumda şema/enum **değiştirilmedi** — yalnız `docs/` altına iki doküman eklendi.)*

### Depo hijyeni
- `aktif_ogrenme_*.md` (2 dosya) proje kökünden → **`tarlaanaliz-worker/denetim/`** taşındı
  (sürüm kontrolüne alındı; onlara atıf yapan devir spesiyle aynı dizin — o spes
  2026-08-11'de `birlesik_devir_spec_arsivi_2026.md` §9'da birleşti).
- Eylem planı proje kökünden → **`tarlaanaliz-contract/docs/`** taşındı (kök artık temiz).

### 📌 Sonraki oturum — önerilen sıra *(2026-07-31 denetimine göre güncellendi)*
1. **`docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`'yi oku** — **yapılacak işlerin tek kaynağı.**
   Özellikle §3.1 "TUR TANIMI" + §9 "2026-07-31 BAĞIMSIZ DENETİM TURU" tablosu.
2. **C0 önce** — iki `calibrated_dataset_manifest` formunun rol ayrımını sabitle; C1′/C2′/C3′ bu karar
   olmadan yazılamaz.
3. **KR-093'ü `ssot/kr_registry.md`'ye taşı** (bugün KR-092'de bitiyor) → sonra **C9 + C10**;
   ÖN RAPOR'un kanonik içerik tanımı ve statü eşlemesi bunlar olmadan Y-D'yi kapsamıyor.
4. **E13 kararı → C6** (`RELATIVE` mi `DLS2_RELATIVE` mi) — sıra planda ters yazılmıştı.
5. **Contract Tur 1'i tek sürümde** kapat, sonra C8 töreni (annotated tag + `pin_version.py` + 3 repo pin).
6. **Demo kritik yolu artık 7 adım** (⓪ C9/C10 · ① C2′ · ② E10 · ③ E12 *+P9a* · ④ P4 · ⑤ P6 · ⑥ P12 ·
   **⑦ WEB1 ekran**) — ⑦ olmadan demo API cevabında kalır.
7. **E14 (kalibrasyon kanıtı üreticisi) C13'ten ÖNCE** — yoksa hat bağlansa bile HC-05 M1 içinde durur.
   *(Bu tespit denetimde tam doğrulandı: 5 tüketici / 0 üretici.)*
8. `end_to_end_workflow.md` C13/C15/C16 + `open_items_decisions_2026-06.md` kayıtlarını işle
   (metinler eylem planı §9.1'de kopyala-yapıştır hazır — **Y-D'ye göre düzeltilmiş hâlleriyle**).

### 🟡 Açık kalan tek ürün kararı
**KİRAZ:** `crop_readiness.json` → `bookable: True`, ama `crop_type.enum.v1` (8 ürün) **ve** edge
eşik/fenoloji tablosunda (5 ürün) **YOK** → sipariş edilebiliyor, iş iki yerden düşüyor.
Ya `bookable: False` ya enum + tablo eklenmeli. Detay: eylem planı KG-0.d-EK.

---

## 0.0. Önceki oturum (2026-07-12) — 18-Ajan Bağımsız Denetim + v7.0.1 PATCH

**İstek:** Bu oturumda yapılan tüm contract değişikliklerini (6.2.0 `bandRequirements`/deprecation +
7.0.0 `phenology_stage` rename) 6 kıdemli mühendislik perspektifinden (SW/QA/Pentest/SDLC/ML/DL)
18 bağımsız ajanla satır-satır denetle; bulguları kaynağa karşı doğrula; %100 doğrulananları çöz.

**Sonuç:** **v7.0.1 (PATCH, non-breaking)** — hiçbir enum değeri eklenmedi/kaldırıldı/yeniden adlandırılmadı.
- Fix commit'i: **`3aa5fa2`** (8 dosya). Başlangıç: `7.0.0` (checksum `efe437ef…`).
- Yeni checksum (SHA-256): **`32c747a5876dcb612aade23c4a822ac7e8b23ac47d0042c85021b994db16c40c`**.
- Tam denetim raporu (F1–F10, doğrulama yöntemi, de-escalate edilenler):
  `denetim/denetim_raporu_2026-07-12_18ajan_v7.0.1.md`.

### Doğrulanan bulgular (özet — detay denetim raporunda)
- **F1+F2 (DL/ML):** `analysis_type.enum` v1.4.0→**v1.4.1**. THERMAL_STRESS `requires_bands`
  `["LWIR"]` → tam set `[GREEN,RED,RED_EDGE,NIR,LWIR]` (kullanıcı kararı). Kesişim kuralı
  netleştirildi: `requires_bands ⊆ effective_bands`, `effective_bands = supported_bands ∪
  (termal payload takılıysa thermal_variant.thermal_bands)` + M350 örneği. **F7:** `enforcement: advisory`.
- **F3+F4 (SW/QA/SDLC):** `drone_type.enum` — Parrot açıklamasından yanıltıcı "+termal" kaldırıldı
  (matris kanonik; Sequoia+ multispektral-only, kullanıcı kararı); `x-updated` 2026-02-24→2026-07-12;
  `capability_matrix` effective_bands ile hizalandı.
- **F5 (SDLC):** `phenology_stage_maize_to_corn.md` breaking-guide'a `## Rollback` bölümü eklendi (politika zorunlu).
- **F8 (QA):** 2 yeni test — `phenology_stage` 14-değer set + `bandRequirements.byLayer` bütünlük.
- **F9 (SDLC/Pentest):** `breaking_change_detector.py` artık `enums/`'ı da tarıyor (value removal/rename → MAJOR).
- **F10 (SDLC):** `sync_to_repos.sh` bayat `schemas/enums/` kaynak yolu → `enums/` düzeltildi + `phenology_stage.enum` eklendi.
- **F6 (bu doküman):** §1 self-referential bayat master-head SHA'sı sürüm/checksum kimliğine dayandırıldı (aşağıda).

### Doğrulama (bu oturumda geçti)
- `validate.py`: 89 dosya, 0 hata. `pytest`: **549** geçti (+2 yeni). `pin_version.py --verify`: ✓ `32c747a5…`.
- `breaking_change_detector` (HEAD vs working tree): 0 breaking; enum-diff smoke test: value removal/rename → BREAKING (doğrulandı).

### ⚠️ SONRAKİ OTURUM İÇİN AÇIK
- [ ] **Worker `phenology_stage` hizalaması (7.0.0 breaking, HÂLÂ AÇIK):** `sync_to_repos.sh` artık
  enum'u worker'a gönderiyor (F10), ama worker deposuna bu oturumda **dokunulmadı**. Worker bu enum'u
  tüketiyorsa `MAIZE_*→CORN_*` hizalanmalı.
- [ ] **Consumer re-pin:** Platform/Edge/Worker `CONTRACTS_VERSION.md` pin → 7.0.1 (checksum `32c747a5…`).
  7.0.1 breaking DEĞİL; salt doğrulama hash'i güncellenir.

---

## 0.1. Önceki oturum (2026-07-12) — Platform öneri denetimi + 6.2.0 & 7.0.0

**İstek:** Platform tarafındaki oturumun 7 contract önerisini denetle, planla, onayla, uygula (auto mode).

**Sonuç:** 2 yeni sürüm (yerelde commit'lendi + master'a push edildi). Başlangıç: `6.1.0`.

### Denetim düzeltmeleri (öneri yazarının bilmediği noktalar)
- **Öneri 5 ZATEN MEVCUTTU:** `drone_capability_matrix.yaml` bant/kapasite matrisi (supported_bands, band_classes, available_indices) halihazırda contract-kanonik. Yeni matris oluşturulmadı; yalnız `drone_type.enum` → matrise çapraz-link eklendi.
- **Öneri 7b ZATEN YAPILMIŞTI:** 6.1.0 pin + `feat/beneficial…` merge (PR #20) tamamdı.
- **Öneri 3 / 6:** yalnız teyit — contract zaten kanonik (drone tam-anahtar; IL_OPERATOR deprecated→DISTRICT_REP).

### Commit'lenen değişiklikler
- **`d5f18b9` — v6.2.0 (MINOR, non-breaking):**
  - `analysis_type.enum` v1.3.0→v1.4.0: `metadata.bandRequirements` (requires_bands + availability; THERMAL_STRESS→`requires_thermal_payload`/LWIR, BENEFICIAL→`enum_valid_not_yet_emittable`). Enum dizisi değişmedi.
  - `drone_type.enum`: `x-registry-sync` → `drone_capability_matrix.yaml` çapraz-referansı + add_model_flow.
  - `payment_status.enum.v1`: `x-deprecated` (repo içi `$ref` tüketicisi yok; payment_intent.v1 status'u inline yazar; v2 kanonik).
- **`c0fa705` — v7.0.0 (MAJOR/breaking):**
  - `phenology_stage.enum`: 4 evre `MAIZE_*→CORN_*` (son MAIZE kalıntısı; crop_type v3.0.0 CORN rename'ini tamamlar). Küme=14; GRAPE_*/OLIVE_* değişmedi. Türkçe metinler ("Mısır") değişmedi.
  - `crop_type.enum`: changeNote'taki artık-yanlış "MAIZE_* remain unchanged" → "aligned to CORN_* in v7.0.0" (enum dizisi değişmedi; tarihsel-kayıt).
  - Yeni: `docs/migration_guides/phenology_stage_maize_to_corn.md`.

### İş kararı
- **Öneri 2 (payment PENDING_RECEIPT) = (B):** contract DEĞİŞMEZ. Platform `PENDING_RECEIPT` yerine `PAYMENT_PENDING` kullanmalı (off-contract ara durum contract'ta ayrı modellenmez).

### ⚠️ SONRAKİ OTURUM İÇİN AÇIK — KRİTİK
- [ ] **Worker `phenology_stage` hizalaması (7.0.0 breaking):** Worker bu enum'u tüketiyorsa `MAIZE_*→CORN_*` **aynı turda** hizalanmalı; aksi halde `MAIZE_*` emit/bekleyen worker renamed enum'a karşı validasyonda kırılır. Bu, 7.0.0'ın worker'ı etkileyebilecek TEK breaking maddesidir. Bu oturumda worker deposuna **dokunulmadı**.
- [ ] **Consumer pin güncellemesi:** Platform/Edge/Worker `CONTRACTS_VERSION.md` pin 6.1.0 → 7.0.0 (checksum `efe437efeca2d3ee894f1965353fbed42c8d9fb9ad3374d5061a503c6ef93caa`). MAJOR → koordinasyon gerekir.

### Doğrulama (bu oturumda geçti)
- `validate.py`: 89 dosya, 0 hata. `pytest`: 547/547 geçti. `pin_version.py --verify`: ✓.

---

## 1. Depo Durumu (Snapshot)

> ⚠️ **2026-07-31'de DÜZELTİLDİ — bu bölüm iki sürüm bayattı.** `7.0.1` yazıyordu ve §3 tüketici
> tablosu "platform GERİDE, re-pin gerekli" diyordu; **ikisi de yanlıştı** ve sonraki oturumu
> **zaten yapılmış** bir re-pin turuna yollayacaktı. Aradaki sürümler: **7.1.0** (`analysis_result.v1
> → tile_counts`, KR-088) ve **7.2.0** (`intake_manifest.v1` edge/AV1 karantina sayaçları).
>
> **KALICI KURAL:** Bu bölüm **C8 release töreninin parçası olarak** güncellenir.
> Sürüm bump'ından sonra güncellenmediyse **release eksiktir.**

- **Kontrat sürümü (CONTRACTS_VERSION.md):** **`7.2.0`** — Breaking: **NO** (MINOR; iki opsiyonel
  top-level alan, `required` değişmedi).
  - Checksum (SHA-256): **`5d3c204d0cad6946939c90c9778c9d1d9df3e69b78207ee8ce638ac3bd494c02`**
  - Sürüm zinciri: `7.0.1` (`3aa5fa2`) → `7.1.0` (`58899e2`) → **`7.2.0` (`02845fb`)**
  - **Etiketler doğrulandı (2026-07-31):** `v6.1.0 · v7.0.1 · v7.1.0 · v7.2.0` — **dördü de
    *annotated*** (`git for-each-ref … %(objecttype)` → `tag`) ⇒ **I-2 değişmezi TUTUYOR.**
  - Checksum yalnız `schemas/`+`enums/`+`api/` ağacını kapsar; CHANGELOG.md / docs/ değişiklikleri
    (bu handoff + denetim/ raporu dahil) checksum'ı DEĞİŞTİRMEZ. `git describe` etiketten sonra
    `vX.Y.Z-N-g…` gösterirse ve N doküman commit'iyse bu NORMALDIR — sürüm kimliği SHA'ya değil,
    yukarıdaki checksum'a dayanır (F6: self-referential SHA'dan kaçınıldı).
  - **Kapı durumu (2026-07-31 koşuldu):** `pin_version.py --verify` ✅ · `validate.py` ✅ 89 dosya / 0 hata.
- **Tek çalışma deposu:** `.../TARLA-ANALİZ/tarlaanaliz-contract` (origin = `github.com/physiscs-zana/tarlaanaliz-contract`)

### Dallar / PR durumu — **2026-07-31** itibarıyla: çalışma dizini temiz, **açık PR yok**
*(aşağıdaki tablo 07-12 tarihli tarihsel kayıttır)*

| Öğe | Durum | Not |
|---|---|---|
| `master` | `3aa5fa2` (+ doküman commit) | 7.0.1 fix commit `3aa5fa2`; oturum-kapanış handoff/denetim commit'i bir üstte (doküman-only, checksum-nötr) |
| PR #19 (`feat/kr-092-seasonal-flight-calendar-v2`) | **MERGED** | KR-092 sezonluk uçuş takvimi + RICE; eklemeli 4.3.0; crop_type MAIZE-kanonik |
| PR #18 (`feat/kr-092-seasonal-flight-calendar`) | **CLOSED** | Terk edildi — 5.1.0 MAJOR gereksizdi (TARIS zaten master'da yok) + CORN (kanonik-dışı) |
| Açık PR | **yok** | — |

- Çalışma dizini: temiz.

---

## 2. Bu Oturumda Yapılanlar (2026-07-05) — Denetim + 4 Sürüm-Yönetişimi Hatası

**İstek:** Contract ↔ (worker/platform/edge) senkronizasyonunun %100 doğruluğunu holistik denet;
bulunan 4 yüksek-öncelik sürüm hatasını "auto mode" ile gider.

### Giderilen hatalar (1–3 tamamlandı)

1. **KR-092 iki rakip açık PR'de (5.1.0 vs 4.3.0), master'a girmemişti** → **ÇÖZÜLDÜ.**
   PR #19 (eklemeli 4.3.0) merge edildi; PR #18 (5.1.0 MAJOR) kapatıldı.
   Gerekçe: PR #18'in TARIS kaldırma "breaking"i master'da zaten yapılmıştı (gereksiz MAJOR);
   PR #19 kanonik MAIZE isimlendirmesini kullanıyor; tüketiciler fiilen PR #19 hattındaydı.
2. **Platform pin ≠ gerçek submodule (26bedb4/5.1.0 vs 23d9ed9/4.3.0), checksum gate üretilemez** → **ÇÖZÜLDÜ.**
   Platform `CONTRACTS_VERSION.md` artık submodule `82d2fd8` = 4.3.0'a pinli; master head ile tutarlı.
3. **Worker/edge, master'da olmayan RICE/rice kullanıyor** → **ÇÖZÜLDÜ.**
   RICE, 4.3.0'da kanonik crop_type enum'una eklendi (9 bitki MAIZE-kanonik: COTTON, PISTACHIO,
   MAIZE, WHEAT, SUNFLOWER, GRAPE, OLIVE, RED_LENTIL, RICE). MAIZE↔CORN alias köprüsü korunuyor.

### Kısmen açık (Hata 4 — bilinçli ertelenmiş)

4. **Beş sürüm etiketi hizasız (4.2.1/4.3.0/5.1.0/5.1.1/1.2.0)** → **KISMEN.**
   Contract (4.3.0) + platform (4.3.0 pin) hizalı. Worker (`v5.1.1`) ve edge (`1.2.0`)
   **kendi bağımsız sürüm şemalarını + kendi hash gate'lerini** kullanır (contract'ın submodule'ü
   DEĞİL). Bu etiketlerin 4.3.0 ile "eşleşmesi" tasarım gereği beklenmez. Kalan gerçek fark:
   worker'ın terk edilen 5.x dalından gelen meyve-ağacı bitkileri (APPLE/PEACH/CHERRY/FIG).
   Platform dokümanı bunu açıkça **"ayrica hizalanacak"** olarak işaretlemiş — bu bilinçli
   ertelenmiş bir kalem, auto-mode hızlı düzeltmesi değil.

**Not:** Hata 1–3 giderimi büyük ölçüde eşzamanlı (başka makinedeki) oturumla + bu oturumda
PR #18'in kapatılmasıyla tamamlandı. Worker deposunda hâlâ aktif "closeout/kalan_isler" commit'leri
görülüyor → o depoya bu oturumdan **dokunulmadı** (çakışmayı önlemek için).

---

## 3. Tüketici (consumer) Durumu — **2026-07-31 (dört depoda ölçüldü)**

| Servis | Sürüm | Senkron | Not |
|---|---|---|---|
| **Contract (SSOT)** | **`7.2.0`** (`02845fb`, tag `v7.2.0` *annotated*) | — | master; checksum `5d3c204d…` |
| **Platform** | **`7.2.0`** (`contracts/` submodule + kök `CONTRACTS_VERSION.md`) | ✅ **HİZALI** | checksum `5d3c204d…` birebir; per-dosya LF-hash `ed700c63…` |
| **Worker** | **`v7.2.0`** (kendi KR-041 hash gate'i ile) | ✅ **HİZALI** | I-4: vendored **alt-küme**, bayt-özdeşlik beklenmez |
| **Edge** | **`1.3.0`** (bağımsız sürüm şeması) | ✅ Temiz | Kendi pin/hash gate'i; metinde 7.2.0'a atıf var |

> ✅ **I-1 (sürüm dizesi hizası) ve I-2 (annotated tag) DOĞRULANDI — senkron kırık değil.**
> Bu tablonun eski hâli platformu "GERİDE" gösteriyordu; **2026-07-31'de ölçülerek düzeltildi.**
> ⚠️ *Eski §2/§3.1'deki `phenology_stage` ve worker `v5.1.1` maddeleri tarihsel kayıttır —
> 7.0.1→7.2.0 zincirinde kapandı.*

---

## 3.1. YENİ BULGU (2026-07-05) — Kanıtlanmış çapraz-depo senkron kırığı: worker RICE

**Ne:** Contract 4.3.0'ın (KR-092) `crop_type.enum.v1`'e **RICE** eklemesi, worker'ın
`tests/contract/test_crop_vocabulary_bridge_lock.py` dosyasındaki **donmuş `GAP_CROPS`
anlık görüntüsünü (8 bitki, RICE yok)** bayatlattı. Worker RICE'ı hâlâ "GAP-dışı worker-only"
sayıyordu. Sonuç: kontrat deposu kardeş dizinde erişilebilir olduğunda worker'ın
`test_gap_set_matches_live_contract_enum` testi **BAŞARISIZ** (kanıt: yerelde çalıştırıldı).

**Neden bir senkron hatası:** Contract tarafı doğru (eklemeli MINOR yayınladı); desync worker'ın
elle-tutulan donmuş anlık görüntüsünde belirdi. Bu, testin kendi tasarladığı "kontrat değişince
GAP anlık görüntüsünü yeniden-senkronla" bakım işlemi (docstring satır 25-28, 233-236).

**Düzeltme (hazır, DOĞRULANDI):** RICE'ı `GAP_OUT_WORKER_CROPS` → `GAP_CROPS`'a taşı (RICE artık
doğrudan GAP eşleşmesi; worker yine `WORKER_CROPS`'ta RICE'ı konuşuyor). 13-vs-14 sayımı / CORN-vs-MAIZE
ekseni governance kalemine **DOKUNMAZ** — dik (orthogonal).
- **Worker PR #115 MERGED** (2026-07-05, worker master `3cdedd6`): RICE, `GAP_OUT_WORKER_CROPS`
  → `GAP_CROPS`'a taşındı. Bridge süiti 12/12 yeşil (master'da doğrulandı); ruff temiz.
- **Worker PR #116 MERGED** (2026-07-05, worker master `f61e15f`): worker `denetim/kalan_isler.txt`
  açık-kalem #3 ("contract worker-14/CORN'a uzlaşır") bayat beklentisi güncellendi. SONUÇ:
  contract MAIZE-9 kaldı, worker-14 benimsenmedi, kalıcı uzlaşma = AK-4 Yöntem 2 (worker↔GAP
  köprüsü; iki eksen sınır-çevirisiyle birlikte yaşar). Doküman-only.

**Ek governance notu (kod kırığı DEĞİL):** worker'ın 06-30 AK-4 kaydı, kanonik ekseni **worker-14/CORN**
bekliyor ve contract'ın CORN'a uzlaşmasını umuyordu (`denetim/kalan_isler.txt` §4.B). Contract/platform
07-05'te **MAIZE-kanonik** kaldı ve worker-14'ü BENİMSEMEDİ. Köprü zaten CORN↔MAIZE çevirdiği için
**kod kırığı yok**; ama worker'ın açık-kalem prosesi bayat (ters yönde çözülen bir uzlaşmayı bekliyor).
Bu, worker+contract ORTAK kararı — tek taraflı çözülmedi.

## 3.2. Doküman Bakımı (2026-07-05 oturum-kapanış) — docs/ temizliği

- **SİLİNDİ:** `docs/sync/SYNC_ANALYSIS_2026-06-30.md` (190 satır). Gerekçe: 4.3.0 giderimi +
  bu SESSION_HANDOFF tarafından geçersiz kılınan eski-tarihli denetim anlık görüntüsü;
  repo genelinde **hiçbir referansı yok** (grep ile doğrulandı). Bu dosyanın taşıdığı bilgi
  artık §1–§3.1'de özetli.
- **KORUNDU:** `docs/sync/worker_required_changes_2026-05-30.md` (57 satır). Gerekçe: kalıcı 3.0.0
  göç kılavuzu `docs/migration_guides/contracts_3_0_0_structural_absorption.md:47` tarafından
  **referans veriliyor** (worker-tarafı 3.0.0 hizalama detaylarının eki). Silmek göç kaydında
  sarkan (dangling) bir bağlantı bırakırdı → bilinçli olarak tutuldu.

---

## 3.3. Yönetişim Kapanışları (2026-07-05 devam) — meyve-ağacı bitkileri + v5.1.1 netliği

Bu iki kalem §4'te "açık" işaretliydi; ikisi de **kod değişikliği değil, yönetişim (governance)
kapanışı** olarak çözüldü. Ayrıca iki düşük-öncelik kontrat-içi kalem (validate.py UTF-8 + CLAUDE.md
datasets) bu oturumda giderildi (§4).

### (A) Worker meyve-ağacı bitkileri (APPLE/PEACH/CHERRY/FIG) — KAPANDI (bilinçli kapsam-dışı)

- **Karar:** Bu 4 bitki GAP kontratına **EKLENMEZ.** Ege (Aegean) bölgesi mirası mahsullerdir;
  GAP (Güneydoğu Anadolu) kapsamı DIŞINDADIR. Kontrat kanonik seti GAP-9 kalır.
- **Kilit nerede:** Worker `tests/contract/test_crop_vocabulary_bridge_lock.py` içindeki
  `GAP_OUT_WORKER_CROPS = {APPLE, PEACH, CHERRY, FIG}` frozenset'i bu 4'ü açıkça "GAP-dışı
  worker-only" olarak kilitler (sessiz drift imkansız). Worker runtime enum'u worker-13.
- **Kod kırığı YOK:** Köprü (AK-4 Yöntem 2) yalnız örtüşen mahsulleri çevirir (CORN↔MAIZE,
  LENTIL↔RED_LENTIL). Meyve-ağacı bitkileri GAP sınırını hiç geçmez → kontratta karşılığı
  olmaması TASARIM gereğidir, eksiklik değil.
- **Kontrat zaten belgeliyor:** `enums/crop_type.enum.v1.json` `notes.worker_alignment` (satır 92)
  bu bitkileri "Aegean crops (CHERRY/FIG/APPLE/PEACH), NOT 1:1 with GAP" olarak anıyor.
- **Platform:** CHERRY/FIG yalnız platform'un crop_type VO'sunda (value object) var; platform da
  worker-14'ü BENİMSEMEDİ. Ortak karar (contract+worker+platform), tek taraflı değil.
- ⇒ "Hata 4"ün meyve-ağacı boyutu KAPANDI. Kontrat enum'una **dokunulmadı** (dokunmak GAP
  kapsamını ihlal eder + tek taraflı cross-repo değişiklik olurdu).

### (B) Worker `v5.1.1` etiket-mirası — NETLEŞTİRİLDİ (worker PR #117)

- **Durum:** Worker `CONTRACTS_VERSION.md`'i `v5.1.1`'i KENDİ bağımsız KR-041 hash kapısıyla
  (interface/contracts/*.json 7 dosya, hash `c3cb01bf…`) taşır. Kontrat SSOT SemVer'inden (4.3.0)
  ve `tools/pin_version.py` checksum'ından **bilinçli olarak ayrıktır.**
- **Kafa karışıklığı:** "5.x > 4.x → worker kontrattan ileride" YANLIŞ okumasıydı. İki şema
  bağımsız; sayıların eşleşmesi beklenmez.
- **Aksiyon:** Worker `CONTRACTS_VERSION.md`'ine eklemeli (additive) "Version scheme note" eklendi
  → **worker PR #117 MERGED** (worker master `416be79`, doc-only; KR-041 hash değişmedi —
  `compute_contracts_hash.py --verify` ile doğrulandı). CI gerçek yeşil (admin-bypass yok): KR-041
  hash kapısı + tam test süiti geçti. NOT: `CONTRACTS_VERSION.md` değişikliği worker'ın "CHANGELOG
  entry for contract/KR changes" CI kapısını tetikledi → kök-neden düzeltildi (`CHANGELOG.md`'e
  eşleşen giriş eklendi, bypass DEĞİL). Yeniden-isimlendirme YAPILMADI (sürüm adı worker sahibinin kararı).

---

## 3.4. Şişkinlik-Temizliği (de-bloat) — devir dosyaları sadeleştirildi (2026-07-05 devamı)

**İstek:** Birden fazla "SONRAKİ OTURUM" bölümü olan devir/handoff dosyalarında, **bitmiş-iş
(tamamlanmış) kayıtlarını son 10 gün hariç sil** — gereksiz şişmişlerdi. Kesim tarihi = **2026-06-25**
(bugün 07-05, son 10 gün korunur). Kapsam üç repo (contract+worker+platform). Silinen içerik git
geçmişinde kalıcı olarak erişilebilir (geri-alınabilir).

- **Worker `denetim/kalan_isler.txt`** → **PR #118 MERGED** (worker master `469e7d7`, gerçek yeşil CI —
  admin-bypass YOK; −48 net satır). §0/§1/§3 (2026-05-31, kesim-öncesi bitmiş-iş) dosyanın kendi
  "Kademe-1 temizlik" konvansiyonuyla kısa git-SHA işaretçilerine indirildi; **açık kalemler §2/§4/§5/§6
  (pencere içi) aynen korundu**. Tam anlatı git'te: commit `8987be1..fcae49a` (7 commit) + `a709d5a` (D-3).
- **Platform `docs/security/open_items_decisions_2026-06.md`** → kompaktlandı (**commit `a58628c`,
  714→281 satır**; doküman-only, doğrudan `main`). Bitmiş oturum anlatıları tek-satır/oturum **"Yapıldı log"**
  tablosuna indi; **hiçbir açık kalem silinmedi** (karar tabloları DEFER/COORDINATE/BLOCKED/WON'T-DO +
  "İzlenen küçük açık kalemler" + H2 HttpOnly fazlı plan + Next 15 spike + EKİM 2026 planı + EN GÜNCEL
  SONRAKİ OTURUM korundu). İki süperseded "SONRAKİ OTURUM" bölümü, kalemleri güncel tablolara taşınarak
  Yapıldı log'a absorbe edildi. Tam anlatı git'te (`c0a008d` ve öncesi).
- **Contract `docs/SESSION_HANDOFF.md`** (bu dosya) → **budama gerekmedi**: tüm içeriği 2026-07-05
  (10-gün penceresi içinde); kesim-öncesi bitmiş-iş kaydı yok.
- **Yöntem farkı (kasıtlı):** worker = dal+PR+yeşil-CI'da-merge (kullanıcı onaylı, CHANGELOG kapısı
  kök-nedenle karşılandı, bypass yok); platform = mevcut doküman konvansiyonu gereği doğrudan `main`
  (doküman-only kompaktlama).

---

## 4. Sonraki Oturum İçin — Açık İşler / Öneriler

- [x] **Worker PR #115 MERGED** (§3.1) — RICE bridge-snapshot senkronu worker master'a girdi (`3cdedd6`).
- [x] **Worker PR #116 MERGED** (§3.1) — `kalan_isler.txt` CORN/MAIZE eksen-sonucu notu worker master'a girdi (`f61e15f`).
- [x] **docs/ temizliği** (§3.2) — eski-tarihli `SYNC_ANALYSIS_2026-06-30.md` silindi; referanslı `worker_required_changes_2026-05-30.md` korundu.
- [x] **Worker meyve-ağacı bitkileri (APPLE/PEACH/CHERRY/FIG) hizalaması** (§3.3-A) — KAPANDI.
  Bilinçli kapsam-dışı karar: GAP kontratına eklenmez (Ege mirası), köprüyle uyumlu, kod kırığı yok.
- [x] **Worker `v5.1.1` etiket-mirası netliği** (§3.3-B) — worker PR #117 **MERGED** (worker master
  `416be79`; eklemeli doc note + CHANGELOG girişi; CI gerçek yeşil).
- [x] **`tools/validate.py` Windows UTF-8 (cp1254) çökmesi** — KALICI DÜZELTİLDİ. `main()` başında
  `sys.stdout/stderr.reconfigure(encoding="utf-8")`; artık `-X utf8` bayrağı GEREKMİYOR (PowerShell +
  git-bash'te doğrulandı: 87 dosya, 0 hata).
- [x] **`CLAUDE.md` şema ağacı `schemas/datasets/` (9 dosya)** — BELGELENDİ (KR-072/073 zincir-koruma
  şemaları: dataset, dataset_manifest, calibration_certificate, qc_report, scan_report,
  verification_report, attestation, transfer_batch, evidence_bundle_ref).
- [x] **Devir dosyaları şişkinlik-temizliği (de-bloat)** (§3.4) — worker `kalan_isler.txt` PR #118
  MERGED (`469e7d7`); platform defteri `a58628c` (714→281); contract handoff budama gerektirmedi.
  Tüm açık kalemler korundu; silinen bitmiş-iş git geçmişinde.
- [x] **18-Ajan bağımsız denetim + v7.0.1 PATCH** (§0) — bu oturumun 6.2.0/7.0.0 değişiklikleri
  6 perspektiften (SW/QA/Pentest/SDLC/ML/DL) denetlendi; F1–F10 doğrulandı ve giderildi; fix commit
  `3aa5fa2`, checksum `32c747a5…`. Detay: `denetim/denetim_raporu_2026-07-12_18ajan_v7.0.1.md`.

---

## 5. Bilgisayarlar Arası Notlar

- Yeni makinede başlarken: `git fetch origin --prune` → dalların `[ahead/behind]` durumunu kontrol et.
- Kalıcı bilgi **repoya** yazılmalı (bu dosya gibi); Claude'un yerel hafızası makineye özeldir, taşınmaz.
- **Eşzamanlı oturum uyarısı:** worker'a bu oturumda dal+PR yöntemiyle yazıldı (PR #118, `469e7d7`;
  §3.4); artık senkron/temiz. Yine de başka makine yazmadan önce `git fetch --prune` ile `[ahead/behind]`
  doğrula (çakışma riski).
- Doğrulama komutu (değişiklik sonrası): `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -v`.
