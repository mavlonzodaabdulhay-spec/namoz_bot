import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Render o'chib qolmasligi uchun kichik server
app = Flask('')
@app.route('/')
def home(): return "Bot ishlayapti!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Bot sozlamalari
TOKEN = "8461895608:AAHrTyxLsnlyUnXLhoPltb3XOuwQXRGBBIE"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Pastki menyu tugmalari
def main_menu():
    kb = [
        [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
        [KeyboardButton(text="ℹ️ Ma'lumot"), KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Namoz vaqtlarini aniqlash uchun joylashuvingizni yuboring:",
        reply_markup=main_menu()
    )

@dp.message(lambda m: m.location is not None)
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=3"
    
    try:
        res = requests.get(url).json()
        t = res['data']['timings']
        d = res['data']['date']
        
        text = (
            f"🌍 **Hudud:** {res['data']['meta']['timezone']}\n"
            f"📅 **Sana:** {d['readable']} ({d['hijri']['day']} {d['hijri']['month']['en']})\n\n"
            f"🏙 **Bomdod:** {t['Fajr']}\n"
            f"☀️ **Quyosh:** {t['Sunrise']}\n"
            f"☀️ **Peshin:** {t['Dhuhr']}\n"
            f"🌇 **Asr:** {t['Asr']}\n"
            f"🌆 **Shom:** {t['Maghrib']}\n"
            f"🌃 **Xufton:** {t['Isha']}\n\n"
            f"✨ Ramazonga taxminan 25 kun qoldi."
        )
        await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
