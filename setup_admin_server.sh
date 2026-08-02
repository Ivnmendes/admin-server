#!/bin/bash
# Script para configurar e iniciar o Admin Server do Project Zomboid (Django) no Host

echo "1. Subindo Banco de Dados (Postgres) e Cache (Redis) via Docker..."
sudo docker compose up -d

echo "2. Instalando uv (Gerenciador de Dependências Python super rápido)..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
fi

cd adminserver

echo "3. Criando ambiente virtual e instalando dependências do Django via uv..."
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml

echo "4. Aplicando migrações no Banco de Dados..."
uv run python manage.py migrate

echo "5. Coletando arquivos estáticos..."
uv run python manage.py collectstatic --noinput

echo "6. Criando superusuário do Painel Admin (Siga as instruções na tela):"
uv run python manage.py createsuperuser

echo "=========================================================="
echo "Pronto! O ambiente do Django Admin Server está configurado."
echo "Para iniciar o painel Admin agora, basta rodar:"
echo "cd adminserver && source .venv/bin/activate"
echo "gunicorn --bind 0.0.0.0:8000 adminserver.wsgi:application"
echo "=========================================================="
