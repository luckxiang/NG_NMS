import pycurl
import cStringIO
import ConfigParser
import sys
from time import sleep

line_print_speed = 0.2

class Ngnms:
    '''
    NGNMS.
    '''
    ngnms_data = None
    def __init__(self, **ngnms_info):
        '''
        NGNMS initialization
        '''
        config = ConfigParser.RawConfigParser()
        config.read('configs/ngnms.cfg')
        self.working_point = {
        'OB symbol rate'                : config.get('NGNMS OIDS', 'OB symbol rate'),
        'OB mode code'                  : config.get('NGNMS OIDS', 'OB mode code'),
        'RTN Channels Frequency Plan'   : config.get('NGNMS OIDS', 'RTN Channels Frequency Plan'),
        'IB symbol rate'                : config.get('NGNMS OIDS', 'IB symbol rate'),
        'IB mode code'                  : config.get('NGNMS OIDS', 'IB mode code'),
        'Dynamic/Static'                : config.get('NGNMS OIDS', 'Dynamic/Static'),
        'Number of Channels'            : config.get('NGNMS OIDS', 'Number of Channels'),
        'Symbol Rate'                   : config.get('NGNMS OIDS', 'Symbol Rate')
        #'IB number of ATM'              : config.get('NGNMS OIDS', 'IB number of ATM'),
        #'IB Preamble'                   : config.get('NGNMS OIDS', 'IB Preamble')
        }

