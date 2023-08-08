import asyncio

import aiohttp
import os  # Import the os module to work with file paths
from aiogram import Bot, types, Dispatcher
import logging

API_TOKEN = '6522526477:AAF2Tt50hzFVeHTTyeJJ1ar8rKs60cueDBg'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Enable logging to see the detailed log of what's happening
logging.basicConfig(level=logging.INFO)


# async def upload_photo_to_api(photo_path):
#     url = "http://your_drf_api_endpoint/photo_upload/"  # Replace with your DRF API endpoint
#
#     # Upload the photo to your DRF API using aiohttp
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, data={'photo': open(photo_path, 'rb')}) as response:
#             if response.status == 201:
#                 logging.info("Photo uploaded successfully!")
#             else:
#                 logging.error("Failed to upload photo:", await response.text())


@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def handle_photo(message: types.Message):
    # Get the largest photo size available (last item in the list)
    photo = message.photo[-1]

    # Download the photo using the file ID
    photo_file = await message.photo[-1].download()
    print(photo_file)



    # Upload the photo to your DRF API
    # await upload_photo_to_api(absolute_photo_path)


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
