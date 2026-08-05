# DJI Mavic 3M — kaç indeks üretilebilir ve radyometri gerçekte nasıl işler

**Tarih:** 2026-08-06 · **Yöntem:** sayı alıntılanmadı, **hesaplandı**; kaynaklar aşağıda.

> Bu dosya iki soruyu kapatır: (1) *"4 bantla kaç indeks çıkar?"* — önceki oturumda
> "~50" denmişti, doğrusu ölçüldü. (2) *"Panelsiz kalibrasyon mümkün mü?"* — DJI'ın kendi
> kılavuzu formülü veriyor ve cevap **evet**.

---

## 1. Kaç indeks? — kataloğu filtreleyerek hesaplandı

**Kaynak:** *Awesome Spectral Indices* (ASI) — Montero et al., **Scientific Data 10, 197 (2023)**,
`doi:10.1038/s41597-023-02096-0`. Makine okunur katalog: `output/spectral-indices-dict.json`.
Ağustos 2026 itibarıyla **280 indeks**.

**M3M bantlarının ASI karşılığı** (XMP'den ölçülen merkez ± bant genişliği ile eşleştirildi):

| M3M | XMP `BandFreq` | ASI kodu | ASI aralığı | Eşleşme |
|---|---|---|---|---|
| Green | 560 ± 16 nm | `G` | 510–600 | ✅ tam |
| Red | 650 ± 16 nm | `R` | 620–690 | ✅ tam |
| Red Edge | **730 ± 16 nm** | **`RE2`** | **730–750** | ✅ tam |
| NIR | 860 ± 26 nm | `N` (+ `N2`) | 760–900 (850–880) | ✅ tam |

**Sonuç (üç varsayım, üç sayı):**

| Varsayım | Toplam | Vejetasyon |
|---|---:|---:|
| A) Kırmızı kenar **hiç** kullanılmadan (`G,R,N,N2`) | **68** | 54 |
| **B) M3M'in GERÇEK kırmızı kenarıyla (`+RE2`)** | **72** | **58** |
| C) `RE1`/`RE3` de "kırmızı kenar" sayılırsa (İKAME) | 102 | 87 |

> **Dürüst cevap: 58 vejetasyon indeksi** (tüm alanlar dahil 72). Önceki oturumdaki "~50"
> yanlış değildi ama düşüktü ve dayanaksızdı.

### 🔴 Beklenmedik bulgu — kırmızı kenar sandığınız kadar kapı açmıyor

`B − A = yalnızca 4` indeks. Kırmızı kenarın M3M'de açtığı tek şey:
`GM1` (RE2/G) · `RVI` (RE2/R) · `SR555` (RE2/G) · `TRRVI`.

Sebep: literatürdeki kırmızı-kenar indekslerinin çoğu **`RE1` (695–715 nm)** için
tanımlıdır — Sentinel-2 B5 ve MicaSense/Sentera (~715 nm) bandı. M3M'in bandı **730 nm**.
Kataloğun kanonik tanımı:

```
NDREI = (N − RE1)/(N + RE1)      ← 705 nm sınıfı bant
CIRE  = (N / RE1) − 1
```

