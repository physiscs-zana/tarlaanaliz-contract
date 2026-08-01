# ÖZ-DENETİM — bir önceki oturumun (2026-08-01, dördüncü tur) işi

**Tarih:** 2026-08-02 · **Kapsam:** `ee4aed7 … 20e541f` (5 commit, doğrudan `master`) +
oturumun beyan ettiği kapanış durumu · **Yöntem:** elle ölçüm (ajan turu değil), her iddia
komutla yeniden üretildi.

> Bu dosya **kanıt arşividir, iş listesi değildir.** Açık kalan işler yalnız
> `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` §14.9'da tutulur.

---

## 1. Beyan edilen kapanış durumu — yeniden ölçüldü

| İddia | Ölçüm komutu | Sonuç |
|---|---|---|
| süit yeşil, `1227 passed / 2 beyanlı xfail` | `python -m pytest tests/ -q` | ✅ **1227 passed, 2 xfailed, 0 skipped** |
| `validate` 164 dosya / 0 hata | `python tools/validate.py` | ✅ **164 / 0** |
| `dist` güncel | `python tools/inline_refs.py --check` | ✅ **68 dosya, yetim yok** |
| dört depo temiz + senkron | `git status` · `git rev-list --left-right --count` | ✅ dördü de `0 0`, çalışma ağaçları temiz |
| dört depoda açık PR yok | `gh pr list --state open` ×4 | ✅ dördü de boş |
| `master` CI yeşil | `gh run list --branch master` | ✅ son 5 push'un 5'i de `success` |
| dedektör C8 için hazır | `python tools/breaking_change_detector.py --old v7.3.0 --new .` | ✅ **9 değişiklik / 0 breaking** (MINOR) |

**Şeffaflık notunun kendisi de doğrulandı:** `ee4aed7` gerçekten süit doğrulanmadan
push'landı; `9c1b829` düzeltmesi **iddiayı zayıflatmadı, güçlendirdi** — eski test yalnız
"küçük harf yazılıyor mu" diyordu, yenisi hem BÜYÜK harfi hem *"edge'in gerçek çıktısı
düzeltme olmadan kanoniği geçiyor"*u (0 doğrulama hatası) zorluyor.

---

## 2. 🔴 Ö1 — CI, yerelde KIRMIZI olan commit'i YEŞİL geçirdi (kök bulgu)

`ee4aed7`'in CI koşusu (**run 30709798931**) `success` döndü:

```
1090 passed, 134 skipped, 2 xfailed
```

Kırılan test (`test_c11_sorties_absorption.py`) **o 134'ün içindeydi.** Bu dosya kardeş
depo fixture'ını okur (`WORKSPACE/tarlaanaliz-edge/tests/fixtures/intake_manifest_valid.json`);
contract CI'ında kardeş depo checkout edilmez → test atlanır.

**⇒ "CI otoriterdir" bu depoda KOŞULLUDUR.** Kardeş-bağımlı kapılar için contract CI
otoriter değildir; süitin **%11'ini** hiç koşmaz.

Ölçülen dağılım (run 30710485267, commit `20e541f`):

| Dosya | CI'da atlanan |
|---|---|
| `tests/test_vendored_parity.py` | 132 |
| `tests/test_c11_sorties_absorption.py` | **2** |
| **Toplam** | **134** (yerelde `1093 + 134 = 1227` ✅ birebir örtüşüyor) |

**Yeniden üretim (yerelde, 20 saniye):** kardeş depoların olmadığı bir ağaca klonla ve koş —
CI'ın gördüğünü birebir gösterir:

```bash
git clone --local . /tmp/ci_sim/tarlaanaliz-contract && cd /tmp/ci_sim/tarlaanaliz-contract && python -m pytest tests/ -q
```

Bu denetimde koşuldu: **`1093 passed, 134 skipped, 2 xfailed`** — GitHub CI çıktısıyla
**birebir aynı**. Yani "CI'da ne görünecek" sorusu push'tan ÖNCE yerelde cevaplanabilir.

---

## 3. 🟠 Ö2 — E17/W10 kaleminin kapsamı bir dosya eksikti *(düzeltildi)*

Plan kalemi *"vendored parite kapısını kardeş CI'da koştur"* diyordu ve yalnız
`test_vendored_parity.py`'yi anıyordu. Ölçüm: kardeş-bağımlı dosya **iki** tanedir.
Kalem eski hâliyle uygulansaydı C11/E16 kapısı **hiçbir CI'da** koşmayacaktı — contract
CI atlıyor, kardeş CI ise çağırmıyor olacaktı. Kalem metni ikisini de adıyla sayacak
şekilde düzeltildi (§14.9 SIRA 3).

---

## 4. 🟠 Ö3 — atlama kapısı DOSYAYA bakmıyordu *(düzeltildi + mutasyonla doğrulandı)*

