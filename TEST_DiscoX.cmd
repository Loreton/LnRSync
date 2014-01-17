@ECHO OFF
@COLOR 1F
@SET PATH=.;L:\LNFree\SynchBackup\cwRsync\bin;L:\LNFree\UnixUtils;L:\Loreto\Procs\Bat;L:\LnFree\Pgm\Python Portable 2.7.3.1\Lib\site-packages\win32com;L:\LnFree\Pgm\Python Portable 2.7.3.1\DLLs;L:\LnFree\Pgm\Python Portable 2.7.3.1\APP;C:\oracle\jre\1.4.2\bin\client;C:\oracle\jre\1.4.2\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\Programmi\Toshiba\Bluetooth Toshiba Stack\sys\;C:\PROGRA~1\IBM\SQLLIB\BIN;C:\PROGRA~1\IBM\SQLLIB\FUNCTION;C:\WINDOWS\system32\archiflowdll;C:\Programmi\MIT\Kerberos\bin;C:\windows\system32\archiflowdll;C:\Programmi\IBM\Personal Communications\;C:\Programmi\IBM\Trace Facility\;C:\Programmi\landesk\shared files;C:\Programmi\LANDesk\LDClient;C:\Programmi\Windows Imaging\
@SET PYTHONPATH=L:\Loreto\ProjectsAppl\PythonProjects\LnRSync/Bin;L:\Loreto\ProjectsAppl\PythonProjects\LnRSync/Bin/HomeBackup_LNf.zip
@SET DRIVE=L:
@SET ALIAS=HomeBackup
@SET PRJ_NAME=HomeBackup

@CD /D L:\Loreto\ProjectsAppl\PythonProjects\LnRSync
python.exe "L:\Loreto\ProjectsAppl\PythonProjects\LnRSync\SOURCE\__Main__.py" -c HomeBackup.cfg -a step -s Test_DiscoX
