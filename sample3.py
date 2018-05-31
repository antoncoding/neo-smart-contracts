from boa.interop.Neo.Storage import Get,Put,Delete,GetContext
def Main(operation, addr, value):
    if not is_valid_addr(addr):
        return False

    ctx = GetContext()

    if operation == 'add':
        balance = Get(ctx, addr)
        new_balance = balance + value
        Put(ctx, addr, new_balance)
        return new_balance

    elif operation == 'remove':
        balance = Get(ctx, addr)
        Put(ctx, addr, balance - value)
        return balance - value

    elif operation == 'balance':
        return Get(ctx, addr)

    return False

def is_valid_addr(addr):

    if len(addr) == 20:
        return True
    return False


# Call: neo> build docs/source/example/sample3.py test 070502 02 True False add AG4GfwjnvydAZodm4xEDivguCtjCFzLcJy 3