`tests/conftest.py` → `ALLOWED_SKIP_REASONS` eşleşmesi yalnız **gerekçe alt dizesine**
bakıyordu. Sonuç: `test_c11_sorties_absorption.py` aynı `"kardeş depo yok"` gerekçesiyle
atlamaya başladı ve **adı hiçbir yerde geçmeden** parite süiti için yazılmış beyanın
altına sığındı. Beyanın notu ayrıca bayattı: *"→ 47 test atlanır (ölçüm 2026-08-01: 972
passed, 47 skipped)"* — bugünkü gerçek **134 / 1093**.

**Düzeltme:** beyan artık `(gerekçe, dosya listesi, not)` üçlüsüdür; kapı ikisini birden
zorlar ve rapor satırı dosyayı da yazar.

**Kapı ölçüldü (kapsamı ölçülmeyen kapı, olmayan kapıdır):**

| Mutasyon | Beklenen | Ölçülen |
|---|---|---|
| Beyanlı gerekçeyi **beyansız bir dosyada** kullan (`tests/test_zz_skipgate_probe.py`) | kırmızı | ✅ `ATLAMA KAPISI DÜŞTÜ`, **exit 1** |
| Kontrol: beyanlı iki dosya kardeşsiz ağaçta atlasın | yeşil | ✅ exit 0, `1093 passed / 134 skipped`, ikisi de `[beyanlı]` |

> ⚠️ Ölçüm tuzağı, yine yakalandı: `pytest … | tail` kurulumunda `$?` **tail**'in kodudur;
> mutasyonun gerçek exit kodu boruyu kaldırınca görüldü (bkz. aynı ders, git/CI mekaniği).

---

## 5. 🟡 Ö4 · Ö5 · Ö6 — kararlar koda yazıldı, çevresindeki metin eski dünyayı anlatmaya devam etti *(üçü de düzeltildi)*

Aynı sınıfın üç üyesi; D16'nın kapattığı *"ikinci gövde sessizce çürür"* deseninin **yorum
satırı** hâli:

| # | Nerede | Ne diyordu | Gerçek |
|---|---|---|---|
| **Ö4** | §14.9 SIRA 1 adım 2 | *"bugün 3 beyan açık"*, üçüncüsü `analysis_job` *"(W13'te yapıldı; beyanı sil)"* | `PENDING_PROPAGATION` **2** girişli; `analysis_job` beyanı `527c174`'te **zaten silinmişti** — §14.9 ondan SONRA yazıldı ve bayat kopyaladı. Talimat bir no-op'tu |
| **Ö5** | `test_vendored_parity.py` → `MEASURED_DEBT_VALUES` üstü | *"4 dosya girişi / 5 pointer / 16 değer"* | Sabit doğru (**6**), yorum yanlış: E16 ile iki giriş **aynı commit'te** silinmişti → bugün **2 giriş / 3 pointer / 6 değer** |
| **Ö6** | `test_c11_sorties_absorption.py` modül docstring'i | *"⚠️ BİLİNÇLİ SAPMA (E16): edge küçük harf yazıyor, eşlemeyi C8'de yapacak"* | E16 kapandı; **altındaki testin gövdesi bunun tersini** iddia ediyor |

**Ders (yeni değil, tekrarlanan):** bir kararı uygularken değişen satırın **çevresindeki
gerekçe metni** de kararın parçasıdır. Üç örneğin üçü de aynı oturumda, kararın kendisi
doğru uygulanmışken oluştu.

---

## 6. 🔵 Ö7 — taksonomi karışması (açık, küçük)

W14 ile *"kalıcı, beyan edilmiş eksen farkı"* ilan edilen iki giriş, `KNOWN_VENDORED_AHEAD`
içinde duruyor. O yapının kendi beyanı: *"I-5'e göre **KALICI OLAMAZ** · her giriş bir
BORÇTUR · borç yalnız KÜÇÜLÜR"*. Aynı dosyada kalıcı beyanlar için ayrı bir ev zaten var
(`DECLARED_NARROWER_DEFS`, notu: *"`PENDING_PROPAGATION` geçici borç içindir; burası 'bu
hiç yayılmayacak' beyanıdır"*).

Bugün **delik değil**: iki beyan 6 değerin tamamını doldurduğu için eşik yeni sapmaya yer
bırakmıyor. Ama sayaç artık tanımı gereği 0'a inemez ve yapının değişmez metni yanlıştır.
Yorumla açıklandı; yapısal ayrıştırma C8 sonrasına bırakıldı (§14.9).

---

## 7. Denetimin kendi sınırı

* Ajan turu **açılmadı**; hepsi elle ölçüm. Kapsam: son 5 commit + kapanış beyanları.
* Kardeş depoların (edge/worker/platform) **kendi** son turları bu denetimin dışında.
* `ÖD-0` (`sürüm-riski` lensi) hâlâ borç — bu denetim onun yerine geçmez.
