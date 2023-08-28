from aiohttp import ClientSession, ClientResponseError, ClientError

from tgbot.config import Config


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

    async def update_user(self, user_id: int, data: dict):
        return await self.make_request("PATCH",
                                       "/users/" + str(user_id) + "/", data)

    async def get_user(self, user_id: int):
        url = self.base_url + "/users/%s/" % str(user_id)
        async with ClientSession() as session:
            async with session.request('GET', url) as resp:
                if resp.status not in [200, 201]:
                    # resp, _status = await self.create_user(
                    #     username=username,
                    #     user_id=user_id,
                    #     fullname=fullname,
                    #     user_lang=user_lang
                    # )
                    return None, None
                else:
                    response = await resp.json()
                return response, resp.status

    async def create_or_update_user(self, user_id, fullname, username, config: Config):
        if user_id in config.tg_bot.admin_ids:
            return
        return await self.make_request("POST", "/users/",
                                       {'fullname': fullname, 'username': username, 'id': user_id,
                                        'stopped': False, 'password': '12345678aA'})

    async def get_organizations_list(self):
        return await self.make_request("GET", "/organizations/")

    async def get_organization_obj(self, slug):
        url = self.base_url + f"/organizations/{str(slug)}/"

        try:
            async with ClientSession() as session:
                async with session.request("GET", url) as resp:
                    # r = await resp.json()
                    # logging.info(r)
                    if resp.status in [200, 201]:
                        return await resp.json(), resp.status
                    elif resp.status == 404:
                        return None, resp.status
                    else:
                        raise ClientResponseError(resp.request_info,
                                                  resp.history,
                                                  status=resp.status,
                                                  message=resp.reason)
        except ClientError as e:
            raise e
        finally:
            await session.close()

    async def create_order(self, data):
        url = self.base_url + "/orders/"
        try:
            async with ClientSession() as session:
                async with session.request("POST", url, json=data) as resp:
                    if resp.status in [200, 201]:
                        return await resp.json(), resp.status
                    else:
                        return None, resp.status
        finally:
            await session.close()

    async def update_order(self, order_id, data):
        return await self.make_request("PATCH", f"/orders/{order_id}/", data)

    async def get_user_orders(self, user_id):
        return await self.make_request("GET", f"/orders/?user__id={user_id}")

    async def get_users_by_pagination(self, page=1):
        return await self.make_request("GET", f"/users/?page={page}")

    async def get_prices(self):
        return await self.make_request("GET", "/prices/")

    async def update_organization(self, product_id, data):
        return await self.make_request(
            "PATCH",
            f"/organizations/{str(product_id)}/", data)

    async def get_user_subscribe(self, user_id):
        url = self.base_url + f"/subscriber/{str(user_id)}/"
        async with ClientSession() as session:
            async with session.request('GET', url) as resp:
                if resp.status not in [200, 201]:
                    return None, None
                else:
                    response = await resp.json()
                return response, resp.status
