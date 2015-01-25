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
    myPaths = []

    if thisModuleDIR.endswith('.zip'):
        ZIP = True
        myPaths.extend([
            os.path.normpath('{0}'.format(thisModuleDIR) ) ,
        ])
    else:
        ZIP = False
        myPaths.extend([
            os.path.normpath('{0}'.format(thisModuleDIR) ) ,
            os.path.normpath('{0}'.format('../') ) ,    # Per cercare le LnFunctionsNew
        ])

    myPaths.reverse()
    for path in myPaths: sys.path.insert(0, path)
    os.environ['PYTHONPATH'] = os.pathsep.join(myPaths)

    if ZIP:
        import LnFunctions    as ln
    else:
        import LnFunctionsNew as ln

    return ln


class LnClass(): pass

################################################################################
# - getSectionItem
################################################################################
def getSectionItem(rSyncCMD, sourceBaseDir, destBaseDir, subDir, sourceHOST, destHOST):
    # p = LnClass()
    # p.sourceDir = []
    # p.destDir = []
    # p.rSyncOPT = []
    rsyncOPT = []

    subDir = subDir.strip()
    if not subDir: return []
    if not subDir[-1] == '/': subDir += '/'
    sourceDir = "{}/{}".format(sourceBaseDir.strip(), subDir)
    destDir   = "{}/{}".format(destBaseDir.strip(), subDir)

        # convert to cygWin path
    sourceHOST = 'REMOTE'
    if not sourceDir[0] == '/' and sourceDir[1] == ':':
        sourceDir = '/cygdrive/' + sourceDir[0] + sourceDir[2:].replace('\\', '/')
        sourceHOSTType = 'WINDOWS'
        if gv.OpSys.upper() == 'WINDOWS':
            sourceHOST = 'LOCAL'

    destHOST = 'REMOTE'
    if not destDir[0] == '/' and destDir[1] == ':':
        destDir = '/cygdrive/' + destDir[0] + destDir[2:].replace('\\', '/')
        destHOSTType = 'WINDOWS'
        if gv.OpSys.upper() == 'WINDOWS':
            destHOST = 'LOCAL'

    XFER_TYPE = '{}_TO_{}'.format(sourceHOST, destHOST)


    # OPTIONS
    for key, val in optionSECT.items():
        key0, key1 = key.split('.')

        if XFER_TYPE        == 'LOCAL_TO_LOCAL' and key1.startswith('LR_'): continue
        if destHOSTType     == 'WINDOWS'        and key1.startswith('LINUX_'): continue
        if not destHOSTType == 'WINDOWS'        and key1.startswith('WIN_'): continue
        if key1 == 'EXCLUDE':
            for item in val.split():
                # rsyncOPT.append('--exclude {}'.format(item))
                rsyncOPT.append('--exclude')
                rsyncOPT.append(item)
        else:
            rsyncOPT.append(val)

    rSyncCMD.extend(rsyncOPT)


    if sourceHOST == 'LOCAL':
        rSyncCMD.append('"{}"'.format(sourceDir))
    else:
        rSyncCMD.append('"{}{}"'.format(sourceHost, sourceDir))

    if destHOST   == 'LOCAL':
        rSyncCMD.append('"{}"'.format(destDir))
    else:
        rSyncCMD.append('"{}{}"'.format(destHost, destDir))


    print ()
    print ('*'*50)
    print ('*   XFER_TYPE:  {}_TO_{}'.format(sourceHOST, destHOST))
    print ('*   sourceDir:  {}'.format(sourceDir))
    print ('*   destDir:    {}'.format(destDir))
    print (' '.join(rSyncCMD))
    print ('*'*50)
    print ()

    return rSyncCMD


