@ECHO OFF
call %pp%
SET "Project=WinToHD"
SET "LOGFile=d:\zTemp\rSync\%Project%.log"
python __main__.py PortitToOther.ini %Project% --go >%LOGFile% 2>>&1 && echo "Process completed" >>%LOGFile%