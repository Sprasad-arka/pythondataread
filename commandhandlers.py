COMMAND_HANDLER_R_W_BYTE_POS=2
COMMAND_HANDLER_WRITE_CMD = True
COMMAND_HANDLER_READ_CMD = False
COMMAND_HANDLER_ACTIVE_MODE = 0x01
COMMAND_HANDLER_ACTIVE_DC = 0x07
COMMAND_HANDLER_ACTIVE_DC_MSB = 0x00

#*****************************************************************************
# Define phase for caliberation Default 1 phase
COMMAND_HANDLER_PhaseA = 0x01
#********************************************************************************/

#*******************************************************************************
# Define used to identify packet as EM GUI Design Center packet
#*******************************************************************************/
COMMAND_HANDLER_EM_GUI_ID_BYTE= 0x04
#/*******************************************************************************
#*  EM GUI Design Center Configuration packet
#*******************************************************************************/
COMMAND_HANDLER_CONFIG_MODE=0x01
COMMAND_HANDLER_APP_VERSION=0x02
COMMAND_HANDLER_CALIBRATION =0x02
COMMAND_HANDLER_REQ_CALIB_VALUES=0x03
COMMAND_HANDLER_ADC_BUFFER_SIZE=0x04
#// Command 0x05-0x7F  are reserved for future configuration commands

#/*******************************************************************************
#* EM GUI Design Center Result packet
#*******************************************************************************/
COMMAND_HANDLER_VRMS_ID=    0x80
COMMAND_HANDLER_IRMS_ID=    0x81
COMMAND_HANDLER_VPEAK_ID=   0x82
COMMAND_HANDLER_IPEAK_ID=   0x83
COMMAND_HANDLER_POWER_FACTOR_ID=0x84
COMMAND_HANDLER_FREQUENCY_ID=   0x85
COMMAND_HANDLER_ACTIVE_POWER_ID=0x86
COMMAND_HANDLER_REACTIVE_POWER_ID=0x87
COMMAND_HANDLER_APPARENT_POWER_ID=0x88
COMMAND_HANDLER_ACTIVE_ENERGY_ID=0x89
COMMAND_HANDLER_REACTIVE_ENERGY_ID=0x8A
COMMAND_HANDLER_APPARENT_ENERGY_ID=0x8B
#// Command 0x8C-0xAF  are reserved for future result commands

#/*******************************************************************************
#*  EM GUI Design Center Calibration packet
#*******************************************************************************/
COMMAND_HANDLER_CALIB_VALUES= 0xB0
COMMAND_HANDLER_CALIB_PHASE=0xB1
COMMAND_HANDLER_CALIB_SAVE=0xB2
#// Command 0xB3-0xFF  are reserved for future calibration commands

#/*******************************************************************************
#*  EM GUI Calibration Request Flag Values for COMMAND_HANDLER_REQ_CALIB_VALUES
#*******************************************************************************/
COMMAND_HANDLER_CALIB_REQ_IDLE=0x00
COMMAND_HANDLER_CALIB_REQ_IN_PROGRESS=0x01
COMMAND_HANDLER_CALIB_REQ_COMPLETED=0x02

def del_my_list(k,length):
    for i in range(0,length):
        k.pop(0)

