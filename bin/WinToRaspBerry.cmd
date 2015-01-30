@ECHO OFF
call %pp%
SET "Project=WinToRaspBerry"
SET Caption="Esecuzione: %Project%"
echo %Caption%

SET "MAIN=__main__.py"
SET "MAIN=LnRsync.zip"
SET "LOGFile=d:\zTemp\rSync\%Project%.log"
TITLE "%Caption%"

rem python %MAIN% LnRsync.ini %Project% --go >%LOGFile% 2>>&1
python %MAIN% ..\conf\LnRsync.ini %Project% --go
pause
