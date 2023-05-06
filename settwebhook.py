import telegram

TOKEN= "6244092180:AAH_10MCMX4wAESk6TTp-iboI1EMSe6FeZ8"
url="https://davronjan.pythonanywhere.com/webhook"
bot = telegram.Bot(TOKEN)

print(bot.set_webhook(url))