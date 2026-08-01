# Project Zomboid Admin Server & Cloud ARM Server Setup

Este é um projeto para gerenciar um servidor de Project Zomboid rodando em uma instância na nuvem da Oracle (arquitetura ARM/aarch64). Ele foi refatorado para usar **Docker**, facilitar o deploy via **uv** e permitir a configuração via **variáveis de ambiente**.

## Arquitetura

O projeto é composto por:
1. **Django Admin Server**: Uma aplicação web para gerenciar o servidor (iniciar, parar, resetar o mundo).
2. **PostgreSQL**: Banco de dados para a aplicação Django.
3. **Redis**: Cache para o Django.
4. **Zomboid Server (ARM)**: O servidor de Project Zomboid que roda usando emulação (box86/box64) já configurada dentro de uma imagem Docker, voltada para processadores ARM como os da Oracle Cloud.

## Requisitos

- **Docker** e **Docker Compose** instalados na sua instância da Oracle Cloud.
- **Git** para clonar o repositório.

## Variáveis de Ambiente

Os caminhos hardcoded nos scripts shell (`start_pz.sh`, `stop_pz.sh`, etc) foram substituídos por variáveis de ambiente. Você pode configurá-los no `docker-compose.yml` ou exportá-los no seu ambiente:
- `PZ_USER` (padrão: `pzuser`)
- `SCREEN_NAME` (padrão: `pzserver`)
- `SERVER_DIR` (padrão: `/home/pzuser/Steam/steamapps/common/Project Zomboid Dedicated Server`)
- `SAVE_DIR` (padrão: `/home/pzuser/Zomboid/Saves/Multiplayer/servertest`)
- `PZ_ADMIN_PASSWORD`: A senha de administrador do servidor Zomboid (configure no `docker-compose.yml`).

## Como Rodar

### 1. Preparação

Clone o repositório e navegue até a pasta do projeto:
```bash
git clone <seu-repo>
cd admin-server
```

### 2. Construir e Iniciar os Containers

Devido à arquitetura ARM, o build do servidor do Zomboid (`Dockerfile.zomboid`) fará o download e compilação do `box86` e `box64`. Isso pode demorar vários minutos.

Para construir as imagens e iniciar tudo, rode:

```bash
docker compose up --build -d
```

Isso subirá 4 containers:
- `adminserver-web` (na porta 8000)
- `adminserver-db` (Postgres)
- `adminserver-redis` (Redis)
- `zomboid-server` (nas portas UDP 16261, 16262, etc)

### 3. Executar as Migrações do Django

A primeira vez que iniciar a aplicação Django, você precisará aplicar as migrações no banco de dados Postgres:

```bash
docker compose exec web uv run python manage.py migrate
docker compose exec web uv run python manage.py createsuperuser
```

### 4. Integração do Admin Server com o Zomboid Container

Se você desejar que o Admin Server controle o servidor Zomboid via Docker (já que estão em containers separados), os scripts shell podem ser adaptados para usar comandos `docker` uma vez que o socket do Docker (`/var/run/docker.sock`) já está montado no container `web`.

Atualmente, os scripts mantêm compatibilidade para uso com `screen` caso você decida rodar o servidor Zomboid diretamente no host.

### 5. Portas do Firewall da Oracle

Certifique-se de acessar o painel de controle da Oracle Cloud e abrir as seguintes portas nas Regras de Entrada (Ingress Rules) do Firewall:
- `8000` (TCP) - Para o Admin Server
- `16261`, `16262`, `8766`, `27015` (UDP) - Para o servidor do Project Zomboid

## Gerenciamento de Dependências (uv)

A aplicação Django agora usa o **uv** para gerenciar dependências. O arquivo de configuração está localizado em `adminserver/pyproject.toml`.

Caso queira rodar o Django localmente sem o Docker:
```bash
cd adminserver
uv pip install -r pyproject.toml
uv run python manage.py runserver
```