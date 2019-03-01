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
                    warn_channel = message.guild.get_channel(str(configs[message.guild.id]["Mod"]["TextChannel"]))
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
