#!/usr/bin/env python3
"""Betik ağacı kapısı — AL-K32. İki katman: sözdizimi + yasaklı komut.

NEDEN VAR (2026-08-11 ölçümü):
    Bu deponun betik ağacı **tümden kapısızdı**: 3 dosya / 1021 satır, ve workflow'larda
    onları ayrıştıran ya da denetleyen **0 isabet**. Dört yeşil kapı (validate · pytest ·
    redocly · checksum) o satırların hiçbirini görmüyordu.

    Uyarı edge oturumundan geldi: onların yeni kurduğu ayrıştırma kapısı, **hiç
    dokunulmamış** bir dosyada gerçek bir sözdizimi hatası buldu — betik yıllardır
    çalıştırılamıyordu ve donanım sahada olmadığı için görünmüyordu.

    Burada aynı ölçüm yapıldı: **sözdizimi kusuru YOK** (dürüst negatif sonuç).
    Ama kök dizinde yetim ve **koşarsa zararlı** bir betik bulundu
    (`update-contracts.ps1`, tek commit 2026-03-03, çağıranı workflow/belge/test = 0):
    `Downloads` içindeki bir ZIP'i çalışma ağacının **tamamının üstüne** kopyalıyor ve
    bitince kullanıcıya kök `CLAUDE.md`'nin **yasakladığı** toplu ekleme komutunu
    yazdırıyordu. Dosya kaldırıldı; bu kapı sınıfın geri gelmesini engeller.

İKİ KATMAN:
    ① SÖZDİZİMİ — her betik ilgili yorumlayıcının ayrıştırıcısından geçmeli.
       `.sh`/`.bash` → `bash -n` · `.ps1` → PowerShell `Parser::ParseFile`.
    ② YASAKLI KOMUT — ölçülerek seçilmiş dar bir liste. Desenler **meşru kodu
       kırmızıya çevirmeyecek** kadar dar tutuldu; ölçüm (2026-08-11):
         · `sync_to_repos.sh`'teki **4** `git add` kullanımının hepsi **yol-sınırlı**
           (`git add contracts/` gibi) → yasak yalnız `-A` / `--all` / `.` biçimlerine.
         · `generate_types.sh:52`'deki `rm -rf` hedefi `$BASE_DIR/generated`, tırnaklı
           ve `-d` kontrolüyle korumalı → yasak yalnız **çalışma dizini kökünü** silen
           ya da onun üstüne özyinelemeli kopyalayan biçimlere.

⚠️ YORUM SATIRLARI TARANMAZ. Bu bilinçli: bu oturumda **dört kez**, bir kusuru
   *yasaklayan* kapı, kusuru *anlatan* metne takıldı. Bir kuralı betiğin içinde
   gerekçelendirmek mümkün olmalı.

FAIL-CLOSED:
    · Hiç betik bulunamazsa hata döner — keşif bozulmuşsa "0 bulgu" yeşil sayılmaz.
    · `.ps1` varken PowerShell yorumlayıcısı yoksa hata döner; "ölçemedim" ≠ "temiz".

KULLANIM:
    python3 tools/check_scripts.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).parent.parent

#: Uzantı → yorumlayıcı ailesi.
SCRIPT_SUFFIXES = {".sh": "bash", ".bash": "bash", ".ps1": "powershell"}

#: Yorum satırı önekleri (aile başına).
_COMMENT = {"bash": "#", "powershell": "#"}


class Finding(NamedTuple):
    path: str
    line: int
    rule: str
    text: str
    reason: str


class Rule(NamedTuple):
    name: str
    pattern: re.Pattern[str]
    reason: str


FORBIDDEN: list[Rule] = [
    Rule(
        "toplu-ekleme",
        re.compile(r"\bgit\s+add\s+(-A\b|--all\b|\.(?:\s|$))"),
        "Kök CLAUDE.md toplu ekleme komutunu YASAKLAR: paralel oturumda başkasının "
        "satırını sızdırır. Yol-sınırlı biçimi kullanın (`git add -- <yol>`). "
        "Kaldırılan `update-contracts.ps1` bu komutu kullanıcıya yazdırıyordu.",
    ),
    Rule(
        "calisma-agacini-ezme",
        re.compile(
            r"(Copy-Item[^\n]*-Recurse[^\n]*-Force[^\n]*(\(Get-Location\)|\$PWD)"
            r"|Copy-\w+[^\n]*\(Get-Location\)\.Path"
            r"|\bcp\s+-[a-zA-Z]*r[a-zA-Z]*\s+[^\n]*\s+\"?\$?(PWD|\(pwd\))\"?\s*$)"
        ),
        "Çalışma ağacının TAMAMININ üstüne özyinelemeli kopyalama. Kaldırılan betik "
        "tam olarak bunu yapıyordu (Downloads'taki bir ZIP'i depo köküne açıyordu): "
        "izlenen dosyalar sessizce ezilir, git geçmişi bunu bir değişiklik gibi gösterir.",
    ),
    Rule(
        "kok-dizini-silme",
        re.compile(
            r"(\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?\s+\"?(\.|\./|/|\$PWD|\$\(pwd\))\"?\s*(;|$)"
            r"|Remove-Item[^\n]*-Recurse[^\n]*-Force[^\n]*(\(Get-Location\)|\$PWD))"
        ),
        "Çalışma dizini kökünü özyinelemeli siliyor. Hedef her zaman ADLANDIRILMIŞ bir "
        "alt dizin olmalı (örnek: `generate_types.sh` yalnız kendi üretim dizinini "
        "siler, tırnaklı ve varlık kontrolüyle).",
    ),
]


def tracked_scripts(root: Path) -> list[Path]:
    """İZLENEN betik dosyaları. Çalışma ağacı değil, git'in gördüğü ağaç ölçülür."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return []
    return [
        root / rel
        for rel in result.stdout.splitlines()
        if Path(rel).suffix.lower() in SCRIPT_SUFFIXES
    ]


