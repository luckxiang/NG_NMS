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
        # 'OB symbol rate'                : config.get('NGNMS OIDS', 'OB symbol rate'),
        'OB mode code'                  : config.get('NGNMS OIDS', 'OB mode code'),
        'Most Efficient MODCOD'           : config.get('NGNMS OIDS', 'Most Efficient MODCOD'),
        'RTN Channels Frequency Plan'   : config.get('NGNMS OIDS', 'RTN Channels Frequency Plan'),
        'IB symbol rate'                : config.get('NGNMS OIDS', 'IB symbol rate'),
        'IB mode code'                  : config.get('NGNMS OIDS', 'IB mode code'),
        'Dynamic/Static'                : config.get('NGNMS OIDS', 'Dynamic/Static'),
        'Number of Channels'            : config.get('NGNMS OIDS', 'Number of Channels'),
        'Symbol Rate'                   : config.get('NGNMS OIDS', 'Symbol Rate')
        #'IB number of ATM'              : config.get('NGNMS OIDS', 'IB number of ATM'),
        #'IB Preamble'                   : config.get('NGNMS OIDS', 'IB Preamble')
        }
        self.ob_symbol_rate_oid = config.get('NGNMS OIDS', 'OB symbol rate')

        host_name = ngnms_info.get('URL')
        host_name = host_name.decode()
        self.ngnms_host = host_name.encode('ascii', 'ignore').rstrip('/')
        
        self.ngnms_login = {'ngnms_user': ngnms_info.get('User'),
                             'ngnms_password': ngnms_info.get('Password')}
        self.ngnms_info = ngnms_info

        print 'step:\> Connecting to:', self.ngnms_host
        print 'info:\> [user: {ngnms_user}] [password: {ngnms_password}]'.format(**self.ngnms_login)

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
        print 'step:\> changing data on server ...'
        c = self.connect()
        indata = cStringIO.StringIO(ngnms_data)
        response = cStringIO.StringIO()
        log = cStringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, log.write)
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
            sys.exit()

        response = response.getvalue()
        print 'status:', c.getinfo(pycurl.HTTP_CODE), c.getinfo(pycurl.EFFECTIVE_URL)
        print 'response:', response
        print
        c.close()
        

    def change_values(self, ngnms_data, testcase):
        '''
        Changing data values.
        '''
        from ngnms.ngnmsconst import data
        from ngnms.ngnmsdebug import debug

        # ngnms new data container.
        new_data = []

        # enable/disable parsing debug oids.
        if debug.get('status'):
            # remove old debug data.
            for line in ngnms_data:
                if (line.get('oid') not in [debug.get('lines')[key].get('oid') for key in debug.get('lines').keys()] and
                    line.get('oid') not in [self.working_point.get(key) for key in self.working_point.keys()]):
                    new_data.append(line)
            # adding new debug data.
            for key in debug.get('lines').keys():
                if key in ['For NE Symbol Rate', 'Alternate Symbol Rate', 'Source Symbol Rate']:
                    debug.get('lines')[key]['value'] = testcase['OB symbol rate']
                    new_data.append(debug.get('lines')[key])
                else:
                    new_data.append(debug.get('lines')[key])
        else:
            # get only old values.
            for line in ngnms_data:
                if (line.get('oid') not in [self.working_point.get(key) for key in self.working_point.keys()]):
                    new_data.append(line)

        # add new values.
        for key in sorted(testcase.keys()):
            index = key.split('_')
            if self.working_point.get(index[0]) != None:
                line = {}
                if testcase.get(key) == '': continue
                line['value'] = testcase.get(key)
                line['oid'] = self.working_point.get(index[0])
                if len(index) == 2:
                    line['instance'] = index[1]
                else:
                    line['instance'] = '0'
                # replace testcase value with correct data.
                if index[0] in data.keys():
                    line['value'] = str(data.get(index[0]).get(testcase.get(key)))
                
                new_data.append(line)
                # adding Most Efficient MODCOD
                if index[0] == 'OB mode code':
                    modcod = {}
                    modcod['oid'] = self.working_point.get('Most Efficient MODCOD')
                    modcod['value'] = line.get('value')
                    modcod['instance'] = line.get('instance')
                    # adding most efficient modcod.
                    new_data.append(modcod)

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
            # line print speet do stdout.
            sleep(0.1)
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
        new_ngnms_data = self.change_values(ngnms_data, testcase)

        new_ngnms_data = str(new_ngnms_data).replace("'", '"')

        # put data to NGNMS
        try:
            url = '{url}/{id}'.format(**folder)
            self.put_config(url, new_ngnms_data)
        except Exception as e:
            print e
        
        changed = True
        for line in ngnms_data:
            if (line.get('oid') == '1.3.6.1.4.1.7352.3.36.4.14' and 
                line.get('value') == testcase.get('OB symbol rate')):
                changed = False

        return (changed, url, ngnms_data)

    def check_ngnms(self):
        '''
        Set NGNMS working point
        '''
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




