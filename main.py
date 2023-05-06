from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import os
from db import DB
from cartdb import Cart
TOKEN=os.environ.get("TOKEN")
cart=Cart()
db = DB()
#1
def start(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    chat_id = update.message.chat.id
    btn1 = InlineKeyboardButton(text='🛍 View Products', callback_data="view_product_data")
    btn2 = InlineKeyboardButton(text='📦 View Cart', callback_data="viec_cart_data")
    btn3 = InlineKeyboardButton(text='📞 Contact Us', callback_data="contact_us_data")
    btn4 = InlineKeyboardButton(text='📝 About Us', callback_data="about_us_data")
    keyboard = InlineKeyboardMarkup([[btn1, btn2], [btn3, btn4]])
    bot.sendMessage(chat_id, "Assalomu alaykum! Xush kelipsiz.\nQuyidagi menyudan kerakli tugmani bosing!", reply_markup=keyboard)

def menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    btn1 = InlineKeyboardButton(text='🛍 View Products', callback_data="view_product_data")
    btn2 = InlineKeyboardButton(text='📦 View Cart', callback_data="viec_cart_data")
    btn3 = InlineKeyboardButton(text='📞 Contact Us', callback_data="contact_us_data")
    btn4 = InlineKeyboardButton(text='📝 About Us', callback_data="about_us_data")
    keyboard = InlineKeyboardMarkup([[btn1, btn2], [btn3, btn4]])
    query.edit_message_text("Bosh Menu", reply_markup=keyboard)

def view_products(update: Update, context: CallbackContext)-> None:
    query = update.callback_query

    brends = db.get_tables()
    keyboard = []
    for brend in brends:
        btn = InlineKeyboardButton(
            text = brend.capitalize(),
            callback_data=f"brend_{brend}"
        )
        keyboard.append([btn])
    btn1 = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([btn1])

    keyboard = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Quyidagi brandlardan birini tanlang!", reply_markup=keyboard)

def get_product(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    query = update.callback_query

    chat_id = query.message.chat.id
    data = query.data
    brend = data.split('_')[-1]

    products = db.get_phone_list(brend)
    # create keyboard
    keyboard = [[], []]
    phone_text = f"1-10/{len(products)}\n\n"
    pr_range = 10
    k=0
    for i, phone in enumerate(products[:pr_range], 1):
        k+=1
        phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
        # create button
        print(phone)
        btn = InlineKeyboardButton(
            text = str(i),
            callback_data=f"product_{brend}_{k}"
        )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)
    
    # btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'nextleft_{brend}_{pr_range}')
    btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
    keyboard.append([btn2])

    btn3 = InlineKeyboardButton(text="Brend", callback_data="view_product_data")
    keyboard.append([btn3])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(phone_text, reply_markup=reply_markup)

def next_product(update, context):
    query = update.callback_query
    data = query.data.split('_')
    text, brend, pr_range = data

    pr_range = int(pr_range)
    products = db.get_phone_list(brend)

    if len(products) < pr_range:
        pr_range = 0

    #print(len(products), pr_range)
    keyboard = [[], []]
    phone_text = f"{pr_range}-{pr_range+10}/{len(products)}\n\n"

    for i, phone in enumerate(products[pr_range:pr_range+10], 1):
        phone_text += f"{i}. {phone['name']} {phone['memory']}\n"
        # create button
        btn = InlineKeyboardButton(
            text = str(i),
            callback_data=f"product_{brend}_{pr_range}"
        )
        if i < 6:
            # 1 2 3 4 5
            keyboard[0].append(btn)
        else:
            # 6 7 8 9 10
            keyboard[1].append(btn)
    pr_range += 10
    # btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'nextleft_{brend}_{pr_range}')
    btn2 = InlineKeyboardButton(text="➡️", callback_data=f'nextright_{brend}_{pr_range}')
    keyboard.append([btn2])

    btn3 = InlineKeyboardButton(text="Brend", callback_data="view_product_data")
    keyboard.append([btn3])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(phone_text, reply_markup=reply_markup)

    query.answer("Next")

def get_phone(update, context):
    bot  = context.bot
    query = update.callback_query
    data = query.data.split('_')
    text, brend, doc_id = data

    phone = db.getPhone(brend, doc_id)['product']
    print(phone)
    price = phone['price']
    ram = phone['RAM']
    memory = phone['memory']
    name = phone['name']
    color = phone['color']
    img = phone['img_url']
    text = f"📲{name}\n\n🎨{color}\n💾{ram}/{memory}\n💰{price}\n\n@telefonBozor"
    btn1 = InlineKeyboardButton(text="Add Card", callback_data=f'addcard_{brend}_{doc_id}')
    btn2 = InlineKeyboardButton(text="❌", callback_data='removeproduct')
    keyboard = InlineKeyboardMarkup([
        [btn1, btn2]
    ])

    bot.send_photo(chat_id=query.message.chat.id, photo=img, caption=text, reply_markup=keyboard)
    

def add_card(update, context):
    query = update.callback_query
    data = query.data.split('_')
    chat_id = query.message.chat.id
    textt,brend,doc_id=data

    r = cart.add(brend=brend,doc_id=int(doc_id),chat_id=chat_id)

    query.answer("Done✅")

def remove_product(update, context):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
    query.answer('deleted')

#2////////////////////////////////////////////////////////

def View_Cart(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "🛒 Cart", callback_data="Cart")
    button2 = InlineKeyboardButton(text = "📦 Order", callback_data="Order")
    button3 = InlineKeyboardButton(text = " 📝 Clear cart", callback_data="Clear cart")
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1,button2],[button3,button4]])
    query.edit_message_text(text='Cart menu:', reply_markup=keyboard)
