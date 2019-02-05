import discord
import asyncio
import json
import random
import datetime

#custom imports
import minesweeper

f = open("token.txt")
TOKEN = f.read().strip()
f.close()
f = open("error_codes.json")
ERROR_CODES = json.load(f)
f.close()

LUUK_ID = "183315569745985545"

#colors
FROG_GREEN = 0x00b700
HONEY_ORANGE = 0xfa6912
BEE_YELLOW = 0xfadd16
FIRE_RED = 0xff0000
SKY_BLUE = 0xb9e3e6

WARN_COLOR = SKY_BLUE
BAN_COLOR = FIRE_RED

configs = {}

client = discord.Client()

def generate_error(code) :
    return "ERROR {}: {} <a:TsuTearsBot:541326614143959050>".format(code, ERROR_CODES[code])

def import_config(server, retry=True) :
    print("====Loading Config====\nServer Name: {}\nID: {}\n\n".format(server.name, server.id))
    try :
        f = open("{}-config.json".format(server.id), encoding="latin-1")
        configs[server.id] = json.load(f)
        f.close()
    except Exception as e :
        print(e)
        #create a new config file
        f = open("empty_config.json", encoding="latin-1")
        data = f.read()
        f.close()
        f = open("{}-config.json".format(server.id), "a+", encoding="latin-1")
        f.write(data)
        f.close()
        if retry :
            import_config(server, retry=False)

def import_all_configs() :
    for server in client.servers :
        import_config(server)

def save_config(server) :
    print("====Saving Config====\nServer Name: {}\nID: {}\n\n".format(server.name, server.id))
    try :
        f = open("{}-config.json".format(server.id), "w+", encoding="latin-1")
        f.seek(0)
        f.truncate()
        f.write(json.dumps(configs[server.id], indent="  "))
        f.close()
    except Exception as e :
        print(e)

def save_all_configs() :
    for server in client.servers :
        save_config(server)

def get_config_embed() :
    embed=discord.Embed(title="Config", description="", color=FROG_GREEN)
    #embed.set_footer(text="Page {}".format(page_number))
    return embed

