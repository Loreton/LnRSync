#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import subprocess

# #############################################################################
# # prepareServerPath()
# #############################################################################
def prepareServerPath(partner, subDir):
    TYPE, SERVER, dirName = partner.split(hostSepCahr, 2)
    baseDir   = dirName.strip()
    hostName  = SERVER.strip()

    if not subDir[-1] == '/': subDir += '/'
    fullDir = "{}/{}".format(baseDir.strip(), subDir)

        # convert to cygWin path (if required)
    if fullDir[1] == ':' and not fullDir[0] == '/':
        fullDir = '/cygdrive/' + fullDir[0] + fullDir[2:].replace('\\', '/')

    if TYPE.strip() == 'SOURCE':
        sourceHostName  = 'LOCAL' if hostName == 'LOCAL' else hostName
        sourcePATH      = fullDir
        if gv.Ln.isWindows: gv.SOURCE.HostType = 'WINDOWS'
    else:
        destHostName    = 'LOCAL' if hostName == 'LOCAL' else hostName
        destPATH        = fullDir
        if gv.Ln.isWindows: gv.DEST.HostType = 'WINDOWS'


def addEXCLUDE(line):
    lista = []
    for item in line.split():
        lista.append('--exclude="{}"'.format(item))
    return lista


################################################################################
# - getSectionItem
################################################################################
def prepareRsyncCommand(rSyncCMD, sourcePART, destPART, subDir, extraOptions):

    sourceHostName  = sourcePART[0].strip()
    destHostName    = destPART[0].strip()

    if not subDir[-1] == '/': subDir += '/'
    sourcePATH   = "{}/{}".format(sourcePART[1].strip(), subDir)
    destPATH     = "{}/{}".format(destPART[1].strip(), subDir)


        # -------------------------------------------
        # - convert to cygWin path (if required)
        # -------------------------------------------
    sourceTYPE = 'UNIX_SOURCE'

    if sourceHostName == 'LOCAL' and gv.Ln.isWindows:
        sourceTYPE = 'WIN_SOURCE'
        if sourcePATH[1] == ':' and not sourcePATH[0] == '/':
            sourcePATH = '/cygdrive/' + sourcePATH[0] + sourcePATH[2:].replace('\\', '/')

    destTYPE = 'UNIX_DEST'
    if destHostName == 'LOCAL' and gv.Ln.isWindows:
        destTYPE = 'WIN_DEST'
        if destPATH[1] == ':' and not destPATH[0] == '/':
            destPATH = '/cygdrive/' + destPATH[0] + destPATH[2:].replace('\\', '/')

    rsyncOPT = []
    gv.sourcePATH   = sourcePATH
    gv.destPATH     = destPATH

        # -----------------------
        # - Load OPTIONS
        # -----------------------
    XFER_TYPE = 'LOC_TO_LOC' if sourceTYPE.split('_')[0] == destTYPE.split('_')[0] else 'ONE_IS_REMOTE'


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
    # print (rsyncOPT)
    rsyncOPT.extend(extraOptions)
    # print (rsyncOPT)

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
    for item in rSyncCMD:
        cPrint.Yellow(item, tab=4)
    print()
    print ()


    return rSyncCMD




