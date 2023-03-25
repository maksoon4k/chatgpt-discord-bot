#Perhaps there is something unnecessary here, I am too lazy to fix it, let you yourself
import discord
from discord.ext.commands import Bot, context
from discord.ext import commands
import openai
import json
import asyncio
import datetime
import time

#import from config.json
file = open('config.json', 'r')
config = json.load(file)
bot = Bot(config['prefix'], intents=intents)
openai.api_key = config['token_openai']

#Intents. What else is there to say?
intents = discord.Intents.all()

#Well, if it runs, it will work
@bot.event
async def on_ready():
    print('Call On')

#The model can be any (of the available), the main thing is to edit the response block, they seem to differ slightly there
model_engine = "text-davinci-003"

#for cooldowns
cooldowns = {}

#Here's the most juice
@bot.command(name='s')
async def cont(ctx: commands.context, *, args):
    if ctx.message.channel.id == 855383995286028318: #The numbers can be whatever you want, you can make at least a billion such blocks if you want. numbers are if anything the id of the channel for which you want to make a cd. if you do not need a cd, then you can just all from here (including this line) to the line where I will write "banana" in the comments
        if ctx.message.channel.id not in cooldowns or time.time() - cooldowns[ctx.message.channel.id] > 3600: #3600 is seconds for cooldown, you can put any number here
            result = str(args)
            response = openai.Completion.create(
                engine=model_engine,
                prompt=result,
                temperature=0.9,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
            )
            await ctx.send(embed=discord.Embed(title=f'{result}', description=response['choices'][0]['text']))
            cooldowns[ctx.message.channel.id] = time.time()
        else:
            remaining_time = round(3600 - (time.time() - cooldowns[ctx.message.channel.id])) #oh, and here you need to change seconds, if you need
            await ctx.send(f"Im in cooldown, lets try after {remaining_time} seconds.") #oh, wait, what? i have two errors for cooldown...why? idk, maybe fix this later.
    else: #banana, this line is also unnecessary if cd is not needed
        result = str(args)
        response = openai.Completion.create(
            engine=model_engine,
            prompt=result,
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=""
        )
        await ctx.send(embed=discord.Embed(title=f'{args}', description=response['choices'][0]['text'])) #this creates the message itself

#here error for cooldown, if you dont need cooldown, you can delete this
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = str(datetime.timedelta(seconds=error.retry_after)).split('.')[0]
        await ctx.send(f'**Im in cooldown, {ctx.author.name}, try in {retry_after}**')

#This launches the bot
bot.run(config['token'])
