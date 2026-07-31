# TarlaAnaliz SSOT — KR Registry (Kanonik)

> **Versiyon notu (2026-02-24 — sync with SSOT v1.2.0):**  
> - KR-015 başlığı drone-agnostik olarak güncellendi  
> - KR-021, 027, 028, 033: "yıllık abonelik" → "Sezonluk Paket" terminolojisi düzeltildi  
> - KR-030, KR-061: drone politikası drone-agnostik listeye güncellendi  
> - KR-033 normatif özeti: `PAID` durum makinesi, otomatik expire kaldırma, IBAN in-app dekont bilgisi eklendi  
> - KR-040 applies-to: platform-only → contracts, edge-kiosk, platform, worker  
> _Önceki versiyon: kr_registry_OPTIMAL_2026-02-14_v7.md_


## KR Domain Paketleri İndeksi (Navigasyon)

**KR Şablonu (Kanonik):**
1) Amaç
2) Kapsam / Applies-to
3) Zorunluluklar (MUST) — test edilebilir maddeler
4) Kanıt / Artefact (manifest, raporlar, sertifika, event)
5) Audit / Log (olay adları + correlation_id)
6) Hata Modları / Quarantine kararları
7) Test / Kabul Kriterleri (E2E senaryolar)
8) Cross-refs (ilgili KR’ler)

**Not:** Bu bölüm sadece navigasyon içindir. Asıl normatif metin her KR başlığının altındadır.

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

### KR-000

**Başlık:** Bu doküman seti nasıl okunur?  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** Saha adımları ve DJI entegrasyon ayrıntıları ayrı bir SOP dokümanında tutulur

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-001

**Başlık:** Proje Özeti  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** *Amaç:** Çiftçilerin ürün kaybını erken uyarı ile azaltmak ve dönüm bazlı analiz hizmeti satmak. Başlangıç bölgesi GAP, ardından Türkiye geneline ölçekleme.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-002

**Başlık:** Harita Katmanı Anlamları (Renk + Desen)  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** | Katman | Renk | Desen |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-010

**Başlık:** Web (PWA) - Genel  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** 

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-011

**Başlık:** Kullanıcı Rolleri ve Temel Yaklaşım  
**Applies to:** edge-kiosk, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** | Rol | Sorumluluk |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-012

**Başlık:** İş Planlaması  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** 

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-013

**Başlık:** Çiftçi Üyeliği ve Tarla Yönetimi  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** *Üyelik:** PWA veya web üzerinden üye olunur. İl, ilçe, ad, soyad ve telefon numarası alınır; üye olunca kendi sayfasına yönlendirilir.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-014

**Başlık:** Kooperatif/Üretici Birliği Üyeliği ve İşleyiş  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** *Doğrulama:** Hesap 'Onay Bekliyor' açılır. Evrak kontrolü sonrası Merkez yönetim 'Aktif' yapar; eksik evrak varsa aktif edilemez.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-015

**Başlık:** Drone Pilotları (Desteklenen Drone/Sensör Kombinasyonları ile Uçuş)  
**Applies to:** edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** **Üyelik/Kayıt:** İl, ilçe, ad soyad, telefon; drone modeli ve seri numarası; hizmet verdiği mahalle/köy listesi (başlangıçta opsiyonel). Drone seri numarası doğrulama referansıdır. Desteklenen drone/sensör kombinasyonları drone_registry.yaml'a kayıtlı olmalıdır (DJI Mavic 3M birincil/önerilen; DJI M350 RTK+Sentera 6X, WingtraOne Gen II+MicaSense RedEdge-P, Parrot Anafi USA+Sequoia+, AgEagle eBee X+Altum-PT desteklenir). Bkz. KR-034 (DJI risk planı).

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-016

**Başlık:** Drone - Tarla - Bitki Eşleştirme Politikası (Routing)  
**Applies to:** worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** *Amaç:** Veri setini doğru FieldID ve o tarihte geçerli bitki türü ile eşleştirip doğru bitki-özel YZ modelini otomatik seçmek.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-017

