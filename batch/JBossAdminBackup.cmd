@ECHO OFF
    setlocal
        :: impostazione nome progetto
    SET     "Project=%~n0"
    SET     "iniFile=LnRSync.ini"
    SET     Caption="Esecuzione: %Project%"
    echo    %Caption%
    TITLE   "%Caption%"
    SET     PARAMS=%*


        :: prelievo path corrente ed impostazione path vari
    set     "thisPATH=%~dp0"
    chdir  /D  %thisPATH%..\                       &:: e spostiamoci sulla parent dir
    set currDIR=%CD%
    set "sourceDIR=%CD%\SOURCE"
    set "binDIR=%CD%\bin"
    set "confDIR=%CD%\conf"


    set "mainProgram=%binDIR%\LnRSync.zip"
    if  not exist "%mainProgram%" set "mainProgram=%sourceDIR%\__main__.py"



:Execute
    echo *******************************
    echo *  %mainProgram%  *
    echo *******************************
    call %pp%                                       &:: call Python setup - L:\LNFree\_LnPortable\PythonPATH.cmd 3.2
    python %mainProgram% %confDIR%\%iniFile% %Project% %PARAMS% --GO
    goto :END


:END
    endlocal
    pause