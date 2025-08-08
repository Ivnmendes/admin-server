#!/bin/bash
# Script para resetar o mundo do servidor Project Zomboid

PZ_USER="pzuser"
SCREEN_NAME="pzserver"
SAVE_DIR="/home/pzuser/Zomboid/Saves/Multiplayer/servertest" # Atenção ao nome da pasta do save
SERVER_DIR="/home/pzuser/Steam/steamapps/common/Project Zomboid Dedicated Server"

echo "AVISO: Este script irá apagar permanentemente o mundo do servidor."
read -p "Você tem certeza que deseja continuar? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]
then
    exit 1
fi

echo "Iniciando o reset do mundo..."

# Para o servidor
if sudo -u $PZ_USER screen -list | grep -q "$SCREEN_NAME"; then
    echo "Parando o servidor..."
    sudo -u $PZ_USER screen -S $SCREEN_NAME -X quit
    sleep 2
fi

# Apaga a pasta do save
if sudo -u pzuser test -d "$SAVE_DIR"; then
    echo "Apagando os arquivos do mundo em $SAVE_DIR..."
    sudo -u $PZ_USER rm -rf "$SAVE_DIR"
    echo "Arquivos do mundo apagados."
else
    echo "Diretório do save não encontrado. Pulando a remoção."
fi

# Inicia o servidor novamente
echo "Iniciando o servidor com um novo mundo..."
sudo -u $PZ_USER screen -dmS $SCREEN_NAME bash -c "cd '$SERVER_DIR' && ./start-server.sh"

echo "Reset do mundo concluído. O servidor está iniciando."

