import pytz
from bitconverter import check_convert, convert8to16bit, convert8to32bit, convert8to64bit
from commandhandlers import del_my_list
import json 
from datetime import datetime
import math 

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)        
    return val

payload_json = {'voltage':0,'current':0,'voltage_peak':0,'current_peak':0,'Power_factor':0,'Frequency':0,'Active_Power':0,'Reactive_Power':0,'Apparent_Power':0,'Active_Energy':0,'time':0,'Phase_Angle':0}
class valuesswitch:

    def switch(self,para,length):
        self.params =para.copy()
        self.lengths=length-4
        default = None
        return getattr(self,'case_'+ str(para[0]),lambda:default,)()
  
    def case_128(self):
        del_my_list(self.params,3)
        voltage=check_convert(self.params,self.lengths)
        voltage = round(voltage,4)         
        payload_json['voltage']=voltage*0.001
        return None 

    def case_129(self):
        del_my_list(self.params,3)
        current=check_convert(self.params,self.lengths)
        payload_json['current']=current*0.0001
        return None 

    def case_130(self):
        del_my_list(self.params,3)
        vpeak=check_convert(self.params,self.lengths)
        payload_json['voltage_peak']=vpeak*0.001
        return None  
 
    def case_131(self):
        del_my_list(self.params,3)
        Ipeak=check_convert(self.params,self.lengths)
        payload_json['current_peak']=Ipeak*0.0001
        return None 
 
    def case_132(self):
        del_my_list(self.params,3)
        #if self.params[0] != 255 and self.params[1] != 255 and self.params[2] != 255 and self.params[3] != 255:
        powerfactor=check_convert(self.params,self.lengths)
        payload_json['Power_factor']=powerfactor*0.0001
        phase_value = math.acos(powerfactor*0.0001)
        payload_json['Phase_Angle']= phase_value * 57.2957795
        return None 
 
    def case_133(self):
        del_my_list(self.params,3)
        freq=check_convert(self.params,self.lengths)
        freq= round(freq,5)
        payload_json['Frequency']=freq*0.01
        return None 

    def case_134(self):
        del_my_list(self.params,3)
        #if self.params[0] != 255 and self.params[1] != 255 and self.params[2] != 255 and self.params[3] != 255:
        i=7
        test_list=[]
        while self.lengths !=0: 
            test_list.append(self.params[i])
            i-=1
            self.lengths -=1
        res = ''.join(format(x, '02x') for x in test_list)
        #reactive_power = twos_comp(int(test_list,16), 64)
        val = int(res,16)
        if (val & (1 << (64 - 1))) != 0:
            val = val - (1 << 64)
        active_power = val
        payload_json['Active_Power']=active_power * 0.0000001
        return None 
 
    def case_135(self):
        del_my_list(self.params,3)
        i=7
        test_list=[]
        while self.lengths !=0: 
            test_list.append(self.params[i])
            i-=1
            self.lengths -=1
        res = ''.join(format(x, '02x') for x in test_list)
        val = int(res,16)
        if (val & (1 << (64 - 1))) != 0:
            val = val - (1 << 64)
        reactive_power = val
        payload_json['Reactive_Power']=reactive_power * 0.0000001
        return None 
 
    def case_136(self):
        del_my_list(self.params,3)
        #if self.params[0] != 255 and self.params[1] != 255 and self.params[2] != 255 and self.params[3] != 255:
        apparent_power=check_convert(self.params,self.lengths)
        apparent_power= round(apparent_power,5)
        payload_json['Apparent_Power']=apparent_power*0.0000001
        return None 
 
    def case_137(self):
        del_my_list(self.params,3)
        active_energy=check_convert(self.params,self.lengths)
        payload_json['Active_Energy']=active_energy*0.0000000001
        return None 
 
    def case_138(self):
        del_my_list(self.params,3)
        reactive_energy=check_convert(self.params,self.lengths)
        payload_json['reactive_energy']=reactive_energy*0.0000000001
        return None 
 
    def case_139(self):
        del_my_list(self.params,3)
        apparent_energy=check_convert(self.params,self.lengths)
        payload_json['apparent_energy']=apparent_energy*0.0000000001
        dt = datetime.now(pytz.timezone('Asia/Kolkata'))
        payload_json['time']= dt.strftime('%Y-%m-%d %H:%M:%S')

        print(payload_json)
        json_data = json.dumps(payload_json)
        with open('data.json', 'a', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
            f.close()
        return None 
