from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler)
from planing_utils import cargar_planing, crear_estructura_vacia, guardar_planing, cargar_datos_completos
from funcion_interpretador import interpretar_mensaje
from tareas_utils import agregar_tarea, modificar_tarea, eliminar_tarea, buscar_tarea, ver_tareas, ver_tareas_dia, completado_tarea

# Cargar el token del bot desde un archivo .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /start para iniciar el bot.
    """
    await update.message.reply_text("¡Hola! Estoy aquí para ayudarte a planificar tu semana. Escribe un dia de la semana (lunes, martes, miércoles, jueves, viernes, sábado, domingo) para empezar.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
     """
     Maneja los mensajes de texto.
    """
     user_id = str(update.effective_user.id)
     planning = cargar_planing(user_id)
     estado = user_state.get(user_id, {})
     # Interpretar el mensaje
     accion, tarea, dia, casa = interpretar_mensaje(update.message.text.lower())

     if accion == "añadir":
        if dia and casa and tarea:
            agregar_tarea(user_id, planning, dia, casa, tarea)
            await update.message.reply_text(f"Tarea añadida: {tarea} en {casa} para el {dia}.")

        elif not estado.get("dia"):
            await update.message.reply_text("¿Qué día de la semana quieres añadir la tarea? (lunes, martes, miércoles, jueves, viernes, sábado, domingo)")
            return
        elif not estado.get("casa"):
            await update.message.reply_text("¿Qué casa quieres añadir la tarea? (casa pequeña, casa grande)")
            return
        else:
            await update.message.reply_text("¿Qué tarea quieres añadir?")
            return
        
     elif accion == "eliminar":
         if dia and casa and tarea:
             indice = buscar_tarea(planning, dia, casa, tarea)
             if indice is not None:
                 eliminar_tarea(user_id, planning, dia, casa, indice)
                 await update.message.reply_text(f"Tarea eliminada: {tarea} en {casa} para el {dia}.")
             else:
                 await update.message.reply_text("No se encontró la tarea a eliminar.")
         elif not estado.get("dia"):
            await update.message.reply_text("¿De que dia de la semana es la tarea que quieres eliminar? (lunes, martes, miércoles, jueves, viernes, sábado, domingo)")
            return
         elif not estado.get("casa"):
            await update.message.reply_text("¿En que casa está la tarea? (casa pequeña, casa grande)")
            return
         else:
            await update.message.reply_text("¿Qué tarea quieres eliminar?")
            return
         
     elif accion == "modificar":
         if dia and casa and tarea and isinstance(tarea, tuple):
            tarea_vieja, tarea_nueva = tarea
            indice = buscar_tarea(planning, dia, casa, tarea_vieja)
            if indice is not None:
                modificar_tarea(user_id, planning, dia, casa, indice, tarea_nueva)
                await update.message.reply_text(f"Tarea modificada: '{tarea_vieja}' → '{tarea_nueva}' en {casa} para el {dia}.")
            else:
                await update.message.reply_text("No se encontró la tarea a modificar.")
         else:
            await update.message.reply_text("Por favor escribe la tarea así: 'cambia limpiar cocina por barrer salón'")
            return
         
     elif accion == "ver":
         if dia:
             mensaje = ver_tareas_dia(planning, dia)
             await update.message.reply_text(mensaje, parse_mode="Markdown")
         else:
             mensaje = ver_tareas(planning)
             await update.message.reply_text(mensaje, parse_mode="Markdown")
     elif accion == "completar":
         if dia and casa and tarea:
             indice = buscar_tarea(planning, dia, casa, tarea)
             if indice is not None:
                 exito = completado_tarea(user_id, planning, dia, casa, indice)
                 if exito:
                    await update.message.reply_text(f"Tarea completada: {tarea} en {casa} para el {dia}.")
                 else:
                    await update.message.reply_text("La tarea ya estaba completada.")
             else:
                 await update.message.reply_text("No se encontró la tarea a completar.")
         else:
             await update.message.reply_text("¿Qué tarea quieres completar?")
             return

async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /ver para ver el planing.
    """
    user_id = str(update.effective_user.id)
    planing = cargar_planing(user_id)
    
    mensaje= ver_tareas(planing)
    await update.message.reply_text(mensaje or "No hay tareas programadas para esta semana.", parse_mode="Markdown")

async def nueva(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /nueva para cambiar de semana.
    """
    user_id = str(update.effective_user.id)
    from datetime import date
    semana_actual = f"{date.today().year}-W{date.today().isocalendar().week}"
    planing = {
        "ultima_semana": semana_actual,
        "planing": crear_estructura_vacia()
    }
    
    datos = cargar_datos_completos(user_id)
    datos["planing"] = planing
    guardar_planing(user_id, datos)
    await update.message.reply_text("Semana cambiada. Puedes empezar a añadir tareas.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
 *Comandos disponibles:*
 /start - Iniciar el bot
 /ver - Ver toda la semana
 /nueva - Iniciar nueva semana
 Puedes escribir frases como:
 - "limpiar cocina en casa pequeña el lunes"
 - "completada recoger salón"
 - "cambia lavar platos por barrer"
 """, parse_mode="Markdown")


async def main():
    """
    Función principal para iniciar el bot.
    """
    # Crear la aplicación
    application = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ver", ver))
    application.add_handler(CommandHandler("nueva", nueva))
    application.add_handler(CommandHandler("ayuda", ayuda))

    # Manejar mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar el bot
    print("Bot iniciado. Esperando mensajes...")
    try:
        await application.run_polling()
    except KeyboardInterrupt:
        print("Bot detenido.")

#lanzar el bot
if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
