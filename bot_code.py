import telebot

# 2. Tokenni o'rnatish (Sizning rasmingizdagi token bu yerda)
TOKEN = "8263552008:AAHGjEl2-pU8wEufhkOgu3oQUSxhzY6Iooo"

# 3. Bot obyektini yaratish
bot = telebot.TeleBot(TOKEN)

# 4. /start buyrug'iga javob beruvchi funksiya (Masalan)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men sizning youtube yuklovchi botingizman.")

# 5. Botni ishga tushirish
if __name__ == '__main__':
    # none_stop=True qilish tavsiya etiladi
    bot.polling(none_stop=True) 
