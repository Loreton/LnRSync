@ECHO OFF
    setlocal
    SET "Project=WinToRaspBerry"
    SET Caption="Esecuzione: %Project%"
    echo %Caption%
    TITLE "%Caption%"

    set "thisPATH=%~dp0"
    cd /D %thisPATH%..\

    SET "MAINPRG=SOURCE\__main__.py"
    IF NOT EXIST "%MAINPRG%" SET "MAINPRG=bin\LnRSync.zip"


:Execute
    echo *******************************
    echo *  %MAINPRG%  *
    echo *******************************
    call %pp%                               &:: call Python setup
    python %MAINPRG% ..\conf\LnRsync.ini %Project% --go

:END
    endlocal
    pause



