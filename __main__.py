#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import subprocess

# import functions           as ln


# #############################################################################
# # preparePATHs()
# # Impostazione delle PATHs
# # La scriptDir è la current dir a meno che:
# # non finisce con .zip - nel qual caso saliamo di un livello.
# # non finisce con /bin - nel qual caso saliamo di una subDir.
# #############################################################################
def preparePATHs():
    mySep = os.sep
    mySep = '/'

    thisModuleDIR   = os.path.dirname(os.path.realpath(__file__))
    # print (thisModuleDIR)
    myPaths = []

    if thisModuleDIR.endswith('.zip'):
        EXTERNAL = False
        myPaths.extend([
            os.path.normpath('{0}'.format(thisModuleDIR) ) ,
        ])
    elif os.path.isdir(('lnfunctions')):
        EXTERNAL = False
        myPaths.extend([
            os.path.normpath('{0}'.format(thisModuleDIR) ) ,
        ])
    else:
        EXTERNAL = True
        myPaths.extend([
            os.path.normpath('{0}'.format(thisModuleDIR) ) ,
            os.path.normpath('{0}'.format('../') ) ,    # Per cercare le LnFunctionsNew
        ])

    myPaths.reverse()
    for path in myPaths:
        sys.path.insert(0, path)
        # print (path)
    os.environ['PYTHONPATH'] = os.pathsep.join(myPaths)

    if EXTERNAL:
        import LnFunctionsNew as ln
    else:
        import LnFunctions    as ln

    return ln


class LnClass(): pass


# #############################################################################
# # printLnClass()
# #############################################################################
def printLnClass(dictID, level=1):
    dictID = vars(dictID)
    for key, val in dictID.items():
        if key.startswith('__') and key.endswith('__'): continue    # elimina tutti i built-in (presente in un modulo)
        if isinstance(val, LnClass):
            print()
            print('[{}] {}{:<20} : {}'.format(level, ' '*level*4, key, "LnClass"))
            printLnClass(val, level=level+1)
        else:
            print('[{}] {}{:<20} : {}'.format(level, ' '*level*4, key, val))


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
        if gv.OpSys.upper() == 'WINDOWS': gv.SOURCE.HostType = 'WINDOWS'
    else:
        destHostName    = 'LOCAL' if hostName == 'LOCAL' else hostName
        destPATH        = fullDir
        if gv.OpSys.upper() == 'WINDOWS': gv.DEST.HostType = 'WINDOWS'




################################################################################
# - getSectionItem
################################################################################
def prepareRsyncCommand(rSyncCMD, sourcePART, destPART, subDir):

    sourceHostName  = sourcePART[0].strip()
    destHostName    = destPART[0].strip()

    if not subDir[-1] == '/': subDir += '/'
    sourcePATH   = "{}/{}".format(sourcePART[1].strip(), subDir)
    destPATH     = "{}/{}".format(destPART[1].strip(), subDir)


        # -------------------------------------------
        # - convert to cygWin path (if required)
        # -------------------------------------------
    sourceTYPE = 'UNIX_SOURCE'

    if sourceHostName == 'LOCAL' and gv.OpSys.upper() == 'WINDOWS':
        sourceTYPE = 'WIN_SOURCE'
        if sourcePATH[1] == ':' and not sourcePATH[0] == '/':
            sourcePATH = '/cygdrive/' + sourcePATH[0] + sourcePATH[2:].replace('\\', '/')

    destTYPE = 'UNIX_DEST'
    if destHostName == 'LOCAL' and gv.OpSys.upper() == 'WINDOWS':
        destTYPE = 'WIN_DEST'
        if destPATH[1] == ':' and not destPATH[0] == '/':
            destPATH = '/cygdrive/' + destPATH[0] + destPATH[2:].replace('\\', '/')

    rsyncOPT = []

        # -----------------------
        # - Load OPTIONS
        # -----------------------
    XFER_TYPE = 'LOC_TO_LOC' if sourceTYPE.split('_')[0] == destTYPE.split('_')[0] else 'ONE_IS_REMOTE'

    for key, val in baseOptionSECT.items():
        token = key.split('.'); keyPrefix = token[0]; keySuffix = token[-1]

        if keySuffix == 'EXCLUDE':
            for item in val.split():
                rsyncOPT.append('--exclude="{}"'.format(item))
                # rsyncOPT.append(item)
            continue

        ADD = False
        if   keyPrefix == 'BASE':       ADD = True
        elif keyPrefix == sourceTYPE:   ADD = True
        elif keyPrefix == destTYPE:     ADD = True
        elif keyPrefix == XFER_TYPE:    ADD = True
        if ADD:
            rsyncOPT.append(val)

    rSyncCMD.extend(rsyncOPT)


    if sourceHostName == 'LOCAL':
        rSyncCMD.append('"{}"'.format(sourcePATH))
    else:
        rSyncCMD.append('"{}:{}"'.format(sourceHostName, sourcePATH))

    if destHostName   == 'LOCAL':
        rSyncCMD.append('"{}"'.format(destPATH))
    else:
        rSyncCMD.append('"{}:{}"'.format(destHostName, destPATH))

    print ('\n'*3)
    print ('*'*50)
    print ('*   XFER_TYPE:  {}_TO_{}'.format(sourceHostName, destHostName))
    print ('*   sourcePATH:  {}:{}'.format(sourceHostName, sourcePATH))
    print ('*   destPATH:    {}:{}'.format(destHostName, destPATH))
    # print (' '.join(rSyncCMD))
    print ('*'*50)
    print ()


    return rSyncCMD

