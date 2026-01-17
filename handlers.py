from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import config
from database import db
from keyboards import *

router = Router()

class WithdrawState(StatesGroup):
    choosing_method = State()
    entering_number = State()

class AdminState(StatesGroup):
    waiting_id = State()
    waiting_amount = State()
    waiting_proof = State()
    confirm_proof = State()

# --- Helper to Check Channels ---
async def check_all_channels(bot: Bot, user_id: int) -> bool:
    for channel in config.CHANNEL_IDS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception as e:
            # If bot can't see channel (not admin), assume True or Log Error
            print(f"Error checking channel {channel}: {e}")
            continue
    return True

# --- Start Handler ---
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Check if referral
    args = message.text.split()
    referrer_id = None
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])
        if referrer_id == user_id: 
            referrer_id = None # Cannot refer self

    # Check if user exists
    user = await db.get_user(user_id)
    
    if not user:
        # Create pending user
        new_user = {
            "name": first_name,
            "balance": 0,
            "refer_count": 0,
            "join_date": str(datetime.now().date()),
            "status": "pending",
            "referred_by": referrer_id,
            "id": user_id
        }
        await db.update_user(user_id, new_user)
        
    await message.answer(
        f"প্রিয় {first_name} আপনাকে স্বাগতম Bot এ । এখানে রেফার করার মাধ্যমে আপনি টাকা ইনকাম করতে পারবেন । বট চালু করতে নিচের চ্যানেল গুলো তে জয়েন করুন ধন্যবাদ",
        reply_markup=get_join_keyboard()
    )

