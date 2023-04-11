# Protocol for the serial port 
import json
import time
import serial
from caliberation_frames import *
from commandhandlers import COMMAND_HANDLER_ACTIVE_DC, COMMAND_HANDLER_ACTIVE_DC_MSB, COMMAND_HANDLER_ACTIVE_MODE, COMMAND_HANDLER_CONFIG_MODE, COMMAND_HANDLER_EM_GUI_ID_BYTE, COMMAND_HANDLER_WRITE_CMD
import math
import packets
from threading import Thread, current_thread
import serial.rs485
global Comm_transmitBuffer ,exsamplepack, fPrevVoltCalibValue, fPrevCurrCalibValue, fPrevPwrCalibValue,  iPrevPhAngleCalibValue ,Voltage_read ,current_read ,power_read ,phase_read ,Ref_volt,Ref_curr,Ref_Powr 
Comm_transmitBuffer = []
fPrevVoltCalibValue = 0
fPrevCurrCalibValue = 0 
fPrevPwrCalibValue = 0
iPrevPhAngleCalibValue=0
Voltage_read = None 
current_read = None
power_read = None
phase_read = None
Ref_volt = 0
Ref_curr = 0
Ref_Powr = 0
Ref_Phase = 60


import sys
from bitconverter import check_convert
import checksum
import array as arr
from commandhandlers import del_my_list
from comm import Voltage_read 
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

                         

def pack_V_I_Pw(k):
    global Voltage_read,current_read,power_read 
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
                        buffer_parse = values_buff[0:packet_length-1]
                        if buffer_parse[0] == 128:
                            packet = packet_length -4 
                            del_my_list(buffer_parse,3)
                            voltage=check_convert(buffer_parse,packet)
                            voltage = round(voltage,4)         
                            Voltage_read=voltage * 0.001
                        if buffer_parse[0] == 129:
                            packet = packet_length -4
                            del_my_list(buffer_parse,3)
                            current=check_convert(buffer_parse,packet)
                            current = round(current,4)         
                            current_read=current * 0.0001
                        if buffer_parse[0] == 134:
                            packet = packet_length-4
                            del_my_list(buffer_parse,3)
                            Power=check_convert(buffer_parse,packet)
                            Power = round(Power,4)         
                            power_read=Power*0.0000001
                        del_my_list(values_buff,packet_length+1)
                   
                        break
                    else:
                        del_my_list(values_buff,1)
                if  Voltage_read !=None and  current_read != None and  power_read != None :
                    break 
                else :
                    values_buff.clear()

class comport_initalize:
    def __init__(self,port,baudrate,timeout,parity):
        self.comport = port
        self.baudrate=baudrate
        self.timeout=timeout
        self.parity=parity
        
def initialize():
    Voltage_read = None
    current_read = None 
    power_read = None 
    phase_read = None 

def comport_setup():
    port = comport_initalize('/dev/ttyAMA1',256000,2,serial.PARITY_NONE)
    return port 


def Comm_writePacket(packet):
    global Comm_transmitBuffer
	# Simply call the write buffer function, passing the packet parameters.
    listes  = (packets.Packet_convertToStream(packet))
    Comm_transmitBuffer = listes.copy()


def CommandHandler_transmitdataenable(packet):
    packet.length = 6
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_CONFIG_MODE)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_MODE)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC_MSB)
    Comm_writePacket(packet)

