import os
import json
from datetime import date
import shutil

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

    hoy = date.today()
    semana_actual = f"{hoy.year}-W{hoy.isocalendar().week}"

    if os.path.exists(path):
        with open(path, "r") as f:
            datos = json.load(f)
        
        if datos.get("ultima_semana") != semana_actual:
            backup_path = os.path.join(DATA_DIR, "backups")
            os.makedirs(backup_path, exist_ok=True)

            nombre_backup = f"{user_id}_{datos.get('ultima_semana')}.json"
            shutil.copy(path, os.path.join(backup_path, nombre_backup))

            datos["ultima_semana"] = semana_actual
            datos ["planing"] = crear_estructura_vacia()
            guardar_planing(user_id, datos)
        
        return datos["planing"]
    else:
        datos = {
            "ultima_semana": semana_actual,
            "planing": crear_estructura_vacia()
        }
        guardar_planing(user_id, datos)
        return datos["planing"]
    
    
def guardar_planing(user_id, datos_completos):
    """
    Guarda el planing en un archivo JSON.
    """
    path = os.path.join(DATA_DIR, f"{user_id}.json")
    with open(path, "w") as f:
        json.dump(datos_completos, f, indent=4)

def cargar_datos_completos(user_id):
    path = os.path.join(DATA_DIR, f"{user_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "ultima_semana": f"{date.today().year}-W{date.today().isocalendar().week}",
        "planing": crear_estructura_vacia()
    }
