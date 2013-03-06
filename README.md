Automated Testing flow:

1.	Using REST API we export the configuration file {JSON format with OID}.
2.	From our Excel file with Test Cases we read one line that contains Test Case To Run.
3.	Changing the value of needed OID with needed values.
4.	Using REST API, we import back configuration file to NGNMS.
5.	Checking NGNMS is ready for statistics result.
6.	Starting SELFTEST Mode.
7.	Over Telnet protocol, we collect result data.
8.	Storing data into Excel file.
9.	Go to again to P.1 until go through all Test Cases.
