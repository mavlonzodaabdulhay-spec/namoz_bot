import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread

# 1. Web server (Render o'chirib qo'ymasligi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot tirik!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot sozlamalari
TOKEN = "8461895608:AAHrTyxLsnlyUnXLhoPltb3XOuwQXRGBBIE"
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_namoz_vaqti():
    url = "http://api.aladhan.com/v1/timingsByCity?city=Tashkent&country=Uzbekistan&method=3"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            t = data['data']['timings']
            text = (
                f"📅 Bugun: {data['data']['date']['readable']}\n"
                f"🏙 Bomdod: {t['Fajr']}\n☀️ Quyosh: {t['Sunrise']}\n"
                f"☀️ Peshin: {t['Dhuhr']}\n🌇 Asr: {t['Asr']}\n"
                f"🌆 Shom: {t['Maghrib']}\n🌃 Xufton: {t['Isha']}"
            )
            return text
    except:
        return "Xatolik yuz berdi."
    return "Ma'lumot topilmadi."

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(f"Assalomu alaykum!\n\n{get_namoz_vaqti()}")

async def main():
    keep_alive() # Serverni ishga tushirish
    print("Bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
