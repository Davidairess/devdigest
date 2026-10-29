import json
from pathlib import Path
from typing import List

CONFIG_DIR = Path.home() / ".devdigest"
CONFIG_FILE = CONFIG_DIR / "watchlist.json"

DEFAULT_WATCHLIST = [
    "fastapi/fastapi",
    "tailwindlabs/tailwindcss",
    "encode/httpx"
]

def ensure_config() -> List[str]:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_watchlist(DEFAULT_WATCHLIST)
        return DEFAULT_WATCHLIST

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("repos", DEFAULT_WATCHLIST)
    except Exception:
        return DEFAULT_WATCHLIST

def save_watchlist(repos: List[str]):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"repos": sorted(list(set(repos)))}, f, indent=2)

def add_repo(owner_repo: str) -> bool:
    current = ensure_config()
    clean = owner_repo.strip().lower()
    if "/" not in clean:
        raise ValueError("Formato inválido. Use 'owner/repo' (ex: facebook/react)")
    if clean not in current:
        current.append(clean)
        save_watchlist(current)
        return True
    return False

def remove_repo(owner_repo: str) -> bool:
    current = ensure_config()
    clean = owner_repo.strip().lower()
    if clean in current:
        current.remove(clean)
        save_watchlist(current)
        return True
    return False

def list_repos() -> List[str]:
    return ensure_config()
