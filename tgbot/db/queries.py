class Database:
    API_URL = 'http://localhost:8000'

    async def get_user(self, user_id: int):
        return {
            "user_lang": "uz"
        }