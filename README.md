# Project Zomboid Admin Server & Cloud ARM Server Setup (Native Host)

Este é um projeto para gerenciar um servidor de Project Zomboid rodando em uma instância na nuvem da Oracle (arquitetura ARM/aarch64). Esta arquitetura roda de forma **nativa no Host** (sem isolar a aplicação no Docker), garantindo máxima performance, facilidade de debugging e que o Django possa interagir diretamente com o processo do Zomboid.

## Arquitetura

O projeto é composto por:
1. **Zomboid Server (ARM)**: O servidor de Project Zomboid que roda usando emulação (box86/box64) nativamente no seu Ubuntu (via script `arm64_zomboid_server`).
2. **Django Admin Server**: Uma aplicação web gerenciada pelo `uv` rodando no host para gerenciar o servidor.
3. **PostgreSQL & Redis**: Rodam em containers Docker isolados apenas para persistência de dados e cache (leve e fácil).

## Requisitos

- Máquina Ubuntu na Oracle Cloud.
- **Docker** e **Docker Compose** instalados (apenas para o Banco de Dados).
- Portas liberadas na Oracle (VCN Ingress Rules) e no Ubuntu (iptables/ufw):
  - `8000` (TCP) - Painel Admin
  - `16261`, `16262`, `8766`, `27015` (UDP) - Jogo Zomboid

## Passo 1: Instalar o Servidor do Zomboid no Host

Siga as instruções originais contidas na pasta `zomboid-arm` para compilar e instalar o Zomboid nativamente. Esse processo vai compilar os emuladores para o processador ARM da Oracle:

```bash
cd zomboid-arm
chmod +x arm64_zomboid_server
sudo bash arm64_zomboid_server
```

*(O script vai pedir para você definir a senha de admin do servidor Zomboid e criar um serviço systemd).*

## Passo 2: Instalar e Configurar o Painel Admin (Django)

Eu criei um script automático (`setup_admin_server.sh`) que sobe o banco de dados via Docker e instala todo o ambiente do Django na sua máquina usando o gerenciador super rápido `uv`.

Volte para a pasta raiz do projeto e rode:

```bash
chmod +x setup_admin_server.sh
./setup_admin_server.sh
```

*(No final do script, ele vai pedir para você criar um usuário e senha para entrar no painel).*

## Passo 3: Rodar o Painel Admin

Sempre que quiser rodar o painel para gerenciar o seu jogo:

```bash
cd adminserver
source .venv/bin/activate
gunicorn --bind 0.0.0.0:8000 adminserver.wsgi:application
```

Acesse no seu navegador: `http://163.176.128.68:8000/`

---
### Observações Importantes
- Os scripts de inicialização do painel (`start_pz.sh`, `stop_pz.sh`) foram atualizados para ler as variáveis de ambiente com fallback para os caminhos e usuários padrão do script `arm64_zomboid_server`. Eles continuarão abrindo o servidor em uma sessão `screen` de forma transparente.
- Se o IP da máquina na Oracle mudar, edite o arquivo `adminserver/adminserver/settings.py` e adicione o novo IP em `ALLOWED_HOSTS`.