# SDLC Gate Checklists

**Kapsam:** PR → CI → Release kapıları — tek normatif doküman.  
**SSOT Uyum:** 1.2.0 (2026-02-24)  
**KR Referanslar:** KR-041 (SDLC Kapıları), KR-081 (Contract-First), KR-033 (Ödeme)

> Bu dosya üç aşamalı kalite kapısını tek kaynakta toplar.  
> Eski `PR_GATE_CHECKLIST.md`, `CI_GATE_CHECKLIST.md`, `RELEASE_GATE_CHECKLIST.md` dosyaları bu dosya ile değiştirilmiştir.

---

# GATE 1 — PR (Pull Request)

Her PR açılmadan önce geliştirici tarafından yapılacak kontroller.

## 1A) Schema + Enum Doğrulama

- [ ] `python tools/validate.py` hatasız çalışıyor
- [ ] Tüm JSON Schema dosyaları `"$schema": "https://json-schema.org/draft/2020-12/schema"` içeriyor
- [ ] Object tipli şemalarda `unevaluatedProperties: false` var
- [ ] Tekrarlı alt tipler `$defs` + `$ref` ile tanımlanmış

## 1B) Forbidden-Field Guard

- [ ] Hiçbir şema/enum/API alanında `email`, `tckn`, `otp` string'i geçmiyor
- [ ] `user_pii.v1` dışında hiçbir şemada telefon numarası zorunlu alan değil
- [ ] **[SSOT 1.2.0]** `payment_status` alanlarında `APPROVED` veya `EXPIRED` değeri YOK
- [ ] **[SSOT 1.2.0]** IBAN_TRANSFER akışında "e-posta" / "odeme@tarlaanaliz.com" referansı YOK

## 1C) Breaking-Change Kontrolü

- [ ] `python tools/breaking_change_detector.py` çalıştırıldı
- [ ] Breaking-change tespit edilmişse:
  - [ ] MAJOR versiyon bump yapıldı (`CONTRACTS_VERSION.md`)
  - [ ] Migration guide yazıldı (`docs/migration_guides/`)
  - [ ] `CHANGELOG.md` güncellendi

## 1D) Contracts Versiyonlama

- [ ] `CONTRACTS_VERSION.md` güncel (semver + sha256)
- [ ] Consumer repo'lar (platform/edge/worker) bu versiyon ile senkronize

## 1E) Ödeme Kontrolleri (KR-033) — [SSOT 1.2.0]

- [ ] `PaymentStateMachine` servisi bypass etmeyen tek yol; doğrudan status update kodu YOK
- [ ] `mark-paid` endpoint'i `admin_note` zorunluluğunu uyguluyor
- [ ] `reject` endpoint'i `rejection_reason` zorunluluğunu uyguluyor
- [ ] `PAYMENT.MARK_PAID` ve `PAYMENT.REJECTED` audit olaylarında `admin_user_id` zorunlu
- [ ] `receipt_blob_id` upload endpoint'i (`POST /payments/intents/{id}/upload-receipt`) tanımlı
- [ ] Sezonluk Paket `PAID` olmadan `ACTIVE` olamıyor (scheduler gate)
- [ ] Mission `PAID` olmadan `ASSIGNED` olamıyor (assignment gate)

## 1F) Drone Registry Kontrolü — [SSOT 1.2.0]

- [ ] Yeni drone modeli eklendiyse `enums/drone_type.enum.v1.json` güncellendi
- [ ] `drone_registry.yaml` ile `drone_type.enum.v1.json` senkronize
- [ ] `intake_manifest.v1`: `drone_model` alanı DroneType enum değerlerinden biri
- [ ] Eski DJI-only kısıtlaması kaldırıldı (tek model whitelist YOK)

## 1G) Örnekler + Testler

- [ ] `docs/examples/` altındaki tüm örnek JSON'lar ilgili şemaya uyuyor
- [ ] `python -m pytest tests/` tüm testleri geçiyor
  - `test_validate_all_schemas.py`
  - `test_examples_match_schemas.py`
  - `test_no_breaking_changes.py`

## 1H) SSOT Senkronizasyon

- [ ] `docs/ssot/kr_registry.md` bu PR'ın etkilediği KR'lerle uyumlu
- [ ] `docs/ssot/contracts_ssot.md` güncel uygulama notları içeriyor

---

# GATE 2 — CI (Continuous Integration)

Her PR'da CI pipeline'ında otomatik koşacak kontroller.

## 2A) Schema Validation (`tools/validate.py`)

