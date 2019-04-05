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

    await member.guild.get_channel(int(joinchannel)).send(random.choice(joinmessages).format(user=member.mention, guild=member.guild))

async def remove_link(message) :
    channel = message.channel
    id = message.author.id
    #await channel.send(content="ta!warn {} Posted an invite link.".format(id))
    try :
        warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
        embed, case_number, got_kicked = warn_user(message.guild, client.id, id, "For posting an invite link.")
        if got_kicked :
            await ctx.send(content="*User {} has been kicked...*".format(member.name))
            try :
                await member.send(content=configs[message.guild.id]["KickMessage"].format(guild=message.guild.name, user=member.name))
            except Exception :
                await channel.send(content="*Unable to send {} the kick message, he might've blocked me or turned off DMs* <a:TsuCryingBot:541325707540824085>".format(member.name))
            await client.kick(member)
        else :
            await channel.send(content="*User {} has been warned...*".format(member.name))
    except Exception as e :
        print(e)
    await message.delete()

@client.event
async def on_message(message) :
    if "discordapp.com/invite/" in message.content or "discord.gg/" in message.content :
        await remove_link(message)
    else :
        await client.process_commands(message)

client.run(TOKEN)
