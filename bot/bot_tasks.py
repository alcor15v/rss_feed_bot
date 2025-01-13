import discord
from discord.ext import tasks

from rss_feed import get_new_articles, extract_data
from db import delete_old_articles, record_article_in_db
from config import CHANNEL_ID, UPDATE_INTERVAL

'''Main task'''
@tasks.loop(minutes=UPDATE_INTERVAL)
async def post_new_articles_task():
    channel = await bot.fetch_channel(CHANNEL_ID)
    new_articles = get_new_articles()
    for article in new_articles:
        message = extract_data(article)
        if message != "":
            await channel.send(embed=message)
        record_article_in_db(article["article"])

'''Deletes old articles from the database'''
@tasks.loop(hours=24)
async def delete_old_articles_task():
    delete_old_articles()