**Başlık:** YZ Modeli ile Analiz (Şemsiye Kural)  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:**
- AnalysisJob semantiği: `FieldID + CropType + MissionID (varsa)`; **PII yok**.
- Edge tarafında model çalıştırılmaz (model theft riski).
- Worker inbound kapalıdır; job **pull/poll** ile kuyruktan alınır; sonuçlar **tek yönlü** yayınlanır.
- KR-017, aşağıdaki KR’lerle operasyonel olarak ayrıştırılır:
  - [KR-070] Worker izolasyonu + egress allowlist (network policy)
  - [KR-071] One-way data flow + allowlist Ingress’te + mTLS cihaz kimliği
  - [KR-072] Dataset lifecycle + chain-of-custody (manifest/hash/signature/verification)
  - [KR-073] Untrusted file handling + AV1/AV2 + sandbox + quarantine
- Kalibrasyon hard gate: [KR-018 / KR-082] sağlanmadan job çalışmaz.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md`
- Platform: bkz. `platform_ssot.md`
- Edge-Kiosk: bkz. `edgekiosk_ssot.md`
- Worker: bkz. `worker_ssot.md`

---
### KR-018

**Başlık:** Tam Radyometrik Kalibrasyon Zorunluluğu (Radiometric Calibration: ışık/sensör etkilerini düzeltme)  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** Model eğitimi (training: modelin öğrenmesi) ve saha sonuçları arasında tutarlılık (training-serving parity: eğitim/çalıştırma aynı dağılım).

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-019

**Başlık:** Expert Portal (Uzman İnceleme)
**Applies to:** platform, worker
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** Uzman portalı, modelin düşük güven verdiği veya çelişkili durumlarda manuel inceleme için kullanılır (**PII görünmez**)

**5 Eskalasyon Tetikleyicisi (BİRİ yeterli):**
1. `final_confidence < dynamic_threshold[crop][analysis_type]` — dinamik eşik (KARAR-13)
2. `agreement_score < 0.6` — DualHead çelişkisi
3. `cosine_sim < 0.3` — OOD tespiti (FAISS embedding store)
4. `epistemic_uncertainty > 0.4` — MC-Dropout yüksek model belirsizliği
5. `expert_verdict == "needs_more_expert"` — döngü re-trigger (aktif öğrenme bütünlüğü)

**Dinamik Threshold (KARAR-13):**
- Kaynak: `config/dynamic_thresholds.yaml` (crop × analysis_type bazlı)
- `global_floor = 0.80` — mutlak alt sınır, threshold_adjuster.py aşağı inemez
- `initial_threshold = 0.75` — 50 feedback öncesi tüm crop'lar
- `pamuk.disease = 0.82` — özel: ilk 6 hafta (Türkiye MS verisi sıfır)
- `max_adjustment_delta = ±0.05` — tek güncellemede maksimum değişim
- `min_feedback_count = 50` — güncelleme için minimum feedback

**Fail-Closed Seviyeler (Worker → Platform hizalı):**

| Confidence Aralığı | Worker ResultMode | Platform EscalationLevel | Eskalasyon |
|---------------------|-------------------|--------------------------|------------|
| ≥ dynamic_threshold | FULL_REPORT | NONE | Yok |
| 0.45 – dynamic_threshold | PARTIAL_REPORT | STANDARD | Evet |
| 0.25 – 0.45 | INDICES_ONLY | PRIORITY | Evet |
| < 0.25 | NO_RESULT | CRITICAL | ACİL |

**Sorumluluk ayrımı:**
- **Worker:** 5 tetikleyiciyi değerlendirir, ResultMode belirler, eskalasyon paketi üretir (field_id YOK — KR-071)
- **Platform:** Eskalasyon paketini alır, EscalationLevel belirler, expert atar. Worker'ın escalation_reasons'ını severity booster olarak kullanır (OOD/epistemic → seviye yükseltme).

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-020

**Başlık:** Ücretlendirme  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** 

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-021

**Başlık:** Genel Prensip  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Ücretler bitki türü ve analiz seçeneğine göre: tek seferlik analiz veya **Sezonluk Paket**

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-022

**Başlık:** Fiyat Yönetimi Politikası  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Fiyatlar uygulamada serbest **yazılmaz**; tek kaynak **PriceBook** (Fiyat Kataloğu)

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-023

**Başlık:** Örnek Fiyat Kurgusu (Pamuk)  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** | Seçenek | Liste Fiyat | İlk Yıl / Abonelik Kurgusu |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-024

**Başlık:** Önerilen Tarama Periyodu (Gün)  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** | Bitki | Önerilen Periyot (gün) |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-025

**Başlık:** Analiz İçeriği (Hizmet Kapsamı)  
**Applies to:** worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** *Temel İlke:** Sistem ilaçlama kararı **vermez**; yalnızca tespit, risk skoru ve erken uyarı sağlar.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-026

**Başlık:** Sunum Biçimi  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Harita katmanları (ısı haritası / grid / zonlama)

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-027

**Başlık:** Abonelik Planlayıcı (Subscription Scheduler)  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, DEV

**Normatif özet:** **Amaç:** **Sezonluk Paket** seçen kullanıcılar için otomatik, periyodik Mission üretimi.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-028

**Başlık:** Mission Yaşam Döngüsü ve SLA Alanları  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, DEV

**Normatif özet:** **Mission Tanımı:** Bir tarlanın belirli bir tarihte yapılacak tek analiz görevi. Tek seferlik talepten veya **Sezonluk Paket**'ten oluşabilir.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-029

**Başlık:** YZ Eğitim Geri Bildirimi (Training Feedback Loop)  
**Applies to:** contracts, platform, worker  
**Kaynaklar:** SSOT, DEV

**Normatif özet:** *Amaç:** Uzman düzeltmelerini YZ modeline geri beslemek ve model iyileştirmesi yapmak.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-030

**Başlık:** Notlar, Sınırlar ve Uyum  
**Applies to:** edge-kiosk, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** **Drone standardı:** Drone-agnostik mimari. Desteklenen modeller drone_registry.yaml'a kayıtlı olmalıdır (DJI Mavic 3M birincil/önerilen; M350 RTK+Sentera 6X, WingtraOne Gen II+MicaSense RedEdge-P, Parrot Anafi USA+Sequoia+, AgEagle eBee X+Altum-PT). Bkz. KR-034 (DJI risk planı). KVKK: PII ile operasyon verisi ayrıdır. Model çıktısı karar değildir.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-031

**Başlık:** Pilot Hakediş ve Ödeme Politikası  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Pilotlar, bir ay içinde **ONAYLANMIŞ** görevlerde taradıkları alan üzerinden hakediş kazanır

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-032

**Başlık:** Training Export Standardı  
**Applies to:** contracts, platform, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** *Amaç:** Uzman feedback'lerini standart formatta export ederek model eğitim pipeline'ına aktarmak.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-033

**Başlık:** Ödeme ve Manuel Onay (Müşteri Tahsilat Akışı)
**Applies to:** contracts, platform, worker
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** **Amaç:** Tek seferlik Mission veya **Sezonluk Paket Subscription** taleplerinde tahsilat standartlaştırma. Durum: `PAYMENT_PENDING`→`PAID`/`REJECTED`/`CANCELLED`; `PAID`→`REFUNDED`. Otomatik expire yoktur. IBAN dekont uygulama içi yüklenir; e-posta kanal değildir. Tüm geçişler `PaymentStateMachine` üzerinden — bypass yasaktır.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-040

**Başlık:** Güvenlik Kabul Kriterleri/Test Checklist (SDLC Entegrasyonu)  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** **Amaç:** Savunma-derinliği (defense-in-depth) güvenlik yaklaşımını, ölçülebilir kabul kriterlerine ve SDLC kapılarına (PR/CI/Release/Ops) bağlamak. PR/CI/Release/Ops kapıları tüm bileşenleri (contracts, edge-kiosk, platform, worker) kapsar; yalnızca platform değildir.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-041

**Başlık:** SDLC Kapıları (Gate) - Zorunlu Kontroller  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Contracts pinleme: CONTRACTS_VERSION (SemVer) + CONTRACTS_SHA256 zorunlu; değişiklikte breaking-change kontrolü

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-042

**Başlık:** Kabul Kriterleri Matrisi  
**Applies to:** edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** | Güvenlik Katmanı | Kabul Kriteri (DoD) | Test Kanıtı | SDLC Gate |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-043

**Başlık:** Test Checklist (Senaryo Bazlı)  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** | Senaryo | Adımlar (özet) | Beklenen Sonuç | Kanıt/Artefakt |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-050

**Başlık:** Kimlik Doğrulama ve Üyelik Akışı (Sade Model)
**Applies to:** contracts, worker
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Kimlik bilgisi olarak yalnızca **Telefon Numarası** kullanılır (E-posta ve TCKN **toplanmaz**)

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-060

**Başlık:** Ürün/Teknik Spesifikasyondan Normatif  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** 

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-061

**Başlık:** Amaç ve Sabit Çerçeve  
**Applies to:** platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Drone-agnostik mimari. DJI Mavic 3M birincil/önerilen; desteklenen diğer modeller drone_registry.yaml'a kayıtlıdır. Bkz. KR-001 (radyometri notu) ve KR-034 (DJI bağımsızlık planı).

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-062

**Başlık:** Tasarım İlkeleri  
**Applies to:** edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** 1. **Tek kaynak gerçek:** API ve veri modeli. Web (PWA) iş kuralı kopyalamaz.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-063

**Başlık:** Roller ve Yetkiler (RBAC)  
**Applies to:** edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** | Rol Kodu | Kısa Tanım | Özet Yetki |

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-064

**Başlık:** Harita Katman Standardı (Layer Registry)  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** Katmanlar web (PWA) arayüzünde aynı Layer Registry üzerinden tanımlanır. Renk + desen/ikon + opaklık + öncelik tutarlı olmalıdır.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-065

**Başlık:** Pilot Hakediş Doğrulama (Expected vs Observed)  
**Applies to:** platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** **Expected Area:** FieldBoundary veya Mission flightplan sınırı (m²)

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-066

**Başlık:** Güvenlik ve KVKK  
**Applies to:** edge-kiosk, platform  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** PII ayrı veri alanında tutulur; raporlama ve KPI katmanı pseudonymous kimliklerle çalışır

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-070

**Başlık:** YZ Analiz İzolasyonu (Worker Isolation & Egress Policy)
**Kapsam / Applies-to:** worker

**1) Amaç**
- (Kanonik) Güvenlik ve veri akışı kuralını test edilebilir hale getirmek.

**2) Zorunluluklar (MUST)**
**Kaynaklar:** SSOT, KANONIK

**Normatif kurallar (Hard):**
1) Worker **inbound kapalıdır** (deny-by-default). “ingest/upload” HTTP endpoint’i **yoktur**.  
2) Worker job’ı **pull/poll** ile alır (queue/dispatch). Platform→Worker push **yok**.  
3) Worker egress **allowlist** ile sınırlıdır:  
   - Object Storage (S3-uyumlu) → **read-only**  
   - Queue/Dispatch → **consume-only**  
   - Observability → **append-only**  
   - Internet → **DENY**  
4) Worker job çalıştırmadan önce **precondition** doğrular:  
   - `CALIBRATED` kanıtı (**[KR-018]**)  
   - manifest/hash/(varsa signature) + AV raporları + verification (**[KR-072]**, **[KR-073]**)  
5) Ops erişimi: bastion + MFA + JIT; yönetim portları public internete açılmaz.

**Network Policy Matrix:**
- Platform → Worker: **DENY**
- Web/PWA → Worker: **DENY**
- Worker → Storage/Queue/Results/Observability: **ALLOW (outbound only, mTLS)**
- Worker → Internet: **DENY**

**Audit/WORM olayları (minimum):**
- `SECURITY.DENY`, `JOB.REJECT`, `DATASET.REJECTED_QUARANTINE`

**SDLC Gate / Test (minimum):**
- Policy deny test (platform→worker TCP)  
- Calibrated yok → job reject  
- Hash mismatch → quarantine  
- Contracts CI validate + breaking-change detector (**[KR-081]**)

---

**4) Kanıt / Artefact**
- Üretilen raporlar/manifestler/sertifikalar ve referanslar (KR-072/KR-073 ile).

**5) Audit / Log**
- SECURITY.DENY / JOB.REJECT / HASH.MISMATCH vb. olaylar; correlation_id zorunlu.

**6) Hata Modları / Quarantine**
- Şüpheli/tamper/malware → REJECTED_QUARANTINE; işlem durur ve kanıt üretilir.

**7) Test / Kabul Kriterleri**
- Negatif testler: inbound denemeleri reddedilir; eksik kanıtla job reddedilir; hash mismatch yakalanır.

**8) Cross-refs**
- KR-017 (şemsiye), KR-018 (kalibrasyon), KR-070..KR-073 (akış/kanıt).

---
### KR-071

**Başlık:** Tek Yönlü Veri Akışı + Allowlist Yerleşimi (One-way Data Flow)
**Kapsam / Applies-to:** edge-kiosk, platform, worker

**1) Amaç**
- (Kanonik) Güvenlik ve veri akışı kuralını test edilebilir hale getirmek.

**2) Zorunluluklar (MUST)**
**Kaynaklar:** SSOT, KANONIK

**Kanonik akış (Hard):**
1) EdgeKiosk → Platform/Ingress: HTTPS 443 + **mTLS cihaz kimliği** (client cert).  
2) Platform: ham veriyi public API’de servis etmez; storage + queue üzerinden orkestrasyon yapar.  
3) Worker: queue/storage’dan **pull** eder; analiz eder.  
4) Worker → Platform: sadece **türev sonuç** (AnalysisResult/layers) yazar.  
5) Web/PWA: sadece sonuç okur; ham veri **yok**.

**Allowlist yerleşimi:**
- IP allowlist **kimlik değildir** (dinamik IP/CGNAT).  
- Allowlist yalnızca **Ingress kapısında** ikincil katmandır. Ana kontrol **mTLS**’tir.

**SDLC Test (minimum):**
- allowlist dışı IP → deny + audit  
- sertifikasız istek → deny + audit  
- worker’a direct HTTP → deny (policy)

---

**4) Kanıt / Artefact**
- Üretilen raporlar/manifestler/sertifikalar ve referanslar (KR-072/KR-073 ile).

**5) Audit / Log**
- SECURITY.DENY / JOB.REJECT / HASH.MISMATCH vb. olaylar; correlation_id zorunlu.

**6) Hata Modları / Quarantine**
- Şüpheli/tamper/malware → REJECTED_QUARANTINE; işlem durur ve kanıt üretilir.

**7) Test / Kabul Kriterleri**
- Negatif testler: inbound denemeleri reddedilir; eksik kanıtla job reddedilir; hash mismatch yakalanır.

**8) Cross-refs**
- KR-017 (şemsiye), KR-018 (kalibrasyon), KR-070..KR-073 (akış/kanıt).

---
### KR-072

**Başlık:** Dataset Lifecycle + Kanıt Zinciri (Chain of Custody) — Contract-First
**Kapsam / Applies-to:** contracts, edge-kiosk, platform, worker

**1) Amaç**
- (Kanonik) Güvenlik ve veri akışı kuralını test edilebilir hale getirmek.

**2) Zorunluluklar (MUST)**
**Kaynaklar:** SSOT, KANONIK

**Dataset durumları (minimum):**
`RAW_INGESTED` → `RAW_SCANNED_EDGE_OK` → `RAW_HASH_SEALED` → `CALIBRATED` (**[KR-018]**) →  
`CALIBRATED_SCANNED_CENTER_OK` → `DISPATCHED_TO_WORKER` → `ANALYZED` → `DERIVED_PUBLISHED` → `ARCHIVED`  
Hata/şüphe: `REJECTED_QUARANTINE`

**Zorunlu kanıt artefact’leri:**
- `dataset_manifest.json` + `manifest.sha256` + (opsiyonel) `signature.sig`
- `scan_report_edge.json` (AV1)
- `scan_report_center.json` (AV2)
- `verification_report.json` (hash match/mismatch)
- `calibration_result.json` + `qc_report.json`
- `evidence_bundle_ref` (platform sonuçlarında sadece referans)

**Hard gate:**
- Hash mismatch / AV fail / QC fail → `REJECTED_QUARANTINE`
- `CALIBRATED_SCANNED_CENTER_OK` olmadan Worker job kabul etmez.

**Contract-first:**
- Şemalar `tarlaanaliz-contracts` altında JSON Schema + örnekler + CI doğrulama (**[KR-081]**)

---

**4) Kanıt / Artefact**
- Üretilen raporlar/manifestler/sertifikalar ve referanslar (KR-072/KR-073 ile).

**5) Audit / Log**
- SECURITY.DENY / JOB.REJECT / HASH.MISMATCH vb. olaylar; correlation_id zorunlu.

**6) Hata Modları / Quarantine**
- Şüpheli/tamper/malware → REJECTED_QUARANTINE; işlem durur ve kanıt üretilir.

**7) Test / Kabul Kriterleri**
- Negatif testler: inbound denemeleri reddedilir; eksik kanıtla job reddedilir; hash mismatch yakalanır.

**8) Cross-refs**
- KR-017 (şemsiye), KR-018 (kalibrasyon), KR-070..KR-073 (akış/kanıt).

---
### KR-073

**Başlık:** Untrusted File Handling + AV1/AV2 + Sandbox Dönüştürme
**Kapsam / Applies-to:** contracts, edge-kiosk, platform, worker

**1) Amaç**
- (Kanonik) Güvenlik ve veri akışı kuralını test edilebilir hale getirmek.

**2) Zorunluluklar (MUST)**
**Kaynaklar:** SSOT, KANONIK

**Normatif kurallar (Hard):**
- Ham dosyalar (TIFF/JPEG/RAW vb.) **untrusted input** kabul edilir. Parse/convert işlemleri sandbox’ta yapılır.
- **AV1 EdgeKiosk** + **AV2 Merkez Security Gateway** zorunludur.
- AV/verification olmadan dataset bir sonraki duruma geçemez (**[KR-072]**).
- Güvenli türev (tiles/COG/thumbnail) üretimi merkezde sandbox işçisinde yapılır; platform public ham servis etmez.

**Quarantine:**
- AV fail / hash mismatch / QC fail → `REJECTED_QUARANTINE` + audit.

**SDLC Test (minimum):**
- (Lab) EICAR tetiklemesi  
- AV1 PASS ama AV2 FAIL → quarantine  
- Sandbox crash olmadan kontrollü hata

---

**4) Kanıt / Artefact**
- Üretilen raporlar/manifestler/sertifikalar ve referanslar (KR-072/KR-073 ile).

**5) Audit / Log**
- SECURITY.DENY / JOB.REJECT / HASH.MISMATCH vb. olaylar; correlation_id zorunlu.

**6) Hata Modları / Quarantine**
- Şüpheli/tamper/malware → REJECTED_QUARANTINE; işlem durur ve kanıt üretilir.

**7) Test / Kabul Kriterleri**
- Negatif testler: inbound denemeleri reddedilir; eksik kanıtla job reddedilir; hash mismatch yakalanır.

**8) Cross-refs**
- KR-017 (şemsiye), KR-018 (kalibrasyon), KR-070..KR-073 (akış/kanıt).

---
### KR-080

**Başlık:** Ana İş Akışları için Teknik Kurallar  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK

**Normatif özet:** Bu bölüm; ana iş akışlarının iş planı anlatısında zaten bulunan kısımlarını tekrar etmez. Sadece teknik spesifikasyonda eklenen/sertleştirilen kuralları listeler.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-081

**Başlık:** Kontrat Şemaları (Contract-First) — Kanonik JSON Schema  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** *Amaç:** "olmalı" seviyesinden çıkıp, kodlamadan önce ortak dilin **makine-doğrulanabilir** (machine-verifiable) hale gelmesi.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-082

**Başlık:** RADIOMETRY / Radyometrik Kalibrasyon (Uyumluluk Etiketi)  
**Applies to:** contracts, edge-kiosk, platform, worker  
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** Bu madde, **[KR-018] Tam Radyometrik Kalibrasyon Zorunluluğu** ile **aynı zorunluluğu** “KR-082” etiketiyle de referanslayabilmek için eklenmiştir.

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-083

**Başlık:** İl Operatörü
**Applies to:** platform
**Kaynaklar:** SSOT, KANONIK, DEV

**Normatif özet:** *Rol Kodu:** ProvinceOperator

**Component dokümanları:**
- Contracts: bkz. `contracts_ssot.md` (bu KR contracts kapsamındaysa)
- Platform: bkz. `platform_ssot.md` (bu KR platform kapsamındaysa)
- Edge-Kiosk: bkz. `edgekiosk_ssot.md` (bu KR edge-kiosk kapsamındaysa)
- Worker: bkz. `worker_ssot.md` (bu KR worker kapsamındaysa)

---
### KR-084

**Başlık:** Termal Veri İşleme ve Sulama Stresi Analizi (Thermal Pipeline)
**Applies to:** contracts, worker, platform (rapor katmanı)
**Kaynaklar:** SSOT, KANONIK

**1) Amaç**
- Termal bant (LWIR 8–14 μm) mevcut olduğunda sulama stresi, su yönetimi ve erken dönem bitki sağlığı sorunlarını görünür bantlardan önce tespit etmek; termal bant yoksa analiz akışını etkilememek (graceful degradation).

**2) Zorunluluklar (MUST)**

1) Termal pipeline yalnızca `intake_manifest.available_bands[]` içinde `LWIR` bant tanımı varsa etkinleşir. Termal bant yoksa bu KR'nin hiçbir kuralı uygulanmaz.
2) Termal kalibrasyon gereksinimleri sensör tipine göre belirlenir:
   - **Altum-PT (FLIR Boson 320×256):** Fabrika radyometrik kalibrasyon sertifikası + Pix4Dfields termal kalibrasyon pipeline'ı.
   - **Sentera 6X Thermal (FLIR Boson 640):** Fabrika radyometrik kalibrasyon + ILS düzeltmesi.
3) Termal kalibrasyon kanıtı `calibration_result.json` içinde `thermal_calibration` bölümünde tutulur.
4) Worker termal analiz çıktıları: Canopy sıcaklık haritası (°C), CWSI (0.0–1.0), canopy-soil sıcaklık deltası, sulama etkinliği göstergesi.
5) Termal katmanlar `THERMAL_STRESS` LayerCode ile raporda sunulur (bkz. KR-064).
6) Termal verinin çözünürlüğü MS'den düşüktür; Worker termal katmanı MS çözünürlüğüne yeniden örnekler.

**4) Kanıt / Artefact**
- `calibration_result.json` → `thermal_calibration{}` bölümü
- `thermal_analysis_result.json` (CWSI haritası + canopy temp + delta)
- `qc_report.json` → `thermal_qc{}` (sıcaklık aralığı makul mü, sensör drift var mı)

**5) Audit / Log**
- `THERMAL.PIPELINE_ACTIVATED`, `THERMAL.CALIBRATION_VERIFIED`, `THERMAL.QC_PASS/WARN/FAIL`, `THERMAL.RESULT_PUBLISHED`

**6) Hata Modları / Quarantine**
- Termal kalibrasyon kanıtı eksik/geçersiz → `THERMAL.QC_FAIL` → termal pipeline devre dışı, MS pipeline normal devam
- Sıcaklık değerleri fiziksel olarak anlamsız aralıkta (< -20°C veya > 70°C) → `THERMAL.QC_WARN` → admin inceleme

**7) Test / Kabul Kriterleri**
- Termal bant olmayan manifest ile job → termal pipeline etkinleşmez
- Termal bant + kalibrasyon kanıtı eksik → `THERMAL.QC_FAIL` + termal katman üretilmez
- Termal bant + kalibrasyon OK → CWSI haritası + canopy temp katmanı üretilir
- CWSI değerleri 0.0–1.0 aralığında

**8) Cross-refs**
- KR-018/KR-082 (spektral kapasite), KR-017 (şemsiye), KR-072 (dataset lifecycle), KR-064 (layer registry)

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

## KR-092 — Fenolojik/Sezonluk Uçuş Parametreleri (İrtifa & Hız)

> **Versiyon notu (2026-07-05):** Yeni KR — sezonluk (haftalık) uçuş parametreleri; tarama protokolü v1.6 §10'dan türetilir. Kanonik normatif metin platform SSOT'undadır (`docs/TARLAANALIZ_SSOT_v1_2_0.txt` KR-092); burada contract yüzeyi referanslanır, çoğaltılmaz.

**1) Amaç**
Bir görevin uçuş yüksekliği (Y) ve hızı (v) değerlerini bitki türü + sezon haftasına (fenolojik evre) göre türetmek; hedef GSD tutturularak analiz kalitesini sabitlemek. Sonuç pilota ekranda o hafta öne çıkarılıp tam sezon tablosuyla ve KMZ uçuş planına gömülü olarak teslim edilir.

**2) Kapsam / Applies-to:** platform, worker, edge-kiosk, contracts

**3) Zorunluluklar (MUST)**
1) 5 aktif GAP ürünü (COTTON/CORN/RICE/GRAPE/PISTACHIO; CORN kanonik, MAIZE legacy alias — crop_type aliases CORN↔MAIZE) için **tek yetkili kaynak** haftalık sezon takvimidir (`data/seasonal_flight_calendar.json`); bu ürünlerde haftalık takvim, evre-bazlı fenoloji fallback'inden (`data/phenology_flight_profiles.json`) önceliklidir.
2) Çözüm anahtarı `crop_type` + `mission_date` → bölgesel haftalık pencere (MM-DD) → (bbch, altitude_m, speed_ms, critical); yeni DB "ekim tarihi" alanı eklenmez.
3) Fiziksel/mevzuat sınırları fail-closed doğrulanır: RGB GSD=H/37,2 · ÇS GSD=H/21,7, **H/v ≥ 3,9**, **≤ 120 m AGL** (SHGM), güneş açısı > 30°.
4) Görev tarihi sezona düşmezse en yakın sınır haftasına snap edilir (matched=false); kapsam dışı bitkide haftalık DTO None döner (çağıran fenoloji/varsayılana düşer).
5) CRP radyometrik kalibrasyonu her uçuş başı+sonu zorunludur (KR-018/082 hard-gate); karar desteğidir, sistem ilaçlama kararı vermez (KR-025).

**4) Kanıt / Artefact**
- Veri: `data/seasonal_flight_calendar.json` (kanonik haftalık takvim)
- Contract şeması: `schemas/core/seasonal_flight_calendar.v1.schema.json` (bu repo; SeasonalFlightCalendar)
- Domain: `seasonal_flight_calendar.py` (VO), `seasonal_flight_planner.py` (servis), `seasonal_flight_calendar_loader.py` (loader)
- DTO/Contract: `WeeklyFlightDTO`, `SeasonWeekDTO`, `SeasonFlightScheduleDTO`
- API: `GET /missions/{id}/season-flight-schedule`, `weekly_flight` alanı (mission + pilot mission response), `GET /missions/{id}/flight-route.kmz` (Y/v gömülü)

**5) Audit / Log**
- Loader olayları: `SEASONAL_CALENDAR_MISSING` / `READ_FAILED` / `PARSE_SKIP` / `LOADED`
- Snap/fallback notu DTO içinde taşınır (`FLIGHT.PARAMS_FALLBACK`)

**6) Hata Modları**
- Takvim dosyası yok/bozuk → ilgili ürün atlanır (parse-skip), diğer ürünler yüklenir; negatif cache zehirlenmesi önlenir.
- Fiziksel sınır ihlali (Y>120 veya H/v<3,9) → VO kurulumunda `SeasonalFlightCalendarError` (fail-closed).
- Kapsam dışı bitki → 404 (season-flight-schedule) veya `weekly_flight=None` (mission response).
- IDOR: sezon takvimi erişimi KMZ ile aynı sahiplik/atama kontrolüne tabidir (farmer sahip / atanmış pilot / admin).

**7) Test / Kabul Kriterleri**
- COTTON Hafta-11 (06-22..06-28) → altitude_m=35, speed_ms=5, critical=true.
- Sezon dışı tarih → en yakın haftaya snap (matched=false).
- 5 GAP ürününde KMZ Y/v takvimden gelir (varsayılan 50/5 override edilir); kapsam dışı bitkide fenoloji fallback.
- Kapsam dışı bitkide `GET /season-flight-schedule` → 404.
- Yetkisiz kullanıcı (sahip/atanmış pilot/admin değil) → 403.

**8) Cross-refs**
- KR-024 (fenoloji fallback), KR-016 (uçuş rotası/KMZ), KR-018 (kalibrasyon hard-gate), KR-082 (kalibrasyon sertifikası), KR-025 (karar desteği sınırı), KR-015 (pilot planlama)

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

