import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Cargar las credenciales seguras
load_dotenv("../.env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 2. Definir el comando de bienvenida (/start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_bienvenida = (
        "¡Hola! Soy Fungiagente. 🍄\n\n"
        "Tu asistente en los procesos de cultivo de hongos comestibles de Nigredo.\n"
        "Te puedo ayudar proporcionándote información general acerca de los hongos que trabajamos, el sustrato que puedes usar, parámetros de cultivo y muchas cosas más\n\n."
	"¿Listo para sumergirte en el proceso alquímico del cultivo de hongos? ¡Vamos allá!"
    )
    await update.message.reply_text(mensaje_bienvenida)

# 3. Procesar las consultas técnicas
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text
    
    # Enviar un indicador visual de que la IA está trabajando
    mensaje_espera = await update.message.reply_text("⏳ Consultando los archivos de Nigredo...")
    
    try:
        # Enviar la consulta a nuestro servidor FastAPI local
        respuesta_api = requests.post(
            "http://localhost:8000/api/v1/consultar",
            json={"pregunta": pregunta}
        )
        
        # Verificar la conexión y actualizar el mensaje con la respuesta final
        if respuesta_api.status_code == 200:
            respuesta_texto = respuesta_api.json()["respuesta"]
            await context.bot.edit_message_text(
                chat_id=update.message.chat_id, 
                message_id=mensaje_espera.message_id, 
                text=respuesta_texto
            )
        else:
            await context.bot.edit_message_text(
                chat_id=update.message.chat_id, 
                message_id=mensaje_espera.message_id, 
                text=f"⚠️ Error interno. Código: {respuesta_api.status_code}"
            )
            
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id, 
            message_id=mensaje_espera.message_id, 
            text="⚠️ El servidor central de Fungiagente está desconectado."
        )

# 4. Inicializar y encender el bot
def main():
    if not TOKEN:
        print("Error: No se encontró el TELEGRAM_BOT_TOKEN en el archivo .env")
        return

    app = Application.builder().token(TOKEN).build()
    
    # Rutear los comandos y mensajes a sus funciones
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    
    print("🍄 Fungiagente móvil en línea. Escuchando mensajes en Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()
