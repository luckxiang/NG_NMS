__DONE.__

        Automated Testing flow:
        
        1.  Using REST API we export the configuration file {JSON format with OID}.
        2.  From our Excel file with Test Cases we read one line that contains Test Case To Run.
        3.  Changing the value of needed OID with needed values.
        4.  Using REST API, we import back configuration file to NGNMS.
        5.  Checking NGNMS is ready for statistics result.
        6.  Starting SELFTEST Mode.
        7.  Over telnet protocol, we collect result data.
        8.  Storing data into Excel file.
        9.  Go to again to P.1 until go through all Test Cases.


__Usage examples:__

C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py -h__

        Usage: ngnmstest.py [options]
        
        Copyright 2013 Gilat
        
        Options:
          --version             show program's version number and exit
          -h, --help            show this help message and exit
          -c DEVICE, --check=DEVICE
                                check [hub, vsat]'s status.
          -n NAME, --name=NAME  vsat name to check.
          -s INFO, --show=INFO  show [all, hub, vsat, testcases]'s info.
          -d, --disabled        show disabled rows only.
          -i INFILE, --in-file=INFILE
                                testcases input file [default: data/demo.xls]
          -o OUTFILE, --out-file=OUTFILE
                                save result to file [default: data/output.xls]
          -r, --run             run one or [default:enabled] test cases
        
        ngnmstest.py - read and run test cases from excel file.
        
        
__Show all active rows from VSAT Sheet:__
        
C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --show vsat__
        
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                             VSAT : ENABLED
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ------------------------------------------------------------
                           VSAT : V1 : ENABLED
        ------------------------------------------------------------
        Active                                   = X
        Name                                     = V1
        ID                                       = 3001.0
        Console IP                               = 192.168.140.76
        Console PORT                             = 1016.0
        Connection timeout                       = 10.0
        Number of tries                          = 2.0
        Tries timeout                            = 3.0
        ------------------------------------------------------------
        ------------------------------------------------------------
                           VSAT : V2 : ENABLED
        ------------------------------------------------------------
        Active                                   = X
        Name                                     = V2
        ID                                       = 3002.0
        Console IP                               = 10.111.35.4
        Console PORT                             = 1002.0
        Connection timeout                       = 10.0
        Number of tries                          = 2.0
        Tries timeout                            = 3.0
        ------------------------------------------------------------
        
        
__Show all disabled rows from VSAT sheet (-d|--disabled option):__
        
C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --show vsat --disabled__
        
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            VSAT : DISABLED
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ------------------------------------------------------------
                          VSAT : V3 : DISABLED
        ------------------------------------------------------------
        Active                                   =
        Name                                     = V3
        ID                                       = 3003.0
        Console IP                               = 10.111.35.5
        Console PORT                             = 1003.0
        Connection timeout                       = 10.0
        Number of tries                          = 2.0
        Tries timeout                            = 3.0
        ------------------------------------------------------------
        ------------------------------------------------------------
                          VSAT : V4 : DISABLED
        ------------------------------------------------------------
        Active                                   =
        Name                                     = V4
        ID                                       = 3004.0
        Console IP                               = 10.111.35.6
        Console PORT                             = 1004.0
        Connection timeout                       = 10.0
        Number of tries                          = 2.0
        Tries timeout                            = 3.0
        ------------------------------------------------------------
        
__Check from one specified VSAT (-n|--name option):__
        
C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --show vsat --name V1__
        
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                             VSAT : ENABLED
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ------------------------------------------------------------
                           VSAT : V1 : ENABLED
        ------------------------------------------------------------
        Active                                   = X
        Name                                     = V1
        ID                                       = 3001.0
        Console IP                               = 192.168.140.76
        Console PORT                             = 1016.0
        Connection timeout                       = 10.0
        Number of tries                          = 2.0
        Tries timeout                            = 3.0
        ------------------------------------------------------------
        VSAT: V2
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            VSAT : DISABLED
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        VSAT: V3
        VSAT: V4
        VSAT: V5
        VSAT: V9
        VSAT: V10
        
__Check just one specified VSAT (-n|--name option):__

__Link UP output example__

C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --check vsat --name V1__

        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        ------------------------------------------------------------
                         -- V1 : ENABLED --
        ------------------------------------------------------------
        Active               = x
        Name                 = V1
        ID                   = 3001.0
        Console IP           = 192.168.140.76
        Console PORT         = 1010.0
        Connection timeout   = 10.0
        Number of tries      = 2.0
        Tries timeout        = 3.0
        
        step:\> Checking connection ...
        status: -> SUCCESS!
        
        step:\> Checking link status!
        status: Total Backbone Links UP = 1
        status: ->Link UP!
        ------------------------------------------------------------
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        VSAT : V2
        VSAT : V3
        VSAT : V4
        VSAT : V5
        VSAT : V9
        VSAT : V10
        
C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --check vsat --name V1__

__Link DOWN example__

        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        VSAT : V1
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        ------------------------------------------------------------
                         -- V2 : DISABLED --
        ------------------------------------------------------------
        Active               =
        Name                 = V2
        ID                   = 3002.0
        Console IP           = 192.168.140.76
        Console PORT         = 1016.0
        Connection timeout   = 10.0
        Number of tries      = 2.0
        Tries timeout        = 3.0
        
        step:\> Checking connection ...
        status: -> SUCCESS!
        
        step:\> Checking link status!
        status: Total Backbone Links UP = 0
        status: ->Link DOWN!
        ------------------------------------------------------------
        VSAT : V3
        VSAT : V4
        VSAT : V5
        VSAT : V9
        VSAT : V10
        

