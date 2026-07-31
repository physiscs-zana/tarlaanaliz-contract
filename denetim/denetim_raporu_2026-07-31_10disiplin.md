# 10-DİSİPLİN BAĞIMSIZ DENETİM — KONSOLİDE RAPOR

**Tarih:** 2026-07-31 · **Kapsam:** `9fd07ca..61717bd` (Contract Tur 1) · **31 dosya**
**Yöntem:** 10 bağımsız disiplin ajanı → ajanlar arası tartışma → senkronizasyon çatışma matrisi
→ **ana ajanın kanıta karşı kendi ölçümü**.

> ## 📐 BU DOSYA **KANIT ARŞİVİDİR — İŞ LİSTESİ DEĞİLDİR**
> Yapılacak işler **yalnız** `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` §14'tedir.
> Bu dosya "neden" sorusunun `dosya:satır` dayanağını tutar.

**Toplam:** 146 bulgu — 14 KRİTİK · 45 YÜKSEK.
**Ön ek:** A=Agronomi · S=Sensör · M=ML/DS · P=Pentest · AR=Mimari · Q=QA · SD=SDLC · K=KVKK · E=Edge · G=GIS

---

## 0. ANA AJANIN DOĞRULAMA HÜKMÜ

### ✅ DOĞRULANDI (10/10 KRİTİK — kendi ölçümüm)

| Bulgu | Ölçüm |
|---|---|
| **A1** | plan *"CWSI/SWIR gerekir, ikisi de yok"* ↔ `analysis_type: availability=available` ↔ `stage_b`'de var |
| **A3** | `stress_ratio` repo geneli **3 atıf / 0 tanım** |
| **S1** | `calibration_type` required'da değil ✓ · alt-küme `NONE`'suz ✓ · `"missing -> PANEL_ABSOLUTE"` var ✓ |
| **M3** | `detections` **dizi** ✓ · `Detection.tile_id` **var** ✓ → "job_id ile JOIN" yetersiz |
| **AR1** | SSOT:744 *"YALNIZCA ortomozaik/indeks"* ↔ registry *"YALNIZCA iki aşama, Aşama A dahil"* |
| **AR3** | `## KR-`=**6**, `### KR-`=**48** → CLAUDE.md'deki "6 of ~49, tamamlayıcı" yanlış |
| **E2** | edge `intake_manifest_valid.json` → kanoniğe karşı **2 hata** |
| **E3** | kanonik **3** harici `$ref` · vendored **0** → air-gap `Unresolvable` |
| **G1** | `calibration_result`'ta CRS/SRID alanı **yok** |
| **SD1** | **kendi mutasyonum:** `QUARANTINE_CAUTION` silindi → dedektör `Breaking Changes: 0` |

### ⚠️ ŞÜPHELİ — atılmadı, plana alındı

| Bulgu | Neden şüpheli | Nasıl kesinleşir |
|---|---|---|
| **M2** | Şemada muafiyet yok (doğru), ama platform konsensüs kodunun denetim satırını nasıl ele aldığı ölçülmedi | Platform `expert_review` konsensüs yolu |
| **M4** | Toplu-onay yayılımının denetim satırına fiilen uygulanıp uygulanmadığı doğrulanmadı | Worker `bulk_approval` yolu |
| **M1/P4** | `AuditSelection.rate/bucket` üretiliyor ama emisyon kodu **henüz yazılmamış** — "kayıp" değil "hiç bağlanmamış" | E11/AL-W1 yazılırken |
| **Q21** | 11 koşumun 2'sinde ikinci kırmızı; yeniden üretilemedi | C8 öncesi `pytest -q` ×5 |
| **SD8** | 4 etiketin annotated olduğu **doğru**; "her sürüm etiketlenir" 16 sürümde tutmuyor | Koordinatör kararı (retro-tag mı, kayıt notu mu) |
| **A7** | Fıstık dikim aralığı **literatür teyidi gerekli** (ajan kendisi işaretledi) | TAGEM/Bakanlık |

---

## 0.1 TARTIŞMA SONUÇLARI (ajanlar arası, 4 çatışma)

