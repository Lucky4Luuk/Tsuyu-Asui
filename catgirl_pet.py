from globals import *
from utils import *

def get_random_catgirl(name) :
    global BREEDS, TRAITS
    catgirl = {
        "name": name,
        "breed": random.choice(list(BREEDS.keys())),
        "traits": [],
        "stats": {
            "courage": random.randint(35, 60),
            "extroversion": random.randint(35, 60),
            "laziness": random.randint(35, 60)
        }
    }
    catgirl["traits"] = BREEDS[catgirl["breed"]]["base_traits"]
    available_traits = list(TRAITS.keys())
    idx = 0
    for trait in available_traits :
        if trait in catgirl["traits"] :
            available_traits.pop(idx)
        idx += 1

    for i in range(random.randint(0, 4)) :
        idx = random.randint(0, len(available_traits)-1)
        catgirl["traits"].append(available_traits[idx])
        available_traits.pop(idx)

    for trait in catgirl["traits"] :
        trait_modifiers = TRAITS[trait]
        for key, value in trait_modifiers.items() :
            catgirl["stats"][key] += value * 10

    return catgirl

@client.group(aliases=["cg", "catgirl"])
async def catgirls(ctx) :
    if ctx.invoked_subcommand is None :
        await ctx.send(content="Buy yourself a catgirl with ta!catgirls buy <name>!")

@catgirls.command()
async def buy(ctx, name) :
    if name :
        if (not "Catgirl" in main_config["Profiles"][str(ctx.message.author.id)].keys()) and main_config["Profiles"][str(ctx.message.author.id)]["Yen"] >= 250 :
            main_config["Profiles"][str(ctx.message.author.id)]["Yen"] -= 250
            main_config["Profiles"][str(ctx.message.author.id)]["Catgirl"] = get_random_catgirl(name)
            await ctx.send("You just bought your very own catgirl!")
            save_main_config()
        elif main_config["Profiles"][str(ctx.message.author.id)]["Yen"] < 250 :
            await ctx.send("Sorry, you don't have enough funds. You need at least 250 yen to buy a catgirl!")
        else :
            await ctx.send("You already have a catgirl! You can't buy another one. Everyone should be able to enjoy one!")
    else :
        await ctx.send("You need to give her a name!")

@catgirls.command()
async def info(ctx) :
    await ctx.send("Not implemented yet!")
