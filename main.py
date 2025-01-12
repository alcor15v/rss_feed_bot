import feedparser
from datetime import datetime, timedelta, timezone
import sqlite3
import discord
from discord.ext import commands, tasks
from bs4 import SoupStrainer, BeautifulSoup
import re

from config import TOKEN, CHANNEL_ID, UPDATE_INTERVAL, LAST_ARTICLE_RANGE, RSS_FEEDS, CONTENT_SIZE, EMBED_COLOR

NO_EXECUTE = 'NO'

'''Connects to the database and creates the table if it doesn't exist'''
connection = sqlite3.connect('articles.db')
c = connection.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles (title TEXT, link TEXT, date TEXT)''')
connection.commit()

'''Creates the bot instance'''
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

'''Main task'''
@tasks.loop(minutes=UPDATE_INTERVAL)
async def post_new_articles():
    channel = await bot.fetch_channel(CHANNEL_ID)
    new_articles = get_new_articles()
    for article in new_articles:
        message = format_to_message(article)
        if message != NO_EXECUTE:
            await channel.send(embed=message)
        record_article_in_db(article["article"])

'''Looks for new articles to post them'''
def get_new_articles():
    new_articles = []
    for rss_feed in RSS_FEEDS:
        entries = feedparser.parse(rss_feed["url"]).entries
        for entry in entries:
            if not article_in_db(entry):
                pub_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) - pub_date <= timedelta(days=LAST_ARTICLE_RANGE):
                    new_articles.append({"article": entry, "keyword_filter":rss_feed["keyword_filter"]})
    return new_articles

'''Verifies if the article is already in the database'''
def article_in_db(entry):
    c.execute("SELECT link FROM articles WHERE link=?", (entry.link,))
    if c.fetchone() is None:
        return False
    else:
        return True

'''Makes the content of the post look cleaner'''
def format_to_message(article):
    if article["keyword_filter"].upper() in (article["article"].title).upper():
        article_title = article["article"].title
        article_link = article["article"].link
        article_content = str(article["article"].content[0].value) #extract_content(str(article["article"].content[0].value))
        # Truncates the content if it exceeds the limit set
        if len(article_content) > CONTENT_SIZE:
            article_content = f"{article_content[:CONTENT_SIZE]}..."
        message = create_embed(article_title, article_link, article_content)
    else:
        message = NO_EXECUTE
    return message

'''Extracts the content from the HTML'''
def extract_content(html_text):
    only_div_tags = SoupStrainer("div")
    div_text = BeautifulSoup(html_text, "html.parser", parse_only=only_div_tags).prettify()
    soup = BeautifulSoup(div_text, 'html.parser')
    text = re.sub(' +', ' ', soup.get_text().replace('\n', ' '))[1:]
    return text

'''Creates embed'''
def create_embed(article_title, article_link, article_content):
    embed = discord.Embed(title=article_title[:256], url=article_link, description=article_content, color=discord.Colour.from_str(EMBED_COLOR), timestamp=datetime.now())
    return embed

'''Saves the article in the databse so it doesn't post it on the discord channel again'''
def record_article_in_db(article):
    today_date = datetime.today().replace(tzinfo=timezone.utc)
    c.execute("INSERT INTO articles (title, link, date) VALUES (?, ?, ?)", (article.title, article.link, datetime.today().strftime('%Y-%m-%d')))
    connection.commit()

'''Deletes old articles from the database'''
@tasks.loop(hours=24)
async def delete_old_articles():
    delete_before_date = (datetime.now() - timedelta(days=LAST_ARTICLE_RANGE)).strftime('%Y-%m-%d')
    c.execute("DELETE FROM articles WHERE date < ?", (delete_before_date,))
    connection.commit()
    print(f'Articles older than {delete_before_date} have been deleted.')

'''The bot starts looping the task once it's connected'''
@bot.listen()
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    post_new_articles.start()
    delete_old_articles.start()

'''Starts the bot so it connects to discord'''
if __name__ == "__main__":
    bot.run(TOKEN)
