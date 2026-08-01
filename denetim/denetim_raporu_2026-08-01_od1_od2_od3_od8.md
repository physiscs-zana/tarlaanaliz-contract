# ÖD-1 · ÖD-2 · ÖD-3 · ÖD-8 — ölçüm ve kapı kanıtı (2026-08-01, ikinci oturum)

> ⚠️ **BU DOSYA BİR İŞ LİSTESİ DEĞİLDİR.** Kanıt arşividir: her düzeltmenin `dosya:satır`
> dayanağı, her kapının mutasyon kaydı. Yapılacak işlerin tek kaynağı
> `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md` **§14.8**'dir.

**Girdi:** `denetim/denetim_raporu_2026-08-01_ozdenetim_6lens.md` → §14.8'in elle doğrulanmış
üç KRİTİK kalemi (ÖD-1/2/3) + ölçümle onlara bağlanan ÖD-8.

**Ortak kök neden (dördü de aynı):** *bir karar bir yere yazıldı, belgeyi DOĞRULAYAN yüzeye
yazılmadı ve hiçbir kapı ikisini karşılaştırmadı.* D16 bunu normatif **metin** tarafında
kapatmıştı (tek gövde + işaretçi); bu tur aynı deseni **şema** tarafında kapattı.

---

## 1. ÖD-1 — kayıt defteri ile şema ayrışıktı

**Ölçüm (değişiklikten önce):**

| Yüzey | Değer |
|---|---|
| `enums/calibration_type.enum.v1.json` → `x-context-subsets['edge/calibrated_dataset_manifest']` | `[ABSOLUTE, RELATIVE, PANEL_ABSOLUTE]` |
| `schemas/edge/calibrated_dataset_manifest.v1.schema.json:52-58` → `calibration_result.calibration_type.enum` | `[ABSOLUTE, RELATIVE]` |

⇒ C6b/S2 kararı **fiilen uygulanmamıştı**: `PANEL_ABSOLUTE` taşıyan kalibre manifest o gün de
reddediliyordu. Kararın gerekçesi ve iki bilinçli dışlaması (`NONE` — D8 · `DLS2_RELATIVE` —
E13) zaten enum'un `notes.c6b_subset_alignment` bloğunda yazılıydı; eksik olan **uygulamaydı**.

**Sınıf taraması (ad listesiyle değil ölçümle):** `schemas/` altındaki her `enum`, değerleri
kanonik kalibrasyon sözlüğünün alt kümesi **ve** ayırt edici bir değer taşıyorsa
(`ABSOLUTE`/`PANEL_ABSOLUTE`/`DLS2_RELATIVE`/`AGNOSTIC`) bir kalibrasyon yüzeyidir. Kural
**8 yüzey** buluyor, yanlış pozitif yok:

```
schemas/edge/calibrated_dataset_manifest.v1  /properties/calibration_result/properties/calibration_type
schemas/edge/intake_manifest.v1              /$defs/PlatformForm/properties/calibration_type
schemas/edge/intake_manifest.v1              /$defs/EdgeForm/properties/calibration_type
schemas/platform/calibrated_dataset_manifest.v1  /properties/calibration_type
schemas/worker/analysis_job.v1               /$defs/CalibrationMetadata/properties/calibration_type
schemas/worker/calibrated_dataset.v1         /properties/calibration_type
schemas/worker/calibration_metadata.v1       /properties/calibration_type
schemas/worker/expert_labeling_card.v1       /properties/calibration_assumed
```

**Yapılan:** şema deftere hizalandı (`PANEL_ABSOLUTE` eklendi) + açıklaması kararın
gerekçesini ve iki dışlamayı taşıyor.

---

## 2. ÖD-2 — S5 + W12 tel üstünde ölüydü

**Ölçüm (değişiklikten önce):**

