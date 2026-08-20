# CLAUDE.md — tarlaanaliz-contract

Tüm TarlaAnaliz veri sözleşmelerinin **SSOT**'u (tek doğruluk kaynağı). **Contract-first:**
hiçbir servis (platform, edge, worker) kendi API'sini veya veri yapısını tanımlamaz — hepsi
buradan doğar. Tüketiciler `CONTRACTS_VERSION.md` + SHA-256 ile bir sürüme pinlenir.

**Alan:** GAP bölgesinde drone tabanlı tarla analizi. Belgeler Türkçe; şema açıklamaları ve
kod İngilizce.

Dizin ağacı, bağımlılık listesi ve kod stili **bu dosyada tekrarlanmaz** — `pyproject.toml`,
`package.json` ve ağacın kendisi kanoniktir. Aşağıda yalnız koddan türetilemeyen kurallar,
tuzaklar ve kapılar var.

<!-- KESTIRME-YOK-BLOGU-BASLANGIC · bayt-özdeş: dört depoda AYNI · kapı: check_kestirme_yok.py -->
## 🔴 KESTİRME YOK — ispatlı ve kalite odaklı çalış

*(ürün sahibi, 2026-08-20 — bu dosyadaki diğer bütün kuralların şemsiyesi)*

Bir işi **"çalışıyor gibi görünen"** en kısa yoldan yapmak yasaktır.

1. **Kolay olanı seçme.** Doğru çözüm zor diye kolayı seçme — kolay olan *yamadır*, yama yasak.
2. **Ölçmeden söyleme.** *"Kod yolu böyle"* ile *"canlıda böyle oluyor"* ayrı cümlelerdir.
   **"Merge edildi" ≠ "dağıtıldı" ≠ "çalışıyor"** — üçünü ayrı ayrı ölç ve ayrı yaz.
3. **Kapsamı sessizce daraltma.** Bir sınıfın tek örneğini düzeltip "gördüm" deme:
   sınıfı **say**, hepsini kapat ya da **kalanı sayısıyla beyan et**.
4. **Sessiz borç bırakma.** Engele takılınca `TODO` / `şimdilik` / `geçici` bırakıp geçme;
   ya bitir ya da kaleme yazıp **sayısıyla** bildir. Sessiz borç en pahalı borçtur.
5. **Susturma gerekçe ister.** `except: pass`, gerekçesiz `skip`, gerekçesiz `type: ignore`
   veya `@ts-ignore` birer kestirmedir — her biri **neden** yorumu taşımalı.
6. **Kendi çıktını çürütmeye çalış.** Tur sonunda kendi iddialarını yeniden ölç.
   Ölçüldü 2026-08-20: aynı gün yazılan açık kalem listesini çürütme turu
   **2 bayat kalem + 3 yanlış atıf + 3 yeni gerçek kusur** çıkardı.

