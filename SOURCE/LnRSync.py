#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Programma per la gestione start/stop di un'istanza di JBoss EAP 6.x
#                                               by Loreto Notarantonio 2013, February
# Comando per eseguire uno script all'interno di uno ZIP file:
#        SET PYTHONPATH=JBossStart_LNf.zip python -m JBossStart [parameters]
#     oppure creare un file che si chiama __main__.py e lanciare il comando:
#        python JBossStart_LNf.zip [parameters]
# ######################################################################################


# RSync log interpretation: http://stackoverflow.com/questions/4493525/rsync-what-means-the-f-on-rsync-logs

import os, sys
import textwrap
import __main__ as mainwrapper

class myClass():
    def __dir__(self):  # forse non serve
        pass

################################################################################
# - M A I N
# - Prevede:
# -  1 - Impostazioni dei path per il corretto import dei moduli personali
# -  3 - Lettura del file di configurazione applicazione (per logFile)
# -  4 - Inizializzazione del logger
# -  2 - Controllo parametri di input per capire il file di config da utilizzare
# -  5 - Chiamata al programma principale del progetto
################################################################################
def Main(gv, args):
    LN          = gv.LN
    Prj         = gv.Prj
    calledBy    = gv.LN.sys.calledBy


        # ------------------------------------------------------------------------------------
        # - Inizializzazione di variabili globali
        # ------------------------------------------------------------------------------------
    Prj.setup.initVariables(gv)                                               # Imposta i valori JBStatus

        # ------------------------------------------------------------------------------------
        # - Leggiamo il file di configurazione di base per inizializzare il file di LOG
        # ------------------------------------------------------------------------------------
    iniFileName = gv.scriptName + '.ini' if gv.OpSys.upper() != 'WINDOWS' else gv.scriptName + 'Win.ini'
    logInfo     = Prj.setup.readIniConfig(gv, os.path.join(gv.mainConfigDIR, iniFileName))


        # --------------------------------------------------------
        # SetUp del log
        # --------------------------------------------------------
    Prj.setup.initLog(gv)

        # --------------------------------------------------------------------------
        # - lettura degli Input parameters
        # --------------------------------------------------------------------------
    options = Prj.setup.parseInput(gv)
    fDEBUG = gv.INP_PARAM.fDEBUG
    if fDEBUG: LN.dict.printDictionaryTree(gv, gv.INP_PARAM, header="INPUT Parameters [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)

        # =======================================
        # - Lettura del file di configurazione
        # =======================================
    MainDICT    = Prj.readConfig(gv, cfgFileName=gv.INP_PARAM.mainCfgFile)
    if fDEBUG: LN.dict.printDictionaryTree(gv, MainDICT, header="Main Configuration File data [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)

    sectionDICT  = Prj.readConfig(gv, sectionName=gv.INP_PARAM.SECTION_NAME)
    if fDEBUG: LN.dict.printDictionaryTree(gv, sectionDICT, header="Section Configuration File data [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)

    # Prj.exit(gv, 9999, "Uscita Temporanea - [called by: %s] " % (calledBy(1)))

    if MainDICT and sectionDICT:
        for flowName in sectionDICT.keys():
            if flowName.upper().startswith('FLUSSO'):
                flowID    = sectionDICT[flowName]
                flowVARs  = Prj.readConfig(gv, flowID=flowID)   # ritorna un dictionary con tutti i valori necessari per eseguire rSync
                if fDEBUG: LN.dict.printDictionaryTree(gv, flowVARs, header="Flow-VARs [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)
                Prj.flowProcess(gv, flowID, flowVARs)


    # LN.dict.printDictionaryTree(gv, gv, header="Main variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)
    return
    Prj.exit(gv, 9999, "Uscita Temporanea - [called by: %s] " % (calledBy(1)))
























    # cfgFile     = gv.INP_PARAM.mainCfgFile
    cfgDICT = Prj.readConfig(gv, gv.INP_PARAM.mainCfgFile, gv.INP_PARAM.SECTION_NAME)

    # (cfgMODULE, cfgDICT, cfgPATH, cfgFULLPATH) =  LN.dict.loadDictFile(gv, cfgFile, moduleName=None, fDEBUG=False)
    if not cfgDICT:
        Prj.exit(gv, 11, "[%-12s] - file %s NOT Found. It's mandatory." % (gv.projectID, cfgFile) )


    if gv.INP_PARAM.SECTION_NAME == None:
        Prj.exit(gv, 12, "[%-12s] - Immettere il nome della sezione. It's mandatory." )
    else:
        sectionID = cfgDICT.get(gv.INP_PARAM.SECTION_NAME, {})

    # for section in cfgDICT.sections():        print section

    if gv.INP_PARAM.fDEBUG:
        print "ciao"
        LN.dict.printDictionaryTree(gv, vars(sectionID), retCols='TV', lTAB=' '*4, console=True)

    print sectionID
    if not hasattr(cfgDICT, "Main"):
        Prj.exit(gv, 11, "Main{} section NOT present in file"  )


if __name__ == "__main__":
    Main(sys.argv)