from pydantic import BaseModel, Field
from typing import List, Optional

class ReleaseInfo(BaseModel):
    repo: str
    tag_name: str
    name: Optional[str] = None
    published_at: str
    body: str = ""
    html_url: str

class DigestSummary(BaseModel):
    repo: str
    version: str
    published_at: str
    html_url: str
    breaking_changes: List[str] = Field(default_factory=list)
    key_features: List[str] = Field(default_factory=list)
    bug_fixes: List[str] = Field(default_factory=list)
    migration_advice: str = "Nenhuma ação especial de migração necessária."
    ai_generated: bool = False
