# Kalibre veri seti nasıl üretilir (DK-21)

> ## ⛔ 2026-08-06 DÜZELTMESİ — bu dosyanın ilk hâli YANLIŞTI
>
> İlk sürüm şöyle diyordu: *"Panel gerekmiyor; Terra'da Radiometric Correction'ı açın,
> **Sun sensor** seçeneğini seçin (~10-15 dk)."* **Bu yanlıştı ve geri alındı.**
> Kullanıcının gönderdiği Terra 5.3.0 ekran görüntüleri gösterdi ki o ekranda
> **"Sun sensor" diye bir seçenek yok**; ekranın tamamı **kalibrasyon paneli**
> (calibration board) içindir. Ders: bir arayüzü görmeden adım adım tarif yazma —
> ölçülebilen kısmı (iş kaydı parametreleri) ölçüp, geri kalanını **soru** olarak bırak.

---

## 1. Sorun (ölçüldü, değişmedi)

Elimizdeki tek işlenmiş Terra projesinin iş kaydı
(`.../Multispectral Project_1/records/94280574-*.json`):

```
use_reflectance_calibration = False
use_sun_sensor_per_image    = False
reflectance_calibration_info = []      <- kalibrasyon paneli listesi BOŞ
```

Çıktı **ham DN**'dir (Digital Number = kameranın işlenmemiş sayısal değeri, yansıma değil).
KR-018/082: *"Worker ham DN veya kalibrasyonu belirsiz veriyi kabul etmez."* Dürüst bir işte
`calibration_type: NONE` yazılır ve worker **reddeder** (koşuldu, ölçüldü:
`"KR-018: Calibration NONE — job rejected"`).

## 2. Terra'nın "Radiometric Correction" ekranı gerçekte ne (ekran görüntüsünden)

| Ekranda ne var | Anlamı |
|---|---|
| Başlık: *Camera Reflectance Factor* | Kamera yansıma katsayısı |
| 3 sekme: *Calibration Board 1/2/3* | Üç adede kadar **kalibrasyon paneli** |
| 5 bant satırı: Blue · Green · Red · Red Edge · Near Infrared (hepsi `NaN`) | Her bant için panelin yansıma değeri |
| Düğme: *Import Calibration Photo* | Panel fotoğrafı içe aktar |
| İpucu metni | *"…add photos for different bands… outline the calibration target… Enter each calibration target's reflectance…"* |

**Sonuç: bu ekran, uçuş sırasında çekilmiş bir kalibrasyon paneli fotoğrafı İSTER.**
Bizim 29-07 uçuşumuzda panel fotoğrafı **yok** → bu yol **geriye dönük tamamlanamaz**.

*(Yan not: ekran **Blue** bandı da istiyor; M3M'de mavi bant yok — diyalog DJI'ın tüm
çok-bantlı kameraları için ortak, M3M'de 5 kutudan 4'ü doldurulur.)*

## 3. Elimizde OLAN — güneş sensörü verisi (ölçüldü, ham karelerin XMP'sinde)

```
DJI_20260729142624_0001_MS_*.TIF  (aynı kare, dört bant)
  G   Irradiance = 16077.6   BlackLevel = 3200   BandFreq = 560(±16)nm
  R   Irradiance = 13096.1   BlackLevel = 3200   BandFreq = 650(±16)nm
  RE  Irradiance = 10038.8   BlackLevel = 3200   BandFreq = 730(±16)nm
  NIR Irradiance =  9741.7   BlackLevel = 3200   BandFreq = 860(±26)nm
ayrıca: SensorGain · SensorGainAdjustment · ExposureTime · VignettingData
uçuş boyunca (134 NIR karesi): Irradiance 9600 → 9742 (%1.5 değişim)
```

**Bu neden önemli:** aynı anda, aynı sahnede bantların irradyansı **%65 farklı**
(G 16078 ↔ NIR 9742). Bu farkı düzeltmeden hesaplanan bant oranları sistematik olarak
kaymış olur — mutlak NDVI eşiklerinin (%85 zayıf gibi) ham DN'de neden güvenilmez olduğu
tam olarak budur.

Yani **veri var**; eksik olan, onu kullanacak motor ayarı.

## 4. Üç gerçek seçenek

### A) Terra + kalibrasyon paneli → **yeni uçuş gerekir**
Panel fotoğrafı sonradan eklenemez. En iyi kalite (mutlağa yakın) ama bir uçuş + bir
yansıma paneli maliyeti var. Yalnız zaten tekrar uçacaksanız mantıklı.

