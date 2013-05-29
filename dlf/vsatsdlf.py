'''
Created on May 27, 2013

@author: me
'''

from vsat import console
import re
from itertools import izip
from ConfigParser import SafeConfigParser

from dlf.dlftcp import *

def change_dlf_ini(section = 'DefaultsChng', **channels):
        '''
        Changing DLF ini file parameters.
        '''
        parser = SafeConfigParser()
        parser.read('../configs/dlf.ini')
        for channel, value in channels.items():
            print 'Changing: %s = %s' % (channel, value)
            parser.set(section, channel, value)
        with open('../configs/dlf.ini', 'w') as fp:
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
            channels_values.append(re.findall('\d+.\d+', line)[0])
        if 'TS Id' in line:
            channels_keys.append(line)
        if 'Total Power' in line:
            channels_values.append(re.findall('\d+.\d+', line)[0])
            
    channels = []
    for line in izip(channels_keys, channels_values):
        channels.append(line)
    
    # return values for available channels.
    return channels

def dlf_controller(channel_number, channel_name, **vsat):
    '''
    DLF controller.
    '''
    # getting all vsat channels.
    all_channels = get_vsat_channels(**vsat)
    ref_ch = all_channels[0][1]

    # getting only trf channels
    trf_channels = []
    for channel in all_channels:
        print channel
        if 'TRF' in channel[0]:
            trf_channels.append(channel[1])
    
    stop = False
    value = 63
    while not stop:
        this_ch = trf_channels[channel_number]
        # handle first channel.
        if channel_number == 0:
            next_ch = trf_channels[channel_number + 1]
            if ref_ch > this_ch and ref_ch < next_ch:
                stop = True
        
        # handle channels between first and last channels.
        if channel_number != 0 and channel_number != len(trf_channels):
            prev_ch = trf_channels[channel_number - 1]
            next_ch = trf_channels[channel_number + 1]
            if ref_ch > prev_ch and ref_ch > this_ch and ref_ch < next_ch:
                stop = True
        
        # handle last channel.
        if channel_number == len(trf_channels):
            if ref_ch > this_ch:
                stop = True
        
        # changing ini file values.
        value -= 5
        channels = dict(channel_name = value)
        change_dlf_ini(**channels)

        # send data to DLF.
        data = DlfTcp()
        data.DLF_Set_Defaults()
        



if __name__ == '__main__':
    '''
    Main program.
    '''
    vsat = dict(vsat_ip = '192.168.140.76', vsat_port = 1014, timeout = 3)
    
    dlf_controller(1, **vsat)
    
        
    channels = {}
    channels['INB2'] = '22'
    section = 'DefaultsChng'
    change_dlf_ini(section, **channels)
    
    pass

