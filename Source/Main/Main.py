#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import subprocess


################################################################################
# - M A I N
# - sectionName è il nome della [SECTION] del file_config.ini da elaborare
################################################################################
def Main(gVars, sectionName):
    global gv, cPrint
    gv = gVars
    gv.fCONSOLE = True
    cPrint = gv.Ln.LnColor()

    CallType = 'CHECK_OUTPUT'
    CallType = 'CALL'
    CallType = 'OS_SYSTEM'


    logger = gv.Ln.SetLogger(package=__name__)

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
    lastRunData = gv.Prj.LastRunLog(gv, fName=os.path.normpath(os.path.abspath(gv.env.dataDIR + '/LAST_RUN.log')))

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
    # loop = 5
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

        # loop -= 1
        # if loop <= 0: break

        thisCmd.printTree(header="rSync command in esecuzione...", whatPrint='KV', fEXIT=False)

        if CallType == 'OS_SYSTEM':
            print(' '.join(rSyncCMD))

            rCode = os.system(' '.join(rSyncCMD))

            print('-'*60)
            print("process for subDir: {0} completed. [rCode={1}]".format(subDir, rCode))
            print('-'*60)


        elif CallType == 'CALL':
            print(' '.join(rSyncCMD))
            print()
            SHELL=False; CMD=rSyncCMD
            SHELL=True;  CMD=' '.join(rSyncCMD)

            try:
                    # non metto il timeout altrimenti rischio di bloccare la copia
                    # in quanto non so quanto impiega rsync a completarsi
                rCode = subprocess.call(CMD, shell=SHELL, timeout=None)  # ritorna <class 'bytes'>

            except subprocess.TimeoutExpired as why:
                msg = str(why)
                logger.error(msg)
                rCode = 9

            finally:
                print('-'*60)
                print("process for subDir: {0} completed. [rCode={1}]".format(subDir, rCode))
                print('-'*60)

                                      # converti in STRing

        if rCode == 0:
            print ("saving on LAST-RUN {0}".format(currentPaths))
            lastRunData = gv.Prj.LastRunLog(gv, data=currentPaths)