__Example with no connection:__

C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --check vsat --name V3__
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        VSAT : V1
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        VSAT : V2
        ------------------------------------------------------------
                         -- V3 : DISABLED --
        ------------------------------------------------------------
        Active               =
        Name                 = V3
        ID                   = 3003.0
        Console IP           = 192.168.140.76
        Console PORT         = 101.0
        Connection timeout   = 10.0
        Number of tries      = 2.0
        Tries timeout        = 3.0
        
        step:\> Checking connection ...
        status: [Errno 10061] No connection could be made because the target machine actively refused it
        
        VSAT: ip: 192.168.140.76 port:101
        HINT: ngnmstest.py --check vsat --name <vsat_name>

__How to run test cases:__

__If provide a non existing name, we get all posible sheet related cases__

C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --run --name blabla__

        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
        TESTCASES: 1
        TESTCASES: 4
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
        TESTCASES: 2
        TESTCASES: 3
        TESTCASES: 5
        TESTCASES: 6
        TESTCASES: 7
        TESTCASES: 8
        TESTCASES: 9
        TESTCASES: 10
        TESTCASES: 11

__Running existing testcase:__

C:\Documents and Settings\VitalieG\git\ngnms>__ngnmstest.py --run --name 1__

        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        TODO: check ngnms and vsat
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        ------------------------------------------------------------
                         -- V1 : ENABLED --
        ------------------------------------------------------------
        Active               = x
        Name                 = V1
        ID                   = 3001.0
        Console IP           = 192.168.140.76
        Console PORT         = 1010.0
        Connection timeout   = 10.0
        Number of tries      = 2.0
        Tries timeout        = 3.0
        
        step:\> Checking connection ...
        status: -> SUCCESS!
        
        step:\> Checking link status!
        status: Total Backbone Links UP = 1
        status: ->Link UP!
        ------------------------------------------------------------
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                               ENABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
        
        ------------------------------------------------------------
                             TESTCASES: 1
        ------------------------------------------------------------
        
        step:\> TODO: set ngnms working point!
        step:\> TODO: check ready ngnms working point!
        info:\> connecting to ... ip:192.168.140.76 port:1010 timeout:10
        
        step:\> Checking link status!
        status: Total Backbone Links UP = 1
        
        test:\> ip selftest ftpup 1 10
        step:\> inbound -> start!
        step:\> Please wait 5 sec: [5]
        step:\> Checking link status!
        status: Total Backbone Links UP = 1
        status: inbound -> done!
        step:\> Please wait 7 sec: [7]
        test:\> ip selftest ftpdown 10
        step:\> outbound -> start!
        step:\> Please wait 5 sec: [5]
        step:\> Checking link status!
        status: Total Backbone Links UP = 1
        status: outbound -> done!
        
        ------------------------- TEST: 1 ------------------------
        Active                                 = X
        Test Nr.                               = 1.0
        OB symbol rate                         = 45000000.0
        OB mode code                           = QPSK 1/3
        RTN Channels Frequency Plan            = DYNAMIC
        IB symbol rate_1                       = 768.0
        IB symbol rate_2                       = 1024.0
        IB symbol rate_3                       = 2048.0
        IB symbol rate_4                       = 256.0
        IB mode code_1                         = QPSK 1/2
        IB mode code_2                         = QPSK 3/4
        IB mode code_3                         = 8PSK 4/5
        IB mode code_4                         = 8PSK 2/3
        Number of Channels_1                   = 1.0
        Number of Channels_2                   = 10.0
        Number of Channels_3                   = 5.0
        Number of Channels_4                   = 1.0
        Dynamic/Static_1                       = STATIC
        Dynamic/Static_2                       = DYNAMIC
        Dynamic/Static_3                       = STATIC
        Dynamic/Static_4                       = DYNAMIC
        Symbol Rate_11                         = 1024.0
        Symbol Rate_12                         = 256.0
        Symbol Rate_21                         = 128.0
        Symbol Rate_22                         = 768.0
        Symbol Rate_31                         = 1536.0
        Symbol Rate_32                         = 2048.0
        Symbol Rate_41                         = 512.0
        Symbol Rate_42                         = 2560.0
        IB Preamble                            = 96/128
        IB Number of ATM                       = 2.0
        Test duration                          = 10.0
        
        ------------------------- OUTPUT: 1 ------------------------
        
        Max OB bit rate                        = 0
        Max IB bit rate                        = 0
        VSAT CPU                               = $18$
        Number of transmitted OB packets       = 0
        Number of received IB packets          = 0
        Number of OB retransmit packets        = 0
        Number of IB retransmit packets        = 0
        
        ------------------------------------------------------------
        
        TESTCASES: 4
        TESTCASES: 8
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                              DISABLED
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
        TESTCASES: 2
        TESTCASES: 3
        TESTCASES: 5
        TESTCASES: 6
        TESTCASES: 7
        TESTCASES: 9
        TESTCASES: 10
        TESTCASES: 11
        
        info:\> Saving result to [data/output.xls] excel file!
        
        
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
        SUCCESS!: Successfully saved data to file: [data/output.xls]!
        
        HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
        
        ------------------------------------------------------------
        
                        Good job!
                        Congratulations! @};-
                        Well done!
        
        ------------------------------------------------------------
