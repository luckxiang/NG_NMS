'''
Created on May 27, 2013

@author: me
'''

from vsat import console
import re
from itertools import izip

def get_output():
    tnvsat = console.Grab('192.168.140.76', 1014, 3)
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
            channels_values.append([re.findall('\d+.\d+', line)[0], line.split('<')[1].strip('>')])
            
    
    for line in izip(channels_keys, channels_values):
        print line
if __name__ == '__main__':
    get_output()
    pass