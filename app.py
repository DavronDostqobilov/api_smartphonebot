from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, Updater, MessageHandler, CommandHandler, Filters,CallbackQueryHandler
import os
from db import DB
import telegram
from bot import start,view_products,menu,get_product,next_product,get_phone,add_card,remove_product,View_Cart,see_products,order,remove_card,Contact_Us,phone_num,address,location,email,About_Us,Company_Information
TOKEN='6244092180:AAH_10MCMX4wAESk6TTp-iboI1EMSe6FeZ8'
bot = telegram.Bot(TOKEN)

app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def home():
    dp = Dispatcher(bot, None, workers=0)
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    #1
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(view_products, pattern="view_product_data"))
    dp.add_handler(CallbackQueryHandler(menu, pattern="bosh_menu"))
    dp.add_handler(CallbackQueryHandler(get_product, pattern="brend"))
    dp.add_handler(CallbackQueryHandler(next_product, pattern="next"))
    dp.add_handler(CallbackQueryHandler(get_phone, pattern="product"))
    dp.add_handler(CallbackQueryHandler(add_card, pattern="addcard"))
    dp.add_handler(CallbackQueryHandler(remove_product, pattern="removeproduct"))
    #2
    dp.add_handler(CallbackQueryHandler(View_Cart, pattern="viec_cart_data"))
    dp.add_handler(CallbackQueryHandler(see_products, pattern="Cart"))
    dp.add_handler(CallbackQueryHandler(View_Cart, pattern="bosh_view"))
    dp.add_handler(CallbackQueryHandler(order, pattern="Order"))
    dp.add_handler(CallbackQueryHandler(remove_card, pattern="Clear cart"))
    #3
    dp.add_handler(CallbackQueryHandler(Contact_Us, pattern="contact_us_data"))
    dp.add_handler(CallbackQueryHandler(phone_num, pattern="Phone number"))
    dp.add_handler(CallbackQueryHandler(address, pattern="Address"))
    dp.add_handler(CallbackQueryHandler(location, pattern="Location"))
    dp.add_handler(CallbackQueryHandler(email, pattern="Email"))
    #4
    dp.add_handler(CallbackQueryHandler(About_Us, pattern="about_us_data"))
    dp.add_handler(CallbackQueryHandler(menu, pattern="bosh_menu"))
    dp.add_handler(CallbackQueryHandler(Company_Information, pattern="Company Information"))
    dp.add_handler(CallbackQueryHandler(About_Us, pattern="Orqaga"))
    return 'ok'
if __name__ == "__main__":
    app.run(debug=True)