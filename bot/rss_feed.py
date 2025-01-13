import feedparser
from datetime import datetime, timedelta, timezone
from bs4 import SoupStrainer, BeautifulSoup
import re

from db import article_in_db
from formatting import create_embed
from config import LAST_ARTICLE_RANGE, RSS_FEEDS, CONTENT_SIZE

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

'''Makes the content of the post look cleaner'''
def extract_data(article):
    if article["keyword_filter"].upper() in (article["article"].title).upper():
        article_title = article["article"].title
        article_link = article["article"].link
        article_content = extract_content(str(article["article"].content[0].value))
        # Truncates the content if it exceeds the limit set
        if len(article_content) > CONTENT_SIZE:
            article_content = f"{article_content[:CONTENT_SIZE]}..."
        message = create_embed(article_title, article_link, article_content)
    else:
        message = ""
    return message

'''Extracts the content from the HTML'''
def extract_content(html_text):
    only_div_tags = SoupStrainer("div")
    div_text = BeautifulSoup(html_text, "html.parser", parse_only=only_div_tags).prettify()
    soup = BeautifulSoup(div_text, 'html.parser')
    text = re.sub(' +', ' ', soup.get_text().replace('\n', ' '))[1:]
    return text
