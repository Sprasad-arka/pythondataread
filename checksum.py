def checksum_computechecksum(buffer,length):
    checksum =0
    for i in range(0,length):
        checksum += buffer[i]
    return checksum

def checksum_verifychecksum(buffer,length,checksum):
    calcChecksum = checksum_computechecksum(buffer, length)
    if calcChecksum == checksum:
        return True
    else:
        return False
