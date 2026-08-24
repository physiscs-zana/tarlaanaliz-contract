# Eylem Planı — ARŞİV (2026-08 turları)

> **Rolü: KANIT ARŞİVİ, iş listesi DEĞİL.** Buradaki bölümler
> `TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` içinden **bayt-özdeş taşındı**
> (2026-08-24); plan dosyası 3993 satıra şişmişti ve dört ayrı
> *"SONRAKİ OTURUM — BURADAN BAŞLA"* iddiası taşıyordu. O sınıf bu depoda
> zaten bir kez zararlı ilan edilmişti (§14.15'in kaldırılma gerekçesi).
>
> **Hiçbir satır silinmedi.** Taşınan bölümlerin **açık kalemleri** planda
> `§14.A` altında canlı tabloda durur; buradaki gövdeler o kalemlerin
> **gerekçesi ve ölçüm kanıtıdır**.
>
> ⚠️ **Yeni iş buraya yazılmaz.** Bir kalem yeniden canlanırsa plan dosyasına
> taşınır; burası yalnız okunur geçmiştir.
>
> | Ararken | Bak |
> |---|---|
> | Bugünün iş listesi | `TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` |
> | Devralınan açık kalemler | aynı dosya, **§14.A** |
> | Depo durumu / devir | `SESSION_HANDOFF.md` §0.A |

---

## 14.9 ▶️ SONRAKİ OTURUM — **"DEVAM ET" DENİNCE BURADAN BAŞLA** (2026-08-01 kapanışında yazıldı)

> §14.8 (ÖD-1…ÖD-16) **kapandı**; W14 · E16 · SD9 · SD10 · SD11 kararları **verildi ve uygulandı**.
> Aşağıdaki sıra **yürürlüktedir**: bir kalem burada yoksa yapılmaz; yapılacaksa önce buraya yazılır.

### 🔬 ÖZ-DENETİM (2026-08-01 gece) — önceki oturumun işi ölçüldü
Kanıt: `denetim/denetim_raporu_2026-08-01_gece_ozdenetim_onceki_oturum.md` (elle ölçüm, ajan turu değil).
**Kapanış beyanlarının 7'si de yeniden üretildi ve tuttu** (süit 1227/2 · validate 164/0 · dist 68
yetimsiz · dört depo temiz+senkron · 0 açık PR · master CI 5/5 yeşil · dedektör 9 değişiklik/0 breaking).

| # | Bulgu | Durum |
|---|---|---|
| 🔴 **Ö1** | **CI, yerelde kırmızı olan `ee4aed7`'i YEŞİL geçirdi.** Kırılan test contract CI'ında **atlanan** 134 testin içindeydi (kardeş depo okuyor). ⇒ Bu depoda CI, kardeş-bağımlı kapılar için **otoriter değildir**; süitin %11'ini koşmaz. Yerelde 20 sn'de yeniden üretilir: `git clone --local . <boş dizin>` → `pytest` → CI'ın çıktısı birebir (`1093 passed, 134 skipped`) | ölçüldü · kalıcı çözümü **E17/W10** |
| 🟠 **Ö2** | **E17/W10 kapsamı bir dosya eksikti** — yalnız `test_vendored_parity.py` (132 atlama) sayılıyordu, `test_c11_sorties_absorption.py` (2 atlama) sayılmıyordu. Eski hâliyle uygulansaydı o 2 test **hiçbir CI'da** koşmayacaktı | ✅ kalem metni düzeltildi (SIRA 3) |
| 🟠 **Ö3** | **Atlama kapısı dosyaya bakmıyordu:** eşleşme yalnız gerekçe dizesineydi → C11 dosyası, parite süiti için yazılmış beyanın altına **adı geçmeden** sığındı; beyanın notu da bayattı (47 → gerçek 134) | ✅ beyan `(gerekçe, dosya, not)` oldu; **mutasyon kırmızı** (beyansız dosya → exit 1), kontrol yeşil |
| 🟡 **Ö4·Ö5·Ö6** | **Karar koda yazıldı, çevresindeki metin eski dünyayı anlatmaya devam etti** (3 örnek): §14.9'un *"3 beyan açık"*ı (gerçek **2**) · `MEASURED_DEBT_VALUES` yorumu (*"16 değer"*, gerçek **6**) · C11 docstring'i (*"E16 açık"*, gerçek **kapandı** — altındaki test tersini iddia ediyor) | ✅ üçü de düzeltildi |
| 🔵 **Ö7** | W14'ün **kalıcı** beyanı, *"kalıcı olamaz · yalnız küçülür"* diyen `KNOWN_VENDORED_AHEAD` içinde duruyor. Bugün delik değil (6 değerin 6'sı dolu, yeni sapmaya yer yok) ama sayaç 0'a inemez ve yapının metni yanlış | ⬜ **C8 SONRASI**: kalıcı beyanları `DECLARED_NARROWER_DEFS` benzeri ayrı yapıya taşı |

### ✅ SIRA 1 — **C8 töreni TAMAMLANDI (2026-08-02, v7.4.0 YAYIMLANDI)**

> Altı adımın altısı da koşturuldu. **Beş değişmez ölçüldü ve tuttu:**
> I-1 `7.4.0 = 7.4.0 = v7.4.0` (edge yerel `1.5.0` / upstream `7.4.0`) · I-2 `objecttype=tag`,
> `describe` temiz, **23 tag** · I-3 platform submodule `eb28b74` = `v7.4.0^{}`, checksum
> **96/96** · I-4 worker öz-hash `bb66e1bc…` OK · I-5 devir spesi **uzlaştı ve silindi**.
>
> | Adım | Sonuç |
> |---|---|
> | 1 · dedektör | **9 değişiklik / 0 breaking** + dedektörden bağımsız düzleştirilmiş tarama (89 dosya) **0 bulgu**; ikinci araç **3/3 mutasyonla** görür kanıtlandı |
> | 2 · `PENDING_PROPAGATION` **boşaltıldı** | edge #51 (`PANEL_ABSOLUTE` · `RGB` · `qc_report.flags` 5 değerlik) · worker #189 (`calibration_method`). ⚠️ `flags` bir DARALTMADIR; güvenli olduğu **ölçüldü** (`qc_report_writer.py:154-165` tam o beşini yazıyor). S4 beyanının gerekçesi **yön değiştirdi**: alan eksik kaldıkça onu yazan ilk belge worker kapısında reddedilirdi → vendor'lamak ölü alan değil **mayın temizleme** |
> | 3 · `pin_version --minor` | 7.4.0 + `info.version` üçü birden (SD9). 🔴 **Araçta hata bulundu** (aşağıda) |
> | 4 · annotated tag | `v7.4.0` atıldı ve push'landı, I-2 ölçümle doğrulandı |
> | 5 · üç depo re-pin | platform **#352** · worker **#189** · edge **#51** — dördü de CI yeşil, merge edildi |
> | 6 · devir spesi | worker **#190** — uzlaşma koşulu `git show v7.4.0:<yol>` ile ölçüldü (ileri alan **0**), sonra silindi |
>
> 🔴 **Tören release aracının kendisinde bir hata buldu:** `pin_version.py` agrega checksum'ı
> yazdıktan **sonra** `api/*.yaml`'ı senkronluyordu; o dosyalar checksum kümesinin **içinde**
> olduğu için pin doğduğu anda bayat oldu (`--verify` anında kırmızı). v7.3.0 turunda
> görünmemişti: `info.version` o tur `1.0.0`'da kalmış, senkron hiçbir baytı değiştirmemişti.
> Sıra düzeltildi (senkron → hash → yaz) + regresyon kapısı yazıldı, mutasyonla doğrulandı.
> **Ders:** bir release adımı, checksum kümesinin içindeki dosyayı değiştiriyorsa **hash'ten
> önce** koşmalıdır; "ilk kez gerçekten çalışan" bir adım ilk koşuşunda denetlenmelidir.
>
> Kapılar: pytest **1232 passed / 0 skip / 0 xfail** · validate **164/0** · dist 68 yetimsiz
> · `pin_version --verify` ✅ `c7b8d46e…`.

<details><summary>Törenin özgün 6 adımlık tarifi (tarihsel — bir sonraki C8 için)</summary>

#### C8 töreni: TUR kapatma (referans)
Tur açık kaldıkça `PENDING_REPIN` beyanı iki xfail'i canlı tutuyor ve **üç depo checksum'ı
doğrulanamıyor**. Turun taşıdığı içerik: `S5 · C6b/S2 · S4 · S6 · S7` + **ÖD-1** (edge kalibre
enum) + **ÖD-2** (`analysis_job` `$defs`) + **E13-R** (türetme bloğu) + **SD9** (`info.version`)
+ **SD10** (OpenAPI düzeltmeleri).

**Sıralı adımlar (SDLC_GATES §3G ile birebir):**
1. `python tools/breaking_change_detector.py --old v7.3.0 --new .` → **0 breaking** bekleniyor
   (artık git ref kabul ediyor — ÖD-16). İkinci bağımsız ölçüm: elle diff (`required`/enum/tip).
2. `PENDING_PROPAGATION`'ı **BOŞALT** — bugün **2** beyan açık *(ölçüldü 2026-08-01 gece; bu satır
   önce "3" diyordu ve üçüncüsü `analysis_job` idi — o beyan `527c174`'te **zaten silinmişti**,
   §14.9 yazılırken bayat kopyalandı. Öz-denetim bulgusu Ö4)*:
   * edge `calibrated_dataset_manifest`: `calibration_type` ←`PANEL_ABSOLUTE` · `raw_frames[].band`
     ←`RGB` · `qc_report.flags` ← 5 değerlik sözlük *(edge PR gerekir)*
   * worker `calibration_metadata`: `calibration_method` *(okuyan kod yok — S4; ya okuma kodu
     yazılır ya beyan gerekçesi tazelenir)*
3. `python tools/pin_version.py --minor` → `CONTRACTS_VERSION.md` + **`info.version` üçü birden**
   otomatik yazılır (SD9). `PENDING_REPIN` satırı **kendini siler** → üç kapı sertleşir.
4. `git tag -a v7.4.0 <release commit>` + push (**I-2**: `objecttype=tag`, `git describe` temiz).
5. Üç depo re-pin: platform submodule → etiketli commit · worker `compute_contracts_hash.py
   --update --version v7.4.0` · edge upstream ref. **I-1** üç depoda aynı dizeyi göstermeli.
6. Worker `denetim/scale_wire_devir_spec_2026_08_01.md` **silinir** (uzlaşma koşulu bu turdu).

</details>

### ✅ SIRA 1 — **P1 UYGULANDI (2026-08-02): iki bayrak da `True`**
`worker_result_schema_enforce` **ve** `edge_manifest_schema_enforce` açıldı. Plan tek bayraktan
söz ediyordu; ölçümde **iki** bayrak ve **üç** doğrulama yüzeyi olduğu görüldü. Önkoşul
varsayılmadı, her yüzeyin **ret kümesi** ölçüldü:

| Yüzey | `enforce=True` bugün neyi reddeder | Sonuç |
|---|---|---|
| `intake_manifest` (edge→platform, 422) | edge'in gerçek fixture'ı Pydantic'ten geçip `model_dump` edildikten sonra kanoniğe karşı **0 hata** | güvenli |
| `analysis_result` (worker→platform, DLX) | vendored kopya kanonikten **DAHA SIKI** (`required` ⊇ kanonik: +`confidence_score`, +`result_mode`; fazladan enum değeri yok) ⇒ worker'ın ürettiği her belge kanoniği de geçer | güvenli |
| `expert_review_queue` (worker→platform, DLX) | vendored `crop_type`'ta kanonikte **olmayan 4 değer** (APPLE/CHERRY/FIG/PEACH — W14 ekseni) ⇒ ret kümesi teorik olarak **boş değil** | bugün **ulaşılamaz**: `GAP_OFFERED_CROPS` = {COTTON, CORN, PISTACHIO, RICE, GRAPE}, dördü de yok |

🔴 **İki bayat beyan bulundu ve temizlendi:** `settings.py` ve `ingest.py` engel olarak
*"Pydantic↔intake_manifest.v1 alan-drift'i (`av_scan_result` string vs object …)"* diyordu;
o drift **DENETIM-FIX (K-3) turunda zaten giderilmişti**. Yani P1 aylardır **var olmayan bir
gerekçeyle** kilitliydi. (`docs/architecture/data_lifecycle_transfer.md:195` de aynı bayat
gerekçeyi tekrarlıyordu — düzeltildi.)

⚠️ **Güvence nerede duruyor:** `expert_review_queue` için tel üstünde değil **platform
kapısında** (bookable ürün kümesi). W14'ün yeniden açılma koşulu aynen geçerli ve artık
maliyeti daha yüksek: bu ürünlerden biri siparişe açılırsa **tel önce genişletilmeli**, yoksa
escalation nack→DLX ile **kaybolur**.

📌 Yeni bulgu **P20** (aşağıda): kapı ham gövdeyi değil `model_dump()` çıktısını doğruluyor.

<details><summary>P1'in özgün kaydı</summary>

E16 ile edge çıktısı kanonik sözlüğü konuşuyor **ve** TUR 2 kapandı → P1'in iki önkoşulu da
karşılandı. Platform deposu: **commit için kullanıcı onayı gerekir** (platform CLAUDE.md
*"Commit yalnızca kullanıcı açıkça istediğinde oluşturulur"*). Yöntem bu turda kanıtlandı:
dal + PR + CI yeşilse merge.
</details>

### 🥈 SIRA 2 — ~~P1 açılabilir (kilit kalktı)~~ → **SIRA 1'e taşındı**
E16 ile edge çıktısı kanonik sözlüğü konuşuyor → platform `enforce=True` artık edge'i kırmaz.
Plan bunu *"E16'dan SONRA"* diye kilitlemişti; kilit **açıldı**. (Platform deposu; commit için
kullanıcı onayı gerekir — CLAUDE.md kuralı.)

### ✅ SIRA 3 — kardeş depo kuyruğu **KAPANDI** (2026-08-02, otonom tur)

