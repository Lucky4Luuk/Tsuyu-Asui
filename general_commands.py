from globals import *
from utils import *

@client.command()
async def ping(ctx) :
    await ctx.send(content="Pong! Current ping: {} ms!".format(math.floor(client.latency * 10000)/10))

@client.command()
async def status(ctx) :
    async with ctx.typing() :
        ping = math.floor(client.latency * 10000) / 10
        guilds = len(client.guilds)
        e = discord.Embed(description="[Status Report]", colour=FROG_GREEN)
        e.add_field(name="** **", value="**PING:**   {}ms".format(ping), inline=True)
        e.add_field(name="** **", value="**GUILDS:** {}".format(guilds), inline=True)
        await ctx.send(embed=e)

#TODO: alias wtf lol
@client.command(alias="server")
async def server_status(ctx) :
    owner = ctx.guild.owner
    features = ctx.guild.features
    e = discord.Embed(colour=FROG_GREEN)
    e.set_author(name="[**{0}** - *by {1}*]".format(ctx.guild.name, owner.name), icon_url=ctx.guild.icon_url)
    e.add_field(name="** **", value="**Members:** {}".format(len(ctx.guild.members)), inline=True)
    e.add_field(name="** **", value="**Boost Level:** {}/3".format(ctx.guild.premium_tier), inline=True)
    e.add_field(name="** **", value="**Created at:** {}".format(ctx.guild.created_at.strftime("%b {}, %Y").format(int_to_ordinal(int(ctx.guild.created_at.strftime("%d"))))), inline=False)
    e.add_field(name="** **", value="**MFA Level:** {}".format(ctx.guild.mfa_level), inline=True)
    e.add_field(name="** **", value="**Partnered:** {}".format( ("✅" if "PARTNERED" in features else "❌") ), inline=True)
    e.set_footer(text="Kindly provided by Tsuyu Asui")
    await ctx.send(embed=e)

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

@client.command(name="discord")
async def _discord(ctx) :
    await ctx.send(content="Check your DM's! <:TsuSmileBot:541997306413580288>")
    await ctx.message.author.send(content="Here's my Discord invite link: https://discord.gg/He9ZcwR <:TsuComfyBot:541315853149536257>")
