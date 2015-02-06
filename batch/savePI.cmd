@ECHO OFF
    setlocal
    SET "Project=savePI"
    SET Caption="Esecuzione: %Project%"
    echo %Caption%
    TITLE "%Caption%"

    set "thisPATH=%~dp0"
    cd /D %thisPATH%..\

    set "PRGTYPE=ZIP"
    SET "MAINPRG=SOURCE\__main__.py"
    IF "%PRGTYPE%" == "ZIP" SET "MAINPRG=bin\LnRSync.zip"


:Execute
    echo *******************************
    echo *  %MAINPRG%  *
    echo *******************************
    call %pp%                               &:: call Python setup
    python %MAINPRG% ..\conf\LnRsync.ini %Project% --go

:END
    endlocal
    pause



