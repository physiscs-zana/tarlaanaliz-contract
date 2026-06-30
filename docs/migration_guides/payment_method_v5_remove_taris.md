# Migration Guide — v5.0.0: `payment_method` `TARIS_DEDUCTION` kaldırma

**Sürüm:** 4.1.1 → **5.0.0** (MAJOR / BREAKING)
**Tarih:** 2026-06-30
**Etkilenen sözleşme:** `enums/payment_method.enum.v1.json` (PaymentMethod 2.0.0 → 3.0.0)

## Ne değişti

`payment_method` enum'undan `TARIS_DEDUCTION` değeri **kaldırıldı**. Enum artık yalnızca iki
değer içerir:

```
CREDIT_CARD
IBAN_TRANSFER
```

## Neden

Tariş, **Ege bölgesi (İzmir/Ege)** tarım satış kooperatifidir. `tarlaanaliz` platformu yalnızca
**GAP (Güneydoğu Anadolu Projesi)** bölgesine hizmet eder; Tariş GAP'ta faaliyet göstermez.
`TARIS_DEDUCTION`, `egeanaliz → tarlaanaliz` port'undan kalan bir artefakttı ve hiçbir GAP
senaryosunda geçerli değildi. Platform tarafı (PR #307) ve uygulama kodu zaten temizlendi; bu
sürüm sözleşmeyi de hizalar.

## Breaking etki ve tüketici aksiyonları

`TARIS_DEDUCTION` içeren bir mesaj/payload artık `payment_method`'a karşı **valide olmaz**.

| Tüketici | Etki | Aksiyon |
|---|---|---|
| **Platform (backend)** | Yok — `payment_method` enum'u koddan okunmaz (`get_payment_methods` pricing-config'ten döner); `PaymentMethod` domain enum'unda `TARIS_DEDUCTION` zaten yok (PR #307). | Pin'i 5.0.0'a güncelle. |
| **Frontend (PWA)** | Ödeme yöntemi listesinde Tariş seçeneği zaten yok. | Pin/yansıtma 5.0.0. |
| **Worker / Edge** | **Yok** — bu servisler ödeme yöntemi enum'unu tüketmez (ödeme `farmer → platform` akışıdır; worker=analiz, edge=intake). | Aksiyon gerekmez; min-contract 4.0.0 korunur. |

## Veri/geçmiş

`payment_method` DB seviyesinde enum-kısıtlı DEĞİLDİR (platform tarafında `String`), bu yüzden
DDL geçişi gerekmez. Geçmişte `TARIS_DEDUCTION` ile yazılmış bir kayıt (platform pilotunda
üretilmedi) varsa, contract-valide bir yola sokulursa reddedilir; bilinen üretim verisi yoktur.

## Doğrulama

```bash
python tools/validate.py
pytest tests/ -v
python tools/pin_version.py --verify
```
