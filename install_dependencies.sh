#!/bin/bash
#
# Script para instalar as dependências de sistema e Python para o projeto gestorsites-2.0.

# Garante que o script pare se algum comando falhar
set -e

# 1. Atualiza a lista de pacotes do sistema
echo "--- Atualizando pacotes do sistema (apt) ---"
sudo apt-get update

# 2. Instala as dependências de sistema necessárias para compilar pacotes Python
echo "--- Instalando dependências de sistema (libmariadb-dev, python3.12-dev) ---"
sudo apt-get install -y libmariadb-dev python3.12-dev

# 3. Instala as dependências Python a partir do arquivo dependence.txt
echo "--- Instalando dependências Python (pip) ---"
pip install -r dependence.txt

echo ""
echo "--- Instalação concluída com sucesso! ---"
