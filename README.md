# 🤖 DevDigest

> **Assistente CLI com IA que transforma changelogs longos e poluídos do GitHub em briefings técnicos executivos.**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20Flash-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

---

## 📌 O Problema
Quantas bibliotecas e frameworks o seu time usa hoje? React, FastAPI, Tailwind, Pydantic, Next.js...
* Ler páginas inteiras de changelogs cheias de merges de bots e nomes de PRs é exaustivo.
* Deixar de notar uma **Breaking Change** em uma atualização de versão menor pode derrubar o ambiente de produção.
* Saber se vale a pena atualizar ou esperar exige análise manual repetitiva.

O **`DevDigest`** monitora os repositórios da sua stack e usa **Inteligência Artificial (Gemini 1.5 Flash)** para sintetizar as novidades com foco cirúrgico no desenvolvedor:
1. 🚨 **Breaking Changes** destacadas no topo.
2. 🚀 **Key Features** sem enrolação técnica.
3. 🛠️ **Bug Fixes** críticos.
4. 💡 **Dica de Migração** com conselhos diretos.

---

## ✨ Funcionalidades

- 🧠 **IA com Gemini:** Prompt engineering especializado em arquitetura de software para extrair o que realmente importa.
- ⚡ **Modo Heurístico Híbrido:** Se você não tiver uma chave de API configurada no momento ou estiver sem internet, o motor heurístico local assume o controle automaticamente.
- 📋 **Watchlist Personalizada:** Adicione ou remova repositórios facilmente (`devdigest track facebook/react`).
- 📄 **Exportação Markdown:** Gere relatórios técnicos completos em Markdown para compartilhar no Slack, Notion ou em reuniões de equipe com `--export digest.md`.
- 🎨 **Terminal Elegante:** Painéis e tabelas estilizadas com a biblioteca `Rich`.

---

## 🖥️ Demonstração Visual

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🤖 DevDigest v0.1.0 - Inteligência de Changelogs & Releases com IA          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─ 📦 fastapi/fastapi (0.115.0) ──────────────────────────────────────────────┐
│ Publicado em: 2026-10-20 | Link: https://github.com/fastapi/fastapi         │
│ Modo: 🤖 IA (Gemini)                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
✔ Nenhuma breaking change crítica detectada.

🚀 Principais Novidades & Recursos:
  • Suporte aprimorado para validação nativa de modelos Pydantic v2.
  • Melhoria no overhead de serialização de respostas assíncronas.

🛠️ Correções Importantes:
  • Correção de vazamento de contexto em middlewares com streaming.

┌─ Guia Rápido ───────────────────────────────────────────────────────────────┐
│ 💡 Dica de Migração:                                                        │
│ Atualização segura e retrocompatível recomendada para projetos em produção. │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalação & Setup

### 1. Clonar o repositório
```bash
git clone https://github.com/Davidairess/devdigest.git
cd devdigest
```

### 2. Configurar o ambiente virtual
```bash
python -m venv .venv

# No Windows:
.\.venv\Scripts\activate

# No Linux / macOS:
source .venv/bin/activate

# Instalar em modo de desenvolvimento
pip install -e .[dev]
```

### 3. Configurar a Chave da IA (Opcional, mas recomendado)
Obtenha uma chave gratuita no [Google AI Studio](https://aistudio.google.com/):

```powershell
# No Windows PowerShell:
$env:GEMINI_API_KEY="sua_chave_aqui"

# No Linux / macOS:
export GEMINI_API_KEY="sua_chave_aqui"
```

*(Se não definir a chave, o DevDigest usará automaticamente o motor heurístico local sem travar).*

---

## 🛠️ Comandos Disponíveis

### Gerar o Digest de todos os repositórios monitorados
```bash
devdigest digest
```

### Resumir apenas um repositório específico
```bash
devdigest digest --repo tailwindlabs/tailwindcss
```

### Exportar relatório para Markdown
```bash
devdigest digest --export resumo-semanal.md
```

### Gerenciar a lista de repositórios
```bash
# Ver a lista atual
devdigest list

# Adicionar um novo projeto
devdigest track facebook/react

# Remover um projeto
devdigest untrack encode/httpx
```

---

## 📂 Estrutura do Projeto

```text
devdigest/
├── .github/workflows/ci.yml   # Pipeline de CI automático
├── devdigest/
│   ├── __init__.py
│   ├── cli.py                 # Interface CLI (Click + Rich)
│   ├── models.py              # Modelos Pydantic (ReleaseInfo, DigestSummary)
│   ├── github_client.py       # Integração com a API de Releases do GitHub
│   ├── ai_summarizer.py       # Pipeline de IA (Gemini) + Motor Heurístico
│   ├── config.py              # Gerenciador de watchlist local
│   └── formatter.py           # Renderizador de painéis e exportador Markdown
├── tests/
│   └── test_digest.py         # Testes automatizados com pytest
├── pyproject.toml             # Empacotamento moderno
├── README.md                  # Documentação do projeto
└── LICENSE                    # Licença MIT
```

---

## 🧪 Testes Automatizados

```bash
pytest -v
```

---

## 📜 Licença
Distribuído sob a licença **MIT**. Veja `LICENSE` para detalhes.