# --- Join Verification ---
@router.callback_query(F.data == "check_join")
async def verify_join(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    is_joined = await check_all_channels(bot, user_id)
    
    if is_joined:
        user = await db.get_user(user_id)
        if user and user.get("status") != "active":
            # Activate User
            user["status"] = "active"
            user["balance"] += 100 # Welcome Bonus
            await db.update_user(user_id, user)
            
            # Handle Referrer Reward
            if user.get("referred_by"):
                ref_id = user["referred_by"]
                ref_user = await db.get_user(ref_id)
                if ref_user:
                    ref_user["balance"] += 20
                    ref_user["refer_count"] += 1
                    await db.update_user(ref_id, ref_user)
                    try:
                        await bot.send_message(ref_id, f"আপনার রেফার লিংক ব্যবহার করে নতুন একজন যুক্ত হয়েছে! আপনি ২০ টাকা পেয়েছেন।")
                    except: pass

        await call.message.delete()
        await call.message.answer(
            f"প্রিয় {call.from_user.first_name} আপনাকে ধন্যবাদ সবগুলো চ্যানেল এ জয়েন করার জন্য | স্বাগতম বোনাস হিসেবে পাচ্ছেন ১০০ টাকা বোনাস | এবং প্রতি সফল রেফার এ পাবেন ২০ টাকা করে | ধন্যবাদ ™",
            reply_markup=get_main_menu()
        )
    else:
        await call.answer("আপনি এখনও কিছু চ্যানেল জয়েন করেননি।", show_alert=True)

# --- Profile ---
@router.message(F.text == "প্রোফাইল")
async def show_profile(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user or user["status"] != "active": return
    
    msg = f"""
👤 **Name:** {user['name']}
🆔 **User ID:** `{user['id']}`
💰 **Balance:** {user['balance']} BDT
👥 **Total Refer:** {user['refer_count']}
📅 **Join Date:** {user['join_date']}
    """
    await message.answer(msg, parse_mode="Markdown")

# --- Referral ---
@router.message(F.text == "রেফার")
async def show_refer(message: Message):
    user_id = message.from_user.id
    await message.answer(
        "আপনার রেফারেল লিংক তৈরি হয়েছে। এটি শেয়ার করুন:",
        reply_markup=get_referral_share(config.BOT_USERNAME, user_id)
    )

# --- Withdraw Flow ---
@router.message(F.text == "উত্তোলন")
async def start_withdraw(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user: return
    
    if user['refer_count'] < 20:
        remaining = 20 - user['refer_count']
        await message.answer(
            f"প্রিয় {user['name']} আপনার সর্বমোট রেফার {user['refer_count']} এবং সর্বমোট ব্যালেন্স {user['balance']} । রূলস অনুযায়ী আপনাকে সর্বমোট ২০ টি রেফার কমপ্লিট করতে হবে অন্যথায় উত্তোলন করতে পারবেন না । দয়া করে বাকি {remaining} টি রেফার কমপ্লিট করুন এবং আবারো চেষ্টা করুন । ধন্যবাদ ™"
        )
        return

    if user['balance'] < 500:
        await message.answer("আপনার ব্যালেন্স পর্যাপ্ত নয়। মিনিমাম ৫০০ টাকা।")
        return

    await message.answer("পেমেন্ট মেথড সিলেক্ট করুন:", reply_markup=get_withdraw_methods())
    await state.set_state(WithdrawState.choosing_method)

@router.message(WithdrawState.choosing_method)
async def process_method(message: Message, state: FSMContext):
    if message.text == "Back":
        await state.clear()
        await message.answer("Main Menu", reply_markup=get_main_menu())
        return

    await state.update_data(method=message.text)
    await message.answer(f"আপনার সঠিক {message.text} একাউন্ট নাম্বার দিন", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Cancel")]], resize_keyboard=True))
    await state.set_state(WithdrawState.entering_number)

@router.message(WithdrawState.entering_number)
async def process_withdraw(message: Message, state: FSMContext, bot: Bot):
    if message.text == "Cancel":
        await state.clear()
        await message.answer("Cancelled", reply_markup=get_main_menu())
        return

    data = await state.get_data()
    method = data['method']
    number = message.text
    user_id = message.from_user.id
    
    user = await db.get_user(user_id)
    amount = user['balance']
    
    # Deduct Balance
    user['balance'] = 0
    await db.update_user(user_id, user)
    
    # Notify Admin
    msg_admin = f"🔔 **New Withdraw Request**\nUser: {user['name']} (`{user_id}`)\nAmount: {amount}\nMethod: {method}\nNumber: `{number}`"
    
    # Send to Admin (Assuming Admin handles via command or manual check for now, simplified)
    await bot.send_message(config.ADMIN_ID, msg_admin, reply_markup=get_payment_proof_kb(user_id))
    
    await message.answer(
        f"প্রিয় {user['name']} আপনার উত্তোলন রিকোয়েস্ট সঠিকভাবে গৃহীত হয়েছে । দয়া করে কিছুক্ষণ অপেক্ষা করুন আপনার দেওয়া {method} এ {amount} টাকা পাঠানো হবে । ধন্যবাদ ™",
        reply_markup=get_main_menu()
    )
    await state.clear()

# --- Admin Handlers (Simplified) ---
@router.callback_query(F.data.startswith("proof_"))
async def admin_proof_check(call: CallbackQuery, state: FSMContext):
    action, user_id = call.data.split("_")[1], call.data.split("_")[2]
    
    if action == "no":
        await call.message.edit_text("Marked as Complete (No Proof Sent).")
        await call.bot.send_message(user_id, "উত্তোলন সফলভাবে সম্পন্ন হয়েছে")
    elif action == "yes":
        await call.message.answer("Please upload the screenshot now.")
        await state.update_data(target_user=user_id)
        await state.set_state(AdminState.waiting_proof)
    
    await call.answer()

@router.message(AdminState.waiting_proof, F.photo)
async def admin_send_proof(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_user = data['target_user']
    photo_id = message.photo[-1].file_id
    
    await bot.send_photo(target_user, photo_id, caption="উত্তোলন সফলভাবে সম্পন্ন হয়েছে")
    await message.answer("Proof sent to user.")
    await state.clear()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id == config.ADMIN_ID:
        await message.answer("Admin Panel", reply_markup=get_admin_dashboard())

@router.message(F.text == "এড ইউজার রেফার")
async def admin_add_refer_start(message: Message, state: FSMContext):
    if message.from_user.id == config.ADMIN_ID:
        await message.answer("Enter User ID:")
        await state.set_state(AdminState.waiting_id)

@router.message(AdminState.waiting_id)
async def admin_got_id(message: Message, state: FSMContext):
    await state.update_data(uid=message.text)
    await message.answer("How many refers to add?")
    await state.set_state(AdminState.waiting_amount)

@router.message(AdminState.waiting_amount)
async def admin_add_refer_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    uid = data['uid']
    count = int(message.text)
    
    user = await db.get_user(uid)
    if user:
        user['refer_count'] += count
        user['balance'] += (count * 20)
        await db.update_user(uid, user)
        await message.answer("Updated successfully.")
    else:
        await message.answer("User not found.")
    await state.clear()

# --- Rules & Support ---
@router.message(F.text == "নীতিমালা")
async def rules(message: Message):
    txt = "1) Minimum 20 refers required to withdraw\n2) Balance must be 500 or above\n3) No cheating or leaving channels\n4) Bot checks every 2 minutes"
    await message.answer(txt)

@router.message(F.text == "সাপোর্ট")
async def support(message: Message):
    await message.answer("Support: https://swygen.xyz")