def forbidden_hits(text: str, family: str, path: str = "?") -> list[Finding]:
    """Saf fonksiyon — sentetik olarak sınanabilir. Yorum satırları TARANMAZ."""
    yorum = _COMMENT.get(family, "#")
    bulunan: list[Finding] = []
    for index, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(yorum):
            continue
        for rule in FORBIDDEN:
            if rule.pattern.search(line):
                bulunan.append(Finding(path, index, rule.name, line.strip()[:90], rule.reason))
    return bulunan


def _powershell() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def syntax_errors(path: Path, family: str, base: Path | None = None) -> list[str]:
    """Yorumlayıcının AYRIŞTIRICISINI çağırır — betiği ÇALIŞTIRMAZ.

    ⚠️ Yol DAİMA `base` dizinine **göreli** verilir ve süreç `cwd=base` ile koşar.
    Mutlak Windows yolu geçirmek MSYS `bash`'te sessizce bozuluyor (ölçüldü: sürücü
    harfli yolun ters bölüleri yutuluyor → "No such file or directory" → kapı, dosyayı
    hiç ayrıştırmadan **yanlış kırmızı** verir). Göreli yol + `cwd` iki platformda da
    çalışır ve CI (Linux) ile geliştirme makinesi (Windows) aynı şeyi ölçer.
    """
    base = base or ROOT
    # ⚠️ stdin BAYT olarak verilir. Metin kipinde (`text=True`) Python, boruya yazarken
    # `\n`'i platform satır sonuna GERİ ÇEVİRİR — Windows'ta CR'yi tam da temizledikten
    # sonra yeniden ekler ve `bash -n` yine CRLF hatası verir (ölçüldü). Kapının ölçüm
    # ortamı hedefle (Linux CI) aynı olmalı; bayt kipi bunu garanti eder.
    #
    # 📌 Aşağıdaki `.replace(...)` MUTASYONLA ÖLÇÜLDÜ ve **hiçbir testi öldürmüyor** —
    # bunu gizlemiyoruz: `read_text()` zaten evrensel satır sonu çevirimi yapar, yani
    # CR'ler burada ulaşmadan önce temizlenmiş oluyor. Çağrı **savunma derinliği** olarak
    # duruyor (ileride `read_bytes`'a geçilirse gerekli olur). Gerçek koruma bir alttaki
    # bayt kipidir: onu metin kipine çeviren mutasyon **4 testi** öldürüyor.
    ham = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    veri = ham.encode("utf-8")

    def _coz(b: bytes) -> str:
        return b.decode("utf-8", errors="replace").strip()

    if family == "bash":
        if not shutil.which("bash"):
            return ["bash yorumlayıcısı yok — ayrıştırma yapılamadı (fail-closed)"]
        result = subprocess.run(
            ["bash", "-n"], input=veri, cwd=str(base), capture_output=True,
        )
        return [] if result.returncode == 0 else [_coz(result.stderr) or "bash -n başarısız"]

    shell = _powershell()
    if not shell:
        return ["PowerShell yorumlayıcısı yok — ayrıştırma yapılamadı (fail-closed)"]
    script = (
        "$src=[Console]::In.ReadToEnd();$e=$null;$t=$null;"
        "[System.Management.Automation.Language.Parser]::ParseInput($src,[ref]$t,[ref]$e)|Out-Null;"
        "if($e.Count -gt 0){$e|ForEach-Object{'satir '+$_.Extent.StartLineNumber+': '+$_.Message};exit 1}"
    )
    result = subprocess.run(
        [shell, "-NoProfile", "-NonInteractive", "-Command", script],
        input=veri, cwd=str(base), capture_output=True,
    )
    return [] if result.returncode == 0 else [_coz(result.stdout) or "ayrıştırma başarısız"]


