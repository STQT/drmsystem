import asyncio
from geopy.geocoders import Nominatim


async def get_location_name_async(latitude, longitude):
    loop = asyncio.get_event_loop()
    geolocator = Nominatim(user_agent="Svetlogorsk")

    location = await loop.run_in_executor(None, geolocator.reverse, (latitude, longitude))

    return location.address