def warn_user(server, modid, id, reason) :
    #print("yeet")
    if reason.strip() == "" :
        reason = "Please set a reason using ta!set_reason <case_number> <reason> <:TsuSmileBot:541997306413580288>"
    case_number = len(configs[server.id]["Mod"]["Cases"])+1
    case = {
        "ModId":int(modid),
        "UserId":int(id),
        "Reason":reason,
        "CaseNumber":case_number,
        "MessageId":0,
        "CaseType":6
    }
    configs[server.id]["Profiles"][id]["Warnings"] += 1
    if configs[server.id]["Profiles"][id]["Warnings"] > configs[server.id]["Mod"]["MaxWarnings"] :
        print("this guy should be kicked")
    member = server.get_member(id)
    moderator = server.get_member(modid)
    configs[server.id]["Mod"]["Cases"].append(case)
    timestamp = datetime.datetime.now()
    embed = discord.Embed(color=WARN_COLOR)
    embed.set_author(name="Case #{case_number} | Warning | {name}#{tag}".format(case_number=case_number, name=member.name, tag=member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text="ID: {} • {}".format(id, timestamp.strftime("%c")))
    #save_config(server)
    return embed, case_number

def kick_user(server, modid, id, reason) :
    #print("yeet")
    if reason.strip() == "" :
        reason = "Please set a reason using ta!set_reason <case_number> <reason> <:TsuSmileBot:541997306413580288>"
    case_number = len(configs[server.id]["Mod"]["Cases"])+1
    case = {
        "ModId":int(modid),
        "UserId":int(id),
        "Reason":reason,
        "CaseNumber":case_number,
        "MessageId":0,
        "CaseType":2
    }
    member = server.get_member(id)
    moderator = server.get_member(modid)
    configs[server.id]["Mod"]["Cases"].append(case)
    timestamp = datetime.datetime.now()
    embed = discord.Embed(color=WARN_COLOR)
    embed.set_author(name="Case #{case_number} | Kick | {name}#{tag}".format(case_number=case_number, name=member.name, tag=member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text="ID: {} • {}".format(id, timestamp.strftime("%c")))
    #save_config(server)
    return embed, case_number

def ban_user(server, modid, id, reason) :
    #print("yeet")
    if reason.strip() == "" :
        reason = "Please set a reason using ta!set_reason <case_number> <reason> <:TsuSmileBot:541997306413580288>"
    case_number = len(configs[server.id]["Mod"]["Cases"])+1
    case = {
        "ModId":int(modid),
        "UserId":int(id),
        "Reason":reason,
        "CaseNumber":case_number,
        "MessageId":0,
        "CaseType":1
    }
    member = server.get_member(id)
    moderator = server.get_member(modid)
    configs[server.id]["Mod"]["Cases"].append(case)
    timestamp = datetime.datetime.now()
    embed = discord.Embed(color=BAN_COLOR)
    embed.set_author(name="Case #{case_number} | Ban | {name}#{tag}".format(case_number=case_number, name=member.name, tag=member.discriminator), icon_url=member.avatar_url)
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Moderator", value=moderator.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_footer(text="ID: {} • {}".format(id, timestamp.strftime("%c")))
    #save_config(server)
    return embed, case_number

def set_reason(server, warn_channel, case_number, msgid, msg, reason) :
    old_embed = msg.embeds[0] #always the first embed, because that's how the commands work
    if reason.strip() == "" :
        reason = old_embed["fields"][2]["value"]
    case = configs[server.id]["Mod"]["Cases"][case_number-1]
    id = case["UserId"]
    modid = case["ModId"]

    member = server.get_member(id)
    moderator = server.get_member(modid)
    configs[server.id]["Mod"]["Cases"].append(case)
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
    return member.server_permissions.administrator or member.server_permissions.kick_members or member.server_permissions.ban_members

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    import_all_configs()

@client.event
async def on_member_join(member):
    joinchannel = str(configs[member.server.id]["JoinChannel"]).strip()
    joinmessages = configs[member.server.id]["JoinMessages"]
    #print(member.server)
    #print(member.server.get_channel(joinchannel))
    await client.send_message(member.server.get_channel(joinchannel), random.choice(joinmessages).format(user=member.mention, guild=member.server))

@client.event
async def on_message(message):
    if message.server == None : #PM
        f = open("DM_LOGS.txt", "r+")
        f.write("{}: {}\n".format(message.author.name, message.content))
        f.close()

    if message.content == message.server.me.mention :
        await client.send_message(message.channel, "Hello! Do you need help with anything? Feel free to use ta!help at any point if you need my help <:TsuComfyBot:541315853149536257>")

    if message.content.startswith("ta!lmgtfy") :
        args = message.content.split("ta!lmgtfy")[1].lstrip().rstrip().split(" ")
        result = generate_error("101")
        if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
            result = "<http://lmgtfy.com/?q="
            for arg in args :
                result += arg + "+"
            result = result[:-1] + ">"
        await client.send_message(message.channel, result)
    #elif message.content.startswith("ta!crab") :
    #    args = message.content.split("ta!crab")[1].lstrip().rstrip().split(" ")
    #    result = generate_error("101")
    #    if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
    #        arg_len = 0
    #        for arg in args :
    #            arg_len += len(arg)
    #        result = "🦀{}🦀\n".format(args[0].ljust((arg_len - len(args[0]))*2)) + "-"*arg_len*2 + "\n🦀"
    #        args.pop(0)
    #        for arg in args :
    #            result += arg+" "
    #        result += "🦀"
    #    await client.send_message(message.channel, result)
    elif message.content.startswith("ta!admin") :
        if message.author.server_permissions :
            if message.author.server_permissions.administrator :
                if message.content == "ta!admin" :
                    #msg = await client.send_message(message.channel, embed=get_config_embed())
                    #res = await client.wait_for_reaction(["⬅", "➡"])
                    await client.send_message(message.channel, embed=get_config_embed())
                elif message.content.startswith("ta!admin set_join_message") : #25 chars
                    msg = message.content[26:]
                    await client.send_message(message.channel, "Your join message is now: '{}'".format(msg.format(user=message.author.mention, guild=message.server)))
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))

    elif message.content.startswith("ta!warn") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                #do a warn
                args = message.content[8:].split(" ")
                id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                member = message.server.get_member(id)
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.server.get_channel(str(configs[message.server.id]["Mod"]["TextChannel"]))
                    embed, case_number = warn_user(message.server, message.author.id, id, reason)
                    await client.send_message(message.channel, "*User {} has been warned...*".format(member.name))
                    msg = await client.send_message(warn_channel, embed=embed)
                    configs[message.server.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.server)
                else :
                    await client.send_message(message.channel, generate_error("305"))
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!kick") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                #do a kick
                args = message.content[8:].split(" ")
                id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                member = message.server.get_member(id)
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.server.get_channel(str(configs[message.server.id]["Mod"]["TextChannel"]))
                    embed, case_number = kick_user(message.server, message.author.id, id, reason)
                    await client.send_message(message.channel, "*User {} has been kicked...*".format(member.name))
                    await client.send_message(member, configs[message.server.id]["KickMessage"].format(guild=server.name, user=member.name))
                    msg = await client.send_message(warn_channel, embed=embed)
                    await client.kick(member)
                    configs[message.server.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.server)
                else :
                    await client.send_message(message.channel, generate_error("305"))
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!ban") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                #do a ban
                args = message.content[7:].split(" ")
                id = args[0].replace("<","").replace("@","").replace(">","").replace("!","")
                member = message.server.get_member(id)
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.server.get_channel(str(configs[message.server.id]["Mod"]["TextChannel"]))
                    embed, case_number = ban_user(message.server, message.author.id, id, reason)
                    await client.send_message(message.channel, "*User {} has been banned...*".format(member.name))
                    await client.send_message(member, configs[message.server.id]["BanMessage"].format(guild=server.name, user=member.name))
                    msg = await client.send_message(warn_channel, embed=embed)
                    await client.ban(member)
                    configs[message.server.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.server)
                else :
                    await client.send_message(message.channel, generate_error("305"))
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!set_reason") :
        if message.author.server_permissions :
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
                    server = message.server
                    warn_channel = server.get_channel(str(configs[server.id]["Mod"]["TextChannel"]))
                    msgid = configs[server.id]["Mod"]["Cases"][case_number-1]["MessageId"]
                    msg = await client.get_message(warn_channel, str(msgid))
                    embed = set_reason(server, warn_channel, case_number, msgid, msg , reason)
                    await client.edit_message(msg, embed=embed)
                    save_config(server)
                else :
                    await client.send_message(message.channel, generate_error("304"))
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!set_kick_message") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                reason = message.content[20:]
                configs[message.server.id]["KickMessage"] = reason
                await client.send_message(message.channel, "Your new kick message is now '{}'".format(reason.format(user=message.author, guild=message.server.name)))
                save_config(message.server)
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!set_ban_message") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                reason = message.content[19:]
                configs[message.server.id]["BanMessage"] = reason
                await client.send_message(message.channel, "Your new ban message is now '{}'".format(reason.format(user=message.author, guild=message.server.name)))
                save_config(message.server)
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!save_config") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                save_config(message.server)
                await client.send_message(message.channel, "Your config file has been saved!")
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!reload_config") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                import_config(message.server)
                await client.send_message(message.channel, "Your config file has been reloaded!")
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
    elif message.content.startswith("ta!export_config") :
        if message.author.server_permissions :
            if is_moderator(message.author) :
                import_config(message.server)
                await client.send_file(message.channel, "{}-config.json".format(message.server.id), content="Your config file has been reloaded!")
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))
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
    #                await client.send_message(message.channel, generate_error("104"))
    #            if successful :
    #                lines = minesweeper.create_board(size_x, size_y, num_of_mines)
    #                for line in lines :
    #                    await client.send_message(message.channel, line)
    #        else :
    #            await client.send_message(message.channel, generate_error("102"))
    #    else :
    #        await client.send_message(message.channel, generate_error("103"))

    elif message.content.startswith("ta!") :
        await client.send_message(message.channel, generate_error("301"))

    elif message.author.id == LUUK_ID :
        if message.content.startswith("ta!reload_error_codes") :
            f = open("error_codes.json")
            ERROR_CODES = json.load(f)
            f.close()
            await client.send_message(message.channel, "No problem <:TsuAdorableBot:541315335169507345>")
        elif message.content.startswith("ta!reload_config_file_current") :
            if message.server :
                import_config(message.server.id)
            else :
                await client.send_message(message.channel, generate_error("201"))
        elif message.content.startswith("ta!save_configs") :
            save_all_configs()
            await client.send_message(message.channel, "No problem <:TsuAdorableBot:541315335169507345>")

        elif message.content.startswith("ta!") :
            await client.send_message(message.channel, generate_error("301"))

client.run(TOKEN)
