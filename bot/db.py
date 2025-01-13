from datetime import datetime, timedelta, timezone
import sqlite3

from config import LAST_ARTICLE_RANGE

DATABASE = 'articles.db'

'''Connects to the database and creates the table if it doesn't exist'''
def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (title TEXT, link TEXT, date TEXT)''')
    connection.commit()

'''Verifies if the article is already in the database'''
def article_in_db(entry):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT link FROM articles WHERE link=?", (entry.link,))
        if cursor.fetchone() is None:
            return False
        else:
            return True

'''Saves the article in the databse so it doesn't post it on the discord channel again'''
def record_article_in_db(article):
    today_date = datetime.today().replace(tzinfo=timezone.utc)
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO articles (title, link, date) VALUES (?, ?, ?)", (article.title, article.link, datetime.today().strftime('%Y-%m-%d')))
        connection.commit()

def delete_old_articles():
    delete_before_date = (datetime.now() - timedelta(days=LAST_ARTICLE_RANGE)).strftime('%Y-%m-%d')
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM articles WHERE date < ?", (delete_before_date,))
        connection.commit()
    print(f'Articles older than {delete_before_date} have been deleted.')