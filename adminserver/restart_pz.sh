#!/bin/bash
# Script para reiniciar o servidor Project Zomboid via systemd

echo "Reiniciando o servidor..."
sudo systemctl restart zomboid-server
echo "Comando de reinicializacao enviado para o systemd."
