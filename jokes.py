from globals import *
from utils import *

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

#Will finish these 2 commands at some point, however first I'd like to finally add a custom help command
#UPDATE: help command seems to be working, next commit hopefully has these 2 working.
@client.command()
async def pat(ctx) :
    await ctx.send(content="WIP")

@client.command()
async def hug(ctx) :
    await ctx.send(content="WIP")
