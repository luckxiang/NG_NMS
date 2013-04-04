# enable/disable debug mode parameters.

debug = {
    'status':True,
    'lines':{
        # range: {0,1}
        # default: 0
        'OB Migration Remove From LB':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.20', 
             'value':'0', 
             'instance':'0'},

        # range: {0,1}
        # default: 0
        'Allow Update OB Migration Parameters':
            {'oid':'1.3.6.1.4.1.7352.3.36.2.14', 
             'value':'1', 
             'instance':'0'},

        # range: {0,1}
        # default: 0
        'Allow Config Changes From Debug Section':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.22', 
            'value':'1', 
            'instance':'0'},

        # range: {0,1}
        # default: 0
        'Use Source For Stream':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.17', 
             'value':'0', 
             'instance':'0'},

        # range 300.000 - 30.000.000
        # default: 28000000
        'Alternate Uplink Center Frequency ':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.13', 
             'value':'28000000', 
             'instance':'0'},

        # range 300.000 - 30.000.000
        # default: 28000000
        'For NE Uplink Center Frequency ':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.15', 
             'value':'28000000', 
             'instance':'0'},

        # range 300.000 - 60.000.000
        # default: 45000000
        'For NE Symbol Rate ':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.16', 
             'value':'45000000', 
             'instance':'0'},

#         # range 1.000.000 - 30.000.000
#         default: 27000000
#         'For NE RFT Uplink LO':
#            {'oid':'1.3.6.1.4.1.7352.3.36.4.21', 
#         'value':'27000000', 
#         'instance':'0'},

        # range 300.000 - 60.000.000
        # default: 45000000
        'Alternate Symbol Rate ':
            {'oid':'1.3.6.1.4.1.7352.3.36.4.14', 
             'value':'45000000', 
             'instance':'0'},

        # range 3.000.000 - 30.000.000
        # default: empty
        #'Source Uplink Center Frequency ':
        #    {'oid':'1.3.6.1.4.1.7352.3.36.4.18', 'value':'', 'instance':'0'},

        # range 300.000 - 60.000.000
        # default: empty
        #'Source Symbol Rate ':
        #    {'oid':'1.3.6.1.4.1.7352.3.36.4.19', 'value':'', 'instance':'0'},

        # range 1.000.000 - 30.000.000
        # default: empty
        #'Source RFT Uplink LO':
        #    {'oid':'1.3.6.1.4.1.7352.3.36.4.23', 'value':'', 'instance':'0'}
    }
}