def comm_ParseCalibValues(bKData):
    bRxData = list(bKData)
    bPrevVoltCalibData=[]
    bPrevCurrCalibData=[]
    bPrevPwrCalibData=[]
    bPrevPhAngleCalibData=[]
    global fPrevVoltCalibValue,fPrevCurrCalibValue,fPrevPwrCalibValue,iPrevPhAngleCalibValue
    if ((bRxData[0] == 0x55) and  (bRxData[1] == 0xAA) and (bRxData[2] == 0x14) and  (bRxData[3] == 0x04) and (bRxData[4] == 0xB0)):
        bPrevVoltCalibData.append(bRxData[7])
        bPrevVoltCalibData.append(bRxData[8])
        bPrevVoltCalibData.append(bRxData[9])
        bPrevVoltCalibData.append(bRxData[10])
        iTemp = (bPrevVoltCalibData[3] << 24 | bPrevVoltCalibData[2] << 16 | bPrevVoltCalibData[1] << 8 | bPrevVoltCalibData[0])
        fPrevVoltCalibValue = iTemp / 16777216
        bPrevVoltCalibData.clear()
        bPrevCurrCalibData.append(bRxData[11])
        bPrevCurrCalibData.append(bRxData[12])
        bPrevCurrCalibData.append(bRxData[13])
        bPrevCurrCalibData.append(bRxData[14])
        iTemp = bPrevCurrCalibData[3] << 24 | bPrevCurrCalibData[2] << 16 |  bPrevCurrCalibData[1] << 8 | bPrevCurrCalibData[0]
        fPrevCurrCalibValue = iTemp / 16777216
        bPrevCurrCalibData.clear()
        bPrevPwrCalibData.append(bRxData[15])
        bPrevPwrCalibData.append(bRxData[16])
        bPrevPwrCalibData.append(bRxData[17])
        bPrevPwrCalibData.append(bRxData[18])
        iTemp = bPrevPwrCalibData[3] << 24 | bPrevPwrCalibData[2] << 16 | bPrevPwrCalibData[1] << 8 | bPrevPwrCalibData[0]
        fPrevPwrCalibValue = float(iTemp) / 1073741824
        bPrevPwrCalibData.clear()
        bPrevPhAngleCalibData.append(bRxData[19])
        bPrevPhAngleCalibData.append(bRxData[20])
        iPrevPhAngleCalibValue = bPrevPhAngleCalibData[1] << 8 | bPrevPhAngleCalibData[0]
        print(iPrevPhAngleCalibValue)
        bPrevPhAngleCalibData.clear()
        return True
    else :
        return False

def convert(iNewValue):
    bNewCalibValue=[]
    iNewValue = iNewValue % 4294967296
    bNewCalibValue.append(int(iNewValue % 256))
    iNewValue = iNewValue / 256
    bNewCalibValue.append(int(iNewValue % 256))
    iNewValue = iNewValue / 256
    bNewCalibValue.append(int(iNewValue % 256))
    bNewCalibValue.append(int(iNewValue / 256))
    return bNewCalibValue

def volt_scalefactor():
    bNewVoltCalibValue=[]
    if Voltage_read == 0.0:
        fNewVoltCalib = 1.0
    else :
        fNewVoltCalib = (Ref_volt/Voltage_read) * fPrevVoltCalibValue
    if fNewVoltCalib > 128 :
        fNewVoltCalib = 127.999999
    iNewVoltValue = fNewVoltCalib * 16777216.0
    bNewVoltCalibValue= convert(iNewVoltValue)
    return bNewVoltCalibValue

def Phase_volt_scalefactor():
    bNewVoltCalibValue=[]
    iNewVoltValue = fPrevVoltCalibValue * 16777216.0
    bNewVoltCalibValue= convert(iNewVoltValue)
    return bNewVoltCalibValue

def current_scalefactor():
    bNewCurrCalibValue=[]
    if current_read == 0.0:
        fNewCurrCalib = 127.9999
    else :
        fNewCurrCalib = ( Ref_curr/current_read) * fPrevCurrCalibValue
    if fNewCurrCalib > 128.0 :
        fNewCurrCalib = 127.9999999
    iNewCurrValue = fNewCurrCalib * 16777216.0
    bNewCurrCalibValue=convert(iNewCurrValue)
    return bNewCurrCalibValue

