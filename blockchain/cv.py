# check deposit confirmation
def check_confirmations():
    """
    Query unconfirmed deposits from database
    Check bank for confirmation status
    """
    unconfirmed_deposits = DEPOSITS.find({
        'confirmation_checks': {'$lt': MAXIMUM_CONFIRMATION_CHECKS},
        'is_confirmed': False
    })

    for deposit in unconfirmed_deposits:
        block_id = deposit['block_id']
        url = (
            f'{BANK_PROTOCOL}://{BANK_IP}/confirmation_blocks'
            f'?block={block_id}'
        )

        try:
            data = fetch(url=url, headers={})
            # confirmations = data['count']
            confirmations = 1

            if confirmations:
                # what we wanna do in business logics
                handle_deposit_confirmation(deposit=deposit)

        except Exception:
            pass

        increment_confirmation_checks(deposit=deposit)

# increament confirmation check in DB
def increment_confirmation_checks(*, deposit):
    """
    Increment the number of confirmation checks for the given deposit
    """

    DEPOSITS.update_one(
        {'_id': deposit['_id']},
        {
            '$inc': {
                'confirmation_checks': 1
            }
        }
    )

# deposti confirmation
def handle_deposit_confirmation(*, deposit):
    """
    Update confirmation status of deposit
    Increase users balance or create new user if they don't already exist
    """

    DEPOSITS.update_one(
        {'_id': deposit['_id']},
        {
            '$set': {
                'is_confirmed': True
            }
        }
    )

    registration = REGISTRATIONS.find_one({
        'account_number': deposit['sender'],
        'verification_code': deposit['memo']
    })

    if registration:
        handle_registration(registration=registration)
    else:
        USERS.update_one(
            {'account_number': deposit['sender']},
            {
                '$inc': {
                    'balance': deposit['amount']
                }
            }
        )
