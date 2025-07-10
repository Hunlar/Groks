import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Ayarlar
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_IDS = [123456789, 987654321]  # SAHİP ID’LERİ BURAYA YAZ
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")  # Hugging Face Token

# Loglama
logging.basicConfig(level=logging.INFO)

# Hugging Face Fonksiyonu
def generate_reply(prompt: str) -> str:
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result[0]["generated_text"] if isinstance(result, list) else "Cevap alınamadı."
    except Exception as e:
        logging.error(f"HuggingFace Hatası: {e}")
        return "Bir hata oluştu..."

# Mesajlara cevap
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        prompt = update.message.text
        reply = generate_reply(prompt)
        await update.message.reply_text(reply)

# /hell komutu
async def hell_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if user_id not in OWNER_IDS:
        await update.message.reply_text("Bu komutu kullanamazsın.")
        return

    # Adminleri listele
    admin_members = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admin_members]

    # Üyeleri banla
    async for member in context.bot.get_chat_administrators(chat_id):
        pass  # dummy read to make this async loop valid

    async for member in context.bot.get_chat_members(chat_id):
        if member.user.id not in admin_ids and member.user.id != context.bot.id:
            try:
                await context.bot.ban_chat_member(chat_id, member.user.id)
            except Exception as e:
                logging.warning(f"Kullanıcı banlanamadı: {member.user.id} - {e}")
    
    await update.message.reply_text("Yöneticiler hariç herkes kovuldu.")

# Ana fonksiyon
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hell", hell_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
