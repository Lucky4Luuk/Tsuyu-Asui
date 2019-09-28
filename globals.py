import os
import json
import discord
from discord.ext import commands, tasks
import asyncio
import requests
import re
import urllib.parse
import math
import datetime
import random
import sys
import io
from PIL import Image, ImageFont, ImageDraw

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

MESSAGE_COOLDOWN = 60
MESSAGE_SHECKELS = 10
DAILY_SHECKELS = 750

f = open("catgirls/breeds.json")
BREEDS = json.load(f)
f.close()
f = open("catgirls/traits.json")
TRAITS = json.load(f)
f.close()

LUUK_ID = 183315569745985545
BOT_ID = 515859822441136130
RHONE_ID = 84131451431292928

GITHUB = "https://github.com/Lucky4Luuk/Tsuyu-Asui"

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

PASTE_MYST = "https://paste.myst.rs/"

configs = {}
f = open("main_config.json")
main_config = json.load(f)
f.close()

#client = discord.Client()
client = commands.Bot(command_prefix="ta!", help_command=None)
