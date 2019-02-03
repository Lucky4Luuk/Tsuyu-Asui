import discord
import asyncio
import json
import random

f = open("token.txt")
TOKEN = f.read().strip()
f.close()
f = open("error_codes.json")
ERROR_CODES = json.load(f)
f.close()

LUUK_ID = "183315569745985545"

configs = {}

client = discord.Client()

def generate_error(code) :
    return "ERROR {}: {} <a:TsuTearsBot:541326614143959050>".format(code, ERROR_CODES[code])

def import_config(server) :
    print("====Loading Config====\nServer Name: {}\nID: {}\n\n".format(server.name, server.id))
    try :
        f = open("{}-config.json".format(server.id), encoding="latin-1")
        configs[server.id] = json.load(f)
        f.close()
    except Exception as e :
        print(e)

def import_all_configs() :
    for server in client.servers :
        import_config(server)

def get_config_embed() :
    embed=discord.Embed(title="Config", description="", color=0x00b700)
    #embed.set_footer(text="Page {}".format(page_number))
    return embed

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    import_all_configs()

@client.event
async def on_member_join(member):
    joinchannel = str(configs[member.server.id]["JoinChannel"]).strip()
    joinmessages = configs[member.server.id]["JoinMessages"]
    #print(member.server)
    #print(member.server.get_channel(joinchannel))
    await client.send_message(member.server.get_channel(joinchannel), random.choice(joinmessages).format(user=member.mention, guild=member.server))

@client.event
async def on_message(message):
    if message.content == message.server.me.mention :
        await client.send_message(message.channel, "Hello! Do you need help with anything? Feel free to use ta!help at any point if you need my help <:TsuComfyBot:541315853149536257>")
    elif message.content.startswith("ta!lmgtfy") :
        args = message.content.split("ta!lmgtfy")[1].lstrip().rstrip().split(" ")
        result = generate_error("101")
        if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
            result = "<http://lmgtfy.com/?q="
            for arg in args :
                result += arg + "+"
            result = result[:-1] + ">"
        await client.send_message(message.channel, result)
    #elif message.content.startswith("ta!crab") :
    #    args = message.content.split("ta!crab")[1].lstrip().rstrip().split(" ")
    #    result = generate_error("101")
    #    if len(args) > 0 and not (len(args) == 1 and args[0] == '') :
    #        arg_len = 0
    #        for arg in args :
    #            arg_len += len(arg)
    #        result = "🦀{}🦀\n".format(args[0].ljust((arg_len - len(args[0]))*2)) + "-"*arg_len*2 + "\n🦀"
    #        args.pop(0)
    #        for arg in args :
    #            result += arg+" "
    #        result += "🦀"
    #    await client.send_message(message.channel, result)
    elif message.content.startswith("ta!admin") :
        if message.author.server_permissions :
            if message.author.server_permissions.administrator :
                if message.content == "ta!admin" :
                    #msg = await client.send_message(message.channel, embed=get_config_embed())
                    #res = await client.wait_for_reaction(["⬅", "➡"])
                    await client.send_message(message.channel, embed=get_config_embed())
                elif message.content.startswith("ta!admin set_join_message") : #25 chars
                    msg = message.content[26:]
                    await client.send_message(message.channel, "Your join message is now: '{}'".format(msg.format(user=message.author.mention, guild=message.server)))
            else :
                await client.send_message(message.channel, generate_error("302"))
        else :
            await client.send_message(message.channel, generate_error("303"))

    elif message.content.startswith("ta!") :
        await client.send_message(message.channel, generate_error("301"))

    elif message.author.id == LUUK_ID :
        if message.content.startswith("ta!reload_error_codes") :
            f = open("error_codes.json")
            ERROR_CODES = json.load(f)
            f.close()
            await client.send_message(message.channel, "No problem <:TsuAdorableBot:541315335169507345>")
        elif message.content.startswith("ta!reload_config_file_current") :
            if message.server :
                import_config(message.server.id)
            else :
                await client.send_message(message.channel, generate_error("201"))
        elif message.content.startswith("ta!save_configs") :
            print("no")

        elif message.content.startswith("ta!") :
            await client.send_message(message.channel, generate_error("301"))

client.run(TOKEN)