| # | Sonuç |
|---|---|
| **Ç1** `spot_check` | **A itirazı KABUL etti.** Dışlama kalır ama **yönü zorunlu**: "denetim çekilişi ÖNCE ve bağımsız; çakışmada `audit_sample` kazanır". A'nın nüansı: gerçek engel **sunumsal** — aynı inceleme hem "modeli denetle" hem "modelden bağımsız etiketle" olarak render edilemez |
| **Ç2** quasi-id | **K bulgusunu GERİ ÇEKTİ.** Eksenler üst düzey alanların kopyası; CHERRY enum'da yok; PISTACHIO'da fenoloji null. Kalıntı: yayın politikasına `n≥5` |
| **Ç4** `confidence_score` | **M kendi iddiasını DÜZELTTİ:** `const:0` bilgi kanalını kapatır, **seviye kaymasını** kapatmaz. SD ile **dik**, rakip değil → sıralı uygulanır. M'nin bağlayıcı uyarısı: **M2/M3 kapanmadan Ç4 ikincil kalem** |
| **Ç5** `layer_type` | **A, A10'u GERİ ÇEKTİ** (S-10'un çıktısı olarak beklenmeli). Zamanlama uyarısı: `IRRIGATION_EFFICIENCY` yeniden adlandırması **üretici yokken bedava, sonra MAJOR** |
| **Ç7** `footprint_wkt` | **G ve K, E'nin önerisini KABUL etti.** K tartışmada **YENİ gerekçe üretti**: 35 m'de kare ~42×31 m, uçuş dönüşleri tarla dışına taşar → **komşu parsel = üçüncü kişi verisi, hukuki sebep yok (KVKK md.5)** — riski ORTA→YÜKSEK yükseltti. G ölçtü: **EWKT `shapely.wkt.loads`'u KIRIYOR** |

---


## 1. KRİTİK (14)

