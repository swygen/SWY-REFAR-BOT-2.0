import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiohttp import web
import config
from handlers import router
from background import check_users_task

# Logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Bot Setup
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

# Web Server for Render (Keep Alive)
async def handle_ping(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.add_routes([web.get('/', handle_ping)])

async def on_startup(bot: Bot):
    # Start Cron Job
    asyncio.create_task(check_users_task(bot))
    # Set webhook or just log
    print("Bot Started")

async def main():
    # Setup Web Server runner
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    
    # Start Bot (Polling is easiest for this setup, Webhook is complex with Render without domain)
    # Note: On Render free tier, Polling is fine if you use the keep-alive script logic properly
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
