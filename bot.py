import asyncio
import aiohttp # requests o'rniga asinxron kutubxona
from datetime import date
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Web Server (Render uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Token (Buni xavfsiz saqlang!)
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
    await message.answer("Assalomu alaykum! Namoz vaqtlarini bilish uchun joylashuvni yuboring:", reply_markup=main_menu())

@dp.message(F.location)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    # Aladhan API asinxron chaqiruv bilan
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=3"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                t = data['data']['timings']
                
                # Ramazon 2026-yil 18-fevral atrofida boshlanadi (taqvimga ko'ra)
                # Siz yozgan 1-mart shunchaki misol sifatida qoldirildi
                ramazon_boshi = date(2026, 2, 18) 
                bugun = date.today()
                qolgan_kun = (ramazon_boshi - bugun).days
                
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
        print(f"Xatolik: {e}")
        await message.answer("⚠️ Ma'lumot olishda xatolik yuz berdi.")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi")
