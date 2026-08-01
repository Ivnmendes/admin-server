#!/bin/bash
# Script para iniciar o servidor Project Zomboid

PZ_USER="${PZ_USER:-pzuser}"
SCREEN_NAME="${SCREEN_NAME:-pzserver}"
SERVER_DIR="${SERVER_DIR:-/home/pzuser/Steam/steamapps/common/Project Zomboid Dedicated Server}"

# Verifica se a sessão screen já existe
if sudo -u $PZ_USER screen -list | grep -q "$SCREEN_NAME"; then
    echo "O servidor já está rodando na sessão screen '$SCREEN_NAME'."
else
    echo "Iniciando o servidor..."
    # Executa o comando de start como o usuário pzuser dentro de uma nova sessão screen
    sudo -u $PZ_USER screen -dmS $SCREEN_NAME bash -c "cd '$SERVER_DIR' && ./start-server.sh"
    echo "Servidor iniciado na sessão screen '$SCREEN_NAME'."
fi
