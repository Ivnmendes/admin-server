#!/bin/bash
# Script para reiniciar o servidor Project Zomboid

PZ_USER="${PZ_USER:-pzuser}"
SCREEN_NAME="${SCREEN_NAME:-pzserver}"
SERVER_DIR="${SERVER_DIR:-/home/pzuser/Steam/steamapps/common/Project Zomboid Dedicated Server}"

echo "Tentando reiniciar o servidor..."

# Para a sessão screen existente, se houver
if sudo -u $PZ_USER screen -list | grep -q "$SCREEN_NAME"; then
    echo "Parando a sessão screen '$SCREEN_NAME'..."
    sudo -u $PZ_USER screen -S $SCREEN_NAME -X quit
    sleep 2 # Dá um tempo para o processo morrer
fi

# Inicia o servidor novamente
echo "Iniciando o servidor..."
sudo -u $PZ_USER screen -dmS $SCREEN_NAME bash -c "cd '$SERVER_DIR' && ./start-server.sh"
echo "Servidor reiniciado com sucesso na sessão screen '$SCREEN_NAME'."
