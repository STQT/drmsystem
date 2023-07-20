import logging

import aioredis


async def get_redis():
    # Create a Redis connection
    redis = await aioredis.create_redis_pool('redis://redis:6380/0')
    return redis


async def get_user_shopping_cart(user_id):
    redis = await get_redis()
    key = f"shopping_cart:{user_id}"
    cart_items = await redis.hgetall(key)
    decoded_cart_items = {key.decode('utf-8'): value.decode('utf-8') for key, value in cart_items.items()}
    return decoded_cart_items


def get_cart_items_dict(cart_items):
    items = []
    for item_key, price in cart_items.items():
        item_name, count = item_key.split(":")
        items.append({'name': item_name, 'count': count})
    return items


def get_cart_items_text(cart_items):
    logging.info(cart_items.items(), "###########################")
    cart_items_text = ""
    total_price = 0
    for item_key, price in cart_items.items():
        item_name, count = item_key.split(":")
        item_price = int(price)
        item_total_price = item_price * int(count)
        total_price += item_total_price
        cart_items_text += f"{count} ✖️ {item_name} {item_price} so'm\n"

    return cart_items_text, total_price
