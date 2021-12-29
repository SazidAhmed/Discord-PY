#query blockchain and check deposit
def check_deposits():
    """
    Fetch bank transactions from bank
    Insert new deposits into database
    """

    next_url = (
        f'{BANK_PROTOCOL}://{BANK_IP}/bank_transactions'
        f'?recipient={BOT_ACCOUNT_NUMBER}'
        f'&ordering=-block__created_date'
    )

    while next_url:
        data = fetch(url=next_url, headers={})
        bank_transactions = data['results']
        next_url = data['next']

        for bank_transaction in bank_transactions:

            try:
                DEPOSITS.insert_one({
                    '_id': bank_transaction['id'],
                    'amount': bank_transaction['amount'],
                    'block_id': bank_transaction['block']['id'],
                    'confirmation_checks': 0,
                    'is_confirmed': False,
                    'memo': bank_transaction['memo'],
                    'sender': bank_transaction['block']['sender']
                })
            except DuplicateKeyError:
                break

