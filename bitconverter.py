

def check_convert(list_val,length):
    if length == 4 :
        obtained_value=convert8to32bit(list_val)
    if length == 8 :
        obtained_value=convert8to64bit(list_val) 
    if length == 2 :
        obtained_value=convert8to16bit(list_val)
    return obtained_value

def convert8to16bit(list_val):
    return (list_val[1]<<8)|list_val[0]

def convert8to32bit(list_val):
    return ((list_val[3] << 24) | (list_val[2] << 16)|(list_val[1]<<8)|(list_val[0]))

def convert8to64bit(list_val):
    return ((list_val[7] << 56)|(list_val[6] << 48) | (list_val[5] << 40)|(list_val[4]<<32)|(list_val[3] << 24) | (list_val[2] << 16)|(list_val[1]<<8)|(list_val[0]))

