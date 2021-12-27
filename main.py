from discord.ext import commands, tasks
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from config.settings import (
    BANK_IP,
    BANK_PROTOCOL,
    BOT_ACCOUNT_NUMBER,
    DISCORD_TOKEN,
    MAXIMUM_CONFIRMATION_CHECKS,
    MONGO_DB_NAME,
    MONGO_HOST,
    MONGO_PORT
)
from utils.discord import generate_verification_code, send_embed, send_verification_message
from utils.network import fetch
from utils.thenewboston import is_valid_account_number

bot = commands.Bot(command_prefix='>')

mongo = MongoClient(MONGO_HOST, MONGO_PORT)
database = mongo[MONGO_DB_NAME]

DEPOSITS = database['deposits']
REGISTRATIONS = database['registrations']
USERS = database['users']

@bot.event
async def on_ready():
    """
    Start polling blockchain
    """
    print('Bot is logged in as {0.user}'.format(bot))


@bot.command()
async def register(ctx, account_number):
    """
    >register a37e2836805975f334108b55523634c995bd2a4db610062f404510617e83126f
    """

    if not is_valid_account_number(account_number):
        await send_embed(
            ctx=ctx,
            title='Invalid',
            description='Invalid account number.'
        )
        return

    user = USERS.find_one({'account_number': account_number})

    if user:
        await send_embed(
            ctx=ctx,
            title='Already Registered',
            description=f'The account {account_number} is already registered.'
        )
        return

    discord_user_id = ctx.author.id
    verification_code = generate_verification_code()

    results = REGISTRATIONS.update_one(
        {'_id': discord_user_id},
        {
            '$set': {
                'account_number': account_number,
                'verification_code': verification_code
            }
        },
        upsert=True
    )

    if results.modified_count:
        await send_embed(
            ctx=ctx,
            title='Registration Updated',
            description=(
                'Your registration has been updated. '
                'To complete registration, follow the instructions sent via DM.'
            )
        )
    else:
        await send_embed(
            ctx=ctx,
            title='Registration Created',
            description=(
                'Registration created. '
                'To complete registration, follow the instructions sent via DM.'
            )
        )

    await send_verification_message(
        ctx=ctx,
        registration_account_number=account_number,
        registration_verification_code=verification_code
    )

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
