from globals import *
from utils import *
import aiohttp

@client.command
async def nsfw(ctx) :
    message = ctx.message
    if message.channel.is_nsfw :
        search = message.content[8:]
        if search != "" and search in NEKOS_NSFW_ENDPOINTS :
            url = NEKOS_LIFE.format(search)
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    res = await r.json()
                    await ctx.send(content=res["url"])
