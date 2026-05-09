#!/usr/bin/env python3
from __future__ import annotations

import uvicorn

from workbench.config import Settings


def main() -> int:
    settings = Settings()
    uvicorn.run("workbench.app:app", host=settings.host, port=settings.port, reload=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
