import asyncio
from database import db
import config

async def check_users_task(bot):
    while True:
        try:
            # Sleep first to allow bot startup
            await asyncio.sleep(120) 
            
            all_users = await db.get_all_users()
            
            # Use semaphore to limit concurrent checks (Avoid FloodWait)
            for uid, data in all_users.items():
                if data.get('status') == 'active':
                    is_member = True
                    for channel in config.CHANNEL_IDS:
                        try:
                            member = await bot.get_chat_member(chat_id=channel, user_id=int(uid))
                            if member.status in ['left', 'kicked']:
                                is_member = False
                                break
                        except:
                            # If error, skip checking this user to be safe
                            continue
                    
                    if not is_member:
                        data['status'] = 'blocked'
                        await db.update_user(uid, data)
                        try:
                            await bot.send_message(uid, "আপনি চ্যানেল থেকে বের হয়ে গেছেন। আবার জয়েন করুন: /start")
                        except:
                            pass
                    
                    # Sleep between users to be gentle on Telegram API
                    await asyncio.sleep(0.5) 
                    
        except Exception as e:
            print(f"Cron Error: {e}")
            await asyncio.sleep(60)