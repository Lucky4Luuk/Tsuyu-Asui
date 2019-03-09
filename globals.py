import os
import json
import discord
from discord.ext import commands
import asyncio

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

#client = discord.Client()
client = commands.Bot(command_prefix="ta!")
