from globals import *
from utils import *

@client.command(aliases=["daily", "dailyreward"])
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily_reward(ctx) :
    author_id = str(ctx.message.author.id)
    main_config["Profiles"][author_id]["Yen"] += DAILY_SHECKELS
    await ctx.send(content="You received your daily {} yen!".format(DAILY_SHECKELS))

@client.command(aliases=["bal", "balance", "credits", "sheckels"])
async def yen(ctx) :
    author_id = str(ctx.message.author.id)
    try :
        await ctx.send(content="You currently have {} yen!".format(main_config["Profiles"][author_id]["Yen"]))
    except Exception :
        await ctx.send(content="You currently have 0 yen!")

@client.command()
async def leaderboard(ctx) :
    def custom_sort(val) :
        return val[1]["Yen"]
    profiles = []
    for key, value in main_config["Profiles"].items() :
        profile = [key, value]
        profiles.append(profile)
    profiles.sort(key=custom_sort, reverse=True)
    result = "```\n"
    for i in range(min(len(profiles), 10)) :
        name = client.get_user(int(profiles[i][0]))
        amount = profiles[i][1]["Yen"]
        result += "{}. {} - {}\n".format(i, name, amount)
    result += "```"
    await ctx.send(content=result)

def on_message(message) :
    author_id = str(message.author.id)
    if "LastMessage" in main_config["Profiles"][author_id].keys() :
        #These checks are for converting the old format to python
        if "T" in main_config["Profiles"][author_id]["LastMessage"] :
            main_config["Profiles"][author_id]["LastMessage"] = main_config["Profiles"][author_id]["LastMessage"].replace("T", " ")
        if "." in main_config["Profiles"][author_id]["LastMessage"] :
            main_config["Profiles"][author_id]["LastMessage"] = main_config["Profiles"][author_id]["LastMessage"].split(".")[0]

        last_message = datetime.datetime.strptime(main_config["Profiles"][author_id]["LastMessage"], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        if (now - last_message).total_seconds() > MESSAGE_COOLDOWN :
            main_config["Profiles"][author_id]["Yen"] += MESSAGE_SHECKELS
            main_config["Profiles"][author_id]["LastMessage"] = now.strftime("%Y-%m-%d %H:%M:%S")
    else :
        last_message = datetime.datetime.now()
        main_config["Profiles"][author_id]["LastMessage"] = last_message

    save_main_config()
