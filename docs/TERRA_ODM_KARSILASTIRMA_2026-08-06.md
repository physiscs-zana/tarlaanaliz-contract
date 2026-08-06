# Terra ↔ ODM karşılaştırması — kontrollü, üç kollu (2026-08-06)

**Soru (kullanıcı):** *"ODM ile kalibrasyonları yap ve DJI Terra tarafından üretilenle karşılaştır."*

**Tasarım düzeltmesi:** cümlenin düz hâli **iki değişkeni karıştırır** — Terra çıktısı
kalibresiz, ODM `camera+sun` kalibreli. Aradaki fark "motor mu, kalibrasyon mu" ayırt edilemez.
Bu yüzden **üç ODM kolu** koşuldu (aynı 670 fotoğraf, aynı parametreler, yalnız radyometrik
bayrak farklı): `none` · `camera` · `camera+sun`.

## Ham sonuçlar

Ortak ızgaraya getirilmiş, maske-doğru (Terra `nodata=0.0` nöbetçisi dikkate alındı — DK-22),
3.3–3.8 M ortak geçerli piksel.

| Karşılaştırma | Spearman | ort-A | ort-B | "en zayıf %20" IoU |
|---|---:|---:|---:|---:|
| **KALİBRASYON — aynı motor** | | | | |
| ODM camsun ↔ ODM none | 0.759 | 0.266 | 0.181 | 0.355 |
| ODM camsun ↔ ODM **camera** | **0.857** | 0.266 | **0.267** | 0.507 |
| ODM camera ↔ ODM none | 0.747 | 0.267 | 0.182 | 0.353 |
| **MOTOR — farklı motor** | | | | |
| Terra ↔ ODM camsun | **0.299** | 0.263 | 0.270 | 0.176 |
| Terra ↔ ODM none | 0.154 | 0.263 | 0.183 | 0.132 |

## Dört sonuç

### 1. Kalibrasyonun ağırlığı **kamera düzeltmelerinde**, güneş sensöründe değil

`none → camera` ortalama NDVI'yi **0.182 → 0.267** taşıyor (**+%47**). `camera → camera+sun`
ise ortalamayı neredeyse hiç değiştirmiyor (0.267 → 0.266) ve iki kol arasındaki sıra
korelasyonu **0.857**.

**Ürün kararı:** ODM'nin **`camera`** seçeneği (resmen *deneysel değil*) faydanın neredeyse
tamamını veriyor. `camera+sun` — ki ODM onu **"experimental"** diye işaretliyor — küçük bir
rötuş ekliyor. **Deneysel bayrağa bağımlı kalmak gerekmiyor.**

### 2. Terra "kalibresiz" değil, **yarı kalibre** — ve bu ölçüldü

Terra'nın ortalaması **0.263**, ODM'nin **kalibre** çıktısına (0.267) neredeyse eşit; ODM'nin
**kalibresiz** çıktısı ise 0.182. Yani Terra, `use_reflectance_calibration=False` iken bile
kamera düzeyi düzeltmeleri (siyah seviye / kazanç / pozlama) **zaten uyguluyor**; kapalı olan
yalnız panel/DLS adımı.

⛔ **Bu, 2026-08-06 sabahındaki iki ifademi birden düzeltir:**
* *"Kalibrasyon '%85 zayıf'ı ~%62'ye indirir"* — **yanlıştı** (Terra zaten yarı kalibreydi).
* *"Kalibrasyon farkı yalnız %0.6"* — **eksikti**; o, Terra ile karşılaştırmanın sonucuydu.
  Saf kalibrasyon etkisi **+%47**'dir (ODM none ↔ camera).

### 3. Piksel düzeyindeki düşük korelasyonun sebebi **radyometri değil, konumsal kayma**

Terra ↔ ODM Spearman'ı 0.30 çıktı — alarm gibi görünüyor. Hipotez testi: iki raster artan
blok boyutlarında ortalanıp korelasyon yeniden ölçüldü.

| blok | ~yer | Spearman |
|---:|---:|---:|
| 1 px | 5 cm | 0.299 |
| 4 px | 20 cm | 0.386 |
| 10 px | 50 cm | 0.475 |
| 20 px | 1 m | 0.593 |
| 40 px | 2 m | 0.725 |
| 80 px | 4 m | 0.851 |

Korelasyonun blok boyutuyla tırmanması **kayma imzasıdır**; radyometrik/motor farkı olsaydı
blok boyutuna duyarsız kalırdı. Uçuşun kendi kaydı bunu doğruluyor: **RTK hiç FIX olmadı**
(`FIX=0 · FLOAT=0 · SINGLE=114 · NONE=20`), **Georeferencing RMSE 1.838 m** ≈ 5 cm/px'te
**~37 piksel**.

**Ürün kararı:** motor değişimi göründüğü kadar riskli **değil** — iki motor, georeferansın
desteklediği ölçekte (**≥1–2 m**) aynı bölgeleri işaret ediyor. Ama **bölge haritası ~2 m'nin
altında yorumlanmamalı**; ÖN RAPOR'daki "sorunlu bölge" çıktısı bu çözünürlüğe göre sunulmalı.

### 4. W8 / Ç-2 için kanıt

`encoder_version` tetikleyici listesine "kalibrasyon motoru / reflektans ölçeği değişimi"
eklenmeli — çünkü **aynı tarla, aynı fotoğraflar**, yalnız radyometrik bayrak değişince
ortalama NDVI **%47** kayıyor ve "en zayıf %20" bölgesinin **IoU'su 0.355**'e düşüyor.
Bu, saklı FAISS gömmelerini kıyaslanamaz kılacak büyüklüktedir. (W8 bu turda **açık kaldı**.)

---

## Yöntem notları (tekrar üretmek için)

* Betikler: `compare_ndvi.py` (ortak ızgara + Spearman + IoU + Cohen κ) — oturum scratchpad'inde.
* Terra NDVI `masked=True` ile okundu → `nodata=0.0` NaN'a çevrildi. **Bu adım atlanırsa
  ortalama 0.264 yerine 0.1525 çıkar (%42 hata)** — DK-22.
* ODM'de geçerlilik **alpha bandından** gelir (`nodata` beyanı yok).
* Spearman scipy'siz: sıralara Pearson. Örneklem 400.000 piksel, sabit tohum.
* ODM 3.6.1 · `--orthophoto-resolution 5 --feature-quality medium --skip-3dmodel`
  · her kol ~14 dk · GPU gerekmedi.
