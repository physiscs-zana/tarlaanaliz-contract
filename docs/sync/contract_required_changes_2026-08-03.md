# Contract — Kanonik Tarafta Yapılması Gerekenler (RAPOR-ONLY, devir)

**Tarih:** 2026-08-03
**Yön:** worker/platform → **contract** (bu deponun yapması gereken işler)
**Statü:** UYGULANMADI — bu tur platform tarafında çalışıldı; kanonik depo tek-taraflı
düzenlenmez (KESİN KURAL). Bu dosya kanonik oturumun karar-hazır devridir.
**Kardeş kayıt:** `tarlaanaliz-worker/denetim/b4_worker_contract_devir_spec_2026_06_30.md`
(E2/E3 kalemlerinin kökeni) · `tarlaanaliz-platform/docs/security/open_items_decisions_2026-06.md`
(CHERRY satırı).

> **Sade dil:** Worker'ın tanıdığı ürün ve bölge listesi, kanonik sözleşmenin listesinden
> **geniş**. Bugüne kadar bu fark görünmüyordu çünkü platform gelen sonuçları fiilen
> doğrulamıyordu. O arıza bu tur onarıldı — dolayısıyla fark artık gerçek bir ret sebebi
> hâline gelebilir. Aşağıdaki iki kalem kanonik tarafta kapatılmalı.

---

## 0. Neden şimdi — doğrulama fiilen çalışmaya başladı

Platform gelen `analysis_result` gövdelerini kanonik şemaya karşı doğruluyor
(`worker_bridge_consumer._validate_inbound`, `schema_key="analysis_result"`).
Bu doğrulama **uzun süre sessizce atlanıyordu**: kanonik şemalar dosyalar arası `$ref`
kullanıyor (`crop_type` → `../../enums/crop_type.enum.v1.json`), platform ise
`jsonschema`'yı registry bağlamadan çağırıyordu → referans çözülemiyor,
`ValidationError` OLMAYAN bir hata fırlıyor, üst katman onu "doğrulanamadı" sayıp
geçiyordu. Yani `worker_result_schema_enforce=True` fiilen NO-OP'tu.

Ölçüldü (2026-08-03, platform): düzeltmeden önce `CORN` da uydurma bir değer de aynı
yutulan hatayı veriyordu — geçerli/geçersiz ayrımı **hiç** yapılmıyordu. Yüklenen 68
şemanın 23'ü dış `$ref` taşıyor. Onarıldı (`SchemaRegistry.reference_registry`, `$id`
anahtarlı offline çözüm).

**Sonuç:** kanonik enum'lar artık gerçekten bağlayıcı. Aşağıdaki iki sapma, önceden
uykudayken, bundan sonra ret üretebilir.

---

## 1. E3 — `crop_type` enum'u worker'ın 12'sine genişletilmeli

**Ölçüm (2026-08-03):**

| Kaynak | Değer sayısı | Küme |
|---|---|---|
| Kanonik `enums/crop_type.enum.v1.json` | **8** | COTTON, PISTACHIO, CORN, WHEAT, SUNFLOWER, GRAPE, OLIVE, RICE |
| Worker `interface/contracts/analysis_result.v1.schema.json` | **12** | yukarıdaki 8'den WHEAT/SUNFLOWER dahil + **APPLE, PEACH, CHERRY, FIG** |

Worker `AnalysisResult.to_dict()` `crop_type` alanını yayıyor
(`src/core/domain/analysis_result.py:222` — `result["crop_type"] = self.crop_type.value`).
Kanonik `analysis_result.v1` bu alanı `$ref` ile 8-değerli enum'a kısıtlıyor →
worker `APPLE/PEACH/CHERRY/FIG` yayarsa platform sonucu **reddeder** (nack→DLX).

**Bugünkü risk: SIFIR — ama tesadüfen.** Platform'un dört giriş kapısı da
(`fields.py:277`, `missions.py:285`, `subscriptions.py:161`, `change_crop_type.py:107`)
`is_gap_offered` ile korunuyor ve sunulan küme
`GAP_OFFERED_CROPS = {COTTON, CORN, PISTACHIO, RICE, GRAPE}` — dördü de dışarıda.
Ölçüldü: `GAP_OFFERED ⊆ kanonik-8` = **True**. Yani bu dört ürün için tarla/görev/abonelik
hiç açılamıyor, worker'a iş gitmiyor, sonuç üretilmiyor.

**Sıra kilitlendi:** Platform tarafına bir kapı eklendi
(`tests/unit/domain/value_objects/test_crop_type.py::test_every_offered_crop_exists_in_canonical_wire_enum`):
sunum kümesi kanonik enum'un alt kümesi değilse build kırılır. Mutasyonla doğrulandı —
FIG/APPLE/PEACH sunuma alınırsa yakalayan **tek** test bu. Yani bu sapma artık sessizce
canlıya giremez; ama sunum kapsamını genişletmek isteyen herkes **önce buraya** bakmak
zorunda kalacak.

