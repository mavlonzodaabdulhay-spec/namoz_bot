import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# 1. Render serverini uxlab qolmasligi uchun sozlash
app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 ishlamoqda!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. Yangi TOKEN sozlamalari (@Namozvoqti_bot)
TOKEN = "8456499271:AAEuc6zQc76bz0sXwvG2mHOiSZwzTMR1o9I"
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
        "Assalomu alaykum! @Namozvoqti_bot ga xush kelibsiz.\n"
        "Namoz vaqtlarini aniqlash uchun quyidagi tugmalardan foydalaning:",
        reply_markup=main_menu()
    )

# 📅 BUGUN tugmasi
@dp.message(F.text == "📅 Bugun")
async def today_info(message: types.Message):
    await message.answer("Bugungi namoz vaqtlarini yangilash uchun 📍 Joylashuvni yuborish tugmasini bosing.")

# 🌅 ERTAGA tugmasi
@dp.message(F.text == "🌅 Ertaga")
async def tomorrow_info(message: types.Message):
    await message.answer("Ertangi namoz vaqtlari tizimi sozlanmoqda. Hozircha faqat bugungi vaqtlarni ko'rishingiz mumkin.")

# 🕋 QIBLA tugmasi
@dp.message(F.text == "🕋 Qibla yo'nalishi")
async def qibla_info(message: types.Message):
    await message.answer("🕋 O'zbekiston bo'yicha Qibla yo'nalishi taxminan 251° (Janubi-g'arb) tomonda.")

# ⚙️ SOZLAMALAR tugmasi
@dp.message(F.text == "⚙️ Sozlamalar")
async def settings_info(message: types.Message):
    await message.answer("⚙️ Sozlamalar: Bot hozirda O'zbek tilida ishlamoqda.")

# JOYLASHUVNI QABUL QILISH VA VAQTLARNI CHIQARISH
@dp.message(F.location)
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
    except Exception:
        await message.answer("⚠️ Ma'lumot olishda xatolik yuz berdi.")

async def main():
    keep_alive()
    # Eski xatoliklarni tozalash uchun
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
