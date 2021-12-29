from discord.ext import commands
from pymongo import MongoClient

from config.settings import (
    MONGO_DB_NAME,
    MONGO_HOST,
    MONGO_PORT
)
from utils.discord import (
    generate_verification_code,
    send_embed,
    send_verification_message
)
from utils.thenewboston import is_valid_account_number

bot = commands.Bot(command_prefix='>')
#DB
mongo = MongoClient(MONGO_HOST, MONGO_PORT)
database = mongo[MONGO_DB_NAME]

#collections
USERS = database['users']

async def register(ctx, account_number):
    """
    >register 8b9706ccfcaa58b20208a7121f869d9429d63cd90c4b6a380ce91f2b3132b05a
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

def handle_registration(*, registration):
    """
    Ensure account number is not already registered
    Create a new users or update account number of existing user
    """

    discord_user_id = registration['_id']
    account_number_registered = bool(USERS.find_one({'account_number': registration['account_number']}))

    if not account_number_registered:
        existing_user = USERS.find_one({'_id': discord_user_id})

        if existing_user:
            USERS.update_one(
                {'_id': discord_user_id},
                {
                    '$set': {
                        'account_number': registration['account_number']
                    }
                }
            )
        else:
            USERS.insert_one({
                '_id': discord_user_id,
                'account_number': registration['account_number'],
                'balance': 0
            })

    REGISTRATIONS.delete_one({'_id': discord_user_id})