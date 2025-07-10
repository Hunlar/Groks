import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")
OWNER_IDS = os.getenv("OWNER_IDS", "").split(",")

logging.basicConfig(level=logging.INFO)

def generate_reply(prompt: str) -> str:
    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": prompt}
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result[0]["generated_text"] if isinstance(result, list) else "Cevap alınamadı."
    except Exception as e:
        logging.error(f"HuggingFace Hatası: {e}")
        return "Cevap üretilemedi."

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    reply = generate_reply(text)
    update.message.reply_text(reply)

def hell_command(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id

    if user_id not in OWNER_IDS:
        update.message.reply_text("Bu komutu kullanamazsın.")
        return

    admins = context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]

    # Burada get_chat_members async olmadığı için direkt kullanım biraz farklı olabilir,
    # ama 13.x sürümünde toplu kullanıcı işlemi kolay değil.
    # O yüzden sadece uyarı mesajı bırakıyorum.

    update.message.reply_text("Bu sürümde toplu banlama async olmadığı için desteklenmiyor.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("hell", hell_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
