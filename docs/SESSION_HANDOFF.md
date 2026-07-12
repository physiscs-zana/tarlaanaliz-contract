# Oturum Devir Notu (Session Handoff)

> Amaç: Farklı bilgisayarlar arasında çalışırken oturum durumunu taşımak.
> Yerel makine hafızası taşınmaz; bu dosya repo ile GitHub üzerinden senkronize olur.
> **Bir sonraki oturumda önce bu dosyayı oku.**

**Son güncelleme:** 2026-07-12

---

## 0. EN GÜNCEL OTURUM (2026-07-12) — Platform öneri denetimi + 6.2.0 & 7.0.0

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

- **Kontrat sürümü (CONTRACTS_VERSION.md):** `7.0.0` — Breaking: **YES** (phenology_stage MAIZE_*→CORN_* rename)
  - Checksum (SHA-256): `efe437efeca2d3ee894f1965353fbed42c8d9fb9ad3374d5061a503c6ef93caa`
  - 7.0.0 rename commit'i: `c0fa705`. Ondan önce 6.2.0 (bant-gate tek-kaynak + v1 deprecation) commit'i: `d5f18b9`.
  - Checksum yalnız `schemas/`+`enums/`+`api/` ağacını kapsar; CHANGELOG.md / docs/ değişiklikleri
    (bu handoff dahil) checksum'ı DEĞİŞTİRMEZ. `git log` daha yeni bir head gösterirse (ör. bu
    oturum-kapanış handoff commit'i) bu normaldir.
- **Tek çalışma deposu:** `.../TARLA-ANALİZ/tarlaanaliz-contract` (origin = `github.com/physiscs-zana/tarlaanaliz-contract`)

### Dallar / PR durumu — 2026-07-12 itibarıyla

| Öğe | Durum | Not |
|---|---|---|
| `master` | `c0fa705` | Güncel referans dal (7.0.0); 2 commit ileride (d5f18b9=6.2.0, c0fa705=7.0.0) |
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

## 3. Tüketici (consumer) Durumu — 2026-07-12

| Servis | Sürüm | Senkron | Not |
|---|---|---|---|
| **Contract (SSOT)** | `7.0.0` (c0fa705) | — | master; checksum `efe437ef…` |
| **Platform** | 4.3.0 pin (submodule 82d2fd8) | ⚠ GERİDE (4.3.0 → 7.0.0) | 6.2.0 + 7.0.0'a re-pin gerekli; checksum `efe437ef…` |
| **Worker** | `v5.1.1` (bağımsız şema + kendi hash gate) | ⚠ AKSİYON | phenology_stage tüketiyorsa MAIZE_*→CORN_* aynı turda hizalanmalı (7.0.0 breaking) |
| **Edge** | `1.2.0` (bağımsız pin + kendi hash gate) | Temiz | phenology_stage tüketmez; 7.0.0 rename edge'i etkilemez |

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

---

## 5. Bilgisayarlar Arası Notlar

- Yeni makinede başlarken: `git fetch origin --prune` → dalların `[ahead/behind]` durumunu kontrol et.
- Kalıcı bilgi **repoya** yazılmalı (bu dosya gibi); Claude'un yerel hafızası makineye özeldir, taşınmaz.
- **Eşzamanlı oturum uyarısı:** worker'a bu oturumda dal+PR yöntemiyle yazıldı (PR #118, `469e7d7`;
  §3.4); artık senkron/temiz. Yine de başka makine yazmadan önce `git fetch --prune` ile `[ahead/behind]`
  doğrula (çakışma riski).
- Doğrulama komutu (değişiklik sonrası): `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -v`.