| Tanım | Alanlar |
|---|---|
| `schemas/worker/calibration_metadata.v1.schema.json` (kanonik) | `calibration_method, calibration_panel_id, calibration_timestamp, calibration_type, irradiance_sensor, red_edge_center_nm, scale, sensor_model` (8) |
| `schemas/worker/analysis_job.v1.schema.json → $defs/CalibrationMetadata` (**işi taşıyan**) | `calibration_panel_id, calibration_timestamp, calibration_type, irradiance_sensor` (4) |

Gömülü tanım `unevaluatedProperties: false` taşıyor. `jsonschema` ile ölçüldü:

```
Unevaluated properties are not allowed ('scale' was unexpected)
```

**Zincirin tamamı ölçüldü — kod tarafı hazır, sözleşme tarafı kapalıydı:**

| Halka | Kanıt |
|---|---|
| worker ölçeği okuyor | `src/core/domain/analysis_job.py` → `CalibrationMetadata.reflectance_scale/scale_factor` + `resolve_reflectance_divisor` |
| pipeline onu çağırıyor | `src/core/services/inference/pipeline.py:2218-2221` |
| worker gelen işi **vendored** şemaya karşı doğruluyor | `src/application/job_handler.py:136` → `validate_analysis_job` → `contract_validator.py:242` |
| platform ölçek YAZMIYOR (henüz) | `worker_job_publisher.py:152-154` yalnız `calibration_type` yazıyor |

⇒ Sözleşme düzeltilmeden platform ölçeği yazsa **belge reddedilirdi**; yazmadığı için hata
bugüne dek görünmedi. Aynı delikten S4'ün `calibration_method` alanı da düşüyordu.

**Bilerek taşınmayan iki alan (ölçülerek karar verildi):** `sensor_model` ve
`red_edge_center_nm` iş belgesinde `drone_metadata` altında yaşıyor
(`schemas/worker/analysis_job.v1` → `properties/drone_metadata`; worker domain modeli de
onları `DroneMetadata` altında tutuyor). İkinci bir kopya "hangi kaynak kazanır" sorusunu
doğururdu. Beyan **ölçülüyor**: kapı, gösterilen taşıyıcı yolun gerçekten var olduğunu
doğruluyor (yazılı gerekçe yeterli sayılmıyor).

---

## 3. ÖD-3 — kapılar korudukları yüzeyi ölçmüyordu

`tests/test_calibration_type_axis.py` içindeki `_calibrated_subset()` yalnız
`x-context-subsets`'i okuyordu; `tests/test_calibrated_manifest_fields.py` içindeki
`test_edge_calibrated_subset_matches_the_c6b_decision` de öyle. Kararın değeri **şemadan**
silinse iki kapı da yeşil kalırdı.

**Yapılan:** her iki dosya artık **iki yüzeyi birden** ölçüyor (`kayıt defteri` +
`şema inline enum`); eşitliğin kendisini yeni sınıf kapısı zorluyor. Bayat kalmış iki docstring
cümlesi (*"alt küme bugün [ABSOLUTE, RELATIVE]"*, *"C6 iş yok"*) C6b/S2 sonrası hâliyle düzeltildi.

---

## 4. ÖD-8 — parite kapısı iki yönden dardı

**Ölçüm:** 16 vendored dosya (8 edge + 8 worker), izlenen **9**. İzlenmeyen 7'nin içinde
`analysis_job.v1` vardı — ÖD-2 tam oradan geçti. Ayrıca karşılaştırma yalnız **üst düzey**
`properties`/`required` idi: `$defs` ve **enum değerleri** hiç ölçülmüyordu.

**Kapsam genişletilince ilk koşuşta bulunan, daha önce hiç görülmemiş beş sapma:**

| # | Dosya | Sapma | Yön | Kalem |
|---|---|---|---|---|
| 1 | worker `analysis_job.v1` | `$defs/CalibrationMetadata` `scale`+`calibration_method` yok, form KAPALI | kanonik ileri | **W13** 🔴 |
| 2 | worker `expert_labeling_card.v1` | `EGE` bölgesi (2 pointer) | **vendored ileri** | **W14** |
| 3 | worker `expert_review_queue.v1` | `APPLE/CHERRY/FIG/PEACH` | **vendored ileri** | **W14** |
| 4 | edge `intake_manifest.v1` | `sorties[].crop_type` küçük harf | **vendored ileri** | **E16-b** |
| 5 | edge `calibrated_dataset_manifest.v1` | `raw_frames[].band` `RGB` yok (**S7 yayılmamış**) · `qc_report.flags` **kısıtsız string** (D7 sözlüğü yok) | kanonik ileri | C8 yayılımı (beyanlı) |

