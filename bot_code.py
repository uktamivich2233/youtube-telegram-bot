import telebot
from flask import Flask # Yangi: Flask'ni import qilish
import os # Yangi: Atrof-muhit o'zgaruvchilarini o'qish uchun

# 1. Telegram Bot Tokenni o'rnatish
# Iltimos, bu qatorda tokendagi '...' o'rniga o'z tokendingizni to'liq kiriting
TOKEN = "8263552008:AAHGjEl2-pU8wEufhkOgu3oQUSxhzY6Iooo"

# 2. Bot obyektini yaratish
bot = telebot.TeleBot(TOKEN)

# 3. /start buyrug'iga javob beruvchi funksiya
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men sizning youtube yuklovchi botingizman.")

# 4. Telegramdan video yoki link kelganda javob beruvchi funksiya
# Iltimos, bu joyga o'zingizning to'liq yuklash kodingizni kiriting
# (Masalan, sizning botingizda bu joyga youtube linkni olib, videoni yuklab berish kodi yozilgan bo'lishi kerak)
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if 'youtube.com' in message.text or 'youtu.be' in message.text:
        bot.reply_to(message, "Link qabul qilindi. Hozircha men faqat 'Salom' deyishni bilaman, lekin kelajakda videolarni yuklab beraman!")
    else:
        bot.reply_to(message, "Iltimos, menga YouTube video linkini yuboring.")


# 5. Botni ishga tushirish (Web Service uchun maxsus kod)
# Bu kod botni Web Service'da bepul ishlashga majbur qiladi.
# Oldingi "bot.polling(none_stop=True)" kodi o'rniga buni qo'yamiz:
PORT = int(os.environ.get('PORT', 5000)) 
server = Flask(__name__)

@server.route('/')
def webhook():
    # Telegram xabarlari Render portiga kelmaydi, lekin Render portni ochiq deb biladi
    return '!', 200

if __name__ == "__main__":
    # Botni ishga tushirish (polling)
    try:
        # Long polling'ni alohida thread'da ishga tushiramiz
        import threading
        polling_thread = threading.Thread(target=lambda: bot.polling(none_stop=True))
        polling_thread.start()
        
        # Flask serverni ishga tushirish (Render portini band qilish uchun)
        server.run(host="0.0.0.0", port=PORT)
    except Exception as e:
        # Xatolikni qayd qilish
        print(f"Ishga tushirishda xatolik yuz berdi: {e}")
