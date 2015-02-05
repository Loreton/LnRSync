#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os; sys.dont_write_bytecode = True
import subprocess

class LnClass(): pass





################################################################################
# - inseriamo la lista delle dir dove possiamo trovare le LnFunctions
# - vale anche per quando siamo all'interno del .zip
################################################################################
def preparePATHs(fDEBUG):
    thisModuleDIR   = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    print (thisModuleDIR)
    if thisModuleDIR.endswith('.zip'):
        LnFunctionsPath = [ '../', '../../', '../../../' ]

    else:
        LnFunctionsPath = [ '.', '../', '../../',  ]

    LnFunctionsPath.reverse()
    for path in LnFunctionsPath:
        if fDEBUG: print ('......', path)
        sys.path.insert(0, os.path.abspath(os.path.join(thisModuleDIR, path)))

    import LnFunctionsLight as ln
    return ln

################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    ln = preparePATHs(fDEBUG=False)
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
        iniFileName = os.path.abspath(os.path.join(gv.scriptDir, sys.argv[1]))
        INIcParse, INI = ln.readIniFile(iniFileName, RAW=False)

    if len(sys.argv) < 3 :
        print('  Immettere anche il none della SECTION.')
        printSections(INIcParse)
        sys.exit()

    sectionName = sys.argv[2]

