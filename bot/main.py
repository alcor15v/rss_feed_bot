import discord
from discord.ext import commands

import bot_tasks
from db import create_table
from config import TOKEN

'''Creates the bot instance'''
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

'''The bot starts looping the task once it's connected'''
@bot.listen()
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    bot_tasks.post_new_articles.start()
    bot_tasks.delete_old_articles.start()

'''Starts the bot so it connects to discord'''
if __name__ == "__main__":
    create_table()
    bot.run(TOKEN)