def Phase_current_scalefactor():
    bNewCurrCalibValue=[]
    iNewCurrValue = fPrevCurrCalibValue * 16777216.0
    bNewCurrCalibValue=convert(iNewCurrValue)
    return bNewCurrCalibValue

def power_scalefactor():
    bPrevPwrCalibData=[]
    if power_read == 0.0: 
        fNewPwrCalib =1.0
    else :
        fNewPwrCalib = ( Ref_Powr/power_read) * fPrevPwrCalibValue
    if fNewPwrCalib > 128.0 :
        fNewPwrCalib= 127.9999999
    iNewPwrValue = fNewPwrCalib * 1073741824
    bPrevPwrCalibData=convert(iNewPwrValue)
    return bPrevPwrCalibData

def Phase_power_scalefactor():
    bPrevPwrCalibData=[]
    iNewPwrValue = fPrevPwrCalibValue * 1073741824
    bPrevPwrCalibData=convert(iNewPwrValue)
    return bPrevPwrCalibData

def Phase_scalefactor():
    bPrevPhAngleCalibData=[]
    iNewPhangleValue = Ref_Phase 
    bPrevPhAngleCalibData.append(int(iNewPhangleValue % 256))
    bPrevPhAngleCalibData.append(int(iNewPhangleValue/ 256))
    return bPrevPhAngleCalibData

def Prev_Phase_scalefactor():
    bPrevPhAngleCalibData=[]
    iNewPhangleValue = iPrevPhAngleCalibValue 
    bPrevPhAngleCalibData.append(int(iNewPhangleValue % 256))
    bPrevPhAngleCalibData.append(int(iNewPhangleValue/ 256))
    return bPrevPhAngleCalibData




def serial_write(ser,transmitBuffer):
    index_list = []
    for index_range in transmitBuffer:
        index_list.append(index_range)
        ser.write(serial.to_bytes(index_list))
        time.sleep(0.15)
        index_list.clear()


