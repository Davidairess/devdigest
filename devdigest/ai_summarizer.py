import os
import re
import json
from typing import Optional, Dict, Any, List
import httpx
from devdigest.models import ReleaseInfo, DigestSummary

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

class AISummarizer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

    def summarize(self, release: ReleaseInfo, force_offline: bool = False) -> DigestSummary:
        if self.api_key and not force_offline:
            try:
                return self._summarize_with_gemini(release)
            except Exception as e:
                # Fallback gracioso para o motor heurístico em caso de erro na API
                summary = self._summarize_heuristically(release)
                summary.migration_advice += f" (Nota: IA indisponível, fallback ativo: {str(e)})"
                return summary

        return self._summarize_heuristically(release)

    def _summarize_with_gemini(self, release: ReleaseInfo) -> DigestSummary:
        prompt = f"""
Você é um especialista sênior em engenharia de software e Developer Relations.
Analise as notas de lançamento (changelog) abaixo para o repositório '{release.repo}', versão '{release.tag_name}'.
Extraia um resumo técnico de alto valor para outros desenvolvedores.

Changelog Bruto:
{release.body[:6000]}

Responda ESTRITAMENTE em formato JSON com as seguintes chaves:
{{
  "breaking_changes": ["lista de mudanças que quebram compatibilidade ou exigem atenção imediata. Se nenhuma, array vazio []"],
  "key_features": ["lista das 3 a 5 principais novidades/recursos mais impactantes"],
  "bug_fixes": ["lista de 2 a 4 correções críticas"],
  "migration_advice": "uma ou duas frases com recomendação prática para quem vai atualizar"
}}
"""
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        url = f"{GEMINI_API_URL}?key={self.api_key}"
        with httpx.Client(timeout=20.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code != 200:
                raise ValueError(f"Gemini API Error {resp.status_code}: {resp.text}")

            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text)

            return DigestSummary(
                repo=release.repo,
                version=release.tag_name,
                published_at=release.published_at,
                html_url=release.html_url,
                breaking_changes=parsed.get("breaking_changes", []),
                key_features=parsed.get("key_features", []),
                bug_fixes=parsed.get("bug_fixes", []),
                migration_advice=parsed.get("migration_advice", "Atualização direta recomendada."),
                ai_generated=True
            )

    def _summarize_heuristically(self, release: ReleaseInfo) -> DigestSummary:
        """
        Motor heurístico rápido que parseia seções markdown típicas do GitHub
        quando a IA não está configurada ou em modo offline.
        """
        lines = release.body.splitlines()
        breaking = []
        features = []
        fixes = []

        current_section = None
        for line in lines:
            stripped = line.strip()
            lower = stripped.lower()

            if any(h in lower for h in ["# breaking", "breaking changes", "breaking:"]):
                current_section = "breaking"
                continue
            elif any(h in lower for h in ["# features", "# new features", "highlights", "what's new"]):
                current_section = "features"
                continue
            elif any(h in lower for h in ["# fixes", "# bug fixes", "bugfixes"]):
                current_section = "fixes"
                continue
            elif stripped.startswith("#"):
                current_section = "other"
                continue

            # Captura bullets
            if stripped.startswith(("-", "*", "•")) and len(stripped) > 4:
                item = stripped.lstrip("-*• ").strip()
                # Remove links de PR (#123) e menções (@user)
                item = re.sub(r"\(#\d+\)", "", item)
                item = re.sub(r"by @[\w-]+", "", item)
                item = re.sub(r"in https://github\.com/\S+", "", item).strip()

                if current_section == "breaking" or "breaking" in item.lower():
                    breaking.append(item)
                elif current_section == "fixes" or "fix" in item.lower():
                    if len(fixes) < 5:
                        fixes.append(item)
                else:
                    if len(features) < 5:
                        features.append(item)

        # Fallbacks caso o changelog não tenha headers padronizados
        if not features and not breaking and not fixes and lines:
            for line in lines:
                s = line.strip().lstrip("-*• ")
                if s and len(s) > 10 and not s.startswith("<") and not s.startswith("#"):
                    features.append(s[:120])
                if len(features) >= 4:
                    break

        return DigestSummary(
            repo=release.repo,
            version=release.tag_name,
            published_at=release.published_at,
            html_url=release.html_url,
            breaking_changes=breaking[:5],
            key_features=features[:5],
            bug_fixes=fixes[:5],
            migration_advice="Revisão padrão de changelog recomendada antes de atualizar em produção.",
            ai_generated=False
        )
