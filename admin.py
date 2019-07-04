from globals import *
from utils import *
import datetime

@client.command()
async def admin(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if message.author.guild_permissions.administrator :
            await ctx.send(embed=get_config_embed()) #TODO: fix pls
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_word_blacklist(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            args = message.content[22:].split(",")
            if not "," in message.content[22:] :
                args = [message.content[22:]]
            if len(args) > 0 :
                configs[message.guild.id]["WordBlacklist"] = args
                await ctx.send("The new word blacklist is:\n'{}'".format(args))
            else :
                await ctx.send(content=generate_error("308"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_word_blacklist(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            if "WordBlacklist" in configs[message.guild.id].keys() :
                await ctx.send(content="The current word blacklist is:\n'{}'".format(configs[message.guild.id]["WordBlacklist"]))
            else :
                await ctx.send(content=generate_error("311"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_slowmode_delay(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            delay = int(message.content.split(" ")[1])
            #ctx.message.channel.slowmode_delay = delay
            await ctx.message.channel.edit(slowmode_delay=delay)
            await ctx.send("Set slowmode delay in current channel to `{}`".format(delay))
        else :
            print("yeet")
    else  :
        print("yeet")

@client.command()
async def warn(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a warn
            args = message.content[8:].split(" ")
            id = args[0].strip('"" @ <>')
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
                        await ctx.send(content="*User {} has been kicked...*".format(member.name))
                        try :
                            await member.send(content=configs[message.guild.id]["KickMessage"].format(guild=message.guild.name, user=member.name))
                        except Exception :
                            await ctx.send(content="*Unable to send {} the kick message, he might've blocked me or turned off DMs* <a:TsuCryingBot:541325707540824085>".format(member.name))
                        await member.kick()
                    else :
                        await ctx.send(content="*User {} has been warned...*".format(member.name))
                    try :
                        msg = await warn_channel.send(embed=embed)
                        configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                        save_config(message.guild)
                    except Exception :
                        save_config(message.guild)
                else :
                    await ctx.send(content=generate_error("305"))
            else :
                await ctx.send(content=generate_error("307"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def kick(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a kick
            args = message.content[8:].split(" ")
            id = args[0].strip('"" @ <>')
            if id != "" and id.isdigit() :
                member = message.guild.get_member(int(id))
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number = kick_user(message.guild, message.author.id, id, reason)
                    await ctx.send(content="*User {} has been kicked...*".format(member.name))
                    try :
                        await member.send(content=configs[message.guild.id]["KickMessage"].format(guild=message.guild.name, user=member.name))
                    except Exception :
                        await ctx.send(content="*Unable to send {} the kick message, they might've blocked me or turned off DMs* <a:TsuCryingBot:541325707540824085>".format(member.name))
                    msg = await warn_channel.send(embed=embed)
                    await member.kick()
                    configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.guild)
                else :
                    await ctx.send(content=generate_error("305"))
            else :
                await ctx.send(content=generate_error("307"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def ban(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a ban
            args = message.content[7:].split(" ")
            id = args[0].strip('"" @ <>')
            if id != "" and id.isdigit() :
                member = message.guild.get_member(int(id))
                if message.author.top_role.position > member.top_role.position :
                    args.pop(0)
                    reason = ""
                    for arg in args :
                        reason += arg + " "
                    warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
                    embed, case_number = ban_user(message.guild, message.author.id, id, reason)
                    await ctx.send(content="*User {} has been banned...*".format(member.name))
                    try :
                        await member.send(content=configs[message.guild.id]["BanMessage"].format(guild=message.guild.name, user=member.name))
                    except Exception :
                        await ctx.send(content="*Unable to send {} the ban message, they might've blocked me or turned off DMs* <a:TsuCryingBot:541325707540824085>".format(member.name))
                    msg = await warn_channel.send(embed=embed)
                    await member.ban()
                    configs[message.guild.id]["Mod"]["Cases"][case_number-1]["MessageId"] = int(msg.id)
                    save_config(message.guild)
                else :
                    await ctx.send(content=generate_error("305"))
            else :
                await ctx.send(content=generate_error("307"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_reason(ctx) :
    message = ctx.message
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
                await ctx.send(content=generate_error("304"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_kick_message(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            reason = message.content[20:]
            configs[message.guild.id]["KickMessage"] = reason
            await ctx.send(content="Your new kick message is now '{}'".format(reason.format(user=message.author, guild=message.guild.name)))
            save_config(message.guild)
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_ban_message(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            reason = message.content[19:]
            configs[message.guild.id]["BanMessage"] = reason
            await ctx.send(content="Your new ban message is now '{}'".format(reason.format(user=message.author, guild=message.guild.name)))
            save_config(message.guild)
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_kick_message(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            if configs[message.guild.id]["KickMessage"] :
                await ctx.send(content="The current kick message is:\n{}".format(configs[message.guild.id]["KickMessage"]))
            else :
                await ctx.send(content=generate_error("309"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_ban_message(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            if configs[message.guild.id]["BanMessage"] :
                await ctx.send(content="The current ban message is:\n{}".format(configs[message.guild.id]["BanMessage"]))
            else :
                await ctx.send(content=generate_error("310"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_warning_channel(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a edit
            channel_id = str(message.content[23:].strip('"" # <>'))
            guild = message.guild
            configs[guild.id]["Mod"]["TextChannel"] = channel_id
            await ctx.send(content="The warning channel has been set!\nChannel: {} - ID: {}".format(guild.get_channel(channel_id).mention, channel_id))
            save_config(guild)
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_warning_channel(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            guild = message.guild
            channel_id = configs[guild.id]["Mod"]["TextChannel"]
            await ctx.send(content="The warning channel is currently: {} - ID: {}".format(guild.get_channel(channel_id).mention, channel_id))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_join_message(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            msg = message.content[20:]
            configs[message.guild.id]["JoinMessages"] = [msg]
            await ctx.send(content="Your join message is now: '{}'".format(msg.format(user=message.author.mention, guild=message.guild)))
            save_config(message.guild)
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_join_message(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            msg = configs[message.guild.id]["JoinMessages"][0]
            await ctx.send(content="Your join message is currently: '{}'".format(msg.format(user=message.author.mention, guild=message.guild)))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_welcome_channel(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            #do a edit
            channel_id = str(message.content[23:].strip('"" # <>'))
            guild = message.guild
            configs[guild.id]["JoinChannel"] = channel_id
            await ctx.send(content="The welcome channel has been set!\nChannel: {} - ID: {}".format(guild.get_channel(int(channel_id)).mention, channel_id))
            save_config(guild)
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_welcome_channel(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            guild = message.guild
            channel_id = configs[guild.id]["JoinChannel"]
            await ctx.send(content="The current welcome channel is: {} - ID: {}".format(guild.get_channel(int(channel_id)).mention, channel_id))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def set_max_warns(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            num = message.content[17:].strip()
            try :
                num = int(num)
                configs[message.guild.id]["Mod"]["MaxWarnings"] = num
                await ctx.send(content="The maximum amount of warnings before a kick occurs is now '{}'".format(num))
                save_config(message.guild)
            except Exception as e :
                await ctx.send(content=generate_error("306"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_max_warns(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            num = configs[message.guild.id]["Mod"]["MaxWarnings"]
            await ctx.send(content="The maximum amount of warnings before a kick occurs is currently '{}'".format(num))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def reset_warns(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            id = message.content[15:].strip().replace("<", "").replace(">", "").replace("!", "").replace("@", "")
            if id != "" and id in configs[message.guild.id]["Profiles"] :
                member = message.guild.get_member(int(id))
                configs[message.guild.id]["Profiles"][str(id)]["Warnings"] = 0
                await ctx.send(content="{}'s warnings have been reset!".format(member.mention))
                save_config(message.guild)
            else :
                await ctx.send(content=generate_error("307"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def get_warns(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            id = message.content[13:].strip().replace("<", "").replace(">", "").replace("!", "").replace("@", "")
            if id != "" and id in configs[message.guild.id]["Profiles"] :
                member = message.guild.get_member(int(id))
                warnings = int(configs[message.guild.id]["Profiles"][str(id)]["Warnings"]) #probably not needed to cast to int, but im tired so i cannot think straight lol
                if warnings == 0 :
                    await ctx.send(content="{} has {} warnings! <a:TsuDanceBot:542450965463433226>".format(member.mention, warnings))
                elif warnings == 1 :
                    await ctx.send(content="{} has {} warning!".format(member.mention, warnings))
                else :
                    await ctx.send(content="{} has {} warnings!".format(member.mention, warnings))
                #save_config(message.guild)
            else :
                await ctx.send(content="Either the ID is incorrect, or this person has never joined this guild. You can assume they have 0 warnings <:TsuSmileBot:541997306413580288>")
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def purge(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            num = message.content[9:].strip()
            if num != "" and num.isdigit() :
                #purge
                num = int(num)
                await message.channel.purge(limit=num+1)
                await ctx.send(content="*Purged {} messages...*".format(num))
            else :
                await ctx.send(content=generate_error("306"))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def save_server_config(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            save_config(message.guild)
            await ctx.send(content="Your config file has been saved!")
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def reload_config(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            import_config(message.guild)
            await ctx.send(content="Your config file has been reloaded!")
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@client.command()
async def export_config(ctx) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            import_config(message.guild)
            await ctx.send(file="{}-config.json".format(message.guild.id))
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))
