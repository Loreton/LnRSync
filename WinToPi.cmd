@ECHO OFF
call %pp%
SET "MAIN=__main__.py"
SET "MAIN=LnRsync.zip"
SET "Project=WinToPI"
SET "LOGFile=d:\zTemp\rSync\%Project%.log"
rem python __main__.py PortitToOther.ini %Project% --go >%LOGFile% 2>>&1
python %MAIN% PortitToOther.ini %Project% --go
