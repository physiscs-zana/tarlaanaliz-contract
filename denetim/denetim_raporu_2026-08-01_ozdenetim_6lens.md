# Öz-denetim raporu — 6 lens · 2026-08-01

> **BU DOSYA BİR İŞ LİSTESİ DEĞİLDİR.** Kanıt arşividir; her bulgunun `dosya:satır`
> dayanağını ve çalıştırılan komutun çıktısını taşır. Yapılacak işler **yalnızca**
> `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` §14.8'de tutulur.

## Nasıl üretildi

2026-07-31 ve 2026-08-01 oturumlarının çıktısı **6 bağımsız lensten** denetlendi
(karar doğruluğu · kapı etkinliği · ölçüm dürüstlüğü · çapraz-repo bütünlüğü ·
sınıf taraması · yayımlanmış sürüm riski). Her bulgu ayrıca **iki skeptik** tarafından
çürütülmeye çalışıldı (biri "gözden kaçan koruma var mı / bu bilinçli bir karar mı",
diğeri "somut zarar senaryosu yazabiliyor musun").

**Ölçüm:** 109 ajan başlatıldı · 40 tamamlandı · **69'u oturum kotası nedeniyle düştü**
(sentez ajanı ve `sürüm-riski` lensi dahil) · 3.5M token · 1187 araç çağrısı.

## ⚠️ BU RAPORUN BİLİNEN SINIRLARI (dürüstlük notu)

1. **`sürüm-riski` lensi hiç koşmadı** (API hatası) → v7.3.0'ın yayımlanmış içeriği,
   migration-guide gereksinimi ve "TUR 2 açıkken master'ı vendor'lama riski" **denetlenmedi**.
2. **Çürütme eksik kaldı.** 51 bulgunun yalnız 35'i skeptik gördü. Workflow'un eleme
   mantığı "hiç skeptik dönmediyse ele" şeklindeydi → **skeptikleri düşen bulgular
   haksız yere elenmiş olabilir.** Bu yüzden aşağıdaki liste HAM bulgulardır;
   "elendi" damgası güvenilir değildir.
3. **Aşağıdaki üç bulgu oturum sahibi tarafından ELLE DOĞRULANDI** (ajan iddiası kanıt
   sayılmadı) ve gerçek çıktı — plana KRİTİK olarak işlendi:
   * C6b/S2 kararı şemaya yazılmadı (yalnız enum kayıt defterine)
   * S5/W12 tel üstünde ölü (`analysis_job.$defs/CalibrationMetadata` `scale` reddediyor)
   * E13/C6b kapıları kayıt defterini ölçüyor, şemanın inline enum'unu değil
4. Kalan bulgular **doğrulanmamıştır**; plana "önce doğrula" notuyla girdi.

---

# Öz-denetim ham bulgular (51 adet)

## 1. [KRITIK] Worker'ın vendored kopyası yayımlanmış v7.3.0'ın ÖNÜNDE — beyansız AK-4 sapması; proje kendi kapısı bunu "sert hata" ilan ediyor
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-worker/interface/contracts/calibration_metadata.v1.schema.json:55 (`scale` bloğu) + tarlaanaliz-worker/CONTRACTS_VERSION.md:3 (`Version: v7.3.0`)
- **ne yanlış:** Worker `Version: v7.3.0` beyan ediyor, ama vendored `calibration_metadata.v1` içinde `scale` (reflectance_scale + scale_factor) bloğu var. Bu blok yayımlanmış `v7.3.0` etiketinde YOK — kanoniğe S5 (47b30fc) ile etiketten SONRA girdi. Yani "7.3.0" adı altında iki farklı sözleşme dolaşıyor: platform'un pinlediği (submodule a8cf512 = tag) ve worker'ın vendor'ladığı (post-tag master). I-1 hizası yalnız dize düzeyinde doğru, içerik düzeyinde KIRIK. Testin ters yön için yazdığı hüküm net: "Ters yön (vendored ileri) NORMAL DEĞİLDİR: o bir AK-4 sapmasıdır ve sert hata verir" (tests/test_vendored_parity.py:117-118). Sapma I-5'in gerektirdiği hiçbir yerde beyan edilmemiş.
- **kanıt:** 1) Etikette yok: `git show v7.3.0:schemas/worker/calibration_metadata.v1.schema.json | grep -c '"scale"'` → 0 (HEAD'de → 1).
2) Ekleyen commit etiket sonrası: `git merge-base --is-ancestor 47b30fc v7.3.0^{}` → NOT-IN-TAG(post-release); fd929ef de aynı.
3) Projenin KENDİ kapısı, contract yayımlanmış etikette (W10'un plan §2029'da tarif edildiği hâl) koşturulduğunda kırmızı — scratchpad'de izole çalışma alanı kurup ölçtüm (depoda hiçbir şey değiştirilmedi):
   git clone --shared … && git checkout v7.3.0  (→ "contract at: v7.3.0")
   python -m pytest tests/test_vendored_parity.py -q -rs --no-cov  → EXIT=1
   FAILED TestVendoredParity::test_no_vendored_only_properties[calibration_metadata]
   "A
