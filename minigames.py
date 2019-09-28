from globals import *
from utils import *

@client.command(aliases=["coin", "coinflip"])
async def coin_flip(ctx) :
    msg = await ctx.send(content="Flipping coin...")
    await asyncio.sleep(1)
    result = "heads"
    if random.randint(0,1) > 0 :
        result = "tails"
    await msg.edit(content="It's {}!".format(result))

@client.group(aliases=["lot"])
async def lottery(ctx) :
    if ctx.invoked_subcommand is None :
        lottery_draw_time = datetime.datetime.strptime(main_config["LotteryDraw"], "%Y-%m-%d %H:%M:%S")
        time_left = datetime.timedelta(seconds=(lottery_draw_time - datetime.datetime.now()).total_seconds())
        hours = math.floor(time_left.seconds / 3600)
        minutes = math.floor(time_left.seconds / 60) % 60
        time_left_formatted = "0 seconds"
        if time_left.days > 0 :
            time_left_formatted = "{} days, {} hours and {} minutes".format(time_left.days, hours, minutes)
        elif hours > 0 :
            time_left_formatted = "{} hours and {} minutes".format(hours, minutes)
        elif minutes > 0 :
            time_left_formatted = "{} minutes and {} seconds".format(minutes, math.floor(time_left.seconds))
        amount = 0
        try :
            amount = len(configs[ctx.guild.id]["LotteryParticipants"]) * 50
        except Exception as e :
            print(e)
        await ctx.send(content="Buy a lottery ticket with ta!lottery buy <amount>! Each ticket is 50 yen.\nNext draw is in {}, with currently a prizepool of {}!".format(time_left_formatted, amount))

@lottery.command()
async def buy(ctx, amount) :
    author_id = str(ctx.message.author.id)
    guild_id = ctx.guild.id
    amount = int(amount)
    if int(main_config["Profiles"][author_id]["Yen"]) >= 50 * amount :
        if "LotteryTickets" in main_config["Profiles"][author_id].keys() :
            main_config["Profiles"][author_id]["LotteryTickets"] += amount
        else :
            main_config["Profiles"][author_id]["LotteryTickets"] = amount
        if not "LotteryParticipants" in configs[guild_id].keys() :
            configs[guild_id]["LotteryParticipants"] = []
        for i in range(amount) :
            configs[guild_id]["LotteryParticipants"].append(author_id)
        main_config["Profiles"][author_id]["Yen"] -= 50 * amount
        await ctx.send(content="You bought {} tickets!".format(amount))
        save_main_config()
        save_config(ctx.guild)
    else :
        await ctx.send(content="Sorry, you don't have enough money!")

def generate_ticket_image(count, author) :
    img = Image.open("assets/empty_ticket.png")
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("rm_typerighter_medium.ttf", 96)
    font_info1 = ImageFont.truetype("rm_typerighter_medium.ttf", 64)
    font_info2 = ImageFont.truetype("rm_typerighter_medium.ttf", 48)
    draw.text((9,0), "Ticket - {}x".format(count), (127,127,127), font=font_title)
    draw.text((9,42), "Owned by: {}".format(author), (127,127,127), font=font_info1)
    draw.text((9,74), "Cost: {}¥".format(count * 50), (127,127,127), font=font_info1)
    return img

@lottery.command()
async def tickets(ctx) :
    author_id = str(ctx.message.author.id)
    if "LotteryTickets" in main_config["Profiles"][author_id].keys() and main_config["Profiles"][author_id]["LotteryTickets"] > 0 :
        img = generate_ticket_image(main_config["Profiles"][author_id]["LotteryTickets"], str(ctx.message.author))
        img.save("assets/tmp/ticket.png")
        file = discord.File("assets/tmp/ticket.png")
        await ctx.send(content="You currently have {} tickets!".format(main_config["Profiles"][author_id]["LotteryTickets"]), file=file)
    else :
        await ctx.send(content="You currently don't have any tickets! Buy some using ta!lottery buy <amount>.")

@lottery.command()
async def set_channel(ctx, channel_id) :
    message = ctx.message
    if message.author.guild_permissions :
        if is_moderator(message.author) :
            configs[message.guild.id]["LotteryChannel"] = str(channel_id)
            await ctx.send(content="Your new lottery channel is now '{}'".format(client.get_channel(int(channel_id))))
            save_config(message.guild)
        else :
            await ctx.send(content=generate_error("302"))
    else :
        await ctx.send(content=generate_error("303"))

@lottery.command()
async def draw_now(ctx) :
    if int(ctx.message.author.id) == LUUK_ID :
        await ctx.send("Lottery should be drawn soon!")
        main_config["LotteryDraw"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tasks.loop(seconds=2.0)
async def lottery_check() :
    await client.wait_until_ready()
    time_left = (datetime.datetime.strptime(main_config["LotteryDraw"], "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()).total_seconds()
    if time_left < 1 :
        print("Draw lottery!")
        next_date = datetime.datetime.now() + datetime.timedelta(seconds=14400)
        main_config["LotteryDraw"] = next_date.strftime("%Y-%m-%d %H:%M:%S")
        for guild_id in configs.keys() :
            guild = client.get_guild(guild_id)
            if "LotteryChannel" in configs[guild_id].keys() :
                channel = guild.get_channel(int(configs[guild_id]["LotteryChannel"]))
                if channel :
                    participants = []
                    if not "LotteryParticipants" in configs[guild_id] :
                        await channel.send(content="Lottery has been drawn! There were no participants, so no winners either :(")
                    else :
                        for participants_id in configs[guild_id]["LotteryParticipants"] :
                            main_config["Profiles"][str(participants_id)]["LotteryTickets"] = 0
                            participants.append(client.get_user(int(participants_id)))
                        configs[guild_id]["LotteryParticipants"] = []
                        winner = random.choice(participants)
                        won_amount = len(participants) * 250
                        time_left = datetime.timedelta(seconds=(next_data - datetime.datetime.now()).total_seconds())
                        hours = math.floor(time_left.seconds / 3600)
                        minutes = math.floor(time_left.seconds / 60) % 60
                        time_left_formatted = "0 seconds"
                        if time_left.days > 0 :
                            time_left_formatted = "{} days, {} hours and {} minutes".format(time_left.days, hours, minutes)
                        elif hours > 0 :
                            time_left_formatted = "{} hours and {} minutes".format(hours, minutes)
                        elif minutes > 0 :
                            time_left_formatted = "{} minutes and {} seconds".format(minutes, math.floor(time_left.seconds))
                        await channel.send(content="Lottery has been drawn! The winner is {}! They won {} yen!\nNext lottery will be drawn on {}, get your tickets now!".format(winner, won_amount, time_left_formatted))
                        save_main_config()
                        save_config(guild)
