import re

COMANDOS = {
    "completar": ["hecho","completada"," ya hice","terminado","listo","completado"],
    "añadir": ["crear", "añadir", "agregar", "hacer", "nueva tarea", "tengo que hacer", "tengo que"],
    "eliminar": ["borrar", "eliminar", "quitar", "sacar", "no quiero hacer"],
    "ver": ["ver", "mostrar", "enseñar", "revisar", "mirar"], 
    "modificar": ["modificar", "cambiar", "editar", "actualizar"]
}

PALABRAS_INUTILES = [
    "el", "la", "los", "las", "de", "del", "en", "al", "a", "un", "una", "que", "y", "e"
]


def interpretar_mensaje(texto):
    """
    Interpreta el mensaje del usuario y devuelve la intención y la tarea.
    """
    texto = texto.lower()
    accion = detectar_intencion(texto)
    tarea = extraer_tarea(texto)
    dia = extraer_dia(texto)
    casa = extraer_casa(texto)
    return accion, tarea, dia, casa

def detectar_intencion(texto):
    """
    Detecta la intención del usuario a partir de un texto dado.
    """
    texto = texto.lower()
    for comando, comandos in COMANDOS.items():
        for palabara in comandos:
            if palabara in texto:
                return comando
    return "añadir"

def extraer_tarea(texto):
    """
    Extrae la tarea del texto dado.
    """
    texto = texto.lower()
    for palabras in COMANDOS.values():
        for palabra in palabras:
            texto = re.sub(rf'\b{re.escape(palabra)}\b', '', texto)

    # Eliminar días
    for dia in ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]:
        texto = re.sub(rf'\b{dia}\b', '', texto)

    # Eliminar casas
    for casa in ["casa pequeña", "casa grande"]:
        texto = re.sub(rf'\b{casa}\b', '', texto)

    # Eliminar palabras inútiles
    for palabra in PALABRAS_INUTILES:
        texto = re.sub(rf'\b{palabra}\b', '', texto)
    # Eliminar conectores
    conectores = ["y", "e", "además", "tambien", "también", ","]
    for conector in conectores:
        texto = texto.replace(conector, "|")
    
    return [tarea.strip() for tarea in texto.split("|") if tarea.strip()]
    
def extraer_dia(texto):
    """
    Extrae el día de la semana del texto dado.
    """
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    for dia in dias:
        if dia in texto:
            return dia
    return None

def extraer_casa(texto):
    """
    Extrae la casa del texto dado.
    """
    casas = ["casa pequeña", "casa grande"]
    for casa in casas:
        if casa in texto:
            return casa
    return None

def formatear_tarea(tarea):
    if isinstance(tarea, list):
        return "\n".join(f"• {t}" for t in tarea)
    if isinstance(tarea, tuple):
        return f"{tarea[0]} → {tarea[1]}"
    return str(tarea)