if __name__ == '__main__':
    # read file
    with open('statusfile.json', 'r') as myfile:
        data=myfile.read()
        myfile.close()
        # parse file
        obj = json.loads(data)
        calibration_complete=(obj['calibration_status'])
        Ref_volt=(obj['Reference_voltage'])
        Ref_curr=(obj['Reference_Current'])
        Ref_Powr=(obj['Reference_Power'])
        for Phase_values in obj['PhaseCorrection']:
            Phasecalibration_complete = (Phase_values['Phase_calibration_status'])
            Ref_Phase=(Phase_values['Reference_PhaseCor_value'])
    port = comport_setup()
    payload=[]
    ser = serial.Serial(port.comport,port.baudrate,timeout=port.timeout,parity=port.parity,xonxoff=False,dsrdtr=True)
    exsamplepack = packets.packet_struct() 
    #calibration request
    packet_obtained=CommandHandler_IdleMode(exsamplepack)
    Comm_writePacket(packet_obtained)
    serial_write(ser,Comm_transmitBuffer)
    print(Comm_transmitBuffer)
    packets.packet_struct.reset(exsamplepack) 
    bkbuff = bkdata=ser.read_all()
    bkbuff = None
    while calibration_complete == 0 or Phasecalibration_complete == 0:
        for i in range(0,1):
            packet_obtained=CommandHandler_ReqCalibValues(exsamplepack)
            Comm_writePacket(packet_obtained)
            serial_write(ser,Comm_transmitBuffer)
            print(Comm_transmitBuffer)
            packets.packet_struct.reset(exsamplepack)
        while 1:
            bkdata=ser.read_all()
            if len(bkdata)>23:
                print(bkdata)
                if (comm_ParseCalibValues(bkdata)):
                    break
            # print("caliculate the calibration value")
            time.sleep(2)
        print ("voltage_cal",fPrevVoltCalibValue , "Current_cal",fPrevCurrCalibValue,"Phase_cal",iPrevPhAngleCalibValue)
        time.sleep(2)
        if calibration_complete == 0 or Phasecalibration_complete == 0:
            for mode in range(0,1):
                packet_obtained=CommandHandler_calibrationMode(exsamplepack)
                Comm_writePacket(packet_obtained)
                serial_write(ser,Comm_transmitBuffer)
                #print(Comm_transmitBuffer)
                packets.packet_struct.reset(exsamplepack)
                packet_obtained= CommandHandler_Phasecalibrationconfig(exsamplepack)
                Comm_writePacket(packet_obtained)
                serial_write(ser,Comm_transmitBuffer)
                print(Comm_transmitBuffer)
                packets.packet_struct.reset(exsamplepack)
                initialize()
                count_list = 0
                while 1 :
                    count_list +=1
                    if count_list == 6:
                        k=ser.read(size = 11)    
                    elif count_list == 7:
                        k=ser.read(size = 17)
                    else :
                        k=ser.read(size = 13)
                    if len(k)>1:
                        #print(k)                   
                        pack_V_I_Pw(k)
                        if (Voltage_read != None and current_read != None and power_read != None ):
                            break
                if calibration_complete == 0:
                    Obta_Voltscalevalue=volt_scalefactor()
                    Obta_Currscalevalue=current_scalefactor()
                    Obta_Pwrscalevalue=power_scalefactor()
                    Obta_PhAnglescalevalue=Prev_Phase_scalefactor()
                    Phasecalibration_complete = 0
                    print(Obta_Voltscalevalue)
                elif Phasecalibration_complete == 0:
                    Obta_Voltscalevalue=Phase_volt_scalefactor()
                    Obta_Currscalevalue=Phase_current_scalefactor()
                    Obta_Pwrscalevalue=Phase_power_scalefactor()
                    Obta_PhAnglescalevalue=Phase_scalefactor()
                    Phasecalibration_complete =1 
                packet_obtained=CommandHandler_CalibrationValues(exsamplepack,Obta_Voltscalevalue,Obta_Currscalevalue,Obta_Pwrscalevalue,Obta_PhAnglescalevalue)
                Comm_writePacket(packet_obtained)
                print(Comm_transmitBuffer)
                serial_write(ser,Comm_transmitBuffer)
                packets.packet_struct.reset(exsamplepack)
                packet_obtained= CommandHandler_saveCalibValues(exsamplepack)
                Comm_writePacket(packet_obtained)
                serial_write(ser,Comm_transmitBuffer)
                packets.packet_struct.reset(exsamplepack)
                print(Comm_transmitBuffer)
                calibration_complete = 1 
                json_update = {"calibration_status" : 1,"Reference_voltage":Ref_volt,"Reference_Current":Ref_curr,"Reference_Power":Ref_Powr,"PhaseCorrection":[{"Phase_calibration_status": Phasecalibration_complete,"Reference_PhaseCor_value":Ref_Phase}]}
                with open('statusfile.json', 'w') as f:
                    json.dump(json_update, f, ensure_ascii=False)
                    f.close()
        #Comm_writePacket(packet_obtained)
        # time.sleep(50)                   
        # for test in  range(0,1):
        #     serial_write(ser,[0x55,0xAA,0x06,0x04,0x01,0x01,0x01,0x07,0x00])
        #     time.sleep(10)
        #     break       
        time.sleep(5)
    exsamplepack = packets.packet_struct()
    CommandHandler_transmitdataenable(exsamplepack)
    print(Comm_transmitBuffer)
    read_once =0
    while 1:
        if ser.in_waiting == 0 and read_once == 0:
                ser.write(serial.to_bytes(Comm_transmitBuffer))
        try:
                k=ser.read_all()
                if len(k)>1:
                    read_once = 1
                    parsing_thread = Thread(target=packets.pack_to_list, args=(k,))
                    parsing_thread.start()
                    parsing_thread.join()
                time.sleep(0.1)
        except:
            print("Failed to read the serial data")

               
    ser.close

