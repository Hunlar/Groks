# Grok1xBot 🤖🔥

Yapay zekâ destekli Telegram botu. Hugging Face API kullanır.  
Gruptaki mesajlara yanıt verir ve sadece sahiplerin kullanabileceği özel komutlara sahiptir.

---

## 🚀 Özellikler

- 💬 Grupta yazışmaları takip edip GPT benzeri cevaplar verir.
- 🔥 `/hell` komutu → sadece sahipler kullanabilir. Yöneticiler dışındaki tüm üyeleri gruptan atar.
- 🧠 Hugging Face ile ücretsiz yapay zekâ entegrasyonu.
- ☁️ **Heroku uyumlu** yapı (anında deploy edebilirsin).

---

## 🛠️ Kurulum

### 1. Heroku ile Tek Tık Kurulum:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Hunlar/Groks)

### 2. Ortam Değişkenlerini (Config Vars) Heroku’da tanımla:

| Key         | Açıklama                     |
|-------------|------------------------------|
| `BOT_TOKEN` | Telegram Bot Token'ınız      |
| `HF_API_KEY`| Hugging Face API anahtarınız |
| `OWNER_IDS` | Virgülle ayrılmış sahip ID’leri (örnek: `123456789,987654321`) |

---

## 🧠 Hugging Face Modeli

Varsayılan model: `microsoft/DialoGPT-medium`  
İstersen Hugging Face üzerinde başka bir sohbet modelini de bağlayabilirsin.

---

## 📂 Dosya Yapısı

```bash
.
├── main.py
├── requirements.txt
├── Procfile
└── README.md
