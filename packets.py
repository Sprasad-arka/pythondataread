import sys
import checksum
import array as arr
from commandhandlers import del_my_list

from data_extraction import valuesswitch
#def Packet synchronization byte in serial stream
PACKET_SYNC = 0x55

#def Packet blank byte in serial stream
PACKET_BLANK= 0xAA

#def Packet payload start offset
PACKET_PAYLOAD_START=0x03

#def Max packet payload size 62 byte ( 60 byte + 2 checksum bytes)
PACKET_PAYLOAD_MAX_SZ=0x3E

#def Max packet payload size
PACKET_CHECKSUM_SZ=0x02

class packet_struct:
    def __init__(self):  
        self.payloads = []
        self.length = 0
    def reset(self):
        self.payloads = []
        self.length = 0

def Packet_appendChecksum(sourceBuffer, sourceLength):
    checksum_value = checksum.checksum_computechecksum(sourceBuffer, sourceLength)
    sourceBuffer[sourceLength] = (checksum_value & 0x00FF)
    sourceBuffer[sourceLength+1] = (checksum_value >> 8)
    return sourceLength + 2

def Packet_convertToStream(packets_received):
    
    streamPtr = []
    streamPtr.append(PACKET_SYNC)
    streamPtr.append(PACKET_BLANK)
    streamPtr.append(packets_received.length)
    for Payload_values in range(0,packets_received.length - 2):
       streamPtr=Packet_stuffByte(streamPtr, packets_received.payloads[Payload_values])
    checksum_value = checksum.checksum_computechecksum(packets_received.payloads, packets_received.length-2)
    streamPtr = Packet_stuffByte(streamPtr, (checksum_value & 0xFF))
    streamPtr = Packet_stuffByte(streamPtr, (checksum_value >> 8))
    return streamPtr


def pack_to_list(k):
    values_buff = list(k)
    currIndex = -1
    detectedStuffedByte = False
    check_sum = 0
    x=0 
    checksumVerified = False
    packet_parse=[]
    packet_length = 0
    while len(values_buff)!= 0:
        try : 
            if (currIndex < 0):
                if values_buff[0] != PACKET_SYNC:
                    currIndex = -1 
                    del_my_list(values_buff,1)
                elif values_buff[0] == PACKET_SYNC and values_buff[1] == PACKET_BLANK and values_buff[2] <= PACKET_PAYLOAD_MAX_SZ:
                    currIndex = 0
                    packet_length=values_buff[2]-PACKET_CHECKSUM_SZ
                    del_my_list(values_buff,3)
                else :
                    del_my_list(values_buff,3)
                    currIndex = -1
                    continue
        except:
            values_buff.clear()
        if currIndex >= 0 :
            while len(values_buff) != 0: 
                currIndex = -1
                if len(values_buff) >= (packet_length + PACKET_CHECKSUM_SZ):
                    check_sum = values_buff[packet_length]
                    check_sum |= values_buff[packet_length+1] << 8
                    buffer = values_buff[0:packet_length]
                    checksumVerified = checksum.checksum_verifychecksum(buffer,packet_length,check_sum)
                    if checksumVerified :
                        del_my_list(values_buff,1)
                        valueclass= valuesswitch()
                        buffer_parse = values_buff[0:packet_length-1]
                        valueclass.switch(buffer_parse,packet_length)
                        #print(checksumVerified)
                        del_my_list(values_buff,packet_length-1)
                        break
                    else:
                        del_my_list(values_buff,1)
                else :
                    values_buff.clear()

def Packet_stuffByte(next_Position,post_byte):
    next_Position.append(post_byte)
    if(post_byte == PACKET_SYNC):
        next_Position.append(post_byte)
    return next_Position

