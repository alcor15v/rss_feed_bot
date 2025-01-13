from datetime import datetime
import discord

from config import EMBED_COLOR



'''Creates embed'''
def create_embed(title, link, body):
    embed = discord.Embed(title=title[:256], url=link, description=body, color=discord.Colour.from_str(EMBED_COLOR), timestamp=datetime.now())
    return embed
