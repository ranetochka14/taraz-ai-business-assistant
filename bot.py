import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = "8647688191:AAELFYCIkdHgXlVIouicUEnjRarLzpmAu3U"

BACKEND_URL = "http://localhost:8000/api/chat/interact/"

BUSINESS_ID = 1

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  """Обработчик команды /start"""
  welcome_text = (
      "Привет! Я умный ИИ-ассистент бизнеса в Таразе.\n"
      "Спроси меня о меню, ценах или товарах нашей кофейни, и я с радостью"
      " помогу!"
  )
  await message.answer(welcome_text)


@dp.message()
async def handle_user_message(message: types.Message):
  """Обработчик всех текстовых сообщений от клиента"""
  client_id = str(message.from_user.id)
  user_text = message.text

  async with aiohttp.ClientSession() as session:
    payload = {
        "business_id": BUSINESS_ID,
        "client_id": client_id,
        "message": user_text,
    }
    try:
      async with session.post(BACKEND_URL, json=payload) as response:
        if response.status == 200:
          data = await response.json()
          ai_reply = data.get("ai_response", "Извините, произошла ошибка.")
          await message.answer(ai_reply)
        else:
          await message.answer(
              "Сервер временно недоступен. Попробуйте позже."
          )
    except Exception as e:
      logging.error(f"Ошибка связи с бэкендом: {e}")
      await message.answer("Не удалось связаться с сервером обработки данных.")


async def main():
  print("Бот запущен и ожидает сообщения...")
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())