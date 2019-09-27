from globals import *
from utils import *

@client.command(aliases=["daily", "dailyreward"])
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily_reward(ctx) :
    author_id = str(ctx.message.author.id)
    main_config["Profiles"][author_id]["Sheckels"] += DAILY_SHECKELS
    await ctx.send(content="You received your daily {} sheckels!".format(DAILY_SHECKELS))

@client.command(aliases=["bal", "balance", "credits"])
async def sheckels(ctx) :
    author_id = str(ctx.message.author.id)
    try :
        await ctx.send(content="You currently have {} sheckels!".format(main_config["Profiles"][author_id]["Sheckels"]))
    except Exception :
        await ctx.send(content="You currently have 0 sheckels!")

def on_message(message) :
    author_id = str(message.author.id)
    if not author_id in main_config["Profiles"].keys() :
        main_config["Profiles"][author_id] = {
            "LastMessage": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Sheckels": 0
        }
    if "LastMessage" in main_config["Profiles"][author_id].keys() :
        #These checks are for converting the old format to python
        if "T" in main_config["Profiles"][author_id]["LastMessage"] :
            main_config["Profiles"][author_id]["LastMessage"] = main_config["Profiles"][author_id]["LastMessage"].replace("T", " ")
        if "." in main_config["Profiles"][author_id]["LastMessage"] :
            main_config["Profiles"][author_id]["LastMessage"] = main_config["Profiles"][author_id]["LastMessage"].split(".")[0]

        last_message = datetime.datetime.strptime(main_config["Profiles"][author_id]["LastMessage"], "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        if (now - last_message).total_seconds() > MESSAGE_COOLDOWN :
            main_config["Profiles"][author_id]["Sheckels"] += MESSAGE_SHECKELS
            main_config["Profiles"][author_id]["LastMessage"] = now.strftime("%Y-%m-%d %H:%M:%S")
    else :
        last_message = datetime.datetime.now()
        main_config["Profiles"][author_id]["LastMessage"] = last_message

    save_main_config()
