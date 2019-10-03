from globals import *
from utils import *

#To be called by the raw functions
async def on_reaction_add(reaction, user) :
    if user != client.user :
        print("User {}; Reaction {}".format(reaction, user))

async def on_reaction_remove(reaction, user) :
    if user != client.user :
        print("User {}; Reaction {}".format(reaction, user))

#Messages don't need to be in cache for these
@client.event
async def on_raw_reaction_add(payload) :
    guildid = payload.guild_id
    channelid = payload.channel_id
    msgid = payload.message_id
    userid = payload.user_id
    emoji = payload.emoji

    guild = client.get_guild(guildid)
    channel = guild.get_channel(channelid)
    message = await channel.fetch_message(msgid)
    member = guild.get_member(userid)

    if userid != client.user.id :
        print("Member {}; Emoji {}".format(member, emoji.name))
        if configs[guild.id]["ReactMessage"] :
            print("ReactMessage")
            if channelid == configs[guild.id]["ReactMessage"][0] and msgid == configs[guild.id]["ReactMessage"][1] :
                print("Correct channel/message")
                for item in configs[guild.id]["ReactRoles"] :
                    if int(item[0]) == emoji.id :
                        print("Assigning member a role")
                        role = guild.get_role(int(item[1]))
                        await member.add_roles(role, reason="He clicked the damn button")
                        print("User received his role!")

@client.event
async def on_raw_reaction_remove(payload) :
    guildid = payload.guild_id
    channelid = payload.channel_id
    msgid = payload.message_id
    userid = payload.user_id
    emoji = payload.emoji

    guild = client.get_guild(guildid)
    channel = guild.get_channel(channelid)
    message = await channel.fetch_message(msgid)
    member = guild.get_member(userid)

    if userid != client.user.id :
        print("Member {}; Emoji {}".format(member, emoji.name))
        if configs[guild.id]["ReactMessage"] :
            print("ReactMessage")
            if channelid == configs[guild.id]["ReactMessage"][0] and msgid == configs[guild.id]["ReactMessage"][1] :
                print("Correct channel/message")
                for item in configs[guild.id]["ReactRoles"] :
                    if int(item[0]) == emoji.id :
                        print("Removing a role from member")
                        role = guild.get_role(int(item[1]))
                        await member.remove_roles(role, reason="He clicked the damn button")
                        print("Remove user's role!")
