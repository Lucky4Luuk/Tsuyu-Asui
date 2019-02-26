import discord
import asyncio
import json
import random
import datetime
import os
import aiohttp

#custom imports
import minesweeper
import interpreters

if not os.path.isfile("token.txt"):
    print("token.txt was not found, create it and put your token in there")
    exit()

f = open("token.txt")
TOKEN = f.read().strip()
f.close()
if TOKEN == "":
    print("token.txt was empty, please put your token in there")
    exit()

f = open("error_codes.json")
ERROR_CODES = json.load(f)
f.close()
f = open("help.json")
HELP_DATA = json.load(f)
f.close()

LUUK_ID = 183315569745985545

#colors
FROG_GREEN = 0x00b700
HONEY_ORANGE = 0xfa6912
BEE_YELLOW = 0xfadd16
FIRE_RED = 0xff0000
SKY_BLUE = 0xb9e3e6

WARN_COLOR = SKY_BLUE
BAN_COLOR = FIRE_RED
HELP_COLOR = FROG_GREEN

NEKOS_LIFE = "https://nekos.life/api/v2/img/{}"
f = open("nekos_nsfw_endpoints.json")
NEKOS_NSFW_ENDPOINTS = json.load(f)
f.close()

configs = {}

client = discord.Client()

def generate_error(code) :
    return "ERROR {}: {} <a:TsuTearsBot:541326614143959050>".format(code, ERROR_CODES[code])

def import_config(guild, retry=True) :
    print("====Loading Config====\nguild Name: {}\nID: {}\n\n".format(guild.name, guild.id))
    try :
        f = open("{}-config.json".format(guild.id), encoding="latin-1")
        configs[guild.id] = json.load(f)
        f.close()
    except Exception as e :
        print(e)
        #create a new config file
        f = open("empty_config.json", encoding="latin-1")
        data = f.read()
        f.close()
        f = open("{}-config.json".format(guild.id), "a+", encoding="latin-1")
        f.write(data)
        f.close()
        if retry :
            import_config(guild, retry=False)

def import_all_configs() :
    for guild in client.guilds :
        import_config(guild)

def save_config(guild) :
    print("====Saving Config====\nguild Name: {}\nID: {}\n\n".format(guild.name, guild.id))
    try :
        f = open("{}-config.json".format(guild.id), "w+", encoding="latin-1")
        f.seek(0)
        f.truncate()
        f.write(json.dumps(configs[guild.id], indent="  "))
        f.close()
    except Exception as e :
        print(e)

def save_all_configs() :
    for guild in client.guilds :
        save_config(guild)

def get_config_embed() :
    embed=discord.Embed(title="Config", description="", color=FROG_GREEN)
    #embed.set_footer(text="Page {}".format(page_number))
    return embed

