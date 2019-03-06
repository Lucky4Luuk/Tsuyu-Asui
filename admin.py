from globals import *
from utils import *
import datetime

async def admin(message) :
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

async def warn(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a warn
            args = message.content[8:].split(" ")
            id = args[0].replace("<","").replace("@","").replace(">","").replace("!","").strip()
            if id != "" and id.isdigit() :
                member = message.guild.get_member(int(id))
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number, got_kicked = warn_user(message.guild, message.author.id, id, reason)
                    if got_kicked :
                        await message.channel.send(content="*User {} has been kicked...*".format(member.name))
                        await client.kick(member)
                    else :
                        await message.channel.send(content="*User {} has been warned...*".format(member.name))
                    try :
                        msg = await warn_channel.send(embed=embed)
                        configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                        save_config(message.guild)
                    except Exception :
                        save_config(message.guild)
                else :
                    await message.channel.send(content=generate_error("305"))
            else :
                await message.channel.send(content=generate_error("307"))
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))

async def kick(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a kick
            args = message.content[8:].split(" ")
            id = args[0].replace("<","").replace("@","").replace(">","").replace("!","").strip()
            if id != "" and id.isdigit() :
                member = message.guild.get_member(int(id))
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number = kick_user(message.guild, message.author.id, id, reason)
                    await message.channel.send(content="*User {} has been kicked...*".format(member.name))
                    await member.send(content=configs[message.guild.id]["KickMessage"].format(guild=message.guild.name, user=member.name))
                    msg = await warn_channel.send(embed=embed)
                    await member.kick()
                    configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.guild)
                else :
                    await message.channel.send(content=generate_error("305"))
            else :
                await message.channel.send(content=generate_error("307"))
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))

async def ban(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a ban
            args = message.content[7:].split(" ")
            id = args[0].replace("<","").replace("@","").replace(">","").replace("!","").strip()
            if id != "" and id.isdigit() :
                member = message.guild.get_member(int(id))
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
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
                await message.channel.send(content=generate_error("307"))
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))

async def set_kick_message(message) :
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

async def set_ban_message(message) :
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

async def set_warning_channel(message) :
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

async def set_welcome_channel(message) :
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

async def set_max_warns(message) :
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

async def reset_warns(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            id = message.content[15:].strip().replace("<", "").replace(">", "").replace("!", "").replace("@", "")
            if id != "" and id in configs[message.guild.id]["Profiles"] :
                member = message.guild.get_member(int(id))
                configs[message.guild.id]["Profiles"][str(id)]["Warnings"] = 0
                await message.channel.send(content="{}'s warnings have been reset!".format(member.mention))
                save_config(message.guild)
            else :
                await message.channel.send(content=generate_error("307"))
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))

async def get_warns(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            id = message.content[13:].strip().replace("<", "").replace(">", "").replace("!", "").replace("@", "")
            if id != "" and id in configs[message.guild.id]["Profiles"] :
                member = message.guild.get_member(int(id))
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

async def purge(message) :
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

async def save_config(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            save_config(message.guild)
            await message.channel.send(content="Your config file has been saved!")
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))

async def reload_config(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            import_config(message.guild)
            await message.channel.send(content="Your config file has been reloaded!")
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))

async def export_config(message) :
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            import_config(message.guild)
            await message.channel.send(file="{}-config.json".format(message.guild.id))
        else :
            await message.channel.send(content=generate_error("302"))
    else :
        await message.channel.send(content=generate_error("303"))