```
BEKLENEN: EXIT 0
KONTROLLER:
  ✓ JSON Schema Draft 2020-12 format doğrulama (tüm schemas/*.json)
  ✓ unevaluatedProperties:false policy (object tipli şemalar)
  ✓ Forbidden-field guard: email/tckn/otp → FAIL
  ✓ [SSOT 1.2.0] payment_status guard: APPROVED/EXPIRED değerleri → FAIL
  ✓ [SSOT 1.2.0] drone_model değerleri drone_registry.yaml ile eşleşiyor → FAIL yoksa
  ✓ Enum dosyaları format + benzersizlik kontrolü
  ✓ OpenAPI lint + schema reference bütünlüğü
```

## 2B) Örnek Doğrulama (`tests/test_examples_match_schemas.py`)

```
BEKLENEN: TÜM TESTLER PASS
KONTROLLER:
  ✓ docs/examples/field.example.json → schemas/core/field.v1.schema.json
  ✓ docs/examples/mission.example.json → schemas/core/mission.v1.schema.json
  ✓ docs/examples/intake_manifest.example.json → schemas/edge/intake_manifest.v1.schema.json
  ✓ docs/examples/analysis_job.example.json → schemas/worker/analysis_job.v1.schema.json
  ✓ docs/examples/analysis_result.example.json → schemas/worker/analysis_result.v1.schema.json
  ✓ [SSOT 1.2.0] docs/examples/payment_intent_iban_pending.example.json → payment_intent.v2
  ✓ [SSOT 1.2.0] docs/examples/payment_intent_iban_paid.example.json → payment_intent.v2
  ✓ [SSOT 1.2.0] docs/examples/payment_intent_creditcard_paid.example.json → payment_intent.v2
```

## 2C) Breaking-Change Detector (`tests/test_no_breaking_changes.py`)

```
BEKLENEN: Breaking-change yoksa PASS; varsa semver MAJOR bump kontrolü
KONTROLLER:
  ✓ Önceki versiyonla şimdiki şemalar diff'lendi
  ✓ Breaking-change var ama MAJOR bump yok → FAIL
  ✓ Migration guide eksik → WARN
```

## 2D) Ödeme Durum Makinesi Guard — [SSOT 1.2.0]

```
BEKLENEN: EXIT 0
KONTROLLER:
  ✓ enums/payment_status.v1.json: APPROVED yok, EXPIRED yok → yoksa FAIL
  ✓ enums/payment_status.v2.json: APPROVED yok, EXPIRED yok → yoksa FAIL
  ✓ payment_intent.v1 + v2 status enum: PAID kanonik → değilse FAIL
```

## 2E) Drone Registry Senkronizasyon — [SSOT 1.2.0]

```
BEKLENEN: EXIT 0
KONTROLLER:
  ✓ enums/drone_type.enum.v1.json değerleri drone_registry.yaml ile eşleşiyor
  ✓ DJI-only kısıtlaması içeren herhangi bir kod/şema → WARN
```

## CI Failure Tablosu

| Hata | Eylem |
|---|---|
| validate.py FAIL | PR merge engellenir |
| test_examples FAIL | PR merge engellenir |
| breaking-change FAIL | PR merge engellenir; MAJOR bump gerekli |
| payment guard FAIL | PR merge engellenir |
| drone registry FAIL | PR merge engellenir |

---

# GATE 3 — Release

Yayın (release) öncesi yapılacak son kontroller.

> ⚠️ **2026-07-31 (KADEME 0 / D6) — bu kapı iki yerde yalan söylüyordu:**
> ① **Annotated tag adımı hiç yoktu** (SD8). Değişmez I-2 *"her contract sürümü annotated
> `vX.Y.Z` etiketi alır"* diyor; ölçüm ise **20 sürüme karşılık 4 etiket** buldu — yani I-2
> bugün tutmuyor. Adım aşağıda §3G'ye eklendi.
> ② **`PENDING_PROPAGATION` release kapısında yoktu** (SD7): `tests/test_vendored_parity.py`
> içindeki bu liste *"kanonik ileri, vendored henüz almadı"* beyanıdır ve C8 töreninin
> görevi tam olarak onu **boşaltmaktır**. Kontrol edilmediği için beyanlar bayatlayabiliyordu.
>
> 🔴 **Koordinatör kararı bekliyor (SD8, §14.6):** etiketsiz 16 eski sürüm için
> *retro-tag mı, "etiketsiz sürümler" kayıt notu mu?* Karar verilene kadar I-2'nin
> "tarihsel olarak da tutuyor" biçiminde raporlanması YASAK.

## 3A) Versiyon + Changelog

