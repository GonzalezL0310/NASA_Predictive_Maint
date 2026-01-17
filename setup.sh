#!/bin/bash

# --- 1. System Dependency Installation ---
# Instala Python y el soporte para entornos virtuales si no están presentes.
echo "[STEP 1] Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential

# --- 2. Python Environment Setup ---
# Crea el entorno virtual en la raíz del proyecto.
echo "[STEP 2] Setting up Python virtual environment..."
python3 -m venv venv

# Activa el entorno para la sesión actual del script
source venv/bin/activate

# --- 3. Dependency Installation ---
# Instala los paquetes definidos en requirements.txt.
if [ -f "requirements.txt" ]; then
    echo "[STEP 3] Installing project dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "[ERROR] requirements.txt not found. Please ensure the file exists."
    exit 1
fi

echo "------------------------------------------------"
echo "[SUCCESS] Setup complete."
echo "To start working, run:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo "------------------------------------------------"
