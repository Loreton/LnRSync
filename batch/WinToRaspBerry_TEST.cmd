@ECHO OFF
    setlocal
    SET "Project=WinToRaspBerry"
    SET Caption="Esecuzione: %Project%"
    echo %Caption%
    TITLE "%Caption%"

    set "thisPATH=%~dp0"
    cd /D %thisPATH%..\

    set "PRGTYPE=ZIP"
    SET "MAINPRG=SOURCE\__main__.py"
    :: IF "%PRGTYPE%" == "ZIP" SET "MAINPRG=bin\LnRSync.zip"


:Execute
    echo *******************************
    echo *  %MAINPRG%  *
    echo *******************************
    call %pp% 3.2                              &:: call Python setup
    python %MAINPRG% ..\conf\LnRsync.ini %Project% --gos

:END
    endlocal
    pause



