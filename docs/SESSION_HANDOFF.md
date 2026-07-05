# Oturum Devir Notu (Session Handoff)

> Amaç: Farklı bilgisayarlar arasında çalışırken oturum durumunu taşımak.
> Yerel makine hafızası taşınmaz; bu dosya repo ile GitHub üzerinden senkronize olur.
> **Bir sonraki oturumda önce bu dosyayı oku.**

**Son güncelleme:** 2026-07-05

---

## 1. Depo Durumu (Snapshot)

- **Kontrat sürümü (CONTRACTS_VERSION.md):** `4.3.0` — Breaking: **NO** (eklemeli/additive)
  - Checksum (SHA-256): `7295e395723746c03d1438885a307b1df6cb75d2f1357db9edffb2c5b3ee801c`
  - master head: `82d2fd8` (PR #19 merge)
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

## 4. Sonraki Oturum İçin — Açık İşler / Öneriler

- [ ] **Worker meyve-ağacı bitkileri (APPLE/PEACH/CHERRY/FIG) hizalaması** — Hata 4 kuyruğu.
  Worker/platform crop_type modelinde var, kontrat karşılığı YOK. Ayrı ve bilinçli bir hizalama
  kararı gerektirir (GAP kapsamına dahil mi?). Worker deposunun sahibi/eşzamanlı oturum uyguluyor
  olabilir — **dokunmadan önce o oturumun durumunu doğrula.**
- [ ] **Worker `v5.1.1` etiketi** terk edilen 5.x dalından türedi; worker sahibi kendi şemasında
  isimlendirmeyi netleştirmeli (etiket contract'la eşleşmek zorunda değil, ama 5.x mirası kafa karıştırıcı).
- [ ] (Düşük öncelik) `tools/validate.py` Windows UTF-8 (cp1254) çökmesi — yerelde `python -X utf8 tools/validate.py`
  ile çalıştır; kalıcı düzeltme için aracın başında `sys.stdout.reconfigure(encoding="utf-8")`.
- [ ] (Düşük öncelik) `CLAUDE.md` şema ağacı `schemas/datasets/` (9 dosya) dizinini belgelemiyor.

---

## 5. Bilgisayarlar Arası Notlar

- Yeni makinede başlarken: `git fetch origin --prune` → dalların `[ahead/behind]` durumunu kontrol et.
- Kalıcı bilgi **repoya** yazılmalı (bu dosya gibi); Claude'un yerel hafızası makineye özeldir, taşınmaz.
- **Eşzamanlı oturum uyarısı:** worker deposunda aktif closeout commit'leri var; o depoya yazmadan
  önce başka bir makinenin çalışıp çalışmadığını doğrula (çakışma riski).
- Doğrulama komutu (değişiklik sonrası): `python -X utf8 tools/validate.py && python -X utf8 -m pytest tests/ -v`.
