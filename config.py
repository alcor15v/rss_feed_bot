# Bot Token
TOKEN = "Here you put the Token"

# Channel ID
CHANNEL_ID = 0

# Update interval for how often the bot is supposed to check if a new entry in the RSS feed exists (in Minutes)
UPDATE_INTERVAL = 1.0

# How far a new entry in the RSS feed can can be published in the past before being ignored (in Days)
LAST_ARTICLE_RANGE = 5

# Add the RSS feeds here, and the keyword (optional)
RSS_FEEDS = [
    {
        "url": "",
        "keyword_filter": ""
    }
]

# Maximum number of characters to display from the body of each post
CONTENT_SIZE = 350

# The message the bot should send if a post has no body
EMPTY_BODY = '_ _'

# Color of the embed
EMBED_COLOR = '#13224F'