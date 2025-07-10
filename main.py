import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    MessageHandler, CommandHandler, filters
)

# Ortam değişkenlerini al
BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")
OWNER_IDS = os.getenv("OWNER_IDS", "").split(",")  # '123,456' → ['123', '456']

# Loglama
logging.basicConfig(level=logging.INFO)

# Hugging Face mesaj üretimi
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
        logging.error(f"HuggingFace API Hatası: {e}")
        return "Grok cevap veremedi."

# Mesajlara yanıt
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = generate_reply(text)
    await update.message.reply_text(reply)

# /hell komutu
async def hell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id

    if user_id not in OWNER_IDS:
        await update.message.reply_text("Yetkin yok.")
        return

    admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]

    async for member in context.bot.get_chat_members(chat_id):
        if member.user.id not in admin_ids and member.user.id != context.bot.id:
            try:
                await context.bot.ban_chat_member(chat_id, member.user.id)
            except Exception as e:
                logging.warning(f"Ban hatası: {member.user.id} - {e}")

    await update.message.reply_text("Yöneticiler dışındaki herkes kovuldu.")

# Botu başlat
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("hell", hell_command))

    app.run_polling()

if __name__ == "__main__":
    main()
