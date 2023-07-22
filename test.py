import aiohttp
import asyncio

async def create_order():
    url = "https://icecreambot.itlink.uz/v1/orders/"
    headers = {"Content-Type": "application/json"}
    data = {
        "address": "9A, Mirobod ko'chasi, Hamid Sulaymonov mahallasi, Yakkasaroy Tumani, Toshkent, 100000, Oʻzbekiston",
        "check_id": "Naqd pul",
        "phone": "+77473793994",
        "payment_method": "Naqd pul",
        "cost": 13333,
        "products": [
            {
                "product_lang": "uz",
                "product_name": "Krem-bruli muzqaymoq",
                "count": "1"
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status in [200, 201]:
                result = await response.json()
                print(result)
            else:
                print(f"Request failed with status: {response.status} - {response.reason}")

# Run the asyncio event loop to execute the async function
loop = asyncio.get_event_loop()
loop.run_until_complete(create_order())
