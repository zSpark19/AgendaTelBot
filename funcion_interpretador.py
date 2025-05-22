COMANDOS = {
    "completar": ["hecho","completada"," ya hice","terminado","listo","completado"],
    "añadir": ["crear", "añadir", "agregar", "hacer", "nueva tarea", "tengo que hacer", "tengo que"],
    "eliminar": ["borrar", "eliminar", "quitar", "sacar", "no quiero hacer"],
    "ver": ["ver", "mostrar", "enseñar", "revisar", "mirar"], 
    "modificar": ["modificar", "cambiar", "editar", "actualizar"]
}

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
    return "Añadir"

def extraer_tarea(texto):
    """
    Extrae la tarea del texto dado.
    """
    for palabras in COMANDOS.values():
        for palabra in palabras:
            texto = texto.replace(palabra, "")

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