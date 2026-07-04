# Oturum Devir Notu (Session Handoff)

> Amaç: Farklı bilgisayarlar arasında çalışırken oturum durumunu taşımak.
> Yerel makine hafızası taşınmaz; bu dosya repo ile GitHub üzerinden senkronize olur.
> **Bir sonraki oturumda önce bu dosyayı oku.**

**Son güncelleme:** 2026-07-04

---

## 1. Depo Durumu (Snapshot)

- **Kontrat sürümü (CONTRACTS_VERSION.md):** `4.2.1` — Breaking: YES
  - Checksum (SHA-256): `614d41d207b89b80148e8781ae5e015d0a486a6d4ce525708a3f8f3fd0487d99`
- **Tek çalışma deposu:** `.../TARLA-ANALİZ/tarlaanaliz-contract` (origin = `github.com/physiscs-zana/tarlaanaliz-contract`)

### Dallar (branch) — 2026-07-04 itibarıyla

| Dal | Yerel SHA | GitHub ile | Not |
|---|---|---|---|
| `master` | `5f0aac4` | Eşit | Güncel referans dal |
| `feat/field-code-schema` (aktif) | `2535de2` | Eşit | **master'a birleştirilmiş** (PR #16); master 3 commit önde |
| `security/audit-fixes-2026-03` | `2fe6ac8` | Eşit | Bu oturumda push edildi |

- Açık PR: **yok**
- Çalışma dizini: temiz.

---

## 2. Bu Oturumda Yapılanlar (2026-07-04)

1. **Yedek/karışık depo silindi:** `.../tarlaanaliz-workspace/tarlaanaliz-contract` kalıcı olarak silindi.
   - Silmeden önce doğrulandı: tek benzersiz commit'i (`172bcee`, 2026-06-07 "ci: sync workflows") yalnızca eski GitHub Actions sürüm numaraları içeriyordu ve çalışma deposunda zaten aşılmıştı. Kayıp yok.
   - `.../tarlaanaliz-workspace` üst klasörü artık **boş** (silinebilir).
2. **`security/audit-fixes-2026-03` GitHub'a gönderildi** (`c657f54..2fe6ac8`):
   - `732685d fix(KR-025): remove recommendations/PRESCRIPTION from analysis_result schema`
   - `2fe6ac8 docs: update documentation cross-references for v2.0.2`

---

## 3. Sonraki Oturum İçin — Açık İşler / Öneriler

- [ ] **Aktif dalı değiştir:** `feat/field-code-schema` artık master'a birleşmiş. Yeni işe başlamadan önce:
  `git checkout master && git pull` sonra yeni bir dal aç.
- [ ] **`security/audit-fixes-2026-03` durumu:** GitHub'da güncel ama master'a **birleştirilmedi**. Gerekiyorsa bir PR açılmalı; gerekmiyorsa dal kapatılabilir.
- [ ] (Opsiyonel) Boş `.../tarlaanaliz-workspace` klasörünü sil.
- [ ] `docs/sync/worker_required_changes_2026-05-30.md` — worker tarafına uygulanması gereken (RAPOR-ONLY) değişiklikler hâlâ bekliyor olabilir; sahibi uygulamalı.

---

## 4. Bilgisayarlar Arası Notlar

- Yeni makinede başlarken: `git fetch origin --prune` → dalların `[ahead/behind]` durumunu kontrol et.
- Kalıcı bilgi **repoya** yazılmalı (bu dosya gibi); Claude'un yerel hafızası makineye özeldir, taşınmaz.
- Doğrulama komutu (değişiklik sonrası): `python tools/validate.py && pytest tests/ -v`.
