<!-- KANONIK GOVDE. Bu dosya TARLA-ANALIZ/CLAUDE.md tarafindan `@` ile ice alinir.
     Kapsayici klasor bir git deposu DEGILDIR, bu yuzden kural govdesi burada (git'te) yasar:
     boylece surumlenir, PR'da incelenir ve ikinci makineye git ile gider.
     Kok dosyayi duzenleme -- KURALI BURADA degistir. Kurulum: docs/workspace/KURULUM.md -->

# TARLA-ANALİZ — Çalışma Alanı Haritası (kanonik gövde)


> **Sade dil kuralı:** her teknik terim ilk geçtiği yerde parantezle açıklanır —
> "fail-closed (hata olunca güvenli tarafta durup sonucu paylaşmama)". Proje standardı.

## 0. Burası nedir

`TARLA-ANALİZ` bir git deposu **değildir** — 4 bağımsız depoyu yan yana tutan kapsayıcı
klasördür. Git işlemleri daima `git -C <repo> …` ile yapılır.

**TarlaAnaliz:** GAP bölgesinde drone ile çekilen çok-bantlı (multispektral = gözün
görmediği kızılötesi bantları da kaydeden) tarla görüntülerinden hastalık / zararlı / ot
tespiti yapan SaaS platform.

## 1. Dört depo

| Klasör | Rol | Çelişkide kazanan kanonik kaynak |
|---|---|---|
| `tarlaanaliz-contract` | **SSOT** (tek doğruluk kaynağı). JSON Schema + enum + OpenAPI. Kod yazmaz. | `docs/TARLAANALIZ_SSOT_v1_2_0.txt` |
| `tarlaanaliz-platform` | Backend + web/PWA. Sözleşmeyi `contracts/` submodule'ü olarak alır. | `docs/TARLAANALIZ_SSOT_v1_2_0.txt` |
| `tarlaanaliz-edge` | EdgeKiosk — M1/M2 iki makineli saha istasyonu. | kendi `CLAUDE.md` |
| `tarlaanaliz-worker` | YZ analiz işçisi — RabbitMQ tüketir, 3 aşamalı çıkarım koşar. | `docs/reference/kr_registry.md` |

**Veri akışı (tek yönlü):**
`EdgeKiosk → Platform/Ingress (mTLS) → Object Storage + Kuyruk → Worker → Platform → Web/PWA`
Worker gelen HTTP kabul etmez, platforma geri çağrı yapmaz (KR-070/KR-071).

**İş kuralları `KR-NNN` ile anılır.** Bir KR'nin gövdesi **tek yerde** yaşar (contract
deposunda `docs/TARLAANALIZ_SSOT_v1_2_0.txt`); `ssot/kr_registry.md` yalnız gezinme indeksi.
Sayı ezberleme — contract `CLAUDE.md`'deki üreteç komutunu koş.

## 2. Oturuma başlarken

1. **Çalışacağın deponun İÇİNDEN `claude` başlat** — kapsayıcı klasörden değil.
   Gerekçe ölçüldü: Claude Code alt dizin `CLAUDE.md`'lerini *talep üzerine* yükler ve
   `/compact` (bağlam dolunca geçmişin özetlenmesi) sonrası **yeniden enjekte etmez** —
   yalnız başlatma dizinindeki `CLAUDE.md` sıkıştırmaya dayanır. Kapsayıcıdan başlarsan
   uzun oturumun ortasında depo kuralların sessizce düşer.
2. **Nerede kalındığını depodan oku — hafızadan değil.** İki dosya tek kaynaktır,
   `tarlaanaliz-contract` içinde yaşar (yani git ile makineler arası taşınır):
   - `docs/SESSION_HANDOFF.md` — durum fotoğrafı. En güncel bölüm başta (`## 0.A`). İş listesi TUTMAZ.
   - `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` — yapılacak işlerin tek kaynağı.
3. Bir depoda iş yapmadan önce **o deponun `CLAUDE.md`'sini oku** — yasak örüntüler ve
   kabul ölçütleri orada.
4. **Çelişki sırası:** depo içi kanonik kaynak > depo `CLAUDE.md` > bu dosya > hafıza.
5. `git -C <repo> fetch` + `log --oneline -10` — başka makineden push gelmiş olabilir.

