from commandhandlers import COMMAND_HANDLER_ACTIVE_DC_MSB, COMMAND_HANDLER_APP_VERSION, COMMAND_HANDLER_CALIB_PHASE, COMMAND_HANDLER_CALIB_SAVE, COMMAND_HANDLER_CALIBRATION, COMMAND_HANDLER_CONFIG_MODE, COMMAND_HANDLER_EM_GUI_ID_BYTE, COMMAND_HANDLER_READ_CMD, COMMAND_HANDLER_WRITE_CMD, COMMAND_HANDLER_PhaseA,COMMAND_HANDLER_REQ_CALIB_VALUES, COMMAND_HANDLER_CALIB_VALUES

def CommandHandler_connection(packet):
    packet.length =7
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_APP_VERSION)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC_MSB)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC_MSB)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC_MSB)
    return packet


def CommandHandler_calibrationMode(packet):
    packet.length = 6
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_CONFIG_MODE)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_CALIBRATION)
    return packet

def CommandHandler_Phasecalibrationconfig(packet):
    packet.length = 6
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_CALIB_PHASE)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    return packet

def CommandHandler_ReqCalibValues(packet):
    packet.length = 6
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_REQ_CALIB_VALUES)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    return packet



def CommandHandler_CalibrationValues(packet,Voltscalevalue,Currscalevalue,Pwrscalevalue,PhAnglescalevalue):
    packet.length = 20
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_CALIB_VALUES)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    print(Voltscalevalue)
    packet.payloads.append(Voltscalevalue[0])
    packet.payloads.append(Voltscalevalue[1])
    packet.payloads.append(Voltscalevalue[2])
    packet.payloads.append(Voltscalevalue[3])
    packet.payloads.append(Currscalevalue[0])
    packet.payloads.append(Currscalevalue[1])
    packet.payloads.append(Currscalevalue[2])
    packet.payloads.append(Currscalevalue[3])
    packet.payloads.append(Pwrscalevalue[0])
    packet.payloads.append(Pwrscalevalue[1])
    packet.payloads.append(Pwrscalevalue[2])
    packet.payloads.append(Pwrscalevalue[3])
    packet.payloads.append(PhAnglescalevalue[0])
    packet.payloads.append(PhAnglescalevalue[1])
    return packet

#0x07,0x04,0xB2,0x01,0x01,0x00,0xB8,0x00
def CommandHandler_saveCalibValues(packet):
    packet.length = 7
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_CALIB_SAVE)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC_MSB)
    return packet

def CommandHandler_activeMode(packet):
    packet.length = 6
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_WRITE_CMD)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    return packet

def CommandHandler_IdleMode(packet):
    packet.length = 6
    packet.payloads.append(COMMAND_HANDLER_EM_GUI_ID_BYTE)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    packet.payloads.append(COMMAND_HANDLER_PhaseA)
    packet.payloads.append(COMMAND_HANDLER_ACTIVE_DC_MSB)
    return packet