################################################################################
# - printSections()
################################################################################
def printSections(INI):
    print()
    print('        SECTIONs disponibili nel file indicato.')
    for section in INI.sections():
        if not section in ['myVAR', 'PATH', 'MAIN', 'dirVARS', 'RSYNC_OPTIONS', ]:
            print ('            {}'.format(section))
    print ()



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    ln = preparePATHs()
    gv = ln.gv              # shortLink
    gv.fCONSOLE = True

        # cerchiamo il parametro --GO  e lo togliamo dalla lista
    DRY_RUN = '--dry-run'
    for inx, item in enumerate(sys.argv):
        if item.upper() in ['--GO']:
            DRY_RUN = ''
            del sys.argv[inx]


        # ==========================================================
        # PARAMETRI
        #   Param1: Nome del file.ini.
        #           Es. dir=sendKey,   file=sendKey.ini
        #   Param2: Nome della section da lavorare nel file.ini
        #           se mancante allora la SECTION=dir
        # ==========================================================
    # print(len(sys.argv))
    if len(sys.argv) < 2 :
        print('''
        Immettere:
            file.ini:       nome del file di configurazione
            sectionName:    [section] da processare
            ''')
        sys.exit()

    if len(sys.argv) >= 2:
        iniFileName = sys.argv[1]
        INIcParse, INI = ln.readIniFile(iniFileName, RAW=False)

    if len(sys.argv) < 3 :
        print('  Immettere anche il none della SECTION.')
        printSections(INIcParse)
        sys.exit()

    sectionName = sys.argv[2]

    TYPE_OF_COMMAND = 'OS_SYSTEM'
    TYPE_OF_COMMAND = 'CALL'
    # iniFileName     = 'Portit-Backup.ini'
    # ln.printINIconfigparser(INIcParse)



    try:
            # Path Section
        pathSECT        = INI['PATH']

            # Options Section
        baseOptionSECT  = INI['RSYNC_OPTIONS']

        workingSECT     = INI[sectionName]

            # Main Section
        mainSECT        = INI['MAIN']
        RSYNC_Program   = mainSECT['RSYNC_Program']
        LOGDir          = mainSECT['LOGDir']

    except (KeyError) as why:
        print("Errore nella lettura della chiave: {}".format(str(why)))
        printSections(INIcParse)
        sys.exit(-1)

    except (Exception) as why:
        print("Errore nella lettura del file: {} - {}".format(iniFileName, str(why)))
        printSections(INIcParse)
        sys.exit(-1)

        # aggiungiamo i percorsi nelle PATH
    for key, val in pathSECT.items():
        sys.path.insert(0, val.strip())

        # - preparazione comando di base
    baseRSyncCMD = []
    baseRSyncCMD.append(RSYNC_Program)
    baseRSyncCMD.append(DRY_RUN)

        # - LOG File
    LOG = None
    if 'LOGFile' in workingSECT:
        logFile = workingSECT['LOGFile'].strip('"').strip("'").strip()
        del workingSECT['LOGFile']
        if logFile == None or logFile == '':    logFullName = None
        elif logFile.lower() == 'true':         logFullName = os.path.join(LOGDir, sectionName) + '.log'
        else:                                   logFullName = os.path.join(LOGDir, logFile)
        if logFullName:
            # gv.fCONSOLE = False
            if os.path.isfile(logFullName):
                os.remove(logFullName)
            baseRSyncCMD.append('--log-file={}'.format(logFullName))
            # sys.stdout = open(logFullName, 'a')
            # LOG = print("starting rSync for section:{0}".format(sectionName), fName=logFullName)
            print('#'*80)
            print('#'*80)


    # print (baseRSyncCMD); sys.exit()


        # - Elaborazione della section interessata.
    keyDONE = ['var', 'x']  # keyPrefix da saltare
    for key, val in workingSECT.items():
        key1, rest = key.split('.', 1)
        if key1 in keyDONE: continue        # l'abbiamo gi�  analizzata oppure è una var. o x.

        sourcePART = workingSECT[key1 + '.SOURCE'].split(',')
        destPART   = workingSECT[key1 + '.DEST'].split(',')
        subDirs    = workingSECT[key1 + '.SubDirs'].split(',')
        keyDONE.append(key1)
        # print(subDirs)
        # continue
        for subDir in subDirs:
            subDir = subDir.strip()
            if not subDir: continue

            rSyncCMD = prepareRsyncCommand(baseRSyncCMD[:], sourcePART, destPART, subDir)

            print('........... {} ...............'.format(TYPE_OF_COMMAND))
            if TYPE_OF_COMMAND == 'OS_SYSTEM':
                print(' '.join(rSyncCMD))
                # rCode = os.system(' '.join(rSyncCMD))
                # print (rCode)

            elif TYPE_OF_COMMAND == 'CALL':
                print(' '.join(rSyncCMD))
                rCode = subprocess.call(' '.join(rSyncCMD), stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
                print('-'*60)
                print("process for subDir: {0} completed. [rCode={1}]".format(subDir, rCode))
                print('-'*60)



            elif TYPE_OF_COMMAND == 'CHECK_OUTPUT':
                res = subprocess.check_output(rSyncCMD, stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
                res = res.decode('utf-8')                                           # converti in STRing


    if logFullName:
        print("process for sectionName: {0} completed.".format(sectionName), quit=True)



