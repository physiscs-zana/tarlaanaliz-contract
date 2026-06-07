# Subscription (Sezonluk Paket) Yaşam Döngüsü Rehberi

> **SSOT Uyum:** v1.2.0 (2026-02-24)
> **İlgili KR:** KR-027 (Abonelik Planlayıcı), KR-015-5 (Reschedule Token), KR-033 (Ödeme Gate)
> **İlgili Şemalar:** `platform/subscription.v1.schema.json`, `platform/payment_intent.v2.schema.json`

---

## 1. Abonelik Durum Makinesi

```
PENDING_PAYMENT → ACTIVE → PAUSED → CANCELLED
      │              │                   ▲
      │              └───────────────────┘
      └─── (ödeme timeout) ──→ CANCELLED
```

| Durum | Tetikleyici | Sonraki Durum |
|---|---|---|
| `PENDING_PAYMENT` | Abonelik oluşturuldu, ödeme bekleniyor | `ACTIVE` (ödeme onayı) veya `CANCELLED` (timeout) |
| `ACTIVE` | KR-033 ödeme gate geçildi | `PAUSED` (kullanıcı talebi) veya `CANCELLED` (iptal) |
| `PAUSED` | Kullanıcı geçici durdurma talebi | `ACTIVE` (devam) veya `CANCELLED` (iptal) |
| `CANCELLED` | İptal veya ödeme timeout | Terminal durum |

---

## 2. Görev Üretim Akışı

Abonelik `ACTIVE` olduğunda `SubscriptionCreatedHandler` otomatik görev üretir:

```
Subscription {
    interval_days: 14,
    start_date: "2026-06-01",
    end_date: "2026-10-31"
}
    ↓
Görevler:
  Mission #1 → 2026-06-01  (T+0)
  Mission #2 → 2026-06-15  (T+14)
  Mission #3 → 2026-06-29  (T+28)
  Mission #4 → 2026-07-13  (T+42)
  ...
  Mission #N → 2026-10-19  (T+140)
```

Her görev `PLANNED` durumunda oluşturulur ve haftalık planlama motoru (`planning_engine.py`) tarafından pilotlara atanır.

---

## 3. Reschedule Token Sistemi (KR-015-5)

| Alan | Varsayılan | Açıklama |
|---|---|---|
| `reschedule_tokens_per_season` | 2 | Sezon başına kullanıcı reschedule hakkı |
| `reschedule_tokens_remaining` | 2 | Kalan hak |

**Kullanım kuralları:**
- Çiftçi bir görevin tarihini değiştirmek istediğinde 1 token harcar
- Hava engeli (KR-015-3A) nedeniyle yapılan reschedule token harcamaz (force majeure)
- Token bittiğinde reschedule talebi reddedilir

---

## 4. Ödeme Entegrasyonu (KR-033)

```
Subscription oluştur
    ↓
PaymentIntent oluştur (target_type: "SUBSCRIPTION", target_id: subscription_id)
    ↓
Çiftçi ödeme yapar (IBAN dekont veya kredi kartı)
    ↓
BILLING_ADMIN onaylar (IBAN) veya otomatik onay (kredi kartı)
    ↓
PaymentIntent → PAID
    ↓
Subscription → ACTIVE
    ↓
Görevler otomatik üretilir
```

**Hard gate:** `PAID` durumuna geçmeden abonelik `ACTIVE` olmaz ve görev üretilmez.

---

## 5. İlgili API Endpoint'leri

| Endpoint | Method | Açıklama |
|---|---|---|
| `/api/v1/subscriptions` | POST | Abonelik oluştur |
| `/api/v1/subscriptions/{id}` | GET | Abonelik detay |
| `/api/v1/subscriptions/{id}/pause` | POST | Geçici durdur |
| `/api/v1/subscriptions/{id}/resume` | POST | Devam ettir |
| `/api/v1/subscriptions/{id}/cancel` | POST | İptal |
| `/api/v1/subscriptions/{id}/reschedule` | POST | Görev tarih değiştir (token harcar) |

---

## 6. Schema Alanları

`platform/subscription.v1.schema.json` temel alanları:

| Alan | Tip | Zorunlu | Açıklama |
|---|---|---|---|
| `subscription_id` | UUID | Evet | Benzersiz kimlik |
| `farmer_user_id` | UUID | Evet | Abonelik sahibi çiftçi |
| `field_id` | UUID | Evet | Hedef tarla |
| `crop_type` | CropType enum | Evet | Bitki türü |
| `analysis_type` | string | Evet | Analiz tipi |
| `interval_days` | integer (>0) | Evet | Tarama aralığı (gün) |
| `start_date` | date | Evet | Başlangıç tarihi |
| `end_date` | date | Evet | Bitiş tarihi |
| `status` | enum | Evet | PENDING_PAYMENT / ACTIVE / PAUSED / CANCELLED |
| `reschedule_tokens_remaining` | integer | Evet | Kalan reschedule hakkı |
| `payment_intent_id` | UUID | Hayır | İlişkili ödeme |
| `price_snapshot_id` | UUID | Evet | Fiyat snapshot referansı |
