#!/bin/bash
# Script para iniciar o servidor Project Zomboid via systemd

echo "Iniciando o servidor..."
sudo systemctl start zomboid-server
echo "Comando de inicio enviado para o systemd."
