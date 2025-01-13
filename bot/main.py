import discord
from discord.ext import commands, tasks

from rss_feed import get_new_articles, extract_data
from db import create_table, delete_old_articles, record_article_in_db
from config import TOKEN, CHANNEL_ID, UPDATE_INTERVAL, IGNORE

'''Creates the bot instance'''
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

'''Main task'''
@tasks.loop(minutes=UPDATE_INTERVAL)
async def post_new_articles_task():
    channel = await bot.fetch_channel(CHANNEL_ID)
    new_articles = get_new_articles()
    for article in new_articles:
        message = extract_data(article)
        if message != IGNORE:
            await channel.send(embed=message)
        record_article_in_db(article["article"])

'''Deletes old articles from the database'''
@tasks.loop(hours=24)
async def delete_old_articles_task():
    delete_old_articles()

'''The bot starts looping the task once it's connected'''
@bot.listen()
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    post_new_articles_task.start()
    delete_old_articles_task.start()

'''Starts the bot so it connects to discord'''
if __name__ == "__main__":
    create_table()
    bot.run(TOKEN)
