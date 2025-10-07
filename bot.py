import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

# === LOG ===
logging.basicConfig(level=logging.INFO)

# === TOKEN ===
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render’da ortama ekleyeceğiz
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# === MESAJ (kaydedilen mesaj gibi davranacak metin) ===
MESSAGE_TO_SEND = "🔥 Merhaba! Bu mesaj bot tarafından otomatik gönderilmiştir."

# === GRUPLARA MESAJ GÖNDERME ===
async def send_to_all_groups():
    dialogs = await bot.get_updates()
    sent_count = 0
    try:
        async for dialog in bot.get_chat_administrators(chat_id=None):
            if dialog.chat.type in ["group", "supergroup"]:
                await bot.send_message(dialog.chat.id, MESSAGE_TO_SEND)
                sent_count += 1
        logging.info(f"{sent_count} gruba mesaj gönderildi.")
    except Exception as e:
        logging.error(f"Hata: {e}")

# === KOMUTLAR ===
@dp.message(commands=["start"])
async def start_command(msg: Message):
    await msg.answer("✅ Bot çalışıyor!\nHer 1 saatte bir tüm gruplara mesaj atılacak.")

# === PROGRAM ===
async def main():
    scheduler.add_job(send_to_all_groups, "interval", hours=1)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
