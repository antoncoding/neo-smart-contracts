from boa.interop.Neo.Blockchain import GetHeader, GetHeight
from boa.interop.Neo.Header import GetTimestamp

def Main():
    current_height = GetHeight()
    currentBlock = GetHeader(current_height)
    time = currentBlock.Timestamp
    return time
