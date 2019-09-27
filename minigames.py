from globals import *
from utils import *

@client.command(aliases=["coin", "coinflip"])
async def coin_flip(ctx) :
    msg = await ctx.send(content="Flipping coin...")
    await asyncio.sleep(1)
    result = "heads"
    if random.randint(0,1) > 0 :
        result = "tails"
    await msg.edit(content="It's {}!".format(result))
