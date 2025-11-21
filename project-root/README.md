# Project Root

Estrutura de exemplo:

```
project-root/
├─ bot.py
├─ agent.py
├─ trader.py
├─ watcher.py
├─ project_checker.py
├─ requirements.txt
├─ README.md
├─ .env.example
├─ .gitignore
└─ utils.py
```

Uso rápido

- Instalar dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Criar um `.env` com base em `.env.example` e rodar o bot:

```bash
cp .env.example .env
python bot.py --mode run
```

Scripts úteis

- Rodar verificação rápida de arquivos:

```bash
python project_checker.py
```

