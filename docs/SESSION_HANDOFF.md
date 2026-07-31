# Oturum Devir Notu (Session Handoff)

> Amaç: Farklı bilgisayarlar arasında çalışırken **oturum durumunu** taşımak.
> Yerel makine hafızası taşınmaz; bu dosya repo ile GitHub üzerinden senkronize olur.
> **Bir sonraki oturumda önce bu dosyayı oku.**

**Son güncelleme:** 2026-07-31

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

## 0.B EN GÜNCEL OTURUM (2026-07-31, ikinci oturum) — **KADEME 0 kapandı**

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

### 🔴 SONRAKİ OTURUMUN İLK İŞİ — **KADEME 1 (D7 · D8 · D9)**
Eylem planı **§14.1**: `raw_frames[].footprint_wkt` → `sees_patch_ids[]` (Ç7 tek hamle) ·
C6a `calibration_type` fail-closed · Ç5 `layer_type` zinciri.
⏳ **Maliyet penceresi:** D9② (`IRRIGATION_EFFICIENCY` → `CANOPY_TEMP_UNIFORMITY`) ve D7
(`footprint_wkt` kaldırma) **bu tur bedava**, sonra MAJOR olur.

**Ayrıca karar bekleyen tek KADEME 0 kalemi: D4-b** — parite kapısı CI'da hâlâ ölçüm
yapmıyor (kardeş depolar Actions'ta yok). Ya CI'a çapraz-repo erişimi verilir ya
"parite yalnız C8'de yerel ölçülür" **yazılı** kabul edilir.

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
> **Kaynak devir spesi:** `tarlaanaliz-worker/denetim/audit_escalation_reason_devir_spec_2026_07_19.md`
> (worker'ın karar-hazır devri — **platform seçer, worker uydurmaz**).
> **Neden değiştiği:** `denetim/denetim_raporu_2026-07-31_plan_devir_ozdenetim.md` (kanıt arşivi).

### Doğrulama (bu oturumda geçti)
`python tools/check_no_egeanaliz.py` → OK · `python tools/validate.py` → **0 hata, ALL VALIDATIONS PASSED**
*(Not: bu oturumda şema/enum **değiştirilmedi** — yalnız `docs/` altına iki doküman eklendi.)*

### Depo hijyeni
- `aktif_ogrenme_*.md` (2 dosya) proje kökünden → **`tarlaanaliz-worker/denetim/`** taşındı
  (sürüm kontrolüne alındı; onlara atıf yapan `audit_escalation_reason_devir_spec` ile aynı dizin).
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
