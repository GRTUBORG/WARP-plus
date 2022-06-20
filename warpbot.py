import telebot
import random
import httpx
import os
import time
import requests

from telebot import types

ppkeys = requests.get('https://Keyses-for-generator.serdarad.repl.co')
pkeys = ppkeys.content.decode('UTF8')
keys = pkeys.split(',')
gkeys = []
value_int = 1

token = os.environ.get('bot_token')
bot = telebot.TeleBot(str(token))
print('Бот работает!')

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, способный создавать ключи WARP+ для VPN 1.1.1.1, приятного использования!\nДля того, чтобы это сделать, введи команду /generate \n\n• `by` @whomet, \n• `github:` https://github.com/GRTUBORG", parse_mode = 'Markdown')

@bot.message_handler(commands = ['generate'])
def send_key(message):
    a = 0
    while a < value_int:
        a += 1

        try:
            keyboard = types.InlineKeyboardMarkup()
			donate = types.InlineKeyboardButton(text = "Поддержать автора 💸", callback_data = 'donate')
			keyboard.row(donate)

            headers = {
                "CF-Client-Version": "a-6.11-2223",
                "Host": "api.cloudflareclient.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.12.1",
            }
            
            with httpx.Client(
				base_url="https://api.cloudflareclient.com/v0a2223", headers=headers, timeout=30.0
            ) as client:
                
                r = client.post("/reg")
                id = r.json()["id"]
                license = r.json()["account"]["license"]
                token = r.json()["token"]
    
                r = client.post("/reg")
                id2 = r.json()["id"]
                token2 = r.json()["token"]
                bot.send_message(message.from_user.id, "*Создаю ключ, ожидайте...*", parse_mode = 'Markdown')

                headers_get = {"Authorization": f"Bearer {token}"}
                headers_get2 = {"Authorization": f"Bearer {token2}"}
                headers_post = {
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {token}",
                }
                
                json = {"referrer": f"{id2}"}
                client.patch(f"/reg/{id}", headers=headers_post, json=json)
    
                client.delete(f"/reg/{id2}", headers=headers_get2)
    
                
                key = random.choice(keys)
    
                json = {"license": f"{key}"}
                client.put(f"/reg/{id}/account", headers=headers_post, json=json)
    
                json = {"license": f"{license}"}
                client.put(f"/reg/{id}/account", headers=headers_post, json=json)
    
                r = client.get(f"/reg/{id}/account", headers=headers_get)
                account_type = r.json()["account_type"]
                referral_count = r.json()["referral_count"]
                license = r.json()["license"]
    
                client.delete(f"/reg/{id}", headers=headers_get)
                gkeys.append(license)
                
        except:
            bot.send_message(message.from_user.id, "Создание ключей временно недоступно, попробуйте через `3 минуты`\nЕсли ошибка повторяется, напишите @whomet", parse_mode = 'Markdown')

    for x in gkeys:
        bot.send_message(message.from_user.id, f"*Ваш ключ:* `{x}`\n*Данных выделено:* `{referral_count} GB`, \n*Тип аккаунта:* `{account_type}`", parse_mode = 'Markdown', reply_markup = keyboard)
    
    gkeys.clear()
	
@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'donate':
			bot.send_message(call.message.chat.id, 'Поддержать автора можно, *отправив любой донат* на QIWI/ЮMoney-кошелёк ❤️\nРеквизиты:\nQIWI: `qiwi.com/n/TILYI849`\nЮMoney: `4100117470392066`', parse_mode = 'Markdown')
        

bot.polling(none_stop = True)
