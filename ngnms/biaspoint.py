import pycurl
import cStringIO
import ConfigParser
import sys

class Ngnms:
    '''
    NGNMS.
    '''
    def __init__(self, ngnms_host):
        '''
        NGNMS initialization
        '''
        config = ConfigParser.RawConfigParser()
        config.read('../configs/ngnms.cfg')
        self.working_point = {
        'OB symbol rate'      : config.get('NGNMS OIDS', 'OB symbol rate'),
        'OB mode code'        : config.get('NGNMS OIDS', 'OB mode code'),
        'IB symbol rate'      : config.get('NGNMS OIDS', 'IB symbol rate'),
        'IB mode code'        : config.get('NGNMS OIDS', 'IB mode code'),
        'IB number of ATM'    : config.get('NGNMS OIDS', 'IB number of ATM'),
        'IB Preamble'         : config.get('NGNMS OIDS', 'IB Preamble'),
        'Dynamic channel'     : config.get('NGNMS OIDS', 'Dynamic channel')
        }
        
        self.ngnms_login = {'ngnms_user' : config.get('NGNMS AUTH', 'user'), 
                       'ngnms_password' : config.get('NGNMS AUTH', 'password')}
        self.ngnms_host = ngnms_host

    def connect(self):
        '''
        Connect to NGNMS server
        '''
        c = pycurl.Curl()
        c.setopt(c.URL, self.ngnms_host + '/login')
        c.setopt(pycurl.TIMEOUT, 10)
        
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.POSTFIELDS, 'j_username={ngnms_user}&j_password={ngnms_password}'.format(**self.ngnms_login))
        c.setopt(pycurl.COOKIEJAR, '../data/ngnms.cookie')
        
        c.setopt(c.VERBOSE, True)

        c.setopt(pycurl.SSL_VERIFYPEER, 0);
        session = c
        return session

    def get_config(self, url):
        '''
        Get NGNMS devices configuration.
        '''
        
        c = self.connect()
        data = cStringIO.StringIO()
        try:
            c.perform()
        except Exception as e:
            print e
        
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, data.write)
        
        try:
            c.perform()
        except Exception as e:
            print e
        data = data.getvalue()
        c.close()
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

    def change_values(self, ngnms_data):
        '''
        Changing data values.
        '''
        for item in ngnms_data:
            if item.get('oid') == self.working_point.get('OB symbol rate'):
                item['value'] = testcase.get('OB symbol rate')
            if item.get('oid') == self.working_point.get('OB mode code'):
                item['value'] = testcase.get('OB mode code')
            if item.get('oid') == self.working_point.get('IB symbol rate'):
                item['value'] = testcase.get('IB symbol rate')
            if item.get('oid') == self.working_point.get('IB mode code'):
                item['value'] = testcase.get('IB mode code')
            if item.get('oid') == self.working_point.get('IB number of ATM'):
                item['value'] = testcase.get('IB number of ATM')
            if item.get('oid') == self.working_point.get('IB Preamble'):
                item['value'] = testcase.get('IB Preamble')
            if item.get('oid') == self.working_point.get('Dynamic channel'):
                item['value'] = testcase.get('Dynamic channel')
        return ngnms_data

    def set_ngnms_working_point(self, testcase, ngnms_devices):
        '''
        Set NGNMS working point
        '''
        folder = {'id': None}
        network_url = self.ngnms_host + '/navigation/statustree/network'
        data = self.get_config(network_url)
        data = data.replace("false", "False")
        # transform json to python object.
        ngnms_data = eval(data)
        device = ngnms_data.get('subFolders')[0].get('subFolders')[0].get('subFolders')[0].get('subFolders')

        # Search for correct Network Segment.
        network_segment_names = []
        for index in xrange(len(device)):
            network_segment_names.append(device[index].get('name'))
            if device[index].get('name') == ngnms_devices.get('NS'):
                folder['id'] = device[index].get('_id')
        
        if folder.get('id') is None:
            print ("\nERROR: Cannot find network segment name: [%s]!\r"
                   "INFO: Available network segments names on NGNMS server: %s\r"
                   "SOLUTION: Verify network segment name in B-HUB Sheet from excel file.\n" % (ngnms_devices.get('NS'), repr(network_segment_names)))
            sys.exit()

        # url to get data from ngnms
        folder['url'] = self.ngnms_host + '/folders/config'
        # get data from NGNMS.
        data = self.get_config('{url}/{id}'.format(**folder))

        # getting data ngnms network segment configuration
        ngnms_data = eval(data)

        for item in ngnms_data:
            print item
        # parse and update data.
        ngnms_data = self.change_values(ngnms_data)
#         for item in ngnms_data:
#             if item.get('oid') == self.working_point.get('OB symbol rate'):
#                 item['value'] = '45000000'
        print '='*40
        for item in ngnms_data:
            print item
        ngnms_data = str(ngnms_data).replace("'", '"')
        print ngnms_data
        # TODO: put data to NGNMS
        # self.put_config('{url}/{id}'.format(**folder), ngnms_data)

if __name__ == '__main__':
    '''
    Main program
    '''

    ngnms_host = 'https://172.20.255.1'
#      ngnms_host = 'https://ngnms-server'
    
    data = Ngnms(ngnms_host)
    testcase = {
                'OB symbol rate':'OB symbol rate',
                'OB mode code':'OB mode code',
                'IB symbol rate':'IB symbol rate',
                'IB mode code':'IB mode code',
                'IB number of ATM':'IB number of ATM',
                'IB Preamble':'IB Preamble',
                'Dynamic channel':'Dynamic channel',
                }
    ngnms_devices = {'NS':'NS_2', 'HSP':'HSP1'}
    data.set_ngnms_working_point(testcase, ngnms_devices)




