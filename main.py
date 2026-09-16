import logging, os, asyncio, json, aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, WebAppInfo
from aiohttp import web

BOT_TOKEN = "8810572867:AAEleoFb5RH4BW7yY4MGimQOcN8H93dfY8Q"
# Render bepul sayti beradigan ixtiyoriy domen nomi (pastda avtomatik aniqlanadi)
APP_NAME = "://onrender.com" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

FILE_PATH = "scores.json"

def get_lb():
    if not os.path.exists(FILE_PATH): return []
    with open(FILE_PATH, "r") as f:
        try: return sorted(json.load(f).items(), key=lambda x: x, reverse=True)[:10]
        except: return []

@dp.message(Command("start"))
async def cmd_start(m: Message):
    kb = [[types.KeyboardButton(text="🎮 Play Free Game")],
          [types.KeyboardButton(text="🌟 Unlock Premium Game (5 Stars)")],
          [types.KeyboardButton(text="🏆 View Leaderboard")]]
    await m.answer("👋 **Welcome to Global Arcade Games!**\n\n🎮 *Free Game*: Play Snake!\n🌟 *Premium Game*: Unlock Tetris for 5 Stars!\n🏆 *Leaderboard*: See the top players worldwide!", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True), parse_mode="Markdown")

@dp.message(F.text == "🏆 View Leaderboard")
async def show_lb(m: Message):
    lb = get_lb()
    if not lb:
        return await m.answer("🏆 **Global Leaderboard**\n\nNo scores recorded yet. Be the first to play and set a high score!")
    txt = "🏆 **Global Leaderboard - Top Players**\n\n"
    for i, (usr, scr) in enumerate(lb):
        txt += f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else f'{i+1}.'} @{usr} — `{scr} pts`\n"
    await m.answer(txt, parse_mode="Markdown")

@dp.message(F.text == "🎮 Play Free Game")
async def free_g(m: Message):
    await m.answer("🎮 **Free Game is Ready!**", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🚀 Launch Snake", web_app=WebAppInfo(url="https://gamepix.com"))]]))

@dp.message(F.text == "🌟 Unlock Premium Game (5 Stars)")
async def prem_g(m: Message):
    await bot.send_invoice(
        chat_id=m.chat.id, title="Premium Tetris", description="Unlock Tetris Game!", 
        payload="premium_pass_payload", provider_token="", currency="XTR", 
        prices=[LabeledPrice(label="Pass", amount=5)]
    )

@dp.pre_checkout_query()
async def pre_c(q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

@dp.message(F.successful_payment)
async def succ_p(m: Message):
    await m.answer("🎉 **Unlocked!**", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="🔥 Launch Tetris", web_app=WebAppInfo(url="https://gamepix.com"))]]))

async def h(r):
    return web.Response(text="Bot is Active")

# 🔄 SERVERNI HAR 5 DAQIQADA AVTOMATIK UYG'OTIB TURUVCHI TIZIM (PINGER)
async def keep_alive():
    await asyncio.sleep(30) # Bot birinchi marta yonganda 30 soniya kutadi
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://{APP_NAME}"
                async with session.get(url) as response:
                    logging.info(f"Self-ping successful: {response.status}. Server is awake!")
        except Exception as e:
            logging.error(f"Self-ping failed: {e}")
        await asyncio.sleep(300) # Har 5 daqiqada (300 soniya) avtomatik takrorlanadi

async def main():
    app = web.Application()
    app.router.add_get('/', h)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(runner, '0.0.0.0', port).start()
    
    # Uyg'otuvchi pinger funksiyasini orqa fonda tinimsiz yoqib qo'yish
    asyncio.create_task(keep_alive())
    
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())