## 3. Çapraz-repo senkron — 5 değişmez

Üçlü senkron: **contract = SSOT · platform + worker = tüketici**. Tam metin üç deponun
`CLAUDE.md`'sinde; burada özet + komut.

- **I-1 Sürüm hizası:** `CONTRACTS_VERSION.md` sürümü üç depoda aynı (worker `v` önekli).
- **I-2 Etiket:** Her contract sürümü release commit'inde annotated tag `vX.Y.Z` taşır.
- **I-3 Platform ↔ Contract: bayt-özdeş.** Platform aynalar, ikinci değer hesaplamaz.
- **I-4 Worker ↔ Contract: bayt-özdeş DEĞİL.** Worker 8 dosyayı dar bir **alt küme** olarak
  vendor'lar. Byte-diff çıkması senkron kırık demek **değildir** — kasıtlıdır.
- **I-5 Sapma yalnız GEÇİCİ.** Kalıcı ayrışma yasak; gerekçesi devir notuna yazılır.

```bash
git -C tarlaanaliz-platform submodule status contracts   # I-3: başında '+/-' OLMAMALI
git -C tarlaanaliz-contract describe --tags HEAD         # I-2: temiz vX.Y.Z dönmeli
```

## 4. Kalıcı çalışma kuralları

Her kuralın gerekçesi ve ölçülmüş örnekleri parantezdeki hafıza dosyasında
(`~/.claude/memory/tarlaanaliz/`) — kural kırıldığında oraya bak, buraya değil.

- **Sade dil + parantezli terim.** Yukarıdaki kutu. (`plain-language-with-technical-terms`)
- **Önce tam oku, sonra işlem.** İlgili dosyaların TAMAMI okunmadan değişiklik yok.
  `grep` **dosya bulmak** içindir, **karar vermek** için değil. (`once-tam-oku-sonra-islem`)
- **Gündeme getirdiğini kanıtla.** Öneri / bulgu / risk **aynı mesajda kanıtıyla** yazılır:
  kanonik atıf, `dosya:satır` ya da komut çıktısı. Kanıtın **neyi desteklemediğini** de söyle.
  Kanıtlayamıyorsan ölç; ölçemiyorsan gündeme getirme. Kanıt öneriyi çürütürse geri al.
  (`gundeme-getirdigini-kanitla`)
- **Test = mutasyon + pozitif kontrol.** Yeşil test kanıt değildir: kodu boz → testin
  kırmızıya döndüğünü gör → geri al. Tek yönlü her iddianın ("şu kötü şey yok") yanına
  "meşru içerik değişmeden hayatta kalıyor" kontrolü koy. Tam liste:
  `tarlaanaliz-platform/CLAUDE.md` → "Test Kabul Ölçütleri". (`mutation-test-green-suites`)
- **Ölçümün geçerliliğini ölç.** Yanlış ölçüm ölçmemekten kötüdür. "Yerelde geçti / CI'da
  geçmedi" çelişkisinde **① `git status` ② araç sürümü karşılaştırması ③ teori** — bu sırayla.
  Doğrulamayı taze klonda yap (`git clone --no-local . /tmp/x`); `git stash` izlenmeyen
  dosyaları almaz. (`olcumun-gecerliligini-olc`)
- **Yama yok.** Geçici/kısmi çözüm istenmez — kalıcı, uçtan uca (backend + sözleşme +
  arayüz + test). (`feedback-no-patches-permanent-solutions`)
- **Tek seferde bul, tek seferde çöz.** Keşif ile uygulama ayrı fazdır: önce kapsamı tara ve
  sorunların TAMAMINI ispatıyla çıkar, sonra tek turda uygula. Tarayıcını **önce kendi
  üzerinde** sına. Bir örneği düzeltip "sınıfı gördüm" deme — sınıfı say, hepsini aynı turda
  kapat ya da kalanı sayısıyla beyan et. (`tek-seferde-bul-tek-seferde-coz`)
- **Az kod, steril yapı.** İşlev kaybı OLMADAN en az dosya/kod; varsayılan yön
  silme/birleştirme. "Kayıp yok" **ölçülerek** kanıtlanır. Ölü **koruma** istisnadır —
  sil değil, BAĞLA. (`az-kod-steril-yapi`)