def committed_crlf(root: Path) -> list[str]:
    """İNDEKSTE CRLF taşıyan betikler — Linux'ta çalışmazlar.

    🔴 Bu kontrol, kapının kendi yanlış-kırmızısından doğdu. İlk hâli dosyayı **çalışma
    ağacından** ayrıştırıyordu ve bu makinede (`core.autocrlf=true`) `bash -n` her
    betikte CRLF hatası verdi. Neredeyse *"betikler bozuk"* diye rapor edecektim.

    Ölçüm iddiayı çürüttü — `git ls-files --eol`:

        i/lf  w/lf    tools/generate_types.sh
        i/lf  w/crlf  tools/sync_to_repos.sh

    İndeks (commit'lenen içerik) **LF**; CRLF yalnız Windows checkout'unda. Yani gerçek
    bir kusur yoktu, **kapının ölçüm ortamı hedefle aynı değildi**. Ayrıştırma artık
    CR'siz metin üzerinde yapılıyor (CI ile geliştirme makinesi aynı şeyi ölçer).

    Ama *indekste* CRLF olsaydı bu **gerçek** bir kusur olurdu (Linux'ta betik düşer),
    ve o ayrım kaybolmasın diye ayrı bir kontrol olarak burada duruyor.
    """
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--eol"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        return ["`git ls-files --eol` koşamadı — satır sonu ölçülemedi (fail-closed)"]
    bozuk = []
    for line in result.stdout.splitlines():
        parcalar = line.split("\t")
        if len(parcalar) < 2:
            continue
        yol = parcalar[-1].strip()
        if Path(yol).suffix.lower() not in SCRIPT_SUFFIXES:
            continue
        if "i/crlf" in parcalar[0]:
            bozuk.append(
                f"{yol}: İNDEKSTE CRLF — Linux'ta bu betik ayrıştırılamaz. "
                "Satır sonlarını LF'e çevirin."
            )
    return bozuk


def main() -> int:
    scripts = tracked_scripts(ROOT)
    if not scripts:
        print(
            "HATA: hiç betik bulunamadı. Depoda gerçekten yoksa bu kapı kaldırılmalı; "
            "aksi hâlde keşif bozulmuştur. '0 bulgu' ile '0 dosya taradım' aynı şey "
            "DEĞİLDİR — fail-closed."
        )
        return 1

    # Kaç dosya tarandığını DAİMA bas: sessizce boş küme taramak en sinsi fail-open'dır.
    print(f"taranan betik: {len(scripts)}")
    for path in sorted(scripts):
        print(f"  - {path.relative_to(ROOT).as_posix()}")

    hatalar: list[str] = committed_crlf(ROOT)
    bulgular: list[Finding] = []
    for path in sorted(scripts):
        family = SCRIPT_SUFFIXES[path.suffix.lower()]
        for message in syntax_errors(path, family, ROOT):
            hatalar.append(f"{path.relative_to(ROOT).as_posix()}: {message}")
        bulgular.extend(
            forbidden_hits(
                path.read_text(encoding="utf-8", errors="replace"),
                family,
                path.relative_to(ROOT).as_posix(),
            )
        )

    if hatalar:
        print("\nSÖZDİZİMİ HATASI:")
        for h in hatalar:
            print(f"  {h}")

    if bulgular:
        print("\nYASAKLI KOMUT:")
        for f in bulgular:
            print(f"  {f.path}:{f.line}  [{f.rule}]  {f.text}")
            print(f"      {f.reason}")

    if hatalar or bulgular:
        return 1

    print("\nOK: betik ağacı temiz (sözdizimi + yasaklı komut).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
