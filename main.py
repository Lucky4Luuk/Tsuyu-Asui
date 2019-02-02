import discord
import asyncio
import json

f = open("token.txt")
TOKEN = f.read().strip()
f.close()
f = open("error_codes.json")
ERROR_CODES = json.load(f)
f.close()

LUUK_ID = "183315569745985545"

client = discord.Client()

def generate_error(code) :
    return "ERROR {}: {}".format(code, ERROR_CODES[code])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for server in client.servers :
        print("Name: {}\nID: {}".format(server.name, server.id))

@client.event
async def on_message(message):
    if message.content.startswith("ta!lmgtfy") :
        args = message.content.split("ta!lmgtfy")[1].lstrip().rstrip().split(" ")
        result = generate_error("101")
        if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
            result = "<http://lmgtfy.com/?q="
            for arg in args :
                result += arg + "+"
            result = result[:-1] + ">"
        await client.send_message(message.channel, result)
    if message.author.id == LUUK_ID :
        if message.content.startswith("ta!reload_error_codes") :
            f = open("error_codes.json")
            ERROR_CODES = json.load(f)
            f.close()
            await client.send_message(message.channel, "No problem <:TsuAdorableBot:541315335169507345>")

client.run(TOKEN)
