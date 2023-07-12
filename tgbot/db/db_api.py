import aiohttp


async def get_user(user_id, config):
    return "uz"


from aiohttp import ClientSession


async def get_data():
    url = "http://django:8000/v1/users/1/"

    async with ClientSession(trust_env=True) as session:
        async with session.get(url) as resp:
            print(resp.status)
            return resp.status