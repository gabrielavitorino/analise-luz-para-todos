from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from config import DOMICILIOS_URL, RAW_DIR, RECURSOS_URL


def download(url: str, destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(
        url,
        timeout=120,
        headers={"User-Agent": "analise-luz-para-todos/1.0"},
    )
    response.raise_for_status()
    destination.write_bytes(response.content)
    return {
        "arquivo": destination.name,
        "url": url,
        "bytes": len(response.content),
        "sha256": hashlib.sha256(response.content).hexdigest(),
        "baixado_em_utc": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    manifests = [
        download(DOMICILIOS_URL, RAW_DIR / "domicilios_atendidos.csv"),
        download(RECURSOS_URL, RAW_DIR / "recursos_aplicados.csv"),
    ]
    (RAW_DIR / "manifest.json").write_text(
        json.dumps(manifests, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("Dados oficiais baixados com sucesso.")


if __name__ == "__main__":
    main()