- [ ] `CONTRACTS_VERSION.md` doğru semver içeriyor
  - Breaking-change varsa: MAJOR bump yapıldı (örn: v1.x.x → v2.0.0)
  - Non-breaking değişiklik: MINOR veya PATCH
- [ ] `CONTRACTS_VERSION.md` sha256 hash güncel (tüm şema dosyaları dahil)
- [ ] **`**Checksum State:** PENDING_REPIN` satırı KALKTI.**
      Bu satır tur içi "beklenen kırmızı"nın makine-okunur beyanıdır; `tools/pin_version.py`
      dosyayı baştan ürettiği için re-pin ile kendiliğinden kaybolur. **Hâlâ duruyorsa
      re-pin yapılmamıştır** — CI `verify-checksums` işi uyarıya düşer, `pytest` ise
      `test_real_repo_checksum_verifies`'i `xfail` sayar. İkisi de release'de KABUL EDİLMEZ.
      ```bash
      grep -n "Checksum State" CONTRACTS_VERSION.md   # ÇIKTI BOŞ OLMALI
      ```
- [ ] `CHANGELOG.md` bu release için tüm değişiklikleri kapsıyor:
  - `### Breaking Changes` bölümü (varsa)
  - `### Added / Changed / Fixed` bölümleri

## 3B) Migration Guide

- [ ] Breaking-change varsa `docs/migration_guides/` altında migration guide hazır
- [ ] **[SSOT 1.2.0]** `payment_intent_v1_to_v2.md` mevcut ve güncel
- [ ] Migration guide içeriyor: DB değişiklikleri, kod değişiklikleri, rollback planı, test kriterleri

## 3C) Consumer Repo Senkronizasyon

- [ ] `tools/sync_to_repos.sh` çalıştırıldı
- [ ] platform repo: `CONTRACTS_VERSION.md` bu release ile eşleşiyor
- [ ] edge repo: `CONTRACTS_VERSION.md` bu release ile eşleşiyor
- [ ] worker repo: `CONTRACTS_VERSION.md` bu release ile eşleşiyor
- [ ] Tüm consumer'larda SHA-256 hash uyumu doğrulandı
- [ ] **`PENDING_PROPAGATION` BOŞ** (SD7). `tests/test_vendored_parity.py` içindeki bu sözlük
      *"kanonik ileri gitti, vendored kopya henüz almadı"* beyanıdır. C8 töreninin işi onu
      **boşaltmaktır**; dolu kalırsa release, kendi beyanına göre yarım demektir.
      Kontrol elle değil **testle** yapılır (checklist maddesi ile kod aynı şeyi söyler):
      ```bash
      python -m pytest tests/test_vendored_parity.py::test_pending_propagation_is_empty -v
      ```
      Tur içinde bu test `xfail`'dir (beyan açık); `pin_version.py` re-pin'i beyanı silince
      **gerçek kırmızıya** döner ve yayılım yapılmadan release'i durdurur.
- [ ] **Vendored parite kapısı YEREL koşuldu.** ⚠️ Bu kapı **CI'da KOŞMAZ**: kardeş depolar
      (`tarlaanaliz-edge`, `tarlaanaliz-worker`) GitHub Actions'ta checkout edilmiyor, testler
      `kardeş depo yok` gerekçesiyle atlanıyor (atlama artık CI özetinde görünür ama yine de
      **ölçüm yapılmamış** demektir). C8'de kardeş depoların yanında koşturun:
      ```bash
      python -m pytest tests/test_vendored_parity.py -v -rs
      ```
      Beklenen: **0 skip**. Skip görüyorsanız depo düzeni yanlış (üç depo aynı üst dizinde olmalı).

## 3D) SSOT 1.2.0 Özgül Kontroller — [YENİ]

- [ ] `enums/payment_status.v1.json`: APPROVED ve EXPIRED değerleri yok
- [ ] `enums/payment_status.v2.json`: APPROVED ve EXPIRED değerleri yok, REFUNDED var
- [ ] `enums/drone_type.enum.v1.json`: Tüm desteklenen modeller mevcut
- [ ] `schemas/platform/payment_intent.v2.schema.json`: receipt_blob_id, admin_note, rejection_reason, admin_user_id alanları mevcut
- [ ] `schemas/edge/intake_manifest.v1.schema.json`: drone_model DroneType enum'una bağlı
- [ ] `docs/examples/payment_intent_*.example.json` dosyaları mevcut ve v2 şemasına uyuyor

## 3E) Son Testler

