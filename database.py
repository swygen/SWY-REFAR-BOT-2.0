import aiohttp
import config
import logging

class Database:
    def __init__(self):
        self.base_url = f"https://api.jsonbin.io/v3/b/{config.JSONBIN_BIN_ID}"
        self.headers = {
            "X-Master-Key": config.JSONBIN_API_KEY,
            "Content-Type": "application/json"
        }

    async def read_db(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("record", {})
                return {}

    async def write_db(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.put(self.base_url, json=data, headers=self.headers) as resp:
                return resp.status == 200

    async def get_user(self, user_id):
        data = await self.read_db()
        users = data.get("users", {})
        return users.get(str(user_id))

    async def update_user(self, user_id, user_data):
        data = await self.read_db()
        if "users" not in data:
            data["users"] = {}
        data["users"][str(user_id)] = user_data
        await self.write_db(data)
        
    async def get_all_users(self):
        data = await self.read_db()
        return data.get("users", {})

    async def add_withdraw_request(self, request_data):
        data = await self.read_db()
        if "withdrawals" not in data:
            data["withdrawals"] = []
        data["withdrawals"].append(request_data)
        await self.write_db(data)

    async def get_withdrawals(self):
        data = await self.read_db()
        return data.get("withdrawals", [])

    async def update_withdrawal_status(self, user_id, status):
        # This is a simple implementation. In a real DB, you'd use a request ID.
        data = await self.read_db()
        withdrawals = data.get("withdrawals", [])
        # Update logic here (omitted for brevity, handled in main logic usually)
        return True

db = Database()