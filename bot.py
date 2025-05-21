from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler)
from planing_utils import cargar_planing, guardar_planing, crear_estructura_vacia

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
     text = update.message.text.lower()

     planning = cargar_planing(user_id)
     estado = user_state.get(user_id, {})
     if "dia" not in estado:
         if text in planning.keys():
             estado["dia"] = text
             user_state[user_id] = estado
             await update.message.reply_text("¿Casa pequeña o casa grande?")
         else:
             await update.message.reply_text("Por favor, selecciona un día de la semana válido.")
         
     
     elif "casa" not in estado:
            if text in ["casa pequeña", "casa grande"]:
                estado["casa"] = text
                user_state[user_id] = estado
                await update.message.reply_text("¿Qué tarea quieres añadir?")
            else:
                await update.message.reply_text("Por favor, selecciona 'casa pequeña' o 'casa grande'.")
            
     else:
          planning[estado["dia"]][estado["casa"]].append(text)
          guardar_planing(user_id, planning)
          await update.message.reply_text(f"Tarea añadida: {text} en {estado['casa']} para el {estado['dia']}.")
          user_state.pop(user_id, None)  # Limpiar el estado del usuario




async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /ver para ver el planing.
    """
    user_id = str(update.effective_user.id)
    planing = cargar_planing(user_id)
    
    mensaje= ""
    for dia, casas in planing.items():
         mensaje += f"\n📅 *{dia.capitalize()}*:\n"
         for casa, tareas in casas.items():
             if tareas:
                    mensaje += f"🏠 *{casa.capitalize()}*:\n"
                    for tarea in tareas:
                        mensaje += f"- {tarea}\n"
    await update.message.reply_text(mensaje or "No hay tareas programadas para esta semana.", parse_mode="Markdown")

async def main():
    """
    Función principal para iniciar el bot.
    """
    # Crear la aplicación
    application = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ver", ver))


    # Manejar mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar el bot
    print("Bot iniciado. Esperando mensajes...")
    await application.run_polling()

#lanzar el bot
if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
