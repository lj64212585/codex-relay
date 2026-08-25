from __future__ import annotations

import sys

from relay_installer import main


if __name__ == "__main__":
    raise SystemExit(main(["--desktop", *sys.argv[1:]]))