def see_products(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    products=cart.get_cart(chat_id=chat_id)
    if products!=[]:
        Total=0
        k=0
        text='🛒Xaridlar:\n'
        for i in products:
            k+=1
            brand=i['company']
            doc_id=i['product_id']
            phone=db.getPhone(brend=brand,idx=doc_id)
            Total+=int(phone['price'])
            text+=f"{k}. {phone['name']}  Narxi: {phone['price']}\n"
        text+=f"Jami: {Total}"    
        chat_id = query.message.chat.id
        button4 = InlineKeyboardButton(text = "Orqaga", callback_data="bosh_view")
        keyboard=InlineKeyboardMarkup([[button4]])
        bot.sendMessage(chat_id=chat_id, text=text,reply_markup=keyboard)
    else:
        button4 = InlineKeyboardButton(text = "Orqaga", callback_data="bosh_view")
        keyboard=InlineKeyboardMarkup([[button4]])
        bot.sendMessage(chat_id=chat_id, text='Savat Bo`sh\n',reply_markup=keyboard)
def order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer('Buyurtmangiz yuborildi🚀')


#2/////////////////////////////////////////////////////////////
def View_Cart(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "🛒 Cart", callback_data="Cart")
    button2 = InlineKeyboardButton(text = "📦 Order", callback_data="Order")
    button3 = InlineKeyboardButton(text = " 📝 Clear cart", callback_data="Clear cart")
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1,button2],[button3,button4]])
    query.edit_message_text(text='Cart menu:', reply_markup=keyboard)
def see_products(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    products=cart.get_cart(chat_id=chat_id)
    if products!=[]:
        Total=0
        k=0
        text='🛒Xaridlar:\n'
        for i in products:
            k+=1
            brand=i['company']
            doc_id=i['product_id']
            quantity=i['quantity']
            phone=db.getPhone(brand=brand,idx=doc_id)['product']
            print(phone)
            Total+=int(phone['price']*quantity)
            text+=f"{k}. {phone['name']}  Narxi: {phone['price'] }    count: {quantity}\n"
        text+=f"Jami: {Total}"    
        chat_id = query.message.chat.id
        button4 = InlineKeyboardButton(text = "Orqaga", callback_data="bosh_view")
        keyboard=InlineKeyboardMarkup([[button4]])
        query.edit_message_text(text=text,reply_markup=keyboard)
    else:
        button4 = InlineKeyboardButton(text = "Orqaga", callback_data="bosh_view")
        keyboard=InlineKeyboardMarkup([[button4]])
        query.edit_message_text(text='Savat Bo`sh\n',reply_markup=keyboard)
def order(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    query.answer('Buyurtmangiz yuborildi🚀')

def remove_card(update, context):
    query = update.callback_query
    chat_id = query.message.chat.id
    print(chat_id)
    cart.remove(chat_id=chat_id)
    query.answer("Removed")

#3///////////////////////////////////

def Contact_Us(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "📞 Phone number", callback_data="Phone number")
    button2 = InlineKeyboardButton(text = "📌 Address", callback_data="Address")
    button3 = InlineKeyboardButton(text = "📍 Location", callback_data="Location")
    button4 = InlineKeyboardButton(text = "📧 Email", callback_data="Email")
    button5 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1, button2],[button3, button4],[button5]])
    query.edit_message_text(text='Contact Us', reply_markup=keyboard)
def phone_num(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id=chat_id, text='Murojat uchun:\n📞 +998 99 755 07 33\n📞 +998 94 665 07 33\n@telefonBozor',reply_markup=keyboard)
def address(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id, text='📌Address:\n Samarqand viloyati\nQo`shrabot tumani\nbozorjoy maxallsi 312-uy\n@telefonBozor')
def location(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    bot.sendLocation(chat_id=chat_id,latitude=40.26834059511894,longitude=66.68811723628676)
def email(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id=chat_id, text='📧 Email:\ndostqobilovdavron885@gmail.com\n@telefonBozor',reply_markup=keyboard)
#4
def About_Us(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    button1 = InlineKeyboardButton(text = "📝 Company Information", callback_data="Company Information")
    button2 = InlineKeyboardButton(text = "📝 Shipping & Returns", callback_data="Shipping & Returns")
    button3 = InlineKeyboardButton(text = " 📝 Privacy Policy", callback_data="Privacy Policy")
    button4 = InlineKeyboardButton(text = "🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard = InlineKeyboardMarkup([[button1],[button2],[button3],[button4]])
    query.edit_message_text(text='About menu:', reply_markup=keyboard)
def Company_Information(update: Update, context: CallbackContext):
    query = update.callback_query
    bot = context.bot
    chat_id = query.message.chat.id
    text="""
    Telefon savdo botimizga tushunmagan joylaringizga quidagi textda javob topasiz
    lhjkmnhfdsfh,mnhbgfdsa
    dfbfgbdghngh
    hgdhn
    dghngh
    nghndgh
    nhgddddddddd edj greeeeeeeeeeeeeeeee gergerg erg argekrga
    gergghaergaerghuaerguaergiuaergbrg
    gergaegrghlaegargbgrg
    ergjaeora;geragregrghrg
    """
    button4 = InlineKeyboardButton(text ="Orqaga", callback_data="Orqaga")
    keyboard=InlineKeyboardMarkup([[button4]])
    bot.sendMessage(chat_id=chat_id, text=text,reply_markup=keyboard)

updater = Updater(token=TOKEN)
dp = updater.dispatcher
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

updater.start_polling()
updater.idle()