#!/bin/bash
# Script para resetar o mundo do servidor Project Zomboid via systemd

SAVE_DIR="/root/Zomboid/Saves/Multiplayer/servertest"

echo "Parando o servidor para o reset..."
sudo systemctl stop zomboid-server
sleep 3

if sudo test -d "$SAVE_DIR"; then
    echo "Apagando os arquivos do mundo em $SAVE_DIR..."
    sudo rm -rf "$SAVE_DIR"
    echo "Arquivos do mundo apagados."
else
    echo "Diretório do save não encontrado. Pulando a remoção."
fi

echo "Iniciando o servidor com um novo mundo..."
sudo systemctl start zomboid-server
echo "Reset concluído."