**Yani DJI Terra'nın ürettiği "NDRE" katmanı, NDRE'nin tanımlandığı bandı KULLANMIYOR.**
Bu bir hata değil, bir **ikame** — ama sonucu değiştirir ve uydu/başka sensör verisiyle
kıyaslanamaz. SSOT bunu zaten uyarıyor (`TARLAANALIZ_SSOT_v1_2_0.txt`, KR-018/082 içindeki
*"Red Edge Bant Pozisyonu Farkı (Dikkat)"* notu): *"DJI Mavic 3M Red Edge bandı ~730 nm'dir
(Sentinel-2 Band 6'ya yakın)… Bu fark NDRE hesaplamalarında farklı sonuçlar üretir."*
Bu araştırma o uyarıyı **sayıya çevirir: 30 indeks bu ikameye bağlıdır** (C − B).

### Kaç tanesi işimize yarar — ayrı soru

Sayının büyüklüğü yanıltıcıdır. Üç filtre:
1. **Kalibrasyon:** sabit terimli indeksler (OSAVI'nin `+0.16`'sı, SAVI'nin `L`'si, EVI'nin
   `C1/C2`'si) **0–1 yansıma** varsayar. Ham DN'de anlamsızdır — ölçüldü: OSAVI 0.0337 ↔
   beklenen 0.2639 (8 kat sapma). Oran indeksleri (NDVI/GNDVI/NDRE/LCI) formülle birebir uyuştu.
2. **Bilgi tekrarı:** 58'in çoğu aynı iki-bant oranının yeniden parametrelenmişi. Aynı uçuşta
   ölçülen ayrım skoru (üst %25 − alt %25 / std): GNDVI 2.50 · NDRE 2.49 · LCI 2.47 ·
   NDVI 2.38 · OSAVI 2.32 — hepsi aynı sinyali farklı ambalajda veriyor.
3. **DJI'ın kendi platformu yalnız 3'ünü sunuyor** (NDVI, GNDVI, NDRE) — 58'i sunmamasının
   sebebi teknik yetersizlik değil, geri kalanının bağımsız bilgi taşımaması.

**Pratik sonuç:** "58 indeks üretebiliyoruz" bir pazarlama cümlesidir; ürün kararı
*hangi 3-5 indeksin bağımsız bilgi taşıdığıdır*. Terra'nın ürettiği 5'li set
(NDVI/GNDVI/LCI/NDRE/OSAVI) bu iş için zaten yeterli — eksik olan indeks değil **kalibrasyon**.

---

## 2. Radyometri — DJI'ın kendi kılavuzu panelsiz yolu TARİF EDİYOR

**Kaynak:** *Mavic 3M Image Processing Guide* (DJI resmî, 2023-08-29),
`https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/Mavic_3M_Image_Processing_Guide_EN.pdf`

Kılavuzun Eq. 4–6'sı NDVI'yi şöyle tanımlıyor (X = NIR veya Red):

```
X_camera = (I_X − I_BlackLevel) / (SensorGain × ExposureTime / 1e6)      (Eq. 9)
              I_X ve I_BlackLevel, 2^bitnum'a bölünerek normalize edilir

pCam_X        = XMP  drone-dji:SensorGainAdjustment
X_LS × pLS_X  = XMP  drone-dji:Irradiance        ← ÇARPIM DOĞRUDAN saklanıyor

X_ref = (X_camera × pCam_X) / (X_LS × pLS_X) × ρ_NIR                     (Eq. 4/5)

NDVI  = (NIR_ref − Red_ref) / (NIR_ref + Red_ref)                        (Eq. 6)
```

**İki sonuç, ikisi de belirleyici:**

1. **Panel formülde YOK.** Gereken her şey — siyah seviye, kazanç, pozlama, bant-başı
   fabrika katsayısı ve güneş sensörü değeri — fotoğrafın **XMP'sinde**. DJI'ın kendi
   yöntemi **panelsizdir**.
2. **`ρ_NIR` Eq. 6'da sadeleşir** (pay ve paydada ortak çarpan). Bu yüzden çıktı
   **mutlak değil, yansımayla ORANTILI** — yani sözleşmemizdeki `RELATIVE` tipinin
   tam karşılığı. Panel, `ρ`'yu sabitleyip `PANEL_ABSOLUTE`'a çıkarmak içindir.

### Elimizdeki veride ölçülen eksik terim

```
aynı kare → Irradiance   G 16077.6 · R 13096.1 · RE 10038.8 · NIR 9741.7
            SensorGain   G 1.000   · R 1.000   · RE 1.033   · NIR 1.005
            ExposureTime G 732     · R 518     · RE 976     · NIR 976
            BlackLevel   hepsi 3200
R/NIR irradyans oranı = 1.3443     ← UYGULANMAMIŞ olan düzeltme
```

Terra çıktısı bu bölmeyi yapmadı (`use_sun_sensor_per_image=False`), dolayısıyla NDVI'de
R ile NIR arasında **~%34'lük** sistematik bir kayma duruyor.

### Üçüncü motor — Fiji/Metashape değil, **OpenDroneMap (ODM)**

**Kaynak:** `https://docs.opendronemap.org/arguments/radiometric-calibration/` (2026-08-06'da
yeniden doğrulandı; planın 2026-07-30 kaydıyla aynı):

| Değer | Ne yapar |
|---|---|
| `none` | çıktı **digital number** |
| `camera` | siyah seviye + vinyetleme + satır gradyanı/kazanç-pozlama telafisi |
| **`camera+sun`** | `camera`'nın hepsi **+ DLS spektral radyansı, güneş açısı hesaba katılarak** — resmen **"experimental"** |

Yani `camera+sun`, DJI'ın Eq. 4–6 zincirini **kare bazında, mozaiklemeden ÖNCE** uygular.
Panel istemiyor. **Maliyet $0.** M3M desteği **v3.5.3+**.

**Motor karşılaştırması (bu uçuşu kurtarma açısından):**

| Motor | Panelsiz `RELATIVE` | Maliyet | Bu uçuşu kurtarır mı |
|---|---|---|---|
| DJI Terra | ❌ ekranı yalnız panel istiyor | $300/yıl | **Hayır** |
| **OpenDroneMap** | ✅ `--radiometric-calibration camera+sun` | **$0** | **Evet** ⭐ |
| Pix4Dfields | ✅ (SSOT:79) | $1.990/yıl | Evet ama ücretli |
| Metashape Pro | (ayrı iş akışı) | $3.499 kalıcı | — |

> **Fiji/ImageJ bu listede yok** ve olmamalı: genel amaçlı bir görüntü işleme aracıdır,
> fotogrametri + bant hizalama + DLS zinciri sunmaz. Üçüncü motor **ODM**'dir.

**Bilinen risk (planda zaten kayıtlı):** ODM'de M3M **bant hizalama kayması** topluluk
tarafından bildiriliyor; `--skip-band-alignment` ve ön-hizalama seçenekleri var. Pilotta
Terra-NDVI ↔ ODM-NDVI farkı zaten ölçülecek (§4, "en kritik" metrik).

---

## 3. Bu araştırmanın doğurduğu somut karar

Kalibrasyon için **yeni uçuş da, ücretli lisans da gerekmiyor.** Elimizdeki 670 fotoğraf
gerekli tüm radyometrik üstveriyi taşıyor; eksik olan yalnız o veriyi kullanan motor.
**Önerilen sıra:** ODM `camera+sun` (bedava, resmî, panelsiz) → çıktı `RELATIVE` → KR-018
kapısı geçer → ÖN RAPOR makineden çıkar.

---

## Kaynaklar

- Montero, D. et al. *A standardized catalogue of spectral indices…* **Scientific Data 10, 197 (2023)** — https://www.nature.com/articles/s41597-023-02096-0
- Awesome Spectral Indices, makine okunur katalog — https://github.com/awesome-spectral-indices/awesome-spectral-indices
- DJI *Mavic 3M Image Processing Guide* (resmî PDF, 2023) — https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/Mavic_3M_Image_Processing_Guide_EN.pdf
- DJI Mavic 3M SSS (bant merkezleri) — https://ag.dji.com/mavic-3-m/faq
- OpenDroneMap, radiometric-calibration — https://docs.opendronemap.org/arguments/radiometric-calibration/
- OpenDroneMap, multispectral — https://docs.opendronemap.org/multispectral/
- Heliguy, *What vegetation indexes does the DJI Mavic 3 Multispectral support?* — https://www.heliguy.com/blogs/knowledge-base/what-vegetation-indexes-does-the-dji-mavic-3-multispectral-support/
- Kanonik: `docs/TARLAANALIZ_SSOT_v1_2_0.txt` KR-018/082 (Red Edge bant pozisyonu notu, satır 79)
