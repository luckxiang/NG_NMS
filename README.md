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
        ============================================================
                INFO: Excel file data/demo.xls!
        ============================================================
        step:\> Connecting to: https://192.168.140.42:8443
        info:\> auth: {'ngnms_password': 'manager', 'ngnms_user': 'admin'}
        status: 200 https://192.168.140.42:8443/navigation/statustree/network
        step:\> Scanning ngnms network tree ...
        ------------------------------------------------------------
           Teleport: Chateau de Betzdorf (teleport)
               Satellite: CEC 2R (satellite)
                   RF Cluster: B1 BSS (RF cluster)
                                NS: NS1-HC
                                NS: NS4
                   RF Cluster: B1 FSS (RF cluster)
                                NS: NS2-HC
                                NS: NS3
        ------------------------------------------------------------
        ------------------------------------------------------------
           Teleport: Teleport 2
               Satellite: Satellite 2a
                   RF Cluster: rfCluster 1
                                NS: NS 22
                   RF Cluster: rfCluster 2
                                NS: NS 33
               Satellite: Satellite 2b
        ------------------------------------------------------------
        ------------------------------------------------------------
           Teleport: main
               Satellite: Satellite
                   RF Cluster: rfCluster 1
                                NS: controler
        ------------------------------------------------------------
        info:\> Available network segments names on server:
              NS 33                     =   611
              controler                 =   627
              NS1-HC                    =   580
              NS2-HC                    =   591
              NS 22                     =   606
              NS3                       =   596
              NS4                       =   585
        
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
        ID                   = 3001
        Console IP           = 192.168.140.76
        Console PORT         = 1010
        Connection timeout   = 10
        Number of tries      = 2
        Tries timeout        = 3
        
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
        
        step:\> Connecting to: https://192.168.140.42:8443
        info:\> auth: {'ngnms_password': 'manager', 'ngnms_user': 'admin'}
        status: 200 https://192.168.140.42:8443/navigation/statustree/network
        step:\> getting data: https://192.168.140.42:8443/folders/config/627
        status: 200 https://192.168.140.42:8443/folders/config/627
        step:\> changing values:
        ---------------------------------------------------------------------------------------------------
        |                OID                 |     Instance   |         Old         |         New         |
        ---------------------------------------------------------------------------------------------------
        |   1.3.6.1.4.1.7352.3.36.3.20       |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.5.5        |   0            |   29010000          |   29010000          |
        |   1.3.6.1.4.1.7352.3.36.5.4        |   0            |   29000000          |   29000000          |
        |   1.3.6.1.4.1.7352.3.36.5.1        |   0            |   100               |   100               |
        |   1.3.6.1.4.1.7352.3.36.3.19       |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.3.18       |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.3.17       |   0            |   172.24.4.254      |   172.24.4.254      |
        |   1.3.6.1.4.1.7352.3.36.5.2        |   0            |   19000000          |   19000000          |
        |   1.3.6.1.4.1.7352.3.36.4.13       |   0            |   29216006          |   29216006          |
        |   1.3.6.1.4.1.7352.3.36.4.12       |   0            |   9                 |   9                 |
        |   1.3.6.1.4.1.7352.3.36.4.11       |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.3.16       |   0            |   255.255.0.0       |   255.255.0.0       |
        |   1.3.6.1.4.1.7352.3.36.4.10       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.4.17       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.4.16       |   0            |   60000000          |   60000000          |
        |   1.3.6.1.4.1.7352.3.36.3.11       |   0            |   172.18.0.101      |   172.18.0.101      |
        |   1.3.6.1.4.1.7352.3.36.4.15       |   0            |   29216006          |   29216006          |
        |   1.3.6.1.4.1.7352.3.36.3.12       |   0            |   172.24.4.4        |   172.24.4.4        |
        |   1.3.6.1.4.1.7352.3.36.4.14       |   0            |   60000000          |   60000000          |
        |   1.3.6.1.4.1.7352.3.36.4.2        |   0            |   28100000          |   28100000          |
        |   1.3.6.1.4.1.7352.3.36.4.1        |   0            |   27000000          |   27000000          |
        |   1.3.6.1.4.1.7352.3.36.4.6        |   0            |   15                |   15                |
        |   1.3.6.1.4.1.7352.3.36.4.7        |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.5.17       |   0            |   10000000          |   10000000          |
        |   1.3.6.1.4.1.7352.3.36.5.14       |   0            |   5                 |   5                 |
        |   1.3.6.1.4.1.7352.3.36.5.13       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.4.20       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.4.21       |   0            |   28000000          |   28000000          |
        |   1.3.6.1.4.1.7352.3.36.2.1        |   0            |   4                 |   4                 |
        |   1.3.6.1.4.1.7352.3.36.2.2        |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.4.19       |   0            |   60000000          |   60000000          |
        |   1.3.6.1.4.1.7352.3.36.4.18       |   0            |   29216006          |   29216006          |
        |   1.3.6.1.4.1.7352.3.36.4.9        |   0            |   200               |   200               |
        |   1.3.6.1.4.1.7352.3.36.2.9        |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.7        |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.2.8        |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.5        |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.6        |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.3        |   0            |   controler         |   controler         |
        |   1.3.6.1.4.1.7352.3.36.2.14       |   0            |   1                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.2.15       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.12       |   0            |   127.0.0.1         |   127.0.0.1         |
        |   1.3.6.1.4.1.7352.3.36.2.13       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.10       |   0            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.2.11       |   0            |   127.0.0.1         |   127.0.0.1         |
        |   1.3.6.1.4.1.7352.3.36.7.1.5      |   1            |   0                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.5      |   2            |   0                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.5      |   3            |   -                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.5      |   4            |   -                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.2      |   1            |   2                 |   0                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.2      |   2            |   2                 |   2                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.2      |   3            |   -                 |   7                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.2      |   4            |   -                 |   5                 |
        |   1.3.6.1.4.1.7352.3.36.7.1.1      |   1            |   128000            |   768000            |
        |   1.3.6.1.4.1.7352.3.36.7.1.1      |   2            |   2048000           |   1024000           |
        |   1.3.6.1.4.1.7352.3.36.7.1.1      |   3            |   -                 |   2048000           |
        |   1.3.6.1.4.1.7352.3.36.7.1.1      |   4            |   -                 |   256000            |
        |   1.3.6.1.4.1.7352.3.36.7.1.3      |   1            |   1                 |   111               |
        |   1.3.6.1.4.1.7352.3.36.7.1.3      |   2            |   1                 |   112               |
        |   1.3.6.1.4.1.7352.3.36.7.1.3      |   3            |   -                 |   113               |
        |   1.3.6.1.4.1.7352.3.36.7.1.3      |   4            |   -                 |   114               |
        |   1.3.6.1.4.1.7352.3.36.4.5        |   0            |   7                 |   2                 |
        |   1.3.6.1.4.1.7352.3.36.4.3        |   0            |   45000000          |   45000000          |
        |   1.3.6.1.4.1.7352.3.36.5.3        |   0            |   0                 |   1                 |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   1.1          |   128000            |   1024000           |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   1.2          |   -                 |   256000            |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   2.1          |   128000            |   128000            |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   2.2          |   -                 |   768000            |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   3.1          |   -                 |   1536000           |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   3.2          |   -                 |   2048000           |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   4.1          |   -                 |   512000            |
        |   1.3.6.1.4.1.7352.3.36.8.1.2      |   4.2          |   -                 |   2560000           |
        ---------------------------------------------------------------------------------------------------
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
        Test Nr.                               = 1
        OB symbol rate                         = 45000000
        OB mode code                           = QPSK 1/3
        RTN Channels Frequency Plan            = DYNAMIC
        IB symbol rate_1                       = 768
        IB symbol rate_2                       = 1024
        IB symbol rate_3                       = 2048
        IB symbol rate_4                       = 256
        IB mode code_1                         = QPSK 1/2
        IB mode code_2                         = QPSK 3/4
        IB mode code_3                         = 8PSK 4/5
        IB mode code_4                         = 8PSK 2/3
        Number of Channels_1                   = 111
        Number of Channels_2                   = 112
        Number of Channels_3                   = 113
        Number of Channels_4                   = 114
        Dynamic/Static_1                       = STATIC
        Dynamic/Static_2                       = DYNAMIC
        Dynamic/Static_3                       = STATIC
        Dynamic/Static_4                       = DYNAMIC
        Symbol Rate_1.1                        = 1024
        Symbol Rate_1.2                        = 256
        Symbol Rate_2.1                        = 128
        Symbol Rate_2.2                        = 768
        Symbol Rate_3.1                        = 1536
        Symbol Rate_3.2                        = 2048
        Symbol Rate_4.1                        = 512
        Symbol Rate_4.2                        = 2560
        IB Preamble                            = 96/128
        IB Number of ATM                       = 2
        Test duration                          = 10
        
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
