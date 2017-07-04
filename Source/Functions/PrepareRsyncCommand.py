#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
# by Loreto Notarantonio LnVer_2017-07-04_14.16.11
# ######################################################################################
import sys
import os


################################################################################
# -
################################################################################
def PrepareRsyncCommand(gv, rSyncCMD, sPartner, dPartner, subDir, extraOptions):
    cPrint = gv.Ln.LnColor()
    sourceHostName, sourcePART = sPartner
    destHostName,   destPART   = dPartner


    if not subDir[-1] == '/': subDir += '/'
    sourcePATH   = "{}/{}".format(sourcePART.strip(), subDir)
    destPATH     = "{}/{}".format(destPART.strip(), subDir)


        # -------------------------------------------
        # - convert to cygWin path (if required)
        # -------------------------------------------


    sourceTYPE = 'UNIX_SOURCE'
    sourceHostName = sourceHostName.strip()
    if sourceHostName == 'LOCAL' and gv.Ln.isWindows:
        sourceTYPE = 'WIN_SOURCE'
        if sourcePATH[1] == ':' and not sourcePATH[0] == '/':
            sourcePATH = '/cygdrive/' + sourcePATH[0] + sourcePATH[2:].replace('\\', '/')




    destTYPE = 'UNIX_DEST'
    destHostName = destHostName.strip()
    if destHostName == 'LOCAL' and gv.Ln.isWindows:
        destTYPE = 'WIN_DEST'
        if destPATH[1] == ':' and not destPATH[0] == '/':
            destPATH = '/cygdrive/' + destPATH[0] + destPATH[2:].replace('\\', '/')




        # -----------------------
        # - Load OPTIONS
        # -----------------------
    XFER_TYPE = 'LOC_TO_LOC' if sourceTYPE.split('_')[0] == destTYPE.split('_')[0] else 'ONE_IS_REMOTE'


    # splitRsyncOptions = True
    # if splitRsyncOptions:
    rsyncOPT = []
    for key, val in gv.ini.RSYNC_OPTIONS.items():
        token = key.split('.'); keyPrefix = token[0]; keySuffix = token[-1]

        ADD = False
        if   keyPrefix == 'BASE':       ADD = True
        elif keyPrefix == sourceTYPE:   ADD = True
        elif keyPrefix == destTYPE:     ADD = True
        elif keyPrefix == XFER_TYPE:    ADD = True
        if ADD:
            if keySuffix == 'EXCLUDE':
                for item in val.split():
                    rsyncOPT.append('--exclude="{}"'.format(item))
                continue

            else:
                for item in val.split('--'):
                    if item.strip():
                        rsyncOPT.append('--{}'.format(item.strip()))

    '''
        # print ('....1111\n', rsyncOPT)
    else:
        rsyncOPT = []
        for key, val in gv.ini.RSYNC_OPTIONS.items():
            token = key.split('.'); keyPrefix = token[0]; keySuffix = token[-1]

            if keySuffix == 'EXCLUDE':
                for item in val.split():
                    rsyncOPT.append('--exclude="{}"'.format(item))
                continue

            ADD = False
            if   keyPrefix == 'BASE':       ADD = True
            elif keyPrefix == sourceTYPE:   ADD = True
            elif keyPrefix == destTYPE:     ADD = True
            elif keyPrefix == XFER_TYPE:    ADD = True
            if ADD:
                rsyncOPT.append(val)

        # print ('....2222', rsyncOPT)
    '''

    rsyncOPT.extend(extraOptions)

    rSyncCMD.extend(rsyncOPT)

    if sourceHostName == 'LOCAL':
        rSyncCMD.append('"{}"'.format(sourcePATH))
    else:
        rSyncCMD.append('"{}:{}"'.format(sourceHostName, sourcePATH))

    if destHostName   == 'LOCAL':
        rSyncCMD.append('"{}"'.format(destPATH))
    else:
        rSyncCMD.append('"{}:{}"'.format(destHostName, destPATH))

    cPrint.Cyan ('\n'*3, tab=4)
    cPrint.Cyan ('*'*50, tab=4)
    cPrint.Cyan ('*   Sub Dir      {}'.format(subDir), tab=4)
    cPrint.Cyan ('*   XFER_TYPE:   {}_TO_{}'.format(sourceHostName, destHostName), tab=4)
    cPrint.Cyan ('*   sourcePATH:  {}:{}'.format(sourceHostName, sourcePATH), tab=4)
    cPrint.Cyan ('*   destPATH:    {}:{}'.format(destHostName, destPATH), tab=4)
    cPrint.Cyan ('*'*50, tab=4)

    print ()

    myCommand = gv.Ln.LnDict()

    myCommand.sourcePATH   = sourcePATH
    myCommand.destPATH     = destPATH
    myCommand.cmdList      = rSyncCMD

    return myCommand
