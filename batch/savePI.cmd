@ECHO OFF
    setlocal
    REM la riga che segue è per impostare PATH con un unico ssh.exe
    REM disponibile altrimenti si incontrano problemi di connessione di difficile comprensione
    :: set "PATH=J:\LnFree\SynchBackup\cwRsync\bin"
    SET "Project=savePI"
    SET Caption="Esecuzione: %Project%"
    echo %Caption%
    TITLE "%Caption%"
    CALL %Ln.FreeDir%\PythonPATH.cmd

    set "thisPATH=%~dp0"
    cd /D %thisPATH%..\

    set "PRGTYPE=ZIP"
    SET "MAINPRG=SOURCE\__main__.py"
    IF "%PRGTYPE%" == "ZIP" SET "MAINPRG=bin\LnRSync.zip"



:Execute
    echo *******************************
    echo *  %MAINPRG%  *
    echo *******************************
    call %pp% 3.2                               &:: call Python setup
    python %MAINPRG% ..\conf\LnRSync.ini %Project% --gos

:END
    endlocal
    pause



