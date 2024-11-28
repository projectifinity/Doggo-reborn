import discord
from discord.ext import commands
from functions.randomPick import random_line
import requests, json
from functions.cocktaildb_grabber import drink_info, ingredient_filtered_data_returns_rdm_id, drink_by_id
from functions.mydramalistSearch import drama_link
from config import BOT

#  intents is required for discord.py version 2(?)
intents = discord.Intents.default()
intents.message_content = True

# Defines the bot prefix
bot = commands.Bot(command_prefix = '.',intents=intents)



# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command handler for the 'ping' command
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (bot.latency * 1000)}ms ')




@bot.command(help='Randomly picks from a food list')
async def food(ctx):
    await ctx.send(random_line('lists/foodList.txt'))


@bot.command(help='Randomly picks a snack item to eat')
async def snack(ctx):
    await ctx.send(random_line('lists/snackList.txt'))


@bot.command(help='Picks something from Aici\'s food list')
async def aicifood(ctx):
    await ctx.send(random_line('lists/aicifood.txt'))


@bot.command()
async def pytha(ctx):
    await ctx.send(random_line('lists/pork.txt'))


@bot.command()
async def mousa(ctx):
    await ctx.send(random_line('lists/moose.txt'))


@bot.command(help='Picks a classic cocktail from Serious Eats')
async def cocktail(ctx):
    await ctx.send(random_line('lists/classic-cocktails.txt'))


@bot.command(help='Picks a random mixed beverage that is either alcoholic or non-alcoholic')
async def drink(ctx, *args):
    # checks if tuple, args, is empty
    if len(args) == False:

        # grab data
        res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')

        # converts response data to dict (like an array)
        info = json.loads(res.text)

        # gets information on random drink
        drinkName, direc, imgLink, pfull = drink_info(info)

    # tuple has arguments
    else:
        ingredientFilter = ' '.join(args)

        # grab data
        res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=' + ingredientFilter)

        # converts response data to dict (like an array)
        info = json.loads(res.text)

        drinkID = ingredient_filtered_data_returns_rdm_id(info)
        info = drink_by_id(drinkID)

        print(info)

        drinkName, direc, imgLink, pfull = drink_info(info)

        print(drinkName, direc, imgLink, pfull)

    d = discord.Embed(
        title=drinkName,
    )
    d.set_thumbnail(url=imgLink)
    d.add_field(name="**Ingredients:**", value=pfull, inline=False)
    d.add_field(name="**Directions:**", value=direc, inline=False)
    await ctx.send(embed=d)


@bot.command(help='Searches MyDramaList (CURRENTLY NOT WORKING)')
async def drama(ctx, *args):
    search = ' '.join(args)
    print('Search terms: ' + search)

    res = requests.get("https://kuryana.vercel.app/search/q/" + search)
    dramaData = json.loads(res.text)

    await ctx.send(drama_link(dramaData))



#If there is an error, it will answer with an error
#@bot.event
#async def on_command_error(ctx, error):
#    await ctx.send(f'Error. Try "w help" ({error})')


bot_token = BOT['TOKEN']

bot.run(bot_token)