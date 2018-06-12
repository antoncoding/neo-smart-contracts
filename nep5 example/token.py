from boa.interop.Neo.Storage import *

TOKEN_NAME = 'ANTON_COIN'
TOKEN_SYMBOL = 'ATN'
TOKEN_DECIMALS = 8
TOKEN_CIRC_KEY = b'in_circulation'
CONTRACT_OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'

TOKEN_TOTAL_SUPPLY = 100000 * 100000000  # 100 thousand total supply * 10^8 ( decimals)
TOKEN_INITIAL_AMOUNT = 25000 * 100000000  # 25 thousand to owners * 10^8

def add_to_circulation(ctx, amount):
    """
    Adds an amount of token to circlulation
    :param amount: int the amount to add to circulation
    """

    current_supply = Get(ctx, TOKEN_CIRC_KEY)

    current_supply += amount
    Put(ctx, TOKEN_CIRC_KEY, current_supply)
    return True
