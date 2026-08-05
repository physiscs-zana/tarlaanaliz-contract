# DJI Terra — radyometrik düzeltme AÇIK yeniden koşum (DK-21)

> **Neden gerekiyor.** Elimizdeki tek işlenmiş Terra projesi **radyometrik düzeltme kapalı**
> koşuldu. Ölçüldü — proje iş kaydı
> `Documents/DJI/DJITerra/rmziozkan@gmail.com/Multispectral Project_1/records/94280574-*.json`:
> ```
> use_reflectance_calibration = False
> use_sun_sensor_per_image    = False
> radiometricCorrectionSet    = False
> ```
> Yani çıktı **ham DN**'dir (Digital Number = kameranın ham sayısal değeri; yansıma değil).
> Kanonik kural KR-018/082: *"Worker ham DN veya kalibrasyonu belirsiz veriyi kabul etmez."*
> Bu yüzden dürüst bir işte `calibration_type: NONE` yazılır ve worker işi **reddeder**
> (koşuldu, ölçüldü: `"KR-018: Calibration NONE — job rejected"`).
>
> **Panel (yansıma kartı) GEREKMİYOR.** Mavic 3M'in üstündeki **güneş sensörü** yeterli;
> çıktı `RELATIVE` (göreli kalibrasyon) olur ve kapıdan geçer. Panel yalnız `PANEL_ABSOLUTE`
> için gerekir ve o da model eğitimi içindir, ÖN RAPOR için değil.

---

## Başlamadan önce — 3 kontrol

| Kontrol | Durum (2026-08-05'te ölçüldü) |
|---|---|
| Ham fotoğraflar duruyor mu | ✅ `C:\Users\Bilgisayar\Desktop\DJİ_29-07-ÇEKİM\DJI_202607291415_003_ÇimDeneme\` — 674 dosya (670 fotoğraf) |
| Disk yeter mi | ✅ proje ~15 GB yer kaplıyor, C: sürücüsünde **699 GB boş** |
| İnternet gerekiyor mu | Yalnız **Terra açılırken** (lisans kontrolü). İşleme adımı tamamen çevrimdışı çalışıyor (ölçüldü: 9 dakikalık koşuda ilk 1 dakikadan sonra sıfır ağ isteği) |

⚠️ **Eski projeyi SİLMEYİN, ÜZERİNE DE YAZMAYIN.** Yeni bir proje açın. Sebep: bugünkü
demo haritası o eski çıktıdan üretilmiş COG'lara dayanıyor. Yeni koşum beklenmedik bir
sonuç verirse geri dönecek yeriniz olsun.

---

## Adım adım

**1. Terra'yı açın.** İnternet bağlı olsun (lisans önbelleği tazelensin).

**2. Yeni proje oluşturun.**
`New Mission` / `Yeni Görev` → tür olarak **2D Multispectral** (2D Çok Bantlı) seçin.
Ada anlamlı bir şey verin, örneğin: `Dicle_29-07_RADYOMETRIK`

**3. Fotoğrafları ekleyin.**
`Add Images` / `Görüntü Ekle` → şu klasörü seçin:
```
C:\Users\Bilgisayar\Desktop\DJİ_29-07-ÇEKİM\DJI_202607291415_003_ÇimDeneme
```
Terra fotoğrafları **kopyalamaz**, yerinde okur (ölçüldü: proje `images/survey/image_list.json`
doğrudan bu yolu gösteriyor). Yüklenen fotoğraf sayısı **670** çıkmalı.

**4. 🔴 ASIL ADIM — Radyometrik düzeltmeyi AÇIN.**
İşleme ayarları / `Reconstruction Parameters` ekranında, **2D Multispectral** bölümünde
**Radiometric Correction** (Radyometrik Düzeltme) başlığını bulun ve **açın**.

Seçenek listesi çıkarsa şu sırayla tercih edin:
- **Sun sensor** / *Güneş sensörü* (İRRADYANS) ← **bunu seçin**, elimizdeki donanım bu
- *Sun sensor + Reflectance panel* → panel fotoğrafı çekilmediği için **kullanılamaz**
- *None / Kapalı* → **bu, bugünkü hatalı durumdur, seçmeyin**

Diğer ayarlara dokunmayın — çıktının eskisiyle kıyaslanabilir kalması için aynı kalsınlar.

**5. Başlatın.** Önceki koşu **9 dakika 6 saniye** sürdü (13:59:49 → 14:08:55). Benzer bekleyin.

**6. Bitince bana proje adını söyleyin.** Gerisini ben yaparım:
- çıktıyı doğrularım (aşağıdaki komut),
- 4 bandı tek COG'a yığar, MinIO'ya yüklerim,
- işi `calibration_type: RELATIVE` ile kuyruğa basarım,
- ÖN RAPOR bu kez **makineden** çıkar.

---

## Doğrulama — tıklamaya değil, dosyaya bakın

Bu komut kararı verir; ekranda ne yazdığından bağımsızdır. Yeni projenin adını yazın:

```bash
python -c "import json,glob,sys; p=glob.glob(r'C:/Users/Bilgisayar/Documents/DJI/DJITerra/rmziozkan@gmail.com/PROJE_ADI/records/*.json')[0]; d=json.load(open(p,encoding='utf-8')); r=d['recons_params']['build'][0]['recons_params']['parameter']; print('use_reflectance_calibration =', r.get('use_reflectance_calibration')); print('use_sun_sensor_per_image    =', r.get('use_sun_sensor_per_image'))"
```

**Beklenen:** `use_reflectance_calibration = True`. Hâlâ `False` ise düzeltme açılmamıştır —
işleme tekrar koşulmalıdır (çıktıyı elle "kalibre" saymak kapıyı geçmez ve geçmemelidir).

---

## Sonrası — ne değişecek

| | Bugün (ham DN) | Yeniden koşumdan sonra (RELATIVE) |
|---|---|---|
| `calibration_type` | `NONE` | `RELATIVE` |
| Worker kapısı | **REDDEDER** | **GEÇER** |
| `health_distribution` / `mean_ndvi` | üretilmez (fail-closed) | üretilir |
| `absolute_scale_valid` | — | `false` (sınıf sınırları **yaklaşık**; bu dürüstçe etiketlenir) |
| Fine-tuning'e girer mi | hayır | **hayır** — K-3: RELATIVE eğitime girmez, yalnız SSL morfoloji |

**Not (KR-018 gerekçesi):** NDVI bir orandır, ham DN'de bile "doğru görünür" — tuzak budur.
Bozulan şey mutlak eşikler, zaman serisi ve tarlalar arası kıyastır. Ölçülmüş örnek:
Terra'nın NDVI/GNDVI/LCI/NDRE çıktıları formülle birebir uyuştu ama **sabit terimli OSAVI
bozuldu** (0.0337 ↔ 0.2639).
