#!/bin/bash
# Script para parar o servidor Project Zomboid via systemd

echo "Parando o servidor..."
sudo systemctl stop zomboid-server
echo "Comando de parada enviado para o systemd."
