import asyncio
import logging

from geopy.geocoders import Nominatim


async def get_location_name_async(latitude, longitude) -> str:
    loop = asyncio.get_event_loop()
    geolocator = Nominatim(user_agent="Svetlogorsk2")

    location = await loop.run_in_executor(None, geolocator.reverse, (latitude, longitude))
    # address_components = location.raw.get("address", {})
    # city = address_components.get("city", "")
    # county = address_components.get("county", "")
    # street = address_components.get("road", "")
    # home_number = address_components.get("house_number", "")
    # short_address_components = [comp for comp in [street, home_number, county, city] if comp]
    # short_address = ", ".join(short_address_components)
    #
    # return short_address if address_components['country_code'] == 'uz' else None
    return location.address
