from globals import *
from utils import *

@client.event
async def on_command_error(ctx, error) :
    if type(error) == commands.errors.CommandOnCooldown : await on_command_on_cooldown(ctx, error); return
    if type(error) == commands.errors.CommandNotFound : await on_command_not_found(ctx, error); return
    await ctx.send("An unknown error occured! Please forward the error below to Luuk#5979!\n```\n{}```".format(error))

async def on_command_on_cooldown(ctx, error) :
    time_left = datetime.timedelta(seconds=error.retry_after)
    hours = math.floor(time_left.seconds / 3600)
    minutes = math.floor(time_left.seconds / 60) % 60
    time_left_formatted = "0 seconds"
    if time_left.days > 0 :
        time_left_formatted = "{} days, {} hours and {} minutes".format(time_left.days, hours, minutes)
    elif hours > 0 :
        time_left_formatted = "{} hours and {} minutes".format(hours, minutes)
    elif minutes > 0 :
        time_left_formatted = "{} minutes and {} seconds".format(minutes, math.floor(time_left.seconds))
    await ctx.send(content="Command is still on cooldown! Try again in {}.".format(time_left_formatted))

async def on_command_not_found(ctx, error) :
    await ctx.send(content="Command not found!")
