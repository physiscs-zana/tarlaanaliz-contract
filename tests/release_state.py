"""Tur/release durumunun TEK makine-okunur kaynağı (KADEME 0 / D1·D5·D6).

Bir contract turu (C0…C8) boyunca iki şey **bilerek** yarım kalır:

  1. Agrega checksum yeniden pinlenmez — ara re-pin, yayımlanmış `vX.Y.Z` etiketinin
     checksum anlamını bozar. Tek re-pin noktası **C8 release törenidir**.
  2. Vendored kopyalar kanoniğin gerisinde kalır — yayılım da C8'de yapılır
     (`tests/test_vendored_parity.py` → `PENDING_PROPAGATION`).

Bu iki "beklenen kırmızı" eskiden **ağızdan** beyan ediliyordu (oturum notunda bir cümle).
Sonuç: kırmızının hangisinin beklenen, hangisinin gerçek olduğu ölçülemiyordu ve
"beklenen kırmızı" mazereti bayatlayabiliyordu.

Artık beyan **tek yerde ve makine-okunur**:

    CONTRACTS_VERSION.md → `**Checksum State:** PENDING_REPIN — ...`

Bunu üç kapı okur:
  * `.github/workflows/contract_validation.yml` → `verify-checksums` işi
  * `tests/test_pin_version.py::test_real_repo_checksum_verifies` → `xfail(strict=True)`
  * `tests/test_vendored_parity.py::test_pending_propagation_is_empty` → `xfail(strict=True)`

**Kendini temizler:** `tools/pin_version.py` CONTRACTS_VERSION.md'yi baştan ürettiği için
C8 re-pin'inde bu satır kaybolur → üç kapı da aynı anda sertleşir. Beyanı C8'den ÖNCE elle
silmek, kapıları yalan söyletmek değil, tam tersine **erken sertleştirmek** olur: testler
gerçek kırmızıya döner (bkz. `docs/checklists/SDLC_GATES.md` §3A).
"""

from __future__ import annotations

import re
from pathlib import Path


CONTRACTS_VERSION = Path(__file__).resolve().parents[1] / "CONTRACTS_VERSION.md"

_DECLARATION = re.compile(r"^\*\*Checksum State:\*\*\s*PENDING_REPIN", re.M)


def repin_pending() -> bool:
    """CONTRACTS_VERSION.md tur-içi `PENDING_REPIN` beyanı taşıyor mu?"""
    try:
        return bool(_DECLARATION.search(CONTRACTS_VERSION.read_text(encoding="utf-8")))
    except OSError:
        return False


#: Modül yüklenirken bir kez okunur — işaret (marker) koşulları import zamanında gerekir.
REPIN_PENDING: bool = repin_pending()