| ID | Bulgu | Kanıt | Aksiyon önerisi |
|---|---|---|---|
| **A1** | KG-0.f `WATER_STRESS`'i üretilemez sayıyor; `analysis_type` `availability: available` diyor; KR-093 onu uzman kapısı ÖNCESİ çiftçiye teslim ediyor | plan:1037,1043 ↔ analysis_type:40 ↔ report_phase:34 ↔ kr_registry:1271 | `requires_thermal_payload`/`proxy_only` + stage_b'den çıkar |
| **S1** | Kalibre olmayan (DN) paket fail-open olarak `PANEL_ABSOLUTE`'a yükseliyor: `calibration_type` opsiyonel + alt-kümede `NONE` yok + enum global kuralı `missing → PANEL_ABSOLUTE` | platform/calib_manifest:7-16,61-70 · calibration_type.enum:26,56-61 | Bağlam-bazlı `missing ⇒ FAIL-CLOSED` + alt-kümeye `NONE` |
| **M1** | Tabaka etiketi taşınıyor, dahil-edilme olasılığı π_h taşınmıyor → Horvitz-Thompson yansız kestirim imkânsız | expert_review_queue:216-277 · worker audit_set_sampler.py:84-96 | `audit_selection_rate` + `audit_rotation_key` + `audit_bucket` ekle |
| **M2** | Denetim satırı KR-019 konsensüsüne kardeş inceleme olarak giriyor → kör uzman yayını bloke edebiliyor; ölçüm ölçtüğü sistemi değiştiriyor | SSOT:601 · allOf:280-369 (muafiyet yok) | Sözleşmeye "denetim satırı konsensüse KATILMAZ" |
| **M3** | Tile-düzeyi join anahtarı yok → `propagation_precision` hesaplanamaz; `measurement_join`'daki "job_id ile JOIN" iddiası yanlış (`analysis_result.detections` DİZİ) | expert_review_queue:374 vs :7-14,109-140 | `tile_id` ekle, `audit_sample:true` altında zorunlu |
| **M4** | Denetim satırında `tile_group_*` serbest → toplu-onay yayılımı denetim etiketini kendi ölçtüğü yayılıma besliyor ⇒ `propagation_precision → 1` yapısal | expert_review_queue:177-198 · audit_set_sampler.py:13-17 | `allOf`: audit ⇒ `tile_group_id:null`, `size:const 1` |
| **AR1** | KR-093 aynı depoda İKİ normatif metinle tanımlı ve ÇELİŞİYORLAR (içerik + statü haritası) | SSOT_v1_2_0.txt:744,750 ↔ kr_registry:1264-1272,1279-1284 | Birini normatif olmaktan çıkar + "aynı KR iki yerde gövdeyle tanımlanamaz" kapısı |
| **E1** | C2″ kalemi C2′ kararıyla çelişiyor: "edge regex'ini object_key için genişlet" ⇒ `ManifestWriter` kendi manifestini reddeder | plan:177 · intake_manifest:619 · priority_zone.py:29-31 | C2″ yeniden yaz: regex DEĞİŞMEZ |
| **E2** | C11 (sorties+mission_date) C8'den ÖNCE gelmeli; edge fixture'ı kanoniğe karşı 2 hata veriyor | vendored intake_manifest vs kanonik `$defs.EdgeForm` · manifest_writer.py:216-219 | Sıralama kilidi plana |
| **E3** | Kanonik `intake_manifest` 3 harici `$ref` taşıyor; vendored kopyalarda 0 → air-gapped M1'de çözülemez (`Unresolvable` üretildi) | intake_manifest:56,183,197 | C8'de enum'lar inline veya yerel Registry — YAZILI karar |
| **SD1** | `breaking_change_detector` iç içe enum'lara HİÇ bakmıyor; enum değeri silme → "0 breaking" (ölçüldü) | detector:175,226-254 | `compare_schemas` özyinelemeli + regresyon testi |
| **SD2** | `$defs` altındaki `required`/alan değişiklikleri de görünmez; bu turun `$defs` işlerinin tamamı raporsuz | detector:91-95,129 | SD1 ile aynı düzeltme |
| **Q1** | Dal CI'da KIRMIZI: 22 şema/enum değişti, `CONTRACTS_VERSION.md` re-pinlenmedi; base'de 11/11 yeşil | CONTRACTS_VERSION:7 · test_pin_version:152 | C8'de `pin_version.py`; tur stratejisi CI ile uzlaştırılmalı |
| **G1** | `observed_footprint_wkt` ödeme girdisi ama CRS kanalı YOK; CRS uyuşmazlığı → `coverage_ratio=0.0` → "TEKRAR UÇUŞ" = pilot ödenmez; sessiz (`except → 0.0`) | edge/calib_manifest:35-39 · qc_report_writer.py:267-289 | `footprint_crs` const veya EWKT pattern + fail-loud |

---

## 2. YÜKSEK (45) — özet

**Agronomi:** A2 changeNote KG-0.f'i seçici alıntılıyor (WATER_STRESS atlanmış) · A3 `stress_ratio` hiçbir yerde TANIMLI DEĞİL (4 atıf, 0 tanım) ama KR-093 zorunlu teslimat kalemi · A4 NDWI çelişkisi (worker kilitli giriş kanalı + `ndwi_mean` var; ayrıca 4 banttan NDWI = McFeeters su-kütlesi, Gao bitki-suyu değil) · A5 fenolojik stratifikasyon satılan ürün kümesiyle neredeyse ayrık (satılan 5'in 3'ünde evre yok; kapsanan OLIVE satılmıyor) · A6 contract fenoloji enum'u ↔ edge `phenology_calendar.yaml` iki ayrı sözlük, 1:1 eşleme yok → alan bugün doldurulamaz · A7 Aşama A toprak/kanopi maskesi olmadan bahçede sistematik yanlış-pozitif (fıstık demo ürünü)

