# Oturum Devir Notu (Session Handoff)

> Amaç: Farklı bilgisayarlar arasında çalışırken oturum durumunu taşımak.
> Yerel makine hafızası taşınmaz; bu dosya repo ile GitHub üzerinden senkronize olur.
> **Bir sonraki oturumda önce bu dosyayı oku.**

**Son güncelleme:** 2026-07-05

---

## 1. Depo Durumu (Snapshot)

- **Kontrat sürümü (CONTRACTS_VERSION.md):** `4.3.0` — Breaking: **NO** (eklemeli/additive)
  - Checksum (SHA-256): `7295e395723746c03d1438885a307b1df6cb75d2f1357db9edffb2c5b3ee801c`
  - 4.3.0 içerik-merge commit'i: `82d2fd8` (PR #19). Checksum bu ağaca pinli.
  - Sonraki commit'ler **yalnız-doküman** (bu handoff izleme + docs/ temizliği); checksum'ı
    DEĞİŞTİRMEZ. `git log` farklı bir head gösterirse (ör. bu oturum-kapanış commit'i) bu normaldir.
- **Tek çalışma deposu:** `.../TARLA-ANALİZ/tarlaanaliz-contract` (origin = `github.com/physiscs-zana/tarlaanaliz-contract`)

### Dallar / PR durumu — 2026-07-05 itibarıyla

| Öğe | Durum | Not |
|---|---|---|
| `master` | `82d2fd8` | Güncel referans dal (4.3.0) |
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

## 3. Tüketici (consumer) Durumu — 2026-07-05

| Servis | Sürüm | Senkron | Not |
|---|---|---|---|
| **Contract (SSOT)** | `4.3.0` (82d2fd8) | — | master; checksum `7295e395…` |
| **Platform** | 4.3.0 pin (submodule 82d2fd8) | ✓ Hizalı | vendored `contracts/` ağacı 4.3.0 |
| **Worker** | `v5.1.1` (bağımsız şema + kendi hash gate) | Temiz, origin=eşit | 13-bitki worker-kanonik (CORN/LENTIL + APPLE/PEACH/CHERRY/FIG); MAIZE↔CORN alias |
| **Edge** | `1.2.0` (bağımsız pin + kendi hash gate) | Temiz | 8 edge şeması; `$id` host drift ÇÖZÜLDÜ (hepsi `api.tarlaanaliz.com`) |

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

---

## 5. Bilgisayarlar Arası Notlar

- Yeni makinede başlarken: `git fetch origin --prune` → dalların `[ahead/behind]` durumunu kontrol et.
- Kalıcı bilgi **repoya** yazılmalı (bu dosya gibi); Claude'un yerel hafızası makineye özeldir, taşınmaz.
- **Eşzamanlı oturum uyarısı:** worker deposunda aktif closeout commit'leri var; o depoya yazmadan
  önce başka bir makinenin çalışıp çalışmadığını doğrula (çakışma riski).
- Doğrulama komutu (değişiklik sonrası): `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -v`.
