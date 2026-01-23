import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Render uchun Web Server
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Sozlamalar
TOKEN = "8461895608:AAHz0FEOLZYz0noIeNSlA6rIvsmLqq_Vceo"
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
    await message.answer("Xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=main_menu())

# BUGUN tugmasi uchun
@dp.message(F.text == "📅 Bugun")
async def today_info(message: types.Message):
    await message.answer("Iltimos, bugungi vaqtlarni yangilash uchun 📍 Joylashuvni yuborish tugmasini bosing.")

# ERTAGA tugmasi uchun
@dp.message(F.text == "🌅 Ertaga")
async def tomorrow_info(message: types.Message):
    await message.answer("Ertangi namoz vaqtlari bo'limi hozirda sozlanmoqda.")

# QIBLA tugmasi uchun
@dp.message(F.text == "🕋 Qibla yo'nalishi")
async def qibla_info(message: types.Message):
    await message.answer("🕋 Qibla yo'nalishi Toshkent shahri bo'yicha: Janubi-g'arb (251°).")

# SOZLAMALAR tugmasi uchun
@dp.message(F.text == "⚙️ Sozlamalar")
async def settings_info(message: types.Message):
    await message.answer("⚙️ Sozlamalar: Til - O'zbekcha. (Boshqa sozlamalar tez kunda).")

# LOKATSIYA kelganda ishlaydigan asosiy qism
@dp.message(F.location)
async def handle_location(message: types.Message):
    lat, lon = message.location.latitude, message.location.longitude
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=3"
    res = requests.get(url).json()
    t = res['data']['timings']
    
    text = (
        f"🏙 Bomdod: {t['Fajr']}\n☀️ Quyosh: {t['Sunrise']}\n"
        f"☀️ Peshin: {t['Dhuhr']}\n🌇 Asr: {t['Asr']}\n"
        f"🌆 Shom: {t['Maghrib']}\n🌃 Xufton: {t['Isha']}"
    )
    await message.answer(f"📍 Tanlangan hudud bo'yicha vaqtlar:\n\n{text}")

async def main():
    keep_alive()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