Kanonik gövde ve gerekçeler: **contract deposunun çalışma alanı kuralları
belgesi**, §4 (yol bilerek yazılmadı: bu blok dört depoda bayt-özdeştir ve
çapraz-repo yolu tüketici CI'larında pinli sürüme düşüp sarkan atıf üretiyor).
Bu blok **dört depoda bayt-özdeştir**; kapı: `check_kestirme_yok.py` (iki yönlü mandal).
<!-- KESTIRME-YOK-BLOGU-BITIS -->

## Kritik kurallar

### 1. JSON Schema Draft 2020-12 — zorunlu

Her şema dosyası şunları taşımak zorunda:
- `"$schema": "https://json-schema.org/draft/2020-12/schema"`
- `"$id"`: `https://api.tarlaanaliz.com/schemas/{domain}/{name}.v{N}.schema.json`
- `"title"` + `"type"`
- Her `object` düğümünde `"unevaluatedProperties": false` (alan sızmasını önler) ya da
  **gerekçeli** `additionalProperties`
- Yeniden kullanılan tipler `"$defs"` altında, `"$ref": "#/$defs/TypeName"` ile

### 2. PII asgariliği (KR-050) — sert güvenlik gereği

**YASAK ALAN ADLARI** — hiçbir şemada geçemez: `email`, `e_mail`, `tckn`, `tc_kimlik_no`,
`otp`, `one_time_password`.
**Kimlik modeli:** telefon + 6 haneli PIN. E-posta yok, TC kimlik yok, OTP yok.
`tools/validate.py` ve CI bunu otomatik denetler; ihlal build'i düşürür.

### 3. Sürümleme (SemVer)

- **MAJOR** — kırıcı: `required`'a alan ekleme, tip değiştirme, enum değeri kaldırma/yeniden
  adlandırma, uç değiştirme. `docs/migration_guides/` altında göç kılavuzu + 
  `CONTRACTS_VERSION.md`'de `breaking_change: true` gerektirir.
- **MINOR** — geriye uyumlu ekleme: opsiyonel alan, yeni enum değeri, yeni uç.
- **PATCH** — belge, açıklama, kısıt gevşetme.

Adlandırma: şema `{name}.v{N}.schema.json` · enum `{name}.enum.v{N}.json` (bazı eski ödeme
enum'ları `.enum.` taşımaz) · OpenAPI `{service}_{scope}.v{N}.yaml`.

### 4. KR gövdeleri — gövde TEK yerde yaşar

⚠️ **Buradaki hiçbir sayıya güvenme — üreteci koş.** Bu bölümdeki sabit sayılar iki kez
bayatladı ve iki gerçek yanlış teşhis üretti. Bugünün doğru cevabı bunun çıktısıdır:

```bash
python -c "import sys; sys.path.insert(0,'tests'); from test_kr_reference_integrity import _ssot_defined_krs as s, _registry_defined_krs as r, _collect_kr_refs as x; from test_single_normative_body import _registry_body_krs as rb, _dual_body_krs as d; a,b=s(),r(); print(f'SSOT {len(a)} | registry başlık {len(b)} | registry GÖVDE {len(rb())} | birleşim {len(a|b)} | ÇİFT GÖVDE {len(d())} | şemalarca atıf {len(x())}')"
```

🔴 **`ÇİFT GÖVDE`yi oku, başlık kesişimini DEĞİL.** İşaretçi de başlık taşır, o yüzden
"iki dosyada da tanımlı" ~50 çıkar ve hiçbir şey ifade etmez. Anlamlı sayı — kaç KR'nin
**normatif gövdesi** iki yerde — **0** kalmalı. Bu ikisini karıştırmak, D16-b kapısını
kör olduğu hâlde yeşil gösterdi (2026-07-31).

| Dosya | Rol |
|---|---|
| `docs/TARLAANALIZ_SSOT_v1_2_0.txt` | Tam KR külliyatı; **platform kopyasıyla bayt-özdeş** (çapraz-repo artefaktı). Çelişkide **bu kazanır**. |
| `ssot/kr_registry.md` | **Gezinme + kapsam indeksi, gövde deposu DEĞİL** (2026-08-01/D16-b2). Her başlık SSOT metnine `TÜRETİLMİŞ İŞARETÇİ` damgası taşır. **İstisna:** `KR-088/089/090/091` gövdeleri hâlâ burada — SSOT metninde tanımsızlar. |

Başlık biçimi dört türlüdür (`## [KR-019]`, birleşik `## [KR-018 / KR-082]`, typo
`## # [KR-033]`, parantezsiz `### KR-017`). Yeni regex yazma —
`tests/test_kr_reference_integrity.py` içindeki çıkarıcı dördünü de her başlık düzeyinde
tanıyor.

**Bundan sonra:** bir KR'nin kuralı **önce SSOT metninde** değişir, sonra registry başlığı
(başlık/kapsam) izler. Registry başlığı altına normatif gövde yazmak kapıyı kırmızıya çevirir.

Veri katmanı gövdeleri nerede (ölçüldü, tahmin etme): `KR-092`/`KR-093` → **yalnız SSOT
metni** · `KR-088`/`KR-091` → **yalnız registry** (SSOT metni onları tek satır çapraz-atıfla
anıyor, bu bir tanım DEĞİL — işaretçiye çevirmek kuralı silerdi).

Bu deponun kilit KR'leri: **KR-050** PII · **KR-081** contract-first/şema kapıları ·
**KR-072** dataset yaşam döngüsü + zincir · **KR-073** güvenilmez dosya + malware taraması ·
**KR-018/082** radyometrik kalibrasyon hard gate.

## Araçlar ve kapılar

⛔ **Bu depoda TypeScript zinciri YOKTUR ve HİÇ OLMADI.** 2026-08-11'e kadar Ajv ·
json-schema-to-typescript · Jest · ESLint · Prettier · Husky sayılıyordu; ölçüldü: **0 adet
`.ts`/`.js`**, `tools/*.ts` hedeflerinin hiçbiri commit edilmemiş. En kritiği
`npm run format` checksum kapsamındaki **97 dosyanın 94'ünü** yeniden biçimlendiriyordu —
ölü değil **zararlı**. Zincir kaldırıldı (676→263 paket); `tests/test_node_toolchain_honesty.py`
geri gelmesini yasaklıyor. Tek Node aracı **@redocly/cli**.

⛔ **Depo genelinde `prettier` KOŞTURMAYIN.** `schemas/` · `enums/` · `api/` · `dist/`
`.prettierignore` ile korunuyor: bu ağaçların biçimi elle bakımlıdır ve checksum + vendored
bayt-paritesi + `dist` tazeliği ona bağlıdır.

> ⛔ **"Coverage threshold: %80" iddiası ÇÜRÜTÜLDÜ (2026-08-11, ölçüldü).** O eşik
> `package.json`'daki jest yapılandırmasındaydı ve jest `tools/**/*.ts` üzerinde koşuyordu —
> depoda **0 adet `.ts`** var, yani eşik **hiç uygulanmadı**. Python tarafında
> `--cov-fail-under` **hiçbir yerde tanımlı değil**. Gerçek ölçülen kapsam: `tools/` için
> **%51**. Bir eşik istenirse `pyproject.toml → addopts`'a eklenmeli — o zaman GERÇEK kapı olur.

```bash
python tools/validate.py        # tek doğrulayıcı: schemas/ + enums/ + dist/schemas/ + api/
pytest tests/ -q                # süit Python'dur (test dosyası sayısını `git ls-files 'tests/*.py' | wc -l` ile ölç)
black . && ruff check . && mypy tools/
npm run openapi:validate        # redocly lint (CI: npx @redocly/cli@1 lint)
npm run openapi:bundle          # dist/openapi/ altina bundle
python tools/pin_version.py     # YAZMA kipi: CONTRACTS_VERSION.md hash'ini gunceller
python tools/check_scripts.py   # betik ağacı kapısı (AL-K32)
python tools/check_claude_md_refs.py    # CLAUDE.md kimlik + kod yolu atfı
python tools/pin_version.py --verify   # agrega checksum
```

⚠️ `tools/generate_types.sh` **CI'da çağrılmaz**; araçlarını **global** kurar. Tüketiciler
tipi kendi depolarında üretir.

### CI'da gerçekten ne koşuyor

`.github/workflows/contract_validation.yml` — 8 iş: `validate-schemas` · `test-schemas` ·
`detect-breaking-changes` · `verify-checksums` · `lint-openapi` · `check-forbidden-fields` ·
`check-draft-2020-12` · `check-brand-guard` (+ doc-link kapısı + **I-1 sürüm hizası** AL-K30 +
**betik ağacı** AL-K32 + **CLAUDE.md atıf bütünlüğü**). Hepsi `summary` işinde toplanır. **Tek bir `ci:gate` komutu YOKTUR.**
Kapsam ve `needs` bütünlüğü `tests/test_ci_gate_honesty.py` ile türetilip zorlanır.

### Kırıcı değişiklik dedektörü — bilinen körlükleri

```bash
python tools/breaking_change_detector.py --old <dizin|git-ref> --new .
```

Kapı bunları gördüğünü **iddia ETMEZ**: `$ref` çözülmez (`REF_CHANGED` → insan incelemesi,
SDLC_GATES §3E) · **object politikası daralması hiç sınıflandırılmaz** (2026-08-11: 27 kapatma
→ 0 değişiklik kaydı). Sürüm kararı bu iki sınıfta **elle ölçülür**.

## Çapraz-repo senkron — 5 değişmez

Her değişmez bir komuta bağlı; komutu olmayan kural bir dilektir, kapı değildir.

- **I-1 · Sürüm hizası:** üç depoda birebir aynı (worker `v` önekli). Uyuşmazlık = kırık.
- **I-2 · Kanonik release etiketli:** annotated `vX.Y.Z` (bkz. `docs/versioning_policy.md`
  §Release). Etiketsiz sürüm **eksik release**'tir — tüketici tag ile pinlenemez.
  Tag adımı release checklist'inin parçası, atlanamaz.
- **I-3 · Platform ↔ Contract: bayt-özdeş.** Platform aynalar, ikinci değer hesaplamaz.
- **I-4 · Worker ↔ Contract: bayt-özdeş DEĞİL.** Worker 8 izli dosyayı kanoniğin
  **superset** şemasının dar runtime **alt kümesi** olarak vendor'lar; öz-hash (KR-041)
  geçmesi beklenir. Kanonik superset worker'ın katı formunu kabul eder.
- **I-5 · Sapma yalnız GEÇİCİ (AK-4):** worker kanonikten önce re-pinleyebilir ama
  **kendi deposunda** `denetim/*_devir_spec_*.md` bırakır (bu depoda o dosyalar yoktur). **Kalıcı divergence YASAK.**

```bash
git describe --tags HEAD              # I-2: temiz vX.Y.Z (yoksa: git tag -a vX.Y.Z <commit>)
python tools/pin_version.py --verify  # I-3/I-4 kaynağı
python tools/validate.py && pytest tests/ -q
```

### I-1'in kapısı (AL-K30) — `tools/check_version_alignment.py`

I-1 üç `CLAUDE.md`'de yazılıydı ama **doğrulayan tek komut yoktu**: dört depo tarandı,
worker/edge **0 isabet**. Kural sessizce kırılmıştı — edge `7.6.1`'i **hiç pinlemedi**.
Kapı **burada yazılır, kardeş depolarda koşar** (D4-b modeli). İki kip vardır, karıştırılmaz:

```bash
# contract'ın kendisi (CI'da koşuyor). Sürüm etiketin GERİSİNDE olamaz;
# İLERİSİNDE olabilir (release PR'ının normal hâli).
python tools/check_version_alignment.py --mode canonical \
  --pinned-file CONTRACTS_VERSION.md --label '## Version:' --latest-from-git .

# kardeş depo (kendi CI'ında). Pin en yeni yayımlanmış sürüme EŞİT olmalı.
python tools/check_version_alignment.py --mode consumer \
  --pinned-file CONTRACTS_VERSION.md --label 'Upstream Contract Set' --latest 7.7.2
```

Üçü de mutasyonla sınandı (`tests/test_version_alignment_gate.py`, 34 test):

- ⚠️ **Kardeşin KENDİ checkout'uyla karşılaştırmak TOTOLOJİDİR** — kardeş CI sözleşmeyi
  `ref: v${pin}` ile çeker, çektiği ağacın sürümü elbette pinine eşittir. `--latest` /
  `--latest-from-git` **zorunludur**.
- 🔴 **`--label` şart.** Sürüm dosyaları değişiklik geçmişi de taşıyor: contract'ta **30**,
  worker'da **22**, edge'de **27** farklı sürüm dizesi var. Etiketsiz koşum edge dosyasında
  `1.7.0` (edge'in **kendi** SemVer'i) okudu — doğru cevabı yanlış gerekçeyle verdi.
  Artık belirsizlikte **tahmin etmez, fail-closed kapanır**.
- **`fetch-depth: 0` gerekli.** Sığ checkout etiket getirmez; etiketsiz ortamda kapı
  fail-closed kırmızı verir. *"Ölçemedim" asla "hizalı" sayılmaz.*

I-5 gereği geçici gerilik **yalnız** `--allow-lag-until <tarih> --reason <gerekçe>` ile
kabul edilir; gerekçesiz ya da süresi dolmuş muafiyet kırmızıdır.

## Şema değiştirirken

1. Mevcut şemayı **oku**. 2. Draft 2020-12 zorunluluklarını koru. 3. `$defs` + `$ref` kullan.
4. PII alanı ekleme. 5. **Kırıcı mı ölç** — `required`'a ekleme / tip değişimi / enum kaldırma
= MAJOR. 6. `docs/examples/` altındaki karşılığını güncelle. 7. `python tools/validate.py &&
pytest tests/ -q` koş.

**Enum:** değer *ekleme* MINOR · *kaldırma/yeniden adlandırma* MAJOR + göç kılavuzu.
Uygun yerde iki dilli görünen ad (`tr` + `en`) ekle.
**OpenAPI:** 3.1.0 · mümkün olduğunda JSON Schema'ya `$ref` · kimlik modeli telefon+PIN
oturum belirteci · paylaşılan bileşenler `api/components/`.

## Commit mesajları

`feat(scope):` · `fix(scope):` · `audit:` — kapsamlar `contracts`, `geojson`, `schemas` vb.
