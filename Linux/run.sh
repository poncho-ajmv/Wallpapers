#!/bin/bash

# run.sh - Ejecuta el visor de imágenes en Linux sin necesidad de compilación
# Asegúrate de tener instalados los siguientes requisitos:
#   - Python 3
#   - tkinter
#   - Pillow

# Verificar que Python esté instalado
echo "[INFO] Verificando entorno Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Verificar que tkinter esté instalado
python3 -c "import tkinter" 2>/dev/null || {
    echo "[ERROR] tkinter no está instalado. Ejecuta: sudo apt install python3-tk"
    exit 1
}

# Verificar que Pillow esté instalado
python3 -c "from PIL import Image, ImageTk" 2>/dev/null || {
    echo "[INFO] Pillow no está instalado. Instalando en entorno local..."
    pip install --user pillow
}

# Ejecutar la aplicación
echo "[INFO] Ejecutando visor de imágenes..."
python3 linux.py
