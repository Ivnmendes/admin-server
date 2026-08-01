#!/bin/bash
# Script para parar o servidor Project Zomboid

PZ_USER="${PZ_USER:-pzuser}"
SCREEN_NAME="${SCREEN_NAME:-pzserver}"

echo "Verificando se o servidor está rodando..."

# Verifica se a sessão screen existe antes de tentar parar
if sudo -u $PZ_USER screen -list | grep -q "$SCREEN_NAME"; then
    echo "Enviando comando para parar a sessão '$SCREEN_NAME'..."
    sudo -u $PZ_USER screen -X -S $SCREEN_NAME quit
    echo "Comando de parada enviado. O servidor foi encerrado."
else
    echo "O servidor não parece estar rodando."
fi
