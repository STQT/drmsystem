from aiohttp import ClientSession, ClientResponseError, ClientError


class Database:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = ClientSession(trust_env=True)

    async def make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint

        try:
            async with self.session.request(method, url, json=data) as resp:
                if resp.status in [200, 201]:
                    return await resp.json()
                else:
                    raise ClientResponseError(resp.request_info,
                                              resp.history,
                                              status=resp.status,
                                              message=resp.reason)
        except ClientError as e:
            raise e

    async def create_user(self, username: str,
                          user_id: int,
                          fullname: str,
                          user_lang: str = "uz", ):
        data = {
            "username": username,
            "password": 'password',
            "id": user_id,
            "user_lang": user_lang,
            "fullname": fullname
        }
        return await self.make_request("POST", "/users/", data)

    async def get_user(self, username: str,
                       user_id: int,
                       fullname: str,
                       user_lang: str = "uz", ):
        url = self.base_url + "/users/%s/" % str(user_id)
        async with self.session.request("GET", url) as resp:
            if resp.status == 200:
                return await resp.json()
            elif resp.status == 404:
                return await self.create_user(username=username,
                                              user_id=user_id,
                                              fullname=fullname,
                                              user_lang=user_lang)
            else:
                return None

    async def get_data(self):
        return await self.make_request("GET", "/users/1/")

    async def close(self):
        await self.session.close()
