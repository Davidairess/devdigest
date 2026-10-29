import pytest
from unittest.mock import MagicMock
from devdigest.models import ReleaseInfo
from devdigest.ai_summarizer import AISummarizer
from devdigest.formatter import generate_markdown_report
from devdigest.config import add_repo, remove_repo, list_repos

def test_heuristic_summarizer_sections():
    raw_body = """
    ## Breaking Changes
    - Drop support for Python 3.8 (#100)
    - Rename `client.execute()` to `client.send()` (#102)

    ## Features
    - Add native WebSocket support (#105)
    - New high-speed parser engine

    ## Bug Fixes
    - Fix memory leak on long connections (#110)
    """

    release = ReleaseInfo(
        repo="owner/cool-repo",
        tag_name="v2.0.0",
        published_at="2026-10-25T12:00:00Z",
        body=raw_body,
        html_url="https://github.com/owner/cool-repo/releases/v2.0.0"
    )

    summarizer = AISummarizer()
    digest = summarizer.summarize(release, force_offline=True)

    assert digest.repo == "owner/cool-repo"
    assert digest.version == "v2.0.0"
    assert len(digest.breaking_changes) >= 1
    assert any("Python 3.8" in b for b in digest.breaking_changes)
    assert len(digest.key_features) >= 1
    assert any("WebSocket" in f for f in digest.key_features)
    assert len(digest.bug_fixes) >= 1

def test_markdown_report_generation():
    raw_body = "## Highlights\n- Performance improvements"
    release = ReleaseInfo(
        repo="fastapi/fastapi",
        tag_name="0.115.0",
        published_at="2026-10-20T10:00:00Z",
        body=raw_body,
        html_url="https://github.com/fastapi/fastapi/releases/0.115.0"
    )

    summarizer = AISummarizer()
    digest = summarizer.summarize(release, force_offline=True)

    report = generate_markdown_report([digest])
    assert "# 📰 DevDigest" in report
    assert "fastapi/fastapi" in report
    assert "0.115.0" in report

def test_config_operations(tmp_path, monkeypatch):
    test_file = tmp_path / "watchlist.json"
    monkeypatch.setattr("devdigest.config.CONFIG_FILE", test_file)
    monkeypatch.setattr("devdigest.config.CONFIG_DIR", tmp_path)

    add_repo("golang/go")
    assert "golang/go" in list_repos()

    remove_repo("golang/go")
    assert "golang/go" not in list_repos()
