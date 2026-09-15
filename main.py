import logging, os, asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, WebAppInfo
from aiohttp import web

BOT_TOKEN = "8810572867:AAEleoFb5RH4BW7yY4MGimQOcN8H93dfY8Q"
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(m: Message):
    kb = [[types.KeyboardButton(text="🎮 Play Free Game")],
          [types.KeyboardButton(text="🌟 Unlock Premium Game (5 Stars)")]]
    await m.answer("👋 **Welcome!**\n\n🎮 *Free Game*: Play Snake!\n🌟 *Premium Game*: Unlock Tetris for 5 Stars!", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True), parse_mode="Markdown")

@dp.message(F.text == "🎮 Play Free Game")
async def free_g(m: Message):
    await m.answer("🎮 **Free Game!**", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🚀 Launch Snake", web_app=WebAppInfo(url="https://gamepix.com"))]]))

@dp.message(F.text == "🌟 Unlock Premium Game (5 Stars)")
async def prem_g(m: Message):
    await bot.send_invoice(m.chat.id, "Premium Tetris", "Unlock Tetris!", "payload", "", "XTR", [LabeledPrice("Pass", 5)])

@dp.pre_checkout_query()
async def pre_c(q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

@dp.message(F.successful_payment)
async def succ_p(m: Message):
    await m.answer("🎉 **Unlocked!**", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🔥 Launch Tetris", web_app=WebAppInfo(url="https://gamepix.com"))]]))

# Render tekin rejasi so'raydigan majburiy port qismi
async def h(r):
    return web.Response(text="Bot is Live")

async def main():
    app = web.Application()
    app.router.add_get('/', h)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render so'ragan PORT shu erda avtomatik ochiladi
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(runner, '0.0.0.0', port).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


