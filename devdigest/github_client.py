import os
from typing import Optional, Dict, Any
import httpx
from devdigest.models import ReleaseInfo

GITHUB_API_BASE = "https://api.github.com"

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "DevDigest-CLI/0.1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def get_latest_release(self, repo: str) -> ReleaseInfo:
        clean_repo = repo.strip()
        url = f"{GITHUB_API_BASE}/repos/{clean_repo}/releases/latest"

        with httpx.Client(timeout=10.0, headers=self.headers) as client:
            resp = client.get(url)

            if resp.status_code == 404:
                # Se não tem 'releases' publicadas, tenta a lista de tags
                tags_url = f"{GITHUB_API_BASE}/repos/{clean_repo}/tags"
                tags_resp = client.get(tags_url)
                if tags_resp.status_code == 200 and tags_resp.json():
                    tag = tags_resp.json()[0]
                    return ReleaseInfo(
                        repo=clean_repo,
                        tag_name=tag["name"],
                        name=f"Release {tag['name']}",
                        published_at="Recente",
                        body="Changelog não publicado formalmente no GitHub Releases; release gerada via Git Tag.",
                        html_url=f"https://github.com/{clean_repo}/releases/tag/{tag['name']}"
                    )
                raise ValueError(f"Nenhuma release ou tag encontrada para o repositório '{clean_repo}'.")

            if resp.status_code == 403:
                raise PermissionError("Limite de requisições da API do GitHub atingido. Defina a variável GITHUB_TOKEN para 5000 req/h.")

            if resp.status_code != 200:
                raise ValueError(f"Erro ao buscar releases de '{clean_repo}': {resp.status_code} {resp.text}")

            data = resp.json()
            return ReleaseInfo(
                repo=clean_repo,
                tag_name=data.get("tag_name", "latest"),
                name=data.get("name") or data.get("tag_name"),
                published_at=data.get("published_at", "Desconhecido"),
                body=data.get("body") or "Nenhum changelog em texto fornecido.",
                html_url=data.get("html_url", f"https://github.com/{clean_repo}")
            )
