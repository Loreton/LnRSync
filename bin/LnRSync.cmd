@ECHO On

    SET SCRIPT_DRIVE=%~d0
    SET SCRIPT_PATH=%~dp0
    SET SCRIPT_NAME=%~n0

    CALL L:\LNFree\_LnPortable\PythonPATH.bat

    IF /I "%1" == "HELP" (
        SET PARAMS=--help
        GOTO :PROCESS
    )

    IF "x%1" == "x" (
        SET PARAMS=-c HomeBackup.cfg
        SET PARAMS=-c HomeBackup.cfg -s Portit_DiscoL -a go
        SET PARAMS=-c HomeBackup.cfg -s Portit_DiscoD -a step
        echo %PARAMS%
    )
    ) ELSE (
        SET PARAMS=%*
    )

    GOTO :PROCESS

:PROCESS
    echo %PARAMS%
    echo python.exe %SCRIPT_PATH%\..\SOURCE\__main__.py %PARAMS%

pause