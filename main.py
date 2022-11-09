import discord
import os
import json
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
#from dotenv import load_dotenv

from prefix import get_prefix

'''
auto check if channel is being translated 
Auto translate - post pictures ** should be fixed
double react creates double message ** should be fixed
'''
#line below only need for non-vscode enviroments and line 7 would need to be un-commented
#load_dotenv()
creator_id = int(os.getenv('owner_id'))

#can add more ids here
owner_id = {creator_id}
TOKEN = os.getenv('Discord_token')
with open("data.json", 'r') as file:
    data = json.load(file)
    pre_fix = data['pre_fix']
    bot_channel = data['bot_channel']
    file.close()

def settings(prefix, owner_id):
    global bot
    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix = prefix, owner_ids=owner_id, intents=intents)

settings(get_prefix, owner_id)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
#removes the help command
#bot.remove_command('help')

#prevents bot from responding to self
'''
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.channel.id in chan_id_list:
        ctx = await bot.get_context(message)
        data_for_trans = chan_lang_list[chan_id_list.index(message.channel.id)]
        await auto_translate(ctx, message, data_for_trans)
    await bot.process_commands(message)
'''

@bot.command(hidden=True)
@commands.is_owner()
async def add_cog(ctx, file_name):
    try:
        bot.load_extension(f'cogs.{file_name}')
        await ctx.channel.send(f"{file_name} cog has been loaded")
    except Exception as e:
        await ctx.channel.send(e)

@bot.command(hidden=True)
@commands.is_owner()
async def remove_cog(ctx, file_name):
    try:
        bot.unload_extension(f'cogs.{file_name}')
        await ctx.channel.send(f"{file_name} cog has been unloaded")
    except Exception as e:
        await ctx.channel.send(e)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

#waits till the bot is ready
@bot.event
async def on_ready():
    print('\nLogged in as ', end="")
    print(bot.user.name)
    print('------\n')

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(TOKEN)