def warn_user(guild, modid, id, reason) :
    #print("yeet")
    if reason.strip() == "" :
        reason = "Please set a reason using ta!set_reason <case_number> <reason> <:TsuSmileBot:541997306413580288>"
    case_number = len(configs[guild.id]["Mod"]["Cases"])+1
    case = {
        "ModId":int(modid),
        "UserId":int(id),
        "Reason":reason,
        "CaseNumber":case_number,
        "MessageId":0,
        "CaseType":6
    }
    if id in configs[guild.id]["Profiles"] :
        configs[guild.id]["Profiles"][id]["Warnings"] += 1
    else :
        configs[guild.id]["Profiles"][id] = {
            "DailyReward": None,
            "IsBlacklisted": False,
            #"LastMessage": "2018-07-03T23:25:37.5596571",
            "Warnings": 1,
            "Credits": 0,
            "Commands": {},
            "DailyStreak": 0,
            "ChatXP": 0
        }
    member = guild.get_member(id)
    moderator = guild.get_member(modid)
    configs[guild.id]["Mod"]["Cases"].append(case)
    timestamp = datetime.datetime.now()
    embed = discord.Embed(color=WARN_COLOR)
    embed.set_author(name="Case #{case_number} | Warning | {name}#{tag}".format(case_number=case_number, name=member.name, tag=member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text="ID: {} • {} • Warning #{}".format(id, timestamp.strftime("%c"), configs[guild.id]["Profiles"][id]["Warnings"]))
    got_kicked = False
    if configs[guild.id]["Profiles"][id]["Warnings"] > configs[guild.id]["Mod"]["MaxWarnings"] :
        #print("this guy should be kicked")
        embed, tmp = kick_user(guild, modid, id, reason, from_warn=True)
        got_kicked = True
    #save_config(guild)
    return embed, case_number, got_kicked

def kick_user(guild, modid, id, reason, from_warn=False) :
    #print("yeet")
    if reason.strip() == "" :
        reason = "Please set a reason using ta!set_reason <case_number> <reason> <:TsuSmileBot:541997306413580288>"
    case_number = len(configs[guild.id]["Mod"]["Cases"])+1
    case = {
        "ModId":int(modid),
        "UserId":int(id),
        "Reason":reason,
        "CaseNumber":case_number,
        "MessageId":0,
        "CaseType":2
    }
    configs[guild.id]["Profiles"][id]["Warnings"] += 1
    member = guild.get_member(id)
    moderator = guild.get_member(modid)
    if from_warn == False :
        configs[guild.id]["Mod"]["Cases"].append(case)
        case_number -= 1
    timestamp = datetime.datetime.now()
    embed = discord.Embed(color=WARN_COLOR)
    embed.set_author(name="Case #{case_number} | Kick | {name}#{tag}".format(case_number=case_number, name=member.name, tag=member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text="ID: {} • {} • Warning #{}".format(id, timestamp.strftime("%c"), configs[guild.id]["Profiles"][id]["Warnings"]))
    #save_config(guild)
    return embed, case_number

def ban_user(guild, modid, id, reason) :
    #print("yeet")
    if reason.strip() == "" :
        reason = "Please set a reason using ta!set_reason <case_number> <reason> <:TsuSmileBot:541997306413580288>"
    case_number = len(configs[guild.id]["Mod"]["Cases"])+1
    case = {
        "ModId":int(modid),
        "UserId":int(id),
        "Reason":reason,
        "CaseNumber":case_number,
        "MessageId":0,
        "CaseType":1
    }
    member = guild.get_member(id)
    moderator = guild.get_member(modid)
    configs[guild.id]["Mod"]["Cases"].append(case)
    timestamp = datetime.datetime.now()
    embed = discord.Embed(color=BAN_COLOR)
    embed.set_author(name="Case #{case_number} | Ban | {name}#{tag}".format(case_number=case_number, name=member.name, tag=member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text="ID: {} • {} • Warning #{}".format(id, timestamp.strftime("%c"), configs[guild.id]["Profiles"][id]["Warnings"]))
    #save_config(guild)
    return embed, case_number

def set_reason(guild, warn_channel, case_number, msgid, msg, reason) :
    old_embed = msg.embeds[0] #always the first embed, because that's how the commands work
    if reason.strip() == "" :
        reason = old_embed["fields"][2]["value"]
    case = configs[guild.id]["Mod"]["Cases"][case_number-1]
    id = case["UserId"]
    modid = case["ModId"]

    member = guild.get_member(id)
    moderator = guild.get_member(modid)
    configs[guild.id]["Mod"]["Cases"].append(case)
    timestamp = datetime.datetime.now()
    col = WARN_COLOR
    if case["CaseType"] == 1 :
        col = BAN_COLOR
    embed = discord.Embed(color=col)
    embed.set_author(name=old_embed["author"]["name"], icon_url=old_embed["author"]["icon_url"])
    embed.add_field(name="User", value=old_embed["fields"][0]["value"], inline=True)
    embed.add_field(name="Moderator", value=old_embed["fields"][1]["value"], inline=True)
    embed.add_field(name="Reason", value=reason + " (edited)", inline=False)
    embed.set_footer(text="ID: {} • {}".format(id, timestamp.strftime("%c")))
    return embed

def is_moderator(member) :
    return member.guild_permissions.administrator or member.guild_permissions.kick_members or member.guild_permissions.ban_members

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
        if message.author.guild_permissions :
            if message.author.guild_permissions.administrator :
                if message.content == "ta!admin" :
                    #msg = await message.channel.send(content=embed=get_config_embed())
                    #res = await client.wait_for_reaction(["⬅", "➡"])
                    await message.channel.send(embed=get_config_embed()) #TODO: fix pls
                elif message.content.startswith("ta!admin set_join_message") : #25 chars
                    msg = message.content[26:]
                    await message.channel.send(content="Your join message is now: '{}'".format(msg.format(user=message.author.mention, guild=message.guild)))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))

    elif message.content.startswith("ta!warn") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                #do a warn
                args = message.content[8:].split(" ")
                id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                member = message.guild.get_member(id)
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(str(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number, got_kicked = warn_user(message.guild, message.author.id, id, reason)
                    if got_kicked :
                        await message.channel.send(content="*User {} has been kicked...*".format(member.name))
                        await client.kick(member)
                    else :
                        await message.channel.send(content="*User {} has been warned...*".format(member.name))
                    msg = await warn_channel.send(embed=embed)
                    configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.guild)
                else :
                    await message.channel.send(content=generate_error("305"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!kick") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                #do a kick
                args = message.content[8:].split(" ")
                id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                member = message.guild.get_member(id)
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(str(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number = kick_user(message.guild, message.author.id, id, reason)
                    await message.channel.send(content="*User {} has been kicked...*".format(member.name))
                    await member.send(content=configs[message.guild.id]["KickMessage"].format(guild=guild.name, user=member.name))
                    msg = await warn_channel.send(embed=embed)
                    await member.kick()
                    configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.guild)
                else :
                    await message.channel.send(content=generate_error("305"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!ban") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                #do a ban
                args = message.content[7:].split(" ")
                id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                member = message.guild.get_member(id)
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(str(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number = ban_user(message.guild, message.author.id, id, reason)
                    await message.channel.send(content="*User {} has been banned...*".format(member.name))
                    await member.send_message(content=configs[message.guild.id]["BanMessage"].format(guild=message.guild.name, user=member.name))
                    msg = await warn_channel.send(embed=embed)
                    await member.ban()
                    configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.guild)
                else :
                    await message.channel.send(content=generate_error("305"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
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
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                reason = message.content[20:]
                configs[message.guild.id]["KickMessage"] = reason
                await message.channel.send(content="Your new kick message is now '{}'".format(reason.format(user=message.author, guild=message.guild.name)))
                save_config(message.guild)
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!set_ban_message") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                reason = message.content[19:]
                configs[message.guild.id]["BanMessage"] = reason
                await message.channel.send(content="Your new ban message is now '{}'".format(reason.format(user=message.author, guild=message.guild.name)))
                save_config(message.guild)
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!set_warning_channel") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                #do a edit
                channel_id = str(message.content[23:].replace("<","").replace("#","").replace(">",""))
                guild = message.guild
                configs[guild.id]["Mod"]["TextChannel"] = channel_id
                await message.channel.send(content="The warning channel has been set!\nChannel: {} - ID: {}".format(guild.get_channel(channel_id).mention, channel_id))
                save_config(guild)
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!set_welcome_channel") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                #do a edit
                channel_id = str(message.content[23:].replace("<","").replace("#","").replace(">",""))
                guild = message.guild
                configs[guild.id]["JoinChannel"] = channel_id
                await message.channel.send(content="The welcome channel has been set!\nChannel: {} - ID: {}".format(guild.get_channel(channel_id).mention, channel_id))
                save_config(guild)
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!set_max_warns") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                num = message.content[17:].strip()
                try :
                    num = int(num)
                    configs[message.guild.id]["Mod"]["MaxWarnings"] = num
                    await message.channel.send(content="The maximum amount of warnings before a kick occurs is now '{}'".format(num))
                    save_config(message.guild)
                except Exception as e :
                    await message.channel.send(content=generate_error("306"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!reset_warns") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                id = message.content[15:].strip().replace("<", "").replace(">", "").replace("!", "").replace("@", "")
                if id != "" and id in configs[message.guild.id]["Profiles"] :
                    member = message.guild.get_member(id)
                    configs[message.guild.id]["Profiles"][str(id)]["Warnings"] = 0
                    await message.channel.send(content="{}'s warnings have been reset!".format(member.mention))
                    save_config(message.guild)
                else :
                    await message.channel.send(content=generate_error("307"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!get_warns") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                id = message.content[13:].strip().replace("<", "").replace(">", "").replace("!", "").replace("@", "")
                if id != "" and id in configs[message.guild.id]["Profiles"] :
                    member = message.guild.get_member(id)
                    warnings = int(configs[message.guild.id]["Profiles"][str(id)]["Warnings"]) #probably not needed to cast to int, but im tired so i cannot think straight lol
                    if warnings == 0 :
                        await message.channel.send(content="{} has {} warnings! <a:TsuDanceBot:542450965463433226>".format(member.mention, warnings))
                    elif warnings == 1 :
                        await message.channel.send(content="{} has {} warning!".format(member.mention, warnings))
                    else :
                        await message.channel.send(content="{} has {} warnings!".format(member.mention, warnings))
                    #save_config(message.guild)
                else :
                    await message.channel.send(content="Either the ID is incorrect, or this person has never joined this guild. You can assume they have 0 warnings <:TsuSmileBot:541997306413580288>")
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!purge") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                num = message.content[9:].strip()
                if num != "" and num.isdigit() :
                    #purge
                    num = int(num)
                    await message.channel.purge(limit=num+1)
                    await message.channel.send(content="*Purged {} messages...*".format(num))
                else :
                    await message.channel.send(content=generate_error("306"))
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!save_config") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                save_config(message.guild)
                await message.channel.send(content="Your config file has been saved!")
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!reload_config") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                import_config(message.guild)
                await message.channel.send(content="Your config file has been reloaded!")
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
    elif message.content.startswith("ta!export_config") :
        if message.author.guild_permissions :
            if is_moderator(message.author) :
                import_config(message.guild)
                await client.send_file(message.channel, "{}-config.json".format(message.guild.id), content="Your config file has been reloaded!")
            else :
                await message.channel.send(content=generate_error("302"))
        else :
            await message.channel.send(content=generate_error("303"))
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