> Beş kalem, altı PR, dört depo — hepsi CI yeşil ve merge edildi:
> edge **#52** (E18+E15) · **#53** (E17) · platform **#354** (P15+P19) ·
> worker **#191** (W15+W8) · **#192** (W10) · contract **#27** (C8-a).
>
> | # | Sonuç |
> |---|---|
> | **E18** ✅ | Sessiz `except` fail-loud oldu. **P14 sessizliğin bedelini değiştirmişti**: eskiden tehlikeli bir *yükseltme*, şimdi **teşhis edilemez bir ret** (okunamayan dosya → `NONE` → worker sert kapısı). Üç bayat yorum düzeltildi. **Mutasyon: 6 test kırmızı.** 🔴 Yan bulgu: dört fixture `calibrated.json` yolunu veriyor ama dosyayı **hiç yazmıyordu** — yani düzeltilen hatanın *üzerinde* duruyorlardı (aynı ders P14 turunda da çıkmıştı) |
> | **E15** ✅ | *"Ölçemedik"* ile *"kapsama sıfır"* ayrıldı (`CoverageComputationError`); `min(...,1.0)` kırpması artık WORM kaydına ham oranla giriyor. ⚠️ **Ölçüldü: bu sınıfın bugün üretim çağıranı YOK** (yalnız testler) — düzeltme bugünkü bir kaybı durdurmuyor, ilk çağıranda patlayacak mayını temizliyor |
> | **P15** ✅ | Plan *"tek satır"* diyordu; ölçüm **5 yer** gösterdi (sabit ×1 + `drone_capability_matrix.yaml` ×4, matris **canlı** — `drone_registry_loader` yüklüyor). Beşi de `LCI` |
> | **P19** ✅ | *"Ya besle ya kaldır"* dendi; **üçüncü cevap** çıktı. Önce kaldırdım, sonra **geri aldım**: davranış açıkça test edilmiş, eksik olan kod değil **üretici bağlantısı**. Durum beyan edildi ve **kapıya bağlandı** (AST tabanlı, iki yönde mutasyon kırmızı) |
> | **W15** ✅ | Docstring okumadığı alanı okuduğunu söylüyordu — S4 beyanının gerekçesini yanlış yönlendiriyordu |
> | **W8** ⚠️ | **Yarısı**: builder + 27 test (gerçek vendored şemaya karşı; anti-anchoring kısıtları tek tek sızdırılıp reddedildiği ölçüldü). **Çağrı yeri BİLEREK bağlanmadı → W8-b** (aşağıda) |
> | **E17 / W10** ✅ | Kardeş CI kapıları kuruldu. 🔴 **Kapı ilk koşuşta kendi ölçütümü çürüttü**: *"atlama = 0"* beklentim yanlıştı (`95 passed, 69 skipped`) — parite süiti iki deponun çiftlerini birden kapsıyor, karşı taraf PRIVATE olduğu için meşru atlanıyor. Ölçüt *"BU depoya ait atlama yok"* + *"hiç test koşmadıysa da kırmızı"* oldu. Edge 95 koşuyor, worker 85 — **birleşim** contract CI'ında görünmeyen 134 testi kapsıyor |
> | **C8-a** ✅ | Yayılım aracı. 🔴 **Araç kendi mutasyonuyla iki kez yakalandı**: (a) SUBSET çiftlerine 28 **sahte** öneri, (b) `--check` kusursuzken **`--apply` hiçbir şey yazmıyordu** (exit 0 ile). İkincisi yalnız mutasyonla göründü; mutasyon teste çevrildi (11 test) |

### 🆕 SIRA 3'ten DOĞAN kalemler
| # | Depo | İş | Ölçülmüş gerekçe |
|---|---|---|---|
| 🔴 **W8-b** | worker | Denetim satırı emisyonunun **çağrı yerini** bağla — çekiliş `core/services/inference/pipeline.py:~1715`'te (`tiles`/`healthy_tiles`/`anomaly_tiles`) yapılmalı, üç katman boyunca taşınmalı | Publish noktasında elde **yalnız `result.detections`** var (anomali tile'ları). Oradan çekiliş, örneği *"anomali olma"* koşuluna bağlar — sampler'ın kendi bilimsel gerekçesi bunu yasaklıyor (*"selection indicator must be uncorrelated with the quantity being measured"*). **Yanlı çekiliş, hiç çekiliş yapmamaktan kötüdür**: ölçüm temeli sessizce geçersiz olur ve bunu fark edecek kapı yok |
| ⬜ **P21** | platform | `consensus_participation` alanını **kalıcılaştır** (`ExpertReviewModel` kolonu + worker mesajından okuma) | **P16'nın eksik ortası.** Ölçüldü: kanonik `expert_review_queue.v1` alanı tanımlıyor ✅ · worker yazmıyor (**W8**) · platformda **kolon yok** → konsensüs yolu (`expert_portal._evaluate_publication_gate`) dışlayacak bir şey bulamaz |
| ⬜ **P16** | platform | Konsensüs yolu `EXCLUDED` satırı saymamalı | 🔒 **W8-b + P21'e bağlı.** Bu turda uygulanamadı — yokluğu ölçüldü, uydurulmadı |
| ⬜ **W8-c** | worker | `AuditSetSampler` oran tablosunu doldur (bugün boş → hiçbir tile seçilmiyor) | AL-W1; aktivasyon **bilinçli bir ops kararı**, kod hazır |

<details><summary>SIRA 3'ün özgün kuyruğu (tarihsel)</summary>

| # | Depo | İş | Neden şimdi |
|---|---|---|---|
| **E17 / W10** | edge · worker | Kardeş-bağımlı **İKİ** kapıyı kardeş CI'da koştur (D4-b uygulaması): `tests/test_vendored_parity.py` **+ `tests/test_c11_sorties_absorption.py`** | Kapı bu turda 16 dosyaya genişledi ve **5 gerçek sapma** buldu; kardeş CI'da koşmadıkça sapma yalnız yerel diskte görünür. 🔴 **Kapsam 2026-08-01 gece'de düzeltildi (Ö2):** kalem yalnız parite dosyasını sayıyordu, ama contract CI'ında atlanan 134 testin **2'si C11 dosyasındandır** — kalem eski hâliyle uygulansaydı o 2 test **hiçbir CI'da** koşmayacaktı. Tam da orada yaşandı: `ee4aed7` yerelde kırmızıyken CI'ı **yeşil** geçti (Ö1) |
| **E15** | edge | `qc_report_writer`: `min(...,1.0)` kırpması + `except → 0.0` sessiz yolu **fail-loud** | G1/KR-065 ödeme hesabına giriyor |
| **W8** | worker | Denetim satırı emisyonu (`tile_id`, π_h, rotation, bucket, `confidence_score: 0`) | Sampler bunları zaten hesaplıyor; M1/M3 ölçüm temeli |
| **P15 · P16** | platform | `spectral_tier.py:51` → `LCI` · konsensüs yolu `EXCLUDED` saymamalı | AK-1 · M2 |
| **C8-a** | contract | `tools/propagate_vendored.py` — yayılımı elle yapmayı bırak | C8'de üçüncü kez elle yapılacak; ilk denemede 45 test kırılmıştı |
| 🆕 **E18** | edge | `calibration_pipeline._read_calibration_type`: `except (OSError, ValueError) → None` sessiz yolu **fail-loud** + üç yorumu düzelt | **E15 ile aynı sınıf, aynı turda çözülmeli.** ÖD-0'da ölçüldü: okunamayan kalibre manifest → edge alanı **sessizce atlar** → platform `NONE` türetir → worker KR-018/082 işi reddeder; operatör *"kalibrasyon reddedildi"* görür, gerçek sebep **okunamayan dosya**dır. Üç yorum (`:450` · `:282` · `manifest_writer.py:224`) hâlâ *"platform PANEL_ABSOLUTE varsayar"* diyor — **P14 o ağı 2026-08-01'de kaldırdı**; yanlış değişmez, alanın atlanmasına karar veren `if`'in tam üstünde öğretiliyor |
| 🆕 **P19** | platform | `_derive_calibration_type` 2. adımı (`CalibrationRecord.calibration_manifest`) **ölü** — ya besle ya kaldır | Ölçüldü: `src/`+`tests/`+`scripts/`+`alembic/` içinde o alana **hiç değer atanmıyor** (kolon hep NULL). Docstring 3 kaynak sayıyor, gerçekte **1 kaynak + fail-closed** var → E18'in etkisini büyütüyor (tek kaynak sessizce kaybolunca yakalayacak yedek yok) |
| 🆕 **W15** | worker | `calibration_input_parser.py:3` docstring'i *"Reads calibration_method"* diyor; fonksiyon **`calibration_type`** okuyor | Küçük ama **yanıltıcı**: S4 beyanı *"okuyan kod yok"* gerekçesine dayanıyor; bir sonraki oturum `calibration_method` diye grep atınca bu satırı bulup yanlış sonuca varır |
| 🆕 **P20** | platform | Ingest sözleşme kapısı **ham istek gövdesini değil** Pydantic `model_dump()` çıktısını doğruluyor → modelde tanımsız alanlar doğrulamadan **önce** düşer ve kapı onları hiç görmez | P1 ölçümünde çıktı: `sorties` ve `mission_date` bugün tam olarak böyle düşüyor — **ikisi de C11 ile kanoniğe absorbe edilmişti** ve platform `sorties`'i hiçbir yerde kullanmıyor (0 atıf). Bugün veri kaybı değil (kimse tüketmiyor) ama kapı *"edge'in gönderdiğini doğruluyoruz"* diye okunuyor, oysa **kendi yeniden inşasını** doğruluyor. ÖD-3'ün tam deseni: kapı, koruduğunu iddia ettiği yüzeyi ölçmüyor. Çözüm ya ham gövdeyi de doğrula ya alanları modele ekle — hangisi olacağı ürün kararı (per-sortie ürün atıfı platform entegrasyonunda izlenen bir kalem) |

</details>

### 🔶 SIRA 4 — **MAJOR TURU (v8.0.0)** — ✅ **kilit KALKTI (TUR 2 kapandı, v7.4.0 yayımlandı)**
> ### ✅ AK-11 KAPANDI (2026-08-02) — MAJOR turunun ilk adımı hazır
> Dedektör artık `FIELD_MADE_REQUIRED` yolunda da `x-compat-accepted` beyanını tanıyor.
> **Kusur iki katmanlıydı:** tip kabul listesinde yoktu **ve** o dal `_record()`'u hiç
> çağırmıyordu (doğrudan `self.changes.append`). Yani *"üretici yok, ÖLÇÜLDÜ"* gerekçesi
> bu değişiklik tipinde geçirilemiyor, kalemler **mekanik olarak** MAJOR'a itiliyordu —
> beyan mekanizmasının kendisi tutarsızdı.
>
> **Yeni koşul — açık opt-in:** beyan `"accepts": ["FIELD_MADE_REQUIRED"]` taşımalı.
> Gerekçe ölçüldü: `x-compat-accepted` düğüme yapıştırılır ve aynı düğümde birden fazla
> değişiklik olabilir; mevcut beyanlar `change`'i **serbest metin** yazıyor, dolayısıyla
> tip eşleşmesi metinden çıkarılamaz. Açık liste olmadan, pattern için yazılmış bir
> gerekçe *"zorunlu kıldım"*ı da sessizce indirirdi. Eski beyanlar daraltmalarda **aynen**
> çalışıyor (geriye uyum testli).
>
> Kapı: `tests/test_ak11_required_acceptance.py` (8 test). **Mutasyon iki yönde kırmızı:**
> opt-in kontrolü kaldırılınca 2 test, `_record` bağlantısı geri alınınca 1 test.
>
> ⇒ **S7-b artık beyanla MINOR turda da kapatılabilir.** Zorunlu kılma kararının kendisi
> hâlâ ürün kararıdır ve bu turun içeriğindedir.
>
> 📌 **Küçük borç:** `schemas/edge/calibrated_dataset_manifest.v1` → `raw_frames[].band`
> açıklaması hâlâ *"dedektör … hiç kontrol etmiyor (satır 615-630)"* diyor — artık bayat.
> Bilerek bu turda düzeltilmedi: yalnız prose değişikliği bile checksum + dist kapılarını
> kırıyor ve üç depoyu yeniden pinlemeyi gerektiriyor (ölçüldü). **S7-b aynı alana
> dokunacağı için o turda birlikte düzeltilecek.**

---

## ▶️ GİRİŞ NOKTASI — **MOTOR-AGNOSTİK KALİBRASYON + v7.5.0 TURU** (2026-08-02, araştırma sonrası)

> 🆕 **2026-08-05 EKİ — bu bölüm hâlâ geçerli, ama artık TEK hat değil.** O tarihte
> **donanım gerektirmeyen** ikinci bir hat ilerledi: çiftçi sonuç akışı uçtan uca
> çalıştırıldı ve dört-disiplinli denetimin demo-öncesi kritikleri kapatıldı
> (platform PR #381). Aşağıdaki **P-2 · P-6** hâlâ **donanım/ölçüm kapılıdır** (RTX 3090
> makinesinde işlenmiş export klasörü + GPU ölçümü ister). Donanım yokken çalışılabilecek
> yazılım kuyruğu → **§3.6 (`DK-1…DK-14`)**. Sıra kuralı: donanım geldiğinde **P-2/P-6
> önceliklidir**, çünkü pilotu açan yol odur; §3.6 onu beklemez.
>
> **Bu bölüm aşağıdaki "v8.0.0 TURU" bölümünün YERİNE GEÇER.** Gerekçe: 2026-08-02'de
> yapılan çok dilli motor araştırması (18 ajan, EN+ZH+ES, resmi üretici dokümanı +
> hakemli kaynak, çürütme turlu) iki temel varsayımı çürüttü. Eski bölüm **tarihsel
> kayıt** olarak aşağıda duruyor; iş listesi ARTIK BURASIDIR.
>
> 🔴 **Bağlam değişti:** Kullanıcının elinde **DJI M3M ile yapılmış ilk uçuşun
> görüntüleri var** ve demo uçuşları **birkaç gün içinde** başlıyor. Pilot mahsulü
> `grape` (crop_readiness: stage1/2/3 = pilot, data_status = **strong** — en güçlü mahsul).

### 🔬 ARAŞTIRMA BULGULARI — üç çürütülmüş varsayım

#### AV-1 · İki motorun da YEREL CLI'ı YOK (ölçüldü, 3 dil, 8+ terim)

