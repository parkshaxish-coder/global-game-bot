import logging
import json
import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, WebAppInfo
from aiohttp import web

BOT_TOKEN = "8810572867:AAEleoFb5RH4BW7yY4MGimQOcN8H93dfY8Q"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

SCORES_FILE = "scores.json"

def get_leaderboard():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        try:
            data = json.load(f)
            return sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]
        except:
            return []

@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [types.KeyboardButton(text="🎮 Play Free Game")],
        [types.KeyboardButton(text="🌟 Unlock Premium Game (5 Stars)")],
        [types.KeyboardButton(text="🏆 View Leaderboard")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        "👋 **Welcome to the Global Gaming Arena!**\n\n"
        "🎮 *Free Game*: Play our classic retro game immediately without any limits.\n"
        "🌟 *Premium Game*: Unlock our advanced game by paying 5 Telegram Stars!\n"
        "🏆 *Leaderboard*: Check out the top players worldwide!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.text == "🏆 View Leaderboard")
@dp.message(Command("leaderboard"))
async def show_leaderboard(message: Message):
    leaderboard = get_leaderboard()
    if not leaderboard:
        await message.answer("🏆 **Global Leaderboard**\n\nNo scores recorded yet. Be the first to play and set a high score!")
        return
    text = "🏆 **Global Leaderboard - Top Players**\n\n"
    medals = ["🥇", "🥈", "🥉"]
    for index, (username, score) in enumerate(leaderboard):
        prefix = medals[index] if index < 3 else f"{index + 1}."
        text += f"{prefix} @{username} — `{score} pts`\n"
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "🎮 Play Free Game")
async def play_free_game(message: Message):
    FREE_GAME_URL = "https://gamepix.com" 
    kb = [[types.InlineKeyboardButton(text="🚀 Launch Free Snake", web_app=WebAppInfo(url=FREE_GAME_URL))]]
    inline_kb = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(
        "🎮 **Free Game is Ready!**\n\n🐍 Enjoy the legendary **Classic Snake** right inside your Telegram app.",
        reply_markup=inline_kb,
        parse_mode="Markdown"
    )

@dp.message(F.text == "🌟 Unlock Premium Game (5 Stars)")
async def buy_premium_game(message: Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Premium Tetris Access",
        description="Get full access to the Premium Tetris block puzzle game!",
        payload="premium_tetris_access_payload",
        provider_token="", 
        currency="XTR",   
        prices=[LabeledPrice(label="Premium Pass", amount=5)] 
    )

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    if payload == "premium_tetris_access_payload":
        PREMIUM_GAME_URL = "https://gamepix.com" 
        kb = [[types.InlineKeyboardButton(text="🔥 Launch Premium Tetris", web_app=WebAppInfo(url=PREMIUM_GAME_URL))]]
        inline_kb = types.InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(
            "🎉 **Payment Verified Successfully! Thank you!**\n\n🌟 Click below to launch your Premium Game instantly!",
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )

# Render sayti so'ragan majburiy soxta port tizimi
async def handle(request):
    return web.Response(text="Bot is running!")

async def main():
    # Soxta veb-serverni orqa fonda yoqish
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())
    
    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


