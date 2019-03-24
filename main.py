import discord
import asyncio
import json
import random
import datetime
import os
import aiohttp
import urllib #not actually for doing link stuff, because it's blocking

#custom imports
from globals import *
from utils import *
import admin
import minesweeper
import interpreters
import jokes
import nsfw

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("Guild count: {}!".format(len(client.guilds)))
    print('------')
    await update_presence_guild()
    import_all_configs()

@client.event
async def on_guild_join(guild) :
    await update_presence_guild()

@client.event
async def on_member_join(member) :
    joinchannel = str(configs[member.guild.id]["JoinChannel"]).strip()
    joinmessages = configs[member.guild.id]["JoinMessages"]
    #print(member.guild)
    #print(member.guild.get_channel(joinchannel))
    #if id in configs[member.guild.id]["Profiles"] :
        #configs[member.guild.id]["Profiles"][member.id]
    #else :
    if not (id in configs[member.guild.id]["Profiles"]) :
        configs[member.guild.id]["Profiles"][member.id] = {
            "DailyReward": None,
            "IsBlacklisted": False,
            #"LastMessage": "2018-07-03T23:25:37.5596571",
            "Warnings": 0,
            "Credits": 0,
            "Commands": {},
            "DailyStreak": 0,
            "ChatXP": 0
        }

    await member.guild.get_channel(int(joinchannel)).send_message(random.choice(joinmessages).format(user=member.mention, guild=member.guild))