**Aksiyon (contract):**
1. `enums/crop_type.enum.v1.json` enum dizisine `APPLE`, `PEACH`, `CHERRY`, `FIG` ekle.
   `metadata.version` bump + `displayNames` (tr/en) + varsa `categories`/`gapPriorities`
   girdileri.
2. Sürüm sınıfı: **MINOR** — kendi politikanız (`CLAUDE.md` → "When Modifying Enums")
   *"Adding values: Non-breaking (MINOR)"* diyor. Migration guide gerekmez.
3. C8 töreni: annotated tag + platform submodule re-pin + `CONTRACTS_SHA256.txt`.

**Alternatif (eğer 12'ye genişletmek istenmiyorsa):** worker'a özel dar bir wire enum
tanımlanabilir; ama o zaman `analysis_result.crop_type` hangi enum'u `$ref` edeceği
kararı da bu turda verilmelidir. Karar kanonik tarafın.

---

## 2. E2 — `expert_labeling_card.endemic_regions` enum'una `EGE` eklenmeli

**Ölçüm (2026-08-03):**

| Kaynak | Değer sayısı | Fark |
|---|---|---|
| Kanonik `schemas/worker/expert_labeling_card.v1.schema.json` | **9** | — |
| Worker `interface/contracts/expert_labeling_card.v1.schema.json` | **10** | **+`EGE`** |

Worker `EGE`'yi **fiilen kullanıyor**, teorik değil:
`config/controlled_vocabulary/regions.yaml:19` (`- code: EGE`) ve
`config/expert_labeling_cards/cherry_cards.yaml` içinde 7+ kart girdisi
(`endemic_regions: - EGE`).

Ege çekirdek bir Türkiye bölgesi; kanonikte yokluğu bilinçli bir dışlamadan çok
**kanonik eksiklik** görünüyor (B4 devir spesi 2026-06-30'da da bu gerekçeyle istenmişti).

**Aksiyon (contract):**
1. `endemic_regions` `items.enum` dizisine `EGE` ekle (MARMARA'dan sonra, worker
   sıralamasıyla aynı yere).
2. Sürüm sınıfı: **MINOR** (additive).
3. Eğer bilinçli bir dışlama ise: gerekçeyi enum `changeNote`'una yaz ve worker'a
   `EGE`'yi hangi değere eşleyeceğini bildir — worker bugün kartlarında kullanıyor,
   sessiz bırakılamaz.

---

## 3. Örüntü notu — I-4'ün varsayımı bu iki eksende TERS

`CLAUDE.md` I-4 şöyle diyor: *"Worker `interface/contracts/`'te 8 izli dosyayı vendor'lar;
bunlar kanoniğin **superset** şemalarının **dar runtime alt-kümesidir**… Kanonik superset
worker'ın katı formunu kabul eder."*

Yukarıdaki iki kalemde bu **tersine dönmüş**: worker kanoniğin alt kümesi değil,
**üst kümesi** (crop_type 12 > 8; endemic_regions 10 > 9). Bu yüzden "kanonik superset
worker'ın formunu kabul eder" güvencesi bu iki alanda geçerli DEĞİL — kanonik daha dar
olduğu için worker'ın çıktısını reddeder.

Bu, I-4'ün yanlış olduğu anlamına gelmiyor; **istisnasının kayda geçmediği** anlamına
geliyor. İki kalem kapatılınca istisna da kapanır. Kapatılmayacaksa I-4 metnine
"şu alanlarda worker superset'tir ve kanonik onları kabul etmez" istisnası yazılmalı —
aksi halde değişmez, ölçülmeyen bir dilek olarak kalır.

---

## 4. Özet aksiyon tablosu

| # | Kalem | Dosya | Sürüm sınıfı | Aciliyet |
|---|---|---|---|---|
| E3 | `crop_type` +APPLE/PEACH/CHERRY/FIG | `enums/crop_type.enum.v1.json` | MINOR | Düşük — platform kapısı sessiz girişi engelliyor; sunum kapsamı genişletilmeden ÖNCE yapılmalı |
| E2 | `endemic_regions` +EGE | `schemas/worker/expert_labeling_card.v1.schema.json` | MINOR | Orta — worker kartlarında BUGÜN kullanılıyor |

İkisi de additive/geriye-uyumlu; ayrı tur açmayı hak etmez, **bir sonraki sözleşme
turuna binebilir**. Tek sıra kısıtı: E3, GAP sunum kapsamı `APPLE/PEACH/CHERRY/FIG`'den
birine açılmadan önce inmelidir.

---

*Hazırlayan: Claude Code · platform tarafında ölçülerek doğrulandı (kod + şema okundu,
enum'lar hesaplandı, kapılar mutasyonla sınandı) · 2026-08-03*
