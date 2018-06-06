from boa.interop.Neo.Storage import GetContext, Put, Delete, Get
from boa.builtins import concat

def Main():
    address = 'ARbpKynS2E2dBBrTnAfMjXgf7vsFv7PmZa'
    balance_key = concat(address, '_balance') # ARbpKynS2E2dBBrTnAfMjXgf7vsFv7PmZa_balance
    # Get from Storage
    balance = Get(GetContext(), balance_key)
    if not balance:
        balance = 0

    new_balance = balance + 100
    Put(GetContext(), balance_key, new_balance)

    return new_balance