### B) Pix4Dfields ile **aynı fotoğrafları** işle → uçuş gerekmez ⭐
Kanonik metin bunu açıkça söylüyor — `TARLAANALIZ_SSOT_v1_2_0.txt:79`:
> *"Pix4Dfields, M3M için 'tam radyometrik kalibrasyon değil, **göreli (relative)
> kalibrasyon**' sağlar; mutlak reflectance yerine reflectance'a orantılı relatif
> değerler üretir."*

Yani Pix4Dfields, §3'teki güneş-sensörü verisinden **panelsiz** `RELATIVE` üretir —
worker kapısının kabul ettiği tip. Bu makinede **kurulu değil** (ölçüldü). Mevcut uçuşla
ÖN RAPOR'u açan tek yol budur. Lisans/deneme kararı: eylem planı **§12.4 / §12.5**.

### C) Terra'da güneş-sensörü anahtarı gerçekten yok mu — **1 dakikalık kontrol** 🔍
Terra'nın kendi iş kaydında `use_sun_sensor_per_image` diye bir parametre **var**, yani
motor bunu yapabiliyor; ekran görüntüsünde görünmüyor. Karar vermeden önce şuralara bakın:
1. **Radiometric Correction** panelini **en aşağı kaydırın** (ipucu metninin altında bir şey var mı).
2. Ayarlar panelinde **Camera Info** yanındaki **⚙ dişli**.
3. **Preprocessing (AT)** bölümünü açın.

*"Sunlight sensor" / "Irradiance" / "Güneş" geçen bir şey görürseniz bana söyleyin.*
Bulunursa seçenek B'ye gerek kalmaz.

## 5. Karar akışı

```
C'yi yap (1 dk)
   ├─ güneş-sensörü anahtarı BULUNDU → aç, panel fotoğrafı EKLEME, Start Reconstruction
   │                                    → §6'daki komutla doğrula → ÖN RAPOR açılır
   └─ BULUNAMADI → B (Pix4Dfields, uçuş gerekmez)  ya da  A (yeni uçuş + panel)
```

## 6. Doğrulama — ekrana değil dosyaya bakın

Hangi yolu seçerseniz seçin, karar bu komuttadır (yeni proje adını yazın):

```bash
python -c "import json,glob; p=glob.glob(r'C:/Users/Bilgisayar/Documents/DJI/DJITerra/rmziozkan@gmail.com/PROJE_ADI/records/*.json')[0]; r=json.load(open(p,encoding='utf-8'))['recons_params']['build'][0]['recons_params']['parameter']; print('use_reflectance_calibration =', r.get('use_reflectance_calibration')); print('use_sun_sensor_per_image    =', r.get('use_sun_sensor_per_image')); print('reflectance_calibration_info=', r.get('reflectance_calibration_info'))"
```

İkisinden **en az biri `True`** olmalı. İkisi de `False` ise çıktı yine ham DN'dir ve
kapı yine reddeder — çıktıyı elle "kalibre" saymak çözüm değildir.

## 7. Sonrası — ne değişecek

| | Bugün (ham DN) | Kalibre olduğunda |
|---|---|---|
| `calibration_type` | `NONE` | `RELATIVE` (güneş sensörü) / `PANEL_ABSOLUTE` (panel) |
| Worker kapısı | **REDDEDER** | **GEÇER** |
| `health_distribution` · `mean_ndvi` | üretilmez (fail-closed) | üretilir |
| `absolute_scale_valid` | — | `RELATIVE`'de `false` — sınıf sınırları **yaklaşık**, dürüstçe etiketlenir |
| Fine-tuning'e girer mi | hayır | `RELATIVE` **hayır** (K-3: yalnız SSL morfoloji) · `PANEL_ABSOLUTE` evet |

**Not (KR-018 gerekçesi):** NDVI bir orandır, ham DN'de bile "doğru görünür" — tuzak budur.
Bozulan şey mutlak eşikler, zaman serisi ve tarlalar arası kıyastır. Ölçülmüş örnek: Terra'nın
NDVI/GNDVI/LCI/NDRE çıktıları formülle birebir uyuştu ama **sabit terimli OSAVI bozuldu**
(0.0337 ↔ 0.2639).

## 8. Bu ders motor seçimini de etkiliyor

KR-034 motorları **agnostik** sayar (Pix4Dfields *veya* DJI Terra) — ama ikisi **eşdeğer
değil**: aynı panelsiz uçuşta Pix4Dfields `RELATIVE` üretebiliyor, Terra (görebildiğimiz
kadarıyla) panel istiyor. Motor seçimi bir "zevk" meselesi değil, **hangi uçuşların
kurtarılabildiği** meselesi. Bu, eylem planı **Ç-2 / W8** kalemini de güçlendiriyor:
motor değişimi `encoder_version` tetikleyicisi olmalı.
