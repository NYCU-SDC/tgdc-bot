import discord
import requests
import os
from dotenv import load_dotenv

# Load the environment variable from .env file
load_dotenv()

# Discord settings
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Discord bot token
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Discord channel ID

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Telegram bot token
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')  # Telegram chat ID

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Ensure permission to read message content
client = discord.Client(intents=intents)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Failed to send message on Telegram: {response.text}")
    except Exception as e:
        print(f"Exception in Telegram sending: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Avoid bot replying to itself
    if message.author == client.user:
        return

    # Listen only to a specific channel
    if message.channel.id == CHANNEL_ID:
        content = f"<New message from Discord channel {message.channel.name}>\n\n[{message.author}]\n{message.content}"
        print(content)  # Optional: print the message in the console
        send_telegram_message(content)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)