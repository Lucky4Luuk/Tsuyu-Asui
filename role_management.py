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
    user = guild.get_member(userid)

    if userid != client.user.id :
        print("User {}; Emoji {}".format(user, emoji.name))

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
    user = guild.get_member(userid)

    if userid != client.user.id :
        print("User {}; Emoji {}".format(user, emoji.name))
