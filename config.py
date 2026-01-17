import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8297489470:AAEm-yNNdJknV9ed2Cgu27BMVmLHw40PiMI")
ADMIN_ID = 6243881362
BOT_USERNAME = os.getenv("StudentIncome24Bot", "STUDENT INCOME 24") # without @

# JSONBIN Settings
JSONBIN_API_KEY = os.getenv("$2a$10$FZrUDvxPfpNkGZdCM5Vhm./BRJ9.Z4TeDruLGdis7gfBnSi35FCg2")
JSONBIN_BIN_ID = os.getenv("696bad42d0ea881f40726798")

# Channels to Join (Must be Public or Bot must be Admin)
CHANNELS = [
    "RedX_Developer", 
    "+el8iXkiC4rQ4OWRl",
    "+JiGeVU8nmr04NmQ1",
    "+rMEknXmGU5I4MDA1",
    "+ineRho4LwKo0ZjNl"
]

# Numeric Channel IDs (for checking status)
# IMPORTANT: You need to replace these with the actual numeric IDs (e.g. -100xxxx)
# Use a bot like @JsonDumpBot to forward messages from these channels to get IDs.
# For this code to work strictly with links, we need to resolve them, 
# but for stability, users should put Numeric IDs here.
# I will implement a logic that attempts to use them as provided, 
# but usually, you need -100 IDs for private channels.
CHANNEL_IDS = [
    "@RedX_Developer", # Public example
    # For private invite links, you MUST use the -100 ID in production
    # Placeholder IDs below:
    -1003373517751, 
    -1003630796081,
    -1003662686257,
    -1003610754093
]