# Discord RSS Bot
A lightweight self-hosted Discord bot that checks RSS feeds for new posts and shares them in a designated Discord channel. It can also filter posts based on keywords in the title. While it should work with any RSS feed, it's been tested mainly with Reddit feeds.

## What It Does
- Periodically scans the RSS feed for new posts.
- Sends matching posts as an embed message to a designated Discord channel.
- Works in one channel on one server.

## Example Output
Here's an example of the embed message the bot sends:

![Example Embed](https://github.com/alcor15v/rss_feed_bot/blob/main/example_embed.png?raw=true)

## Prerequisites
- Python 3.8 or higher
- Permissions to manage bots and access the desired Discord channel

## How to Set It Up
1. **Create a Discord Bot:**
    - Go to [Discord's Developer Portal](https://discord.com/developers/docs/intro) and create a bot.
    - Invite the bot to your server (make sure to give it the right permissions).

2. **Prepare the `config.py` file:** Copy the provided `config.py` template and update the following:
    - **Bot token:** The token generated in the Developer Portal.
    - **Channel ID:** Right-click a channel in Discord and select "Copy ID".
    - **RSS feed URL:** The URL of the RSS feed you want to track.
    - **Optional settings (if you don't have any prefferences, leave the default values):**
      - Keyword filter: The keyword you want to filter posts by. If no keywords are needed, use an empty string.
      - Update interval: How often to check for new posts, in minutes.
      - Last article range: How far a new entry in the RSS feed can can be published in the past before being ignored, in days.
      - Content size: The maximum number of characters to display from the body of each post.
      - Empty body: The message the bot should send if a post has no body.
      - Embed color: The hexadecimal color code for the embed message.

3. **Install dependencies:** Run `pip install -r requirements.txt` to install required Python libraries.

4. **Make sure `main.py` and `config.py` are in the same directory.**

5. **Run `main.py`.**

---

If you'd like additional features or run into issues, feel free to drop a note in the Issues section!

## Credits
https://hansimcklaus.iwr.sh/post/how-to-create-a-simple-rss-bot-for-discord/
