import discord
import asyncio
import json
import random
import datetime
import os
import aiohttp
import urllib #not actually for doing link stuff, because it's blocking
import math

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

@client.command()
async def ping(ctx) :
    await ctx.send("Pong! Current ping: {} ms!".format(math.floor(client.latency * 10000)/10))

async def remove_link(message) :
    channel = message.channel
    id = message.author.id
    #await channel.send(content="ta!warn {} Posted an invite link.".format(id))
    if not (message.author.guild_permissions and is_moderator(message.author)) :
        try :
            warn_channel = message.guild.get_channel(int(configs[message.guild.id]["Mod"]["TextChannel"]))
            embed, case_number, got_kicked = warn_user(message.guild, BOT_ID, id, "For posting an invite link.")
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

###WIP just ignore it i dont want to deal with anything right now
#@client.event
#async def on_member_ban(guild, user) :
#

async def handle_codeblock(message) :
    block = re.search("```((.|\n)+)```", message.content)
    other_content = message.content.replace(block.group(), "")
    other_content = "\n" + other_content.replace("\n", "\n//")

    lang = block.group().split("\n",1)[0].strip()[3:]

    code = block.group().replace("```", "").replace(lang, "")

    data = urllib.parse.quote(other_content + code, safe='~()*!.\'')
    payload = {"code": data, "expiresIn": "1w"}
    #print(json.dumps(payload))
    #r = requests.post(PASTE_MYST, data=json.dumps(payload))
#    payload = '{' + '''
#    "code": "{data}",
#    "expiresIn": "1w"
#'''.format(data=data) + '}'
    #print(payload)
    r = requests.post(PASTE_MYST + "api/paste", json=payload)
    #print(r.text)
    #print(r.status_code)
    #print(r.json())
    json_data = r.json()
    link = PASTE_MYST + json_data["id"]
    await message.channel.send("Large codeblock detected!\nThe message and the codeblock have been neatly packaged and uploaded to the internet!\nYou can find it here: {} <:TsuSmileBot:541997306413580288>\nPS: You can find the rest of the message in the link as well, as a comment.".format(link))
    await message.delete()

@client.event
async def on_message(message) :
    if message.author.id != BOT_ID :
        if "discordapp.com/invite/" in message.content or "discord.gg/" in message.content :
            await remove_link(message)
        elif (not message.author.bot) && has_big_codeblock(message) :
            await handle_codeblock(message)
        elif check_word_blacklist(message) :
            print(message.content)
            await message.delete()
            await message.channel.send("One of the words you said are in the word blacklist! Please refrain from using this word in the future. Thank you <:TsuSmileBot:541997306413580288>")
        else :
            await client.process_commands(message)

client.run(TOKEN)
