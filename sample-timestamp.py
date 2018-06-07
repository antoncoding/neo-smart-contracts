from boa.interop.Neo.Blockchain import GetHeader, GetHeight
from boa.interop.Neo.Runtime import GetTime

def Main():
    current_height = GetHeight()
    currentBlock = GetHeader(current_height)
    time = currentBlock.Timestamp

    # # Or just use GetTime Function
    # time = GetTime()
    return time
