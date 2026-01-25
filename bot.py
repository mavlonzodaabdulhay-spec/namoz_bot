import asyncio
import requests
from datetime import date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Web Server
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Token (@Namozvoqti_bot)
TOKEN = "8456499271:AAEuc6zQc76bz0sXwvG2mHOiSZwzTMR1o9I"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def main_menu():
    kb = [
        [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
        [KeyboardButton(text="📅 Bugun"), KeyboardButton(text="🌅 Ertaga")],
        [KeyboardButton(text="🕋 Qibla yo'nalishi"), KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Joylashuvni yuboring:", reply_markup=main_menu())

@dp.message(F.location)
async def handle_location(message: types.Message):
    lat, lon = message.location.latitude, message.location.longitude
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=3"
    
    try:
        res = requests.get(url).json()
        t = res['data']['timings'] # Mana shu 't' o'zgaruvchisi endi aniqlandi
        
        # Ramazonni hisoblash
        qolgan_kun = (date(2026, 3, 1) - date.today()).days
        
        text = (
            f"🏙 **Bomdod:** {t['Fajr']}\n"
            f"☀️ **Peshin:** {t['Dhuhr']}\n"
            f"🌇 **Asr:** {t['Asr']}\n"
            f"🌆 **Shom:** {t['Maghrib']}\n"
            f"🌃 **Xufton:** {t['Isha']}\n\n"
            f"🌙 **Ramazongacha {qolgan_kun} kun qoldi.**"
        )
        await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer("Xatolik yuz berdi!")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
