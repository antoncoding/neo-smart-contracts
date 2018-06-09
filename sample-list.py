from boa.interop.Neo.Runtime import CheckWitness, Serialize, Deserialize
from boa.interop.Neo.Storage import GetContext, Put, Delete, Get

def Main():
    ctx = GetContext()

    # Basic List Operation
    sample_list = ['a', 'b', 'c']
    sample_list.append('d')

    # serialized this list data structure
    serialized_list = Serialize(sample_list)
    # Put into storage
    Put(ctx, 'storage_key', serialized_list)

    # Take out from Storage with the same key
    out = Get(ctx, 'storage_key')
    # Unserialize it
    unserialized_list = Deserialize(out)

    # Remove Item 'a' From List
    nl = remove_from_list(unserialized_list, 'a')
    # Now it's back to normal list object
    print(unserialized_list[3])
    # [SmartContract.Runtime.Log] [b'd']

    return len(nl)

def remove_from_list(target_list, item):
    returnlist = []
    for i in target_list:
        if i != item:
            returnlist.append(i)
    return returnlist
