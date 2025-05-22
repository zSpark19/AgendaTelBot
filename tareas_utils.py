from planing_utils import guardar_planing, cargar_datos_completos

def agregar_tarea(user_id, planing, dia, casa, tareas: list[str]):
    """
    Agrega una tarea al planing.
    """
    if dia not in planing:
        planing[dia] = {}
    if casa not in planing[dia]:
        planing[dia][casa] = []
    planing[dia][casa].extend(tareas)
    datos = cargar_datos_completos(user_id)
    datos["planing"] = planing
    guardar_planing(user_id, datos)
    return planing

def modificar_tarea(user_id, planing, dia, casa, indice: int, tarea: str):
    """
    Modifica una tarea en el planing.
    """
    if dia in planing and casa in planing[dia] and 0 <= indice < len(planing[dia][casa]):
        planing[dia][casa][indice] = tarea
        datos = cargar_datos_completos(user_id)
        datos["planing"] = planing
        guardar_planing(user_id, datos)
        return planing
    return None

def eliminar_tarea(user_id, planing, dia, casa, indice: int):
    """
    Elimina una tarea del planing.
    """
    if dia in planing and casa in planing[dia] and 0 <= indice < len(planing[dia][casa]):
        del planing[dia][casa][indice]
        datos = cargar_datos_completos(user_id)
        datos["planing"] = planing
        guardar_planing(user_id, datos)
        return planing
    return None

def ver_tareas(planing):
    """
    Muestra las tareas del planing.
    """
    mensaje = ""
    for dia, casas in planing.items():
        mensaje += f"\n📅 *{dia.capitalize()}*:\n"
        for casa, tareas in casas.items():
            if tareas:
                mensaje += f"🏠 *{casa.capitalize()}*:\n"
                for i, tarea in enumerate(tareas):
                    mensaje += f"{i+1}. {tarea}\n"
    return mensaje or "No hay tareas programadas para esta semana."

def ver_tareas_dia(planing, dia):
    """
    Muestra las tareas de un día específico en el planing.
    """
    mensaje = ""
    if dia in planing:
        mensaje += f"\n📅 *{dia.capitalize()}*:\n"
        for casa, tareas in planing[dia].items():
            mensaje += f"🏠 *{casa.capitalize()}*:\n"
            for i, tarea in enumerate(tareas):
                mensaje += f"{i+1}. {tarea}\n"
    return mensaje or f"No hay tareas programadas para el {dia} esta semana."

def buscar_tarea(planing, dia, casa, tarea: str) -> int | None:
    """
    Extrae el índice de la tarea a modificar o eliminar del texto dado.
    """
    tareas = planing[dia][casa]
    texto = tarea.lower()
    palabra = texto.split()
    for i, tareas_aux in enumerate(tareas):
        if palabra in tareas_aux.lower():
            return i
    return None

def completado_tarea(user_id, planing, dia, casa, indice):
    """
    Marca una tarea como completada en el planing.
    """
    tareas = planing[dia][casa]
    if 0 <= indice < len(tareas):
        tarea= tareas[indice]
        if tarea.startswith("✅ "):
            return False
        tareas[indice] = f"✅ {tareas[indice]}"
        datos = cargar_datos_completos(user_id)
        datos["planing"] = planing
        guardar_planing(user_id, datos)
        return True
    return False
