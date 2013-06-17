'''
Created on May 27, 2013

@author: me
'''

from vsat import console
import re
from itertools import izip
from ConfigParser import SafeConfigParser
import time

parser = SafeConfigParser()
parser.read('configs/dlf.ini')
serial = parser.getint('Connect', 'serial')

print
if serial:
    from dlf.dlfserial import *
    print 'status:\> connection over SERIAL!'
else:
    from dlf.dlftcp import *
    print 'status:\> connection over TCP!'

def change_dlf_ini(section = 'DefaultsChng', **channels):
        '''
        Changing DLF ini file parameters.
        '''
        for channel, value in channels.items():
            print 'status:\> changing: %s = %s' % (channel, value)
            parser.set(section, channel, value)
        with open('configs/dlf.ini', 'w') as fp:
            parser.write(fp)

def get_vsat_channels(vsat_ip, vsat_port, timeout):
    '''
    Get vsat channels output
    '''
    
    tnvsat = console.Grab(vsat_ip, vsat_port, timeout)
    command = 'rsp pwr_loop get telem'
    stop_pattern = 'abc123'
    output = tnvsat.grab(command, stop_pattern)
    channels_values = []
    channels_keys = []
    for line in output.split('\n'):
        line = line.strip('\r').strip('\t')
        if 'target' in line:
            channels_keys.append(line.strip(':'))
            pattern = re.findall('\d+.\d+', line)
            if pattern: 
                channels_values.append(re.findall('\d+.\d+', line)[0])
            else:
                channels_values.append(0)
        if 'TS Id' in line:
            channels_keys.append(line)
        if 'Total Power' in line:
            channels_values.append(re.findall('\d+.\d+', line)[0])
            
    channels = []
    for line in izip(channels_keys, channels_values):
        channels.append(line)
    
    # return values for available channels.
    return channels

def dlf_controller(channel_number, channel_name, *channels, **vsat):
    '''
    DLF controller.
    '''
    
    # cycle until get needed channel.
    value = 10
    channel_number = int(channel_number)
    while True:
        print
        # getting all vsat channels.
        all_channels = get_vsat_channels(**vsat)
        # getting referince value.
        ref_ch = float(all_channels[0][1])

        # cycle until channel set.
        while not ref_ch:
            # getting all vsat channels.
            all_channels = get_vsat_channels(**vsat)
            # getting referince value.
            ref_ch = float(all_channels[0][1])
            seconds = 10
            print 'info:\> wait next [%d] sec' % seconds
            time.sleep(seconds)
        
        # getting only trf channels
        trf_channels = []
        trf_channels_param = []
        for channel in all_channels:
            if 'TRF' in channel[0]:
                trf_channels.append(channel[1])
                trf_channels_param.append(channel[0])

        # Channel number is set to last trf channel.
        if channel_number > len(trf_channels):
            channel_number = len(trf_channels) - 1
        
        # handle first channel.
        this_ch = float(trf_channels[channel_number])
        
        print 'status:\> trf_channels:', trf_channels, 'ref_ch:', ref_ch 
        
        if channel_number == 0:
            value += (int(round(float(ref_ch), 0)) - int(round(float(this_ch), 0)))/2 + 2
            print 'status:\> first channel:', channel_number
            next_ch = float(trf_channels[channel_number + 1])
            if ref_ch > this_ch and ref_ch < next_ch:
                print 'status:\> finished!'
                return trf_channels_param[channel_number]
        
        # handle bounded channels.
        if channel_number != 0 and channel_number != len(trf_channels)-1:
            value += (int(round(float(ref_ch), 0)) - int(round(float(this_ch), 0)))/2 + 2
            print 'status:\> bounded channel:', channel_number
            next_ch = float(trf_channels[channel_number + 1])
            if ref_ch > this_ch and ref_ch < next_ch:
                print 'status:\> finished!'
                return trf_channels_param[channel_number]
        
        # handle last channel.
        if channel_number == len(trf_channels)-1:
            value += (int(round(float(ref_ch), 0)) - int(round(float(this_ch), 0)))/2 + 2
            print 'status:\> last channel:', channel_number
            if ref_ch > this_ch:
                print 'status:\> finished!'
                return trf_channels_param[channel_number]

        print
        # changing ini file values.
        ini_channels = {}
        ini_channels[channel_name] = str(value)
        change_dlf_ini(**ini_channels)
        
        # send data to DLF.
        data = Dlf()
        data.DLF_Set_Defaults()
        seconds = 20
        print 'status:\> wait [%d] sec' % seconds
        time.sleep(seconds)
        
def dlf_show():
    '''
    Show DLF ini file parameters.
    '''
    for section_name in ['Connect', 'Action', 'DefaultsComp', 'DefaultsChng', 'DefaultsCnst']:
        print
        print '[%s]' % section_name
        for name, value in parser.items(section_name):
            print name, '=', value
            
def dlf_check():
    '''
    Check DLF connection.
    '''
    if serial:
        ser = serial.Serial()
        ser.baudrate = parser.getint('Connect', 'serial_baudrate')
        ser.port = parser.get('Connect', 'serial_port')
        ser.open()
        print
        print 'status:\>', ser
        print 'status:\> checking serial port:', ser.port
        print 'status:\> port open:', ser.isOpen()
        print 'status:\> closing port:', ser.port
        ser.close()
        print 'status:\> port open:', ser.isOpen()
    else:
        print



def dlf_set():
    '''
    Set DLF Defaults.
    '''
    print 'status:\> setting DLF defaults.'
    data = Dlf()
    data.DLF_Set_Defaults()
    print 'status:\> finished!'

def dlf_setup():
    '''
    Set DLF Defaults.
    '''
    print
    print 'status:\> setting DLF defaults.'
    data = Dlf()
    data.DLF_Set_Up()
    print 'status:\> finished!'

if __name__ == '__main__':
    '''
    Main program.
    '''
#     vsat = dict(vsat_ip = '192.168.140.76', vsat_port = 1014, timeout = 3)
#     
#     for channel_number in range(3):
#         channel_name = 'INB4'
#         dlf_controller(channel_number, channel_name, **vsat)
    dlf_show()
    pass

