import os
import json

DATA_DIR = "data"

def crear_estructura_vacia():
    """
    Crea la estructura de carpetas y archivos necesarios para el bot.
    """
    return {
        dia: {"casa pequeña": [], "casa grande": []}
        for dia in ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    }

def cargar_planing(user_id):
    """
    Carga la estructura de carpetas y archivos necesarios para el bot.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        planing = crear_estructura_vacia()
        guardar_planing(user_id, planing)
        return planing
    
def guardar_planing(user_id, planing):
    """
    Guarda el planing en un archivo JSON.
    """
    path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(path, "w") as f:
        json.dump(planing, f, indent=4)