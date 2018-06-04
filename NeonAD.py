from boa.interop.Neo.Runtime import CheckWitness, Log
from boa.interop.Neo.Storage import GetContext, Put, Delete, Get
from boa.builtins import concat

from boa.interop.Neo.Blockchain import GetHeader, GetHeight
from boa.interop.Neo.Header import GetTimestamp


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

def init_board_info(board_id, creator, period, domain_name):
    # Define All the keys we need for a single board
    highest_actual_bid_key = concat(board_id, ".real")
    highest_mask_bid_key = concat(board_id, ".mask")
    period_key = concat(board_id, ".period")
    endtime_key = concat(board_id, ".endtime")
    ad_owner_key = concat(board_id, ".owner")
    highest_bidder_key = concat(board_id, ".bidder")
    domain_name_key = concat(board_id, ".domain")

    current_timestamp = get_current_timestamp()
    first_round_end = current_timestamp + period

    Put(GetContext(), highest_actual_bid_key, 0)
    Put(GetContext(), highest_mask_bid_key, 0)
    Put(GetContext(), period_key, period)
    Put(GetContext(), endtime_key, first_round_end)
    Put(GetContext(), ad_owner_key, creator)
    Put(GetContext(), highest_bidder_key, creator)
    Put(GetContext(), domain_name_key, domain_name)

    return True

def Main(operation, args):
    """
    Main definition for the smart contracts

    :param operation: the operation to be performed
    :type operation: str

    :param args: list of arguments.
        args[0] is always sender script hash
    :param type: str

    :return:
        byterarray: The result of the operation
    """
    user_hash = args[0]
    # domain_owner_key = concat(domain, ".owner")
    # domain_target_key = concat(domain, ".target")
    # # Everything after this requires authorization
    authorized = CheckWitness(user_hash)
    if not authorized:
        Log("Not Authorized")
        return False
    Log("Authorized")

    if operation == "CreateBoard":
        """
        args[1] is domain name
        args[2] is bid round (second)
        """
        # parameters
        domain_name = args[1]
        period = args[2]

        # Create New Board ID
        ad_count = get_ad_count() + 1
        board_id = concat("NeonAD", ad_count)
        Put(GetContext(), "NeonAD.count", ad_count)

        success = init_board_info(board_id, user_hash, period, domain_name)

        return Get(GetContext(), concat(board_id, ".endtime"))



    # This doesn't require authentication
    # if operation == 'GetDomain':
    #     return Get(GetContext(), domain_target_key)


    # if operation == 'RegisterDomain':
    #     if(CheckWitness(owner)):
    #         address = args[2]
    #         Put(GetContext(), domain_owner_key, address)
    #         if len(args) == 4:
    #             target = args[3]
    #             Put(GetContext(), domain_target_key, target)
    #         return True
    #
    # if operation == 'SetDomainTarget':
    #     if CheckWitness(domain_owner_key) or CheckWitness(owner):
    #         # License the product
    #         target = args[2]
    #         Put(GetContext(), domain_target_key, target)
    #         return True
    #
    # if operation == 'DeleteDomain':
    #     if(CheckWitness(owner)):
    #         Delete(GetContext(), domain_owner_key)
    #         Delete(GetContext(), domain_target_key)
    #         return True

    return False
