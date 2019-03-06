import discord
import asyncio
import json
import random
import datetime
import os
import aiohttp

#custom imports
from globals import *
from utils import *
import admin
import minesweeper
import interpreters

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    game = discord.Game(name="Currently in {} guilds!".format(len(client.guilds)))
    await client.change_presence(activity=game)
    import_all_configs()

@client.event
async def on_guild_join(guild) :
    game = discord.Game(name="Currently in {} guilds!".format(len(client.guilds)))
    await client.change_presence(activity=game)

@client.event
async def on_member_join(member):
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

    await client.send_message(member.guild.get_channel(joinchannel), random.choice(joinmessages).format(user=member.mention, guild=member.guild))

@client.event
async def on_message(message):
    if message.guild == None : #PM
        f = open("DM_LOGS.txt", "r+")
        f.write("{}: {}\n".format(message.author.name, message.content))
        f.close()

    elif message.content == message.guild.me.mention :
        await message.channel.send(content="Hello! Do you need help with anything? Feel free to use ta!help at any point if you need my help <:TsuComfyBot:541315853149536257>")

    if message.content.startswith("ta!lmgtfy") :
        args = message.content.split("ta!lmgtfy")[1].lstrip().rstrip().split(" ")
        result = generate_error("101")
        if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
            result = "<http://lmgtfy.com/?q="
            for arg in args :
                result += arg + "+"
            result = result[:-1] + ">"
        await message.channel.send(content=result)
    elif message.content == "ta!neato" :
        await message.channel.send(content="""||```
███╗   ██╗███████╗ █████╗ ████████╗ ██████╗
████╗  ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗
██╔██╗ ██║█████╗  ███████║   ██║   ██║   ██║
██║╚██╗██║██╔══╝  ██╔══██║   ██║   ██║   ██║
██║ ╚████║███████╗██║  ██║   ██║   ╚██████╔╝
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ```||""")
    elif message.content == "ta!epic" :
        await message.channel.send(content="""||```
███████╗██████╗ ██╗ ██████╗
██╔════╝██╔══██╗██║██╔════╝
█████╗  ██████╔╝██║██║
██╔══╝  ██╔═══╝ ██║██║
███████╗██║     ██║╚██████╗
╚══════╝╚═╝     ╚═╝ ╚═════╝```||""")
    elif message.content.startswith("ta!help categories") or message.content.startswith("ta!help category") :
        embed = discord.Embed(color=HELP_COLOR)
        embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
        for line in HELP_DATA["category_lines"] :
            embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
        embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
        await message.channel.send(embed=embed)
    elif message.content.startswith("ta!help admin") :
        embed = discord.Embed(color=HELP_COLOR)
        embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
        for line in HELP_DATA["admin_lines"] :
            embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
        embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
        await message.channel.send(embed=embed)
    elif message.content.startswith("ta!help") or message.content.startswith("ta!help core") :
        embed = discord.Embed(color=HELP_COLOR)
        embed.set_author(name=HELP_DATA["title"], icon_url=HELP_DATA["icon_url"])
        for line in HELP_DATA["core_lines"] :
            embed.add_field(name=line["name"], value=line["value"], inline=line["inline"])
        embed.set_footer(text=" • {}".format(datetime.datetime.now().strftime("%c")))
        await message.channel.send(embed=embed)

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

    elif message.content.startswith("ta!warn") :
        await admin.warn(message)
    elif message.content.startswith("ta!kick") :
        await admin.kick(message)
    elif message.content.startswith("ta!ban") :
        await admin.ban(message)
    elif message.content.startswith("ta!set_reason") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                #do a edit
                args = message.content[14:].split(" ")
                if len(args) > 0 :
                    #id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                    case_number = int(args[0].strip())
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    guild = message.guild
                    warn_channel = guild.get_channel(str(configs[guild.id]["Mod"]["TextChannel"]))
                    msgid = configs[guild.id]["Mod"]["Cases"][case_number-1]["MessageId"]
                    msg = await client.get_message(warn_channel, str(msgid))
                    embed = set_reason(guild, warn_channel, case_number, msgid, msg , reason)
                    await client.edit_message(msg, embed=embed)
                    save_config(guild)
                else :
                    await message.channel.send(content=generate_error("304"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!set_kick_message") :
        await set_kick_message(message)
    elif message.content.startswith("ta!set_ban_message") :
        await set_ban_message(message)
    elif message.content.startswith("ta!set_warning_channel") :
        await set_warning_channel(message)
    elif message.content.startswith("ta!set_welcome_channel") :
        await set_welcome_channel(message)
    elif message.content.startswith("ta!set_max_warns") :
        await set_max_warns(message)
    elif message.content.startswith("ta!reset_warns") :
        await reset_warns(message)
    elif message.content.startswith("ta!get_warns") :
        await get_warns(message)
    elif message.content.startswith("ta!purge") :
        await purge(message)
    elif message.content.startswith("ta!save_config") :
        await save_config(message)
    elif message.content.startswith("ta!reload_config") :
        await reload_config(message)
    elif message.content.startswith("ta!export_config") :
        await export_config(message)
    elif message.content.startswith("ta!brainfuck") :
        code = message.content[13:].replace("`", "").strip()
        if code != "" :
            result = interpreters.brainfuck_evaluate(code)
            await message.channel.send(content="```OUTPUT:\n{}```".format(result))
        else :
            await message.channel.send(content=generate_error("501"))
    elif message.content == "ta!imlonely" :
        await message.channel.send(content="Hi lonely I'm dad")
    #elif message.content.startswith("ta!minesweeper") :
    #    args = message.content[15:].split(" ")
    #    if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
    #        if "x" in args[0] :
    #            size = args[0].split("x")
    #            successful = False
    #            try :
    #                size_x = int(size[0])
    #                size_y = int(size[1])
    #                num_of_mines = int(args[1])
    #                successful = True
    #            except :
    #                await message.channel.send(content=generate_error("104"))
    #            if successful :
    #                lines = minesweeper.create_board(size_x, size_y, num_of_mines)
    #                for line in lines :
    #                    await message.channel.send(content=line)
    #        else :
    #            await message.channel.send(content=generate_error("102"))
    #    else :
    #        await message.channel.send(content=generate_error("103"))

    elif message.content.startswith("ta!nsfw") :
        if message.channel.is_nsfw :
            search = message.content[8:]
            if search != "" and search in NEKOS_NSFW_ENDPOINTS :
                url = NEKOS_LIFE.format(search)
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url) as r:
                        res = await r.json()
                        await message.channel.send(content=res["url"])

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
            response = await client.wait_for_message(timeout=30, author=message.author)
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

client.run(TOKEN)
