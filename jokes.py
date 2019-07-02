from globals import *
from utils import *
import aiohttp

@client.command()
async def imlonely(ctx) :
    await ctx.send(content="Hi lonely I'm dad")

@client.command()
async def neato(ctx) :
    await ctx.send(content="""||```
███╗   ██╗███████╗ █████╗ ████████╗ ██████╗
████╗  ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗
██╔██╗ ██║█████╗  ███████║   ██║   ██║   ██║
██║╚██╗██║██╔══╝  ██╔══██║   ██║   ██║   ██║
██║ ╚████║███████╗██║  ██║   ██║   ╚██████╔╝
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ```||""")

@client.command()
async def epic(ctx) :
    await ctx.send(content="""||```
███████╗██████╗ ██╗ ██████╗
██╔════╝██╔══██╗██║██╔════╝
█████╗  ██████╔╝██║██║
██╔══╝  ██╔═══╝ ██║██║
███████╗██║     ██║╚██████╗
╚══════╝╚═╝     ╚═╝ ╚═════╝```||""")

@client.command()
async def vsauce(ctx) :
    #f = open("assets/tsuyu_michael_please.png")
    await ctx.send(file=discord.File("assets/tsuyu_michael_please.png"))
    #f.close()

@client.command()
async def clap(ctx) :
    await ctx.send(content="👏 " + ctx.message.content[8:].replace(" ", " 👏 ") + " 👏")

@client.command()
async def expand(ctx) :
    result = ""
    for char in ctx.message.content[10:] :
        result += char + " "
    await ctx.send(content=result)

@client.command()
async def pat(ctx, user: discord.Member = None) :
    mention = "themself :O"
    if user :
        mention = user.mention
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://nekos.life/api/v2/img/pat") as r:
            res = await r.json()

            e = discord.Embed(description="**{}** patted **{}**".format(ctx.author.mention, mention), colour=SKY_BLUE)
            e.set_image(url=res["url"])
            await ctx.send(embed=e)

@client.command()
async def hug(ctx, user: discord.Member = None) :
    mention = "themself :O"
    if user :
        mention = user.mention
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://nekos.life/api/v2/img/hug") as r:
            res = await r.json()

            e = discord.Embed(description="**{}** hugged **{}**".format(ctx.author.mention, mention), colour=SKY_BLUE)
            e.set_image(url=res["url"])
            await ctx.send(embed=e)

@client.command()
async def slap(ctx, user: discord.Member = None) :
    mention = "themself :O"
    if user :
        mention = user.mention
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://nekos.life/api/v2/img/slap") as r:
            res = await r.json()

            e = discord.Embed(description="**{}** slapped **{}**".format(ctx.author.mention, mention), colour=SKY_BLUE)
            e.set_image(url=res["url"])
            await ctx.send(embed=e)

@client.command()
async def tickle(ctx, user: discord.Member = None) :
    mention = "themself :O"
    if user :
        mention = user.mention
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://nekos.life/api/v2/img/tickle") as r:
            res = await r.json()

            e = discord.Embed(description="**{}** tickled **{}**".format(ctx.author.mention, mention), colour=SKY_BLUE)
            e.set_image(url=res["url"])
            await ctx.send(embed=e)

@client.command()
async def kiss(ctx, user: discord.Member = None) :
    mention = "themself :O"
    if user :
        mention = user.mention
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://nekos.life/api/v2/img/kiss") as r:
            res = await r.json()

            e = discord.Embed(description="**{}** kissed **{}**".format(ctx.author.mention, mention), colour=SKY_BLUE)
            e.set_image(url=res["url"])
            await ctx.send(embed=e)

@client.command()
async def poke(ctx, user: discord.Member = None) :
    mention = "themself :O"
    if user :
        mention = user.mention
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://nekos.life/api/v2/img/poke") as r:
            res = await r.json()

            e = discord.Embed(description="**{}** poked **{}**".format(ctx.author.mention, mention), colour=SKY_BLUE)
            e.set_image(url=res["url"])
            await ctx.send(embed=e)
