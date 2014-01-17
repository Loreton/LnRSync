@ECHO On
rem @COLOR 1F
rem @SET PATH=.;L:\LNFree\SynchBackup\cwRsync\bin;L:\LNFree\UnixUtils;%PATH%
rem @SET DRIVE=L:
rem @SET ALIAS=HomeBackup
rem @SET PRJ_NAME=HomeBackup


SET APPDATA=l:\LNFree\Editors\Komodo\LN\AppData\Roaming
SET HOMEPATH=l:\LNFree\Editors\Komodo\LN
SET LOCALAPPDATA=l:\LNFree\Editors\Komodo\LN\AppData\Local
SET USERPROFILE=l:\LNFree\Editors\Komodo\LN

rem SET TEMP=C:\Users\F602250\AppData\Local\Temp\1
rem SET TMP=C:\Users\F602250\AppData\Local\Temp\1


rem SET PGM=L:\LNFree\SynchBackup\cwRsync\bin\rsync.exe
rem SET OPTIONS=--dry-run --human-readable --progress --update --archive --links --delete-after --numeric-ids --compress --iconv=ISO-8859-1,utf-8 --protect-args --log-file=L:/tmp/RsyncEXE.LOG --exclude *.log.* --exclude /Thumbs.db --exclude Cache/ --exclude *Cache* --delete-excluded


rem echo %PGM% %OPTIONS% /cygdrive/C/Users/F602250/AppData/Roaming /cygdrive/l/LNFree/Editors/Komodo/LN/Roaming

@CD /D l:\LNFree\Editors\Komodo
pause
@komodo.exe