# TarlaAnaliz SSOT — KR Registry (Navigasyon + Kapsam Dizini)

> 🔗 **BU DOSYA NORMATİF GÖVDE TAŞIMAZ (2026-08-01, D16-b2).**
> Her KR'nin **tek** normatif metni `docs/TARLAANALIZ_SSOT_v1_2_0.txt`'tedir; burada
> yalnız **başlık + `Applies to` + `Kaynaklar`** durur ve her başlık kanonik metne
> işaret eder. Çelişkide **kanonik metin kazanır**.
>
> **İstisna — gövdesi BURADA yaşayan 4 KR:** `KR-088`, `KR-089`, `KR-090`, `KR-091`.
> Bunlar SSOT metninde tanımlı **değildir** (ölçüldü); orada yalnız tek satırlık bir
> çapraz-atıfla anılırlar. Tanımları buradan silinirse tamamen kaybolur.
>
> **Neden (ölçümle, tahminle değil):** D16-b2 turunda 49 gövdenin tamamı ölçüldü —
> hiçbiri kanonik metne normatif madde eklemiyordu; **41'i türetilmiş özet**, 6'sı
> kanonik metnin **alt kümesi**, 2'si (`KR-019`, `KR-092`) gerçek içerik taşıyordu ve
> o içerik kanonik metne **taşındı** (artı `KR-072`'nin `evidence_bundle_ref` maddesi).
> Dahası **üç gövde fiilen yanlıştı**: `KR-083` kaldırılmış rol adını (*İl Operatörü*)
> tek başına taşıyordu — canlı kodda halefi `DISTRICT_REP`; `KR-027` başlığı
> "Abonelik Planlayıcı"da donmuştu; `KR-000` "DJI entegrasyonu" diyordu (mimari
> drone-agnostik). İkili gövdenin sessizce bayatladığının kanıtı budur (AR1).
>
> Kural: bir KR'nin kuralı **önce kanonik metinde** değişir, sonra buraya yansır.
> Kapı: `tests/test_single_normative_body.py` — yeni ikili gövde CI'da kırmızıya döner.

> **Versiyon notu (2026-02-24 — sync with SSOT v1.2.0):**  
> - KR-015 başlığı drone-agnostik olarak güncellendi  
> - KR-021, 027, 028, 033: "yıllık abonelik" → "Sezonluk Paket" terminolojisi düzeltildi  
> - KR-030, KR-061: drone politikası drone-agnostik listeye güncellendi  
> - KR-033 normatif özeti: `PAID` durum makinesi, otomatik expire kaldırma, IBAN in-app dekont bilgisi eklendi  
> - KR-040 applies-to: platform-only → contracts, edge-kiosk, platform, worker  
> _Önceki versiyon: kr_registry_OPTIMAL_2026-02-14_v7.md_


## KR Domain Paketleri İndeksi (Navigasyon)

**KR Şablonu (Kanonik) — kanonik metinde bir KR gövdesi yazılırken izlenen 8 bölüm:**
1) Amaç
2) Kapsam / Applies-to
3) Zorunluluklar (MUST) — test edilebilir maddeler
4) Kanıt / Artefact (manifest, raporlar, sertifika, event)
5) Audit / Log (olay adları + correlation_id)
6) Hata Modları / Quarantine kararları
7) Test / Kabul Kriterleri (E2E senaryolar)
8) Cross-refs (ilgili KR’ler)

**Not:** Bu bölüm de, altındaki KR başlıkları da **yalnız navigasyon** içindir. Normatif
metin `docs/TARLAANALIZ_SSOT_v1_2_0.txt`'tedir (istisna: KR-088/089/090/091 — yukarı bak).

### A) Security & Isolation
- KR-070 — Worker Isolation & Egress Policy
- KR-071 — One-way Data Flow + Allowlist Yerleşimi (Ingress)
- KR-073 — Untrusted File Handling + AV1/AV2 + Sandbox

### B) Data Lifecycle & Evidence (Chain of Custody)
- KR-072 — Dataset Lifecycle + Kanıt Zinciri (manifest/hash/signature/verification)
- KR-018 — Radiometric Calibration Hard Gate (QC + Certificate)
- KR-081 — Contract-First / Schema Gates (CI)

### C) Orchestration & Operations
- KR-017 — YZ Analiz Hattı (Şemsiye KR: 070–073 ayrıştırması)
- KR-015 — Pilot kapasite/planlama alt kuralları

### D) Payments & Governance
- KR-033 — Ödeme + Manuel Onay + Audit


**Tarih:** 2026-02-02  
**Amaç:** KR kodlarını tekil, izlenebilir ve bileşenler arası tutarlı tutmak.

## Temel kurallar (cross-ref standardı)

