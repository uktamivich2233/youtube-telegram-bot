import telebot
from pytube import YouTube # Video yuklash uchun
from flask import Flask # Render uchun
import os 
import threading # Pollingni ajratish uchun

# 1. Telegram Bot Tokenni o'rnatish
# Tokeningizni qo'shtirnoq ichiga yozing!
TOKEN = "8263552008:AAHGjEl2-pU8wEufhkOgu3oQUSxhzY6Iooo" # Tokeningizni tekshiring!

# 2. Bot obyektini yaratish
bot = telebot.TeleBot(TOKEN)

# 3. /start buyrug'iga javob beruvchi funksiya
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men sizning youtube yuklovchi botingizman.")

# 4. Telegramdan video yoki link kelganda javob beruvchi funksiya (YANGI, TO'LIQ KOD)
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    link = message.text

    if 'youtube.com' in link or 'youtu.be' in link:
        # Foydalanuvchiga yuklash boshlanganini xabar berish
        bot.send_message(chat_id, "🔗 Link qabul qilindi. Yuklab olish boshlandi...")

        try:
            yt = YouTube(link)

            # Eng sifatli videoni tanlash
            video_stream = yt.streams.get_highest_resolution()

            # Vaqtinchalik fayl nomini yaratish
            file_name = f"{yt.title[:40]}.mp4"

            # Videoni yuklab olish
            video_stream.download(filename=file_name)

            # Videoni Telegramga yuborish
            with open(file_name, 'rb') as video_file:
                bot.send_video(chat_id, video_file, caption=f"✅ Yuklandi: {yt.title}")

            # Yuklangan faylni serverdan o'chirish
            os.remove(file_name)

        except Exception as e:
            # Agar xatolik bo'lsa
            print(f"Yuklab olishda xatolik yuz berdi: {e}")
            bot.send_message(chat_id, "❌ Uzr, video yuklab olinmadi. Linkni tekshiring (yoki video juda katta/himoyalangan).")

    else:
        bot.reply_to(message, "Iltimos, menga YouTube video linkini yuboring.")


# 5. Botni ishga tushirish (Web Service uchun maxsus kod - O'zgartirmang)
PORT = int(os.environ.get('PORT', 5000)) 
server = Flask(__name__)

@server.route('/')
def webhook():
    return '!', 200

if __name__ == "__main__":
    try:
        # Long polling'ni alohida thread'da ishga tushirish
        polling_thread = threading.Thread(target=lambda: bot.polling(none_stop=True))
        polling_thread.start()

        # Flask serverni ishga tushirish (Render talabi)
        server.run(host="0.0.0.0", port=PORT)
    except Exception as e:
        print(f"Ishga tushirishda xatolik yuz berdi: {e}")
