import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# === LOG ===
logging.basicConfig(level=logging.INFO)

# === TOKEN ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render ortam değişkeninde ekle
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# === GRUPLARA MESAJ GÖNDERME ===
async def send_to_all_groups():
    try:
        # Kaydedilen mesajlardan son mesajı al
        saved = await bot.get_chat(chat_id="me")  # Saved Messages
        last_message = (await bot.get_chat_history(saved.id, limit=1)).messages[0].text

        # Mesajın başına CRYPTEX yaz
        MESSAGE_TO_SEND = f"CRYPTEX'in Botudur 🔥\n{last_message}"

        # Tüm gruplara gönder
        updates = await bot.get_updates()
        sent_count = 0
        for update in updates:
            if update.message and update.message.chat.type in ["group", "supergroup"]:
                await bot.send_message(update.message.chat.id, MESSAGE_TO_SEND)
                sent_count += 1
        logging.info(f"{sent_count} gruba mesaj gönderildi.")
    except Exception as e:
        logging.error(f"Hata: {e}")

# === KOMUT ===
@dp.message(F.text == "/start")
async def start_command(msg: types.Message):
    await msg.answer("✅ Bot çalışıyor!\nHer 1 saatte bir tüm gruplara kaydedilen son mesajı gönderecek.")

# === PROGRAM ===
async def main():
    scheduler.add_job(send_to_all_groups, "interval", hours=1)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