- [ ] `python -m pytest tests/ -v -rs` — tüm testler PASS · **`SKIP BÜTÇESİ: 0`**
      (`-rs` zorunlu: sessiz atlama yeşil sayılmaz. `tests/conftest.py` beyan edilmemiş
      atlama gerekçesinde oturumu zaten düşürür; release'de **beyanlı olsa bile** skip
      kabul edilmez — kardeş depolar yanınızdayken koşun.)
- [ ] **`xfail` sayısı 0** — tur içi beklenen kırmızı (`test_real_repo_checksum_verifies`)
      re-pin ile gerçek PASS'a dönmüş olmalı. `strict=True` olduğu için beyan silinmeden
      re-pin yapılırsa süit **XPASS** ile kırmızıya döner; bu bir hata değil, hatırlatmadır.
- [ ] **`-m "not release_gate"` KULLANILMADI** — deselect `tests/conftest.py` tarafından
      reddedilir (exit 4). Kırmızıyı gizlemek çözmek değildir.
- [ ] `python tools/validate.py` — EXIT 0
- [ ] `python tools/breaking_change_detector.py --old <base> --new .` — rapor incelendi.
      Çıkış kodu sözleşmesi: **0** breaking yok · **1** breaking var · **≥2 araç çalışamadı
      (kapı KÖR — "breaking yok" ile karıştırmayın)**. `$ref` hedefleri **çözülmez**;
      `REF_CHANGED` satırları elle incelenir.
      ```bash
      OUT=$(python tools/breaking_change_detector.py --old ../old --new . --json); RC=$?
      echo "RC=$RC"   # <-- kod KOMUTTAN okunur; pipe'ta $? yanıltır
      ```

## 3F) SSOT Dokümantasyon

- [ ] `docs/ssot/kr_registry.md` son KR Registry versiyonu (v8+)
- [ ] `docs/ssot/GOVERNANCE_PACK_v1_0_1.md` güncel
- [ ] `docs/ssot/contracts_ssot.md` bu release ile uyumlu

## 3G) Release töreni — ANNOTATED TAG (değişmez I-2) 🔴 [YENİ · D6]

> **Neden ayrı bir madde:** etiketsiz sürüm **eksik release**'tir — tüketici `vX.Y.Z` ile
> pinleyemez, `git describe` bulanık kalır (`vA.B.C-N-g…`) ve I-2 raporlanamaz hâle gelir.
> Ölçüm (2026-07-31): **20 sürüm / 4 annotated etiket.** Adım checklist'te olmadığı için
> atlanmıştı; artık atlanamaz.

**Sıra — hepsi bu depoda (yerel makine), belirtilen sırayla:**

```bash
# 1) Sürümü pinle (CONTRACTS_VERSION.md'yi baştan üretir; PENDING_REPIN beyanı burada silinir)
python tools/pin_version.py --minor            # veya --major --breaking / --patch

# 2) Kapılar — hepsi yeşil olmadan etiket YOK
python tools/validate.py
python -m pytest tests/ -v -rs                 # SKIP 0 · xfail 0 · release_gate deselect YOK
python tools/pin_version.py --verify

# 3) Release commit'i
git add -A && git commit -m "release: contracts vX.Y.Z"

# 4) ANNOTATED tag (hafif/lightweight tag KABUL EDİLMEZ — objectype 'tag' olmalı)
git tag -a vX.Y.Z -m "contracts vX.Y.Z — <tek satır özet>"
git push origin master --follow-tags

# 5) Etiketin gerçekten annotated olduğunu DOĞRULA (iddia değil ölçüm)
git for-each-ref refs/tags/vX.Y.Z --format='%(objecttype) %(refname:short)'   # -> "tag vX.Y.Z"
git describe --tags HEAD                                                      # -> temiz "vX.Y.Z"
```

- [ ] Etiket **annotated** (`%(objecttype)` = `tag`; `commit` çıkarsa lightweight'tır → silip yeniden atın)
- [ ] `git describe --tags HEAD` temiz `vX.Y.Z` döndürüyor
- [ ] Etiket push edildi (`git ls-remote --tags origin | grep vX.Y.Z`)
- [ ] Üç tüketici deposunda sürüm dizesi hizalandı (I-1) ve platform submodule pini bu **etiketli commit**

⛔ **Bilinen eksik (koordinatör kararı bekliyor — §14.6/SD8):** etiketsiz 16 tarihsel sürüm.
Karar verilmeden I-2 "tarihsel olarak da tutuyor" diye raporlanamaz; bugün yalnız
**v6.1.0 · v7.0.1 · v7.1.0 · v7.2.0** annotated'tır.
