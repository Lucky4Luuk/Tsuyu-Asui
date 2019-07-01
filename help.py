from globals import *
from utils import *
import discord

@client.group()
async def help(ctx) :
    if ctx.invoked_subcommand is None :
        embed = discord.Embed(color=HELP_COLOR)
        embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
        for line in HELP_DATA["core_lines"] :
            embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
        embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
        await ctx.send(embed=embed)

@help.command(name="categories")
async def _categories(ctx) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["category_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await ctx.send(embed=embed)

@help.command(name="admin")
async def _admin(ctx) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["admin_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await ctx.send(embed=embed)

@help.command(name="jokes")
async def _jokes(ctx) :
    embed = discord.Embed(color=HELP_COLOR)
    embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
    for line in HELP_DATA["joke_lines"] :
        embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
    embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
    await ctx.send(embed=embed)
