from globals import *
from utils import *
import aiohttp

async def nsfw(message) :
    if message.channel.is_nsfw :
        search = message.content[8:]
        if search != "" and search in NEKOS_NSFW_ENDPOINTS :
            url = NEKOS_LIFE.format(search)
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    res = await r.json()
                    await message.channel.send(content=res["url"])
