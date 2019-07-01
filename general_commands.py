from globals import *

@client.command()
async def ping(ctx) :
    await ctx.send(content="Pong! Current ping: {} ms!".format(math.floor(client.latency * 10000)/10))

@client.command()
async def help_run(ctx) :
    await ctx.send(content="If you would like to customize my code and run it yourself, please go to my github page!\nInstructions on how to run it can be found in the readme file.\nGithub: {}".format(GITHUB))

@client.command()
async def github(ctx) :
    await ctx.send(content="Here's my Github link: {} <:TsuComfyBot:541315853149536257>".format(GITHUB))

@client.command()
async def invite(ctx) :
    await ctx.send(content="Check your DM's! <:TsuSmileBot:541997306413580288>")
    await ctx.message.author.send(content="Here you go: https://discordapp.com/api/oauth2/authorize?client_id=515859822441136130&permissions=8&scope=bot\nFor more info, either use ta!help or refer to the readme file on Github! <:TsuComfyBot:541315853149536257>")

@client.command()
async def discord(ctx) :
    await ctx.send(content="Check your DM's! <:TsuSmileBot:541997306413580288>")
    await ctx.message.author.send(content="Here's my Discord invite link: https://discord.gg/He9ZcwR <:TsuComfyBot:541315853149536257>")
