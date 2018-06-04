from boa.interop.Neo.Runtime import CheckWitness, Log
from boa.interop.Neo.Storage import GetContext, Put, Delete, Get
from boa.builtins import concat

from boa.interop.Neo.Blockchain import GetHeader, GetHeight
from boa.interop.Neo.Header import GetTimestamp

from NeonAdUtil import *

def get_current_timestamp():
    current_height = GetHeight()
    currentBlock = GetHeader(current_height)
    current_timestamp = currentBlock.Timestamp
    return current_timestamp


def get_ad_count():
    ad_count_key = "NeonAD.count"
    ad_registered = Get(GetContext(), ad_count_key)
    if ad_registered != None:
        return ad_registered
    return 0


def get_default_content():
    default_content_key = "NeonAD.default"
    default_content = Get(GetContext(), default_content_key)
    return default_content


def update_board_round(board_id):
    owner_key = get_owner_key(board_id)
    content_key = get_content_key(board_id)
    endtime_key = get_endtime_key(board_id)

    highest_bidder_key = get_highest_bidder_key(board_id)
    highest_bid_key = get_highest_bid_key(board_id)
    next_content_key = get_next_content_key(board_id)

    period = Get(GetContext(), get_period_key(board_id))
    current_timestamp = get_current_timestamp()
    round_end = current_timestamp + period

    # update Info
    Put(GetContext(), endtime_key, round_end)

    new_owner = Get(GetContext(), highest_bidder_key)
    Put(GetContext(), owner_key, new_owner)

    new_content = Get(GetContext(), next_content_key)
    Put(GetContext(), content_key, new_content)

    Put(GetContext(), highest_bid_key, 0)

    print('Update Round Completed')


def init_board_info(board_id, creator, period, domain_name):
    # Define All the keys we need for a single board
    period_key = get_period_key(board_id)
    ad_admin_key = get_ad_admin_key(board_id)
    domain_name_key = get_domain_key(board_id)

    Put(GetContext(), period_key, period)
    Put(GetContext(), ad_admin_key, creator)
    Put(GetContext(), domain_name_key, domain_name)

    # Records for next Round
    highest_bid_key = get_highest_bid_key(board_id)
    highest_bidder_key = get_highest_bidder_key(board_id)
    next_content_key = get_next_content_key(board_id)

    # Next Round
    Put(GetContext(), highest_bid_key, 0)
    Put(GetContext(), highest_bidder_key, creator)
    default_content = get_default_content()
    Put(GetContext(), next_content_key, default_content)



def check_expired(board_id):
    current_timestamp = get_current_timestamp()
    board_end_key = get_endtime_key(board_id)
    board_end_timestamp = Get(GetContext(), board_end_key)
    if board_end_timestamp > current_timestamp:
        return False
    return True


def bid_for_board(board_id, bidder, bid, content):
    if bid <= 0:
        ''' and other value checking'''
        return False

    highest_bid_key = get_highest_bid_key(board_id)
    highest_bid = Get(GetContext(), highest_bid_key)
    if bid > highest_bid:
        highest_bidder_key = get_highest_bidder_key(board_id)
        Put(GetContext(), highest_bidder_key, bidder)

        Put(GetContext(), highest_bid_key, bid)

        next_content_key = get_next_content_key(board_id)
        Put(GetContext(), next_content_key, content)
        return True

    else:
        print('Bid Smaller than Current Bid')
        return False


def Main(operation, args):
    """
    Main definition for the smart contracts

    :param operation: the operation to be performed
    :param args: list of arguments.
        args[0] is always sender script hash
    """
    contract_owner = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'
    user_hash = args[0]

    if operation == "GetEndTime":
        board_id = args[1]
        return Get(GetContext(), concat(board_id, ".endtime"))


    # # Everything after this requires authorization
    authorized = CheckWitness(user_hash)
    if not authorized:
        return False
    Log("Authorized")

    if operation == "CreateBoard":
        """
        args[1] is domain name
        args[2] is bid round (second)
        """
        domain_name = args[1]
        period = args[2]

        ad_count = get_ad_count() + 1
        board_id = concat("NeonAD", ad_count)
        Put(GetContext(), "NeonAD.count", ad_count)

        init_board_info(board_id, user_hash, period, domain_name)
        update_board_round(board_id)

        return board_id


    elif operation == "BidForBoard":
        """
        args[1] := board ID
        args[2] := Bid (NEP)
        args[3] := Content
        """

        board_id = args[1]
        bid = args[2]

        expired = check_expired(board_id)
        if expired:
            update_board_round()
            print('Going into next Round')

        content = args[3]
        if bid_for_board(board_id, user_hash, bid, content) == True:
            return 'Bid Placed'
        else:
            return 'Bid Failed'


    elif operation == "SetDefaultContent":
        if CheckWitness(contract_owner):
            ad_content = args[1]
            Put(GetContext(), "NeonAD.default", ad_content)
            return ad_content
        else:
            print('This Function can only be triggered by admin')

    return 'Failed'
