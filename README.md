TODO:

Automated Testing flow:

1.	Using REST API we export the configuration file {JSON format with OID}.
2.	From our Excel file with Test Cases we read one line that contains Test Case To Run.
3.	Changing the value of needed OID with needed values.
4.	Using REST API, we import back configuration file to NGNMS.
5.	Checking NGNMS is ready for statistics result.
6.	Starting SELFTEST Mode.
7.	Over telnet protocol, we collect result data.
8.	Storing data into Excel file.
9.	Go to again to P.1 until go through all Test Cases.


Simple usage:

C:\Documents and Settings\VitalieG\git\ngnms>ngnmstest.py
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

C:\Documents and Settings\VitalieG\git\ngnms>

Show all active rows from VSAT Sheet:

C:\Documents and Settings\VitalieG\git\ngnms>ngnmstest.py --show vsat

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


Show all disabled rows from VSAT sheet (-d|--disabled option):

C:\Documents and Settings\VitalieG\git\ngnms>ngnmstest.py --show vsat -d

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

Check from one specified VSAT (-n|--name option):

C:\Documents and Settings\VitalieG\git\ngnms>ngnmstest.py --show vsat --name V1

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

Check from one specified VSAT (-n|--name option):

C:\Documents and Settings\VitalieG\git\ngnms>ngnmstest.py --check vsat --name V1
============================================================
        INFO: Excel file data/demo.xls!
============================================================
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                       ENABLED
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
--------------------------------------------------
                 -- V1 : ENABLED --
--------------------------------------------------
Active               = X
Name                 = V1
ID                   = 3001.0
Console IP           = 192.168.140.76
Console PORT         = 1016.0
Connection timeout   = 10.0
Number of tries      = 2.0
Tries timeout        = 3.0

Checking connection ...
-> SUCCESS!

------------------------------------------------------------
VSAT : V2
============================================================
        INFO: Excel file data/demo.xls!
============================================================
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                      DISABLED
HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
VSAT : V3
VSAT : V4
VSAT : V5
VSAT : V9
VSAT : V10

TODO: Implement -r|--run option logic.
