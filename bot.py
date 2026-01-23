import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Render serverini o'chib qolmasligi uchun sozlash
app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 rejimida ishlamoqda!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Yangi TOKEN (Oxirgi urunish uchun)
TOKEN = "8461895608:AAHz0FEOLZYz0noIeNSlA6rIvsmLqq_Vceo"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Professional Menyu tugmalari
def main_menu():
    kb = [
        [KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
        [KeyboardButton(text="📅 Bugun"), KeyboardButton(text="🌅 Ertaga")],
        [KeyboardButton(text="🕋 Qibla yo'nalishi"), KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Assalomu alaykum! Namoz vaqtlari botiga xush kelibsiz.\n\n"
        "Aniq vaqtlarni bilish uchun pastdagi tugma orqali joylashuvingizni yuboring:",
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
            f"🟢 **Hudud:** {res['data']['meta']['timezone']}\n"
            f"📅 **Sana:** {d['readable']}\n"
            f"🌙 **Hijriy:** {d['hijri']['day']} {d['hijri']['month']['en']}\n\n"
            f"🏙 **Bomdod:** {t['Fajr']}\n"
            f"☀️ **Quyosh:** {t['Sunrise']}\n"
            f"☀️ **Peshin:** {t['Dhuhr']}\n"
            f"🌇 **Asr:** {t['Asr']}\n"
            f"🌆 **Shom:** {t['Maghrib']}\n"
            f"🌃 **Xufton:** {t['Isha']}\n\n"
            f"✨ Ramazon oyiga 25 kun qoldi inshaAllah."
        )
        await message.answer(text, parse_mode="Markdown")
    except:
        await message.answer("⚠️ Ma'lumot olishda xatolik yuz berdi.")

# Qo'shimcha tugmalar uchun javoblar
@dp.message(lambda m: m.text == "⚙️ Sozlamalar")
async def settings(message: types.Message):
    await message.answer("⚙️ Sozlamalar bo'limi tez kunda ishga tushadi.")

@dp.message(lambda m: m.text == "🕋 Qibla yo'nalishi")
async def qibla(message: types.Message):
    await message.answer("🕋 Qibla yo'nalishini aniqlash uchun joylashuvni yuborganingizdan so'ng hisoblab beriladi.")

async def main():
    keep_alive()
    # Eski buyruqlarni tozalash (o'sha sizga yoqmagan yozuv ketishi uchun)
    await bot.delete_my_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