################################################################################
# - M A I N
# - sectionName è il nome della [SECTION] del file_config.ini da elaborare
################################################################################
def Main(gVars, sectionName):
    global gv, cPrint
    gv = gVars
    gv.fCONSOLE = True
    cPrint = gv.Ln.LnColor()

    TYPE_OF_COMMAND = 'OS_SYSTEM'
    TYPE_OF_COMMAND = 'CALL'



    try:
            # aggiungiamo i percorsi nelle PATH
        for key, val in gv.ini.PATH.items():
            sys.path.insert(0, val.strip())


        wkSection     = gv.ini[sectionName]

            # Main Section
        if gv.Ln.isUnix:
            gv.ini.MAIN        = gv.ini.UNIX_MAIN
        else:
            gv.ini.MAIN        = gv.ini.WIN_MAIN

    except (KeyError) as why:
        print("Errore nella lettura della chiave: {}".format(str(why)))
        gv.ini.printTree(header="Available sections", whatPrint='K', maxDepth=0, fEXIT=True)

    except (Exception) as why:
        print("Errore nella lettura del file: {} - {}".format(gv.env.iniFileName, str(why)))
        gv.ini.printTree(header="Available sections", whatPrint='K', maxDepth=0, fEXIT=True)







        # -----------------------------------------------
        # - preparazione comando di base
        # -----------------------------------------------
    baseRSyncCMD = []
    baseRSyncCMD.append(gv.ini.MAIN.RSYNC_Program)
    if not gv.inputParam.fEXECUTE: baseRSyncCMD.append('--dry-run')

        # -----------------------------------------------------------
        # - lastRun log  (mantiene traccia delle dir già eseguiti)
        # -----------------------------------------------------------
    lastRunData = gv.Prj.LastRunLog(gv, fName=os.path.normpath(os.path.abspath(gv.env.mainConfigDIR + '/LAST_RUN.log')))

    keysToSkip = ['var', 'x']  # keyPrefix da saltare

    wkSection = gv.ini[sectionName]
    if 'logToFile' in wkSection:
        LOGTOFILE = wkSection['logToFile'].strip('"').strip("'").strip()
        del wkSection['logToFile'] # per evitare che dia errore lo split delle key di seguito
    else:
        LOGTOFILE = None


        # -----------------------------------------------
        # - Elaborazione della section richiesta.
        # -----------------------------------------------
    # wkSection.printTree(header='working on section:', whatPrint='KV')

    for key, val in wkSection.items():
        key1, rest = key.split('.', 1)
        if key1 in keysToSkip: continue        # l'abbiamo gia' analizzata oppure e' una var. o x.
        sPartner       = wkSection['{}.SOURCE'.format(key1)].split(',')
        dPartner       = wkSection['{}.DEST'.format(key1)].split(',')
        subDirs        = wkSection['{}.SubDirs'.format(key1)].split(',')

        extraOptions = []
        optKEYs = ( '{0}.OPT.EXTRA'.format(key1), '{0}.OPT.EXCLUDE'.format(key1) )
        if rest == 'OPT.EXTRA': extraOptions.append(val)


        # -----------------------------------------------
        # - processo delle singole directory
        # -----------------------------------------------
    loop = 5
    for subDir in subDirs:
        subDir = subDir.strip()
        if not subDir: continue

        baseCMD = baseRSyncCMD[:]
            # -----------------------
            # - rSync LOG File
            # -----------------------
        logFileName = gv.Prj.rsyncLogFile(gv, LOGTOFILE, sectionName, subDir.replace('/', '.'))
        baseCMD.append('--log-file={}'.format(logFileName))
        cPrint.Yellow('rSync log file:   {}'.format(logFileName), tab=4)

        thisCmd = gv.Prj.PrepareRsyncCommand(gv, baseCMD, sPartner, dPartner, subDir, extraOptions)
        rSyncCMD = thisCmd.cmdList

        currentPaths = "{0:<70} - {1}".format(thisCmd.sourcePATH, thisCmd.destPATH)
        if currentPaths in lastRunData:
            cPrint.YellowH ("skipping...{0}".format(thisCmd.sourcePATH), tab=8)
            continue
        else:
            cPrint.YellowH("- going to copy....{}".format(thisCmd.sourcePATH), tab=8)

        loop -= 1
        if loop <= 0: break

        thisCmd.printTree(whatPrint='KV', fEXIT=False)

        if TYPE_OF_COMMAND == 'OS_SYSTEM':
            print(' '.join(rSyncCMD))
            rCode = os.system(' '.join(rSyncCMD))
            print('-'*60)
            print("process for subDir: {0} completed. [rCode={1}]".format(subDir, rCode))
            print('-'*60)


        elif TYPE_OF_COMMAND == 'CALL':
            print(' '.join(rSyncCMD))
            sys.exit()
            try:
                rCode = subprocess.call( rSyncCMD, shell=False, timeout=100)  # ritorna <class 'bytes'>

                    # output = output.decode('utf-8')                         # converti in STRing
            except subprocess.TimeoutExpired as why:
                msg = str(why)
                logger.error(msg)
                rCode = 9

            # rCode = subprocess.call(' '.join(rSyncCMD), stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
            print('-'*60)
            print("process for subDir: {0} completed. [rCode={1}]".format(subDir, rCode))
            print('-'*60)



        elif TYPE_OF_COMMAND == 'CHECK_OUTPUT':
            res = subprocess.check_output(rSyncCMD, stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
            res = res.decode('utf-8')                                           # converti in STRing

        # print (sourcePART, subDir)


        print ("saving on LAST-RUN {0}".format(currentPaths))
        lastRunData = gv.Prj.LastRunLog(gv, data=currentPaths)



        sys.exit()
    '''



    if logFullName:
        print()
        print()
        print("process for sectionName: {0} completed.".format(sectionName))
    '''



