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
    print (thisModuleDIR)
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
        print (path)
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
def prepareServerPath(partner, subDir, hostSepCahr):
    TYPE, SERVER, dirName = partner.split(hostSepCahr, 2)
    baseDir   = dirName.strip()
    hostName  = SERVER.strip()

    if not subDir[-1] == '/': subDir += '/'
    fullDir = "{}/{}".format(baseDir.strip(), subDir)

        # convert to cygWin path (if required)
    if fullDir[1] == ':' and not fullDir[0] == '/':
        fullDir = '/cygdrive/' + fullDir[0] + fullDir[2:].replace('\\', '/')

    if TYPE.strip() == 'SOURCE':
        gv.SOURCE.HostName  = 'LOCAL' if hostName == 'LOCAL' else hostName
        gv.SOURCE.PATH      = fullDir
        if gv.OpSys.upper() == 'WINDOWS': gv.SOURCE.HostType = 'WINDOWS'
    else:
        gv.DEST.HostName    = 'LOCAL' if hostName == 'LOCAL' else hostName
        gv.DEST.PATH        = fullDir
        if gv.OpSys.upper() == 'WINDOWS': gv.DEST.HostType = 'WINDOWS'




################################################################################
# - getSectionItem
################################################################################
def prepareRsyncCommand(rSyncCMD, hostSepCahr, partner01, partner02, subDir):

    prepareServerPath(partner01, subDir, hostSepCahr)
    prepareServerPath(partner02, subDir, hostSepCahr)
    rsyncOPT = []



    # OPTIONS
    XFER_TYPE = '{}_TO_{}'.format(gv.SOURCE.HostName, gv.DEST.HostName)
    for key, val in baseOptionSECT.items():
        if XFER_TYPE        == 'LOCAL_TO_LOCAL' and key.startswith('TO_FROM_REM.'): continue
        if gv.DEST.HostType == 'WINDOWS'        and key.startswith('LINUX.'): continue
        if gv.DEST.HostType != 'WINDOWS'        and key.startswith('WIN.'): continue
        if key.split('.')[-1] == 'EXCLUDE':
            for item in val.split():
                # rsyncOPT.append('--exclude {}'.format(item))
                rsyncOPT.append('--exclude')
                rsyncOPT.append(item)
        else:
            rsyncOPT.append(val)

    rSyncCMD.extend(rsyncOPT)


    if gv.SOURCE.HostName == 'LOCAL':
        rSyncCMD.append('"{}"'.format(gv.SOURCE.PATH))
    else:
        rSyncCMD.append('"{}:{}"'.format(gv.SOURCE.HostName, gv.SOURCE.PATH))

    if gv.DEST.HostName   == 'LOCAL':
        rSyncCMD.append('"{}"'.format(gv.DEST.PATH))
    else:
        rSyncCMD.append('"{}:{}"'.format(gv.DEST.HostName, gv.DEST.PATH))


    print ()
    print ('*'*50)
    print ('*   XFER_TYPE:  {}_TO_{}'.format(gv.SOURCE.HostName, gv.DEST.HostName))
    print ('*   sourceDir:  {}:{}'.format(gv.SOURCE.HostName, gv.SOURCE.PATH))
    print ('*   destDir:    {}:{}'.format(gv.DEST.HostName, gv.DEST.PATH))
    # print (' '.join(rSyncCMD))
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
        baseOptionSECT      = INI['RSYNC_OPTIONS']

        workingSECT     = INI[sectionName]
        hostSepCahr     = workingSECT['sepChar']; del workingSECT['sepChar']

            # Main Section
        mainSECT        = INI['MAIN']
        RSYNC_Program   = mainSECT['RSYNC_Program']

    except (Exception) as why:
        print("Errore nella lettura del parametro: {}".format(str(why)))
        sys.exit(-1)

        # aggiungiamo i percorsi nelle PATH
    for key, val in pathSECT.items():
        sys.path.insert(0, val.strip())

        # - preparazione comando di base
    baseRSyncCMD = []
    baseRSyncCMD.append(RSYNC_Program)
    baseRSyncCMD.append(DRY_RUN)



    gv.SOURCE = LnClass()
    gv.DEST   = LnClass()
    # gv.SOURCE.Loreto = 'Ciao'
    # gv.SOURCE.Loreto1 = 'Ciao1'

        # - Elaborazione della section interessata.
    for key, val in workingSECT.items():
        if key.startswith('var.'):  continue
        if key.startswith('x.'):    continue

        partner01, partner02, rest = val.split(',', 2)


        subDirs = rest.split(',')
        for subDir in subDirs:
            subDir = subDir.strip()
            if not subDir: continue

            rSyncCMD = prepareRsyncCommand(baseRSyncCMD[:], hostSepCahr, partner01, partner02, subDir)

            # sys.exit()
            # print (rSyncCMD)
            # continue


            print('........... {} ...............'.format(TYPE_OF_COMMAND))
            if TYPE_OF_COMMAND == 'OS_SYSTEM':
                print(' '.join(rSyncCMD))
                # rCode = os.system(' '.join(rSyncCMD))
                # print (rCode)

            elif TYPE_OF_COMMAND == 'CALL':
                print(' '.join(rSyncCMD))
                # rCode = subprocess.call(' '.join(rSyncCMD), stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
                # print (rCode)

            elif TYPE_OF_COMMAND == 'CHECK_OUTPUT':
                res = subprocess.check_output(rSyncCMD, stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
                res = res.decode('utf-8')                                           # converti in STRing





