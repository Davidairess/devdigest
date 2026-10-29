import sys
from pathlib import Path

# Garante suporte seguro a UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import click
from rich.console import Console
from rich.table import Table

from devdigest.github_client import GitHubClient
from devdigest.ai_summarizer import AISummarizer
from devdigest.config import list_repos, add_repo, remove_repo
from devdigest.formatter import print_banner, display_digest, generate_markdown_report

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--repo", "-r", help="Repositório específico para resumir (ex: fastapi/fastapi)")
@click.option("--export", "-e", type=click.Path(), help="Exportar relatório para arquivo Markdown")
@click.option("--offline", is_flag=True, help="Forçar motor heurístico local sem chamar a API de IA")
def main(ctx, repo: str, export: str, offline: bool):
    """🤖 DevDigest: Inteligência artificial para changelogs de software."""
    if ctx.invoked_subcommand is None:
        run_digest(target_repo=repo, export_path=export, force_offline=offline)

def run_digest(target_repo: str = None, export_path: str = None, force_offline: bool = False):
    print_banner()

    repos_to_scan = [target_repo] if target_repo else list_repos()

    if not repos_to_scan:
        console.print("[yellow]Nenhum repositório na lista de monitoramento. Use 'devdigest track owner/repo'[/yellow]")
        return

    client = GitHubClient()
    summarizer = AISummarizer()
    digests = []

    with console.status("[bold blue]Buscando releases e analisando changelogs com IA...[/bold blue]"):
        for repo_name in repos_to_scan:
            try:
                release_info = client.get_latest_release(repo_name)
                digest = summarizer.summarize(release_info, force_offline=force_offline)
                digests.append(digest)
            except Exception as e:
                console.print(f"[bold red]✖ Erro ao processar {repo_name}:[/bold red] {str(e)}")

    if not digests:
        return

    # Exibe no terminal
    for d in digests:
        display_digest(d)

    # Exporta se solicitado
    if export_path:
        md_content = generate_markdown_report(digests)
        out_file = Path(export_path)
        out_file.write_text(md_content, encoding="utf-8")
        console.print(f"[bold green]✔ Relatório Markdown exportado com sucesso para:[/] [cyan]{out_file.resolve()}[/]")

@main.command()
@click.option("--repo", "-r", help="Repositório específico para resumir")
@click.option("--export", "-e", type=click.Path(), help="Salvar em arquivo Markdown")
@click.option("--offline", is_flag=True, help="Forçar motor local offline")
def digest(repo: str, export: str, offline: bool):
    """Gera o resumo técnico das últimas releases monitoradas."""
    run_digest(target_repo=repo, export_path=export, force_offline=offline)

@main.command()
@click.argument("repo")
def track(repo: str):
    """Adiciona um repositório para ser monitorado (ex: devdigest track facebook/react)."""
    try:
        added = add_repo(repo)
        if added:
            console.print(f"[bold green]✔ Repositório '{repo}' adicionado à sua watchlist![/bold green]")
        else:
            console.print(f"[yellow]O repositório '{repo}' já está sendo monitorado.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Erro:[/bold red] {str(e)}")

@main.command()
@click.argument("repo")
def untrack(repo: str):
    """Remove um repositório da lista de monitoramento."""
    removed = remove_repo(repo)
    if removed:
        console.print(f"[bold green]✔ Repositório '{repo}' removido com sucesso.[/bold green]")
    else:
        console.print(f"[yellow]O repositório '{repo}' não estava na sua lista.[/yellow]")

@main.command(name="list")
def list_watchlist():
    """Lista todos os repositórios atualmente monitorados."""
    print_banner()
    repos = list_repos()
    if not repos:
        console.print("[yellow]Sua watchlist está vazia.[/yellow]")
        return

    table = Table(title="📋 Repositórios Monitorados pelo DevDigest", style="cyan", border_style="cyan")
    table.add_column("Repositório", style="bold white")
    table.add_column("Link no GitHub", style="dim")

    for r in repos:
        table.add_row(r, f"https://github.com/{r}")

    console.print(table)

if __name__ == "__main__":
    main()
