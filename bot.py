from datetime import date

# ... (funksiya ichida)
ramazon_sana = date(2026, 3, 1) # 2026-yilgi Ramazonning taxminiy sanasi
bugun = date.today()
qolgan_kun = (ramazon_sana - bugun).days

# Matn qismini shunday o'zgartiring:
text = (
    f"🏙 **Bomdod:** {t['Fajr']}\n"
    f"☀️ **Peshin:** {t['Dhuhr']}\n"
    f"🌇 **Asr:** {t['Asr']}\n"
    f"🌆 **Shom:** {t['Maghrib']}\n"
    f"🌃 **Xufton:** {t['Isha']}\n\n"
    f"🌙 **Ramazongacha {qolgan_kun} kun qoldi.**"
)
