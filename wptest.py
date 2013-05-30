#!/usr/bin/env python
# encoding: utf-8
'''
ngnmstest.py -- run testcases for NGNMS.

ngnmstest.py - run testcases from excel file, 
read configurations tabs for HUB, VSAT,
and store result in excel file.

@author:     Vitalie Ghelbert
@copyright:  2013 Gilat Satellite Networks. All rights reserved.
@contact:    vitalieg
@deffield    updated: Updated
'''

import sys
import os

from vsat import selftest
from optparse import OptionParser
from string import upper
from dlf import vsatdlf

__all__ = []
__version__ = 0.1
__date__ = '2013-03-12'
__updated__ = '2013-03-12'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''
    
    # show help if now arguments provided.
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__
 
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    
    # optional - give further explanation about what the program does
    program_longdesc = "%s - read and run test cases from excel file." % program_name 
    program_license = "Copyright 2013 Gilat"
 
    if argv is None:
        argv = sys.argv[1:]
    #try:
    #setup option parser
    parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
    parser.add_option('-c', '--check', dest='device', type='choice', choices=['hub', 'vsat'], help='''check [hub, vsat]'s status.''')
    parser.add_option('-n', '--name', dest='name', default=None , help='vsat name to check.')
    parser.add_option('-s', '--show', dest='info', type='choice', choices=['all', 'hub', 'vsat', 'test'], help='''show [all, hub, vsat, test]'s info.''')
    parser.add_option('-d', '--disabled', dest='disabled', action='store_true', default=False, help='''show disabled rows only.''')
    parser.add_option('-i', '--in-file', dest='infile', default='data/demo.xls', help='''testcases input file [default: data/demo.xls]''')
    parser.add_option('-r', '--run', dest='run', action='store_true', default=False, help='run one or [default:enabled] test cases')
    parser.add_option('--dlf', dest='dlf', type='choice', choices=['show', 'check', 'set', 'setup'], help='''dlf state [show, check, set, setup]''')
    
    # set defaults
    # parser.set_defaults(infile="test.xls")
    
    # process options
    options, args = parser.parse_args()
        
    # ============== MAIN BODY ============= #
    '''
    Test ngnms.
    '''
    
    try:
        xlfile = options.infile
        with open(xlfile): pass
    except Exception as e:
        print
        print e
        print
        sys.exit()

    # default state.
    state = 'enabled'

    # set disabled value.
    if options.disabled:
        state = 'disabled'

    # change states if name provided.
    if options.name != None:
        states = ['enabled', 'disabled']
    else:
        states = [state]
    # check hub.
    if options.device == 'hub':
        selftest.check(xlfile, state, options.device)
    # check vsat.
    elif options.device == 'vsat':
        for state in states:
            selftest.check(xlfile, state, options.device, options.name)
    # show all enabled and disabled.
    elif options.info == 'all':
        states = [state]
        selftest.show(xlfile, None, None, *states)
    # show hub info.
    elif options.info == 'hub':
        selftest.show(xlfile, upper(options.info), options.name, *states)
    # show vsat info.
    elif options.info == 'vsat':
        selftest.show(xlfile, upper(options.info), options.name, *states)
    # show tests info.
    elif options.info == 'test':
        selftest.show(xlfile, 'TESTCASES', options.name, *states)
    # run tests.
    elif options.run:
        selftest.run(xlfile, states, options.name)
    # show dlf ini file parameters.
    elif options.dlf == 'show':
        vsatdlf.dlf_show()
    # check dlf.
    elif options.dlf == 'check':
        vsatdlf.dlf_check()
    # set dlf.
    elif options.dlf == 'set':
        vsatdlf.dlf_set()
    # setup dlf.
    elif options.dlf == 'setup':
        vsatdlf.dlf_setup()
    else:
        print 
        print "Help: %s -h|--help" % program_name
        print

# #        ============ END MAIN BODY =============== #
#     except Exception, e:
#         indent = len(program_name) * " "
#         sys.stderr.write(program_name + ": " + repr(e) + "\n")
#         sys.stderr.write(indent + "  for help use --help")
#         return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'test_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
    
    