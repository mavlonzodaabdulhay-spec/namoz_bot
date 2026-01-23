import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Web server (Render o'chmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot tirik!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Bot sozlamalari
TOKEN = "8461895608:AAHrTyxLsnlyUnXLhoPltb3XOuwQXRGBBIE"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Start buyrug'i berilganda joylashuv so'rash
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    # Joylashuv yuborish tugmasi
    btn = [[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True, one_time_keyboard=True)
    
    await message.answer(
        "Assalomu alaykum! Namoz vaqtlarini aniqlash uchun quyidagi tugmani bosing va joylashuvingizni yuboring. "
        "Bu dunyoning istalgan nuqtasida (O'zbekiston, Angliya, Afrika...) aniq vaqtni ko'rsatadi.",
        reply_markup=keyboard
    )

# Joylashuv kelganda vaqtni hisoblash
@dp.message(lambda message: message.location is not None)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    
    # Aladhan API koordinata orqali (Method 3 - O'zbekistonga ham mos)
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=3"
    
    try:
        res = requests.get(url).json()
        t = res['data']['timings']
        data = res['data']
        
        text = (
            f"📍 Hudud: {data['meta']['timezone']}\n"
            f"📅 Sana: {data['date']['readable']}\n\n"
            f"💥 Bomdod: {t['Fajr']}\n"
            f"☀️ Quyosh: {t['Sunrise']}\n"
            f"☀️ Peshin: {t['Dhuhr']}\n"
            f"🌇 Asr: {t['Asr']}\n"
            f"🌆 Shom: {t['Maghrib']}\n"
            f"🌃 Xufton: {t['Isha']}\n\n"
            f"⚠️ Vaqtlar siz turgan nuqtaga nisbatan aniq hisoblandi."
        )
        await message.answer(text)
    except:
        await message.answer("Vaqtlarni olishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
