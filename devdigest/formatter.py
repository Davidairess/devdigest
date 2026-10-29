from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from devdigest.models import DigestSummary
from typing import List

console = Console()

def print_banner():
    banner = Text()
    banner.append("🤖 DevDigest ", style="bold cyan")
    banner.append("v0.1.0 - Inteligência de Changelogs & Releases com IA", style="dim")
    console.print(Panel(banner, border_style="cyan"))

def display_digest(digest: DigestSummary):
    ai_tag = "[bold green]🤖 IA (Gemini)[/]" if digest.ai_generated else "[dim]⚡ Motor Heurístico Local[/]"

    header_text = Text()
    header_text.append(f"📦 {digest.repo} ", style="bold white")
    header_text.append(f"({digest.version})\n", style="bold yellow")
    header_text.append(f"Publicado em: {digest.published_at[:10]} | Link: {digest.html_url}\n", style="dim")
    header_text.append(f"Modo: {ai_tag}")

    console.print(Panel(header_text, border_style="blue"))

    # 1. Breaking Changes
    if digest.breaking_changes:
        console.print("[bold red]🚨 BREAKING CHANGES (Atenção Necessária):[/bold red]")
        for b in digest.breaking_changes:
            console.print(f"  [red]•[/red] {b}")
        console.print()
    else:
        console.print("[bold green]✔ Nenhuma breaking change crítica detectada.[/bold green]\n")

    # 2. Key Features
    if digest.key_features:
        console.print("[bold cyan]🚀 Principais Novidades & Recursos:[/bold cyan]")
        for f in digest.key_features:
            console.print(f"  [cyan]•[/cyan] {f}")
        console.print()

    # 3. Bug Fixes
    if digest.bug_fixes:
        console.print("[bold yellow]🛠️ Correções Importantes:[/bold yellow]")
        for fix in digest.bug_fixes:
            console.print(f"  [yellow]•[/yellow] {fix}")
        console.print()

    # 4. Migration Advice
    console.print(Panel(
        f"[bold white]💡 Dica de Migração:[/bold white]\n{digest.migration_advice}",
        border_style="magenta",
        title="Guia Rápido"
    ))
    console.print()

def generate_markdown_report(digests: List[DigestSummary]) -> str:
    md = ["# 📰 DevDigest - Relatório Técnico de Releases\n"]
    md.append("> Gerado automaticamente via **DevDigest CLI**\n\n---\n")

    for d in digests:
        md.append(f"## 📦 [{d.repo}]({d.html_url}) - `{d.version}`\n")
        md.append(f"**Data de Lançamento:** {d.published_at[:10]}  \n")
        md.append(f"**Motor:** {'Inteligência Artificial (Gemini)' if d.ai_generated else 'Heurístico Local'}\n\n")

        if d.breaking_changes:
            md.append("### 🚨 Breaking Changes\n")
            for b in d.breaking_changes:
                md.append(f"- ⚠️ {b}\n")
            md.append("\n")
        else:
            md.append("✅ *Nenhuma breaking change crítica nesta versão.*\n\n")

        if d.key_features:
            md.append("### 🚀 Principais Novidades\n")
            for f in d.key_features:
                md.append(f"- {f}\n")
            md.append("\n")

        if d.bug_fixes:
            md.append("### 🛠️ Correções de Bugs\n")
            for fix in d.bug_fixes:
                md.append(f"- {fix}\n")
            md.append("\n")

        md.append(f"> **💡 Conselho de Atualização:** {d.migration_advice}\n\n---\n")

    return "".join(md)
