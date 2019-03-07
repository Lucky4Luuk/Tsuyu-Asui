from globals import *
from utils import *
import discord

async def categories(message) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["category_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await message.channel.send(embed=embed)

async def admin(message) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["admin_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await message.channel.send(embed=embed)

async def core(message) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["core_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await message.channel.send(embed=embed)
