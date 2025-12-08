import os
from pathlib import Path

# --- RUTAS BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

# --- CONFIGURACIÓN DE BI & MAPEO (LA FUENTE DE LA VERDAD) ---
# Mapeo: ID -> (Technical_Name, Unit, Component)
SENSOR_MAP = {
    's_1': ('Fan_Inlet_Temp', 'R', 'Fan'),
    's_2': ('LPC_Outlet_Temp', 'R', 'LPC'),
    's_3': ('HPC_Outlet_Temp', 'R', 'HPC'),
    's_4': ('LPT_Outlet_Temp', 'R', 'LPT'),
    's_5': ('Fan_Inlet_Press', 'psia', 'Fan'),
    's_6': ('Bypass_Duct_Press', 'psia', 'Duct'),
    's_7': ('HPC_Outlet_Press', 'psia', 'HPC'),
    's_8': ('Physical_Fan_Speed', 'rpm', 'Fan'),
    's_9': ('Physical_Core_Speed', 'rpm', 'Core'),
    's_10': ('Engine_Press_Ratio', '-', 'Engine'),
    's_11': ('Static_Press_Ratio', '-', 'HPC'),
    's_12': ('Bleed_Flow', 'pps', 'Fan'),
    's_13': ('Corr_Fan_Speed', 'rpm', 'Fan'),
    's_14': ('Corr_Core_Speed', 'rpm', 'Core'),
    's_15': ('Bypass_Ratio', '-', 'Duct'),
    's_16': ('Burner_Fuel_Air_Ratio', '-', 'Burner'),
    's_17': ('Bleed_Enthalpy', '-', 'Turbo'),
    's_18': ('Demand_Fan_Speed', 'rpm', 'Fan'),
    's_19': ('Demand_Corr_Fan_Speed', 'rpm', 'Fan'),
    's_20': ('HPT_Coolant_Bleed', 'lbm/s', 'HPT'),
    's_21': ('LPT_Coolant_Bleed', 'lbm/s', 'LPT')
}

# --- LISTAS DERIVADAS (Tu aporte: DRY Principle) ---
# Usamos las claves del mapa para definir qué columnas son sensores.
# Esto reemplaza a la lista manual anterior.
SENSOR_COLS = list(SENSOR_MAP.keys())

# Nombres técnicos para validaciones o uso futuro
TECHNICAL_COLS = [v[0] for v in SENSOR_MAP.values()]

# --- DEFINICIÓN DE COLUMNAS DEL DATASET CRUDO ---
INDEX_COLS = ['unit_nr', 'time_cycles']
SETTING_COLS = ['setting_1', 'setting_2', 'setting_3']

# Armamos la lista total necesaria para el data_loader
ALL_COLUMNS = INDEX_COLS + SETTING_COLS + SENSOR_COLS

# --- PARÁMETROS DE PROCESAMIENTO ---
WINDOW_SIZE = 5