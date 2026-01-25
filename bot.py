import asyncio
import requests
from datetime import date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Render uchun Web Server (Bot o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Token va Bot sozlamalari
TOKEN = "8456499271:AAEuc6zQc76bz0sXwvG2mHOiSZwzTMR1o9I"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Menyu tugmalari
def main_menu():
    kb = [
        [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
        [KeyboardButton(text="📅 Bugun"), KeyboardButton(text="🌅 Ertaga")],
        [KeyboardButton(text="🕋 Qibla yo'nalishi"), KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Namoz vaqtlarini aniqlash uchun joylashuvni yuboring:", reply_markup=main_menu())

# Joylashuv kelganda namoz vaqtlarini hisoblash
@dp.message(F.location)
async def handle_location(message: types.Message):
    lat, lon = message.location.latitude, message.location.longitude
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=3"
    
    try:
        response = requests.get(url).json()
        # 't' o'zgaruvchisini aniqlash (NameError oldini olish uchun)
        t = response['data']['timings']
        
        # Ramazon kunini aniq hisoblash (2026-yil 1-mart deb olindi)
        ramazon_boshi = date(2026, 3, 1)
        bugun = date.today()
        qolgan_kun = (ramazon_boshi - bugun).days
        
        # Ramazon o'tib ketgan bo'lsa yoki kelayotgan bo'lsa
        ramazon_matni = f"🌙 Ramazongacha {qolgan_kun} kun qoldi." if qolgan_kun > 0 else "🌙 Ramazon oyi muborak bo'lsin!"
        
        text = (
            f"🏙 **Bomdod:** {t['Fajr']}\n"
            f"☀️ **Peshin:** {t['Dhuhr']}\n"
            f"🌇 **Asr:** {t['Asr']}\n"
            f"🌆 **Shom:** {t['Maghrib']}\n"
            f"🌃 **Xufton:** {t['Isha']}\n\n"
            f"{ramazon_matni}"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer("⚠️ Ma'lumot olishda xatolik yuz berdi.")

async def main():
    keep_alive()
    # Konfliktni oldini olish uchun webhookni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