1) **Kanonik kimlik:** Her iş kuralı tek bir **[KR-xxx]** kimliğine sahiptir.  
2) **Alias (uyumluluk etiketi):** Tarihsel/harici dokümanlar başka bir KR kodu kullanıyorsa, bu kod **alias** olarak tutulur ve **kanonik KR**’ye bağlanır. Alias **yeni normatif metin üretmez**.  
3) **Component SSOT’lar (filtered view):**  
   - `contracts_ssot.md`, `platform_ssot.md`, `edgekiosk_ssot.md`, `worker_ssot.md` dosyaları KR üretmez.  
   - Sadece bu registry’den **kendine düşen KR’leri** listeler ve *bileşen özel uygulama notu* ekler.  
4) **Referans biçimi:** Metinde her zaman `[KR-018]` gibi yazılır.  
   - Eğer alias kullanılıyorsa: `[KR-082] (alias of KR-018)` şeklinde belirtilir.  
5) **Değişiklik kuralı:** Bir KR’nin anlamı değişecekse aynı kodu “kaydırma” yapma.  
   - Ya KR’nin sürüm notunu yaz,  
   - Ya yeni KR aç, eskisini “deprecated” et.

## KR haritası (kanonik tablo)

| KR | Başlık | Applies To | Kaynaklarda Geçiş | Kısa normatif özet |
| --- | --- | --- | --- | --- |
| [KR-000](#kr-000) | Bu doküman seti nasıl okunur? | contracts, edge-kiosk, platform, worker | SSOT, KANONIK, DEV | Saha adımları ve DJI entegrasyon ayrıntıları ayrı bir SOP dokümanında tutulur |
| [KR-001](#kr-001) | Proje Özeti | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | *Amaç:** Çiftçilerin ürün kaybını erken uyarı ile azaltmak ve dönüm bazlı analiz hizmeti satmak. Başlangıç bölgesi GAP, ardından Türkiye geneline ölçekleme. |
| [KR-002](#kr-002) | Harita Katmanı Anlamları (Renk + Desen) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK, DEV | \| Katman \| Renk \| Desen \| |
| [KR-010](#kr-010) | Web (PWA) - Genel | platform | SSOT, KANONIK |  |
| [KR-011](#kr-011) | Kullanıcı Rolleri ve Temel Yaklaşım | edge-kiosk, worker | SSOT, KANONIK | \| Rol \| Sorumluluk \| |
| [KR-012](#kr-012) | İş Planlaması | platform | SSOT, KANONIK |  |
| [KR-013](#kr-013) | Çiftçi Üyeliği ve Tarla Yönetimi | platform, worker | SSOT, KANONIK | *Üyelik:** PWA veya web üzerinden üye olunur. İl, ilçe, ad, soyad ve telefon numarası alınır; üye olunca kendi sayfasına yönlendirilir. |
| [KR-014](#kr-014) | Kooperatif/Üretici Birliği Üyeliği ve İşleyiş | platform, worker | SSOT, KANONIK | *Doğrulama:** Hesap 'Onay Bekliyor' açılır. Evrak kontrolü sonrası Merkez yönetim 'Aktif' yapar; eksik evrak varsa aktif edilemez. |
| [KR-015](#kr-015) | Drone Pilotları (Desteklenen Drone/Sensör Kombinasyonları ile Uçuş) | edge-kiosk, platform, worker | SSOT, KANONIK | **Üyelik/Kayıt:** İl, ilçe, ad soyad, telefon; drone modeli ve seri numarası; hizmet verdiği mahalle/köy listesi (başlangıçta opsiyonel). Drone seri numarası doğrulama referansıdır. Desteklenen modeller drone_registry.yaml'a kayıtlı olmalıdır. |
| [KR-016](#kr-016) | Drone - Tarla - Bitki Eşleştirme Politikası (Routing) | worker | SSOT, KANONIK | *Amaç:** Veri setini doğru FieldID ve o tarihte geçerli bitki türü ile eşleştirip doğru bitki-özel YZ modelini otomatik seçmek. |
| [KR-017](#kr-017) | YZ Modeli ile Analiz | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | *Veri Akışı:** "FieldID + bitki türü + MissionID; PII yok" bu bilgiler sadece uçuş yapacak drone pilotuna ve hafıza kartlarına işlenir. |
| [KR-018](#kr-018) | Tam Radyometrik Kalibrasyon Zorunluluğu (Radiometric Calibration: ışık/sensör etkilerini düzeltme) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK, DEV | Model eğitimi (training: modelin öğrenmesi) ve saha sonuçları arasında tutarlılık (training-serving parity: eğitim/çalıştırma aynı dağılım). |
| [KR-019](#kr-019) | Expert Portal (Uzman İnceleme) | platform, worker | SSOT, KANONIK, DEV | Uzman portalı, modelin düşük güven verdiği veya çelişkili durumlarda manuel inceleme için kullanılır (**PII görünmez**) |
| [KR-020](#kr-020) | Ücretlendirme | platform | SSOT, KANONIK |  |
| [KR-021](#kr-021) | Genel Prensip | platform, worker | SSOT, KANONIK | Ücretler bitki türü ve analiz seçeneğine göre: tek seferlik analiz veya **Sezonluk Paket** |
| [KR-022](#kr-022) | Fiyat Yönetimi Politikası | platform | SSOT, KANONIK | Fiyatlar uygulamada serbest **yazılmaz**; tek kaynak **PriceBook** (Fiyat Kataloğu) |
| [KR-023](#kr-023) | Örnek Fiyat Kurgusu (Pamuk) | platform, worker | SSOT, KANONIK | \| Seçenek \| Liste Fiyat \| İlk Yıl / Abonelik Kurgusu \| |
| [KR-024](#kr-024) | Önerilen Tarama Periyodu (Gün) | platform | SSOT, KANONIK | \| Bitki \| Önerilen Periyot (gün) \| |
| [KR-025](#kr-025) | Analiz İçeriği (Hizmet Kapsamı) | worker | SSOT, KANONIK | *Temel İlke:** Sistem ilaçlama kararı **vermez**; yalnızca tespit, risk skoru ve erken uyarı sağlar. |
| [KR-026](#kr-026) | Sunum Biçimi | platform | SSOT, KANONIK | Harita katmanları (ısı haritası / grid / zonlama) |
| [KR-027](#kr-027) | Abonelik Planlayıcı (Subscription Scheduler) | platform, worker | SSOT, DEV | **Amaç:** **Sezonluk Paket** seçen kullanıcılar için otomatik, periyodik Mission üretimi. |
| [KR-028](#kr-028) | Mission Yaşam Döngüsü ve SLA Alanları | platform, worker | SSOT, DEV | **Mission Tanımı:** Bir tarlanın belirli bir tarihte yapılacak tek analiz görevi. Tek seferlik talepten veya **Sezonluk Paket**'ten oluşabilir. |
| [KR-029](#kr-029) | YZ Eğitim Geri Bildirimi (Training Feedback Loop) | contracts, platform, worker | SSOT, DEV | *Amaç:** Uzman düzeltmelerini YZ modeline geri beslemek ve model iyileştirmesi yapmak. |
| [KR-030](#kr-030) | Notlar, Sınırlar ve Uyum | edge-kiosk, worker | SSOT, KANONIK, DEV | **Drone standardı:** Drone-agnostik mimari. Desteklenen modeller drone_registry.yaml'a kayıtlı olmalıdır (DJI Mavic 3M birincil/önerilen; M350 RTK+Sentera 6X, WingtraOne Gen II+MicaSense RedEdge-P, Parrot Anafi USA+Sequoia+, AgEagle eBee X+Altum-PT). Bkz. KR-034 (DJI bağımsızlık planı). |
| [KR-031](#kr-031) | Pilot Hakediş ve Ödeme Politikası | platform | SSOT, KANONIK | Pilotlar, bir ay içinde **ONAYLANMIŞ** görevlerde taradıkları alan üzerinden hakediş kazanır |
| [KR-032](#kr-032) | Training Export Standardı | contracts, platform, worker | SSOT, KANONIK, DEV | *Amaç:** Uzman feedback'lerini standart formatta export ederek model eğitim pipeline'ına aktarmak. |
| [KR-033](#kr-033) | Ödeme ve Manuel Onay (Müşteri Tahsilat Akışı) | contracts, platform, worker | SSOT, KANONIK | **Amaç:** Tek seferlik Mission veya **Sezonluk Paket Subscription** taleplerinde tahsilat standartlaştırma. Durum: `PAYMENT_PENDING`→`PAID`/`REJECTED`/`CANCELLED`; `PAID`→`REFUNDED`. Otomatik expire yoktur. IBAN dekont uygulama içi yüklenir. |
| [KR-040](#kr-040) | Güvenlik Kabul Kriterleri/Test Checklist (SDLC Entegrasyonu) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | **Amaç:** TXT repo mantalitesindeki savunma-derinliği (defense-in-depth) güvenlik yaklaşımını, ölçülebilir kabul kriterlerine ve SDLC kapılarına (PR/CI/Release/Ops) bağlamak. PR/CI/Release/Ops kapıları tüm bileşenleri kapsar. |
| [KR-041](#kr-041) | SDLC Kapıları (Gate) - Zorunlu Kontroller | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | Contracts pinleme: CONTRACTS_VERSION (SemVer) + CONTRACTS_SHA256 zorunlu; değişiklikte breaking-change kontrolü |
| [KR-042](#kr-042) | Kabul Kriterleri Matrisi | edge-kiosk, platform, worker | SSOT, KANONIK | \| Güvenlik Katmanı \| Kabul Kriteri (DoD) \| Test Kanıtı \| SDLC Gate \| |
| [KR-043](#kr-043) | Test Checklist (Senaryo Bazlı) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | \| Senaryo \| Adımlar (özet) \| Beklenen Sonuç \| Kanıt/Artefakt \| |
| [KR-050](#kr-050) | Kimlik Doğrulama ve Üyelik Akışı (Sade Model) | contracts, worker | SSOT, KANONIK | Kimlik bilgisi olarak yalnızca **Telefon Numarası** kullanılır (E-posta ve TCKN **toplanmaz**) |
| [KR-060](#kr-060) | Ürün/Teknik Spesifikasyondan Normatif | platform | SSOT, KANONIK |  |
| [KR-061](#kr-061) | Amaç ve Sabit Çerçeve | platform, worker | SSOT, KANONIK | Drone-agnostik mimari. DJI Mavic 3M birincil/önerilen; desteklenen diğer modeller drone_registry.yaml'a kayıtlıdır. Bkz. KR-001 (radyometri notu) ve KR-034 (DJI bağımsızlık planı). |
| [KR-062](#kr-062) | Tasarım İlkeleri | edge-kiosk, platform, worker | SSOT, KANONIK | 1. **Tek kaynak gerçek:** API ve veri modeli. Web (PWA) iş kuralı kopyalamaz. |
| [KR-063](#kr-063) | Roller ve Yetkiler (RBAC) | edge-kiosk, platform, worker | SSOT, KANONIK | \| Rol Kodu \| Kısa Tanım \| Özet Yetki \| |
| [KR-064](#kr-064) | Harita Katman Standardı (Layer Registry) | platform | SSOT, KANONIK, DEV | Katmanlar web (PWA) arayüzünde aynı Layer Registry üzerinden tanımlanır. Renk + desen/ikon + opaklık + öncelik tutarlı olmalıdır. |
| [KR-065](#kr-065) | Pilot Hakediş Doğrulama (Expected vs Observed) | platform | SSOT, KANONIK | **Expected Area:** FieldBoundary veya Mission flightplan sınırı (m²) |
| [KR-066](#kr-066) | Güvenlik ve KVKK | edge-kiosk, platform | SSOT, KANONIK | PII ayrı veri alanında tutulur; raporlama ve KPI katmanı pseudonymous kimliklerle çalışır |
| [KR-070](#kr-070) | YZ Analiz İzolasyonu (Worker Isolation) | worker | SSOT, KANONIK | Inbound kapalı; egress allowlist; job pull; calibrated+evidence hard gate |
| [KR-071](#kr-071) | Tek Yönlü Veri Akışı + Allowlist Yerleşimi | edge-kiosk, platform, worker | SSOT, KANONIK | Allowlist Ingress’te; mTLS ana kontrol; akış Edge→Platform→Storage/Queue→Worker→Platform→Web |
| [KR-072](#kr-072) | Dataset Lifecycle + Kanıt Zinciri (Contract-First) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | Dataset state machine + manifest/hash/signature + AV1/AV2 + verification |
| [KR-073](#kr-073) | Untrusted File Handling + Malware (AV1/AV2) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | Sandbox parse/convert; iki aşamalı tarama; şüphelide quarantine |
| [KR-080](#kr-080) | Ana İş Akışları için Teknik Kurallar | contracts, edge-kiosk, platform, worker | SSOT, KANONIK | Bu bölüm; ana iş akışlarının iş planı anlatısında zaten bulunan kısımlarını tekrar etmez. Sadece teknik spesifikasyonda eklenen/sertleştirilen kuralları listeler. |
| [KR-081](#kr-081) | Kontrat Şemaları (Contract-First) — Kanonik JSON Schema | contracts, edge-kiosk, platform, worker | SSOT, KANONIK, DEV | *Amaç:** "olmalı" seviyesinden çıkıp, kodlamadan önce ortak dilin **makine-doğrulanabilir** (machine-verifiable) hale gelmesi. |
| [KR-082](#kr-082) | RADIOMETRY / Radyometrik Kalibrasyon (Uyumluluk Etiketi) | contracts, edge-kiosk, platform, worker | SSOT, KANONIK, DEV | Bu madde, **[KR-018] Tam Radyometrik Kalibrasyon Zorunluluğu** ile **aynı zorunluluğu** “KR-082” etiketiyle de referanslayabilmek için eklenmiştir. |
| [KR-083](#kr-083) | İl Operatörü | platform | SSOT, KANONIK, DEV | *Rol Kodu:** ProvinceOperator |
| [KR-084](#kr-084) | Termal Veri İşleme ve Sulama Stresi Analizi (Thermal Pipeline) | contracts, worker, platform | SSOT, KANONIK | Termal bant (LWIR) mevcut olduğunda sulama stresi analizi; yoksa graceful degradation. Çıktılar: CWSI, canopy temp, delta haritası. THERMAL_STRESS LayerCode (KR-064). |

---

## KR detayları

### KR-000 Bu doküman seti nasıl okunur?

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-000] Bu doküman seti nasıl okunur?`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-001 Proje Özeti

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-001] Proje Özeti`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-002 Harita Katmanı Anlamları (Renk + Desen)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-002] Harita Katmanı Anlamları (Renk + Desen)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-010 Web (PWA) - Genel

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-010] Web (PWA) - Genel`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-011 Kullanıcı Rolleri ve Temel Yaklaşım

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-011] Kullanıcı Rolleri ve Temel Yaklaşım`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-012 İş Planlaması

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-012] İş Planlaması`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-013 Çiftçi Üyeliği ve Tarla Yönetimi

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-013] Çiftçi Üyeliği ve Tarla Yönetimi`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-014 Kooperatif/Üretici Birliği Üyeliği ve İşleyiş

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-014] Kooperatif/Üretici Birliği Üyeliği ve İşleyiş`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-015 Drone Pilotları (Desteklenen Drone/Sensör Kombinasyonları ile Uçuş)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-015] Drone Pilotları (Desteklenen Drone/Sensör Kombinasyonları ile Uçuş)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-016 Drone - Tarla - Bitki Eşleştirme Politikası (Routing)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-016] Drone - Tarla - Bitki Eşleştirme Politikası (Routing)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-017 YZ Modeli ile Analiz (Şemsiye Kural)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-017] YZ Modeli ile Analiz (Kanonik: İzolasyon + Tek Yönlü Akış + Job Semantiği)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-018 Tam Radyometrik Kalibrasyon Zorunluluğu (Radiometric Calibration: ışık/sensör etkilerini düzeltme)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-018 / KR-082] RADIOMETRY - Tam Radyometrik Kalibrasyon Zorunluluğu + Spektral Kapasite Algılama (Radiometric Calibration + Spectral Capability Detection)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-019 Expert Portal (Uzman İnceleme)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-019] Expert Portal + Konsensüs Yayın Kapısı (Uzman İnceleme)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-020 Ücretlendirme

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-020] Ücretlendirme`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-021 Genel Prensip

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-021] Genel Prensip`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-022 Fiyat Yönetimi Politikası

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-022] Fiyat Yönetimi Politikası`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-023 Örnek Fiyat Kurgusu (Pamuk)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-023] Örnek Fiyat Kurgusu (Pamuk)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-024 Önerilen Tarama Periyodu (Gün)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-024] Önerilen Tarama Periyodu (Gün)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-025 Analiz İçeriği (Hizmet Kapsamı)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-025] Analiz İçeriği (Hizmet Kapsamı)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-026 Sunum Biçimi

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-026] Sunum Biçimi`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-027 Abonelik Planlayıcı (Subscription Scheduler)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-027] Sezonluk Paket Planlayıcı (Subscription Scheduler)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, DEV

---

### KR-028 Mission Yaşam Döngüsü ve SLA Alanları

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-028] Mission Yaşam Döngüsü ve SLA Alanları`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, DEV

---

### KR-029 YZ Eğitim Geri Bildirimi (Training Feedback Loop)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-029] YZ Eğitim Geri Bildirimi (Training Feedback Loop)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, platform, worker · **Kaynaklar:** SSOT, DEV

---

### KR-030 Notlar, Sınırlar ve Uyum

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-030] Notlar, Sınırlar ve Uyum`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-031 Pilot Hakediş ve Ödeme Politikası

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-031] Pilot Hakediş ve Ödeme Politikası`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-032 Training Export Standardı

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-032] Training Export Standardı`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-033 Ödeme ve Manuel Onay (Müşteri Tahsilat Akışı)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## # [KR-033] Ödeme ve Manuel Onay (Müşteri Tahsilat Akışı)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-040 Güvenlik Kabul Kriterleri/Test Checklist (SDLC Entegrasyonu)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-040] Güvenlik Kabul Kriterleri/Test Checklist (SDLC Entegrasyonu)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-041 SDLC Kapıları (Gate) - Zorunlu Kontroller

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-041] SDLC Kapıları (Gate) - Zorunlu Kontroller`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-042 Kabul Kriterleri Matrisi

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-042] Kabul Kriterleri Matrisi`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-043 Test Checklist (Senaryo Bazlı)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-043] Test Checklist (Senaryo Bazlı)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-050 Kimlik Doğrulama ve Üyelik Akışı (Sade Model)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-050] Kimlik Doğrulama ve Üyelik Akışı (Sade Model)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-060 Ürün/Teknik Spesifikasyondan Normatif

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-060] Ürün/Teknik Spesifikasyondan Normatif`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-061 Amaç ve Sabit Çerçeve

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-061] Amaç ve Sabit Çerçeve`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-062 Tasarım İlkeleri

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-062] Tasarım İlkeleri`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-063 Roller ve Yetkiler (RBAC)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-063] Roller ve Yetkiler (RBAC)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-064 Harita Katman Standardı (Layer Registry)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-064] Harita Katman Standardı (Layer Registry)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-065 Pilot Hakediş Doğrulama (Expected vs Observed)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-065] Pilot Hakediş Doğrulama (Expected vs Observed)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-066 Güvenlik ve KVKK

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-066] Güvenlik ve KVKK`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, platform · **Kaynaklar:** SSOT, KANONIK

---

### KR-070 YZ Analiz İzolasyonu (Worker Isolation & Egress Policy)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-070] YZ Analiz İzolasyonu (Worker Isolation & Egress Policy)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-071 Tek Yönlü Veri Akışı + Allowlist Yerleşimi (One-way Data Flow)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-071] Tek Yönlü Veri Akışı (One-way data flow) + Allowlist Yerleşimi`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-072 Dataset Lifecycle + Kanıt Zinciri (Chain of Custody) — Contract-First

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-072] Dataset Lifecycle (Veri Yaşam Döngüsü) + Kanıt Zinciri (Chain of Custody) — Contract-First`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-073 Untrusted File Handling + AV1/AV2 + Sandbox Dönüştürme

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-073] Untrusted File Handling + Malware (AV1/AV2) + Güvenli Dönüştürme`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-080 Ana İş Akışları için Teknik Kurallar

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-080] Ana İş Akışları için Teknik Kurallar`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK

---

### KR-081 Kontrat Şemaları (Contract-First) — Kanonik JSON Schema

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-081] Kontrat Şemaları (Contract-First) — Kanonik JSON Schema`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-082 RADIOMETRY / Radyometrik Kalibrasyon (Uyumluluk Etiketi)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-018 / KR-082] RADIOMETRY - Tam Radyometrik Kalibrasyon Zorunluluğu + Spektral Kapasite Algılama (Radiometric Calibration + Spectral Capability Detection)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, edge-kiosk, platform, worker · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-083 İl Operatörü

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-083] İlçe Temsilcisi`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** platform · **Kaynaklar:** SSOT, KANONIK, DEV

---

### KR-084 Termal Veri İşleme ve Sulama Stresi Analizi (Thermal Pipeline)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-084] Termal Veri İşleme ve Sulama Stresi Analizi (Thermal Pipeline)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

**Applies to:** contracts, worker, platform (rapor katmanı) · **Kaynaklar:** SSOT, KANONIK

---

## KR-088 — Field Index Timeseries (Tarla Zaman Serisi Vejetasyon İndeksleri)

> **Versiyon notu (2026-03-29):** Yeni KR — veri katmanı genişleme projesi kapsamında.

**1) Amaç**
Her başarılı analiz sonucunda tarla bazlı vejetasyon indeksleri, sağlık metrikleri ve tespit istatistiklerini zaman serisi olarak saklamak. Çiftçilerin tarla sağlık trendlerini görmesini ve sezonlar arası karşılaştırma yapmasını sağlamak.

**2) Kapsam / Applies-to:** platform

**3) Zorunluluklar (MUST)**
1) Worker analysis_result payload'undan otomatik olarak timeseries kaydı oluşturulur.
2) Sadece `result_mode ∈ {FULL_REPORT, PARTIAL_REPORT}` olan sonuçlar dahil edilir (KR-019 fail-closed uyumu).
3) `status ∉ {COMPLETED, SUCCESS}` olan sonuçlar için timeseries kaydı YAZILMAZ.
4) Timeseries kaydı, Dataset + Mission güncellemesi ile AYNI transaction'da atomik olarak yazılır.
5) UNIQUE constraint: (field_id, mission_id) — aynı tarla+görev çifti tekrar yazılamaz.
6) health_score aralığı: 0-100 (contract ResultSummary.health_score ile uyumlu).
7) ndvi_mean, ndre_mean, ndwi_mean kolonları NULL kabul eder (worker inference implement olana kadar).

**4) Kanıt / Artefact**
- `field_index_timeseries` PostgreSQL tablosu
- Alembic migration: `YYYYMMDD_kr088_field_index_timeseries.py`

**5) Audit / Log**
- Platform worker_bridge_consumer log: `WORKER_BRIDGE.TIMESERIES_WRITTEN field_id=... mission_id=...`

**6) Hata Modları**
- UNIQUE constraint violation (duplicate) → log warning, skip (idempotent)
- Transaction failure → tüm işlem rollback (Dataset, Mission, Timeseries)

**7) Test / Kabul Kriterleri**
- COMPLETED result → timeseries kaydı oluşturuldu
- FAILED result → timeseries YAZILMADI
- NO_RESULT mode → timeseries YAZILMADI
- Duplicate mission_id → UNIQUE hata, log warning
- Atomik rollback testi: timeseries hata → Dataset/Mission de rollback

**8) Cross-refs**
- KR-019 (fail-closed maskeleme), KR-017 (analiz hattı), KR-091 (dashboard), KR-090 (retention)

---

## KR-089 — Field History (Tarla Yaşam Döngüsü Olay Günlüğü)

> **Versiyon notu (2026-03-29):** Yeni KR — veri katmanı genişleme projesi kapsamında.

**1) Amaç**
Her tarla için kronolojik olay günlüğü tutmak: analiz teslimleri, hastalık/zararlı/ot tespitleri, sağlık değişimleri, bitki değişimleri, abonelik olayları. Çiftçinin "bu tarlada ne oldu?" sorusunu cevaplayabilmek.

**2) Kapsam / Applies-to:** platform

**3) Zorunluluklar (MUST)**
1) 16 kanonik event tipi: field_history_event_type.enum.v1.json ile tanımlıdır.
2) mission_id ve analysis_result_id FK olarak DEĞİL, referans UUID olarak saklanır. Gerekçe: retention politikası eski result'ları sildiğinde history kayıtları korunmalıdır.
3) field_id FK → ON DELETE CASCADE (tarla silinirse geçmişi de silinir).
4) ANALYSIS_DELIVERED event'i her başarılı sonuçta (status ∈ {COMPLETED, SUCCESS}) otomatik yazılır.
5) DISEASE_DETECTED, PEST_DETECTED, WEED_DETECTED event'leri sadece HIGH/CRITICAL severity tespitlerde yazılır.
6) HEALTH_DECLINED/IMPROVED event'leri önceki timeseries kaydıyla delta ≥ ±10 karşılaştırmasıyla yazılır.

**4) Kanıt / Artefact**
- `field_history` PostgreSQL tablosu
- Alembic migration: `YYYYMMDD_kr089_field_history.py`

**5) Audit / Log**
- `WORKER_BRIDGE.FIELD_HISTORY_WRITTEN field_id=... event_type=... count=...`

**6) Hata Modları**
- İlk ölçüm → trend karşılaştırma yapılamaz → HEALTH_DECLINED/IMPROVED yazılmaz (normal)
- Transaction failure → rollback (timeseries ile birlikte)

**7) Test / Kabul Kriterleri**
- Başarılı result → ANALYSIS_DELIVERED event var
- HIGH severity hastalık → DISEASE_DETECTED event var
- LOW severity hastalık → event YOK
- İlk ölçüm → HEALTH_DECLINED/IMPROVED YOK
- İkinci ölçüm, health 85→60 → HEALTH_DECLINED event var (delta=-25)

**8) Cross-refs**
- KR-088 (timeseries, trend kaynağı), KR-091 (dashboard uyarıları), KR-090 (retention — history SÜRESİZ)

---

## KR-090 — Retention Policy (Veri Yaşam Döngüsü Yönetimi)

> **Versiyon notu (2026-03-29):** Yeni KR — veri katmanı genişleme projesi kapsamında.

**1) Amaç**
Verilerin yaşam döngüsünü yöneterek DB boyutu ve S3 depolama maliyetini kontrol altında tutmak. Yasal zorunlulukları (WORM audit, tarla geçmişi) korurken eski analiz sonuçlarını kademeli olarak arşivlemek/silmek.

**2) Kapsam / Applies-to:** platform

**3) Zorunluluklar (MUST)**
1) analysis_results: 730 gün sonra DB'den silinebilir (timeseries'te özeti zaten var).
2) S3 GeoTIFF: 365 gün HOT, sonra GLACIER_IR'a geçiş.
3) S3 tile cache: 180 gün sonra silinir (COG'dan yeniden üretilebilir).
4) audit_logs: ASLA silinmez (WORM yasal zorunluluk).
5) field_history: ASLA silinmez.
6) field_index_timeseries: ASLA silinmez (trend verisi değerli).
7) analysis_results silmeden ÖNCE timeseries'te karşılığının varlığı doğrulanır.
8) İlk çalıştırma dry_run() modunda yapılır (silmeden rapor).

**4) Kanıt / Artefact**
- `config/retention_policy.yaml`
- `retention_service.py`

**5) Audit / Log**
- `RETENTION.CYCLE_COMPLETED records_deleted=... bytes_freed=...`
- `RETENTION.DRY_RUN records_eligible=...`

**6) Hata Modları**
- Timeseries'te karşılık yok + result silme girişimi → backfill önce, sonra sil
- S3 lifecycle rule uygulanamadı → log error, bir sonraki döngüde tekrar dene

**7) Test / Kabul Kriterleri**
- dry_run() doğru kayıtları seçiyor
- WORM tabloları korunuyor
- 730 gün öncesi result silinebiliyor, 729 gün öncesi silinmiyor

**8) Cross-refs**
- KR-088 (timeseries koruma), KR-089 (history koruma), KR-062 (audit WORM)

---

## KR-091 — Aggregation Dashboard (Çiftçi/Bölge/Kooperatif Dashboard)

> **Versiyon notu (2026-03-29):** Yeni KR — veri katmanı genişleme projesi kapsamında.

**1) Amaç**
Çiftçi, ilçe temsilcisi ve kooperatif yöneticisi için tarla/bölge bazlı sağlık özetleri, trend uyarıları ve istatistik dashboardları sunmak.

**2) Kapsam / Applies-to:** platform

**3) Zorunluluklar (MUST)**
1) Dashboard verileri field_index_timeseries tablosundan beslenir (KR-088).
2) Sadece result_mode ∈ {FULL_REPORT, PARTIAL_REPORT} olan kayıtlar dahil edilir (KR-019).
3) RBAC kontrolleri:
   - Çiftçi dashboardı: sadece kendi tarlaları (user_id eşleşmesi)
   - İlçe dashboardı: DISTRICT_REP rolü + ilçe eşleşmesi
   - Kooperatif dashboardı: COOP_OWNER veya COOP_ADMIN rolü
4) Uyarılar: health_score delta ≤ -10 → HEALTH_DECLINED uyarısı gösterilir.
5) Bölge ortalamaları: province + district bazlı AVG(health_score) hesaplanır.

**4) Kanıt / Artefact**
- `aggregation_service.py`
- API endpoints: /dashboard/farmer, /dashboard/district, /dashboard/coop/{id}

**5) Audit / Log**
- Standart API erişim logları (audit_logs tablosunda)

**6) Hata Modları**
- Hiç timeseries verisi yok → boş dashboard dönülür (500 değil)
- RBAC ihlali → HTTP 403

**7) Test / Kabul Kriterleri**
- Farmer başka farmer'ın dashboardını göremez (403)
- DISTRICT_REP sadece kendi ilçesini görür
- Boş timeseries → boş response (crash yok)
- result_mode=NO_RESULT dahil edilmemiş

**8) Cross-refs**
- KR-088 (veri kaynağı), KR-019 (fail-closed filtre), KR-083 (temsilci rolü), KR-014 (kooperatif)

---

### KR-092 Fenolojik/Sezonluk Uçuş Parametreleri (İrtifa & Hız)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-08-01, D16-b2).**
> Kanonik metin: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-092] Fenolojik/Sezonluk Uçuş Parametreleri (İrtifa & Hız)`
> Çelişkide **o kazanır**; bu başlık yalnız navigasyon + kapsam bilgisi taşır.

---

## KR-093 — Çiftçi Ön Raporu (İki-Fazlı Teslimat: PRELIMINARY → FULL)

> 🔗 **TÜRETİLMİŞ İŞARETÇİ — normatif gövde BURADA DEĞİL (2026-07-31, D16-b).**
> KR-093'ün tek normatif metni: **`docs/TARLAANALIZ_SSOT_v1_2_0.txt` → `## [KR-093]`**.
>
> **Karar gerekçesi (ölçümle, tahminle değil):**
> 1. **Her iki dosyanın da alt-akış kopyaları BAYAT.** Ölçüldü: `kr_registry.md`'nin platform
>    (`docs/kr/`, `contracts/ssot/`) ve worker (`docs/reference/`) kopyalarının **hiçbirinde**
>    KR-093 başlığı yok; SSOT metninin platform kopyası da contract'tan farklı. Yani dağıtım
>    kâğıt üzerinde var, içerikte yok.
> 2. **Fark: senkron MEKANİZMASI.** SSOT metni C-SSOT turunda bayt-özdeş hâle getirildi ve
>    `tests/test_kr_reference_integrity.py` onu koruyor. `kr_registry.md` için **hiçbir senkron
>    aracı yok** (`tools/sync_to_repos.sh` yalnız `schemas/`+`enums/`+`CONTRACTS_VERSION.md`
>    taşır — plan kalemi C-SSOT-2). Tutulamayan bir kaynağı normatif ilan etmek, çürümeyi
>    kurala dönüştürmektir.
> 3. **Kayıp yok:** bu dosyaya özgü iki MUST maddesi — *"Aşama A tespit değildir"* ve
>    *"yeni mission state / yeni faz eklenmez"* — ve Aşama A içerik listesi (kaynak:
>    `analysis_priority_zones`) SSOT metnine **taşındı**; ortak maddeler zaten oradaydı.
>
> ⚠️ Bu başlık altına **yeniden gövde yazılmaz** — `tests/test_single_normative_body.py`
> ikili gövde borcunu dondurur ve yeni ikili gövdeyi kırmızıya çevirir.

---

