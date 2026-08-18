# TarlaAnaliz - SessionStart kancasi (hook).
# Her oturum basinda (yeni / devam / clear / compact / fork) Claude'un baglamina kisa bir
# hatirlatma enjekte eder. Hizli olmali: disk/ag islemi YOK.
#
# TASARIM (2026-08-18): Bu mesaj BILEREK kisa tutuldu. Eskiden 44 satirdi ve kok
# CLAUDE.md'nin §2/§4/§6'sini yeniden anlatiyordu -- ayni kurallar baglamda iki kez
# duruyordu. Kanonik Opus 5 rehberi uzun bir istemin SONUNA "kisa bir hatirlatma"
# koymayi onerir (ornegi 2 satir), tam bir tekrar degil. Kancanin isi: (a) daimi iki
# kurali one cikarmak (b) tek-kaynak dosyalarina isaret etmek (c) /compact sonrasi
# ayakta kalmak -- alt dizin CLAUDE.md'leri sikistirma sonrasi yeniden enjekte EDILMEZ.
# Buraya kural GOVDESI eklemeyin; govde kok CLAUDE.md'de yasar.
#
# ENCODING UYARISI: bu dosya UTF-8 + BOM olarak kaydedilmelidir. PowerShell 5.1
# BOM'suz UTF-8'i ANSI sanip Turkce karakterleri bozar. Bir arac ile yeniden yazarsan
# BOM'u geri ekle:
#   $p="C:\Users\Bilgisayar\.claude\hooks\tarlaanaliz-oturum-basi.ps1"
#   [IO.File]::WriteAllText($p,[IO.File]::ReadAllText($p),(New-Object Text.UTF8Encoding $true))

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
if ([Console]::IsInputRedirected) { $null = [Console]::In.ReadToEnd() }

$mesaj = @'
## Oturum başı hatırlatma — TarlaAnaliz

**Sade dil:** her teknik terim ilk geçtiği yerde parantezle açıklanır.

**İki daimî kural:** ① **Kanıtla** — öneri/bulgu/risk aynı mesajda kanıtıyla yazılır
(`dosya:satır`, komut çıktısı ya da kanonik atıf); kanıtın neyi *desteklemediğini* de söyle;
ölçemiyorsan gündeme getirme. ② **Test = mutasyon + pozitif kontrol** — yeşil test kanıt
değildir; kodu boz, kırmızıya döndüğünü gör, geri al.

**Nerede kalındı?** Yalnız iki dosya söyler (`tarlaanaliz-contract` içinde):
`docs/SESSION_HANDOFF.md` (durum, §0.A en güncel) · `docs/TARLAANALIZ_EYLEM_PLANI_2026-07-30.md`
(iş listesi). Kural gövdeleri: kök `TARLA-ANALİZ/CLAUDE.md` + çalıştığın deponun `CLAUDE.md`'si.

**⚠️ Sıkıştırma (compact) uyarısı:** alt dizin `CLAUDE.md`'leri `/compact` sonrası yeniden
yüklenmez. Bir depoda uzun iş yapacaksan **o deponun içinden** `claude` başlat.

**Kapanışta:** hafıza denetimi (çelişki · depo-durumu iddiaları · indeks tutarlılığı) ve
sonucu tek satırla bildir. Reçete: `~/.claude/memory/tarlaanaliz/hafiza-guncelligi-oturum-sonu.md`.
'@

$cikti = @{
    hookSpecificOutput = @{
        hookEventName     = "SessionStart"
        additionalContext = $mesaj
    }
} | ConvertTo-Json -Depth 5

Write-Output $cikti