################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    ln = preparePATHs()
    gv = ln.gv              # shortLink
    gv.fCONSOLE = False
        # - Apertura LOG
    ln.wrLog("Apertura - log:{}".format(gv.logFname), fName=gv.logFname)

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
    if len(sys.argv) < 3:
        print('''
        Immettere:
            file.ini:       nome del file di configurazione
            sectionName:    [section] da processare
            ''')
        sys.exit()

    iniFileName = sys.argv[1]
    sectionName = sys.argv[2]


    TYPE_OF_COMMAND = 'OS_SYSTEM'
    TYPE_OF_COMMAND = 'CALL'
    # iniFileName     = 'Portit-Backup.ini'
    INIcParse, INI = ln.readIniFile(iniFileName, RAW=False)
    # ln.printINIconfigparser(INIcParse)

    try:
            # Path Section
        pathSECT        = INI['PATH']

            # Options Section
        optionSECT      = INI['OPTIONS_' + TYPE_OF_COMMAND]

            # Options Section
        # dirsSECT      = INI['DIRECTORY']

        dirsSECT      = INI[sectionName]
        sourceHOST      = dirsSECT['sourceHOST']; del dirsSECT['sourceHOST']
        destHOST        = dirsSECT['destHOST'];   del dirsSECT['destHOST']

        # sourceHostType   = dirsSECT['sourceHOSTType']; del dirsSECT['sourceHOSTType']
        # dstHostType     = dirsSECT['dstHOSTType']; del dirsSECT['dstHOSTType']

        # XFR_TYPE      = dirsSECT['XFR_TYPE']
        # sourceHost, toHost = dirsSECT['HOSTS'].split(',')
        # del dirsSECT['XFR_TYPE']

            # Main Section
        mainSECT        = INI['MAIN']
        # remoteHost      = mainSECT['REMOTE_HOST']
        RSYNC_Program   = mainSECT['RSYNC_Program']

    except (Exception) as why:
        print("Errore nella lettura del parametro: {}".format(str(why)))
        sys.exit(-1)

        # aggiungiamo i percorsi nelle PATH
    for key, val in pathSECT.items():
        sys.path.insert(0, val.strip())

    '''
    rsyncOPT = []
    if toHost.upper() == 'LOCAL'  and gv.OpSys.upper() == 'WINDOWS':
    if toHost.upper() == 'LOCAL'  and gv.OpSys.upper() == 'WINDOWS':
        for key, val in optionSECT.items():
            key0, key1 = key.split('.')
            if key1 in ['LINUX_SSH', 'LINUX_SUDO', 'COMPRESS', 'LINUX_CHMOD', 'ICONV']:
                continue
            rsyncOPT.append(val)


    if toHost.upper() == 'REMOTE' and gv.OpSys.upper() == 'WINDOWS':


    if sourceHost.upper() == 'LOCAL':


    if TYPE_OF_COMMAND in ['OS_SYSTEM', 'CALL']:
        for key, val in optionSECT.items():
            if XFR_TYPE == 'LOCAL_TO_LOCAL':
                key0, key1 = key.split('.')
                if key1 in ['LINUX_SSH', 'LINUX_SUDO', 'COMPRESS', 'LINUX_CHMOD', 'ICONV']:
                    continue
            rsyncOPT.append(val)

            # da testare
    elif TYPE_OF_COMMAND == 'CHECK_OUTPUT':
        for key, val in optionSECT.items():
            lista = val.split('_,_ ')
            for param in lista:
                rsyncOPT.append(param.strip())


    baseRSyncCMD = []
    baseRSyncCMD.append(RSYNC_Program)
    baseRSyncCMD.append(DRY_RUN)
    baseRSyncCMD.extend(rsyncOPT)
    # print (baseRSyncCMD)
    # sys.exit()
    if XFR_TYPE == 'LOCAL_TO_REMOTE':
        remoteHost += ':'
    else:
        remoteHost = ''

    '''
    baseRSyncCMD = []
    baseRSyncCMD.append(RSYNC_Program)
    baseRSyncCMD.append(DRY_RUN)

    for key, val in dirsSECT.items():
        if key.startswith('var.'):  continue
        if key.startswith('x.'):    continue


        sourceBaseDir, destBaseDir, rest = val.split(',', 2)

        subDirs = rest.split(',')
        for subDir in subDirs:
            if not subDir: continue
            rSyncCMD = getSectionItem(baseRSyncCMD[:], sourceBaseDir, destBaseDir, subDir, sourceHOST, destHOST)
            # print (rSyncCMD)
            # continue

            print('........... {} ...............'.format(TYPE_OF_COMMAND))
            if TYPE_OF_COMMAND == 'OS_SYSTEM':
                print(' '.join(rSyncCMD))
                rCode = os.system(' '.join(rSyncCMD))
                print (rCode)

            elif TYPE_OF_COMMAND == 'CALL':
                print(' '.join(rSyncCMD))
                rCode = subprocess.call(' '.join(rSyncCMD), stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
                print (rCode)

            elif TYPE_OF_COMMAND == 'CHECK_OUTPUT':
                res = subprocess.check_output(rSyncCMD, stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
                res = res.decode('utf-8')                                           # converti in STRing



