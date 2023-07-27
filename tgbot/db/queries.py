import logging

from aiohttp import ClientSession, ClientResponseError, ClientError


class Database:
    # DELIVERY_COST = "10000"

    def __init__(self, base_url):
        self.base_url = base_url

    async def make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint

        try:
            async with ClientSession() as session:
                async with session.request(method, url, json=data) as resp:
                    # r = await resp.json()
                    # logging.info(r)
                    if resp.status in [200, 201]:
                        return await resp.json(), resp.status
                    else:
                        raise ClientResponseError(resp.request_info,
                                                  resp.history,
                                                  status=resp.status,
                                                  message=resp.reason)
        except ClientError as e:
            raise e
        finally:
            await session.close()

    async def create_user(self, username: str,
                          user_id: int,
                          fullname: str,
                          user_lang: str = "uz"):
        data = {
            "username": username,
            "password": 'password',
            "id": user_id,
            "user_lang": user_lang,
            "fullname": fullname.replace("'", "´").replace('"', "”")
        }
        return await self.make_request("POST", "/users/", data)

    async def update_user(self, username: str,
                          user_id: int,
                          fullname: str,
                          user_lang: str = "uz"):
        data = {
            "username": username,
            "password": 'password',
            "id": user_id,
            "user_lang": user_lang,
            "fullname": fullname
        }
        return await self.make_request("PATCH",
                                       "/users/" + str(user_id) + "/", data)

    async def get_user(self, username: str,
                       user_id: int,
                       fullname: str,
                       user_lang: str = "uz", ):
        resp, _status = await self.make_request("GET", "/users/%s/" % str(user_id))
        if _status != 200:
            resp, _status = await self.create_user(
                username=username,
                user_id=user_id,
                fullname=fullname,
                user_lang=user_lang
            )
        return resp

    async def get_user_locations(self, user_id):
        return await self.make_request("GET",
                                       f"/users/{user_id}/get_locations/")

    async def delete_user_locations(self, user_id):
        return await self.make_request("GET",
                                       f"/users/{user_id}/clear_locations/")

    async def create_user_location(self,
                                   user_id: int,
                                   longitude: float,
                                   latitude: float,
                                   address: str):
        data = {
            "user_id": user_id,
            "longitude": longitude,
            "latitude": latitude,
            "name": address.replace("'", "´").replace('"', "”")
        }
        return await self.make_request("POST", "/user-locations/", data)

    async def get_categories(self):
        return await self.make_request("GET", "/categories/")

    async def get_products(self, category, user_lang):
        return await self.make_request(
            "GET",
            f"/products/?category__name_{user_lang}={category}")

    async def get_product(self, name, user_lang):
        _resp, status = await self.make_request("GET", f"/product_by_name/{user_lang}/{name}")
        if status != 200:
            return _resp
        return _resp

    async def update_product(self, product_id, data):
        return await self.make_request(
            "PATCH",
            f"/products/{str(product_id)}/", data)

    async def create_order(self, data):
        logging.info(data)
        return await self.make_request("POST", "/orders/", data)
