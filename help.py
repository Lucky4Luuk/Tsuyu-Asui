from globals import *
from utils import *
import discord

@client.command(name="help categories")
async def categories(ctx) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["category_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await ctx.send(embed=embed)

@client.command(name="help admin")
async def admin(ctx) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["admin_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await ctx.send(embed=embed)

@client.command(name="help")
async def core(ctx) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["core_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await ctx.send(embed=embed)
