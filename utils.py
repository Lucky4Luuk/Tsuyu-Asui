from globals import *
import datetime
import discord

def has_big_codeblock(message) :
    block = re.search("```((.|\n)+)```", message.content)
    if block and (len(block.group()) > 540 or len(block.group().split("\n")) > 12) :
        return True
    return False

def check_word_blacklist(message) :
    if not "WordBlacklist" in configs[message.guild.id].keys() :
        return False
    if "ta!set_word_blacklist" in message.content :
        return False
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            return False
    blacklist = configs[message.guild.id]["WordBlacklist"]
    for word in blacklist :
        if word.lower() in message.content.lower() :
            return True
    return False

async def update_presence_guild() :
    text = "Currently in {} guilds!".format(len(client.guilds))
    if len(client.guilds) == 1 :
        text = "Currently in 1 guild!" #otherwise it says '1 guilds' and i dont like that >:(
    game = discord.Game(name=text)
    await client.change_presence(activity=game)

def generate_error(code) :
    return "ERROR {}: {} <a:TsuTearsBot:541326614143959050>".format(code, ERROR_CODES[code])

def new_config(guild) :
    print("====Creating Config====\nGuild Name: {}\nID: {}\n\n".format(guild.name, guild.id))
    f = open("empty_config.json", encoding="latin-1")
    data = f.read()
    f.close()
    f = open("{}-config.json".format(guild.id), "a+", encoding="latin-1")
    f.write(data)
    f.close()

def import_config(guild, retry=True) :
    print("====Loading Config====\nGuild Name: {}\nID: {}\n\n".format(guild.name, guild.id))
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
    member = guild.get_member(int(id))
    moderator = guild.get_member(int(modid))
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
    member = guild.get_member(int(id))
    moderator = guild.get_member(int(modid))
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
    member = guild.get_member(int(id))
    moderator = guild.get_member(int(modid))
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

    member = guild.get_member(int(id))
    moderator = guild.get_member(int(modid))
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