- **neden önemli:** v7.3.0 yayımlandı ve tüketiciler bu pine güveniyor. Bir tüketici "worker sözleşmesi v7.3.0" diye kanonik etiketten çözerse `scale`'i bulamaz; worker'ın çalışan kopyası ise onu tanımlar. Sapma bugün yalnız yerel diskte ölçülebiliyor — hiçbir CI onu görmüyor (W10 henüz yok). Kapalıyken v7.3.0 etiketinin "bu sürüm şu sözleşmedir" anlamı yalan; bir sonraki C8'e kadar her tüketici entegrasyonu bu belirsizlik üzerine kurulur.
- **öneri:** İki dürüst seçenekten biri: (a) S5+S4'ü içeren turu HEMEN C8 ile kapatıp v7.4.0 yayımla ve worker'ı `Version: v7.4.0`'a al — dize ve içerik yeniden aynı şeyi göstersin; ya da (b) tur açık kalacaksa worker CONTRACTS_VERSION.md'ye bu deponun kendi AK-4 kalıbıyla (satır 30/70/81/99'daki "VENDORED DIVERGENCE (§2.1, AK-4)" biçimi) GEÇİCİ + beyanlı sapma kaydı gir ve sürüm dizesini `v7.3.0+scale` gibi ayırt edilebilir hâle getir. Ayrıca test_vendored_parity.py'ye "vendored ileri" yönü için de PENDING_PROPAGATION'ın simetriği bir beyan sözlüğü ekle — bugün bu yön için beyan mekanizması hiç yok, o yüzden sessiz kalabildi.

## 2. [KRITIK] E13 = ABSOLUTE kararı, aynı depodaki kanonik makine-okunur kaynakla (drone_capability_matrix.yaml) ve SSOT'un iki normatif M3M notuyla ÇELİŞİYOR — gerekçe bu üç kaynağı hiç ölçmemiş
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/drone_capability_matrix.yaml:9-20 · docs/TARLAANALIZ_SSOT_v1_2_0.txt:79 · :1014 · tests/test_calibration_type_axis.py (karar kapısı) · docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md §14.7 kalem 6
- **ne yanlış:** E13 kararı, edge'in kalibre manifeste yazacağı değeri filo-genelinde TEK SABİT (`ABSOLUTE`) olarak belirledi. Oysa contract deposunda zaten DRONE BAŞINA bir kalibrasyon sınıfı ekseni var ve DJI_MAVIC_3M için `relative` diyor. SSOT da iki ayrı normatif yerde aynı şeyi söylüyor: 'Pix4Dfields, M3M için tam radyometrik kalibrasyon DEĞİL, göreli (relative) kalibrasyon sağlar'. E13'ün üç gerekçesi (panel zorunlu · motor Pix4D · enum ABSOLUTE'u Pix4D panel diye tanımlıyor) doğru ama YETERSİZ: 'panel + Pix4D ⇒ ABSOLUTE' çıkarımı, tam bu çıkarımı reddeden kaynakları atlayarak yapıldı. Karar metni ve kapı dosyası bu çelişkiyi ne çürütüyor ne de kaydediyor. Ayrıca SSOT kendi içinde tutarsız (satır 457 M1 akışında 'Pix4Dfields ile tam radyometrik kalibrasyon' diyor, satır 79/1014 M3M için bunu açıkça reddediyor) — E13 çelişkinin bir tarafını seçti, çelişkinin varlığını yazmadı.
- **kanıt:** $ grep -n "calibration_class" drone_capability_matrix.yaml
18:    calibration_class: relative      # DJI_MAVIC_3M bloğu (satır 9)
32:    calibration_class: absolute      # DJI_M350_RTK_SENTERA_6X
51/65/77: absolute (Wingtra/Parrot/eBee)

$ sed -n '9,20p' drone_capability_matrix.yaml
  DJI_MAVIC_3M:
    ...
    calibration_class: relative
    notes: > Red Edge ~730 nm ... Pix4Dfields göreli kalibrasyon sağlar.

$ grep -n "göreli (relative) kalibrasyon\|kalibrasyon \*\*görelidir" docs/TARLAANALIZ_SSOT_v1_2_0.txt
79:  > **⚠️ DJI Mavic 3M Radyometri Notu (KR-018 ile birlikte okuyun):** Pix4Dfields, M3M için "tam radyometrik kalibrasyon değil, göreli (relative) kalibrasyon" sağlar...
1014:Pix4Dfi
- **neden önemli:** Demo/pilot filosunun ana aracı DJI Mavic 3M (BASIC_4BAND, kanonik matriste `relative`). E13 uygulandığında (E14/calibrated_validator yazıcısı geldiğinde) M3M paketleri kalibre manifeste `ABSOLUTE` yazacak. O anda: (1) worker'ın `FINETUNE_ALLOWED_CALIBRATIONS` allowlist'i ABSOLUTE'u fine-tuning'e UYGUN saydığı için, SSOT'un 'mutlak radyometrik tutarlılık gerektiren kullanımlarda M3M tercih edilmez' uyarısına rağmen M3M verisi model eğitimine girer; (2) platform'un RELATIVE için ayırdığı 2.0x tolerans gevşemesi devreye girmez; (3) zaman serisi ve training-serving parity iddiaları ölçülemeyen bir temele oturur. Bu, 'sayıyı değil üreteci yayınla' ilkesinin tersi: filo-genelinde sabit bir etiket, üreticiye (drone_type) bağlı gerçeği siliyor.
- **öneri:** E13'ü YENİDEN AÇ ve kararı sabitten üreticiye çevir: yazılacak değer `drone_capability_matrix.yaml → capabilities[drone_type].calibration_class` üzerinden türetilsin (relative→RELATIVE, absolute→ABSOLUTE/PANEL_ABSOLUTE). Kanonik matrisi `calibration_type` ile bağlayan bir kapı yazılsın (matriste `relative` olan bir drone için kalibre manifeste ABSOLUTE yazılamaz). SSOT'un satır 457 ile 79/1014 arasındaki iç çelişkisi ayrı bir kalem olarak kaydedilip giderilsin. Karar korunacaksa, 79/1014 ve matrisin neden geçersiz sayıldığı kararın gövdesine ÖLÇÜMLE yazılsın.

## 3. [KRITIK] E13 kapısı YEŞİL AMA YALAN: kararın değeri (`ABSOLUTE`) edge şemasından silindiğinde 1001 testin tamamı yeşil kalıyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/tests/test_calibration_type_axis.py:61 · tests/test_calibrated_manifest_fields.py:227-253 · schemas/edge/calibrated_dataset_manifest.v1.schema.json:52-58
- **ne yanlış:** E13'ün kapısı olarak ilan edilen `test_calibration_type_axis.py` yalnız `enums/calibration_type.enum.v1.json → x-context-subsets` KAYIT DEFTERİNİ okuyor; kararın fiilen zorlandığı yeri — `schemas/edge/calibrated_dataset_manifest.v1.schema.json`'daki `calibration_type.enum` listesini — hiç okumuyor. Aynı şekilde `test_calibrated_manifest_fields.py`'de PLATFORM için 'kayıt ↔ şema aynı mı' testi VAR (`test_context_subset_is_registered_and_matches`, `test_platform_subset_and_schema_agree_after_none`) ama EDGE için karşılığı yok — edge testi (`test_edge_calibrated_subset_matches_the_c6b_decision`) yalnız enum kaydını doğruluyor.
- **kanıt:** Mutasyon (scratchpad klonu, gerçek depoya DOKUNULMADI):
$ # schemas/edge/calibrated_dataset_manifest.v1.schema.json → enum ['ABSOLUTE','RELATIVE'] yerine ['RELATIVE'] (+ dist/ kopyası da aynı şekilde)
$ PYTHONIOENCODING=utf-8 python -m pytest tests/ -q --no-cov -p no:randomly
1001 passed, 47 skipped, 2 xfailed in 10.94s
→ E13'ün kararı olan değer şemadan TAMAMEN kalktı, HİÇBİR test kırmızıya dönmedi.
(dist/ senkronlanmadan koşulduğunda yalnız tests/test_inline_refs.py::test_check_mode_reports_current_state düşüyor — o da 'dist bayat' diyor, 'ABSOLUTE kayboldu' demiyor.)
$ cd tarlaanaliz-contract && git status --short   → (boş: gerçek depo temiz)
- **neden önemli:** Karar metni ve plan satırı '4/4 mutasyon kırmızı' diyerek kapıyı kanıt olarak sunuyor. Ama o dört mutasyonun dördü de enum METADATA'sına yapılmış; kararın hayatta kaldığı yüzey (şema) kapının görüş alanı dışında. 'Yeşil ama yalan bir kapı, kırmızı bir kapıdan tehlikelidir' ilkesinin tam örneği: bir sonraki tur edge şemasını daraltırsa CI onay verir ve E13 sessizce ölür.
- **öneri:** `test_calibration_type_axis.py`'ye edge ŞEMASINI okuyan iki assert ekle: (1) `E13_DECISION in schemas/edge/calibrated_dataset_manifest.v1 → calibration_result.calibration_type.enum`, (2) enum `x-context-subsets['edge/calibrated_dataset_manifest']` ile şema enum'u KÜME OLARAK eşit. Genel çözüm: `x-context-subsets`'teki HER anahtar için karşılık gelen şema enum'unu parametrik karşılaştıran tek bir test (bugün yalnız platform için elle yazılmış).

## 4. [KRITIK] C6b/S2 'PANEL_ABSOLUTE eklendi' iddiası ŞEMADA UYGULANMADI — yalnız enum kayıt defterine yazıldı; çözdüğü söylenen sorun bugün aynen duruyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/enums/calibration_type.enum.v1.json:50-55 (kayıt) ↔ schemas/edge/calibrated_dataset_manifest.v1.schema.json:52-58 (şema) · commit fd929ef
- **ne yanlış:** C6b kararı: 'edge/calibrated_dataset_manifest alt-kümesine PANEL_ABSOLUTE eklendi — bir paket intake'te PANEL_ABSOLUTE bildirip AYNI istasyonun ikinci belgesinde yazamıyordu'. Ölçüm: değer yalnızca enum'un `x-context-subsets` bloğuna eklendi. Doğrulayan şema (`schemas/edge/calibrated_dataset_manifest.v1.schema.json`) hâlâ `["ABSOLUTE","RELATIVE"]`. Yani intake'te PANEL_ABSOLUTE bildiren bir paket kalibre manifestte AYNI değeri BUGÜN DE yazamıyor — sorun çözülmedi, yalnız çözüldü diye kaydedildi. Üstelik enum kaydı ile şema artık AYRIŞMIŞ durumda (SSOT ikiye bölündü) ve hiçbir kapı bunu görmüyor.
- **kanıt:** $ python -c "import json; e=json.load(open('enums/calibration_type.enum.v1.json',encoding='utf-8')); s=json.load(open('schemas/edge/calibrated_dataset_manifest.v1.schema.json',encoding='utf-8')); print('kayit:',e['x-context-subsets']['edge/calibrated_dataset_manifest']); print('sema :',s['properties']['calibration_result']['properties']['calibration_type']['enum'])"
kayit: ['ABSOLUTE', 'RELATIVE', 'PANEL_ABSOLUTE']
sema : ['ABSOLUTE', 'RELATIVE']
AYRISMA: ['PANEL_ABSOLUTE']

$ git show fd929ef -- schemas/edge/calibrated_dataset_manifest.v1.schema.json
(TEK değişiklik: raw_frames band enum'una "RGB" eklenmesi — S7. calibration_type bloğuna DOKUNULMAMIŞ.)

$ git show fd929ef -- enums/calibrati
- **neden önemli:** Üç katmanlı zarar: (1) C6b/S2 kalemi ✅ işaretlendi ve MINOR sürüm notuna girdi ama fiilen hiçbir davranış değişmedi — plan gerçeği yanlış raporluyor; (2) kanonik sözlüğün kayıt defteri ile zorlayıcı şema arasında sessiz bir ayrışma doğdu (D16'nın 'tek normatif gövde' ilkesinin ihlali, bu kez enum ekseninde); (3) I-3/I-4 yayılımıyla bu ayrışma dört depoya taşındı. Bir tüketici 'kayıt PANEL_ABSOLUTE diyor' diye üretici yazarsa runtime'da şema reddi alır.
- **öneri:** İki yoldan biri, ama YAZILI olarak: (a) şemaya `PANEL_ABSOLUTE` gerçekten eklensin (additive → MINOR, dist + vendored kopyalar dahil) ve C6b böylece kapansın; ya da (b) enum kaydından geri alınsın ve C6b ⬜ açık kaleme çevrilsin. Her iki halde de kayıt↔şema eşitliğini TÜM bağlamlar için zorlayan parametrik test (bkz. önceki bulgunun düzeltmesi) aynı turda yazılsın, yoksa aynı hata başka bir bağlamda tekrarlanır.

## 5. [KRITIK] S5/W12 TEL ÜSTÜNDE ÖLÜ — `analysis_job` kapısı, bu oturumda eklenen `calibration_metadata.scale` alanını REDDEDİYOR
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-worker/interface/contracts/analysis_job.v1.schema.json:147-168 ($defs/CalibrationMetadata, `additionalProperties: false`) · tarlaanaliz-contract/schemas/worker/analysis_job.v1.schema.json:165-180 ($defs/CalibrationMetadata, `unevaluatedProperties: false`) · tüketici: tarlaanaliz-worker/src/application/job_handler.py:136 ve :257
- **ne yanlış:** S5 `scale` bloğunu YALNIZ bağımsız `calibration_metadata.v1.schema.json`'a ekledi. Ama tel üstündeki mesajı doğrulayan şema o değil: `analysis_job.v1.schema.json` içindeki `$defs/CalibrationMetadata`. Aynı normatif gövde İKİ yerde yaşıyor (D16 ihlali) ve S5 turu yalnız birini taradı. İkinci gövde kapalı (`additionalProperties/unevaluatedProperties: false`) olduğu için `scale` taşıyan iş, `job_handler.py:136`'daki `validate_analysis_job()` çağrısında REDDEDİLİYOR ve `:257`'deki `cal_data.get("scale")` satırına HİÇ ulaşmıyor. Aynı boşluk S4 `calibration_method` için de var. W12'nin 22 testi yeşil çünkü hepsi `resolve_reflectance_divisor`/`_parse_job`'ı izole çağırıyor, hiçbiri `validate_analysis_job`'tan geçmiyor — "yeşil ama yalan kapı".
- **kanıt:** Worker'ın KENDİ doğrulayıcısıyla uçtan uca:
```
$ cd tarlaanaliz-worker && python -c "from src.application.contract_validator import validate_analysis_job; ..."
Schema validation failed (jsonschema)
S5 scale TASIYAN is: (False, ["$.calibration_metadata: Additional properties are not allowed ('scale' was unexpected)"])
scale TASIMAYAN is  : (True, [])
```
Kanonik taraf da aynı:
```
$ cd tarlaanaliz-contract && python -c "...jsonschema.Draft202012Validator(s['$defs']['CalibrationMetadata'])..."
hata: 1
   Unevaluated properties are not allowed ('scale' was unexpected)
calibration_method (S4) icin hata: ["Unevaluated properties are not allowed ('calibration_method' was unexpected)"]
```
İki göv
- **neden önemli:** Bu oturumun iki kaleminin (S5 contract yarısı ✅ + W12 worker yarısı ✅) ürettiği yetenek üretimde SIFIR: platform bir gün `scale` yaymaya başlarsa iş **tamamen reddedilir** (analiz hiç koşmaz), yaymazsa özellik hiç tetiklenmez. Daha kötüsü, S5'in doğuş gerekçesi tam olarak buydu — `EVI`/`SAVI` yanlış bölenle sessizce bozuluyor, `NDVI` doğru göründüğü için hatayı maskeliyor (analysis_job.py:56-62 docstring). Yani ölçülen kusur "düzeltildi" sayıldı ama düzeltmenin yolu kapalı. Ayrıca bu, tam olarak LENS 5'in aradığı desendir: bir alanı bir gövdeye ekleyip aynı şeklin ikinci gövdesini taramamak.
- **öneri:** (1) `scale` (ve C8'de `calibration_method`) bloğunu her iki `analysis_job.v1.schema.json` $defs/CalibrationMetadata'sına taşı — kanonikte `unevaluatedProperties`, vendored'da `additionalProperties` idiomuyla. (2) Kalıcı kapı: `tests/test_reflectance_scale_contract.py`'ye (bugün yalnız 3 dosyaya bakıyor: satır 41-43) `analysis_job.$defs.CalibrationMetadata` ⊇ `calibration_metadata.v1.properties` yüklemi ekle; bu iki gövdenin bir daha ayrışmasını yasakla. (3) Davranış testi: `validate_analysis_job()` üzerinden geçen, `scale` taşıyan gerçek bir job'ın KABUL edildiğini assert eden test (izole `_parse_job` testi bunu yakalayamadı). (4) W12'yi plana "kısmen" olarak geri aç.

## 6. [KRITIK] C6b/S2 kararı zorlanan şemaya HİÇ yazılmadı — kapı yalnız enum anotasyonunu ölçtüğü için yeşil kaldı
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** schemas/edge/calibrated_dataset_manifest.v1.schema.json:52-59 (gerçek enum) ↔ enums/calibration_type.enum.v1.json:52 (x-context-subsets kaydı) · kapı: tests/test_calibrated_manifest_fields.py:232-262 · iddia: CHANGELOG.md:18-24
- **ne yanlış:** C6b/S2 kalemi "edge kalibre manifestine PANEL_ABSOLUTE eklendi" diye kaydedildi ve kapı bunu kodladı. Ama değişiklik YALNIZCA `enums/calibration_type.enum.v1.json` içindeki `x-context-subsets` anotasyonuna yapıldı; belgeyi fiilen doğrulayan `schemas/edge/calibrated_dataset_manifest.v1.schema.json` içindeki iç içe (nested) `calibration_result.properties.calibration_type.enum` hâlâ `["ABSOLUTE","RELATIVE"]`. `platform/calibrated_dataset_manifest` için şema↔alt-küme eşitliğini zorlayan bir test VAR (test_calibrated_manifest_fields.py:158-165), edge için YOK. Yani kararın yazıldığı yer ile zorlandığı yer ayrışmış ve tam bu boşluğu kapatmak için yazılan kapı boşluğun yanlış tarafına bakıyor.
- **kanıt:** $ python -c "...her x-context-subsets bağlamını kendi şemasıyla karşılaştır..."
edge/intake_manifest              subset=[ABSOLUTE,DLS2_RELATIVE,PANEL_ABSOLUTE,RELATIVE]  → MATCH (2 form)
edge/calibrated_dataset_manifest  subset=[ABSOLUTE,PANEL_ABSOLUTE,RELATIVE]
                                  schema/properties/calibration_result/properties/calibration_type = [ABSOLUTE,RELATIVE]  ### MISMATCH
worker/analysis_job               → MATCH
worker/calibration_metadata       → MATCH
worker/calibrated_dataset         → MATCH
platform/calibrated_dataset_manifest → MATCH
(6 bağlamın 5'i tutuyor, TEK sapma bu turda değiştirilen bağlam)

$ python -c "Draft202012Validator(edge şeması).iter_errors({... 
- **neden önemli:** CHANGELOG.md:18-24'ün tarif ettiği somut arıza — "bir paket intake'te PANEL_ABSOLUTE bildirip aynı istasyonun ikinci belgesinde aynı değeri yazamıyordu" — HÂLÂ AYNEN duruyor. Edge üreticisi (E14 calibration_result_writer) yazıldığında panel bildiren gerçek bir manifest runtime'da reddedilecek. Dahası kapı, kalemin "yapıldı" işaretlenmesine kanıt olarak kullanıldı: kararı doğrulayan tek delil, kararın uygulanmadığı yerden bağımsız bir metadata satırı.
- **öneri:** (1) `schemas/edge/calibrated_dataset_manifest.v1.schema.json` içindeki `calibration_result.properties.calibration_type.enum`'a `PANEL_ABSOLUTE` eklenip `dist/` yeniden üretilsin. (2) Kapı genelleştirilsin: `x-context-subsets`'teki HER bağlam anahtarı için ilgili şema dosyasındaki `calibration_type` düğümü bulunup `set(enum) == set(subset)` parametrik olarak zorlansın (platform için var olan test:158-165 deseninin tüm bağlamlara açılması). Böylece anotasyon ile yüzey bir daha ayrışamaz.

## 7. [KRITIK] E13 kapısı, docstring'inde adını koyduğu regresyonu görmüyor — DLS2_RELATIVE gerçek şemaya eklenince süit tamamen yeşil
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_calibration_type_axis.py:85-100 (test_dls2_relative_stays_out_of_the_calibrated_package_surface) · ölçtüğü kaynak: tests/test_calibration_type_axis.py:60-66 (_calibrated_subset → yalnız enums/calibration_type.enum.v1.json)
- **ne yanlış:** Dosyanın kendi "BU KAPI NEYİ KORUR" bölümü şunu yazıyor: *"bir sonraki tur 'M3M'de de ışık sensörü var, DLS2_RELATIVE ekleyelim' diyebilir. O ekleme, yanlış donanım adını ve eksen karışıklığını kalibre paket yüzeyine sokar. Kapı bunu kırmızıya çevirir."* Kapı yalnız `enums/*.json` içindeki `x-context-subsets` listesine bakıyor. Bir sonraki turun değeri fiilen kabul ettirmek için değiştireceği yer ise şemadır. Şemaya eklenince kapı hiçbir şey görmüyor.
- **kanıt:** MUTASYON (scratchpad kopyası): edge/calibrated_dataset_manifest.v1 → calibration_result.calibration_type.enum = ['ABSOLUTE','RELATIVE','DLS2_RELATIVE'], ardından `python tools/inline_refs.py --write` ile dist yeniden üretildi.
$ PYTHONIOENCODING=utf-8 python -m pytest tests/ -q --no-cov
1046 passed, 2 skipped, 2 xfailed in 11.78s      ← TEK BİR KIRMIZI YOK
(Aynı değeri enum'un x-context-subsets satırına eklemek kırmızı verir — yani kapı yalnızca kimsenin kullanmadığı yolu koruyor.)
- **neden önemli:** E13, C8 töreninin önündeki kilidi açan karardı ve "C6 iş yok" hükmü buna dayandırıldı. Kapı, kararın tek koruyucusu olarak plana yazıldı (§14.7 / kalem E13). Gerçekte reddedilen değer sözleşme yüzeyine sızabilir ve hiçbir CI bunu görmez: uygulaması olmayan bir MicaSense donanım adı (DLS2) M3M akışına, irradyans yöntemi de calibration_type eksenine karışır — enum'un kendi `x-separate-axis` bloğunun yasakladığı şey.
- **öneri:** `_calibrated_subset()` iki kaynaktan da okusun: enum kaydı VE `schemas/edge/calibrated_dataset_manifest.v1.schema.json` içindeki fiilî enum düğümü. Testler ikisi üzerinde birden koşsun (`@pytest.mark.parametrize("kaynak", ["enum_kaydi","sema"])`). Ek olarak yasak değer için davranış testi: PANEL/DLS2 taşıyan bir belge Draft202012Validator ile doğrulanıp beklenen kabul/ret ölçülsün.

## 8. [YUKSEK] W12'nin okuma kodu ÖLÜ: hiçbir üretici `scale` göndermiyor ve pinlenen şema göndermeyi yasaklıyor — düzeltildi denen sessiz EVI/SAVI hatası hâlâ canlı
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-platform/src/infrastructure/messaging/worker_job_publisher.py:152-154 · tarlaanaliz-platform/contracts/schemas/worker/calibration_metadata.v1.schema.json:56 · tarlaanaliz-worker/src/core/services/inference/pipeline.py:2219-2225
- **ne yanlış:** W12 (worker PR #186) `calibration_metadata.scale`'i iş başına okuyor ve yoksa global env'e düşüyor. Ama (1) platform'un iş yayıncısı `calibration_metadata` sözlüğüne YALNIZCA `calibration_type` koyuyor, (2) platform/edge kaynak ağacında `reflectance_scale`/`scale_factor` üreten tek satır yok, (3) platform'un pinlediği v7.3.0 şeması `unevaluatedProperties: false` ve `scale` özelliğini tanımlamıyor — yani üretici alanı göndermeye kalksa belge şemaya göre GEÇERSİZ olurdu. Sonuç: `resolve_reflectance_divisor` her işte `fallback` dalına düşüyor, bölen yine tüm filo için tek global sabit. W12'nin commit mesajının kendi tarifiyle "NDVI bir orandır → doğru görünür, EVI/SAVI sessizce bozulur" hatası olduğu gibi duruyor; yalnız artık üstüne "düzeltildi" etiketi var.
- **kanıt:** 1) Üretilen belge: worker_job_publisher.py:152-154 →
   "calibration_metadata": { "calibration_type": _map_calibration_type(dataset, calibration_record), }  ← başka alan yok
2) `grep -rn "reflectance_scale|scale_factor" tarlaanaliz-platform/src --include=*.py` → 0 satır; `grep -rn '"scale"' tarlaanaliz-platform/src tarlaanaliz-edge/src | grep -i "calib|reflect|metadata"` → 0 satır (üretici yok).
3) Pinlenen şema kapalı ve alan tanımsız: `python -c "..."` contracts/schemas/worker/calibration_metadata.v1.schema.json → properties: ['calibration_panel_id','calibration_timestamp','calibration_type','irradiance_sensor','red_edge_center_nm','sensor_model'] · grep satır 56: "unevaluatedProperties": 
- **neden önemli:** Radyometrik bölen yanlışsa EVI ve SAVI'nin toplama sabitleri (−7.5·Blue+1.0, +L) anlamsızlaşır ve NDVI doğru göründüğü için hata maskelenir — bu, çiftçiye giden analiz çıktısını sessizce bozan bir sınıf. Plan ve handoff bu kalemi kapanmış sayıyor ("S5+W12 per-job reflektans ölçeği"), dolayısıyla kimse uçtan uca doğrulamaya dönmeyecek. Uçtan uca hiçbir kapı yok: worker tarafı 21 test geçiyor ama üretici tarafı test edilmiyor.
- **öneri:** Aynı turda üretici yarısını da yaz: platform `worker_job_publisher._build_job_dict`'e `calibration_metadata.scale`'i (dataset/calibration_record'dan çözülen `reflectance_scale` + gerekiyorsa `scale_factor`) ekle ve bunu platform pinini v7.4.0'a taşıyan turla birlikte yayımla. Kapı olarak davranış testi koy: yayınlanan iş sözlüğünün pinlenen `calibration_metadata.v1` şemasına karşı jsonschema ile valide edildiği + `scale` taşıdığı bir test (casus değil, gerçek şemayla). Uçtan uca kapanana kadar worker'da `scale_source == "fallback"` durumunu WARN değil, ölçülebilir bir sayaç/alarm olarak tut.

## 9. [YUKSEK] KR-041 sürüm-pin drift kapısı yeşil ama aynı blokta iki sürüm dizesi hâlâ 7.2.0 — kapı sınıfın tek örneğini görüyor
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-platform/src/presentation/api/main.py:186 ve :188 (kapı: tarlaanaliz-platform/tests/unit/infrastructure/contracts/test_contracts_integrity.py:95)
- **ne yanlış:** main.py:183 `ContractsVersionPin(semver="7.3.0")` olarak güncellenmiş, ama hemen altındaki iki log çağrısı eski değeri taşıyor: `logger.info("contract_orchestration_guard_wired", pinned="7.2.0")` ve `logger.error("contracts_version_pin_mismatch_boot_halt", pinned="7.2.0")`. Drift kapısı yalnız `ContractsVersionPin\(semver="(\d+\.\d+\.\d+)"\)` regex'ini arıyor (test_contracts_integrity.py:95), bu yüzden 3 ve 5 satır aşağıdaki yanlış dizelere kör. Handoff bu satırın yakalandığını ve düzeltildiğini yazıyor — düzeltilen tek örnekti, sınıf taranmadı.
- **kanıt:** 1) `grep -rn "7\.2\.0" tarlaanaliz-platform/src --include=*.py` →
   src/presentation/api/main.py:186:        logger.info("contract_orchestration_guard_wired", pinned="7.2.0")
   src/presentation/api/main.py:188:        logger.error("contracts_version_pin_mismatch_boot_halt", pinned="7.2.0")
   (worker ve edge'de canlı kod eşleşmesi yok — edge'deki 3 eşleşme tarihsel yorum satırı.)
2) Kapı buna rağmen YEŞİL: `APP_ENV=test API_JWT_SECRET=… python -m pytest tests/unit/infrastructure/contracts/test_contracts_integrity.py -q --no-cov -k VersionPinDrift` → EXIT=0, "1 passed". Yani kapı, aynı blokta yanlış bir sürüm dizesi dururken geçiyor.
3) Kapının kapsamı okundu: test_contracts_integrity.py:93
- **neden önemli:** `contracts_version_pin_mismatch_boot_halt` bir üretim kesintisi anında yazılan satır: boot fail-closed olup uygulama açılmıyor ve tek teşhis kaynağı bu log. Log "pinned=7.2.0" derken gerçek pin 7.3.0 olduğu için ops yanlış sürümü, yanlış submodule commit'ini ve yanlış checksum'ı araştırır. Ayrıca kapı yeşil olduğu için ekip bu invaryantın korunduğunu sanıyor — "yeşil ama yalan kapı" tam olarak bu.
- **öneri:** İki log çağrısındaki sabiti kaldır, tek kaynaktan besle: `_pin = "7.3.0"` (veya doğrudan `ContractsVersionPin` nesnesinden `.semver`) kur ve hem `pinned_version=` hem iki `logger.*(..., pinned=_pin)` çağrısı aynı değişkeni kullansın — böylece dize fiziksel olarak tek yerde kalır ve drift imkânsızlaşır. Kapıyı da sınıfa genişlet: `main.py` içinde `\d+\.\d+\.\d+` biçimindeki TÜM sürüm dizelerini tarayıp beyan edilenle karşılaştıran bir assert ekle, sonra mutasyonla doğrula (bir dizeyi 7.2.0 yapıp testin kırmızıya döndüğünü gör).

## 10. [YUKSEK] E13'ün ikinci gerekçesi olan 'platform sınırında PANEL_ABSOLUTE'a normalize edilir' kuralı canlı platform kodunda BİLEREK KALDIRILMIŞ — kanonik enum hâlâ öyle diyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/enums/calibration_type.enum.v1.json:16 ve :24 (`x-normalization`) ↔ tarlaanaliz-platform/src/infrastructure/messaging/worker_job_publisher.py:56-73
- **ne yanlış:** Kanonik enum iki yerde 'Platform, edge/worker ABSOLUTE değerini worker PANEL_ABSOLUTE'una normalize eder' diyor ve E13 kararı gerekçe (2)'de tam bu cümleye dayanıyor ('...→ platform sınırında PANEL_ABSOLUTE'a normalize'). Platform kodu bu normalizasyonu KASITLI olarak kaldırmış ve gerekçesini docstring'e yazmış ('ARTIK normalize EDİLMEZ, olduğu gibi geçer — eski ABSOLUTE→PANEL_ABSOLUTE indirme lossy idi, code-review #4'). Yani kanonik sözleşme, tüketicinin bilerek terk ettiği bir davranışı hâlâ normatif olarak ilan ediyor; E13 bu bayat cümleyi ölçmeden kullandı.
- **kanıt:** $ grep -n "Platform sınırında worker PANEL_ABSOLUTE" enums/calibration_type.enum.v1.json
16:    "ABSOLUTE": "Mutlak reflektans (ör. Pix4D panel-tabanlı). Platform sınırında worker PANEL_ABSOLUTE değerine normalize edilir.",
(ve x-normalization → "ABSOLUTE -> PANEL_ABSOLUTE": "Platform, edge/worker ABSOLUTE değerini worker PANEL_ABSOLUTE'una normalize eder")

$ sed -n '56,73p' tarlaanaliz-platform/src/infrastructure/messaging/worker_job_publisher.py
      1. **Dataset.manifest['calibration_type']** ... G-3 unify
         sonrası worker analysis_job.v1 ABSOLUTE'u kabul ettiğinden ARTIK normalize EDİLMEZ,
         olduğu gibi geçer (eski ABSOLUTE→PANEL_ABSOLUTE indirme lossy idi — code-review #
- **neden önemli:** E13'ün 'ABSOLUTE yaz, nasılsa platform PANEL_ABSOLUTE'a çevirir' varsayımı bugün geçersiz. Karar uygulandığında worker'a `PANEL_ABSOLUTE` değil `ABSOLUTE` ulaşacak — ve `PANEL_ABSOLUTE`, enum'un kendi tanımıyla 'Worker spektral eşiklerinin referans kalibrasyonu'. İki değerin worker'da farklı yollara düştüğü en az bir yer ölçüldü (bkz. `is_fine_tuning_eligible` bulgusu). Kanonik metnin canlı davranışı yanlış tarif etmesi, kararı ölçüme değil bayat belgeye dayandırdı.
- **öneri:** Kanonik enum'daki `ABSOLUTE -> PANEL_ABSOLUTE` normalizasyon beyanı ya SİLİNSİN (platform gerçeğine hizalansın) ya da platform kodu beyanı uygulasın — ikisinden biri, yazılı gerekçeyle. Kararı beyandan değil ölçümden türeten bir kapı: contract'ta 'x-normalization'da ilan edilen her eşlemenin tüketici tarafında bir karşılığı olduğunu doğrulayan çapraz-repo testi (D4-b/E17/W10 ile aynı yüzey).

## 11. [YUKSEK] S1 (KRİTİK) fail-open 'CALIBRATED → PANEL_ABSOLUTE güvenlik-ağı' platform kodunda HÂLÂ CANLI; E13'ün 'panel kanıtı yoksa değer UYDURULMAZ, FAIL-CLOSED' iddiası bugün geçersiz
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-platform/src/infrastructure/messaging/worker_job_publisher.py:80-84 · tarlaanaliz-contract/enums/calibration_type.enum.v1.json (`x-superseded-2026-07-31.consumer_obligation`) · tarlaanaliz-edge/src/core/services/calibration_gate/pix4d_runner.py (üretici yok)
- **ne yanlış:** Kanonik enum 2026-07-31'de bu kuralı SUPERSEDED ilan etti ve tüketici yükümlülüğünü açıkça yazdı: 'Platform: yukarıdaki 3. adım kaldırılmalı, tip yoksa NONE yazılmalı'. Kod bugün hâlâ 3. adımı uyguluyor. Aynı anda edge tarafında `calibration_type` üreten HİÇBİR kod yok (E13'ün kalan işi yapılmadı). İkisi birleşince: tipi hiç bildirilmemiş her CALIBRATED paket, platform tarafından `PANEL_ABSOLUTE` (worker spektral eşiklerinin REFERANS sınıfı) olarak etiketleniyor. E13 karar metnindeki 'Panel kanıtı yoksa değer UYDURULMAZ — enum x-normalization.missing FAIL-CLOSED' cümlesi sözleşmede doğru, çalışan sistemde yanlış.
- **kanıt:** $ sed -n '80,85p' tarlaanaliz-platform/src/infrastructure/messaging/worker_job_publisher.py
    # 3. status CALIBRATED → PANEL_ABSOLUTE (güvenlik-ağı).
    status = getattr(calibration_record, "status", None)
    status_val = getattr(status, "value", status)
    if status_val == "CALIBRATED":
        return "PANEL_ABSOLUTE"

$ grep -rn "calibration_type" tarlaanaliz-edge/src/core/services/calibration_gate/pix4d_runner.py | wc -l
0                                   # motor tipi HİÇ yazmıyor
$ grep -n "calibration_type" tarlaanaliz-edge/src/core/services/calibration_gate/calibrated_validator.py
120:            for required_field in ("tool_name", "tool_version", "observed_footprint_wkt", "calib
- **neden önemli:** S1 denetim bulgusunun kendi tanımı: 'Ham DN'yi kalibre reflektans sanan bir NDVI eşiği, tarlada YANLIŞ agronomik karar üretir.' Kanonik taraf düzeltildi ve kapıyla korundu; tüketici tarafı düzeltilmedi ve hiçbir kapı çapraz-repo yükümlülüğü ölçmüyor (D4-b/E17/W10 de koşmuyor — ayrı bulgu). Yani KRİTİK bulgu 'kapandı' görünürken üretimde açık. E13 kararı bu boşluğu kapatmadığı gibi, kapalı olduğunu varsayıyor.
- **öneri:** P-kalemini (D8 tüketici yükümlülüğü) acil sıraya al: `worker_job_publisher.py` 3. adımı kaldırılsın, tip yoksa `NONE` dönsün (fail-closed). Regresyon testi platform tarafında yazılsın. Ayrıca E13'ün edge yarısı (calibration_result_writer / E14) ile aynı turda planlansın — biri olmadan diğeri sistemi ya fail-open bırakır ya da HC-05 kapısında kilitler.

## 12. [YUKSEK] SD8 nüfusu EKSİK ölçüldü: 2.0.1 / 2.1.0 / 4.1.2 sürümleri CONTRACTS_VERSION.md'ye yazılmış ama etiketsiz ve istisna kaydı da yok — I-2 bugün hâlâ tutmuyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/CONTRACTS_VERSION.md (commit'ler f77f62d · 6b802fd · fb021e3) · docs/versioning_policy.md (SD8 kayıt notu) · docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md §14.7 kalem 4
- **ne yanlış:** SD8 sürüm nüfusunu YALNIZ CHANGELOG'dan saydı ('CHANGELOG 19 sürüm, depoda 4 tag → 15 etiketsiz → 14 tag + 1 istisna'). Ama SD8'in KENDİ yöntemi ('release commit = CONTRACTS_VERSION.md'ye `## Version: X.Y.Z` yazıldığı commit') o dosyanın geçmişine uygulandığında 22 sürüm çıkıyor. Fark üç sürüm: 2.0.1, 2.1.0, 4.1.2 — üçünün de release commit'i SD8'in yöntemiyle NET olarak belirlenebiliyor (yani 2.0.2 istisnasının gerekçesi bunlar için geçerli DEĞİL), ama üçü de etiketsiz ve versioning_policy.md'deki istisna notunda da adı geçmiyor. Sonuç: plan ve SDLC_GATES 'I-2 artık tarihsel olarak da tutuyor' diyor; ölçüm bunu doğrulamıyor.
- **kanıt:** $ git log --format=%H --reverse -- CONTRACTS_VERSION.md | while read c; do echo "$(git show -s --format=%cs $c) v$(git show $c:CONTRACTS_VERSION.md | grep -m1 '^## Version:' | sed 's/## Version: //')"; done
...
2026-03-06 v2.0.0   ← tag VAR
2026-03-06 v2.0.1   ← TAG YOK
2026-03-29 v2.1.0   ← TAG YOK
2026-06-14 v3.0.0   ← tag VAR
...
2026-06-23 v4.1.2   ← TAG YOK
2026-06-26 v4.2.1   ← tag VAR

$ for v in 2.0.1 2.1.0 4.1.2; do echo "$v -> $(git log --oneline -S\"## Version: $v\" -- CONTRACTS_VERSION.md | tail -1)  |  CHANGELOG:$(grep -c \"^## \\[$v\\]\" CHANGELOG.md)  tag:$(git tag -l v$v | wc -l)"; done
2.0.1 -> f77f62d audit(contracts): deep SSOT v1.2.0 compliance  | CHANGELOG:0  tag:0
2.1.0
- **neden önemli:** SD8'in tüm değeri 'I-2 tarihsel olarak da tutsun' iddiasında; C8 töreni bu iddiaya dayanarak 'yalan raporlamıyoruz' dedi (plan §14.7 kalem 7: 'I-2 artık tarihsel olarak da tutuyor'). Üç sürüm hâlâ tag'siz olduğu için iddia yanlış — ve bu üçü 2.0.2 gibi 'ölçülemez' değil, tam tersine SD8'in kendi yöntemiyle ölçülebilir. 'Sayıyı değil üreteci yayınla' ilkesi burada tersine döndü: nüfus CHANGELOG'dan (türev) sayıldı, sürüm kilidinden (üretici) değil.
- **öneri:** Nüfusu üreticiden yeniden say: `git log -S'## Version: '` ile CONTRACTS_VERSION.md geçmişindeki TÜM sürümleri çıkar (22). Eksik üçe (2.0.1, 2.1.0, 4.1.2) aynı yöntemle retro annotated tag at — ya da CHANGELOG girdisi olmadığı için 'yayımlanmamış ara bump' sayılıyorlarsa bunu versioning_policy.md'ye 2.0.2 ile aynı özenle YAZ. Kalıcı kapı: 'CONTRACTS_VERSION.md'de görünmüş her sürüm ya tag'lidir ya versioning_policy.md'de adı geçen bir istisnadır' testi.

## 13. [YUKSEK] SDLC_GATES.md release kapısı SD8'i hem 'KARAR BEKLİYOR' hem 'KAPANDI' diyor — bayat blokta yanlış sayı (16) ve artık geçersiz bir YASAK var
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/checklists/SDLC_GATES.md:153-163 (bayat) ↔ :300-310 (güncel); ayrıca :155
- **ne yanlış:** Aynı dosyanın §3 (Release) başlığının hemen altındaki uyarı bloğu hâlâ şunu diyor: '🔴 Koordinatör kararı bekliyor (SD8, §14.6): etiketsiz 16 eski sürüm için retro-tag mı, kayıt notu mu? Karar verilene kadar I-2'nin "tarihsel olarak da tutuyor" biçiminde raporlanması YASAK.' Oysa 140 satır aşağıda (:300) '✅ SD8 KAPANDI (2026-08-01) — I-2 artık tarihsel olarak da tutuyor' yazıyor ve '16 değil 15' düzeltmesini kendisi yapıyor. Üstelik :155'teki '20 sürüme karşılık 4 etiket' ölçümü de :301'deki 'CHANGELOG 19 sürüm, depoda 4 tag' ile çelişiyor. Commit d919141'in mesajı 'SD8 bayat notu SDLC_GATES'ten temizlendi' diyor — temizlik EKSİK yapılmış, iki bayat nottan yalnız biri gitmiş.
- **kanıt:** $ grep -nE '^\s*>?\s*(🔴|⚠️).*(bekliyor|YASAK|karar)' docs/checklists/SDLC_GATES.md
161:> 🔴 **Koordinatör kararı bekliyor (SD8, §14.6):** etiketsiz 16 eski sürüm için

$ sed -n '300,305p' docs/checklists/SDLC_GATES.md
✅ **SD8 KAPANDI (2026-08-01) — I-2 artık tarihsel olarak da tutuyor.** Eski not
*"etiketsiz 16 tarihsel sürüm"* diyordu; ölçüm **15** buldu (CHANGELOG 19 sürüm, depoda 4 tag).
**14'üne** geriye dönük annotated tag atıldı...

$ sed -n '155p' docs/checklists/SDLC_GATES.md
> `vX.Y.Z` etiketi alır"* diyor; ölçüm ise **20 sürüme karşılık 4 etiket** buldu — yani I-2

BUGÜNKÜ GERÇEK:
$ git tag | wc -l → 19    $ git ls-remote --tags origin | grep -v '\^{}' | wc -l → 19
$ git for-each-re
- **neden önemli:** Bu dosya release TÖRENİNİN kendisi — bir sonraki C8'de yukarıdan aşağı okunacak. Okuyan ajan/insan ilk olarak :161'e çarpar, SD8'i AÇIK sanır, I-2'yi 'tarihsel olarak tutuyor' diye raporlamayı kendine YASAK bilir ve büyük ihtimalle ya kararı yeniden açar ya da 14 retro-tag'i tekrar tartışır. Yani kapatılmış bir koordinatör kararı, kapının kendi metni yüzünden yeniden açılır. Ayrıca aynı dosyanın kendi içinde çelişmesi, kapının 'ölçüm otoritesi' iddiasını zayıflatıyor.
- **öneri:** :153-163 bloğunu tamamen sil ya da tarihsel kayıt olarak işaretleyip ':300'e bak — SD8 KAPANDI' yönlendirmesi bırak. :155'teki '20 sürüme karşılık 4 etiket' ifadesini '19 sürüme karşılık 4 etiket' olarak düzelt (ya da 'o gün ölçülen: 19' notu ekle). Kalıcı çözüm: bu dosyada 'karar bekliyor' bloklarını tek bir '§Açık Kararlar' bölümüne topla — böylece kapanan karar tek yerden silinir, iki yerde unutulmaz.

## 14. [YUKSEK] CHANGELOG'da yayımlanan dedektör komutu ÇALIŞMIYOR — 'üreteci yayınla' kuralı ihlal, üstelik --help de yalan söylüyor
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/CHANGELOG.md:111 (yayımlanan komut) · tools/breaking_change_detector.py:863 (--help metni) · :870-875 (gerçek davranış)
- **ne yanlış:** CHANGELOG.md:111 sürüm kararının kanıtı olarak şu komutu yayımlıyor: `tools/breaking_change_detector.py --old v7.2.0 --new .` → *45 değişiklik, 0 breaking*. Bu komut BUGÜN exit 1 ile düşüyor: araç `--old` argümanını yalnız DOSYA SİSTEMİ YOLU olarak ele alıyor (`old_dir = Path(args.old)` + `if not old_dir.exists()`), git etiketi çözümlemesi HİÇ YOK. Buna rağmen `--help` metni 'Old version directory **or tag**' diyor — yani belgeyi bu yanlış yardım metni yazdırmış. (Sayının kendisi doğru: dizin çıkararak yeniden ürettim, 45/0 birebir tuttu. Bozuk olan ÜRETEÇ, sayı değil.)
- **kanıt:** $ cd contract && python tools/breaking_change_detector.py --old v7.2.0 --new .
❌ Old directory not found: v7.2.0      (exit 1)

$ python tools/breaking_change_detector.py --help
  --old OLD     Old version directory or tag        ← 'or tag' YALAN

$ sed -n '863p;870,875p' tools/breaking_change_detector.py
863:    parser.add_argument('--old', required=True, help='Old version directory or tag')
870:    old_dir = Path(args.old)
873:    if not old_dir.exists():
874:        print(f"❌ Old directory not found: {old_dir}")
875:        sys.exit(1)

SAYI DOĞRU — doğru çağrıyla yeniden üretildi:
$ git archive v7.2.0 schemas enums | tar -x -C $S/old720
$ git archive v7.3.0 schemas enums | tar -x -C $S/o
- **neden önemli:** Deponun kendi ana disiplini 'Sayıyı değil üreteci yayınla' — ve bu kural CLAUDE.md'de iki gerçek yanlış teşhisten sonra konmuş. Burada tam tersi olmuş: sayı doğru ama üreteç koşmuyor. MAJOR/MINOR kararı bu tek satıra dayanıyor. Bir sonraki oturum sürüm kararını yeniden doğrulamak istediğinde komut exit 1 verecek; en iyi ihtimalle zaman kaybı, en kötüsü 'dedektör bozuk' teşhisiyle yanlış yere kazma. Ayrıca --help yalan söylediği sürece aynı hatalı komut belgelere tekrar tekrar yazılacak (sınıf hatası).
- **öneri:** İki uçtan da kapat: (1) `main()`'e git-ref desteği ekle — `--old` bir yol değilse `git rev-parse --verify $old` dene, tutarsa geçici dizine `git archive` ile çıkar ve onu kullan; tutmazsa bugünkü hatayı ver. (2) Bu yapılana kadar `--help` metninden 'or tag' ifadesini KALDIR ve CHANGELOG.md:111'i fiilen koşan biçimiyle yaz (ör. `git archive v7.2.0 schemas enums | tar -x -C /tmp/old && python tools/breaking_change_detector.py --old /tmp/old --new .`). (3) Kapıyı mutasyonla doğrula: yayımlanan komutu CI'da bir kez koşturan smoke adımı ekle — belgedeki komut bozulunca CI kırmızı olsun.

## 15. [YUKSEK] Platform main.py'de sürüm sabiti sınıfı YARIM süpürüldü — pin 7.3.0'a çıktı ama iki log satırı hâlâ 'pinned=7.2.0' diyor
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-platform/src/presentation/api/main.py:186 ve :188 (bayat) ↔ :183 (düzeltilmiş)
- **ne yanlış:** Handoff §0.A/3 şunu iddia ediyor: 'Platform kod sabiti: main.py:183 ContractsVersionPin("7.2.0") unutulmuştu → KR-041 drift kapısı yakaladı' (yani bulundu ve düzeltildi). Ölçüm: :183 gerçekten 7.3.0'a güncellenmiş ✅ — ama AYNI try/except bloğundaki iki log çağrısı hâlâ elle yazılmış `pinned="7.2.0"` taşıyor. Drift kapısı bunları görmüyor çünkü sabit `ContractsVersionPin(...)` içinde değil, `logger.info/error` kwarg'ında. Yani 'sınıf tarandı' izlenimi veren düzeltme, sınıfın 3 üyesinden yalnız 1'ini kapatmış; platform src'de bayat 7.2.0 dizesi başka hiçbir yerde yok, sadece bu ikisi.
- **kanıt:** $ grep -rn '7\.2\.0' tarlaanaliz-platform/src/
src/presentation/api/main.py:186:        logger.info("contract_orchestration_guard_wired", pinned="7.2.0")
src/presentation/api/main.py:188:        logger.error("contracts_version_pin_mismatch_boot_halt", pinned="7.2.0")

$ grep -rn '7\.3\.0' tarlaanaliz-platform/src/
src/presentation/api/main.py:183:            pinned_version=ContractsVersionPin(semver="7.3.0"),

BAĞLAM (181-189):
181 |         _app.state.contract_orchestration_guard = ContractOrchestrationGuard(
182 |             validator=validator_service,
183 |             pinned_version=ContractsVersionPin(semver="7.3.0"),
184 |             contracts_version_path=contracts_base.parent / "C
- **neden önemli:** Kullanıcının yazılı kuralı: 'Sınıfı tara, tek örneği düzeltip geçme' — bu kural üç deploy turu kaybettikten sonra konmuş. Burada tam o hata tekrar edilmiş. Somut zarar: :188 bir BOOT-HALT hata yolunda. Pin uyuşmazlığı yaşandığında platform açılmayı reddedecek ve operatöre 'pinned=7.2.0' diyecek — yani olayın teşhisi için var olan tek log satırı yanlış sürümü gösterecek, ops yanlış contract sürümünü araştıracak. :186 ise normal açılışta yanlış sürümü kayda geçiriyor; bu loglar üzerinden sürüm arkeolojisi yapan herkes yanlış tarih çıkarır. Ayrıca handoff bu kalemi 'kapı yakaladı, düzeltildi' diye kapatmış — bir sonraki oturum burayı temiz sanacak.
- **öneri:** Tek kaynağa bağla, ikinci kez elle yazma: `_PINNED = "7.3.0"` (ya da doğrudan `ContractsVersionPin`in kendisinden oku) tanımla, :183/:186/:188 üçü de onu kullansın — böylece sınıfın gelecekteki üyeleri de doğal olarak kapanır. Sonra kapıyı GENİŞLET: KR-041 drift testine 'src/ altında CONTRACTS_VERSION.md'dekinden farklı bir X.Y.Z dizesi geçmesin' yüklemini ekle ve MUTASYONLA doğrula (bir log satırını 7.2.0'a geri çevir, test kırmızı olmalı) — bugünkü kapı bu mutasyonu kaçırıyor.

## 16. [YUKSEK] SINIF 1 (kodlamasız dosya okuma) KAPANMADI — tarama tek depoya yapıldı, 5 üye denildi, dört depoda 135 üye var; üstelik listelenen 5'ten biri yanlış pozitif
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** Plan kaydı: tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1985 (W11) · Açık üretim üyeleri: tarlaanaliz-worker/src/application/contract_validator.py:233 · src/core/services/memory/cold_storage_manager.py:263,293 · src/core/services/training/ssl_pretrain.py:2131 · Planın kaçırdığı worker üyeleri: scripts/download_grape_datasets.py:402,430,436,457 · Planın yanlış pozitifi: src/shared/safe_path.py:19
- **ne yanlış:** W11 "Sınıf tarandı, 4 üye daha" diyor ama tarama (a) yalnız worker deposunda, (b) yalnız `open()` deseniyle, (c) `read_text`/`write_text` olmadan yapılmış. Üç şey birden yanlış: (1) `safe_path.py:19` bir DOCSTRING içindeki örnek kod — AST ayrıştırması orada hiç çağrı bulmuyor, yani liste bir hayalet üye taşıyor; (2) `download_grape_datasets.py`'nin 4 gerçek üyesi (kilit dosyası `read_text`/`write_text`) listede yok; (3) diğer üç depo HİÇ taranmamış — "dört depo tek standart" kuralı uygulanmamış. Ayrıca planın "yapılacak" maddesindeki lint kuralı hiçbir depoda yok: dört pyproject'in hiçbiri ruff `PL`/`PLW1514` (unspecified-encoding) seçmiyor, yani sınıf kapatılsa bile geri büyür.
- **kanıt:** AST tabanlı tarama (binary açıcılar — rasterio/pdfplumber/faiss/MemoryFile/`"rb"`/`"wb"` — ayıklanmış):
```
contract/tests               12
edge(dist-untracked)         24
edge/tests                   24
platform/tests               13
worker/SRC(URETIM)            4
worker/scripts                4
worker/tests                 54
TOPLAM (yanlis pozitifler ayiklanmis): 135
```
Üretim üyeleri hâlâ açık (okundu, 2026-08-01):
```
contract_validator.py:233   with open(schema_path) as f:
cold_storage_manager.py:263 with open(tmp, "w") as f:
cold_storage_manager.py:293 with open(filepath) as f:
ssl_pretrain.py:2131        with open(config_path, "w") as f:
```
`safe_path.py:14-24` okundu → satır 19'
- **neden önemli:** C8'de tam bu kusur 45 testi birden kırdı ve kök neden "okuyucu" değil "okunan dosya" düzeltilerek geçiştirildi. Ölçüm gösteriyor ki koruma tesadüfi: bugün `contract_validator.py:233`'ün okuduğu şemalarda cp1254'te TANIMSIZ bir bayt (0x81/0x8D/0x8E/0x8F/0x90/0x9D/0x9E) bulunmuyor — ama `analysis_type.enum.v1.json`'da bulunuyor ve o dosya yalnız şans eseri başka bir okuyucudan (encoding='utf-8' veren `sub_specialty_resolver.py:81`) geçiyor. Vendored kopyaya bir tırnak (`”` = E2 80 9D) ya da bir Türkçe cümle daha eklenmesi kusuru aynen geri getirir. CI Linux'ta (UTF-8) görünmez; yalnız Windows demo makinesinde (Latitude 7300 + RTX 3090 masaüstü) patlar — yani kusur tam olarak canlı demonun koştuğu yerde uyanır.
- **öneri:** (1) Dört üretim üyesine + 4 script üyesine `encoding="utf-8"` ekle. (2) Sınıfı KALICI kapat: dört deponun ruff `select` listesine `"PLW"` (ya da doğrudan `PLW1514`) ekle — bu, 135 üyeyi tek kuralla görünür kılar ve yeniden büyümesini engeller; test dosyaları için gerekiyorsa `per-file-ignores` ile kademelendir. (3) W11 kaydını düzelt: `safe_path.py:19`'u listeden çıkar (docstring), `download_grape_datasets.py:402,430,436,457`'yi ekle, kapsamı "worker" değil "dört depo" yaz.

## 17. [YUKSEK] PARİTE KAPISI `$defs`'e KÖR ve 16 vendored dosyanın yalnız 9'unu izliyor — S5 boşluğunun geçtiği delik tam burası
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-contract/tests/test_vendored_parity.py:60-98 (PARITY_PAIRS, 9 çift) · :187-193 (test_no_vendored_only_properties) · :197-205 (test_canonical_ahead_is_declared) · :219-227 (test_required_match)
- **ne yanlış:** Kapının üç yüklemi de yalnız ÜST DÜZEY `properties`/`required` sözlüğünü karşılaştırıyor (`set(vj.get("properties", {})) - set(cj.get("properties", {}))`). `$defs`, `allOf`, `oneOf`, iç içe `properties` — hepsi görünmez. Ayrıca PARITY_PAIRS elle tutulan bir liste ve kendini doğrulayan hiçbir bütünlük kontrolü yok (`glob`/`rglob` yalnız satır 242'de, başka bir test için kullanılıyor): 8 worker + 8 edge = 16 vendored dosyanın 9'u listede, 7'si (worker `analysis_job`, `analysis_result`, `analysis_type.enum`, `expert_labeling_card` · edge `intake_manifest`, `scan_report`, `transfer_batch`) kapının tamamen dışında. Kapı, sistemin EN KRİTİK iki tel sözleşmesini — `analysis_job` ve `analysis_result` — hiç görmüyor.
- **kanıt:** Mutasyon testi (scratchpad kopyası, depo bozulmadı) — kapı yüklemi `expert_review_queue` çifti üzerinde:
```
BASELINE : {'vendored_only': [], 'canonical_ahead': [], 'required_diff': ([], [])}
MUTASYON1 (vendored $defs'e SAHTE_VENDORED_ONLY_ALAN sokuldu): {'vendored_only': [], 'canonical_ahead': [], 'required_diff': ([], [])}
MUTASYON2 (kanonik $defs'e yeni alan sokuldu):                  {'vendored_only': [], 'canonical_ahead': [], 'required_diff': ([], [])}
```
Üç sonuç da AYNI → kapı her iki yönde de `$defs` ayrışmasına kör. AK-4 sapması (vendored ileri) ve yayılım borcu (kanonik ileri) — ikisi de sessiz geçiyor.
Kapsam ölçümü: `PARITY_PAIRS` 9 çift; vendored dosya sayımı `find tarlaanaliz
- **neden önemli:** Bu kapı, dört depo arasındaki tek otomatik parite savunması. Kör olduğu iki eksen (nesting + kapsam) tam olarak KRİTİK bulgunun geçtiği eksenler: `scale` alanı `analysis_job.$defs.CalibrationMetadata`'ya eklenmedi ve HİÇBİR test kırmızıya dönmedi (1048 test yeşil). Kapı bugünkü hâliyle "parite var" diyor ama ölçtüğü şey şemaların yalnız en dış kabuğu. Kullanıcının 2026-07-31 dersinin (`breaking_change_detector` iç içe enum'a kör çıktı) aynısı, ikinci bir araçta tekrarlanmış — yani ders sınıf olarak taranmamış, tek araçta düzeltilip geçilmiş.
- **öneri:** (1) Karşılaştırmayı özyinelemeli yap: `$defs`/`allOf`/`oneOf`/iç `properties` içindeki tüm alan-yolu kümesini (JSON-pointer seti) çıkaran bir yardımcı yaz ve üç yüklemi bu küme üzerinde çalıştır — testi mutasyonla doğrula (yukarıdaki iki mutasyon KIRMIZI olmalı). (2) PARITY_PAIRS'i üretece çevir ya da en azından bir bütünlük testi ekle: `interface/contracts` altındaki HER dosya ya listede olmalı ya da gerekçesiyle `PARITY_EXEMPT`'te. (3) `analysis_job` ve `analysis_result`'ı listeye ekle (ikisinde de vendored-only property YOK — ölçüldü — yani ekleme anında yeşil kalır, sadece bundan sonrasını korur).

## 18. [YUKSEK] SINIF 3 (vendored kopyaya prose taşıma) KAPANMADI — 16 vendored dosyanın yalnız 3'ü işaretçiye çevrildi, 13'ü kanonik prose'un tamamını taşımaya devam ediyor
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-worker/interface/contracts/expert_labeling_card.v1.schema.json (10.559 kar. prose, 0 işaretçi) · analysis_result.v1.schema.json (5.097 kar., 0 işaretçi) · expert_feedback.v1.schema.json (2.040 kar., 0 işaretçi) · analysis_type.enum.v1.json (1.672 kar., 0 işaretçi) · analysis_job.v1.schema.json (1.168 kar., 0 işaretçi) · tarlaanaliz-edge/interface/contracts/schemas/edge/*.v1.schema.json (7 dosya)
- **ne yanlış:** C8'de I-4 ihlali "düzeltildi" ama düzeltme yalnız o turda dokunulan alanlara uygulandı. `→ kanonik tanım: ...` işaretçi deseni bugün sadece 3 dosyada var ve onlarda bile kısmi: `calibration_metadata` 8 prose alanının 3'ü (%37), `expert_review_queue` 33'ün 11'i (%33), edge `calibrated_dataset_manifest` 22'nin 5'i (%22 — yalnız C8'in dokunduğu `raw_frames` bloğu). Kalan 13 dosyada oran %0. `expert_labeling_card` vendored kopyası kanonik prose'un %93'ünü (10.559 / 11.305 karakter) ve 25 uzun bloğun 25'ini birebir taşıyor — D16'nın ("normatif gövde TEK yerde") ve I-4'ün ("vendored = DAR alt küme") ikisini birden ihlal ediyor.
- **kanıt:** Prose ölçümü (schema ağacındaki `description`/`title`/`$comment` alanları, işaretçiyle başlayanlar ayrı sayıldı):
```
VENDORED worker/expert_labeling_card: prose_alani=58 toplam_kar=10559 pointer=0 (0%) uzun_prose(>120kar)=25
CANONICAL worker/expert_labeling_card: prose_alani=58 toplam_kar=11305 pointer=0 (0%) uzun_prose(>120kar)=25
VENDORED worker/analysis_result: prose_alani=27 toplam_kar=5097 pointer=0 (0%) uzun_prose=12
VENDORED worker/expert_feedback: prose_alani=19 toplam_kar=2040 pointer=0 (0%) uzun_prose=5
VENDORED worker/analysis_type.enum: prose_alani=24 toplam_kar=1672 pointer=0 (0%) TR_harf=54
--- C8'in dokunduklari (kismi) ---
VENDORED worker/calibration_metadata: prose_alani=8 
- **neden önemli:** İki somut zarar: (1) Sınıf 1'in tetikleyicisi bu prose — vendored dosyalardaki 512/130/92 non-ASCII karakter, `contract_validator.py:233`'ün kodlamasız `open()`'ıyla birleşince C8'deki 45-test çöküşünü üretti; prose durdukça o mayın da duruyor. (2) D16 ihlali: aynı normatif metin iki yerde yaşadıkça sessizce ayrışır — nitekim `expert_labeling_card`'da ayrışma ÖLÇÜLDÜ: vendored `/properties/sub_specialty/description` "v2.7.0 (2026-07-11)" derken kanonik "v2.7.0 (2026-07-12)" diyor ve gerekçeleri farklı ("platform KR-002 renk ratifikasyonu bekliyor" ↔ "worker v1.3.0/v2.7.0'un AK-4 kanonik aynası"). Bu, D16-b2'nin KR gövdelerinde kapattığı kusurun şema tarafındaki hâli.
- **öneri:** (1) C8-a kalemini (EYLEM_PLANI:1986 — `tools/propagate_vendored.py`) SINIFA GÖRE yaz: araç yalnız beyandaki alanları taşımasın, aynı zamanda vendored'daki HER prose alanını `→ kanonik tanım: <yol> · <alan>` işaretçisine indirsin ve bunu 16 dosyanın tamamına uygulasın. (2) Kapı: parite testine "vendored prose bütçesi" yüklemi ekle — `pointer olmayan description karakteri > N` ise kırmızı (N tur başında ölçülüp kademeli düşürülür). (3) Önce en riskli üçünü çevir: `analysis_type.enum` (na=512, cp1254'te sert çöküyor), `expert_review_queue` (na=130), `expert_labeling_card` (na=92, ölçülmüş ayrışma var).

## 19. [YUKSEK] D16-b2 kapısı işaretçi DAMGASINA bakıyor: damga dururken altına çelişkili normatif gövde yazılabiliyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_single_normative_body.py:100-111 (_registry_body_krs / _dual_body_krs) · KNOWN_DUAL_BODY_COUNT=0 iddiası satır 50 · korunan varlık: ssot/kr_registry.md
- **ne yanlış:** `_registry_body_krs()` bir bölümü "gövdesiz" saymak için tek şart arıyor: bölüm metninde `TÜRETİLMİŞ İŞARETÇİ` dizesinin GEÇMESİ. Yani damga bir sigorta değil, bir muafiyet anahtarı: damgayı bırakıp altına istediğin kadar normatif metin yazabilirsin. Kapının kendi docstring'i (satır 101-105) ilk yazımdaki körlüğü anlatıp "artık damgaya bakıyor" diyor — ama körlüğün ikinci yarısı (damga VAR + gövde de VAR) hiç kapatılmamış.
- **kanıt:** MUTASYON (scratchpad): ssot/kr_registry.md → KR-019 bölümünde işaretçi damgası KORUNARAK altına çelişkili normatif kural eklendi ('...48 saat içinde MUTLAKA karara bağlanır; süresi dolan kayıt otomatik olarak FULL_REPORT statüsüne yükseltilir' — kanonik metindeki fail-closed PARTIAL_REPORT davranışının tersi).
$ pytest tests/test_single_normative_body.py tests/test_kr_reference_integrity.py -q --no-cov
130 passed in 0.89s
$ pytest tests/ -q --no-cov
1046 passed, 2 skipped, 2 xfailed      ← AR1'in tam olarak kendisi, tamamen görünmez
- **neden önemli:** D16-b2 bu turun en pahalı kalemiydi (49 gövde elle taşındı) ve gerekçesi "ikinci gövde sessizce çürür" idi — nitekim KR-083 kaldırılmış rol adı, KR-027 donmuş başlık, KR-000 'DJI' ile tam bunu yaşamıştı. Kapı artık "YASAK kipinde, yükseltilemez" diye ilan edilmiş durumda (satır 49) ama yasağı fiilen uygulamıyor: geri dönüşün en olası yolu (birisi işaretçinin altına "kısa bir açıklama" ekler, sonra o açıklama kurala dönüşür) kapının kör noktası.
- **öneri:** Damga varlığını değil, damga DIŞINDAKİ içeriğin biçimini zorlayın. İşaretçi bölümü için beyaz liste: yalnızca damga bloğu (`> 🔗 ...` alıntı satırları) + tek satır `**Applies to:** ... · **Kaynaklar:** ...` + boş satır/ayraç kabul edilsin; bunların dışında kalan her satır sayılsın ve N>0 ise kırmızı. Ek olarak normatif dil dedektörü (MUST/ZORUNLU/YASAK/edilir/reddedilir) işaretçi bölümlerinde yasaklansın.

## 20. [YUKSEK] "Göç taşımadır, silme değil" kapısı BAŞLIK sayıyor — 40 satırlık normatif güvenlik gövdesi silindiğinde yeşil kalıyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_single_normative_body.py:125-137 (test_migration_did_not_delete_definitions) + 139-145 (test_registry_keeps_navigation_headings) · korunan varlık: docs/TARLAANALIZ_SSOT_v1_2_0.txt
- **ne yanlış:** Testin docstring'i tam olarak şu felaketi engellediğini söylüyor: "göç sırasında gövde, kanonik metne yazılmadan silinmiş olabilir". Ama ölçüsü `len(_ssot_defined_krs() | _registry_defined_krs()) >= 55` — yani BAŞLIK sayısı. Başlık kalıp gövde boşalırsa ölçüm değişmiyor. İçerik kaybını gerçekten arayan tek test (test_migration_preserved_the_registry_only_musts, satır 178-207) 14 sabit dizeye bakıyor ve bu dizeler yalnız 4 KR'yi (019/072/092/093) kapsıyor. Geriye 46 göç etmiş KR gövdesi ölçüsüz kalıyor — üstelik D16-b2'den sonra bu dosya bu gövdelerin TEK kaynağı.
- **kanıt:** MUTASYON (scratchpad): docs/TARLAANALIZ_SSOT_v1_2_0.txt → '## [KR-070] YZ Analiz İzolasyonu (Worker Isolation & Egress Policy)' başlığı korunarak altındaki 40 satırlık gövde silindi. Silinen içerikten örnek:
  '1) **Inbound kapalı:** Worker hiçbir koşulda "ingest/upload" HTTP endpoint'i barındırmaz...'
  '2) **Egress allowlist:** Worker yalnızca izinli hedeflere outbound bağlanabilir; internet geneli kapalıdır.'
$ pytest tests/ -q --no-cov
1046 passed, 2 skipped, 2 xfailed in 10.44s      ← hiçbir kapı görmedi
(Ölçüm: birleşim 55 → 55, registry başlık 54 → 54; eşikler tam sınırda olduğu için de değişmedi.)
- **neden önemli:** KR-070 worker izolasyon/egress politikasıdır — modelin çalınma korkusuyla kurulan self-host mimarisinin normatif dayanağı. D16-b2 kararı bu metni "çatışmada o kazanır" ilan etti; dolayısıyla buradaki sessiz boşalma, kuralın hiçbir yerde kalmaması demek. Bir sonraki senkron turu (AK-10 / sync_kr_corpus --apply) boşalmış metni kardeş depolara yayar ve platform/worker kuralı görmez hâle gelir — C-SSOT-2'nin kök nedeninin aynısı, ters yönde.
- **öneri:** Sayımı gövdeye taşıyın: her KR başlığı için gövde uzunluğu (boş olmayan satır sayısı) hesaplanıp bir taban çizgi dosyasına (ör. ssot/kr_body_baseline.json) pinlensin; kapı "hiçbir KR'nin gövdesi taban çizginin %X'inden fazla küçülemez" desin (D16-b2'nin borç-dondurma deseninin aynısı, bu kez içerik üzerinde). Taban çizgi dosyası üretecinin kendisi yayınlansın ("sayıyı değil üreteci yayınla").

## 21. [YUKSEK] Vendored parite kapısı yalnız ÜST DÜZEY properties/required karşılaştırıyor — iç içe her şeye (enum, allOf, koşullu kısıt) tamamen kör
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_vendored_parity.py:188-234 (test_no_vendored_only_properties / test_canonical_ahead_is_declared / test_required_match) — üçü de `set(cj.get("properties",{}))` ve `set(cj.get("required",[]))` ile sınırlı
- **ne yanlış:** Kapı "properties + required düzeyinde EŞDEĞERDİR" diye ilan ediliyor, ama bu iki küme yalnız KÖKTE okunuyor. Bu turun ürettiği değerin neredeyse tamamı iç içe: S5'in `scale` bloğu (enum + allOf koşulu + exclusiveMinimum), AL-C2/D12–D15'in 5 dallı ölçüm-bütünlüğü `allOf`'u, `escalation_reason` enum'una eklenen `AUDIT_SAMPLE`. Kök anahtar adı aynı kaldığı sürece içi tamamen boşaltılabilir.
- **kanıt:** MUTASYON A (scratchpad kardeş kopya) — vendored worker/calibration_metadata `scale` bloğu 4 yerden bozuldu: enum ['reflectance_0_1','reflectance_0_100','scaled_int','unknown'] → ['reflectance_0_1'] · `allOf` (scaled_int→scale_factor koşulu) SİLİNDİ · scale_factor exclusiveMinimum 0 → -1 · required ['reflectance_scale'] → []
$ pytest tests/ -q --no-cov → 1046 passed, 2 skipped, 2 xfailed   ← 45 parite testi + 10 S5 testi yeşil

MUTASYON B — vendored worker/expert_review_queue: 5 dallı `allOf` SİLİNDİ + `escalation_reason` enum'undan AUDIT_SAMPLE çıkarıldı
$ python -c "Draft202012Validator(bozulmus_vendored).iter_errors(ihlalli_satir)"
worker tarafinda artik gecerli mi (M2+M4+C4 ihlali iceren 
- **neden önemli:** Mutasyon B tam olarak KADEME 3'ün (D12–D15) kapattığı arızayı worker tarafında geri açıyor: denetim satırı konsensüse katılabilir (M2 gözlemci etkisi), tile grubuna bağlanabilir (M4 → propagation_precision yapısal olarak 1'e gider, ölçüm kendini doğrular) ve model güvenini tel üzerinde taşır (Ç4 anti-anchoring ihlali). Kanonik tarafta bunların hepsi davranışsal olarak sınanıyor (test_audit_measurement_integrity.py), vendored tarafta hiçbiri. Worker'ın `compute_contracts_hash.py --verify` kapısı ise planın kendi ölçümüyle (W10 satırı) "dosya izinsiz değişmedi" der, "kanonikle uyumlu" DEMEZ.
- **öneri:** Karşılaştırmayı özyinelemeli (recursive) yapın: her iki belge normalize edilip (idiom farkı `unevaluatedProperties`↔`additionalProperties` tek noktada eşitlenerek, açıklama/description alanları düşürülerek) tüm ağaç boyunca `properties` adları, `required` kümeleri, `enum` değerleri ve `if/then/allOf` dal sayıları karşılaştırılsın. PENDING_PROPAGATION de yol tabanlı olsun (ör. `properties.scale.properties.calibration_method`) — bugünkü düz ad listesi iç içe sapmayı beyan edemiyor zaten.

## 22. [YUKSEK] Parite kapısı HİÇBİR CI'da koşmuyor; conftest'teki skip gerekçesi henüz yapılmamış bir işi olmuş gibi beyan ediyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/conftest.py:30-41 (ALLOWED_SKIP_REASONS → "Kardeş depo bu test dosyasını olduğu gibi koşar (E17/W10)") · tests/test_vendored_parity.py:24-40 · plan: docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:2028-2029 (E17, W10)
- **ne yanlış:** D4-b kararı "kapı KARŞI TARAFTA koşar" dedi ve contract tarafı bu kararı beyan olarak yazdı. Ama beyan geniş zamanla kurulmuş ("koşar"), oysa uygulama E17 (edge) ve W10 (worker) kalemleridir ve ikisi de planda ⬜ (açık) durumda. Kardeş depoların workflow dosyalarında `test_vendored_parity` diye bir şey yok. Sonuç: kapı contract CI'ında beyanlı biçimde atlanıyor, kardeş CI'larda hiç çağrılmıyor → 45+ testlik parite süiti YALNIZCA geliştiricinin yerel makinesinde koşuyor. Ayrıca beyandaki ölçüm de bayat: "972 passed, 47 skipped" yazıyor, bugünkü gerçek 1048 passed / 0 skipped (yerelde kardeşler var).
- **kanıt:** $ grep -rn "test_vendored_parity|tarlaanaliz-contract" --include=*.yml tarlaanaliz-{platform,worker,edge}/.github
  (yalnızca platform'da submodule/PAT yorumları çıktı; test_vendored_parity HİÇ geçmiyor)
$ ls tarlaanaliz-worker/.github/workflows → ci.yml, contracts_gate.yml
$ cat tarlaanaliz-worker/.github/workflows/contracts_gate.yml → Stage 1..4: pytest tests/contract/ · compute_contracts_hash.py --verify · validate_model_registry · check_schema_kr025 · kart raporu  → parite adımı YOK
$ cat tarlaanaliz-edge/.github/workflows/contracts_gate.yml → şema geçerliliği + fixture doğrulama + CONTRACTS_VERSION biçimi + verify_contracts_hashes → parite adımı YOK
$ sed -n '2028,2029p' docs/TARLAANALI
- **neden önemli:** Kapının kendisi bu turun en çok kanıt üreten aracı olarak kullanıldı (9 yanlış parite iddiası onunla bulundu, C8 yayılımı onunla ilan edildi). Bugün ise otomatik hiçbir yerde koşmuyor — ve bunu gizleyen şey, contract CI'ının "beyanlı atlama" olarak yeşile boyaması. "Yeşil ama yalan kapı" tanımının tam örneği: beyan doğru sanılıyor çünkü gelecek zamanlı bir karar geniş zamanla yazılmış. D4-b2 (haftalık cron / yerel zorunluluk) da açık; yani bugün tek koruma insan hafızası.
- **öneri:** (1) conftest beyanını GERÇEĞE çevirin: "kardeş CI'da koşar" yerine "E17/W10 kapanana kadar bu kapı YALNIZ yerel koşumda ölçülür (SDLC_GATES §3C)" + ölçüm satırı güncellensin. (2) E17/W10'u kapatın (kardeş `contracts_gate.yml`'a public contract checkout + `pytest tests/test_vendored_parity.py`). (3) Kapanana kadar contract CI'ının özet adımı bugünkü uyarıyı yalnızca `$GITHUB_STEP_SUMMARY`'ye değil, iş sonucuna da yansıtsın (ör. "parite atlandı" durumunda summary job'ı `neutral` değil açık bir uyarı bloğu üretsin ve C8 checklist'inde imza kutusu olsun).

## 23. [YUKSEK] dist/ yayın ağacı hiçbir PII / validate / checksum kapısının kapsamında değil — yetim dosya denetimi de yok
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** dist/schemas/** (E3 ile yayın biçimi ilan edildi, 50260e7) · kapsam dışı kalanlar: tools/validate.py (schemas/+enums/+api/), .github/workflows/contract_validation.yml → check-forbidden-fields işi (yalnız `grep -r ... schemas/`), tools/pin_version.py:94-104 (schemas/, enums/, api/) · tests/test_inline_refs.py:131-141 yalnız ÜRETİLEN dosyaları karşılaştırıyor
- **ne yanlış:** E3 kararıyla `dist/schemas/` "geçici çıktı değil, YAYIN" ilan edildi ve .gitignore'a istisna açıldı (satır 25-26). Ama üç kapı da kaynak ağaca sabitlenmiş durumda. `test_inline_refs.py::test_check_mode_reports_current_state` yalnızca üreticinin ürettiği yolları dist ile karşılaştırıyor; dist içinde üreticinin bilmediği bir dosya varsa (yetim) hiç bakılmıyor. Sonuç: tüketicinin gerçekten okuduğu ağaç, KR-050'yi (CLAUDE.md'de "Hard Security Requirement") zorlayan hiçbir kapıdan geçmiyor.
- **kanıt:** MUTASYON (scratchpad): dist/schemas/core/legacy_login.v1.schema.json eklendi — properties: email, otp, tckn.
$ pytest tests/ -q --no-cov          → 1046 passed, 2 skipped, 2 xfailed
$ python tools/validate.py; echo $?  → validate rc=0
$ grep -r -i -E '"(email|e_mail|tckn|tc_kimlik_no|otp|one_time_password)"' schemas/; echo $?  → 1 (CI kapısı: TEMİZ)
$ grep -r -i -E '"(email|tckn|otp)"' dist/
  dist/schemas/core/legacy_login.v1.schema.json:  "properties": { "email": ..., "otp": ..., "tckn": ... }
$ grep -n "rglob" tools/pin_version.py → 94: schemas_dir · 99: enums_dir · 104: api_dir   (dist YOK → agrega checksum da kapsamıyor)
- **neden önemli:** Hava-boşluklu M1 ve kardeş depolar bu ağacı okuyacak (E3'ün gerekçesi buydu). Yayın ağacında PII taşıyan bir şema, hem KR-050'yi hem CI'ın kendi "check-forbidden-fields" vaadini boşa çıkarır; üstelik agrega checksum dist'i kapsamadığı için tüketici tarafındaki hash doğrulaması da bunu göremez. Bugün fiilen temiz olması (68/68 dosya üretilenle birebir) tesadüf değil ama kapı değil — kapı yok.
- **öneri:** (1) `tools/validate.py` ve CI'ın grep işi `dist/schemas/` ağacını da tarasın (tek satırlık kapsam genişletmesi). (2) test_inline_refs'e yetim kapısı: `set(dist dosyaları) == set(produced.keys())` assert'i. (3) `pin_version.py` agrega checksum'a `dist/schemas/**` dahil edilsin ya da dist için ayrı bir yayın-checksum bloğu üretilsin — aksi hâlde "yayın biçimi" pinlenmemiş bir yüzey olarak kalır.

## 24. [ORTA] Worker CONTRACTS_VERSION.md'de v7.3.0 changelog girdisi hiç yok — sapma beyanının yaşadığı tek yer boş bırakılmış
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-worker/CONTRACTS_VERSION.md:3 (başlık v7.3.0) vs :10 (changelog v7.2.0 ile başlıyor)
- **ne yanlış:** Dosya `Version: v7.3.0` diyor ama "Changelog:" bölümü doğrudan `v7.2.0 (2026-07-18)` ile başlıyor; v7.3.0 için tek satır yok. Oysa v7.3.0'da worker'da iki ayrı commit vendored şemaları değiştirdi: 73fa09e (C8 yayılımı — 8 denetim alanı + AUDIT_SAMPLE + allOf) ve ed44426 (W12 — `scale`). Bu deponun kendi konvansiyonunda her sürüm girdisi aynı zamanda AK-4 sapma beyanının taşıyıcısı (satır 30/70/81/99: "VENDORED DIVERGENCE (§2.1, AK-4)"). Girdi yazılmayınca 1 numaralı bulgudaki sapmanın beyan edileceği yer de hiç açılmamış oldu.
- **kanıt:** 1) `grep -c "v7.3.0 (" CONTRACTS_VERSION.md` → 0
2) `grep -nE "^  v[0-9]+\.[0-9]+\.[0-9]+ \(" CONTRACTS_VERSION.md` → ilk girdi satır 10: "v7.2.0 (2026-07-18)" (v7.3.0 atlanmış)
3) İki commit vendored dosyaları değiştirdi: `git log --oneline -3 -- interface/contracts/calibration_metadata.v1.schema.json` → ed44426 (W12) · `git log --oneline -6 -- CONTRACTS_VERSION.md` → ed44426, 73fa09e
4) ed44426'nın CONTRACTS_VERSION.md'ye tek dokunuşu öz-hash yenilemesi: commit gövdesi "KR-041 öz-hash yeniden üretildi." (sürüm girdisi eklenmemiş)
- **neden önemli:** Öz-hash kapısı "vendored dosya izinsiz değişmedi" der, "neyin neden değiştiği yazıldı" demez — planın W10 satırı (:2029) bu boşluğu zaten ölçmüş. Sürüm girdisi olmayınca worker'ın v7.3.0'da kanonikten nerede ayrıldığı hiçbir yerde okunamıyor; bir sonraki C8'de yayılımı yapacak kişi neyin taşınacağını dosyadan çıkaramaz.
- **öneri:** CONTRACTS_VERSION.md'ye `v7.3.0 (2026-08-01)` girdisi ekle; iki değişimi ayrı ayrı yaz (C8 absorpsiyonu: expert_review_queue 8 denetim alanı + AUDIT_SAMPLE + allOf · W12: calibration_metadata `scale`) ve W12 satırını mevcut "VENDORED DIVERGENCE (§2.1, AK-4)" kalıbıyla GEÇİCİ sapma olarak işaretle, kapanış koşulunu (bir sonraki C8 / v7.4.0) yaz. Kapı önerisi: contracts_gate.yml'a "CONTRACTS_VERSION.md başlığındaki sürüm için changelog girdisi VAR" biçim kontrolü ekle (edge a5b76ba'da benzerini zaten yapmış: "CONTRACTS_VERSION kapısı sayıyı değil BİÇİMİ zorlasın").

## 25. [ORTA] Kanonik PENDING_REPIN tur beyanı bayat: kapanmış tek bir dalı ve turun beşte birini anlatıyor
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-contract/CONTRACTS_VERSION.md:8 ve :20
- **ne yanlış:** Satır 8: "**Checksum State:** PENDING_REPIN — tur `feat/s5-reflectance-scale` sürüyor" ve satır 20: "**Tur içeriği:** S5 — worker/calibration_metadata.v1'e reflektans ölçeği (scale) bloğu." İkisi de yanlış: o dal PR #23 ile merge edildi (f7fe9b7) ve turun içine ondan sonra PR #24 ile C6b/S2 · S4 · S6 · S7 de girdi. Aynı deponun diğer iki kaydı doğruyu söylüyor — CHANGELOG [Unreleased] hem S5 hem dört kalemi listeliyor, SESSION_HANDOFF "Bu tur S5 · C6b/S2 · S4 · S6 · S7 taşıyor" diyor. Yani üç kayıttan biri ayrışmış ve ayrışan, tam da kapıların okuduğu beyan dosyası.
- **kanıt:** 1) `grep -n "Checksum State|Tur içeriği|feat/s5" CONTRACTS_VERSION.md` → 8: "PENDING_REPIN — tur `feat/s5-reflectance-scale` sürüyor" · 20: "Tur içeriği: S5 — …"
2) Turda gerçekte iki merge var: `git log --oneline v7.3.0..HEAD --merges` → 2a8f1af "Merge PR #24: C6b/S2 · S4 · S6 · S7 + MAJOR turu planı (TUR 2)" · f7fe9b7 "Merge PR #23: S5 …"
3) Karşı kayıtlar doğru: `grep -n "^## \[|^### " CHANGELOG.md` (Unreleased bloğu) → "### C6b/S2 · S4 · S6 · S7 …" ve "### S5 …" ikisi de [Unreleased] altında (satır 10-108 arası)
4) Etkilenen şemalar S5'ten ibaret değil: post-tag eklenenler platform/calibrated_dataset_manifest.v1 `$defs/reflectance_scale` (S6) ve worker/calibration_metadata `calibration_m
- **neden önemli:** Bu dosya üç kapının (CI checksum işi, test_pin_version, test_pending_propagation_is_empty) okuduğu makine-okunur beyan; D5/D6 kararları özellikle "koşul makine-okunur beyandan okunuyor" diye kurulmuş. Beyanın prose yarısı yanlış olunca C8 töreninde "turda ne vardı" sorusuna bu dosyadan bakan kişi S4/S6/S7'yi atlar — SD7'nin kapatmaya çalıştığı bayat-beyan sınıfının aynısı, sadece bir seviye yukarıda.
- **öneri:** Satır 8'i dal adından arındır (dal adı zaten merge sonrası anlamsız): "PENDING_REPIN — TUR 2 açık" yeterli. Satır 20'yi CHANGELOG [Unreleased] başlıklarıyla aynı listeye getir (S5 · C6b/S2 · S4 · S6 · S7). Kalıcı çözüm: bu satırı elle yazma — `pin_version.py` zaten dosyayı baştan üretiyor; tur içeriğini CHANGELOG [Unreleased] `###` başlıklarından türetip yazsın, böylece iki gövde ayrışamaz (D16 ilkesi bu metne de uygulanmış olur).

## 26. [ORTA] Eylem planı W12'yi hâlâ ⬜ gösteriyor ve tersine dönmüş bir kararı yürürlükteymiş gibi uyarı olarak taşıyor
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1852
- **ne yanlış:** Satır hâlâ "⬜ **W12** 🟠 … Sözleşme alanı eklendi ama worker hâlâ global env okuyor" diyor ve şunu emrediyor: "⚠️ Yayılım (vendored kopyaya alan taşıma) okuma kodu hazır olmadan yapılmamalı — alan ölü taşınır." Oysa W12 worker'da merge edildi (ed44426 / PR #186), okuma kodu yazıldı ve yayılım da yapıldı. Kararın değiştiği contract deposunda kayıtlı: test_vendored_parity.py:131-135 "Yayılımı C8'e bırakma kararı W12'de DEĞİŞTİ ve sebebi ölçüldü…". Ayrıca satırın bağımlılık sütunu "S5 · PENDING_PROPAGATION beyanı" diyor ama `scale` o beyandan çıkarıldı.
- **kanıt:** 1) Plan: `grep -n "W12" docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` → tek satır 1852, başında "⬜"
2) İş yapıldı: `cd tarlaanaliz-worker && git log --oneline -3` → 8d26fab "Merge PR #186: W12 — per-job reflektans ölçeği okunuyor (S5'in worker yarısı)"
3) Okuma kodu mevcut: `grep -rn "resolve_reflectance_divisor" tarlaanaliz-worker/src` → analysis_job.py:46 (tanım), job_handler.py:264, pipeline.py:2219-2220
4) Karar değişimi contract'ta yazılı: tests/test_vendored_parity.py:130-135 "✅ `scale` (S5) beyandan ÇIKTI: worker W12 turunda hem okuma kodunu yazdı hem alanı vendor'ladı."
- **neden önemli:** Eylem planı §14 iş listesinin TEK kaynağı olarak ilan edilmiş; yanlış olduğunda hem yapılmış iş tekrar açık görünür hem de artık geçersiz bir yasak ("yayılım yapılmamalı") yürürlükte sanılır. Bir sonraki oturum bu satıra bakıp ya işi tekrar yapmaya kalkar ya da yapılmış yayılımı hata sanıp geri alır. Bu satırın ⬜ kalması ayrıca 1 ve 2 numaralı bulguların gözden kaçmasının doğrudan sebebi: "W12 daha yapılmadı" diyen bir plan, W12'nin ölü çıktığını sormaz.
- **öneri:** Satır 1852'yi ⬜→✅ çevir; "okuma kodu yazıldı + vendored'a `scale` taşındı (worker ed44426 / PR #186), yayılım kararı W12'de değişti ve sebebi test_vendored_parity.py:131-135'te kayıtlı" diye güncelle; bağımlılık sütunundan artık geçersiz olan "PENDING_PROPAGATION beyanı" atıfını kaldır. AYNI SATIRDA yeni bir açık kalem aç: "W12-b — üretici yarısı yok, okuma kodu ölü" (bu raporun 2 numaralı bulgusu) ki iş bitmemişken ✅ görünmesin.

## 27. [ORTA] D4-b uygulaması hiç yapılmadı: E17/W10 kardeş CI adımları eklenmemiş — parite kapısı BUGÜN hiçbir CI'da koşmuyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-edge/.github/workflows/contracts_gate.yml · tarlaanaliz-worker/.github/workflows/contracts_gate.yml · tarlaanaliz-platform/.github/workflows/contract_validation.yml · plan §14.7 E17/W10 satırları
- **ne yanlış:** D4-b kararı ✅ işaretli ve gerekçesi sağlam (görünürlükler doğrulandı). Ama kararın tek somut çıktısı — kardeş CI'ların contract'ı checkout edip `tests/test_vendored_parity.py`'yi koşması — üç kardeş depodan hiçbirinde yok. Contract kendi CI'ında 47 testi atlıyor (beyanlı), kardeşlerde ise adım hiç yok. Yani çapraz-repo sapmayı gören kapı ne burada ne orada koşuyor; yalnız C8 öncesi elle yerel koşum var (D4-b2'de (ii) olarak yazılı). Karar metninin şimdiki zamanlı 'kapı KARŞI TARAFTA koşar' ifadesi bugün için doğru değil; doğrusu 'koşacak'.
- **kanıt:** $ grep -n "tarlaanaliz-contract\|vendored_parity\|repository:" tarlaanaliz-edge/.github/workflows/contracts_gate.yml tarlaanaliz-worker/.github/workflows/contracts_gate.yml tarlaanaliz-platform/.github/workflows/contract_validation.yml
tarlaanaliz-platform/.github/workflows/contract_validation.yml:51: echo "   Çözüm: tarlaanaliz-contract'a read erişimli bir PAT'i CONTRACTS_TOKEN"
tarlaanaliz-platform/.github/workflows/contract_validation.yml:55-56: (submodule URL yorumu)
→ edge ve worker workflow'larında contract checkout'u veya vendored_parity çağrısı SIFIR eşleşme.

$ grep -n "name:" tarlaanaliz-edge/.github/workflows/contracts_gate.yml
16: Validate JSON Schemas · 27: Validate all schemas 
- **neden önemli:** Y3/AR4'ün kökü — 'çapraz-repo sapmayı CI'da gören kapı yok' — açık duruyor. Bu tam olarak yukarıdaki iki bulgunun (C6b kayıt↔şema ayrışması, D8 tüketici yükümlülüğünün uygulanmaması) yakalanmadan geçmesine izin veren boşluk. Karar 'kağıt üzerinde' kalmış durumda: gerekçe ölçüme dayanıyor, uygulama yok, ama plan satırı ✅.
- **öneri:** E17 ve W10'u ayrı PR'larla gerçekten ekle (contract PUBLIC olduğu için `actions/checkout` + `repository: physiscs-zana/tarlaanaliz-contract` + `path:` yeterli, ek sır yok). Eklenene kadar plan satırındaki D4-b durumu '✅ karar / ⬜ uygulama' olarak İKİ AYRI işaretle gösterilsin — bugünkü tek ✅, kapının koştuğu izlenimi veriyor. D4-b2'nin (i) seçeneği (haftalık `schedule: cron`) aynı PR'da değerlendirilsin, yoksa 'kanonik değişti, tüketici PR açmadı' hâli görünmez kalmaya devam eder.

## 28. [ORTA] Worker'da fine-tuning uygunluk politikası İKİ YERDE ve farklı: `is_fine_tuning_eligible()` ABSOLUTE'u dışlıyor, allowlist içeriyor — E13 = ABSOLUTE bu ayrışmayı canlı hale getirdi
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-worker/src/core/domain/analysis_job.py:39-44 ↔ src/core/domain/enums.py:67-79
- **ne yanlış:** `enums.py` FINETUNE_ALLOWED_CALIBRATIONS'ı 'SINGLE SOURCE OF TRUTH' ilan ediyor ve yorumunda 'Both the SSL trainer's fine-tuning gate and the training-export eligibility gate derive from FINETUNE_ALLOWED_CALIBRATIONS, so the K-3 fine-tuning policy lives in exactly one place' diyor. Ama `AnalysisJob.is_fine_tuning_eligible()` politikayı KENDİ İÇİNDE sabit kodluyor ve `ABSOLUTE`'u listeye almıyor. İki yer aynı soruya farklı cevap veriyor: allowlist ABSOLUTE'a EVET, metot HAYIR.
- **kanıt:** $ sed -n '39,44p' src/core/domain/analysis_job.py
    def is_fine_tuning_eligible(self) -> bool:
        """KR-018/K-3: Only PANEL_ABSOLUTE and DLS2_RELATIVE for fine-tuning."""
        return self.calibration_type in (
            CalibrationLevel.PANEL_ABSOLUTE,
            CalibrationLevel.DLS2_RELATIVE,
        )                                    # ← ABSOLUTE YOK

$ sed -n '67,79p' src/core/domain/enums.py
# K-3 canonical calibration allowlists — SINGLE SOURCE OF TRUTH.
FINETUNE_ALLOWED_CALIBRATIONS = frozenset({
    CalibrationLevel.ABSOLUTE,           # ← VAR
    CalibrationLevel.PANEL_ABSOLUTE,
    CalibrationLevel.DLS2_RELATIVE,
})

$ grep -rn "is_fine_tuning_eligible" src/ tests/
s
- **neden önemli:** Bugün fiili etki yok (metot src'de çağrılmıyor; gerçek kapılar allowlist'ten türüyor). Ama E13 = ABSOLUTE + platformun normalize etmemesi (bkz. ilgili bulgu) birleşince worker'a artık `ABSOLUTE` ulaşacak. Bu metodu çağıran ilk kod, üretimin ana kalibrasyon sınıfını fine-tuning dışı sayacak ve hata sessiz olacak (model eğitim havuzu beklenmedik şekilde boşalır). 'Aynı iş için tek kaynak' ilkesi burada beyan ediliyor ama uygulanmıyor.
- **öneri:** `is_fine_tuning_eligible()` gövdesini `return self.calibration_type in FINETUNE_ALLOWED_CALIBRATIONS` yap (docstring de allowlist'e atıf versin). `tests/unit/test_calibration_gate.py`'ye ABSOLUTE vakası eklensin. Kalıcı koruma: politikayı sabit kodlayan başka bir yer kalmadığını doğrulayan bir test (CalibrationLevel üyelerini gezip allowlist ile metodu karşılaştıran parametrik test).

## 29. [ORTA] Şema açıklamaları E13 ve D8/S1 kararlarıyla çelişecek şekilde bayat kaldı — 'DJI Mavic 3M produces RELATIVE only' ve 'yoksa CALIBRATED→PANEL_ABSOLUTE varsayar (güvenlik-ağı)'
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/schemas/edge/calibrated_dataset_manifest.v1.schema.json:58 · schemas/edge/intake_manifest.v1.schema.json:224 ve :524
- **ne yanlış:** E13 kararının yazılacağı ALANIN açıklaması hâlâ 'DJI Mavic 3M produces RELATIVE only' diyor — yani kararın tam tersini normatif açıklama olarak taşıyor. Ayrıca intake_manifest'in iki formundaki açıklama, 2026-07-31'de `x-superseded-2026-07-31` ile açıkça KALDIRILAN fail-open kuralı hâlâ tarif ediyor: 'yoksa CALIBRATED→PANEL_ABSOLUTE varsayar (güvenlik-ağı)'. Sözleşme aynı konuda üç ayrı şey söylüyor (enum: FAIL-CLOSED · şema açıklaması: güvenlik-ağı · platform kodu: güvenlik-ağı).
- **kanıt:** $ grep -n "calibration_type" schemas/edge/calibrated_dataset_manifest.v1.schema.json
58: "description": "Calibration type. DJI Mavic 3M produces RELATIVE only. Subset of enums/calibration_type.enum.v1.json (post-calibration manifest: only ABSOLUTE/RELATIVE)."

$ grep -n "güvenlik-ağı" schemas/edge/intake_manifest.v1.schema.json
224: "...Platform ABSOLUTE'u worker PANEL_ABSOLUTE'una normalize eder; yoksa CALIBRATED→PANEL_ABSOLUTE varsayar (güvenlik-ağı)..."
524: (aynı metin, EdgeForm)

$ grep -n "x-superseded-2026-07-31" -A2 enums/calibration_type.enum.v1.json | head -3
"what": "Eski global 'eksikse PANEL_ABSOLUTE varsay' güvenlik-ağı kuralı KALDIRILDI."
- **neden önemli:** Şema `description` alanları tüketici geliştiricinin okuduğu ilk normatif metin ve `generate_types.sh` ile üretilen tiplere de yansıyor. Kaldırılmış bir güvenlik-ağı kuralını tarif eden açıklama, S1'in kökünü (fail-open) dört depoya yeniden dağıtıyor — nitekim platform kodu tam da o cümleyi uyguluyor. 'DJI Mavic 3M produces RELATIVE only' cümlesi ise E13'ün gerekçesini bizzat çürütüyor ve bu turda kimse fark etmedi.
- **öneri:** Üç açıklamayı da kararlarla hizala: (1) edge calibrated manifest açıklaması ya E13'e uysun ya da E13 yeniden açılsın (bkz. ilk bulgu — bu cümle aslında matrisle aynı şeyi söylüyor, yani kararın karşı kanıtı); (2) intake açıklamalarındaki 'güvenlik-ağı' cümlesi silinip `x-normalization.missing` FAIL-CLOSED politikasına atıf verilsin. Kapı: `enums/*.json` içindeki `x-superseded-*` bloklarında geçen kaldırılmış kural ifadelerinin hiçbir şema `description`'ında bulunmadığını doğrulayan metin testi.

## 30. [ORTA] KR-090 'Applies-to: platform' diyor ama 0.h ile eklenen madde 10 doğrudan EDGE M1 diskine yükümlülük getiriyor — yükümlülüğü uygulayacak taraf KR'yi kendi kapsamında görmüyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/ssot/kr_registry.md:708 (Kapsam/Applies-to) ↔ :729-741 (madde 10, raw_frames)
- **ne yanlış:** KR-090'ın 2. bölümü kapsamı tek kelimeyle 'platform' olarak ilan ediyor. 0.h kararıyla eklenen madde 10 ise ham karelerin 180 günlük süresinin 'hem M1'deki yerel edge diskinde hem merkezde' geçerli olduğunu, 'yalnız merkez için değil' diye vurgulayarak yazıyor. Yani edge deposuna normatif bir saklama yükümlülüğü kondu ama KR'nin kapsam beyanı güncellenmedi. Kapsam alanını okuyarak filtreleme yapan bir edge geliştiricisi/aracı bu maddeyi hiç görmez.
- **kanıt:** $ sed -n '706,710p' ssot/kr_registry.md
**2) Kapsam / Applies-to:** platform

$ sed -n '729,741p' ssot/kr_registry.md
10) **Seçilmiş ham kareler** (`raw_frames`; taşıyıcılar: edge + platform
    `calibrated_dataset_manifest.v1`). **Süre: 180 gün (en kısa kademe).**
    ... Kapsam notu: kareler **hem** M1'deki yerel edge diskinde **hem** merkezde
    bulunabilir — süre **her ikisi** için geçerlidir, yalnız merkez için değil.

$ grep -rn "KR-090" tarlaanaliz-edge/src tarlaanaliz-edge/docs 2>/dev/null | wc -l
0        # edge deposunda KR-090'a tek bir atıf bile yok
- **neden önemli:** 0.h kararının 'üç kategori sözleşmeye MUST olarak girdi' iddiası, uygulayıcısı olmayan bir MUST üretti. Ham kareler kararın kendi gerekçesiyle 'çiftçinin en yüksek çözünürlüklü ve en kolay yeniden kimliklendirilebilir verisi' ve komşu parseli görebiliyor (madde 12, üçüncü kişi verisi) — yani KVKK yüzeyi en yüksek kalem, kapsamı belirsiz KR'de duruyor.
- **öneri:** KR-090 madde 2'yi `platform, edge` olarak güncelle (ya da edge yükümlülüğünü KR-072 dataset yaşam döngüsüne taşıyıp KR-090'dan çapraz atıf ver). `tests/test_data_governance.py`'ye 'taşıyıcısı edge olan bir kategori varsa Applies-to edge içermeli' kontrolü eklensin — bugün taşıyıcı listesi zaten makine-okunur (`DATA_CATEGORIES`), kapsamla karşılaştırmak ucuz.

## 31. [ORTA] W11'in '5 üye' listesindeki safe_path.py:19 YANLIŞ POZİTİF — o satır kod değil, modül docstring'i içindeki örnek
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1985 (W11 satırı) → atıf: tarlaanaliz-worker/src/shared/safe_path.py:19
- **ne yanlış:** Plan W11'de 'Sınıf tarandı, 4 üye daha: src/shared/safe_path.py:19 · cold_storage_manager.py:263,293 · ssl_pretrain.py:2131' diyor ve 'Yapılacak: beşine de encoding="utf-8"' hükmünü veriyor. Ölçüm: safe_path.py:19 çalıştırılabilir kod DEĞİL — 1. satırda açılan ve 21. satırda kapanan modül docstring'inin içindeki kullanım örneği. O dosyada gerçek bir `open()` çağrısı yok. Diğer 3 atıf (263, 293, 2131) ve kök kusur (contract_validator.py:233) doğru. Yani gerçek üye sayısı 5 değil 4. İroni: aynı satır '98 ham eşleşmenin gerisi yanlış pozitif' diye filtreleme titizliğiyle övünüyor, ama filtreden bir yanlış pozitif geçmiş.
- **kanıt:** $ python -c "..." # numaralı okuma, worker/src/shared/safe_path.py
 1 | """
 2 | TarlaAnaliz Worker — Safe path resolution (T3.6).
...
14 | Usage in pipeline._load_model_registry / similar config loaders:
16 |     from src.shared.safe_path import resolve_within, REPO_ROOT
17 |     safe = resolve_within(self._config.model_registry_path,
18 |                           [REPO_ROOT / "config", REPO_ROOT / "data"])
19 |     with open(safe) as f:        ← DOCSTRING İÇİ ÖRNEK
20 |         ...
21 | """
22 |
23 | from __future__ import annotations

BAĞIMSIZ AST TARAMASI (scratchpad/scan_open.py — ast.parse ile, docstring'ler doğal olarak dışarıda;
rasterio/Image/fiona/gzip/... sahipleri ve 'b' modu el
- **neden önemli:** W11 açık (⬜) bir iş kalemi ve bir sonraki oturumun 'sıradaki mantıklı işler' listesinde ilk sırada. O oturum listeyi doğru kabul edip safe_path.py:19'a `encoding="utf-8"` eklemeye çalışacak — bir docstring'i düzenleyecek, ya da 'burada open yok' deyip listenin tamamına güvenini kaybedecek. Daha derini: W11'in tüm gerekçesi 'sınıfı tarayarak' üretilmiş olmasıydı; taramanın çıktısı doğrulanmadan yazılmışsa, sayının kendisi (5) kanıt değil. Kullanıcının 'kapıyı da doğrula / iddiadan önce ölç' disipliniyle doğrudan çelişiyor.
- **öneri:** Plan satır 1985'te listeyi 4 gerçek üyeye indir (contract_validator.py:233 · cold_storage_manager.py:263,293 · ssl_pretrain.py:2131) ve 'safe_path.py:19 docstring örneğiydi — yanlış pozitif olarak düşüldü' notunu bırak (silme, düşme kaydını bırak; aynı hata tekrar keşfedilmesin). W11 işi yapılırken grep yerine AST tabanlı bir kapı yaz (ast.Call + func adı 'open' + kwargs'ta 'encoding' yok + mod 'b' değil) — grep hem docstring'i hem yorumu sayıyor, bu kusur sınıfını doğru ölçemez.

## 32. [ORTA] D4-b gerekçesindeki test_vendored_parity.py:88 atfı yanlış — skip gerekçesi 105. satırda, ve yazıldığı günden beri öyle
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1746 (D4-b satırı) → atıf: tests/test_vendored_parity.py:88
- **ne yanlış:** D4-b kararının ölçüm gerekçesi şöyle yazılmış: '45 değil 47 (CI logu: 972 passed, 47 skipped, 2 xfailed; hepsi tek gerekçe — test_vendored_parity.py:88 "kardeş depo yok")'. Ölçüm: 88. satır `    ),` — parite çifti tablosundaki bir tuple kapanışı. Gerçek `pytest.skip(f"kardeş depo yok: {vendored_rel}")` çağrısı 105. satırda. Üstelik bu atıf sonradan kaymış değil: kararın yazıldığı commit'te (de9ea0f), C8 commit'inde (a8cf512) ve bugün — üçünde de 88. satır `    ),`, skip çağrısı 105. Yani atıf doğduğu anda yanlıştı.
- **kanıt:** $ grep -n 'kardeş depo yok' tests/test_vendored_parity.py
105:        pytest.skip(f"kardeş depo yok: {vendored_rel}")

$ python -c "..."  # 85-93 numaralı
85 |     (
86 |         "schemas/worker/calibration_metadata.v1.schema.json",
87 |         "tarlaanaliz-worker/interface/contracts/calibration_metadata.v1.schema.json",
88 |     ),                                   ← ATFEDİLEN SATIR
89 |     (

GEÇMİŞTE DE YANLIŞ (kayma değil):
$ for rev in de9ea0f a8cf512 HEAD; do git show $rev:tests/test_vendored_parity.py | sed -n '88p'; \
    git show $rev:tests/test_vendored_parity.py | grep -n 'kardeş depo yok'; done
de9ea0f line88:     ),        de9ea0f skip: 105:        pytest.skip(...)
a8cf512 lin
- **neden önemli:** D4-b bu turun kalıcı CI mimarisi kararı (parite kapısı hangi depoda koşacak, PAT kullanılacak mı) ve uygulaması E17/W10 olarak kardeş depolara devredildi. O işi yapacak oturum, skip mekanizmasını anlamak için verilen tek dosya:satır adresine gidip alakasız bir parantez bulacak. Daha önemlisi bu, 'her bulguya dosya:satır ekle' disiplininin denetlenmediğinin kanıtı: atıf hiç koşulmadan yazılmış. Bir atıf ölçülmeden yazılabiliyorsa, aynı satırdaki '47 skip' gibi CI-logu iddiaları da aynı özenle üretilmiş olabilir.
- **öneri:** Atfı `tests/test_vendored_parity.py:105` olarak düzelt. Sistemik çözüm: dosya:satır atıflarının bugün hâlâ iddia edilen şeyi gösterdiğini kontrol eden hafif bir kapı yaz — plan/handoff/CHANGELOG'daki `dosya.py:N` desenlerini toplayıp dosyanın var olduğunu ve N'nin satır sayısını aşmadığını doğrulamak bile bu sınıfın çoğunu yakalar; içerik eşlemesi için atıfların yanına kısa bir 'beklenen dize' konabilir (ör. `test_vendored_parity.py:105 "kardeş depo yok"`) ve kapı o dizeyi o satırda arar.

## 33. [ORTA] §14.7 kalem 4 hâlâ '⏳ push onay bekliyor' diyor — 14 retro-tag dahil 19 tag'in tamamı zaten origin'de
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1980 (kanıt sütunu sonu)
- **ne yanlış:** Plan §14.7 kalem 4 (SD8) ✅ işaretli ama kanıt sütunu '18 tag'in tamamı annotated · ⏳ **push onay bekliyor**' ile bitiyor. Bugün ölçüm: 19 yerel tag, 19 uzak tag, aralarında fark YOK — retro-tag'ler push edilmiş. Ayrıca '18 tag' sayısı da v7.3.0 eklendikten sonra 19 olmuş. Handoff (:31) ise doğru sayıyı ('19 tag') ve push'un tamamlandığını ima ediyor — yani iki kaynak çelişiyor ve İŞ LİSTESİ olarak ilan edilen kaynak (plan) bayat olan.
- **kanıt:** $ git tag | wc -l → 19
$ git ls-remote --tags origin | grep -v '\^{}' | wc -l → 19
$ comm -23 <(git tag | sort) <(git ls-remote --tags origin | grep -v '\^{}' | sed 's|.*refs/tags/||' | sort)
(BOŞ — push edilmemiş tek tag yok)

$ git ls-remote --tags origin | grep -v '\^{}' | sed 's|.*refs/tags/||' | sort | tr '\n' ' '
v2.0.0 v3.0.0 v4.0.0 v4.1.0 v4.1.1 v4.2.1 v4.3.0 v4.4.0 v5.0.0 v5.1.0 v6.0.0 v6.0.1 v6.1.0 v6.2.0 v7.0.0 v7.0.1 v7.1.0 v7.2.0 v7.3.0

ÇELİŞEN İKİ KAYNAK:
plan:1980   → '18 tag'in tamamı annotated · ⏳ **push onay bekliyor**'
handoff:31  → '| contract | `7.3.0` · tag `v7.3.0` · 19 tag | I-2 ✅ |'
- **neden önemli:** Planın kendi kuralı: 'bir kalem burada yoksa yapılmaz; yapılacaksa önce buraya yazılır' — yani plan İŞ LİSTESİNİN TEK KAYNAĞI. Orada duran '⏳ push onay bekliyor' bir sonraki oturum için AÇIK BİR EYLEM gibi okunur. Sonuç: ya kullanıcıya gereksiz bir onay sorusu sorulur, ya `git push origin --tags` gereksiz koşulur, ya da daha kötüsü 'retro-tag'ler henüz uzakta yok' varsayımıyla tüketici pin/`git describe` davranışı hakkında yanlış çıkarım yapılır. Kullanıcının 'aynı iş için tek dosya' kuralı da burada zedeleniyor: durum handoff'ta doğru, iş listesinde yanlış.
- **öneri:** Plan :1980'in kanıt sütununda '⏳ push onay bekliyor'u '✅ push edildi (19/19 tag origin'de, `git ls-remote --tags origin` ile doğrulandı)' ile değiştir; '18 tag' ifadesini '(o an 18; v7.3.0 ile 19)' diye zamanla işaretle ya da sabit sayı yerine üreteç komutunu yaz. Genel olarak: bu tabloda '⏳' taşıyan her hücre için oturum kapanışında tek bir tarama yap — ✅ işaretli bir kalemin kanıt hücresinde bekleyen eylem kalmamalı, kalıyorsa kalem ✅ değil ⚠️ olmalı.

## 34. [ORTA] Edge CONTRACTS_VERSION.md başlığı 1.4.0/7.3.0 diyor ama aynı dosyanın açıklama metni hâlâ 1.3.0 ve 7.2.0'a atıf yapıyor
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-edge/CONTRACTS_VERSION.md:15 ve :20 (bayat) ↔ :3, :5, :11 (güncel)
- **ne yanlış:** C8 yayılımında edge 1.3.0→1.4.0'a çıktı ve upstream ref 7.3.0 oldu; başlık alanları doğru güncellenmiş (:3 CONTRACTS_VERSION=1.4.0, :5 **Version:** 1.4.0, :11 Upstream `7.3.0`). Ama hemen altındaki açıklama bloğu güncellenmemiş: :15 'kendi yerel sürüm pini (**yukarıdaki `1.3.0`**)' — yukarıda 1.4.0 yazıyor; :20 'bu 8 edge şemasının **SSOT contracts `7.2.0`** tarafından valide edildiğini gösterir' — upstream artık 7.3.0. Handoff (:34) bu dosya için 'hash bloğu yeniden üretildi' diyerek dosyanın tazelendiği izlenimi veriyor.
- **kanıt:** $ grep -n 'yukarıdaki `1.3.0`\|SSOT contracts `7.2.0` tarafından valide' tarlaanaliz-edge/CONTRACTS_VERSION.md
15:> Bu repo, edge-lokal şema setini kendi yerel sürüm pini (yukarıdaki `1.3.0`) + LF-normalize
20:> edge şemasının SSOT contracts `7.2.0` tarafından valide edildiğini gösterir. **Bu 8 edge

$ head -12 tarlaanaliz-edge/CONTRACTS_VERSION.md | grep -n '1\.4\.0\|7\.3\.0'
3:CONTRACTS_VERSION=1.4.0
5:**Version:** 1.4.0
11:| **Upstream Contract Set (SSOT)** | `7.3.0` (...)

(Kapı yeşil ve doğru — sorun yalnız metinde:)
$ cd tarlaanaliz-edge && python scripts/verify_contracts_hashes.py
OK: all 8 contract schema hashes match the pin.
- **neden önemli:** Bu dosya edge'in PİN BELGESİ — 'hangi upstream sürüme karşı doğrulandık' sorusunun kanonik cevabı burada. Açıklama metni 7.2.0 dediği sürece, edge tarafında çalışan biri (ya da bir sonraki denetim) 'edge hâlâ 7.2.0'a mı pinli?' diye yanlış sonuca varabilir ve gereksiz bir re-pin turu açar — bu, handoff'un §1'de 'iki sürüm bayat kaldı, sonraki oturumu ZATEN YAPILMIŞ bir re-pin turuna yollayacaktı' diye kayda geçirdiği hatanın aynısı. Makine kapısı (verify_contracts_hashes.py) yeşil olduğu için hata sessiz: kapı baytları ölçüyor, prose'u ölçmüyor.
- **öneri:** :15'teki `1.3.0`'ı `1.4.0`, :20'deki `7.2.0`'ı `7.3.0` yap. Kalıcı çözüm: bu iki cümledeki sürümü sabit yazmak yerine 'yukarıdaki Version satırı' / 'yukarıdaki Upstream Contract Set satırı' diye ATIFLA anlat (sayı tek yerde kalsın — D16'nın 'tek gövde' deseninin sürüm dizesi hâli). Zorlayıcı kapı: edge CI'ına 'dosya içinde `**Version:**` satırındakinden farklı bir edge SemVer dizesi geçmesin' yüklemi ekle ve mutasyonla doğrula.

## 35. [ORTA] Üç edge vendored şeması AK-4 sapmalarını görünmez taşıyor — kanonik `oneOf/$defs` kullanırken vendored düz `properties` kullanıyor, kapı ikisini de göremiyor
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-edge/interface/contracts/schemas/edge/intake_manifest.v1.schema.json · scan_report.v1.schema.json · transfer_batch.v1.schema.json (üçü de PARITY_PAIRS dışında) · kanonik karşılıkları: tarlaanaliz-contract/schemas/edge/{intake_manifest,scan_report,transfer_batch}.v1.schema.json
- **ne yanlış:** Bu üç kanonik şema `oneOf` + `$defs` (iki-form) biçimine geçmiş: üst düzey `properties` BOŞ. Vendored kopyalar hâlâ düz tek-form `properties` taşıyor. Sonuç: yapısal olarak iki taraf artık aynı şekli anlatmıyor ve kapı bunu ne yakalayabiliyor (listede değiller) ne de listeye eklenince doğru ölçebilir (üst-düzey karşılaştırma, vendored'ın 11-22 alanının HEPSİNİ "AK-4 sapması" sanıp yanlış kırmızı verir). Yani sınıf 5'in düzeltmesi (PARITY_PAIRS'e eksik dosyaları eklemek) sınıf 3'ün/`$defs` körlüğünün düzeltmesi olmadan YAPILAMAZ — iki iş birbirine bağlı.
- **kanıt:** ```
intake_manifest.v1.schema.json
   vendored-ONLY props (AK-4 SAPMASI): ['av_scan_result','available_bands','batch_id','calibration_type','card_id','correlation_id','created_at','drone_make','drone_model','drone_serial','field_id','files','kiosk_id','mission_date','mission_id','operator_id','priority_zones','quarantined_bytes','quarantined_file_count','schema_version','signature','sorties']
scan_report.v1.schema.json
   vendored-ONLY props: ['correlation_id','dataset_id','report_id','result','scan_mode','scan_type','scanned_at','scanner_version','schema_version','signature_db_version','threats']
transfer_batch.v1.schema.json
   vendored-ONLY props: ['batch_id','chunk_size_bytes','chunks','
- **neden önemli:** Edge'in en güvenlik-kritik üç belgesi (AV tarama raporu, intake manifesti, transfer partisi — KR-072/KR-073 kanıt zinciri) parite denetiminin tamamen dışında. Bir alan edge tarafında eklenip kanoniğe hiç dönmezse (AK-4 sapması, I-5'e göre kalıcı olamaz) bunu bugün hiçbir kapı söylemiyor. Ayrıca bu, "kapıyı listeye üye ekleyerek kapatırım" kestirmesinin neden çalışmayacağının kanıtı.
- **öneri:** Sıralı yap: önce parite karşılaştırmasını `oneOf`/`$defs` farkındalıklı hâle getir (bir üstteki bulgunun (1) maddesi — kanonik tarafta tüm `oneOf` dallarının alan kümesi BİRLEŞİMİ alınmalı), sonra bu üç çifti PARITY_PAIRS'e ekle. Eklemeden önce her birini tek tek koştur: vendored alanların birleşim kümesinin ALT KÜMESİ olduğunu doğrula; olmayan varsa gerçek AK-4 sapmasıdır ve kanonik absorbe etmelidir.

## 36. [ORTA] SINIF 2, düzeltilen dosyanın KENDİ İÇİNDE kapanmamış — edge CONTRACTS_VERSION.md'nin makine satırı 1.4.0 derken prose'u hâlâ 1.3.0 diyor
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-edge/CONTRACTS_VERSION.md:3 (`CONTRACTS_VERSION=1.4.0`) ↔ :15 (`> Bu repo, edge-lokal şema setini kendi yerel sürüm pini (yukarıdaki \`1.3.0\`) + LF-normalize`)
- **ne yanlış:** C8'de aynı dosyanın CI kapısındaki hardcode sürüm (`grep -q "CONTRACTS_VERSION=1.3.0"`) generik hâle getirildi — doğru düzeltme. Ama "aynı bilgi iki yerde" kusuru bu dosyanın kendi metninde de vardı ve taranmadı: satır 15, satır 3'e "yukarıdaki" diye ATIF YAPARAK 1.3.0 diyor. Bump 1.3.0→1.4.0 yapıldı, makine satırı güncellendi, kendine atıf yapan prose güncellenmedi. Bu, düzeltilen sınıfın (bump'ta bayatlayan hardcode sürüm) tam olarak aynı örneği, aynı dosyada.
- **kanıt:** ```
$ head -5 tarlaanaliz-edge/CONTRACTS_VERSION.md
# Contracts Version Pin

CONTRACTS_VERSION=1.4.0

**Version:** 1.4.0

$ grep -n '1\.3\.0' tarlaanaliz-edge/CONTRACTS_VERSION.md
15:> Bu repo, edge-lokal şema setini kendi yerel sürüm pini (yukarıdaki `1.3.0`) + LF-normalize
```
Satır 11 ve 48-62'deki 1.3.0 geçişleri TARİHSEL kayıt ("1.2.0→1.3.0 bump'ı") — doğru. Yalnız satır 15 GÜNCEL duruma atıf yapıp yanlış değer veriyor.
Düzeltilen CI kapısının kendisi temiz (yorum satır 97-100 kusuru açıkça anlatıyor) ve mutasyonla doğrulandı (bkz. doğrulanan iddialar).
- **neden önemli:** Küçük görünüyor ama bu dosya edge'in sürüm SSOT'u ve bir sonraki denetçi/geliştirici için "hangi sürümdeyiz" sorusunun cevabı. İki satır çelişiyor ve çelişen satır "yukarıdaki" diyerek okuyucuyu yanlış yönlendiriyor. Sınıf tarama disiplini açısından asıl mesele: kusur sınıfı "CI'da hardcode sürüm" değil, **"bump'ta bayatlayan elle yazılmış sürüm dizesi"**; sınıf dar tanımlandığı için aynı dosyadaki ikinci üye kaçtı.
- **öneri:** (1) Satır 15'teki `(yukarıdaki \`1.3.0\`)` ifadesini sürümsüz hâle getir: `(yukarıdaki \`CONTRACTS_VERSION\` satırı)`. (2) Sınıfı doğru tanımla ve kapıyı ona göre kur: edge `contracts_gate.yml`'a ikinci bir adım ekle — dosyada `CONTRACTS_VERSION=` satırı DIŞINDA, güncel sürümden farklı bir SemVer'e "yukarıdaki/geçerli/current" gibi bir işaretle atıf yapılmadığını doğrula; ya da daha basiti: prose'da mevcut sürümü tekrarlamayı tümüyle yasakla.

## 37. [ORTA] I-2 edge'de delik: CONTRACTS_VERSION 1.4.0'a bump edildi ama annotated `v1.4.0` etiketi yok — retro-tag turu (SD8) yalnız contract deposunda koşturuldu
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-edge — `git tag --list` → yalnız `v1.3.0` · bump commit'i 16e7158 (`feat(contracts): C8 v7.3.0 yayılımı — raw_frames vendor'landı (edge 1.3.0→1.4.0)`), merge 1acf6bc
- **ne yanlış:** SD8 kararı "14 retro-tag + 2.0.2 istisnası" ile contract deposundaki her sürüme annotated tag koydu (19/19 doğrulandı). Aynı sınıf edge'de taranmadı: edge 1.3.0 için annotated bir tag VAR (`v1.3.0 - 2026-05-29 ... retroaktif etiket` — yani norm zaten kurulmuş), ama bu oturumda yapılan 1.3.0→1.4.0 bump'ı etiketlenmedi. Kural I-2 "her sürüm annotated tag" diyor; bump'ın kendisi edge'in şema baytlarını değiştirdi (vendored `raw_frames`) ve hash bloğu yeniden üretildi — yani gerçek bir yayın olayı.
- **kanıt:** ```
$ cd tarlaanaliz-edge && git tag --list
v1.3.0
$ git tag -n20 v1.3.0
v1.3.0    v1.3.0 - 2026-05-29 (5-perspektif denetim duzeltmeleri; retroaktif etiket)
$ head -5 CONTRACTS_VERSION.md
CONTRACTS_VERSION=1.4.0
$ git log --oneline -S"CONTRACTS_VERSION=1.3.0" -- CONTRACTS_VERSION.md | head -1
16e7158 feat(contracts): C8 v7.3.0 yayılımı — raw_frames vendor'landı (edge 1.3.0→1.4.0)
```
Karşılaştırma: contract deposunda 19 sürüm → 19 annotated tag (hepsi `git cat-file -t` = `tag`).
- **neden önemli:** Etiketsiz sürüm geri alınamaz/karşılaştırılamaz: kioska hangi şema setinin gittiğini bir commit SHA'sıyla değil sürümle anmak gerekiyor (M1 dağıtımı fiziksel bir kutu). Sınıf açısından: SD8 turu "her sürüm annotated tag" kuralını contract'ta uyguladı ama dört depoya taşımadı — "dört depo tek standart" ihlali ve tam olarak LENS 5 deseni.
- **öneri:** (1) Edge'de `1acf6bc` üzerine annotated `v1.4.0` etiketi at (mesajda SSOT 7.3.0 ↔ edge 1.4.0 eşlemesi ve `raw_frames` gerekçesi yazılı olsun). (2) Sınıfı kapat: dört deponun sürüm dosyasını bump eden her PR için "annotated tag var mı" kapısı — edge/worker `contracts_gate.yml`'a `git describe --exact-match --tags` tabanlı bir release-gate adımı, ya da en azından `SDLC_GATES.md` C8 törenine dört-depo tag kontrol kalemi.

## 38. [ORTA] S5 kapısı "dört depo tek standart" diyor ama vendored kopyayı hiç okumuyor; S6'nın yeni sözlük taşıyıcısı da kapsam dışı
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_reflectance_scale_contract.py:72-94 (test_enum_matches_platform_exactly / test_manifest_uses_the_same_vocabulary) — okuduğu üç dosya: schemas/platform/calibration_result.v1, schemas/worker/calibration_metadata.v1, schemas/platform/calibrated_dataset_manifest.v1 (hepsi kanonik)
- **ne yanlış:** İki ayrı daralma var. (a) Kapının assert mesajı doğrudan kullanıcının kalıcı direktifini alıntılıyor ("dört depo tek standart, yeni ad icat edilmez") ama ölçtüğü yüzey iki kanonik dosya; worker'ın fiilen doğrulama yaptığı `tarlaanaliz-worker/interface/contracts/calibration_metadata.v1.schema.json` hiç açılmıyor (ve bulgu 5'te gösterildiği gibi parite kapısı da onun içine bakmıyor) → sözlük ayrışması hiçbir yerde ölçülmüyor. (b) Aynı PR'da S6 ile eklenen ÜÇÜNCÜ taşıyıcı `platform/calibrated_dataset_manifest.$defs.file_artifact.properties.reflectance_scale` kapının okuduğu yol değil; test yalnız `properties.reflectance_scale` (paket düzeyi) bakıyor.
- **kanıt:** MUTASYON: platform/calibrated_dataset_manifest → $defs.file_artifact.properties.reflectance_scale.enum = ['reflectance_0_1','DN_RAW','percent','byte_0_255'] (uydurma sözlük), ardından `python tools/inline_refs.py --write`
$ pytest tests/ -q --no-cov → 1046 passed, 2 skipped, 2 xfailed   ← yeşil
(dist yeniden üretilmeden koşulduğunda yalnız test_inline_refs stale-dist testi kırmızı oluyordu — yani sözlük uydurmasını değil, dist bayatlığını yakalıyordu.)

Mevcut yollar (ölçüm):
 platform/calibrated_dataset_manifest → /properties/reflectance_scale  ✔ kapıda
 platform/calibrated_dataset_manifest → /$defs/file_artifact/properties/reflectance_scale  ✘ kapıda YOK
 platform/calibration_result → /pro
- **neden önemli:** S5'in tüm gerekçesi "sözlük ayrışırsa tüketici kendi sözlüğünü uydurur (AK-7'de tam bu yaşandı)". Kapı bu ayrışmayı, ayrışmanın gerçekleşeceği iki yerde (vendored kopya ve S6'nın çıktı-düzeyi alanı) ölçmüyor. Ölçeğe duyarlı EVI/SAVI sessizce bozulur ve NDVI'nin doğru görünmesi hatayı maskeler — dosyanın kendi anlattığı arıza sınıfı.
- **öneri:** `reflectance_scale` adlı HER düğümü şemalar ağacında özyinelemeli toplayan bir yardımcı yazıp (bugün 4 taşıyıcı) hepsinin `enum`'unu tek kanonik listeyle eşitleyin; kardeş depo mevcutsa vendored kopyayı da aynı listeye dahil edin (yoksa beyanlı skip). Böylece yeni bir taşıyıcı eklendiğinde kapı otomatik olarak onu da kapsar — bugünkü sabit üç yol listesi her yeni alanla bir daha kör noktaya dönüşüyor.

## 39. [ORTA] release_gate koruması yalnız `-m` bayrağını görüyor; `--deselect`, `-k` ve `--ignore` sessizce geçiyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/conftest.py:57-67 (pytest_configure) — yalnız `config.option.markexpr` içinde "release_gate" + "not" arıyor
- **ne yanlış:** Kural "release_gate testleri deselect EDİLEMEZ" diye ilan ediliyor (docstring satır 17-19) ama sadece tek bir sözdizimi kapatılmış. Aynı sonucu veren en az üç yol açık: `--deselect <nodeid>`, `-k "not <isim>"`, `--ignore=<dosya>`. Üçünde de koşum tam yeşil (rc=0) döner ve hiçbir uyarı basılmaz.
- **kanıt:** $ python -m pytest tests/ -q --no-cov -m "not release_gate" >/dev/null 2>&1; echo $?     → 4   (ENGELLENDİ ✔)
$ python -m pytest tests/ -q --no-cov --deselect tests/test_vendored_parity.py::test_pending_propagation_is_empty >/dev/null 2>&1; echo $?  → 0  (GEÇTİ ✘)
$ python -m pytest tests/ -q --no-cov -k "not pending_propagation" >/dev/null 2>&1; echo $?  → 0  (GEÇTİ ✘)
$ python -m pytest tests/ -q --no-cov --ignore=tests/test_vendored_parity.py >/dev/null 2>&1; echo $?  → 0  (GEÇTİ ✘, 56 test sessizce düştü: 990 passed vs 1046)
- **neden önemli:** Kapının amacı "tur içi beklenen kırmızıyı çözmek yerine saklamayı" engellemekti. Saklamanın en kolay üç yolu açık kaldığı sürece koruma, kuralı bilen kişiye karşı değil yalnızca bir bayrağa karşı çalışıyor. C8 töreninde acele edilen bir koşumda `-k` ile filtrelemek fazlasıyla doğal bir refleks.
- **öneri:** `pytest_collection_modifyitems` içinde toplanan `release_gate` işaretli test sayısını ölçün ve beklenen sayının (bugün 2) altına düşerse `pytest.UsageError` fırlatın — bu, deselect yolunu da `-k` yolunu da `--ignore` yolunu da tek noktadan kapatır. Beklenen sayı sabit yerine "süitte tanımlı release_gate testi sayısı" olarak koleksiyondan türetilebilir (`--ignore` durumunda dosya hiç toplanmayacağı için ayrıca dosya varlığı kontrolü gerekir).

## 40. [ORTA] ALLOWED_SKIP_REASONS alt-dize eşleşmesi: C11/AK-4 absorpsiyon kapısının atlanması, başka bir süit için yazılmış beyanın altına gizleniyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/conftest.py:31-41 (tek beyan girdisi: "kardeş depo yok", gerekçesi açıkça tests/test_vendored_parity.py hakkında) + tests/conftest.py:53-54 (_is_declared → `pattern in reason`) · atlanan yer: tests/test_c11_sorties_absorption.py:161
- **ne yanlış:** Beyan mekanizması "her giriş bir taahhüttür: bu atlama biliniyor, gerekçesi şu ve NEREDE KOŞTUĞU BELLİ" diyor. Ama eşleşme serbest alt-dize olduğu için, tamamen başka bir dosyadaki tamamen başka bir atlama (edge fixture dosyasının yokluğu) aynı cümleyi kullandığı anda beyanlı sayılıyor. O atlamanın "nerede koştuğu" hiçbir yerde yazılı değil — D4-b kararı yalnız parite süitini kapsıyor, C11'i değil.
- **kanıt:** $ pytest tests/ -q --no-cov   (kardeş depo fixture'ı olmayan ortamda)
SKIP BÜTÇESİ: 2 test atlandı
  [beyanlı] 2x Skipped: kardeş depo yok: intake_manifest_valid.json
SKIPPED [2] tests/test_c11_sorties_absorption.py:161
→ tests/test_c11_sorties_absorption.py:160-161: `if not EDGE_FIXTURE.exists(): pytest.skip(f"kardeş depo yok: {EDGE_FIXTURE.name}")`
→ tests/conftest.py:32-40 beyan metni yalnız test_vendored_parity.py'den bahsediyor.
Ayrıca CI özet adımı (contract_validation.yml) `grep -qE "^  \[beyanlı\].*kardeş depo yok"` görünce SADECE "Vendored parite kapısı ÇALIŞMADI" uyarısını basıyor — C11'in atlandığı hiç söylenmiyor.
- **neden önemli:** test_c11_sorties_absorption'ın `TestEdgeRealOutputAgainstCanonical` sınıfı, C11 absorpsiyonunun ASIL ölçüsü: edge'in gerçek çıktısının kanoniğe uyup uymadığı. Bu bilinen AK-4 sapmasının (sorties/mission_date) kapandığını gösteren tek delil. Contract CI'ında koşmuyor, kardeş CI'da da koşmuyor (bulgu 6), ve CI özeti bunu ismen bile anmıyor — yani ölçülmediği görünmüyor bile.
- **öneri:** ALLOWED_SKIP_REASONS girdilerini (desen, hangi test dosyası, gerekçe) üçlüsüne çevirin ve `_is_declared` eşleşmeyi rapor edilen test dosyasıyla birlikte yapsın (`report.nodeid` üzerinden). Böylece bir suite'in beyanı başka bir suite'i örtemez. C11 için ayrı bir beyan girdisi + CI özetinde ayrı bir uyarı satırı yazılsın.

## 41. [ORTA] Parite kapsamı 16 vendored dosyanın 9'u; I-4 ("vendored = kanoniğin dar alt kümesi") worker'ın çekirdek iş sözleşmeleri için hiçbir yerde ölçülmüyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_vendored_parity.py:60-97 (PARITY_PAIRS, elle tutulan 9 çift) · kapsam dışı kalan gerçek vendored dosyalar: worker/analysis_job.v1, worker/analysis_result.v1, worker/analysis_type.enum.v1, worker/expert_labeling_card.v1, edge/scan_report.v1, edge/transfer_batch.v1 (+ beyanlı istisna edge/intake_manifest.v1)
- **ne yanlış:** Docstring yalnız `intake_manifest`'in dışarıda olduğunu ve nedenini yazıyor (satır 42-46). Ölçüldü: dışarıda kalan 7 dosya var ve altısı için hiçbir gerekçe yazılı değil. Üyelik ölçütü de "açıklamasında parite iddiası taşıyan şema" — yani bir şemanın açıklama cümlesini değiştirmek onu kapıdan sessizce çıkarır; kapı üyelik sapmasını (yeni vendor'lanan dosyanın listeye eklenmemesini) hiç ölçmüyor.
- **kanıt:** $ ls tarlaanaliz-edge/interface/contracts/schemas/edge/ | wc -l → 8
$ ls tarlaanaliz-worker/interface/contracts/*.json | wc -l → 8   (toplam 16 vendored dosya; PARITY_PAIRS = 9)
$ python -c "izlenmeyen çiftleri karşılaştır"
 analysis_job.v1     yalniz-kanonik=[19 alan] yalniz-vendored=[] required-fark=['calibration_metadata','image_urls','job_id']
 analysis_result.v1  yalniz-kanonik=[8 alan]  yalniz-vendored=[] required-fark=['confidence_score','result_mode']
 scan_report.v1      kanonik `oneOf` iki-form / vendored düz (flat) → yapısal olarak farklı, hiçbir kapıda değil
 transfer_batch.v1   aynı desen
 expert_labeling_card.v1  properties + required BİREBİR (izlenmese de bugün uyumlu)
- **neden önemli:** I-4 değişmezi ("worker vendored = kanoniğin DAR alt kümesi, kalıcı divergence YASAK") bu altı dosya için hiçbir yerde ölçülmüyor: contract tarafında kapsam dışı, worker tarafında `compute_contracts_hash.py --verify` yalnız dosyanın kendi bütünlüğüne bakıyor. `analysis_job.v1` ve `analysis_result.v1` iş hattının çekirdek sözleşmeleridir; `required` farkları bugün bilinçli (worker daha katı) olabilir ama bu hiçbir yerde BEYAN edilmiş değil — I-5'in ("sapma yalnız GEÇİCİ ve beyanlı") ihlali.
- **öneri:** PARITY_PAIRS'e üyelik kapısı ekleyin: kardeş depodaki her vendored dosya için ya bir çift ya da gerekçeli bir `UNTRACKED_WITH_REASON` girdisi bulunmalı; ikisi de yoksa kırmızı. `analysis_job`/`analysis_result` için asimetrik kapı (kanonik superset, vendored dar alt küme + vendored'ın ekstra `required`'ları beyanlı) yazılsın — bu tam olarak I-4'ün ölçülebilir hâli.

## 42. [ORTA] Denetim testi ölçtüğü sistemi DEĞİŞTİRİYOR: test_inline_refs koşum sırasında kanonik enum dosyasına yazıyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** tests/test_inline_refs.py:143-172 (test_generator_detects_a_changed_enum) — enums/drone_type.enum.v1.json dosyasını `write_text` ile bozup `finally` bloğunda geri yazıyor
- **ne yanlış:** KADEME 3'ün (D12–D15) tüm ilkesi "denetim satırı artık ölçtüğü sistemi değiştiremiyor" idi ve commit başlığı bunu böyle yazıyor (14afd25). Aynı ilkeyi ihlal eden şey testin kendisi: mutasyon kanıtı için KANONİK kaynak dosyaya gerçek bir yazma yapılıyor. Koşum kesilirse (Ctrl-C, timeout, OOM, `pytest-xdist` ile paralel koşum, ya da aynı anda koşan ikinci bir süit) `enums/drone_type.enum.v1.json` DJI_MAVIC_3M'siz kalır ve bu sessizce commit edilebilir.
- **kanıt:** tests/test_inline_refs.py:159-172:
  enum_path = ROOT / "enums" / "drone_type.enum.v1.json"
  backup = enum_path.read_text(...)
  try: ... enum_path.write_text(json.dumps(doc,...))   ← KANONİK DEPO DOSYASINA YAZMA
  finally: enum_path.write_text(backup, ...)
Karşılaştırma: aynı süitte test_kr_corpus_sync.py:72-91 aynı tür mutasyonu `tmp_path` + `monkeypatch.setattr(_sync, "ROOT", contract)` ile GEÇİCİ dizinde kuruyor — doğru desen zaten depoda mevcut ve kullanılmış.
pyproject.toml'da pytest-xdist bağımlılık olarak tanımlı (paralel koşum mümkün).
- **neden önemli:** Kapı doğru şeyi ölçüyor (üreticinin kanonik kaynağa bağlı olduğunu), ama bunu yaparken deponun tek kanonik drone sözlüğünü riske atıyor. Bir kapının yan etkisi, koruduğu varlığı bozabiliyorsa kapı güvenilir bir ölçüm aracı değildir — "kapıyı da doğrula" ilkesinin kendi süitine uygulanmamış hâli.
- **öneri:** test_kr_corpus_sync.py'deki deseni kullanın: `tmp_path` altına minimal bir schemas/+enums/ ağacı kurup `monkeypatch.setattr(_inline, "ROOT", tmp_root)` ile üreteci oraya yönlendirin. Kanonik depo dosyalarına hiçbir test yazmasın; gerekirse ayrı bir kapı ekleyin: "tests/ altında ROOT altındaki bir yola write_text/write_bytes çağrısı yasaktır" (basit AST taraması).

## 43. [DUSUK] Edge CONTRACTS_VERSION.md prose'u kendi başlığıyla ve upstream pinle çelişiyor (1.3.0 / 7.2.0)
- **lens:** LENS 4 — Çapraz-repo bütünlüğü (I-1..I-5 + yayılım), v7.3.0 
- **nerede:** tarlaanaliz-edge/CONTRACTS_VERSION.md:15 ve :20
- **ne yanlış:** Dosya başlığı 1.4.0 / upstream 7.3.0 olarak güncellenmiş ama açıklayıcı paragraf eski değerlerde kalmış. Satır 15: "kendi yerel sürüm pini (yukarıdaki `1.3.0`)" — yukarıdaki değer artık 1.4.0. Satır 20: "bu 8 edge şemasının SSOT contracts `7.2.0` tarafından valide edildiğini gösterir" — upstream artık 7.3.0. "Yukarıdaki" diye kendine atıf yapan bir cümlenin gösterdiği değer yanlış.
- **kanıt:** `grep -n "1\.3\.0|1\.4\.0" CONTRACTS_VERSION.md` → 3: "CONTRACTS_VERSION=1.4.0" · 5: "**Version:** 1.4.0" · 15: "kendi yerel sürüm pini (yukarıdaki `1.3.0`) + LF-normalize" · `grep -n "valide edildi"` → 20: "edge şemasının SSOT contracts `7.2.0` tarafından valide edildiğini gösterir"
- **neden önemli:** Bu dosya edge'in tüketicilere karşı tek sürüm beyanı; içindeki iki değer birbirini tutmayınca hangi satırın otoriter olduğu belirsizleşir. Aynı dosyada a5b76ba ile "kapı sayıyı değil BİÇİMİ zorlasın" düzeltmesi yapılmış — biçim kapısı bu iki prose atfını göremiyor, yani düzeltilen kapının açık kalan kenarı.
- **öneri:** Satır 15'te sabit sayıyı sil, atıfla yaz: "kendi yerel sürüm pini (yukarıdaki `CONTRACTS_VERSION` satırı)". Satır 20'de `7.2.0`→`7.3.0` yap veya aynı şekilde "yukarıdaki Upstream Contract Set değeri" diye atfa çevir. Genel kural: bu dosyada sürüm sayısı yalnız 3. ve 11. satırlarda geçsin, prose hep onlara atıf yapsın — böylece bir sonraki bump'ta bayatlayacak metin kalmaz.

## 44. [DUSUK] test_data_governance.py süre TUTARLILIĞINI korumuyor — 'analiz sonucuyla AYNI (730 gün)' cümlesi madde 1'den koparıldığında kapı yeşil kalıyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-contract/tests/test_data_governance.py:187 (`test_retention_row_states_duration_and_rationale`) · ssot/kr_registry.md:711 (madde 1) ↔ :722-727 (madde 9)
- **ne yanlış:** Kapı bir sürenin YAZILMIŞ ve makul biçimde olduğunu zorluyor (boş bırakılırsa ve saçma değer verilirse kırmızı — ölçüldü). Ama beyan edilen İLİŞKİYİ ('analiz sonucuyla AYNI') doğrulamıyor: madde 9'daki 730'u 365 yapmak da, madde 1'deki 730'u 1095 yapmak da testi geçiyor. Yani 'AYNI' iddiası kapıyla korunmuyor; iki sayı sessizce ayrışabilir.
- **kanıt:** scratchpad klonunda iki mutasyon:
$ # MUT-A: madde 9 '(730 gün)' → '(365 gün)'
$ PYTHONIOENCODING=utf-8 python -m pytest tests/test_data_governance.py -q --no-cov
11 passed        ← YEŞİL
$ # MUT-B: madde 1 'analysis_results: 730 gün' → 'analysis_results: 1095 gün'
$ PYTHONIOENCODING=utf-8 python -m pytest tests/test_data_governance.py -q --no-cov
11 passed        ← YEŞİL
(karşılaştırma: MUT-1 süreyi tamamen silmek → 1 failed; MUT-2 99999 gün → 2 failed. Kapı biçimi görüyor, tutarlılığı görmüyor.)
- **neden önemli:** 0.h kararının madde 9 gerekçesi tam olarak bu ilişkiye dayanıyor: 'bunlar analiz çıktısının bir görünümüdür... ayrı bir saklama ömrü vermek, silinmiş bir analizin konumsal izini geride bırakırdı.' İlişki koparsa gerekçe çöker ama kapı haber vermez — silinmiş bir analizin öncelik-bölgesi poligonu (konum verisi) geride kalabilir. Kararın kendisi doğru, koruması eksik.
- **öneri:** Teste tek bir assert ekle: madde 9'un süresi madde 1'deki `analysis_results` süresinden ÇIKARILSIN (metinden sayıyı üret, elle yazma — 'sayıyı değil üreteci yayınla'), ve eşit olmadığında kırmızıya dön. Aynı desen madde 11'in '730 günde budanır' ifadesi için de geçerli.

## 45. [DUSUK] Platform `_DRONE_CALIBRATION_CLASS` anahtarları kanonik `drone_type.enum.v1` adlarıyla uyuşmuyor — 5 dronedan 3'ü haritada bulunamayıp varsayılana düşüyor
- **lens:** LENS 1 — KARAR DOĞRULUĞU (2026-08-01 oturumu: E13 · SD8 · D4
- **nerede:** tarlaanaliz-platform/src/core/domain/value_objects/calibration_class.py:41-47 ↔ tarlaanaliz-contract/enums/drone_type.enum.v1.json
- **ne yanlış:** Harita anahtarları `WINGTRAONE_GEN2`, `PARROT_SEQUOIA_PLUS`, `AGEAGLE_EBEE_X`; kanonik enum değerleri ise `WINGTRAONE_GEN2_MICASENSE_REDEDGE_P`, `PARROT_ANAFI_USA_SEQUOIA_PLUS`, `AGEAGLE_EBEE_X_ALTUM_PT`. Kanonik ad geldiğinde `.get()` ıskalıyor ve `ABSOLUTE` varsayılanına düşüyor. Bugün davranışsal hata yok (üçü de zaten `absolute`), ama harita kanonik sözlükten kopmuş ve sessizce yanlış çalışıyor.
- **kanıt:** $ python -c "import json;print(json.load(open('enums/drone_type.enum.v1.json',encoding='utf-8'))['enum'])"
['DJI_MAVIC_3M', 'DJI_M350_RTK_SENTERA_6X', 'WINGTRAONE_GEN2_MICASENSE_REDEDGE_P', 'PARROT_ANAFI_USA_SEQUOIA_PLUS', 'AGEAGLE_EBEE_X_ALTUM_PT']

$ sed -n '41,58p' tarlaanaliz-platform/src/core/domain/value_objects/calibration_class.py
_DRONE_CALIBRATION_CLASS = {
    "DJI_MAVIC_3M": ...RELATIVE,
    "DJI_M350_RTK_SENTERA_6X": ...ABSOLUTE,
    "WINGTRAONE_GEN2": ...ABSOLUTE,          # kanonik ad DEĞİL
    "PARROT_SEQUOIA_PLUS": ...ABSOLUTE,      # kanonik ad DEĞİL
    "AGEAGLE_EBEE_X": ...ABSOLUTE,           # kanonik ad DEĞİL
}
...
    return _DRONE_CALIBRATION_CLASS.get(drone_type.stri
- **neden önemli:** 'Dört depo tek standart: yeni ad icat etmeden önce diğer depolarda ölç' ilkesinin ihlali. Bugün zararsız çünkü varsayılan tesadüfen doğru; matriste bir drone `relative`'e çevrilirse (veya yeni bir relative drone eklenirse) harita sessizce ABSOLUTE döner ve tolerans çarpanı 2.0x yerine 1.0x kalır — kalibrasyon doğrulaması gereğinden sıkı olur, sahada geçerli paketler reddedilir.
- **öneri:** Haritayı sil, `calibration_class_for_drone()` değeri kanonik `drone_capability_matrix.yaml → capabilities[drone_type].calibration_class`'tan okusun (vendored kopya üzerinden). Geçici çözüm isteniyorsa en azından anahtarlar kanonik enum değerlerine düzeltilsin ve 'haritadaki anahtar kümesi = drone_type.enum değer kümesi' testi eklensin. Bu iş E13'ün yeniden açılmasıyla aynı turda yapılmalı — ikisi de aynı ekseni (drone → kalibrasyon sınıfı) kullanıyor.

## 46. [DUSUK] D16-b2'nin 'kr_registry.md 1267→791 satır' iddiası tutmuyor — göç commit'inde ölçüm 813
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1974 (kalem 2, kanıt sütunu)
- **ne yanlış:** Plan D16-b2'nin boyut kanıtını '`ssot/kr_registry.md` 1267→791 satır · `docs/TARLAANALIZ_SSOT_v1_2_0.txt` 1906→1954' diye veriyor. İkinci çift TAM DOĞRU (1906→1954, bugün de 1954). Birinci çiftin 'öncesi' doğru (1267), 'sonrası' YANLIŞ: göçün yapıldığı commit'te (fa76469) dosya 813 satır, bugün 849 satır. 791 hiçbir commit'te ölçülmüyor — muhtemelen iş bitmeden ara bir anın sayısı yazılmış.
- **kanıt:** $ for rev in fa76469~1 fa76469 a8cf512 HEAD; do echo "--- $rev ---"; \
    git show $rev:ssot/kr_registry.md | wc -l; git show $rev:docs/TARLAANALIZ_SSOT_v1_2_0.txt | wc -l; done
--- fa76469~1 ---   kr_registry.md: 1267   SSOT txt: 1906     ← 1267 ✅, 1906 ✅
--- fa76469 ---     kr_registry.md:  813   SSOT txt: 1954     ← iddia 791, ölçüm 813 ❌ / 1954 ✅
--- a8cf512 ---     kr_registry.md:  849   SSOT txt: 1954
--- HEAD ---        kr_registry.md:  849   SSOT txt: 1954
- **neden önemli:** Tek başına zararsız bir boyut istatistiği — kararı taşımıyor, D16-b2'nin ASIL kanıtı olan 'DUAL BODIES 0' ölçümü bugün de tutuyor. Ama Lens 3 açısından anlamlı: aynı kanıt hücresindeki iki sayı çiftinden biri commit'e karşı üretilmiş, diğeri değil. Bir sonraki oturum bu hücreyi 'ölçülmüş kanıt' sayıp benzer bir boyut karşılaştırmasına dayanırsa (ör. 'registry beklenenden 58 satır fazla, biri gövde geri mi yazdı?') yanlış alarma gider.
- **öneri:** Sayıyı '1267→813 (göç commit'i fa76469; bugün 849 — 0.h/K3 ile KR-090'a 4 madde eklendi)' olarak düzelt. Genel kural olarak bu tür boyut kanıtlarına ölçüldüğü commit'i iliştir; kalıcı çözüm yine 'sayıyı değil üreteci yayınla': hücreye `git show <rev>:ssot/kr_registry.md | wc -l` komutunu yaz.

## 47. [DUSUK] S5 gerekçesindeki pipeline.py:2358 atfı AYNI OTURUM İÇİNDE bayatladı — alıntılanan yorumu W12 sildi
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1851 (S5 satırı) → atıf: tarlaanaliz-worker/src/core/services/inference/pipeline.py:2358
- **ne yanlış:** S5 satırı şimdiki zamanla yazılmış: 'Worker kodu bunu zaten biliyor ve düzeltmeyi kendisi tarif ediyor: … *"Kalıcı çözüm: per-job reflectance_scale'i calibration_metadata sözleşmesine ekleyip okumak"* (`pipeline.py:2358`)'. Bu alıntı W12 ÖNCESİ doğruydu (28c747a'da tam 2357-2358. satırlar), ama W12 (ed44426, aynı gün, aynı oturum) düzeltmeyi uygulayınca yorum silindi. Bugün pipeline.py:2358 alakasız CRS kodu ('candidate_crs is not None'); 'Kalıcı çözüm' dizesi worker/src'de HİÇ geçmiyor.
- **kanıt:** BUGÜN:
$ grep -rn 'Kalıcı çözüm' tarlaanaliz-worker/src/     → (çıktı yok, exit 1)
$ python -c "..." # pipeline.py 2357-2360
2357 |                         if (
2358 |                             candidate_crs is not None
2359 |                             and candidate_transform is not None

YAZILDIĞI ANDA DOĞRUYDU (W12 öncesi, 28c747a):
$ git show 28c747a:src/core/services/inference/pipeline.py > $S/pl_old.py
$ python -c "...ara..."
QUOTE AT LINE 2357 |         # felaketi ops'un gün-1'de göreceği görünür bir alarma çevirir. Kalıcı çözüm:
QUOTE AT LINE 2358 |         # per-job reflectance_scale'i calibration_metadata sözleşmesine ekleyip okumak.

DÜZELTME GERÇEKTEN LANDİ (atıf bu yüzden bay
- **neden önemli:** İş DOĞRU yapılmış (W12 landi, PR #186 MERGED) — sorun yalnızca kanıtın adresinin oturum kapanmadan geçersizleşmesi ve şimdiki zamanla bırakılması. Bir sonraki oturum 'worker kodu düzeltmeyi kendisi tarif ediyor' cümlesini okuyup 2358'e gittiğinde CRS kodu bulacak ve ya atfı ya da S5'in ✅ statüsünü sorgulayacak. Bu, teşhis atıflarının genel bir zaafı: aynı turda düzeltilen bir kusurun 'kanıt' satırı, tur kapanışında zaten ölü adres olur.
- **öneri:** S5 satırındaki alıntıyı geçmiş zamana çevir ve adresi commit'e sabitle: '(W12 öncesi `pipeline.py:2358` @28c747a — yorum W12/ed44426 ile kaldırıldı; bugünkü okuma yolu `pipeline.py:2219-2225`)'. Kural olarak: aynı turda kapatılacağı bilinen bir kusurun dosya:satır kanıtını daima `dosya:satır @commit` biçiminde yaz — satır numarası kayar, commit kaymaz.

## 48. [DUSUK] KR-092 kanıtındaki seasonal_flight_calendar.py:105-108 aralığı iki koşuldan yalnız birini kapsıyor
- **lens:** LENS 3 — ÖLÇÜM DÜRÜSTLÜĞÜ: 2026-07-31 ve 2026-08-01 oturumla
- **nerede:** tarlaanaliz-contract/docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md:1975 (kalem 2a) → atıf: tarlaanaliz-platform/src/core/domain/value_objects/seasonal_flight_calendar.py:105-108
- **ne yanlış:** 2a şöyle diyor: '`seasonal_flight_calendar.py:105-108` H/v < 3,9 **veya irtifa > 120 m'de** SeasonalFlightCalendarError yükseltiyor'. Ölçüm: 105-108 yalnız H/v (sensör hız kısıtı) kolunu içeriyor; irtifa > MAX_LEGAL_ALTITUDE_M_AGL kolu 101-104'te. Yani iki koşullu iddia tek koluna atfedilmiş; doğru aralık 100-110.
- **kanıt:** $ python -c "..." # platform/src/core/domain/value_objects/seasonal_flight_calendar.py 100-110
100 |         # KR-092 fail-closed: SHGM azami irtifa
101 |         if self.altitude_m > MAX_LEGAL_ALTITUDE_M_AGL:      ← İRTİFA KOLU (atıf dışında)
102 |             raise SeasonalFlightCalendarError(
103 |                 f"altitude_m {self.altitude_m} > {MAX_LEGAL_ALTITUDE_M_AGL} m AGL (SHGM sınırı) — KR-092"
104 |             )
105 |         # KR-092 fail-closed: sensör hız kısıtı H/v ≥ 3,9
106 |         if self.altitude_m / self.speed_ms < SENSOR_SPEED_RATIO_MIN:   ← ATFEDİLEN ARALIK
107 |             raise SeasonalFlightCalendarError(
108 |                 f"H/v = {self.altitude_m}/{self.spee
- **neden önemli:** İddianın ÖZÜ doğru: davranış gerçekten fail-closed (raise), clamp değil — yani 2a'nın 'kod ölçüldü, registry haklı çıktı' hükmü ve SSOT metnindeki düzeltme yerinde. Zarar sınırlı, ama bu atıf KR-092'nin normatif metnini değiştiren kararın tek kod dayanağı; ileride 'irtifa sınırı gerçekten fail-closed mu?' diye kontrol eden biri verilen aralıkta o kolu bulamayacak ve mevzuat (SHGM) sınırının zorlandığından emin olmak için kodu baştan taramak zorunda kalacak.
- **öneri:** Atfı `seasonal_flight_calendar.py:100-110` yap (iki fail-closed kolunu da kapsar), ya da iki koşulu ayrı ayrı yaz: 'irtifa > 120 m → :101-104 · H/v < 3,9 → :105-110'. Bu satırdaki diğer atıflar (seasonal_flight_calendar_loader.py:92, missions.py:855-899) doğrulandı, yalnız bu aralık daraltılmalı.

## 49. [DUSUK] Edge dağıtım paketi dist/M1 iki MINOR geride donmuş — 1.2.0, `raw_frames` bloğu yok, `$id` host'u eski
- **lens:** LENS 5 — Sınıf taraması eksikleri ("tek örneği düzeltip geçm
- **nerede:** tarlaanaliz-edge/dist/M1/CONTRACTS_VERSION.md (`CONTRACTS_VERSION=1.2.0`) · dist/M1/interface/contracts/schemas/edge/*.v1.schema.json (8 dosyanın 8'i canlı vendored'dan farklı) — dizin `.gitignore:5` ile izlenmiyor
- **ne yanlış:** `dist/M1`, edge'in kioska götürülen paketinin yerel kopyası. Depo 1.4.0'a çıktı, dist/M1 hâlâ 1.2.0'da. Aradaki iki bump'ın getirdiği alanlar pakette YOK: C8'in vendor'ladığı `raw_frames` bloğu (~50 satır) tamamen eksik, `$id` host'u eski (`tarlaanaliz.com` ↔ canlı `api.tarlaanaliz.com`). Sınıf 3 taraması "vendored kopyalar" derken bu ÜÇÜNCÜ kopyayı hiç saymadı.
- **kanıt:** ```
$ diff -rq interface/contracts dist/M1/interface/contracts
Files ... attestation_record.v1.schema.json ... differ      (8 dosyanin 8'i)
$ diff interface/.../calibrated_dataset_manifest.v1.schema.json dist/M1/.../calibrated_dataset_manifest.v1.schema.json
3c3
<   "$id": "https://api.tarlaanaliz.com/schemas/edge/calibrated_dataset_manifest.v1.schema.json",
---
>   "$id": "https://tarlaanaliz.com/schemas/edge/calibrated_dataset_manifest.v1.schema.json",
111,160d94
<     "raw_frames": { ... }        # C8'de vendor'lanan blok — dist'te YOK
$ grep -m1 CONTRACTS_VERSION dist/M1/CONTRACTS_VERSION.md  ->  CONTRACTS_VERSION=1.2.0
$ git check-ignore -v dist/M1/CONTRACTS_VERSION.md  ->  .gitignore:5
- **neden önemli:** Şiddeti düşük tutuyorum çünkü dizin git-izli değil ve yeniden üretilebilir bir yapı çıktısı — bir kural ihlali değil. Ama demo donanım profili (Latitude 7300, Docker/GPU yok) düşünüldüğünde kioska fiilen taşınan şey bu dizin olabilir; o hâlde sahada iki MINOR geride, `raw_frames` tanımayan bir şema seti koşar ve platformdan gelen geçerli bir manifest reddedilir.
- **öneri:** (1) Paketi yeniden üret (`dist/M1`'i canlı `interface/contracts` + `CONTRACTS_VERSION.md`'den kur) ya da bayat olduğu görülebilsin diye sil. (2) Kalıcı çözüm: paketleme script'ine bir tazelik kapısı — `dist/M1/CONTRACTS_VERSION.md` ile kök `CONTRACTS_VERSION.md` ayrışıksa paketleme kırmızı.

## 50. [DUSUK] KR-090 saklama satırı `raw_frames` için yanlış taşıyıcı beyan ediyor; iki kanonik ifade birbiriyle çelişiyor ve kapı ikisini de göremiyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** ssot/kr_registry.md:729-730 ("taşıyıcılar: edge + platform `calibrated_dataset_manifest.v1`") ↔ tests/test_calibrated_manifest_fields.py:268-270 (test_raw_frames_live_in_edge_form_only) ↔ tests/test_data_governance.py:68-72 ("ÖLÇÜLDÜ: yalnız EDGE formunda gerçek property. Platform formunda yok.")
- **ne yanlış:** 0.h kapısının kendi docstring'i (satır 46-52) platform formunun `raw_frames` TAŞIMADIĞINI ölçtüğünü açıkça yazıyor ve DATA_CATEGORIES'i buna göre düzeltmiş. Ama saklama politikasının normatif metni düzeltilmemiş: KR-090 madde 10 hâlâ "edge + platform" diyor. Kapı yalnız anahtar adının KR-090 gövdesinde geçip geçmediğine baktığı için, satırın taşıyıcı iddiasının doğruluğunu ölçmüyor.
- **kanıt:** $ grep -n "taşıyıcılar: edge + platform" -B1 -A2 ssot/kr_registry.md
729:10) **Seçilmiş ham kareler** (`raw_frames`; taşıyıcılar: edge + platform
730:    `calibrated_dataset_manifest.v1`). **Süre: 180 gün (en kısa kademe).**
$ python -c "json ... 'raw_frames' in platform_form['properties']" → False
$ tests/test_calibrated_manifest_fields.py:270 → assert "raw_frames" not in _load(PLATFORM_FORM)["properties"]  (yeşil)
$ pytest tests/test_data_governance.py -q → 11 passed  (çelişkiyi görmüyor)
- **neden önemli:** Saklama politikası bir silme yükümlülüğüdür: "platform tarafında da 180 günde sil" diyen bir satır, silinecek bir şey olmayan bir yeri işaret ediyor ve tersine, gerçek taşıyıcının tek olduğu bilgisini bulanıklaştırıyor. Küçük ama D16'nın kapattığı sınıfın aynısı: prose bir şey söylüyor, ölçüm başka.
- **öneri:** KR-090 madde 10'daki taşıyıcı listesi "edge `calibrated_dataset_manifest.v1`" olarak düzeltilsin. Kapıya küçük bir ek: DATA_CATEGORIES'teki `carriers` listesi ile KR-090 satırında ANILAN dosya adları karşılaştırılsın (metinde geçen taşıyıcı, listede olmalı ve tersi) — böylece kayıt ile ölçüm bir daha ayrışamaz.

## 51. [DUSUK] "Tur/release durumunun TEK makine-okunur kaynağı" bayat: PENDING_REPIN beyanı var olmayan bir dal adını ve turun yalnız üçte birini anlatıyor
- **lens:** LENS 2 — KAPI ETKİNLİĞİ (2026-07-31 + 2026-08-01 oturumların
- **nerede:** CONTRACTS_VERSION.md:8 ("**Checksum State:** PENDING_REPIN — tur `feat/s5-reflectance-scale` sürüyor") ve :20 ("**Tur içeriği:** S5 — ...") · bu dosyayı okuyan üç kapı: tests/release_state.py:16-21
- **ne yanlış:** Beyan, S5 PR'ı (#23) merge edildikten sonra güncellenmedi; ardından PR #24 ile C6b/S2 · S4 · S6 · S7 de aynı tura girdi. Bugün: (a) atıf yapılan dal adı depoda yok (gerçek dal `s5-reflectance-scale`, `feat/` öneki yok), (b) "Tur içeriği" satırı turun dört kaleminden üçünü hiç anmıyor. release_state.py bu dosyayı "tur/release durumunun TEK makine-okunur kaynağı" ilan ediyor ve üç kapı (CI verify-checksums işi + iki xfail(strict)) davranışını buradan alıyor.
- **kanıt:** $ grep -n "Checksum State|Tur içeriği" CONTRACTS_VERSION.md
8:**Checksum State:** PENDING_REPIN — tur `feat/s5-reflectance-scale` sürüyor
20:> **Tur içeriği:** S5 — `worker/calibration_metadata.v1`'e reflektans ölçeği (`scale`) bloğu.
$ git branch -a | grep s5 → "  s5-reflectance-scale"   (feat/ önekli dal YOK)
$ git log --oneline -3 → 7a508fb docs(handoff)... / 2a8f1af Merge PR #24: C6b/S2 · S4 · S6 · S7 ... / 0224586 docs: MAJOR turu...
(CHANGELOG.md:17-45 ise dört kalemi de listeliyor → iki kayıt ayrışmış)
- **neden önemli:** Kapıların davranışını belirleyen beyan, C8 töreninde "bu turda ne değişti" sorusunun cevabı olarak okunacak. Bugünkü hâliyle re-pin yapan kişi turu S5'ten ibaret sanabilir; S6'nın eklediği `$defs.file_artifact.reflectance_scale` ve C6b/S2'nin yarım kalan uygulaması (bulgu 1) beyanda hiç görünmüyor. Bu, "beklenen kırmızının gerekçesi bayatlayabiliyordu" (SD7) sorununun aynı dosyada tekrarı.
- **öneri:** PENDING_REPIN satırı dal adı yerine tur kimliği (ör. "TUR 2") taşısın ve "Tur içeriği" satırı CHANGELOG'un [Unreleased] başlıklarından türetilsin. Küçük bir kapı: `test_pin_version.py`'ye "beyanda anılan tur kalemleri ⊇ CHANGELOG [Unreleased] alt başlıkları" assert'i eklenebilir — beyanın bayatlaması artık kırmızı verir.