**Sensör:** S2 edge alt-kümesi `[ABSOLUTE,RELATIVE]` E13'ten BAĞIMSIZ olarak zaten tutarsız (intake 4, worker 5 değer) · S3 `DLS2_RELATIVE` satıcıya özgü ürün adı (MicaSense DLS 2); M3M'de sensör var ama DLS2 değil · S4 `ABSOLUTE`+`PANEL_ABSOLUTE` aynı alt-kümede + mekanizma alanı/ref yok · S5 ölçek FAKTÖRÜ taşınmıyor (`scale_factor` contract'ta VAR, bağ yok); NDVI gizler, EVI/SAVI sessizce bozulur · S6 paket-düzeyi tek `reflectance_scale` heterojen `outputs[]` ile çelişiyor (DSM metre, CWSI birimsiz, ORTHO 8-bit) · S7 RGB kare ayırt edilemez (`band` yokluğu iki şeyi kodluyor)

**ML/DS:** M5 `spot_check` dışlaması gerekçeyi TERSİNE çeviriyor — kesişimi yasaklamak koşullandırmayı yaratır (`P(denetim|spot_check)=0 ≠ P(denetim)`) · M6 çift yönlü `const` bağı "hem eskale hem denetim" ve 2. tur denetimi ifade edilemez kılıyor (MNAR) · M7 `confidence_score` için MINOR-uyumlu TAM kapanış mevcut: `if/then` içinde `{"const": 0}`

**Pentest:** P1 sertleştirilmiş desen çalışma zamanında HİÇ zorlanmıyor (Pydantic gevşek + şema doğrulaması `enforce=False` gözlem modu); erişilebilir küme bucket'taki her `.jpg/.png`

**Mimari:** AR2 KR-093 sahiplik yönü platformun kendi beyanıyla çatışıyor + bitişik KR-092 kaydı tam ters konvansiyonu yazıyor · AR3 CLAUDE.md'nin YENİ "düzeltilmiş" KR tablosu ölçümle YANLIŞ (48 `###` + 6 `##` = 54; iç içe, tamamlayıcı değil) · AR4 parite kapısı CI'da tamamen ATIL (45 test skip) · AR5 bu tur C-PARİTE'nin temizlediği yanlış iddiayı iki şemada geri getirdi

**QA:** Q2 `test_calibrated_manifest_fields` 18/18 CI'da SESSİZCE atlanıyor (`pyyaml` yok) · Q3 parite 45/56 atlanıyor · Q4 yeni 156 testin %40'ı CI'da koşmuyor · Q5 `test_data_layer_kr_present_in_ssot_text` KR-088/091 için TAMAMEN BOŞ · Q6 `## KR-093`→`### KR-093` 29 testi geçiyor; registry çıkarıcısı tanımların %89'unu görmüyor · Q7 CI `paths:` filtresi yeni testlerin okuduğu kaynakları kapsamıyor

**SDLC:** SD3 breaking kapısı `continue-on-error: true` → hiç bloke etmiyor · SD4 "beklenen tek kırmızı" izole değil, `summary`'ye sızıyor → PR sert bloke · SD5 `verify-checksums` `summary.needs`'te yok · SD6 parite kapısı CI'da ölü · SD7 `PENDING_PROPAGATION` release checklist'inde yok · SD8 checklist'te annotated tag adımı YOK; 4 etiket / 20 sürüm → **I-2 bugün yalan**

**KVKK:** K1 `{tenant}` opak değil (`coop-diyarbakir` örneği; `ahmet-yilmaz` de geçer); anahtar presigned URL'e girer · K2 plan §0'ın veri yönetişimi yükümlülüğü eyleme dönüşmemiş (listedeki tek atlanan satır) · K3 üç yeni veri kategorisi KR-090 saklama politikasının dışında · K4 `validate.py` FORBIDDEN_FIELDS sözleşmenin kendi iddiasının gerisinde + `api/` hiç taranmıyor (orada `phone` var)

**Edge:** E4 E11 C8'den önce merge edilirse `additionalProperties:false` → CHECK 1 → `REJECTED_QUARANTINE` (geri dönüş YOK) · E5 `relative_path` deseni gerçek ODM çıktısını (`odm_orthophoto.original.tif`), GDAL yan dosyalarını, boşluklu/Türkçe klasörleri reddediyor; desen E7 ölçümünden ÖNCE donduruldu · E6 `maxItems:5000` tek 25 m uçuşunu karşılamıyor (5.229 kare) · E7 `raw_frames[].footprint_wkt` ≈ atomik GPS; 5000 kare = tam uçuş rotası (HC-02/HC-08); uyarı notu `priority_zones.geom`'da VAR, burada YOK · E9 E10'un dosya listesinde `package_assembler.py` eksik → görsel M1'den çıkmaz

**GIS:** G2 `raw_frames[].footprint_wkt` doğrulanamaz (GPS/irtifa/yaw/GSD şemada yok) · G3 `geom` geçersiz poligonu kabul ediyor (9/9: bowtie, UTM metre, kapanmamış halka…) · G4 `ST_SetSRID(...,4326)` yanlış CRS'i sessizce damgalıyor; sütunda `ST_IsValid` yok · G5 `ndvi_overlay` PNG'si georeferanssız, `geom` ile bağı sözleşmede tanımsız (üretici UTM penceresi okuyor → meridyen yakınsaması 2,11°'ye kadar)

---

## 3. ÇATIŞMA ADAYLARI (senkronizasyon ajanına girdi)

| # | Taraflar | Konu |
|---|---|---|
| Ç1 | **A** (onayladı) ↔ **M5** (tersine çeviriyor) | `spot_check` karşılıklı dışlaması i.i.d.'yi korur mu, bozar mı? |
| Ç2 | **K9** (ORTA) ↔ **P** (bulgu yok) | `audit_stratum` quasi-identifier riski gerçek mi? |
| Ç3 | **S2** (C6'yı E13'ten ayır, şimdi yap) ↔ **plan/E13** (E13 önce) | C6 sıralaması |
| Ç4 | **M7** (`const:0` ile MINOR tam kapanış) ↔ **SD11** (deprecation penceresi başlat) ↔ **AL-C3** (v2'ye ertele) | `confidence_score` |
| Ç5 | **A8/A10** (alt-sınıflandırma + SAVI core'a) ↔ **S10/S11** (matrise `index_requirements`) | `layer_type` bant-gate çözümü |
| Ç6 | **AR12** (`xfail(strict)`) ↔ **SD4** (marker + `-m "not release_gate"`) ↔ **Q1** (şimdi re-pin) | Tur boyunca kırmızı CI |
| Ç7 | **G2** (parametreleri ekle ya da "kanıt değil" işaretle) ↔ **E7** (HC-02: `sees_patch_ids[]` tercih et) ↔ **K7/P3** (maxLength) | `footprint_wkt`'in akıbeti |
| Ç8 | **AR3** (iki kaynak iç içe) ↔ **benim CLAUDE.md düzeltmem** (tamamlayıcı) | KR kaynak ilişkisi |

---

## 4. YAKINSAMALAR (bağımsız disiplinler aynı boşluğa)

| # | Disiplinler | Ortak boşluk |
|---|---|---|
| Y1 | M1 · P4 · A5/A6 · G(dolaylı) | Denetim örnekleminin **seçim kanıtı** ve **stratum ekseni** tel üzerinde yok/uyumsuz |
| Y2 | G2 · K7 · P3 · E7 | `footprint_wkt`: doğrulanamaz + sınırsız + DoS + konum ifşası |
| Y3 | AR4 · SD6 · Q3 · E14 | Kanonik↔vendored sapmayı **hiçbir kapı CI'da görmüyor** (contract skip, edge öz-göndergeli) |
| Y4 | A8/A10 · S10/S11 | `layer_type`'ta bant-gereksinimi/üretilebilirlik mekanizması yok |
| Y5 | SD1/SD2 · Q(mutasyon V7/V8) | Dedektör + parite kapısı **enum ve tip** eksenlerini görmüyor |
| Y6 | AR1 · A1/A3 · K5 | KR-093 metni: çelişkili ikili tanım + tanımsız `stress_ratio` + eksik saklama/rıza MUST'ları |

---

*Konsolide denetim raporu. Yapılacak işler: eylem planı §14. Bu dosya kanıt arşividir.*
