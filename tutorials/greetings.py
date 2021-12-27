import discord
import random
from config.settings import DISCORD_TOKEN

client = discord.Client()

greetings = ["hello", "hi"]

welcome_message = [
    "Welcome to Techminate!",
    "Welcome",
    "Hi there."
]
#on ready event
@client.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(client))

#cmd events
@client.event
async def on_message(message):
    msg = message.content
    #bot
    if message.author == client.user:
        return
    
    options = welcome_message
    if any(word in msg for word in greetings):
      await message.channel.send(random.choice(options))

    #reactions
    if msg == 'cool':
        await message.add_reaction('\U0001F60E')
    
    #custom cmd
    if msg.startswith('>status'):
        await message.channel.send('You are online.')

#reaction feedback
@client.event
async def on_reaction_add(reaction, user):
    await reaction.message.channel.send(f'{user} reacted with {reaction.emoji}')


client.run(DISCORD_TOKEN)