(2) ve (3) kanonikte **bilinçli** bir kapsam kararına dayanıyor: `2d77024` (2026-06-26)
*"fix region leakage in ported examples (Aegean coords/ids → neutral GAP)"* ve
*"Aegean CHERRY/FIG/APPLE/PEACH not adopted"*. Yani kanonik absorbe etmez; kardeş depo düzeltir.

**Neden tek kip yetmiyordu (ölçüldü):** `intake_manifest`/`scan_report`/`transfer_batch`
kanonikte `oneOf[$defs...]`, vendored'da **düz**; `analysis_job`/`analysis_result` vendored'da
dar. Bunlara MIRROR kuralı uygulamak yüzlerce yanlış pozitif üretirdi. SUBSET kipi bunun
yerine üç şeyi zorluyor: ortak `$defs` **çelişemez** · vendored değer **uyduramaz** ·
**kapalı** bir vendored form kanonik alanı **atlayamaz** (ÖD-2'nin tam kuralı).

**`Detection` emsali — kuralın ince ayarı:** worker `analysis_result` vendored formu 17 alan
taşıyor (kanonik 24) ve `required`'ı kanonikten **geniş**. Bu güvenlidir: worker **kendi
çıktısını** doğruluyor, ürettiği her belge kanoniği de geçer. Ters yön (`analysis_job`)
güvenli değildir: orada vendored kopya **gelen** belgeyi doğrular. Bu yüzden kalıcı daralma
`DECLARED_NARROWER_DEFS`'e, geçici gecikme `PENDING_PROPAGATION`'a yazılır.

---

## 5. Kapı kanıtı — **26 mutasyon, 26 kırmızı**

Yöntem: dosya yedeği + `try/finally` geri alma (asla `git checkout --`; commit edilmemiş iş
silinirdi). Kardeş depo dosyalarına dokunan mutasyonlardan sonra `git status` ile **temiz**
olduğu doğrulandı.

### 5.1 `tests/test_context_subset_binding.py` (ÖD-1/ÖD-3 sınıf kapısı) — 7/7

| # | Mutasyon | Düşen test |
|---|---|---|
| M1 | Şema enum'u `[ABSOLUTE, RELATIVE]`'e geri alınır (**ÖD-1'in kendisi**) | `test_surface_matches_registered_subset[edge/calibrated_dataset_manifest]` |
| M2 | Defterden değer silinir (şema doğru kalır) | aynı test, ters yön |
| M3 | Bağlam anahtarı silinir | `test_discovers_every_known_surface` + yetim + sayı |
| M4 | Şemaya kayıtsız değer sızar (`AGNOSTIC`) | `test_surface_matches_registered_subset[platform/…]` |
| M5 | `null` eklenir, tip beyanı yok | `test_null_in_enum_implies_nullable_type` |
| M6 | Kayıtlı dosyaya yeni `$defs` yüzeyi | `test_surface_matches_registered_subset[worker/calibration_metadata]` |
| M7 | **Kayıtsız dosyaya** yüzey (`analysis_result`) | `test_every_calibration_enum_is_registered` |

### 5.2 Onarılan eski kapılar (ÖD-3) — 3/3

| # | Mutasyon | Düşen test |
|---|---|---|
| MA | Şemadan `PANEL_ABSOLUTE` geri alınır | `test_edge_calibrated_subset_matches_the_c6b_decision` (**şema yüzeyi**) |
| MB | Şemaya `DLS2_RELATIVE` sızar (defter temiz) | `test_dls2_relative_stays_out_of_the_calibrated_package_surface` |
| MC | Şemadan `ABSOLUTE` (E13 kararı) silinir | `test_decided_value_is_accepted_by_the_calibrated_manifest` |

*(Üçü de eski hâlde YEŞİL kalırdı — kapılar defteri okuyordu.)*

### 5.3 `tests/test_calibration_metadata_single_definition.py` (ÖD-2) — 9/9

| # | Mutasyon | Düşen test |
|---|---|---|
| M1 | Gömülü kopyadan `scale` silinir (**ÖD-2'nin kendisi**) | `test_every_missing_property_is_declared` + `test_job_with_scale_is_accepted` |
| M2 | Gömülü kopyadan `calibration_method` silinir | aynı ikili (S4 yolu) |
| M3 | Gömülü ölçek enum'u daraltılır | `test_validation_semantics_match[scale]` + belge testi |
| M4 | `if/then` (bölen zorunluluğu) silinir | `test_scaled_int_without_divisor_is_rejected` |
| M5 | Gömülüye kanonikte olmayan alan uydurulur | `test_no_job_only_property` |
| M6 | Beyanın taşıyıcısı kaybolur (`drone_metadata.sensor_model`) | `test_declared_omission_has_a_real_carrier[sensor_model]` |
| M7 | Gömülüde alan sürükleme kapısı açılır | `test_both_forbid_field_drift` + `test_unknown_calibration_field_is_still_rejected` |
| M8 | **Kanoniğe** yeni alan eklenir, gömülüye eklenmez | `test_every_missing_property_is_declared` |
| M9 | `required` ayrışır | `test_required_matches` |

### 5.4 `tests/test_vendored_parity.py` (ÖD-8) — 7/7

| # | Mutasyon | Düşen test |
|---|---|---|
| M1 | MIRROR: vendored enum değeri uydurur | `test_vendored_invents_no_enum_value[attestation_record]` |
| M2 | MIRROR: vendored enum değeri kaybeder (beyansız) | `test_canonical_enum_ahead_is_declared[calibrated_dataset]` |
| M3 | SUBSET: ortak `$defs`'e uydurma alan | `test_shared_defs_do_not_contradict[analysis_job]` |
| M4 | SUBSET: **kapalı** `$defs` kanonik alanı atlar (`PriorityZone`) | `test_closed_vendored_def_carries_every_canonical_property[analysis_job]` |
| M5 | SUBSET: vendored `required` gevşer | `test_shared_defs_do_not_contradict[analysis_job]` |
| M6 | SUBSET: vendored sözlükte olmayan değer | `test_vendored_values_exist_in_canonical_vocabulary[intake_manifest]` |
| M7 | İzlenmeyen yeni vendored dosya | `test_every_vendored_file_is_tracked` |

---

## 6. Sürüm ve kapı durumu

| Ölçüm | Sonuç |
|---|---|
| Dedektör (`master` worktree ↔ çalışma ağacı) | **3 değişiklik / 0 breaking** → MINOR |
| — | enum değeri eklendi ×1 (`PANEL_ABSOLUTE`) · opsiyonel alan eklendi ×2 (`scale`, `calibration_method`) |
| İkinci bağımsız ölçüm (elle diff) | `required` değişmedi · enum silinmedi/yeniden adlandırılmadı · tip değişmedi · dosya silinmedi |
| `pytest tests/` | **1172 passed · 0 skipped · 2 xfailed** (ikisi de tur-içi beyanlı) |
| `tools/validate.py` | 96 dosya / **0 hata** |
| `tools/inline_refs.py --check` | ✅ güncel (68 dosya; `--write` ile yeniden üretildi) |
| `tools/check_no_egeanaliz.py` | OK |
| Kardeş depolar mutasyon sonrası | `git status` **temiz** (edge + worker) |

**Tur durumu değişmedi:** `CONTRACTS_VERSION.md` → `PENDING_REPIN`; iki beyanlı xfail
(checksum + `PENDING_PROPAGATION`) tur içinde beklenen kırmızıdır.