- **Paralel oturum riski.** Depoda eşzamanlı başka aktör olabilir: yazmadan önce oku,
  üzerine yazma, ekleyerek güçlendir. `git add -A` **kullanma** — yol-sınırlı
  `git add -- <yol>`. (`tarlaanaliz-paralel-oturum-riski`)
- **Çoklu makine.** Devir **yalnız git ile**. `.claude/` dört depoda da gitignore'da →
  oraya konan hiçbir şey diğer makineye gitmez. (`coklu-makine-calisma`)
- **Commit/push yalnız açıkça istendiğinde.** Dosya silme, force push, hard reset → onay.
- **Küçük bulguları TEK PR'da topla — her PR ayrı bir maliyettir.** Aynı oturumda aynı
  depoda birden fazla küçük/bağımsız düzeltme (bayat satır, dosya taşıma, tek-satır kanıt
  düzeltmesi) çıktıysa AYRI dal/PR açma — hepsini **tek dal, tek commit (ya da mantıksal
  gruplara ayrılmış az sayıda commit), tek PR**'da topla ve öyle push et. Gerekçe: her
  PR açılışı bir CI koşumu (contract'ta 8-9 iş) + bir merge-sonrası ana-dal koşumu daha
  demektir — N küçük bulguyu N ayrı PR'a bölmek Actions dakikasını ve oturum
  araç-çağrısı/token maliyetini **N kat** büyütür, kullanıcıya aylık fatura olarak döner.
  **İstisna:** değişiklikler birbirini bekliyorsa (biri mergelenmeden diğeri test
  edilemiyorsa) veya kullanıcı ayrı ayrı inceleme istiyorsa ayrı PR meşrudur — aksi hâlde
  varsayılan **toplama**. Bir denetim/tarama turu birden fazla düzeltilebilir bulgu
  çıkarıyorsa, PR açmadan önce **tur bitene kadar bekle**, sonra tek seferde topla.
  (`kredi-tasarrufu-pr-toplama`)

## 5. Ortam gerçekleri (bu makine)

- Windows 11 + PowerShell 5.1. `&&` ve `||` **yok** — `;` veya `if ($?) { … }`.
  Bash aracı da var, POSIX betikler oraya.
- Klasör adında Türkçe `İ` var; yolu tırnak içine al.
- Python için gerektiğinde `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` öneki.
- Kökteki `git_token.txt` bir **sır** dosyasıdır; beş `.claude/settings.json`'da
  `permissions.deny` ile kapatıldı (ölçüldü 2026-08-04: `Read`, `cat`, `Get-Content`
  üçü de engelli). **Kapsam dışı:** dosyayı kendi açan alt süreç — böyle bir betik yazma.

## 6. Hafıza

Dört depo + kök **tek hafıza havuzunu** paylaşır: `~/.claude/memory/tarlaanaliz/`
(`autoMemoryDirectory` ile 5 yerde sabitlendi). Öğrenilen **değişken durum** oraya yazılır;
bu dosyada **yalnız kalıcı kurallar** durur. `MEMORY.md` indekstir (≤ 200 satır ve ≤ 25 KB —
üstü sessizce yüklenmez), detay konu dosyalarında.

**Oturum sonunda hafıza denetimi:** ① bu oturumda öğrenilen bir şey mevcut bir hafızayı
yanlışlıyor mu → düzelt (silme, ⛔ ile *çürütülmüş* işaretle) ② commit/PR/dal iddiası taşıyan
hafızaları komutla doğrula, doğrulayamıyorsan tarihli bayatlık uyarısı koy ③ `MEMORY.md` ile
klasör birebir mi. Sonucu kapanış mesajında tek satırla bildir. Reçete:
*hafiza-guncelligi-oturum-sonu* (`~/.claude/memory/tarlaanaliz/` altında). **Bayat hafıza, hafızasızlıktan kötüdür.**

## 7. İkinci makinede kurulum

Adım adım reçete **bu deponun içinde, git ile taşınır**: `docs/workspace/KURULUM.md`
(kök işaretçi dosyasının tam içeriği, 5 konumluk `settings.json` şablonu ve kanca
kurulumu orada). Hafıza makine-yereldir; yeni makinede sıfırdan birikir.

---
*İçe-alma doğrulama dizesi — silme: KURAL-GOVDESI-YUKLENDI-7Q4X*