#        self.ngnms_host = ngnms_info.get('URL')
#         self.ngnms_login = {'ngnms_user': ngnms_info.get('User'),
#                             'ngnms_password': ngnms_info.get('Password')}
#         print 'step:\> Connecting to:', self.ngnms_host
#         print 'info:\> auth:', self.ngnms_login
#         self.ngnms_info = ngnms_info

        self.ngnms_host = config.get('NGNMS AUTH', 'host')
        self.ngnms_login = {'ngnms_user': config.get('NGNMS AUTH', 'user'),
                            'ngnms_password': config.get('NGNMS AUTH', 'password')}
        print 'step:\> Connecting to:', self.ngnms_host
        print 'info:\> auth:', self.ngnms_login
        self.ngnms_info = ngnms_info

    def connect(self):
        '''
        Connect to NGNMS server
        '''

        host_url = self.ngnms_host + '/login'

        c = pycurl.Curl()
        c.setopt(c.URL, host_url)
        c.setopt(pycurl.TIMEOUT, 10)
        
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.POSTFIELDS, 'j_username={ngnms_user}&j_password={ngnms_password}'.format(**self.ngnms_login))
        c.setopt(pycurl.COOKIEJAR, 'data/ngnms.cookie')
        
        # c.setopt(c.VERBOSE, True)

        c.setopt(pycurl.SSL_VERIFYPEER, 0);
        session = c
        return session

    def get_config(self, url):
        '''
        Get NGNMS devices configuration.
        '''
        
        c = self.connect()
        data = cStringIO.StringIO()
        log = cStringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, log.write)
        try:
            c.perform()
        except Exception as e:
            print e
            sys.exit()
        
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, data.write)
        
        try:
            c.perform()
            print 'status:', c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
        except Exception as e:
            print e
            sys.exit()
        data = data.getvalue()
        c.close()
        self.ngnms_data = data
        return data
    
    def put_config(self, url, ngnms_data):
        '''
        Upload data to NGNMS with PUT command.
        '''
        c = self.connect()
        indata = cStringIO.StringIO(ngnms_data)
        response = cStringIO.StringIO()
        try:
            c.perform()
        except Exception as e:
            print e
            sys.exit()

        headers = ['Content-Type: application/json', 'Expect:']
        c.setopt(pycurl.HTTPHEADER, headers)
        c.setopt(pycurl.PUT, 1)
        c.setopt(pycurl.READFUNCTION, indata.read)
        c.setopt(pycurl.URL, url)
        
        c.setopt(pycurl.WRITEFUNCTION, response.write)
        try:
            c.perform()
        except Exception as e:
            print e
        response = response.getvalue()
        c.close()
        print response

    def change_values(self, ngnms_data, testcase):
        '''
        Changing data values.
        '''
        from const import data

        # get only old values.
        new_data = []
        for line in ngnms_data:
            if line.get('oid') not in [self.working_point.get(key) for key in self.working_point.keys()]:
                new_data.append(line)

        # add new values.
        for key in sorted(testcase.keys()):
            index = key.split('_')
            if self.working_point.get(index[0]) != None:
                line = {}
                line['value'] = testcase.get(key)
                line['oid'] = self.working_point.get(index[0])
                if len(index) == 2:
                    line['instance'] = index[1]
                else:
                    line['instance'] = '0'
                if index[0] in data.keys():
                    line['value'] = str(data.get(index[0]).get(testcase.get(key)))
                new_data.append(line)

        # print table with old and new values.
        lenght = 99 
        print '-'*lenght
        print '|   {0:^30}   |   {1:^12} |   {2:^15}   |   {3:^15}   |'.format('OID', 'Instance', 'Old', 'New')
        print '-'*lenght
        for line in new_data:
            for item in ngnms_data:
                if line.get('oid') == item.get('oid') and line.get('instance') == item.get('instance'): 
                    old_data = item.get('value')
                    break
                else:
                    old_data = '-'
            print '|   {0:30}   |   {1:12} |   {2:15}   |   {3:15}   |'.format(line.get('oid'), line.get('instance'), old_data, line.get('value'))
        print '-'*lenght

        return new_data

    def set_ngnms_working_point(self, testcase):
        '''
        Set NGNMS working point
        '''
        folder = {'id': None}
        network_url = self.ngnms_host + '/navigation/statustree/network'
        data = self.get_config(network_url)
        data = data.replace("false", "False")

        # transform json to python object.
        ngnms_data = eval(data)

        network_segment_names = {}
        for teleport in ngnms_data.get('subFolders'):
            for satellite in teleport.get('subFolders'):
                for cluster in satellite.get('subFolders'):
                    for ns in cluster.get('subFolders'):
                        network_segment_names[ns.get('name')] = ns.get('_id')
 
        # Search for correct Network Segment.
        for ns in network_segment_names.keys():
            if ns == self.ngnms_info.get('Name'):
                folder['id'] = network_segment_names[ns]

        if folder.get('id') is None:
            print ("\nERROR: Cannot find network segment name: [%s]!\n"
                   "SOLUTION: Verify network segment name in excel file." % self.ngnms_info.get('Name'))
            print "info:\> Available network segment names on server:"
            for ns in network_segment_names.keys():
                print ' '*5, '{0:25} = {1:5}'.format(ns, network_segment_names[ns])
            print
            sys.exit()

        # url to get data from ngnms
        folder['url'] = self.ngnms_host + '/folders/config'
        # get data from NGNMS.
        url = '{url}/{id}'.format(**folder)
        print 'step:\> getting data:', url
        data = self.get_config(url)

        # getting data ngnms network segment configuration
        ngnms_data = eval(data)
        
        # parse and update data.
        print 'step:\> changing values:'
        ngnms_data = self.change_values(ngnms_data, testcase)

        ngnms_data = str(ngnms_data).replace("'", '"')

        # TODO: put data to NGNMS
        # self.put_config('{url}/{id}'.format(**folder), ngnms_data)

    def check_ngnms(self):
        '''
        Set NGNMS working point
        '''
        ngnms_data = self.ngnms_data
        network_url = self.ngnms_host + '/navigation/statustree/network'
        data = self.get_config(network_url)
        data = data.replace("false", "False")

        # transform json to python object.
        ngnms_data = eval(data)

        print 'step:\> Scanning ngnms network tree ...'
        network_segment_names = {}
        for teleport in ngnms_data.get('subFolders'):
            print '-'*60
            print 'Teleport: %s'.rjust(15) % teleport.get('name')
            for satellite in teleport.get('subFolders'):
                print 'Satellite: %s'.rjust(20) % satellite.get('name')
                for cluster in satellite.get('subFolders'):
                    print 'RF Cluster: %s'.rjust(25) % cluster.get('name')
                    for ns in cluster.get('subFolders'):
                        sleep(line_print_speed)
                        print 'NS: %s'.rjust(30) % ns.get('name')
                        network_segment_names[ns.get('name')] = ns.get('_id')
            print '-'*60

        print "info:\> Available network segments names on server:"
        for ns in network_segment_names.keys():
            sleep(line_print_speed)
            print ' '*5, '{0:25} = {1:5}'.format(ns, network_segment_names[ns])
        print
        # return all NS.
        return network_segment_names
    
if __name__ == '__main__':
    '''
    Main program
    '''
    pass




