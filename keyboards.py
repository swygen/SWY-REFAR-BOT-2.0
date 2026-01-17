from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_join_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Channel 1", url="https://t.me/RedX_Developer")],
        [InlineKeyboardButton(text="Channel 2", url="https://t.me/+el8iXkiC4rQ4OWRl")],
        [InlineKeyboardButton(text="Channel 3", url="https://t.me/+JiGeVU8nmr04NmQ1")],
        [InlineKeyboardButton(text="Channel 4", url="https://t.me/+rMEknXmGU5I4MDA1")],
        [InlineKeyboardButton(text="Channel 5", url="https://t.me/+ineRho4LwKo0ZjNl")],
        [InlineKeyboardButton(text="Joined 🟢", callback_data="check_join")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_main_menu():
    kb = [
        [KeyboardButton(text="প্রোফাইল"), KeyboardButton(text="রেফার")],
        [KeyboardButton(text="উত্তোলন"), KeyboardButton(text="নীতিমালা")],
        [KeyboardButton(text="সাপোর্ট")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_withdraw_methods():
    kb = [
        [KeyboardButton(text="বিকাশ"), KeyboardButton(text="নগদ"), KeyboardButton(text="রকেট")],
        [KeyboardButton(text="Back")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_admin_dashboard():
    kb = [
        [KeyboardButton(text="এড ইউজার রেফার")],
        [KeyboardButton(text="উত্তোলন দেখুন")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_referral_share(bot_username, user_id):
    link = f"https://t.me/{bot_username}?start={user_id}"
    buttons = [
        [InlineKeyboardButton(text="Share Link 🔗", url=f"https://t.me/share/url?url={link}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_payment_proof_kb(user_id):
    buttons = [
        [InlineKeyboardButton(text="Yes", callback_data=f"proof_yes_{user_id}"), 
         InlineKeyboardButton(text="No", callback_data=f"proof_no_{user_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)