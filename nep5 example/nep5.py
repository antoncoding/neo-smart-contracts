from boa.interop.Neo.Runtime import CheckWitness, Notify, GetTrigger
from boa.interop.Neo.Storage import *
from boa.builtins import concat
from token import *


NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom']

def Main(operation, args):
    ctx = GetContext()
    for op in NEP5_METHODS:
        if operation == op:
            return handle_nep5(ctx, operation, args)
    if operation == 'deploy':
        return deploy()
    else:
        print('Unknown Operation.')
        return False


def deploy():
    """
    :param token: Token The token to deploy
    :return:
        bool: Whether the operation was successful
    """
    if not CheckWitness(CONTRACT_OWNER):
        return "Must be owner to deploy"

    if not Get(ctx, 'initialized'):
        # do deploy logic
        Put(ctx, 'initialized', 1)
        Put(ctx, CONTRACT_OWNER, TOKEN_INITIAL_AMOUNT)
        return add_to_circulation(ctx, TOKEN_INITIAL_AMOUNT)

    return 'Deploy Failed'


def handle_nep5(ctx, operation, args):
    if operation == 'name':
        return TOKEN_NAME

    elif operation == 'decimals':
        return TOKEN_DECIMALS

    elif operation == 'symbol':
        return TOKEN_SYMBOL

    elif operation == 'totalSupply':
        return Get(ctx, TOKEN_CIRC_KEY)

    elif operation == 'balanceOf':
        if len(args) == 1:
            return Get(ctx, args[0])

    elif operation == 'transfer':
        if len(args) == 3:
            return do_transfer(ctx, args[0], args[1], args[2])

    elif operation == 'transferFrom':
        if len(args) == 3:
            return do_transfer_from(ctx, args[0], args[1], args[2])

    return False


def do_transfer(ctx, t_from, t_to, amount):

    if amount <= 0:
        return False

    if len(t_to) != 20:
        return False

    # Check if the transfer function is invoked by address owner
    if CheckWitness(t_from):
        if t_from == t_to:
            print("transfer to self!")
            return True

        from_val = Get(ctx, t_from)

        if from_val < amount:
            print("insufficient funds")
            return False

        if from_val == amount:
            Delete(ctx, t_from)

        else:
            difference = from_val - amount
            Put(ctx, t_from, difference)

        to_value = Get(ctx, t_to)
        to_total = to_value + amount
        Put(ctx, t_to, to_total)

        return True
    else:
        print("from address is not the tx sender")
        return False


def do_transfer_from(ctx, t_from, t_to, amount):
    if amount <= 0:
        return False

    available_key = concat(t_from, t_to)

    if len(available_key) != 40:
        return False

    available_to_to_addr = Get(ctx, available_key)

    if available_to_to_addr < amount:
        print("Insufficient funds approved")
        return False

    from_balance = Get(ctx, t_from)

    if from_balance < amount:
        print("Insufficient tokens in from balance")
        return False

    to_balance = Get(ctx, t_to)

    new_from_balance = from_balance - amount

    new_to_balance = to_balance + amount

    Put(ctx, t_to, new_to_balance)
    Put(ctx, t_from, new_from_balance)

    print("transfer complete")

    new_allowance = available_to_to_addr - amount

    if new_allowance == 0:
        print("removing all balance")
        Delete(ctx, available_key)
    else:
        print("updating allowance to new allowance")
        Put(ctx, available_key, new_allowance)
    return True
