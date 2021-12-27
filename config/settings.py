import os

from dotenv import load_dotenv

load_dotenv()

# Application
MAXIMUM_CONFIRMATION_CHECKS = 20

# thenewboston
BANK_IP = '20.98.98.0'
BANK_PROTOCOL = 'http'
BOT_ACCOUNT_NUMBER = '8c44cb32b7b0394fe7c6a8c1778d19d095063249b734b226b28d9fb2115dbc74'

# Discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Mongo
MONGO_DB_NAME = 'discord-db'
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