| | Pix4Dfields | DJI Terra |
|---|---|---|
| Yerel CLI / headless | **YOK** — doküman merkezinin 10 bölümü, SSS, sürüm notları 2.8→2.13.2 (son: 2.13.2, 2026-07-13), girdi/çıktı belgesi: sıfır atıf. Yalnız Windows/macOS GUI | **YOK** — V5.3.0 kılavuzunun 70+ sayfası tarandı; `command line`/`CLI`/`API`/`script`/`batch`/`headless` geçen sayfa yok |
| Programatik yol | **Ayrı ürünlerde:** Pix4D**mapper** CLI (`-c -r`, belgeler Pix4D tarafından *obsolete* işaretli, **Pix4Dengine Server lisansı şart**) · Pix4D**engine** SDK (`pix4dvortex`, Python, Linux/Win — fotogrametri çekirdeği, Fields'ten hiç bahsetmiyor) · Pix4Dengine **Cloud API** (REST, AWS S3) | **TerraAPI** (bulut REST, HMAC-SHA256) — **Haziran 2026'da kapatıldı**; zaten *"real-time 2D/3D, control points, **agricultural applications**, cluster computing"* İÇERMİYORDU (resmi FAQ). Halefi **FlightHub Mapping API** — o da bulut |
| Air-gap (M1) uyumu | Hayır | Hayır — TerraAPI *"users need upload images to the internet"*, özel kurulum DESTEKLEMİYOR |
| Lisans kısıtı | Floating; eşzamanlı oturum sınırı paralel otomasyonu kısıtlar | Agriculture sürümü: 2D tarla/meyve ✅ 2D multispektral ✅ · küme ✗ |

> ⚠️ Üçüncü-parti bir pazarlama sitesinin (aidoos.com) *"Pix4Dfields REST API sağlar"*
> iddiası **YANLIŞ** — Pix4D'nin hiçbir resmi kaynağında yok. Planlamada kullanılmaz.
>
> 🔴 **Sonuç: `edge/src/core/services/calibration_gate/pix4d_runner.py` VAR OLMAYAN bir
> CLI'a subprocess açıyor.** Argüman dizisi (`--project --template --input --headless`) ve
> çıktı adları (`ortho.tif`/`ndvi.tif`) uydurma. Dosya kendisiyle de çelişiyor:
> satır 86 *"filenames verified on M1 during smoke test"* diyor, satır 229
> *"will be smoke-tested on M1 once the CLI is installed"* diyor — M1 hiç alınmadı
> (KG-0.e), `PIX4D_CLI_PATH=""`. **Bayat beyan sınıfının bir üyesi daha.**

#### AV-2 · İki motorun kalibrasyon çıktısı AYNI ANLAMDA DEĞİL

| Panelsiz M3M | Pix4Dfields | DJI Terra |
|---|---|---|
| Güneş sensörü | EXIF'ten **otomatik** okur; *"only the correction type 'Sun Irradiance' can be applied"* (sensör yönelimi üretici tarafından verilmediği için güneş **açısı** düzeltmesi yapılamıyor) | Kılavuzun **302 JS parçası** grep'lendi: `sunlight sensor`\|`irradiance`\|`sun sensor`\|`light compensation` → **0 eşleşme**. Kullanıp kullanmadığı **belgelenmemiş** |
| Radyometrik düzeltme KAPALI | (her zaman uygular) | 🔴 Çıktı **DN (dijital sayı)** — reflektans değil |
| Radyometrik düzeltme AÇIK | Panel: yalnız **Micasense + Sentera** uyumlu (**Parrot UYUMSUZ**) | 1–3 panel grubu; her bant katsayısı **elle** girilir, panel sınırı fotoğrafta **elle** işaretlenir |
| Panelsiz geçerli indeks | Yalnız kendi-normalize olanlar: **NDVI, NDRE, GNDVI, LCI, BNDVI, VARI, SIPI2**. TGI vb. **geçersiz** | Aynı matematik |

**Bağımsız doğrulama:** DJI'nin kendi *Mavic 3M Image Processing Guide v1.0* (2023.08) Eq. 4-6
matematiksel olarak gösteriyor: `NIR_ref = (NIR_cam × pCam)/(NIR_LS × pLS) × ρ_NIR`; **ρ_NIR
metaveride YOK** ⇒ panelsiz mutlak reflektans türetilemez, katsayı yalnız oranlı indekslerde
sadeleşir. Pix4D de M3M'i *"not fully radiometrically calibrated, only a relative calibration"*
diye sınıflıyor. ⇒ **E13-R'nin `RELATIVE` kararı iki bağımsız üretici kaynağıyla doğrulandı.**

#### 🔴 AV-3 · YENİ DELİK — `calibration_type` türetmesi MOTORU görmüyor

E13-R türetmeyi **yalnız drone'dan** yapıyor (`capabilities[drone_type].calibration_class`).
Ama AV-2 ölçtü: **aynı M3M uçuşu**, DJI Terra'da *radyometrik düzeltme kapalı* işlenirse
çıktı **ham DN**'dir. Sistem yine `RELATIVE` yazar → NDVI eşikleri ham DN'e uygulanır →
tarlada yanlış agronomik karar.

**Bu, S1 fail-open bulgusunun birebir aynı sınıfı** (`x-normalization.x-superseded-2026-07-31`
neden ham DN'in `PANEL_ABSOLUTE`'a yükselmesinin KRİTİK olduğunu zaten yazıyor) — sadece
başka kapıdan giriyor. Türetme artık **iki girdili** olmalı:

```
calibration_type = f(drone_capability_class, engine_radiometric_mode)

  relative + PANEL              → RELATIVE      (panel + göreli sensör)
  relative + SUN_IRRADIANCE     → RELATIVE      (Pix4Dfields varsayılanı)
  relative + NONE (ham DN)      → NONE          🔴 HARD REJECT — bugün RELATIVE yazılıyor
  absolute + PANEL              → ABSOLUTE / PANEL_ABSOLUTE
  absolute + NONE (ham DN)      → NONE
```

#### AV-4 · Çıktı yapıları — adaptörün normalize etmesi gerekenler

| | Pix4Dfields | DJI Terra |
|---|---|---|
| Kök dizin | Export hedefi (kullanıcı seçer). Veri deposu `C:\Users\<USER>\Pix4Dfields` altındaki **Capture/Data/Log/Temp'e YAZILMAZ** (resmi uyarı: veri kaybı) | `C:/Users/<PC>/Documents/DJI/DJI Terra/<hesap>/<görev>/map/` |
| Ortomozaik | Export edilen katman adı = **proje adı** (1.12+; 2.12.1'de özel karakterler kaldırıldı) | `result.tif` (RGB) |
| Bant rasterları | **Tek raster yığını** (Mapper'ın aksine bantları birleştirir) | `result_XXX.tif` — XXX = bant adı |
| İkili dosya kuralı | 🔴 Her katman **İKİ dosya**: `.tif` (sahte-renkli RGB, sıkıştırılmış, **görüntüleme**) + `.data.tif` (gerçek spektral veri, sıkıştırmasız, **analiz**) | 🔴 İki dizin: `map/index_map/` (**sayısal**, analiz) + `map/index_map_color/` (renkli, *"cannot be directly analyzed"*) |
| Reflektans haritası | Otomatik değil — Index generator > *Create custom index* ile **bant bant elle** üretilir | Radyometrik düzeltme açıkken otomatik |
| Rapor | PDF/CSV (`layer-statistics.csv`) | `map_report.json`, `AT/report/sfm_report.json` (**betikle eşik denetimine uygun**) |

> ⚡ **Her iki motorda da yanlış dosyayı okumak sessiz felakettir:** `.tif` yerine
> `.data.tif`, `index_map` yerine `index_map_color` okunursa sayılar anlamsızdır ama
> hiçbir kapı bunu yakalamaz. Adaptörün ilk görevi bu ayrımı zorlamaktır.

#### AV-5 · M3M çekim gerçekleri (intake kapısına girecek)

* Her çekim = **1 RGB + 4 multispektral TIFF** (grup başına 5 foto; P4M'de 6 — karıştırılmamalı).
* 🔴 **Sonek-0 fotoğrafı gerçek-zamanlı NDVI önizlemesi ise yeniden yapılandırma BAŞARISIZ olur.**
  DJI birebir: *"如果是实时 NDVI 照片而非可见光照片，将无法处理成功"*. Bu bir **intake kapısı** olmalı —
  bugün yok, ve saha operatörünün kamera ayarına bağlı.
* XMP `drone-dji` alanları ölçülebilir kalite sinyali taşıyor:
  `LS_status` → **0** = geçersiz (USB dongle takılı) · **1** = geçerli · **2** = geçerli + telafi ediyor.
  Ayrıca `Irradiance` (telafili), `SunSensor` (telafisiz), `RawData` (4 bandın hamı),
  `SunSensorYaw/Pitch/Roll`, `IrradianceGain` (sabit 64).
  ⇒ **Güneş sensörünün o uçuşta gerçekten çalıştığı ölçülebilir.** Bugün ölçen kapı yok.
* Ham TIFF'ler vinyetleme/distorsiyon düzeltmesi **UYGULANMADAN** kaydediliyor
  (`Vignetting Flag` sabit 0); katsayılar metaveride, uygulaması işleme yazılımına ait.

### 🏗️ TASARIM KARARI — **Motor-agnostik ÇIKTI ADAPTÖRÜ** (runner değil)

AV-1 nedeniyle "iki CLI koşucusu, ortak arayüz" tasarımı **imkânsız**. Kullanıcının
istediği *"ikisini de istediğim zaman ayrı ayrı kullanayım"* hedefi şu şekilde karşılanır:

```
Operatör (GUI)                    Edge (otomatik)
─────────────                     ───────────────
Pix4Dfields VEYA DJI Terra   →    ① motor tespiti (dizin imzasından)
elle çalıştırır, export eder  →   ② artefakt normalizasyonu (.data.tif / index_map)
                                  ③ radyometrik kip tespiti (panel / sun-irradiance / DN)
                                  ④ calibration_type = f(drone_class, radiometric_mode)
                                  ⑤ calibrated_dataset_manifest.json YAZ
                                  ⑥ mevcut hard gate (calibrated_validator) devralır
```

**Neden bu doğru tasarım:** ① GUI adımı zaten kaçınılmaz (iki motorda da) — tasarım tercihi
değil, ölçülmüş kısıt. ② Adaptör doğal olarak motor-agnostiktir; üçüncü bir motor (Metashape)
eklemek yeni bir adaptör sınıfıdır. ③ **ENGEL 1'i (kalibre manifest yazıcısı yok) aynı hamlede
kapatır.** ④ Sözleşme değişikliği GEREKTİRMEZ: `calibrated_dataset_manifest.v1` hem üst düzeyde
hem `calibration_result` içinde `tool_name` + `tool_version`'ı **zaten zorunlu** tutuyor ve
**enum kısıtı yok** — motor kimliği için hazır yuva var.

**KR-034 güncellenmeli:** *"Pix4Dfields drone-agnostik (yedek yazılım yok)"* →
*"Motor-agnostik: desteklenen motorlar Pix4Dfields ve DJI Terra; motor kimliği manifestte
`tool_name` ile taşınır."*

### ✅ C-1 · C-2 · C-3 KAPANDI (2026-08-02, kullanıcı onayı) — çapraz depo sözlük hizası

> **Neden bu üçü ayrı bir kalem oldu:** motor adaptörünü yazarken `RadiometricMode`
> kavramını **edge deposunda uydurdum**. Ölçüldü: kanonik sözlükte karşılığı yoktu.
> Bu, worker CLAUDE.md §2.1'in açık ihlali — *"platform otoriter kaynaktır; tüketici
> VENDOR'lar, asla kendi uydurmaz"*. Geri alındı.

| # | Yapılan | Kanıt |
|---|---|---|
| **C-1** | `enums/radiometric_mode.enum.v1.json` **kanonik** olarak yazıldı (PANEL · SUN_IRRADIANCE · RAW_DN, fail-closed varsayılan + ölçüm kanıtları). `calibration_type.enum.v1.json → x-derivation`'a **`x-radiometric-axis-2026-08-02`** eklendi: 6 gözlü makine-okunur tablo + 4 değişmez | `tests/test_radiometric_axis.py` (11 test) · `validate.py` **164 → 165 dosya / 0 hata** |
| **C-2** | KR-034 + KR-030 normatif metni **motor-agnostik** yapıldı; ayrıca *"iki motorun da yerel CLI'ı yoktur → motoru subprocess ile süren tasarım yazılmamalıdır"* ve *"radyometrik düzeltme opsiyonel olabilir → ham DN"* notları eklendi | Çapraz-repo SSOT (contract + platform + worker) `sync_kr_corpus.py --check` → **IN_SYNC** (3 hedef). ⚠️ Araç `--apply`'ı bloke etti (satır-kümesi sezgisi "değiştirildi"yi "silindi" sanıyor); birleştirme elle yapıldı ve `git diff` ile **8+/3−, kayıp yok** diye doğrulandı |
| **C-3** | Edge artık türetme tablosunu **kanonikten YÜKLÜYOR** (hardcode kaldırıldı). İki enum `interface/contracts/enums/`'a vendor'landı; `verify_contracts_hashes.py` kapsamı **8 → 10 artefakt**a genişletildi; contract `test_vendored_parity` MIRROR listesine kaydedildi | Edge **985 passed / 0 failed** · ruff temiz · hash pin OK · contract parite **169 passed** |

**Kapı kanıtı: 8/8 mutasyon KIRMIZI** — ham DN'i reflektans say · tabloda göz sil · kip
anahtarını yeniden adlandır · tabloyu E13-R `allowed` kümesiyle çeliştir · kanonik enum'a
beyansız kip ekle · vendored kopyayı ayrıştır (iki yönde) · Python enum'unu ayrıştır.
Geri yükleme doğrulandı.

**Bu turda üç kapı BENİ yakaladı** (hepsi düzeltildi — kapılar çalışıyor):
`test_build_profiles_ownership` (yeni modüllere M1/M2 ataması yapmamıştım) ·
`test_vendored_parity` (vendored dosya ekledim, parite listesine yazmadım — hata mesajı
ÖD-2 dersini hatırlattı) · `test_all_eight_schemas_pinned` (sabit sayı kilidi; sayıyı
büyütmek yerine değişmez **üretecin kendisiyle** yeniden yazıldı + boş-glob kapısı eklendi).

**Tur içi beklenen tek kırmızı:** `test_real_repo_checksum_verifies` — agrega checksum
bayat (dosyalar değişti), C8 töreninde `pin_version.py` ile kapanır. Ayrıca
`test_detector_accepts_a_git_ref` kırmızı ama **temiz HEAD klonunda da kırmızı** (ölçüldü,
`git clone --local` yöntemiyle) → yerel Windows kodlama sorunu, bu turdan bağımsız.

### 📋 GÜNCELLENMİŞ İŞ SIRASI

| # | Kalem | Depo | Gerekçe / kanıt |
|---|---|---|---|
| **P-1** 🔴 | **Motor adaptör katmanı** — `CalibrationEngineAdapter` protokolü + `Pix4DFieldsAdapter` + `DJITerraAdapter` + normalize `EngineOutput` | edge | AV-1/AV-4. `pix4d_runner.py` **kaldırılır** (var olmayan CLI) |
| **P-2** 🔴 | **`CalibratedManifestWriter`** — adaptör çıktısından şema-geçerli `calibrated_dataset_manifest.json` üretir | edge | ENGEL 1: bugün **0 yazıcı** var; `_read_calibration_type` bu dosyayı okuyamayınca paket reddediliyor |
| **P-3** 🔴 | **Radyometrik-kip duyarlı türetme** — `calibration_type = f(drone_class, engine_radiometric_mode)`; ham DN → `NONE` | contract + edge | AV-3. Bugünkü tek-girdili türetme ham DN'i `RELATIVE` sayıyor |
| **P-4** | **Canlı çağrı noktası** — `build_calibration_pipeline` → API/orkestratör bağlantısı | edge | `pipeline_factory.py` docstring: *"live call site stays gated on hardware"*; `.run()` üretimde **0 çağrı** |
| **P-5** | **M3M intake kapıları** — sonek-0 NDVI önizleme reddi + `LS_status` okuma + grup bütünlüğü (5 foto) | edge | AV-5. Üçü de bugün ölçülmüyor |
| **P-6** | **ENGEL 3 ölçümü** — M3M'in sıfır-Blue'sunun `grape_lr_v1` güven skorlarına etkisi | worker | Tek eğitilmiş artefakt `EXTENDED_5BAND`; `feature_extraction.py:164` Blue'yu sıfırlıyor, `StandardScaler` gerçek Blue ile fit'lenmiş |
| **v7.5.0** | S7-b (`band` zorunlu, `accepts` beyanlı) · **S3-b** (`DLS2_RELATIVE`'i `edge/intake_manifest` alt-kümesinden çıkar) · K1 (opak tenant) · bayat AK-11 cümlesi · **KR-034 metni** | contract | Hepsi ölçülmüş **0 üretici** → beyanlı MINOR. `propagate_vendored.py` + `release_gate` ilk kez geri-alınabilir turda koşar |
| **Kuyruk** | W8-c (`_DEFAULT_STRATUM_RATE = 0.0`) · W8-b · P21 · P20 · Ö7 | worker/platform | Pilotta denetim örneklemesi ölü olmasın |
| **v8.0.0** | Yalnız **DEP-1** kaldı | contract | S3 MINOR'a indi, K1 MINOR'a indi, S7-b zaten MINOR ⇒ tek başına tur açtırmaz |

> **S3 kararı ÇÖZÜLDÜ (ölçümle):** `x-derivation.map`'in tamamı iki anahtar
> (`relative`→`[RELATIVE]`, `absolute`→`[ABSOLUTE, PANEL_ABSOLUTE]`) ⇒ **`DLS2_RELATIVE`
> matristeki HİÇBİR drone için türetilemez**; `relative` için açıkça `forbidden`.
> Yalnız dış veri kümesi etiketi olarak yaşıyor (`calibration_input_parser.py:29-31`,
> Kazakistan buğday seti). **Genel bir ada çevirmek (`IRRADIANCE_RELATIVE`) M3M'i ince
> ayardan uzak tutan tek engeli kaldırır** — enum'un kendi `forbidden.why` bloğu bu
> deliğin üç zinciri nasıl bozduğunu zaten yazıyor. ⇒ **Yeniden adlandırma YAPILMAZ.**
> Yapılacak: değeri "yalnız içe aktarılan veri seti etiketi" diye beyan et + intake
> alt-kümesinden çıkar (daraltma = `ENUM_CONSTRAINT_ADDED` → `x-compat-accepted` ile MINOR).

### 📌 KULLANICININ ÖLÇMESİ GEREKENLER (araştırmanın kapatamadığı)

Bunlar **kendi kurulumunuzda** ölçülür, kaynaktan öğrenilemez:

1. `pix4dfields.exe -h` / `--help` herhangi bir bayrak kabul ediyor mu? (Resmi belge sessiz;
   ihtimal düşük ama ölçüm ucuz. Kabul ederse P-1 tasarımı değişmez, sadece opsiyonel bir
   tetikleyici eklenir.)
2. Pix4Dfields **export klasöründeki** gerçek dosya adları (proje adı kuralı doğrulanmalı).
3. DJI Terra hangi lisansta? (Agriculture = 2D multispektral ✅ ama küme ✗)
4. M3M kartındaki sonek-0 fotoğrafları **görünür ışık mı, gerçek-zamanlı NDVI mi?**
   (NDVI önizlemesiyse Terra yeniden yapılandırması **başarısız olur** — kamera ayarı.)
5. Panel var mı? Varsa Micasense/Sentera mı? (Parrot Pix4Dfields'te **uyumsuz**.)

---

## ▶️ (KALDIRILDI 2026-08-11) v8.0.0 TURU — ÖLÇÜLMÜŞ İŞ PLANI (2026-08-02 gecesi)

> **Bu bölüm 132 satırdı ve kendisi zaten *“ARTIK İŞ LİSTESİ DEĞİLDİR”* diyordu.**
> 2026-08-11'de kaldırıldı. **Hiçbir iş kalemi kaybolmadı — ölçüldü:** bloktaki 28 kalem
> kimliğinin **hiçbiri** yalnız orada geçmiyordu (`kimlik ∈ blok − blok_dışı` = **0**).
> Nereye devredildiği:
>
> | Blokta olan | Bugün nerede |
> |---|---|
> | S3 · S7-b · K1 kalemleri | **§14.5 KADEME 5** tablosu (üçü de ⬜ olarak izleniyor) |
> | S3 kararının çözümü | **§▶️ GİRİŞ NOKTASI** — `x-derivation.map` ölçümüyle çözüldü |
> | DEP-1 (penceresi dolmuş 2 ödeme nesnesi) | **§▶️ GİRİŞ NOKTASI** → `v8.0.0 \| Yalnız DEP-1 kaldı` |
> | *Turdan BAĞIMSIZ kuyruk* 6 kalemi (W8-b · P21 · P16 · W8-c · Ö7 · P20) | **§14.9** (aynı altı satır orada da var) |
> | ÖD-0 sürüm-riski lensi kapanışı | `denetim/denetim_raporu_2026-08-01_gece_od0_surum_riski_lensi.md` |
> | v8.0.0 9 adımlık tur töreni | `docs/checklists/SDLC_GATES.md` §3G + `docs/versioning_policy.md` §Release |

---

## 14.8 🔬 ÖZ-DENETİM SONRASI SIRALI İŞ LİSTESİ (2026-08-01 · **SONRAKİ OTURUM BURADAN BAŞLAR**)

> Kaynak: `denetim/denetim_raporu_2026-08-01_ozdenetim_6lens.md` (6 lens · 51 ham bulgu).
> ⚠️ O rapor **kanıt arşividir, iş listesi değildir**; yapılacak işler **yalnız burada** tutulur.
>
> **Denetimin bilinen sınırı — bunu bilerek oku:** 109 ajanın 69'u oturum kotasında düştü;
> `sürüm-riski` lensi hiç koşmadı ve çürütme turu yarım kaldı. Aşağıdaki **ÖD-1/2/3 elle
> doğrulandı**; ÖD-4 ve sonrası **doğrulanmamıştır** — her birinin ilk adımı "önce ölç".

> ### ✅ 2026-08-01 (ikinci oturum) — **ÖD-1 · ÖD-2 (contract yarısı) · ÖD-3 · ÖD-8 KAPANDI**
> Dedektör: **3 değişiklik / 0 breaking** (MINOR) · süit **1172 passed / 0 skip / 2 beyanlı xfail**
> · validate **96 dosya / 0 hata** · dist yeniden üretildi · **26 mutasyon 26 kırmızı**.
> Kanıt: `denetim/denetim_raporu_2026-08-01_od1_od2_od3_od8.md`.
> 🔴 **ÖD-2'nin WORKER yarısı AÇIK → `W13`** (aşağıda): kanonik düzeldi, ama worker gelen işi
> **kendi vendored kopyasına** karşı doğruluyor (`job_handler.py:136`) ve o kopya hâlâ 4 alanlı
> → `scale` taşıyan iş **worker'ın kapısında** düşer. Zincir W13 kapanana kadar ölü.

### 🔴 ÖNCE — elle doğrulanmış, kanıtlı (bu üçü aynı kök nedene bakıyor)

| # | Kalem | Kanıt (ölçüldü) | Ne yapılacak |
|---|---|---|---|
| ✅ **ÖD-1** | **Enum kayıt defteri ile şemanın inline enum'u ayrışık — ve hiçbir kapı ikisini bağlamıyor.** `enums/calibration_type.enum.v1.json` → `x-context-subsets['edge/calibrated_dataset_manifest']` = `[ABSOLUTE, RELATIVE, PANEL_ABSOLUTE]` **ama** `schemas/edge/calibrated_dataset_manifest.v1.schema.json` → `/properties/calibration_result/properties/calibration_type.enum` = `[ABSOLUTE, RELATIVE]`. **⇒ C6b/S2 kararı FİİLEN UYGULANMADI:** `PANEL_ABSOLUTE` taşıyan belge bugün hâlâ reddedilir | Şema ile defter ayrı yerlerde; bu D16'nın kapattığı "ikili gerçek" deseninin **şema tarafındaki** hâli | ① Şemanın inline enum'unu deftere hizala (C6b'yi gerçekten uygula) ② **Sınıf kapısı yaz:** her bağlam için defter ↔ inline enum eşitliğini zorlayan test (5 bağlamın hepsi) ③ Mutasyonla doğrula |
| ⚠️ **ÖD-2** (contract ✅ · worker ⬜ **W13**) | **S5 + W12 TEL ÜSTÜNDE ÖLÜ.** `schemas/worker/analysis_job.v1.schema.json` → `$defs/CalibrationMetadata` props = `[calibration_panel_id, calibration_timestamp, calibration_type, irradiance_sensor]`, `unevaluatedProperties: false`. `scale` **yok** → `jsonschema.validate` ile ölçüldü: *"Unevaluated properties are not allowed ('scale' was unexpected)"*. Yani platform bir işe `scale` koyarsa **şema reddeder**; worker'ın W12'de yazdığı okuma kodu asla veri görmez | `worker/calibration_metadata.v1.schema.json` güncellendi ama **işin taşıyıcısı** `analysis_job.v1`'in kendi `$defs` kopyası güncellenmedi — aynı kavramın iki şema tanımı var | ① `analysis_job.v1 → $defs/CalibrationMetadata`'ya `scale` ekle (ve `calibration_method` — S4 aynı delikten düşüyor olabilir, **ölç**) ② İki tanımın ayrışmasını yasaklayan kapı yaz ③ Uçtan uca doğrula: örnek job belgesi `scale` ile valide olmalı |
| ✅ **ÖD-3** | **E13/C6b kapıları yalan yeşil.** `tests/test_calibration_type_axis.py:60` `_calibrated_subset()` yalnız `x-context-subsets`'i okuyor; şemanın inline enum'una **hiç bakmıyor**. Aynı desen `tests/test_calibrated_manifest_fields.py`'de de var | Kararın değeri (`ABSOLUTE`) şemadan silinse kapı yeşil kalır — kapı korduğunu iddia ettiği yüzeyi ölçmüyor | ÖD-1'in kapısı bunu da kapatır; ayrıca bu iki test dosyasındaki **tüm** `x-context-subsets` okumalarını gözden geçir: hangisi şemayı da ölçmeli? |

### 🟠 SONRA — denetimden çıkan, **önce doğrulanacak** bulgular

| # | Kalem | İlk adım |
|---|---|---|
| ✅ **ÖD-4** | Worker vendored kopyası yayımlanmış v7.3.0'ın **önünde** olabilir (beyansız AK-4/I-5 sapması) | ✅ **DOĞRULANDI (16 dosya `git show v7.3.0:<yol>` ile karşılaştırıldı).** İki sınıf çıktı: **(a) beyanı eksik geçici sapma** — `calibration_metadata.v1` (`scale`, W12 turunda vendor'lanmış, devir spesi yoktu) + bu turda `analysis_job.v1` → ikisi de artık worker `denetim/scale_wire_devir_spec_2026_08_01.md` ile beyanlı, C8'de uzlaşır. **(b) gerçek borç** — `expert_labeling_card` `EGE` ve `expert_review_queue` meyve ağaçları → **W14**. ⚠️ Yanlış pozitif uyarısı: edge `intake_manifest`/`scan_report`/`transfer_batch` "üst düzey alan fazlası" gösterir; bu **yapı farkıdır** (kanonik `oneOf[$defs]`, vendored düz) — yeni parite kapısı SUBSET kipinde bunu doğru sayıyor, bir sonraki denetim yeniden bulgu yazmasın |
| ✅ **ÖD-5** → **E13-R** | E13 kararı `data/drone_capability_matrix.yaml` ile çelişebilir | ✅ **ÖLÇÜLDÜ, ÇELİŞKİ GERÇEK, KARAR GERİ ALINDI (2026-08-01, koordinatör onayı).** Üç kanonik kaynak da E13'ün tersini söylüyordu: matris `DJI_MAVIC_3M.calibration_class: relative` · SSOT `:79` ve `:1014` *"Pix4Dfields, M3M için tam radyometrik kalibrasyon DEĞİL, göreli kalibrasyon sağlar"* · platform `calibration_class.py:41` `DJI_MAVIC_3M: RELATIVE` (2.0× tolerans buna bağlı). Sonuç ölçüldü: sabit `ABSOLUTE` yazılsaydı worker `FINETUNE_ALLOWED_CALIBRATIONS` (`enums.py:73`) M3M verisini **ince ayara uygun** sayacaktı → K-3 sessizce delinirdi. **Yeni kural:** değer `capabilities[drone_type].calibration_class`'tan türetilir (`relative→RELATIVE` · `absolute→ABSOLUTE/PANEL_ABSOLUTE`), makine-okunur blok `enums/calibration_type.enum.v1.json → x-derivation`, kapı `tests/test_calibration_type_derivation.py` (14 test, **8/8 mutasyon**). E13'ün `DLS2_RELATIVE` reddi **ayakta**. 💰 **Kabul edilen bedel yazılı:** demo/pilot filosu M3M olduğu için M3M verisi ince ayara girmez, yalnız SSL ön-eğitimine girer |
| ⚠️ **ÖD-6** → **P14** | Platform'da S1 fail-open (`CALIBRATED → PANEL_ABSOLUTE güvenlik-ağı`) **hâlâ canlı** olabilir (`worker_job_publisher.py:80-84`) — E13'ün "panel kanıtı" zincirini deler | ✅ **ÖLÇÜLDÜ: CANLI.** `worker_job_publisher.py:80-84` → *"3. status CALIBRATED → PANEL_ABSOLUTE (güvenlik-ağı)"* aynen duruyor; 4. adım zaten `NONE` üretiyor. **P14 ile birleştirildi** (kalem zaten açık, gerekçesi artık iki kez ölçülmüş). 🔴 **E13-R bu kalemi ACİLLEŞTİRDİ:** artık M3M paketleri `RELATIVE` taşıyacak; platform tipi boş bırakan bir pakette `PANEL_ABSOLUTE` yükseltmesi yaparsa **göreli veri mutlak etiketle** worker'a gider ve K-3 tam da bu yoldan delinir |
| ✅ **ÖD-7** | SD8 nüfusu eksik ölçülmüş olabilir: `2.0.1 / 2.1.0 / 4.1.2` sürümleri `CONTRACTS_VERSION.md`'ye yazılmış ama etiketsiz | ✅ **DOĞRULANDI VE KAPATILDI.** Ölçüm biçimden bağımsız yapıldı (dosyanın her commit'indeki başlık blob'dan okundu — SD8 sabit `## Version:` biçimine bakıyordu, bu üçü farklı biçimde yazılmış ve sayıma **hiç girmemişti**; D2'deki KR-çıkarıcısı dersinin aynısı). Nüfus **22 sürüm**, etiketsiz **3**. Yöntem önce **19/19 etiketli sürümde** doğrulandı (ölçümün bulduğu commit = mevcut tag'in commit'i), sonra üç annotated retro-tag atıldı ve push'landı: `v2.0.1`(f77f62d8) · `v2.1.0`(6b802fd8) · `v4.1.2`(fb021e3e). **I-2 artık 22/22 tutuyor**; tek kayıtlı istisna `2.0.2` (CONTRACTS_VERSION.md'ye hiç yazılmamış → release commit'i ölçülemez) |
| ✅ **ÖD-8** | Vendored parite kapısı `$defs`'e kör ve 16 vendored dosyanın yalnız **9'unu** izliyor — S5 boşluğu tam bu delikten geçti | ✅ **YAPILDI (2026-08-01).** Kapsam 16/16; **iki kip** tanımlandı — MIRROR (yapı özdeş → `properties`+`required`+**her pointer'daki enum** eşit) · SUBSET (vendored dar alt küme: eksiklik normal, **çelişki değil**). Eklenen üç kural: ortak `$defs` çelişemez · **kapalı** vendored form kanonik alanı atlayamaz (ÖD-2'nin tam kuralı) · her vendored dosya izlenmek zorunda. **Kapsamı ölçülmeyen kapı olmayan kapıdır:** ilk koşuşta **5 yeni gerçek sapma** buldu (aşağıdaki W13/W14/E16-b) |
| ✅ **ÖD-9** | Sınıf 1 (kodlamasız dosya okuma) tek depoya tarandı — dört depoda çok daha fazla üye olabilir | ✅ **DÖRT DEPO TARANDI (1.631 `.py`, grep değil **AST**).** Sonuç: sınıf **worker'a özgü** — contract **0** · edge **0** · platform **0** · worker `src/`+`scripts/` **12** gerçek üye. ⚠️ Ölçüm aracının kendi hatası da yakalandı: builtin `open(dosya, mod)` ile `Path.open(mod)` imzaları farklı (mod 2. ↔ 1. konum); ilk sürüm `p.open("rb")`'yi (contract `compute_contracts_sha256.py:33`) yanlışlıkla ihlal saydı. **W11 listesi düzeltildi:** `map_renderer.py:262,288` rasterio `MemoryFile.open()`'dır → **yanlış pozitif**; `safe_path.py:19` **docstring örneği** (kod değil, ama yanlış kalıbı öğretiyor). Gerçek `src/` üyeleri: `contract_validator.py:233` · `cold_storage_manager.py:263,293` · `ssl_pretrain.py:2131` (+8 `scripts/`) |
| ✅ **ÖD-10** | Sınıf 3 (vendored'a prose taşıma) kapanmadı — 16 vendored dosyanın 13'ü hâlâ şişkin olabilir | ✅ **ÖLÇÜLDÜ — VARSAYIM ÇÜRÜDÜ.** 16 dosyanın **0'ı** kanoniğinden fazla prose taşıyor; vendored toplam prose **37.336** karakter, kanonik **71.490** (≈%52 — kırpma fiilen yapılıyor). Vendored non-ASCII toplam 379 karakter (245'i `analysis_type.enum`'un Türkçe görünen adları = **veri**, prose değil). ⇒ Kalan risk yükte değil **okuyucuda**: kodlamasız `open()` (**W11**). Yine de olayın tam şekli yasaklandı: yeni kapı `test_vendored_prose_does_not_exceed_canonical` (16 çift) |
| ✅ **ÖD-11** | `D16-b2` kapısı işaretçi **damgasına** bakıyor: damga dururken altına çelişkili gövde yazılabilir | ✅ **KAPATILDI.** Eşik ölçümle seçildi: işaretçiler ≤1366, gerçek gövdeler ≥1483 karakter → sınır **1500**. Ayrıca işaretçi bir **hedef** göstermek zorunda (`TARLAANALIZ_SSOT` atfı). 2/2 mutasyon kırmızı |
| ✅ **ÖD-12** | "Göç taşımadır, silme değil" kapısı **başlık** sayıyor — normatif gövde silinse yeşil kalabilir | ✅ **KAPATILDI — ve kapı yazarken KENDİ körlüğüm mutasyonla yakalandı:** yardımcı yalnız *"daha uzunsa yaz"* diyordu, bu yüzden **boş gövdeler sözlüğe hiç girmiyordu** → gövdesi silinmiş bir KR kapının görüş alanı dışındaydı (KR-000 mutasyonu yeşil döndü). `setdefault` ile düzeltildi. Artık her gövde asgari uzunlukta olmalı (4 bölüm başlığı beyanlı: KR-010/012/020/060) + toplam hacim eşiği (ölçüm: 117.738 karakter) |
| ✅ **ÖD-13** | `dist/` yayın ağacı PII / validate / checksum kapılarının **kapsamı dışında**; yetim dosya denetimi yok | ✅ **KAPATILDI.** `validate.py` artık `dist/schemas/`'i de tarıyor (**96 → 164 dosya**) ve yayın kopyası kaynağının PII **kapsamını devralıyor** (aksi hâlde meşru `user_pii` ikizi "kapsam dışı" diye kırmızı verir). `inline_refs.py --check` artık **yetim** dosya arıyor (kaynağı silinen şema yayın ağacında yaşamaya devam eder; `--write` onu silmez). Yeni kapı: `tests/test_publication_tree_gates.py` |
| ⬜ **ÖD-14** → **P17** | Platform `main.py` sürüm sabiti sınıfı yarım süpürülmüş olabilir (log satırlarında `7.2.0` kalıntısı) | ✅ **ÖLÇÜLDÜ, GERÇEK (ama küçük):** `main.py:183` kodu doğru (`ContractsVersionPin("7.3.0")`), fakat `:186` ve `:188` **log satırları** hâlâ `pinned="7.2.0"` yazıyor — boot-halt incelemesinde ops'u yanlış sürüme yönlendirir. Ayrıca `worker_job_publisher.py:38` yorumu *"platform contract 6.1.0'e PİN'lidir"* diyor. **P17** olarak platform deposuna yazıldı (küçük, tek başına merge edilebilir) |
| ✅ **ÖD-15** | `SDLC_GATES.md` SD8'i hem "karar bekliyor" hem "kapandı" diyor olabilir (bayat blok) | ✅ **TEKİLLEŞTİRİLDİ.** Karar §3G'de **tek gövde** olarak yaşıyor; üstteki blok tarihsel kayda çevrilip ona işaret ediyor. §3G ayrıca ÖD-7'nin düzelttiği nüfus ölçümünü (19→**22** sürüm) ve dersini taşıyor |
| ✅ **ÖD-16** | CHANGELOG'da yayımlanan dedektör komutu çalışmıyor olabilir ("üreteci yayınla" ihlali) | ✅ **DOĞRULANDI VE DÜZELTİLDİ.** `--old v7.2.0` gerçekten `❌ Old directory not found` ile düşüyordu. Dedektör artık **git ref** kabul ediyor (geçici worktree + temizlik + `prune`); yayımlanan komut koşuyor (53 değişiklik / 0 breaking). Bir test CHANGELOG'daki **her** `--old` argümanının bugün çözülebilir olduğunu zorluyor |

### 📌 DENETİMİN KENDİSİNİN BORCU

| # | Kalem |
|---|---|
| ⚠️ **ÖD-0** | **`sürüm-riski` lensi hiç koşmadı** (API hatası). v7.3.0'ın yayımlanmış içeriği ↔ CHANGELOG örtüşmesi, migration-guide gereksinimi, ve **TUR 2 açıkken master'ı vendor'lama riski** denetlenmedi. Sonraki oturumda bu lens tek başına koşturulmalı.<br><br>⚠️ **KISMEN KAPANDI (2026-08-01, ikinci oturum — ajan turu DEĞİL, ELLE ölçüm):** üç sorunun üçü de doğrudan ölçüldü: ① **CHANGELOG örtüşmesi ✅** — dedektör `v7.2.0→v7.3.0` **45 değişiklik / 0 breaking** diyor ve CHANGELOG'un 7.3.0 bölümü kalemleri adıyla anıyor (`priority_zones` ×9 · `sorties` ×6 · `raw_frames` · `crop_type` · C0′/C1′/C2′/C3′ · C11 · AL-C1/C2 · D8) ② **migration guide ✅ gerekmiyor** (MINOR; politika yalnız MAJOR'da şart koşuyor) ③ **vendor'lama riski ✅** ÖD-4'te ölçüldü ve devir spesiyle beyanlandı. 🔴 **Bir yeni bulgu çıktı → SD9** (aşağıda). **Kalan borç:** çok-ajanlı lensin kendisi koşturulmadı (kullanıcı istemeden ajan turu açılmadı) — yukarıdaki üç soru dışında ne bulacağı bilinmiyor. |
| ✅ **SD9** → **KARAR VERİLDİ VE UYGULANDI (2026-08-01, koordinatör onayı)** | `info.version` artık **set sürümünü izliyor** (`1.0.0` → `7.3.0`, üç spec). Elle yazılmaz: `tools/pin_version.py → sync_openapi_versions()` C8 töreninde yazar; kapı `tests/test_publication_tree_gates.py` ölçer (**4/4 mutasyon** kırmızı). Dayanak: OpenAPI 3.1 alanı *"the version of the OpenAPI **Document**"* diye tanımlıyor ve bu depoda belge **set** olarak yayımlanıyor (I-1); "API MAJOR hattı" savunması düştü çünkü hat zaten `servers.url` (`…/v1`) + dosya adında yazılı; alanı okuyan tüketici yok (dört depoda 0 eşleşme) ⇒ geçiş kimseyi kırmadı |
| 🔴 **SD10** (yeni, aynı turda kapatıldı) | **OpenAPI lint kapısı HİÇBİR KURAL KOŞMUYORDU ve daima "pass" gösteriyordu.** Üç katman: `spectral lint` **ruleset'siz** (araç "No ruleset has been found" deyip çıkıyor) + `\|\| echo` + `continue-on-error: true`. Kurallar gerçekten koşturulunca **25 hata + 63 uyarı** çıktı. **Üç GERÇEK kusur** (üçü de düzeltildi): ① `api/components/responses.yaml` → `nullable: true` (**OAS 3.0** anahtarı; 3.1'de sessizce yok sayılıyor, istemci alanı **zorunlu string** sanıyordu) ② `api/edge_local.v1.yaml` → `/batches/{batch_id}/scan` yol parametresini **hiç tanımlamıyordu** ③ `platform_public.v1.yaml` ödeme uçlarında **var olmayan** `PaymentIntent` bileşenine iki sarkan `$ref` (KR-033). ⇒ Kapı **redocly**'ye çevrildi (spectral bu ağaçta çöküyor), susturucular kaldırıldı, `.redocly.yaml` + **beyanlı** `.redocly.lint-ignore.yaml` yazıldı; ayrıca araçtan bağımsız bir pytest `$ref` kapısı eklendi |
| ⬜ **SD11** (yeni) | **Kanonik şema/enum belgelerinin üst düzey `notes` / `metadata` anahtarları OpenAPI'de `struct` ihlali.** Ölçüldü: 23 ihlal / 12 dosya (`notes` ×16 · `metadata` ×7). OpenAPI 3.1 Schema Object uzantı mekanizması `x-` önekidir. Doğru çözüm `x-notes` / `x-metadata` göçü, **ama tek satırlık değil**: `metadata` bloğu KR-018 bant gereksinimlerini taşıyor (`analysis_type.enum.v1 → metadata.bandRequirements`) ve dört depoda okuyanları var → kendi turunu ister. Bugün **beyanlı** (`.redocly.lint-ignore.yaml`, liste yalnız küçülür) | SD10 |
| ~~🔴 SD9 (ilk kayıt)~~ | ~~**Üç OpenAPI spec'inin `info.version`'ı `1.0.0`'da DONMUŞ**~~ ve hiçbir kapı ölçmüyor. Ölçüldü: `api/platform_public.v1.yaml` içeriği `v7.2.0→v7.3.0` arasında değişti (D18-b: `info.contact.email` silindi) ama `info.version` aynı kaldı; `platform_internal` ve `edge_local` de `1.0.0`. `docs/versioning_policy.md` bu alan için **kural içermiyor** (yalnız "OpenAPI endpoint → 3 MINOR deprecation penceresi" satırı var). ⇒ Spec'ten istemci üreten bir tüketici, hangi sözleşme sürümüne baktığını `info.version`'dan **anlayamaz**. **Karar gerekiyor:** (a) `info.version` contract sürümünü izlesin (release adımı + kapı), ya da (b) *"bu alan API MAJOR hattını gösterir, bilerek sabittir"* diye **yazılı** beyan + kapı. Sessiz üçüncü seçenek (bugünkü hâl) ikisinin de faydasını vermiyor |
| **ÖD-0b** | Çürütme turu yarım kaldı (51 bulgunun 35'i skeptik gördü) ve workflow'un eleme mantığı "skeptiği düşen bulguyu ele" şeklinde çalıştı → **haksız elenen bulgu olabilir**. Ham liste denetim raporunda; ÖD-4…ÖD-16 oradan türetildi. |


---

## 14.11 🔬 D12/D13 TURU (2026-08-11) — `stress_ratio` tanımlandı · ön faz kapısı kuruldu · üç-repo 7.6.1

> **Tetikleyici:** `tarlaanaliz-worker/denetim/kalan_isler.txt` §4 **D12** — kanonik
> `analysis_type.enum` *"hiçbir üretici bu adı emit ETMEMELİDİR"* diyordu ama worker
> üretiyordu. Ölçüm iddiayı çürüttü ve asıl kusurun **başka yerde** olduğunu gösterdi.

### Kalemler

| Kod | Depo | İş | Durum |
|---|---|---|---|
| **D12-a** | contract | `indexDefinitions.stress_ratio`: `UNDEFINED_PENDING_DECISION` → **`DEFINED`**. `formula` + makine-okunur `domain_guard` (`valid_where: "NDVI > 0"`, `outside_value: 1.0`) + `measured_producers` (7 yol, `dosya:satır`) + `superseded_claim` (⛔ çürütme kaydı) + **`delivery_rule.preliminary=false`** | ✅ PR #62 |
| **D12-b** | contract | Kapı: `TestDerivedQuantitiesAreDefined` — `delivery_rule.preliminary` ile `report_phase → x-preliminary-content.stage_b.fields` **makine düzeyinde anlaşmak zorunda**; `proxy_only` katmanı besleyen indeks ön fazda teslim edilemez. **9 mutasyon** | ✅ PR #62 |
| **D12-c** | platform | **Asıl kusur:** KR-093 kapalı listesinin platformda **hiç tüketicisi yoktu** (`x-preliminary-content` → 0 eşleşme; pozitif kontrol: `x-derived-from` → 3). `preliminary_content_gate.py` listeyi **kanonikten okur**; kapı katman listesi + `available_indices` + raster tile ucu + tile metadata. Uzman/admin kapsam dışı. **7 mutasyon** (biri ayrıştırma: kapıyı uzmana uygula → 3 pozitif kontrol öldü) | ✅ PR #407 |
| **D12-d** | platform | Yan delik 1: konsensüs RED (`EXPERT_REJECTED`) sonrası özet ucu 409 derken **tile'lar servis ediliyordu** (taban görüntü dahil) → fail-closed | ✅ PR #407 |
| **D12-e** | platform | Yan delik 2: faz türetmesi `"FULL" if DONE else "PRELIMINARY"` idi; kanonik *"listelenmeyen = PRELIMINARY varsayımı YASAKTIR"* der → `CANCELLED`/`FAILED`/`ON_HOLD` artık 409, tek kaynak `derive_report_phase()` | ✅ PR #407 |
| **D12-f** | worker | **Kod DEĞİŞMEDİ (bilinçli).** `reporting_agent.py` + `src/indices/stress_ratio.py` başına "neden burada kalıyor" gerekçesi | ✅ PR #216 |
| **D13** | üç depo | Sürüm töreni **7.6.0 → 7.6.1**: contract re-pin + annotated tag · platform submodule + checksum + `main.py` boot-pin · worker vendored `analysis_type` v1.4.1 → v1.4.4 + KR-041 öz-hash | ✅ #62/#407/#408/#216 |
| **D13-b** | contract | **Öz-denetim bulgusu:** kardeş-CI parite kapısı `metadata` **değerlerine kördü** — hizaladığım ayrışmanın geri kaymasını engelleyen hiçbir şey yoktu. `TestVendoredMetadataDoesNotContradict`: vendored `metadata` paylaşılan bir yolda kanonikle **çelişemez** (I-4 gereği EKSİK tutabilir). 142 yaprak, **6 mutasyon** | ✅ PR #63 |

### Karar — neden seçenek (b) elendi

`reporting_agent._MAPS_BY_RESULT_MODE`'dan `stress_ratio`'yu çıkarmak **sızıntıyı
kapatmazdı**, iki ölçülmüş nedenle:

1. `result_mode` ⟂ `report_phase` (KR-093 §Faz ekseni bağımsızlığı). `report_phase`
   yalnız `mission.status`tan türetilir; **`FULL_REPORT` modundaki iş de uzman onayına
   kadar `PRELIMINARY` fazındadır** → raster yine üretilir, yüklenir, sunulurdu.
2. Kanonik `report_phase.enum → x-removed-2026-07-31.still_computable` worker'ın
   hesaplamaya devam etmesine **açıkça izin verir**; kısıt üretimde değil **sunumda**.
   Üstelik PARTIAL = düşük güven, yani uzmanın rastere en çok ihtiyaç duyduğu mod.

### 📌 Bu turda ölçülüp ÇÜRÜTÜLEN iddialar (tekrar gündeme gelmesin)

| İddia | Neden çürüdü |
|---|---|
| *"`stress_ratio`: ad var, üretim yok — hiçbir üretici emit etmemeli"* (kanonik v1.4.2–v1.4.3) | Ölçüm **yanlış dosyaya** bakmıştı (`compute_indices_v2`). Üretici çıkarım hattındadır; raster S3'e yüklenip `manifest.json`'da listeleniyor. "Şu dosyada yok" ≠ "hiçbir yerde yok" |
| *"Çözüm worker'ın teslim setinden çıkarmaktır"* (paralel oturumun D12 planı) | Yanlış eksen — `result_mode` ⟂ `report_phase`; FULL_REPORT yolunda sızıntı devam ederdi. Kanonik `still_computable` da tersini söylüyor |
| *"Çapraz-repo kapı YOK"* (benim ilk CHANGELOG cümlem) | Fazla genişti: kapı **vardı** (kardeş-CI paritesi) ama `metadata` değerlerine kördü. Düzeltildi; geçerli kalan sınır: contract deposu worker'ın **Python koduna** bakamaz |
| *"Etiket merge sonrası atılır"* | Worker CI contract'ı **pinli etikete** göre checkout ediyor; tag yokken iş `Checkout contract @ pinli etiket` adımında düşer. Tag, tüketici PR'ları CI'a girmeden push edilmeli |

### ⬜ Bu turdan AÇIK KALAN

| Kalem | Neden açık |
|---|---|
| ✅ **AL-K17** · ~~Kanonik `outside_value`/`formula` ile worker'ın Python sabitinin hizasını hiçbir kapı ölçmüyor~~ → **KAPANDI (2026-08-11, worker PR #217)** | Çözüm önerilen yoldan geldi: worker'da `TestStressRatioKanonikSozlesmeyeBAGLI` — beklenen değerler vendored kanonik JSON'dan **TÜRETİLİR** (kopyalanmaz), sonra üretim koduyla davranışsal sınanır. **7 mutasyon, iki yönde**: kodu bozunca 5'er test, sözleşmeyi bozunca (kod doğru kalırken) **yalnız yeni bağ testi** kırılıyor — ayrıştırma kanıtı |
| **AL-K18** 🟡 · Ön faz kapısı **canlı trafikte** doğrulanmadı | Ayakta yığın yoktu. Kabul ölçütü SESSION_HANDOFF §0.A/D-2'de yazılı (`summary` → `WATER_STRESS` yok · tile → 403 · `DONE` olunca 200) |
| **AL-K19** 🟢 · Yeni parite kapısı **yalnız worker CI'ında** koşar | Contract CI'da kardeş depo checkout edilmez (D4-b tasarımı, bilinçli). Edge çiftleri de meşru olarak atlanır |

---

## 14.12 🔬 CERRAHİ KALİTE TURU (2026-08-11) — alan sızması · sözlük bağlama · CI kapı dürüstlüğü

> **Kapandı:** contract PR [#69](https://github.com/physiscs-zana/tarlaanaliz-contract/pull/69)
> (master `d930bcc`) — 3 bulgu kapatıldı, **3 yeni kapı** kuruldu, **2 iddia ölçümle
> geri alındı**. Ayrıntı ve kanıt: `CHANGELOG.md` → `[Unreleased]` blokları.
>
> Kapatılanlar: ① alan sızması (19 şema / 27 düğüm; beyansız 28 → 1) ·
> ② `threat_type` kanonik sözlüğe bağlandı (KR-073) · ③ `paths:` 13 → 21 kök +
> `lint-openapi` özet kapısına.
>
> Yeni kapılar: `_check_object_policy` (validate.py, ağacın tamamı) ·
> `test_enum_binding_ratchet.py` (12 satırlık baseline) · `test_ci_gate_honesty.py`
> (filtre + `needs` TÜRETİLİR, ezberlenmez).

### ⬜ Bu turdan AÇIK KALAN

| Kalem | Durum / neden açık |
|---|---|
| ✅ **AL-K21** · ~~`quarantine_decision` sözlüğü SIFIR KESİŞİMLİ — karar gerekiyor~~ → **KAPANDI (2026-08-11, edge oturumu + kullanıcı kararı): BAĞLANMAYACAK** | Karar *"hangi sözlük kazanacak"* değil **kavram ayrımı** çıktı — benim çerçevem yanlıştı. edge `decision` (`{PASS, QUARANTINE, REJECT}`) AV1'in **EYLEM** kararı; kanonik `quarantine_decision.enum.v1` bir karantina kaydının **YAŞAM DÖNGÜSÜ DURUMU**. Sıfır kesişim uyumsuzluk değil, **iki ayrı eksenin aynı adı taşıması**. Üç ölçüm bağımsız doğrulandı: ① edge bu şemayı **vendor'lamıyor** (`interface/contracts/schemas/edge/` = 8 şema, `quarantine_event` yok) · ② karar platforma bu eksenden gitmiyor — `scan_report_writer._DECISION_TO_RESULT` onu `scan_report.v1 → result`'a eşliyor (PASS→PASS, QUARANTINE→QUARANTINE, REJECT→FAIL) ve `OperationalForm.result` enum'u zaten `[PASS, FAIL, QUARANTINE]` → **edge çıktısı kanoniğe TAM UYUYOR** · ③ `quarantine_events` tablosuna yazan/okuyan üretim kodu **yok** (yalnız DDL). **İleriye dönük kural:** edge bir gün yaşam döngüsü durumu yayınlarsa o **ayrı bir alan** olur (`lifecycle_state`) ve kanonik enum'a bağlanır — `decision` değil. Gerekçe hem kanonik şemaya hem edge `src/core/domain/quarantine_event.py` docstring'ine yazıldı |
| ✅ **AL-K22** · ~~Vendored kopyalarda 5 politika sapması — iki kapının da kör noktası~~ → **KAPANDI (2026-08-11, PR #71)** | İki ayrı hamleyle kapandı. ① **Worker oturumu** 5 düğümü hizaladı (ölçüldü: `tile_coordinates`·`pixel_bbox`·`drone_metadata`·`artifacts.items` KAPALI, `affected_zone` AÇIK) ve üreticileri kendi ölçtü — kritik ek bilgi: worker'ın **gelen doğrulaması BLOKLAYICI** (`feedback_handler.py:471-478`), yani sapma kozmetik değildi. ② **Contract'a kapı kuruldu**: `tests/test_vendored_policy_parity.py` — parite çiftlerinde iki tarafta da var olan her object düğümünün politikası karşılaştırılır, I-4 idiomu normalize edilir, `DÜĞÜM YOK` sapma sayılmaz; ratchet iki yönde, 3 yönde mutasyonla sınandı. **Kalan borç baseline'da 3 satır** (`analysis_result.v1` → `index_maps`·`model_metadata`·`thermal_results`) — üçü de bu turdan ÖNCE vardı, worker'a bildirildi. Kapı kardeş depo checkout'u ister (D4-b); kardeşsiz ortamda **beyanlı** atlanır (ölçüldü: 1345 / 1176+169, beyansız atlama yok) |
| **AL-K23** 🟡 · **`Detection.bbox` parite-kilitli istisna** | Kapatma denendi, **ölçümle geri alındı**: worker'da alan opak taşınıyor (`src/core/domain/analysis_result.py:29,249` → `dict[str, float] \| None`), anahtar kümesini kısıtlayan satır yok; ayrıca kanoniğe **herhangi bir** politika anahtarı koymak I-4 çelişkisi üretiyor (`_strip_annotations` iki idiomu tek anahtara indirger, `test_vendored_parity.py:262-265`). `tools/validate.py → _PARITY_LOCKED_OPEN` içinde tek girişlik istisna; `test_object_drift_gate.py` listenin büyümesini yasaklıyor. **Çıkış sırası: önce vendored kopyayı kapat, sonra istisnayı sil** |
| **AL-K24** 🟢 · **`paths:` filtresi tümden kaldırılsın mı?** | Filtre ölçülen kümeye genişletildi (13 → **24**; bu satır bir süre **21** yazıyordu, sonradan eklenen kökler işlenmemişti — 2026-08-11'de workflow'dan yeniden sayıldı) ve `test_ci_gate_honesty.py` ile kapıya bağlandı. Ama **her filtre bir fail-open yüzeyidir** ve bu tur tam olarak onun rot ettiğini gösterdi (yeni kapı eklendi, filtre genişletilmedi, 9 kök dışarıda kaldı). Kaldırmak en dürüst seçenek; **karşı ağırlık:** deponun CI geçmişinde fatura limiti kaynaklı kırmızılar var (`reference-ci-billing-limit-failure`) ve filtreyi silmek koşum sayısını artırır. Koşum süresi ölçüldü: 44–58 sn. **Karar sahibinin** |
| ✅ **AL-K25** · ~~Parite sayaç kilidi KÜRESELDİ — kardeş CI'ında yapısal kırmızı~~ → **KAPANDI (2026-08-11, PR #81 + #82, `v7.7.1`)** | `MEASURED_SHARED_LEAVES = 142` küresel bir tabandı ama kapı **her kardeşin kendi CI'ında** koşuyor (D4-b) → edge checkout'unda toplam 0, `0 >= 142` **yapısal kırmızı**. Kusur `v7.7.0` kaynaklı değil, **`v7.6.1`** (`8c673e5`, PR #63) ile geldi; edge `7.6.0`'a pinli olduğu için ancak yeni pine geçerken göründü. Etiket değişmez (I-2) → **`v7.7.1` (PATCH)** gerekti. Düzeltmenin tasarımı **edge oturumundan** geldi (taban çift başına + pozitif kontrol) ve ölçümle doğrulandı: 13 MIRROR çiftinin **12'sinde iki tarafta da üst düzey `metadata` yok**, 142'nin tamamı `analysis_type.enum.v1.json`'dan geliyor. ⚠️ İlk (kaba) taramam *"5 çiftte kanonikte `metadata` var"* demişti — o tarama alt-dize aramasıydı, **kapının tanımı değil**; kendi aracımı doğrulamamıştım. Uygularken **kalan bir delik** daha ölçüldü: iki kilit de depo verisini okuduğu için, ölçecek verisi olmayan kardeşte yürüyüşün bozulması görünmüyordu (*edge-only + körelmiş yürüyüş → `2 passed`*); aynı boşluk contract'ın kendi CI'ında daha büyüktü (kardeş yok → hepsi atlanıyordu). `TestWalkMechanismItselfWorks` (5 test, sentetik girdi, kardeş depo gerekmez) ikisini de kapatır |
| ✅ **AL-K26** · ~~I-1 üçlü hiza TUTMUYOR — platform hiç re-pin edilmedi~~ → **KAPANDI (2026-08-13, platform `eaf62e21`)** | Platform `7.6.1` → `7.7.2` re-pin edildi (submodule + `CONTRACTS_SHA256.txt` LF-normalize yeniden üretim, 97→97 dosya + `CONTRACTS_VERSION.md` kanonikten aynalandı) ve platform CI'ına `check_version_alignment.py` **tüketici kipinde** bağlandı (`ci.yml:109`, ayrı tam `contract-latest` klonuyla — submodule'ün pinli checkout'uyla karşılaştırma totolojisine düşmeden). Bu turda **kardeşlerin anti-totoloji kontrolü de düzeltildi**: worker/edge'deki `git describe --exact-match HEAD` yanlış değişmezi ölçüyordu (aracın kaynağı `--latest-from-git` HEAD'i değil `newest_tag(git_tags(...))`'i okur) — üçü de doğru değişmeze (`tag --list 'v*' ≥ 2` + `refs/tags/v${pin}` var) geçti. **Yeniden doğrulandı (2026-08-18):** contract `v7.7.2` (HEAD 16 commit ileride, docs-only) · worker `v7.7.2` (`CONTRACTS_VERSION.md`) · edge `7.7.2` (`Upstream Contract Set (SSOT)`) · platform `7.7.2` (`CONTRACTS_VERSION.md` + `git submodule status` pin eşleşiyor) — **dört depo hizalı, I-1 tutuyor.** Ayrıntı: hafıza `i1-surum-hizasi-kapisi` |
| **AL-K27** 🟡 · **`payment_target_type` bağlanmadı — bilerek ertelendi** | Ölçüldü ve **güvenli**: kanonik `payment_intent.v2` (canlı) ve `.v1` (deprecated) `["MISSION","SUBSCRIPTION"]` değerlerini **inline** yazıyor, kanonik enum ile birebir aynı; platform `PaymentTargetType(str, Enum)` da aynı iki değer; şema **hiçbir vendored parite çiftinde değil** → I-4 sonucu yok. Yapılmadı çünkü `schemas/` değişikliği **checksum'ı kırar** ve tam o sırada `v7.7.0` yayımlanmıştı; `v7.7.1` ise PATCH olduğu için yine kapsam dışı kaldı. **Bir sonraki MINOR turunun ilk kalemi** — ölçümü hazır |
| **AL-K28** 🟡 · **`field_created` değer kısıtı kuralının KAPISI YOK** | Kural yalnız düzyazıda yaşıyor, doğrulayan test/araç yok. Bu turun ana teması *"belgelenmiş ama uygulanmayan kural bir dilektir"* olduğu için kapsam dışı bırakılmadı, **ölçülüp sıraya alındı** |
| **AL-K29** 🟢 · **`tools/sync_to_repos.py` ölü — silme kararı kullanıcının** | Ölçüldü: gerçek çağıran **0**, kapsam **%0**. Dosya silme onay gerektirdiği için yapılmadı. `docs/versioning_policy.md`'deki koşmayan komutlar bu turda düzeltildi, yani belge artık ölü araca **yanlış biçimde** atıf yapmıyor |
| ✅ **AL-K32** · ~~Kök dizinde YETİM ve koşarsa ZARARLI bir PowerShell betiği~~ → **KAPANDI (2026-08-11, kullanıcı onayıyla silindi + kapı kuruldu)** | edge oturumunun sınıf uyarısı üzerine contract'ın betik ağacı ölçüldü: **3 dosya / 1021 satır**, hiçbirini ayrıştıran ya da denetleyen kapı yok (`bash -n` · `shellcheck` · PowerShell ayrıştırıcı → workflow'larda **0** isabet). **İyi haber:** üçü de temiz ayrışıyor — edge'de bulunan sözdizimi kusuru burada **tekrarlanmıyor** (ölçüldü: 2 bash dosyası `bash -n` temiz; `.ps1` PowerShell ayrıştırıcısında **0 hata / 548 token**). **Kötü haber `update-contracts.ps1`:** tek commit'le **2026-03-03**'te geldi (*"SSOT 1.2.0 uyum - v2.0.0"* — depo bugün **7.7.2**), çağıranı **workflow 0 · belge 0 · test 0**. Ölü olması sorun değil; **koşarsa zararlı** olması sorun: ① `Downloads` klasöründeki bir ZIP'i çalışma ağacının **tamamının üstüne** özyinelemeli olarak kopyalıyor (`-Force`) — bu adım hâlâ tamamen canlı; ② 4 adet koşulsuz `Remove-Item -Force` ve bir joker eşleşmeli silme içeriyor; ③ bitince kullanıcıya **`git add -A`** komutunu yazdırıyor — kök `CLAUDE.md`'nin **açıkça yasakladığı** komut; ④ kendi doğrulama listesi bayat (örneklenen 5 dosyanın 2'si artık yok, yani meşru silinmiş dosyalar için "EKSİK" raporlar); ⑤ başlığında başka bir makinenin sabit yolu var. **Silme adayı ama silme kullanıcı onayı ister** (kök `CLAUDE.md`). **Sınırı dürüstçe:** silme listesindeki 4 hedefin **hiçbiri bugün mevcut değil**, yani o adım şu an etkisiz — zarar iddiası ①/③'e dayanıyor, ②'ye değil. **Çözüm önerisi tek turda:** dosya kaldırılır **ve** betik ağacına iki katmanlı bir kapı kurulur (ayrıştırma + yasaklı komut taraması), yoksa aynı sınıf geri döner | **KAPANIŞ:** Kullanıcı onayıyla dosya silindi ve `tools/check_scripts.py` + `tests/test_script_tree_gate.py` (24 test) kuruldu, contract CI'ına bağlandı. Pozitif kontrol: **silinen betik bu kapıdan geçemezdi** — 93. satır *çalışma-ağacını-ezme*, 143. satır *toplu-ekleme* kuralına takılıyor (ölçüldü). Kapı yazarken **kendi yanlış-kırmızısını** üretti ve iddia ölçümle çürütüldü: ilk hâl betikleri çalışma ağacından ayrıştırıyordu, `core.autocrlf=true` olan makinede hepsi CRLF hatası verdi ve neredeyse *"betikler bozuk"* diye raporlanacaktı; `git ls-files --eol` indeksin `lf` olduğunu gösterdi → kusur betiklerde değil **kapının ölçüm ortamındaydı**. İkinci tuzak: CR temizlenip stdin'e *metin* olarak yazılınca Python Windows'ta geri `CRLF` üretiyordu → **bayt kipi** şart. Dokuz mutasyon koşuldu; ikisi ilk turda **uygulanmadı** ve "hepsi geçti" gibi göründü (kaçış hatası) — kaçışsız yöntemle tekrarlandı. Bir mutasyon (açık CR temizliğini kaldırma) **hiçbir testi öldürmedi**; sebebi ölçülüp koda yazıldı: `read_text()` zaten evrensel satır sonu çevirimi yapıyor, gerçek koruma bayt kipi (4 test).
| ✅ **AL-K30** · ~~I-1'i ÖLÇEN KAPI HİÇBİR DEPODA YOK~~ → **KAPANDI (2026-08-11, kapı yazıldı ve contract CI'ına bağlandı)** | edge oturumu bildirdi, **bağımsız doğruladım**. ① edge pin geçmişi `7.5.0 → 7.6.0 → 7.7.0`; **`7.6.1` adımı hiç yok** (edge'in sürüm kilidi dosyasındaki ilgili satırın `git log -L` ile satır geçmişi çıkarıldı) → I-1 o pencerede kırıktı ve **kimse fark etmedi**. ② Dört depoda kapı taraması: contract'taki 2 isabet düzyazı, platform'daki 8 isabet **başka bir numaralandırma** (Dockerfile değişmezi, çapraz-repo sürümüyle ilgisiz — yanlış-pozitif tuzağı), worker/edge **0**. Yani üç `CLAUDE.md`'de *"I-1 tutmalı"* yazıyor ama **onu doğrulayan tek bir komut yok** — bu turun ana temasının (*belgelenmiş ama uygulanmayan kural bir dilektir*) en büyük örneği. **Tasarım (D4-b uyumlu):** kapı contract'ta **yazılır**, kardeşlerde **koşar** — `test_vendored_parity.py` ile aynı model. Kardeş CI zaten bu public depoyu checkout ediyor; check `pin` değerini **yayımlanmış en yüksek etiketle** karşılaştırır (kendi checkout'uyla karşılaştırmak **totolojidir** — kardeş zaten `ref: v${pin}` ile çekiyor). I-5 gereği sapmaya izin verilecekse **tarihli + gerekçeli** bir muafiyet zorunlu olmalı, sessiz gecikme değil. ⚠️ Kapı **sentetik olarak da sınanmalı**: contract'ın kendi CI'ında kardeş yoktur, veriye dayalı kısım orada kördür (bkz. AL-K25'in üçüncü katmanı). **Bu turda YAPILMADI** — iki kardeş oturum tam o sırada re-pin yapıyordu, paralel-oturum kuralı gereği dosyalarına girilmedi | **KAPANIŞ (aynı gün):** `tools/check_version_alignment.py` yazıldı, `tests/test_version_alignment_gate.py` (34 test, **8 mutasyonla** sınandı) ile kilitlendi ve contract CI'ına **kanonik kipte** bağlandı. Kardeşler aynı aracı **tüketici kipinde** koşacak (D4-b). Gerçek veriye karşı koşturmak **kendi kusurumu buldu**: ilk kural "dosyadaki ilk sürüm eşleşmesi"ydi ve edge dosyasında `1.7.0` (edge'in KENDİ SemVer'i) okudu — doğru cevabı yanlış gerekçeyle verdi, sürümler bir gün örtüşse **yanlış YEŞİL** verirdi. Ölçüm: sürüm dosyalarında sırasıyla **30 · 22 · 27** farklı sürüm dizesi var (değişiklik geçmişi aynı dosyada). Artık `--label` ile pin satırı gösterilir, belirsizlikte **fail-closed**. İkinci kurulum tuzağı: `actions/checkout` varsayılanı **etiket getirmez** → kapı fail-closed kırmızı verirdi; `fetch-depth: 0` eklendi (etiketsiz klonla ölçüldü). Canlı sonuç: contract ✅ · worker ✅ 7.7.2 · edge ✅ 7.7.2 · **platform ❌ 7.6.1 (exit 1)** — kapı ilk koşumunda gerçek kırığı yakaladı.
| ✅ **AL-K31** · ~~Aynı kusur KARDEŞ DOSYADA da vardı — "sınıfı kapattım" iddiam yanlıştı~~ → **KAPANDI (2026-08-11, PR #85, `v7.7.2`)** | AL-K25'te `test_vendored_parity.py`'nin küresel tabanını çift başına çevirdim ve **"aynı sınıfın tamamını kapattım"** dedim. Kapatmamışım: `test_vendored_policy_parity.py` aynı kusuru taşıyordu ve **saymadım** — yani AL-K25'in kendi ③ maddesini ("sınıfı gördüm deme, **say**") ihlal ettim. **Worker oturumu yakaladı** (o testi `--deselect` ile dışarıda bırakmışlar). Bildirdiklerinden daha genişti, ölçüldü: worker CI **8 çift / 35 düğüm**, edge CI **10 çift / 13 düğüm**, eşik ise `18 / 48` → **iki kardeşte de** yapısal kırmızı; kapı yalnız dört deponun birden durduğu bir geliştirme makinesinde geçiyordu (yani koşması gereken **hiçbir** ortamda geçmiyordu). Düzeltme AL-K25'le aynı üç katman: çift-başına taban (`MEASURED_NODES_BY_PAIR`, 18 giriş) + taban-0 pozitif kontrolü (üç enum çifti; enum dosyasında object düğümü yok) + sentetik mekanizma sınıfı (6 test, kardeş depo gerekmez). **Altı mutasyon, hepsi öldürdü**; en kritiği `BEYANSIZ` → `KAPALI` (3 test) — politikasız düğümü kapalı saymak sessiz bir **fail-open** ve v7.7.0'ın ana kalemini boşa düşürürdü. Bu turda sınıf araması süitin tamamına yayıldı: kalan iki sabit (`MEASURED_ASYMMETRIC`, `MEASURED_DEBT_VALUES`) **tavan** (`<=`) ve statik sözlüğe bakıyor → kardeşten bağımsız, güvenli |

### 📌 Bu turda ölçülüp ÇÜRÜTÜLEN iddialar (tekrar gündeme gelmesin)

| İddia | Neden çürüdü |
|---|---|
| *"`Detection.bbox` kapatılabilir"* (benim ilk kararım) | Tüketicide alan opak `dict[str, float]`; anahtar kümesini kısıtlayan tek satır yok → kapatma ölçülemeyen bir üreticiyi reddedebilirdi. Ayrıca I-4 parite çelişkisi ölçüldü |
| *"`calibration_type` tek-kaynak kapısı yok"* (ilk mutasyon sonucum) | **Yanlış mutasyon biçimi**: enum'a değer EKLEDİM; alt-küme kopyalar ancak **değer YENİDEN ADLANDIRILINCA** çelişir. Doğru mutasyon **6 testi** kırdı — kapı sağlam |
| *"`x-compat-accepted` `$ref` daralmasını NON_BREAKING'e indirir"* (ilk CHANGELOG cümlem) | Mekanizma yalnız `ACCEPTABLE_TYPES` içindeki 5 tipe uygulanır; bu değişiklik `REF_CHANGED`. Dedektör `$ref`'i **çözmediğini kendi belgeliyor** (docstring 53-55) ve *"manual review required"* yazıyor — beyanlı sınır, gizli kör nokta değil |
| *"contract `.sh` betikleri Linux'ta koşmaz (BOM + CRLF)"* (denetimdeki ilk okumam) | **Ölçüm aracının kusuruydu**: PowerShell `>` yönlendirmesi git blob'una BOM ekleyip LF→CRLF çevirdi. Gerçek blob tertemiz (`23 21 2f…`); Bash `od` ile çürütüldü |

### ⚠️ Kalıcı sınır (kapatılmadı, beyan edildi)

`tools/breaking_change_detector.py` **object-politikası daralmasını hiç görmüyor**:
27 düğüm açıktan kapalıya geçti, dedektör `has_breaking=false` dedi ve o 27 kapatma
için **sıfır değişiklik kaydı** üretti. `unevaluatedProperties`/`additionalProperties`
yalnız `SUBSCHEMA_SINGLE` listesinde (satır 116-120) *alt-şema taşıyıcısı* olarak
tanınıyor; sınıflandırma kuralı yok. Bu, `$ref` sınırından **farklıdır** — orada beyan
var, burada yok. Sürüm kararı bu yüzden **elle ölçüldü** (5385 JSON + üretici kodu).

---

---

## 14.14 🟠 UZMAN EKRANI ZİNCİRİ TURU (2026-08-19/20) — *süperseded: canlı giriş §14.17*

> **Bu bölüm §14.10'un yerine geçer.** Yukarıdaki "TEK YETKİLİ GİRİŞ NOKTASI"
> tablosunda §14.10 🟢 idi; bu turda ölçülen kalemler onu süperseded ediyor.
> §14.10'un AL-K kalemleri **hâlâ açıktır**, oradan silinmedi.
>
> **Turun uygulananları** platform PR #441…#447'de (hepsi merge + dağıtıldı);
> durum fotoğrafı `docs/SESSION_HANDOFF.md` §0.A. Aşağıdakiler **kalanlardır**.

### 🔴 Turun ana bulgusu — ürün sahibinin istediği akışın nerede koptuğu

Ürün sahibi (2026-08-20) akışı şöyle tarif etti: *worker tüm görüntüleri analiz eder,
sorunlu alanları tespit eder, kaynakları hakkında öğrenir ve **tam karar veremediği**
tekli görüntüleri uzmana tam teşhis için gönderir.*

Ölçüm: **karar verme ayağı ÇALIŞIYOR, taşıma ayağı YOK.**

```
worker  : trigger_confidence 0.302 / 0.430  → INDICES_ONLY bandı (0.25-0.45)
          → "tanı SAKLANIR" (confidence_calculator.py:394-454)
          → findings = []  (bastırılan tespitler DIŞA HİÇ VERİLMİYOR)
platform: expert_portal.py içinde findings/detections → 0 atıf
web     : uzman ekranı yalnız katman haritası görüyor
```

Yani worker "karar veremedim" deyip uzmana yolluyor, ama **neye karar veremediğini
göstermiyor**. Bastırma KR-019/KARAR-13 gereği doğrudur; kusur bastırılan bilginin
**uzman kanalına** hiç açılmamasıdır. Uzman bugün görüntüsüz karar veriyor —
üretimdeki ilk iki inceleme (`08b3cac3`) tam da böyle **REDDEDİLDİ**.

**Bu, E11 (ham kare seçici) ile aynı iş DEĞİLDİR.** E11 uçuş kareleri hakkındadır ve
DALGA 3'te, C8'e kilitlidir (D10-E4). Aşağıdaki DK-48/49 ise **bugün var olan** karo
görüntülerini uzmana açar; yeni sözleşme gerektirmez (kanıt: DK-48).

### Yeni kalemler

| # | İş | Depo / dosya | Ne zaman |
|---|---|---|---|
| **DK-48** 🔴 | **Bastırılan tespitler uzman kanalına açılmalı.** Worker INDICES_ONLY/PARTIAL modunda tespitleri `findings`'ten düşürüyor; uzman "modelin kararsız kaldığı karo"yu hiç görmüyor. Sözleşme **hazır**: `analysis_result.v1.schema.json:438,443` → `Detection.rgb_uri` + `Detection.ms_uri` (+ `tile_id`, `confidence`, `confidence_components`, `sub_specialty`). KR-071 kısıtı **yalnız çiftçi yolunda** (`results_service_impl.py:145`, yorum kapsamı açıkça *"çiftçi yanıtı yalnız tarımsal gözlem taşır"*) → **uzman yolunda kısıt yok**. Yapılacak: (a) worker bastırılan tespitleri ayrı bir uzman-alanında dışa versin (b) platform uzman ucunda taşısın (c) web karo görüntüsünü göstersin. ⚠️ Aynı turda: çiftçi yolunun hâlâ sildiğini kanıtlayan **pozitif kontrol** testi | worker `reporting_agent.py` → contract → platform `expert_portal.py` → web | **uçuş sonrası ilk iş** |
| **DK-49** 🟠 | **`trigger_confidence` uzmana gösterilmiyor** — yalnız ADMIN ekranında. Uzman "model %30 emindi ve **zararlı** sandı" bilgisini görmeden karar veriyor. Değer `expert_reviews.trigger_confidence` + `predicted_sub_specialty` olarak **zaten kayıtlı**; iş yalnız uzman ucuna + ekrana taşımak. ⚠️ KR-025 sınırı: bu bir *tanı* değil, *modelin belirsizliği* olarak sunulmalı — uzmanı yönlendirmemeli | platform `expert_portal.py` · web inceleme sayfası | DK-48 ile aynı tur |
| **DK-50** 🔴 | **Sunucu CPU borcu — `numpy<2` pini KALICI DEĞİL, kod bunu çözemez.** Üretim VM'i "Common KVM processor": x86-64-v2 için gereken 4 bayraktan yalnız `cx16` var. numpy 2.5.1 **import anında** düşüyordu → rasterio + rio-tiler ölü → **döşeme üretimi tümden çalışmıyordu** (7770 log satırı). #446 ile `numpy>=1.26,<2` pinlendi ve üretimde doğrulandı. **Asıl çözüm koddaki değil sunucudaki:** VM işlemci modelini `host-passthrough` yap; sonra pin kaldırılabilir. Yapılmazsa numpy 2.x'e geçiş **imkânsızdır** | hosting / VM ayarı → sonra platform `pyproject.toml` | **uçuştan önce değil, ama borç olarak izlenir** |
| **DK-51** 🟠 | **"Gerçek Görünüm" taban görüntüsü boş.** `rgb_ortho_uri` ile `calibrated_ortho_uri` **aynı dosyayı** gösteriyor ve o dosya **5 bantlı** kalibre ortofoto — 3 bantlı RGB değil. Tile servisi dürüst davranıp boş dönüyor (sahte renk üretmiyor, doğru davranış). Kusur **ingest tarafında**: ya ayrı bir RGB kompoziti üretilmeli ya da alan boş bırakılmalı (aynı dosyayı iki alana yazmak sessiz yalan) | platform ingest · edge manifest | demo sonrası |
| **DK-52** 🟠 | **Yama (priority_zones) üretimi üretimde bağlı değil.** `analysis_priority_zones` sistem genelinde **0 satır**, `INGEST.PRIORITY_ZONES_PERSISTED` logu **0 kez** düştü, `ENABLE_NDVI_PRIORITIZATION` varsayılanı **False**. Ayrıca sorunlu alanı **DJI Terra belirlemiyor** — edge'in kendi `NdviPrioritizer`'ı belirliyor ve eşik tablosunun başlığı *"general literature averages… must be calibrated"* diyor. Yani bayrağı açmak yetmez; **eşikler ilk gerçek uçuşla kalibre edilmeli** (ölçüm #5 ile aynı tur) | edge `NdviPrioritizer` · platform ingest bayrağı | ilk uçuş verisiyle |
| **DK-53** 🟡 | **Faydalı böcek kartı YOK.** Katalog 210 kart: disease 84 · pest 56 · abiotic 50 · weed 20 · **beneficial 0**. `BENEFICIAL` geçerli bir alt uzmanlık kodudur ve #447'de PEST'e **yoldaş** bağlandı (zararlı kararı doğal düşman elenmeden verilemez) — kart yazıldığı gün kendiliğinden görünür. Bu bir *ölü koruma bağlama* örneğidir, ölü kolona tüketici ekleme değil | worker kart katalogu (SSOT) → platform aynası | §14.13 ile aynı tur |
| **DK-54** 🟡 | **Kanonik bağ mandalında 2 kalem kaldı.** `scripts/check_kanonik_bag_tuketicileri.py` listesi 5 → 2'ye indi. Mandal **iki yönlü**: düzeltilip listeden silinmeyen kalem de kırmızı verir, yani kalanlar sessizce unutulamaz | platform | demo sonrası |
| **DK-55** 🟡 | **`lock-install-smoke` bütçesi kapağını aşıyor:** `check_ci_butce.py` ölçtü — kapak 20 dk, en kötü adım bütçesi **28,5 dk**. Ya kapak yükseltilmeli ya adım bölünmeli; bugünkü hâlde kapak **yanlış güven** veriyor | platform `.github/workflows/ci.yml` | demo sonrası |

### ⛔ §14.14 ÖZ-DENETİMİ (2026-08-20, aynı gün) — 2 kalem çürütüldü, 3 atıf yanlıştı

> §14.14 yazıldıktan hemen sonra sekiz iddianın her biri **çürütülmeye çalışıldı**
> (bağımsız ölçüm turu). Sonuç: 6 ayakta, **2 çürütüldü**, 3'ünde atıf yanlıştı.
> Kalemler aşağıda düzeltiliyor — silinmiyor, çünkü neyin yanlış iddia edildiği
> de kayıttır.

| # | Yeni statü | Ölçülen doğru |
|---|---|---|
| **DK-55** | ⛔ **ÇÜRÜTÜLDÜ — bayat kalem** | `check_ci_butce.py` bugünkü HEAD'de `lock-install-smoke` için **kapak 20 dk / en kötü bütçe 15,0 dk** ölçüyor ve **temiz** raporluyor (çıkış kodu 0). "28,5 dk" sayısı depoda **dize olarak bile geçmiyor**. Aşım gerçekten vardı ama değeri **34,5 dk** idi, `5c0bda76`'da kaldı ve **`b84a7877` ile kapandı**. Kalem AÇILMADAN ÖNCE kapanmıştı; ben kapanmış bir ölçümü açık diye yazdım. |
| **DK-53** | ⛔ **ÇERÇEVE YANLIŞ** | `BENEFICIAL` bir **kart kategorisi DEĞİLDİR**. Kanonik kart şemasının `category` enum'u yalnız 4 değer taşır (`disease/pest/weed/abiotic`) ve `unevaluatedProperties:false` olduğu için `category: beneficial` yazan kart **reddedilir**. `BENEFICIAL`, **zengin `sub_specialty` ekseninin** bir değeridir (şema: *"faydalı böcek / doğal düşman zengin yuvası — Gap #1"*). Doğru ifade: **`sub_specialty: BENEFICIAL` taşıyan kart yok**. Sözleşme değişikliği **GEREKMİYOR** — alan zaten var. |
| **DK-52** | ✅ ayakta, **atıf yanlıştı** | Platform tarafında yazıcı **VAR ve BAĞLI**: `ingest.py:161` → `ingest_service_impl.py:472-506` (INSERT) → `worker_dispatch_service.py:294-309` (okuyucu). Tablo boş çünkü **ÜRETİCİ göndermiyor** (`edge/intake.py:673` `priority_zones=` vermiyor). Düzeltme **platformda değil EDGE'de**. |
| **DK-48b** | ✅ ayakta, **kapsam daraldı** | Sıfırdan görsel üretici yazmak **gerekmiyor**: yazılmış ama **bağlanmamış** bir üretici zaten var — `expert_bundle_producer.build_expert_visual_bundle` + `expert_bundle_persistence.persist_bundle_to_disk`, `<output_dir>/<job_id>/` altına **6 PNG** (true_color, false_color, ndvi/ndre/ndwi/gndvi ısı haritası) + `manifest.json` yazıyor. İş **yazmak değil BAĞLAMAK**. |
| **DK-48a** | ✅ ayakta, **mekanizma daha iyi** | Tespitler üretilir, sonra `self.detections = []` (`analysis_result.py:200`) listeyi **boşaltmaz, yeniden bağlar** — `PipelineResponse.detections` maskelemeden sonra da tespitleri **TUTUYOR** (ölçüldü: `len=1`, `class_id='karazenk'`). Nesne bellekte var → worker tarafında dışa vermek küçük iş. Ayrıca sınıf etiketi **zaten kalıcıya yazılıyor**: `pipeline.py:3470` + `4056-4081`, `model_pred` alanı `result_mode`'dan **bağımsız** SQLite'a gidiyor. |
| **DK-51** | ✅ ayakta, **atıf yanlıştı** | Düzeltme **EDGE'de** (+ sözleşmede); platform Red/Green/NIR/RedEdge'ten mavi **üretemez**, reddetmesi kasıtlı fail-honest davranıştır. Ayrıca "boş dönüyor" tam olarak şudur: `has_basemap=False` → arayüz "Gerçek Görünüm" düğmesini **hiç çizmez**; karo adresi doğrudan çağrılırsa **HTTP 404** (`tiles.py:257`). Gri kare davranışı **DK-39'dan önceki** hataydı, kapatılmış. |

#### 🔴 Bu öz-denetimin bulduğu YENİ kusur (§14.14'te hiç yoktu)

**DK-56 · Kartın ZENGİN alt uzmanlığı EZİLİYORDU — 182 karttan 83'ü (%46) yanlış.**
PR #447'de eklenen yükleme satırı kartın **kendi** `sub_specialty` değerini koşulsuz
eziyordu (kaba `category`den türetip üzerine yazıyordu):

```
FUNGUS → DISEASE 56 · HEALTH → GENERAL 12 · WATER_STRESS → GENERAL 9
NITROGEN_STRESS 3 · THERMAL_STRESS 2 · SALT_STRESS 1
```

Somut sonuç: **mantar uzmanı 56 mantar kartının hiçbirini "alanımda" göremiyordu.**
Özellik yalnız DISEASE/PEST/WEED'de çalışıyor, **6 alt uzmanlıkta sessizce
başarısız** oluyordu. ✅ **PR #448 ile kapandı** (yazılı değer kanonik, türetme geri
düşüş; kanonik küme dışı token loglanır). Bu, DK-53'ün ikinci tıkacıydı da:
faydalı böcek kartı yazılsa bile eski kod onu `PEST`'e ezerdi.

**DK-57 · Birim testleri geliştiricinin `.env`'ini okuyordu — yerel ≠ CI.**
`Settings.model_config` `env_file=".env"` diyordu; CI'da `.env` yok, geliştirici
makinesinde var. Ölçüldü: bu makinede **5 test kırmızı**, CI'da `main` **yeşil**
(aynı SHA), `git clone --no-local` taze klonda **65/65 geçti**. Yani oturum boyunca
taşınan "beklenen 5 kırmızı" tabanı bir kod gerçeği değil **makine artefaktıydı** ve
yerel ölçümü *"benim değişikliğim mi bozdu"* sorusuna karşı **kör** bırakıyordu.
✅ **PR #448 ile kapandı** (test oturumu `.env` okumaz; üretim yolu değişmedi).
Yerel tam paket artık **sıfır kırmızı**.

**DK-58 · Yönlendirme ipucu, MODELİN TANISI gibi sunuluyordu.**
`predicted_sub_specialty` üreticisi okundu (`worker.py:1455-1458`): INDICES_ONLY'de
tespit maskelendiği için `first_detection` **daima None**, dolayısıyla değer
`classify_from_evidence(crop, ndvi, ndre, month, stage, bbch, active_targets)`
**sezgisel** sınıflandırıcısından gelir (üreticinin kendi yorumu: *"tek tüketici
uzman yönlendirmesi"*). Yani alan **modelin tanısı değil, yönlendirme ipucudur**.
✅ İfade **PR #448**'de düzeltildi. ⬜ **Açık ürün sorusu:** uzmanın hangi alana
yönlendirileceğine bugün *kalibre edilmemiş bir NDVI/fenoloji sezgisi* karar
veriyor — DK-52'deki eşik kalibrasyonuyla aynı kökten. İlk gerçek uçuş verisiyle
birlikte değerlendirilmeli.

> **Bu turun dersi:** kendi yazdığım devir notunu **aynı gün** çürütmeye çalışmak
> 2 bayat/yanlış kalem + 3 yanlış atıf + **3 yeni gerçek kusur** çıkardı. Beyan
> edilen açık kalem listesi, ölçülmeden **kanıt sayılmaz**.

### ✅ DK-48 KAPANDI — uzmana karo kanıtı + görüntüsü (2026-08-20, aynı gün)

> §14.14'te *"açık ürün kararı (insana ait)"* diye bırakılan kalem **ürün sahibi
> tarafından karara bağlandı** ("kapıyı gevşet, uçtan uca uygula") ve aynı gün
> dört depoda uygulandı. Aşağısı ne yapıldığının kaydıdır.

#### Kural değişikliği

KR-019 **tanının** saklanmasını ister — uzmanın bakacağı **kanıtın** değil. Karo
konumu ve görüntüsü tanı değildir, tanının **ön koşuludur**. `INDICES_ONLY` artık
`PARTIAL_REPORT` ile **aynı** maskelemeyi uygular:

| Gizli kalır (tanı) | Korunur (kanıt) |
|---|---|
| `class_id` · `class_name` · `class_name_tr` · `sub_specialty` · `detection_type` | `tile_id` · `confidence` · `ndvi/ndre` · `bbox` · `rgb_uri` · `ms_uri` |

`result_mode` ve `reason_codes` **değişmedi** → aşağı akıştaki her karar noktası
aynen korundu. Çiftçi yolu etkilenmez (platform tespitleri zaten ayıklıyor,
KR-071). **`NO_RESULT` dokunulmadı** ve pozitif kontrolle kilitlendi.

#### Zincir (sözleşme değişikliği GEREKMEDİ)

`Detection.rgb_uri` / `.ms_uri` şemada 2026'dan beri vardı; worker onları **hiç
doldurmuyordu** ve `to_dict()` yazmıyordu bile.

```
pipeline (ham bantlar YALNIZ burada) → tile_crop_renderer (karo başına 2 PNG)
  → PipelineResponse.tile_crop_artifacts (transient) → orchestration
  → worker.py: indeks haritalarıyla AYNI upload() çağrısı + adresleri tespitlere yaz
  → platform: findings → presigned HTTPS → uncertain_tiles
  → web: galeri (solda gerçek renk, sağda NIR-K-Y)
```

Üç tasarım kararı ve gerekçesi: bantlar yukarı **taşınmadı** (tüm uçuşu bellekte
tutmak olurdu) · yükleme **tek** `upload()` çağrısında (ikincisi `manifest.json`'ı
ezerdi) · karo adresleri indeks haritaları boş dönse bile yazılır (iki iş bağımsız).

#### Merge edilen PR'lar

| Depo | PR | İçerik |
|---|---|---|
| worker | **#242** | üretici: maskeleme + renderer + taşıma + yükleme |
| platform | **#450** | tüketici: `uncertain_tiles` + presign + web galerisi · dağıtım kapısı testi · tespit sayımı anahtar hatası |
| platform | **#451** | kapı ASCII + kırılgan test çapası |
| contract | **#103 / #104** | kural gövdesi + kapı |
| edge | **#78** | kural bloğu + kapı |

#### 🔴 Çalışması için kalan TEK adım

Zincir **kodda tam**, ama worker **hiçbir yerde koşmuyor** (üretim sunucusunda
worker konteyneri yok; bu makinede Docker kapalı). Worker `docker-compose.yml`
`./src:/app/src:ro` mount'u taşıdığı için **imaj derlemek gerekmez** — `git pull`
+ yeniden başlatma yeter. Başlatma `sim-worker-baglan.sh` ile yapılır ve o betik
**bilerek kullanıcı tarafından** koşturulur (üretim kimlik bilgileri asistanın
izin katmanı dışında).

Yani: `uncertain_tiles` bugün **boş dönüyor** — kusur değil, üretici kapalı.

### "KESTİRME YOK" kuralı — kural + kapı

Ürün sahibi kuralı (2026-08-20). Kanonik gövde §4'ün **başında** (şemsiye kural).
Dört `CLAUDE.md`'de **bayt-özdeş blok** — çünkü ölçüldü ki **hiçbiri** çalışma
alanı kurallarına atıf yapmıyordu ve projenin kendi "depo içinden başlat"
talimatına uyulduğunda **hiçbir çalışma kuralı yüklenmiyordu**.

Kapı (`check_kestirme_yok.py`, dört depoda) **kelimeyi yasaklamaz**: ölçüldü ki
kelime yasağı **%70 yanlış pozitif** üretir (telefon maskesi, DJI dosya adı).
Ayırt edici olan **izleme kimliği**. İki yönlü mandal + gerekçeli taban:
contract 0 · worker 0 · platform 13 · edge 1.

Kapı ayrıca bir kör noktayı kapatıyor: `check_claude_md_refs.py` **çıplak adları**
atlıyor, yani var olmayan bir kapıyı adıyla vaat eden metin oradan yeşil geçiyordu.

#### Bu turda ölçülen üç depo-farkı (tekrar aramamak için)

1. **edge `RUF002`'yi açıyor** (yalnız `RUF003` muaf) → Türkçe **docstring** yasak,
   Türkçe **yorum** serbest. Gövde ASCII-Türkçe'ye çevrildi.
2. **Yalnız edge `ruff format --check`'i sert kapı yapıyor** (worker'da tavsiye,
   platform/contract'ta hiç yok). Yerelde `ruff check` koşturmak **yetmez**.
3. **Tüketici CI'ları kardeş contract'ı PİNLİ sürümle checkout ediyor** (`v7.7.2`
   = 2026-08-11). 2026-08-18'den sonra eklenen contract dosyalarına yapılan
   çapraz-repo atıfları o checkout'ta **sarkan** görünür. Bayt-özdeş bir bloğa
   böyle bir yol **konulmamalı** — ortama göre durum değiştirir ve hangi ortamı
   seçerseniz diğeri kalıcı kırmızı kalır.

### Bu turda kapanan ve bir daha açılmaması için kapıya bağlanan

`analysis_results.dataset_id` (#441) · kanonik bağ sınıfının tamamı + AST mandalı (#443) ·
CI asılma kapakları (#442) · BOUND kapısı `src/` dışına (#444) · dağıtımda submodule
fail-closed + simülasyon bağımsızlığı (#445) · numpy CPU uyumu (#446) · kartların alt
uzmanlık + bitki duyarlı sunumu (#447).

⚠️ **"Görev başına tek veri seti" varsayımı bu turda DÖRDÜNCÜ kez çıktı.** Artık AST
mandalıyla korunuyor; yeni bir tahmin yolu yazılırsa CI kırmızı verir.

---