"""
@client.event
async def on_message(message):
    if message.content == message.guild.me.mention :
        await message.channel.send(content="Hello! Do you need help with anything? Feel free to use ta!help at any point if you need my help <:TsuComfyBot:541315853149536257>")

    if message.content.startswith("ta!lmgtfy") :
        args = message.content.split("ta!lmgtfy")[1].lstrip().rstrip().split(" ")
        result = generate_error("101")
        if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
            result = "<http://lmgtfy.com/?q="
            for arg in args :
                result += urllib.parse.quote(arg, safe="") + "+"
            result = result[:-1] + ">"
        await message.channel.send(content=result)
    elif message.content.startswith("ta!stats") :
        embed=discord.Embed()
        #embed.set_author(name="Server Stats")
        #embed.add_field(name="Ping", value="{ping}", inline=True)
        #embed.add_field(name="Guild Count", value="{guild_count}"", inline=True)
        #embed.add_field(name="help", value="nope", inline=False)
        await message.channel.send(embed=embed)

    elif message.content == "ta!neato" :
        await jokes.neato(message)
    elif message.content == "ta!epic" :
        await jokes.epic(message)
    elif message.content == "ta!imlonely" :
        await jokes.imlonely(message)

    elif message.content.startswith("ta!help categories") or message.content.startswith("ta!help category") :
        await help.categories(message)
    elif message.content.startswith("ta!help admin") :
        await help.admin(message)
    elif message.content.startswith("ta!help") or message.content.startswith("ta!help core") :
        await help.core(message)

    elif message.content.startswith("ta!github") :
        await message.channel.send(content="If you are interested in my code, you can always find a semi up-to-date version of the code on Github!\nhttps://github.com/Lucky4Luuk/Tsuyu-Asui Have fun <:TsuSmileBot:541997306413580288>")
    elif message.content.startswith("ta!invite") :
        await message.channel.send(content="I have sent you the invite link in PM <a:TsuDanceBot:542450965463433226>")
        await client.send_message(message.author, "Here you go <:TsuSmileBot:541997306413580288>\nhttps://discordapp.com/api/oauth2/authorize?client_id=515859822441136130&permissions=8&scope=bot\nFeel free to join the Discord guild (ta!discord) for support and update notifications!")
    elif message.content.startswith("ta!discord") :
        await message.channel.send(content="I have sent you the invite link in PM <a:TsuDanceBot:542450965463433226>")
        await client.send_message(message.author, "Here you go <:TsuSmilebot:541997306413580288>\nhttps://discord.gg/He9ZcwR")

    elif message.content.startswith("ta!admin") :
        await admin.admin(message)
    #elif message.content.startswith("ta!warn") :
    #    await admin.warn(message)
    elif message.content.startswith("ta!kick") :
        await admin.kick(message)
    elif message.content.startswith("ta!ban") :
        await admin.ban(message)
    elif message.content.startswith("ta!set_reason") :
        await admin.set_reason(message)
    elif message.content.startswith("ta!set_kick_message") :
        await admin.set_kick_message(message)
    elif message.content.startswith("ta!set_ban_message") :
        await admin.set_ban_message(message)
    elif message.content.startswith("ta!set_warning_channel") :
        await admin.set_warning_channel(message)
    elif message.content.startswith("ta!set_welcome_channel") :
        await admin.set_welcome_channel(message)
    elif message.content.startswith("ta!set_max_warns") :
        await admin.set_max_warns(message)
    elif message.content.startswith("ta!reset_warns") :
        await admin.reset_warns(message)
    elif message.content.startswith("ta!get_warns") :
        await admin.get_warns(message)
    elif message.content.startswith("ta!purge") :
        await admin.purge(message)
    elif message.content.startswith("ta!save_config") :
        await admin.save_config(message)
    elif message.content.startswith("ta!reload_config") :
        await admin.reload_config(message)
    elif message.content.startswith("ta!export_config") :
        await admin.export_config(message)

    elif message.content.startswith("ta!brainfuck") :
        await interpreters.brainfuck(message)

    elif message.content.startswith("ta!nsfw") :
        await nsfw.nsfw(message)

    elif message.author.id == LUUK_ID :
        if message.content.startswith("ta!reload_error_codes") :
            f = open("error_codes.json")
            ERROR_CODES = json.load(f)
            f.close()
            await message.channel.send(content="No problem <:TsuAdorableBot:541315335169507345>")
        #elif message.content.startswith("ta!reload_help") :
        #    f = open("help.json")
        #    HELP_DATA = json.load(f)
        #    f.close()
        #    await message.channel.send(content="No problem <:TsuAdorableBot:541315335169507345>")
        elif message.content.startswith("ta!reload_config_file_current") :
            if message.guild :
                import_config(message.guild.id)
            else :
                await message.channel.send(content=generate_error("201"))
        elif message.content.startswith("ta!save_configs") :
            save_all_configs()
            await message.channel.send(content="No problem <:TsuAdorableBot:541315335169507345>")
        elif message.content.startswith("ta!eval") :
            code = message.content[8:].replace("`","")
            if code != "" :
                result = eval(code)
                await message.channel.send(content="```OUTPUT:\n{}```".format(result))
            else :
                await message.channel.send(content=generate_error("501"))
        elif message.content.startswith("ta!exec") :
            code = message.content[8:].replace("`","")
            if code != "" :
                result = exec(code)
                await message.channel.send(content="```OUTPUT:\n[No code output]```")
            else :
                await message.channel.send(content=generate_error("501"))
        elif message.content == "ta!shutdown" :
            await message.channel.send(content="Are you sure? (y/n)")
            def check(msg) :
                return msg.author.id == LUUK_ID
            response = await client.wait_for("message", timeout=30, check=check)
            if response.content == "y" :
                await message.channel.send(content="Okay!")
                await message.channel.send(content="Saving all configs...")
                save_all_configs()
                await message.channel.send(content="All configs saved!")
                await message.channel.send(content="Logging out... bye!")
                await client.logout()
                exit()
            else :
                await message.channel.send(content="Staying online.")

        elif message.content.startswith("ta!") :
            await message.channel.send(content=generate_error("301"))

    elif message.content.startswith("ta!") :
        await message.channel.send(content=generate_error("301"))
"""

client.run(TOKEN)
