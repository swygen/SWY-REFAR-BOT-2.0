import os
from dotenv import load_dotenv

load_dotenv()

# --- এখানে পরিবর্তন করা হয়েছে ---
# os.getenv() বাদ দিয়ে সরাসরি স্ট্রিং হিসেবে ভ্যালু দেওয়া হয়েছে
BOT_TOKEN = "8297489470:AAEm-yNNdJknV9ed2Cgu27BMVmLHw40PiMI"
ADMIN_ID = 6243881362
BOT_USERNAME = "StudentIncome24Bot" # @ ছাড়া শুধু ইউজারনেম দিন

# JSONBIN Settings (সরাসরি ভ্যালু বসানো হয়েছে)
JSONBIN_API_KEY = "$2a$10$FZrUDvxPfpNkGZdCM5Vhm./BRJ9.Z4TeDruLGdis7gfBnSi35FCg2"
JSONBIN_BIN_ID = "6696bad42d0ea881f40726798" # আপনার দেওয়া ID তে একটি ডিজিট কম মনে হচ্ছে, চেক করে নিবেন। ছবিতে 696... ছিল।

# Channels to Join (Must be Public or Bot must be Admin)
CHANNELS = [
    "RedX_Developer", 
    "+el8iXkiC4rQ4OWRl",
    "+JiGeVU8nmr04NmQ1",
    "+rMEknXmGU5I4MDA1",
    "+ineRho4LwKo0ZjNl"
]

# Numeric Channel IDs
CHANNEL_IDS = [
    "@RedX_Developer", 
    -1003373517751, 
    -1003630796081,
    -1003662686257,
    -1003610754093
]
