# TARLA-ANALİZ — Yeni makinede kurulum

Çalışma alanı kuralları ve oturum kancası **bu depoyla (git ile) taşınır**; bu reçete
ikinci makinede kurulumu bitirir. Kanonik gövde: `calisma-alani-kurallari.md` (bu klasör).

## 0. Neden bu mimari

Kapsayıcı `TARLA-ANALİZ/` klasörü git deposu DEĞİLDİR → oradaki hiçbir dosya git ile
taşınmaz. Bu yüzden kök `CLAUDE.md` yalnız bir **işaretçidir**; kural gövdesi ve kanca
bu depoda yaşar → sürümlenir, PR'da incelenir, `git pull` ile güncellenir.

## 1. Depoları yan yana klonla

`TARLA-ANALİZ/` altına: `tarlaanaliz-contract` · `tarlaanaliz-platform`
(`--recurse-submodules`) · `tarlaanaliz-edge` (GitHub adı `tarlaanaliz_edgekiosk`) ·
`tarlaanaliz-worker` (GitHub adı `tarlaanaliz_worker`). Klasör adları BU adlar olmalı —
işaretçideki içe-alma yolu buna göre çözülür.

## 2. Kök işaretçiyi oluştur

`TARLA-ANALİZ/CLAUDE.md` dosyasını aynen şu içerikle oluştur (içe-alma satırı bu kod
bloğunun İÇİNDE etkisizdir — Claude Code çitli blokları içe-alma taramasından muaf tutar;
gerçek dosyada blok dışında olacak):

```markdown
# TARLA-ANALİZ — Çalışma Alanı

> Bu klasör bir git deposu **değildir**, bu yüzden bu dosya git ile taşınmaz.
> Kural gövdesi bu dosyada **tutulmaz** — git'te, `tarlaanaliz-contract` içinde yaşar ve
> aşağıdaki satırla bağlama alınır. Böylece kurallar sürümlenir, PR'da incelenir ve
> ikinci makineye git ile gider. **Kuralı burada değil, o dosyada değiştir.**

@tarlaanaliz-contract/docs/workspace/calisma-alani-kurallari.md

> **İçe-alma doğrulaması:** üstteki satır çalıştıysa bağlamında
> `KURAL-GOVDESI-YUKLENDI-7Q4X` dizesi vardır (gövdenin son satırı). Yoksa içe-alma
> ÇALIŞMIYOR demektir — gövdeyi elle oku:
> `tarlaanaliz-contract/docs/workspace/calisma-alani-kurallari.md`

Yeni makinede kurulum: `tarlaanaliz-contract/docs/workspace/KURULUM.md`
```

## 3. Ayarlar (5 konum)

- **Kök:** `claude-settings-kok.json` → `TARLA-ANALİZ/.claude/settings.json` olarak
  kopyala ve içindeki kanca `-File` **mutlak yolunu kendi klon yoluna göre düzelt**.
- **4 depo:** her birinde `.claude/settings.json` şu tek anahtarla yeter:
  `{ "autoMemoryDirectory": "~/.claude/memory/tarlaanaliz" }`
  (kökteki `permissions.deny` git_token blokları da önerilir — şablondan al).

## 4. Kanca (SessionStart)

Kanca gövdesi bu depoda: `oturum-basi-hook.ps1`. Kök settings **doğrudan bu dosyayı**
işaret eder — kopyalamaya gerek YOK (tek kaynak; `git pull` kancayı da günceller).

- ⚠️ Dosya **UTF-8 BOM'lu** olmalı (PowerShell 5.1 BOM'suz UTF-8'de Türkçe'yi bozar).
  Git BOM'u içerikle birlikte taşır; dosyayı bir araçla yeniden yazarsan BOM'u geri koy
  (reçete dosyanın baş yorumunda).
- ⚠️ Kanca **çalışma ağacından** koşar: eski bir commit'e `checkout` edersen eski kanca
  koşar. Ana dalda kal.
- Ölçüldü (2026-08-18): yol içinde Türkçe `İ` varken `powershell.exe -File` sorunsuz;
  çıktı JSON + Türkçe karakterler sağlam.

## 5. Doğrulama — kur-bitti sayma, ÖLÇ

1. `TARLA-ANALİZ/` içinden `claude` başlat → ilk yanıttan önce "Oturum başı hatırlatma"
   görünmeli (kanca çalıştı).
2. Claude'a sor: *"bağlamında KURAL-GOVDESI-YUKLENDI-7Q4X geçiyor mu?"* → EVET olmalı
   (içe-alma çalıştı).
3. `/context` → Memory files altında kök `CLAUDE.md` listelenmeli.
4. ⚠️ Bir DEPONUN içinden başlatınca içe-alma çalışma dizininin DIŞINA çözülür →
   Claude Code **bir kez onay diyaloğu** gösterir; ONAYLA. Reddedersen gövde yüklenmez
   ve diyalog bir daha çıkmaz (kanonik davranış).

## Makine-yerel kalanlar (git taşımaz — bilerek)

Kök işaretçi (adım 2'de elle) · 5 `settings.json` (adım 3) · `~/.claude/memory/tarlaanaliz/`
hafızası (sıfırdan birikir; gerekçe gövde §6'da).
