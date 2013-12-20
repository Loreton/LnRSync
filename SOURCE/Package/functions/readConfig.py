#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os

class myClass():    pass


RSYNC_BASE_OPTIONS      = 'rSync BASE Options'
RSYNC_EXCLUDED_PATTERN  = 'rSync EXCLUDED PATTERN'
RSYNC_OTHER_OPTIONS     = 'rSync OTHER Options'
RSYNC_LOG_FILE          = 'rSync LOG FILE'

CONFIG_FILE_ID          = 'Config File ID'
SOURCE_SYSTEM           = 'Source System'
SOURCE_HOST             = 'Source HOST'
SOURCE_ROOT_DIR         = 'Source ROOT Dir'

TARGET_SYSTEM           = 'Target System'
TARGET_HOST             = 'Target HOST'
TARGET_ROOT_DIR         = 'Target ROOT Dir'

ACTION                  =  'Action'
COMMAND_TYPE            =  'Type of Command'
GREP_PROGRAM            =  'grep Program'
GREP_OPTIONS            =  'grep options'
RSYNC_PROGRAM           =  'rSync Program'


# #######################################################################
# # Lettura del file di configurazione
# # Esci se le sezioni di interesse non esistono
# #######################################################################
def readCONFIG(gv, cfgFileName=None, sectionName=None, flowID=None):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    xxID = None


        # ---------------------------------------------------------------------
        # - Leggiamo le variabili lette dalla Sezione MAIN
        # ---------------------------------------------------------------------

    if cfgFileName:
        # ----------------------------------------------------------------------
        # - Lettura del file di configurazione
        # - Leggiamo anche i valori considerati Mandatory
        # ----------------------------------------------------------------------
        (cfgMODULE, cfgDICT, cfgPATH, cfgFULLPATH) =  LN.dict.loadDictFile(gv, cfgFileName, moduleName=None, fDEBUG=False)
        if not hasattr(cfgMODULE, "Main"):
            Prj.exit(gv, 97, "Main{} section NOT present in %s file" % (cfgFileName) )

        gv.CONFIG.CONFIG_FILE_ID = cfgMODULE    # SAVE module pointer

            # --------------------------------------------------------
            # - Pointers delle sezioni di interesse
            # --------------------------------------------------------
        MainID = cfgMODULE.Main

            # --------------------------------------------------------
            # - Leggiamo tutte le variabili di nostro interesse
            # --------------------------------------------------------
        gv.CONFIG.COMMAND_TYPE              = MainID.get(COMMAND_TYPE,    '')
        gv.CONFIG.GREP_OPTIONS              = MainID.get(GREP_OPTIONS,    '')
        gv.CONFIG.RSYNC_BASE_OPTIONS        = MainID.get(RSYNC_BASE_OPTIONS,    '')
        gv.CONFIG.RSYNC_EXCLUDED_PATTERN    = MainID.get(RSYNC_EXCLUDED_PATTERN,    '')
        gv.CONFIG.RSYNC_OTHER_OPTIONS       = MainID.get(RSYNC_OTHER_OPTIONS,    '')
        gv.CONFIG.RSYNC_LOG_FILE            = MainID.get(RSYNC_LOG_FILE,    None)

            # --------------------------------------------------------
            # - Siccome alcune variabili potrebbero essere spezzate su più linee,
            # - analizziamo per verificare se esistono aggiunte.
            # - il formato è:
            # -     'varName'       : 'value'
            # -     'varName.+01'   : 'value1'
            # -     'varName.+02'   : 'value2'
            # -  il risultato dovrà essere 'value value1 value2'
            # --------------------------------------------------------
        gv.CONFIG.RSYNC_BASE_OPTIONS        = appendReplCFGVars2(gv, varName=RSYNC_BASE_OPTIONS,        currValue=gv.CONFIG.RSYNC_BASE_OPTIONS, sourceID=MainID )
        gv.CONFIG.GREP_OPTIONS              = appendReplCFGVars2(gv, varName=GREP_OPTIONS,              currValue=gv.CONFIG.GREP_OPTIONS, sourceID=MainID )
        gv.CONFIG.RSYNC_EXCLUDED_PATTERN    = appendReplCFGVars2(gv, varName=RSYNC_EXCLUDED_PATTERN,    currValue=gv.CONFIG.RSYNC_EXCLUDED_PATTERN, sourceID=MainID )
        gv.CONFIG.RSYNC_OTHER_OPTIONS       = appendReplCFGVars2(gv, varName=RSYNC_OTHER_OPTIONS,       currValue=gv.CONFIG.RSYNC_OTHER_OPTIONS, sourceID=MainID )


        # LN.dict.printDictionaryTree(gv, gv.CONFIG, header="CONFIG variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)




        # LN.dict.printDictionaryTree(gv, MainID, header="Main variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)








        # sys.exit()


        '''
        '''










        # if gv.INP_PARAM.actionUPP != 'GO':
        #     gv.CONFIG.RSYNC_BASE_OPTIONS = '--dry-run %s' % (gv.CONFIG.RSYNC_BASE_OPTIONS)

        logDir  = logger.getLogDir()
        gv.CONFIG.RSYNC_LOG_FILE = '--log-file=' + logDir + '/' + gv.CONFIG.RSYNC_LOG_FILE



        xxID = MainID

        # ---------------------------------------------------------------------
        # - Leggiamo le variabili lette dalla Sezione richiesta
        # - proviamo prima con il case passato e poi in uppercase
        # ---------------------------------------------------------------------
    if sectionName:
        cfgMODULE = gv.CONFIG.CONFIG_FILE_ID
        if not hasattr(cfgMODULE, sectionName):
            sectionName = sectionName.upper()
            if not hasattr(cfgMODULE, sectionName.upper()):
                Prj.exit(gv, 201, "%s{} section NOT present in %s file" % (sectionName, cfgFileName) )

            # ---------------------------------------------------
            # - Lettura della funzione nel file.cfg
            # - e trasformazione della stessa in dict
            # ---------------------------------------------------
        myFunction = getattr(cfgMODULE, sectionName)      # otteniamo il l'attributo relativo alla funzione
        sectionID  = myFunction()                         # Otteniamo pointer come dictionary.

        gv.CONFIG.COMMAND_TYPE              = appendReplCFGVars2(gv, sourceID=sectionID, varName=COMMAND_TYPE,     currValue=gv.CONFIG.COMMAND_TYPE)
        gv.CONFIG.GREP_OPTIONS              = appendReplCFGVars2(gv, sourceID=sectionID, varName=GREP_OPTIONS,           currValue=gv.CONFIG.GREP_OPTIONS)
        gv.CONFIG.RSYNC_BASE_OPTIONS        = appendReplCFGVars2(gv, sourceID=sectionID, varName=RSYNC_BASE_OPTIONS,     currValue=gv.CONFIG.RSYNC_BASE_OPTIONS)
        gv.CONFIG.RSYNC_EXCLUDED_PATTERN    = appendReplCFGVars2(gv, sourceID=sectionID, varName=RSYNC_EXCLUDED_PATTERN, currValue=gv.CONFIG.RSYNC_EXCLUDED_PATTERN)
        gv.CONFIG.RSYNC_OTHER_OPTIONS       = appendReplCFGVars2(gv, sourceID=sectionID, varName=RSYNC_OTHER_OPTIONS,    currValue=gv.CONFIG.RSYNC_OTHER_OPTIONS)


        # LN.dict.printDictionaryTree(gv, gv.CONFIG, header="CONFIG variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)


        # gv.CONFIG.COMMAND_TYPE            = appendReplCFGVars(gv, varName=COMMAND_TYPE,          currValue=gv.CONFIG.COMMAND_TYPE,              newValue=sectionID.get(COMMAND_TYPE) )
        # gv.CONFIG.GREP_OPTIONS            = appendReplCFGVars(gv, varName=GREP_OPTIONS,          currValue=gv.CONFIG.GREP_OPTIONS,              newValue=sectionID.get(GREP_OPTIONS) )
        # gv.CONFIG.RSYNC_BASE_OPTIONS      = appendReplCFGVars(gv, varName=RSYNC_BASE_OPTIONS,    currValue=gv.CONFIG.RSYNC_BASE_OPTIONS,        newValue=sectionID.get(RSYNC_BASE_OPTIONS) )
        # gv.CONFIG.RSYNC_EXCLUDED_PATTERN  = appendReplCFGVars(gv, varName=RSYNC_EXCLUDED_PATTERN,currValue=gv.CONFIG.RSYNC_EXCLUDED_PATTERN,    newValue=sectionID.get(RSYNC_EXCLUDED_PATTERN) )
        # gv.CONFIG.RSYNC_OTHER_OPTIONS     = appendReplCFGVars(gv, varName=RSYNC_OTHER_OPTIONS,   currValue=gv.CONFIG.RSYNC_OTHER_OPTIONS,       newValue=sectionID.get(RSYNC_OTHER_OPTIONS) )

        xxID = sectionID

        # ============================================================
        # = Analisi del singolo Flusso
        # ============================================================
    if flowID:
        gv.FLOW = myClass()             # Azzeramento di tutti i valori precedenti (se esistevano)

        # gv.FLOW.COMMAND_TYPE            = appendReplCFGVars(gv, varName=COMMAND_TYPE,          currValue=gv.CONFIG.COMMAND_TYPE,              newValue=flowID.get(COMMAND_TYPE) )
        # gv.FLOW.GREP_OPTIONS            = appendReplCFGVars(gv, varName=GREP_OPTIONS,          currValue=gv.CONFIG.GREP_OPTIONS,              newValue=flowID.get(GREP_OPTIONS) )
        # gv.FLOW.RSYNC_BASE_OPTIONS      = appendReplCFGVars(gv, varName=RSYNC_BASE_OPTIONS,    currValue=gv.CONFIG.RSYNC_BASE_OPTIONS,        newValue=flowID.get(RSYNC_BASE_OPTIONS) )
        # gv.FLOW.RSYNC_EXCLUDED_PATTERN  = appendReplCFGVars(gv, varName=RSYNC_EXCLUDED_PATTERN,currValue=gv.CONFIG.RSYNC_EXCLUDED_PATTERN,    newValue=flowID.get(RSYNC_EXCLUDED_PATTERN) )
        # gv.FLOW.RSYNC_OTHER_OPTIONS     = appendReplCFGVars(gv, varName=RSYNC_OTHER_OPTIONS,   currValue=gv.CONFIG.RSYNC_OTHER_OPTIONS,       newValue=flowID.get(RSYNC_OTHER_OPTIONS) )

        gv.FLOW.COMMAND_TYPE              = appendReplCFGVars2(gv, sourceID=flowID, varName=COMMAND_TYPE,           currValue=gv.CONFIG.COMMAND_TYPE)
        gv.FLOW.GREP_OPTIONS              = appendReplCFGVars2(gv, sourceID=flowID, varName=GREP_OPTIONS,           currValue=gv.CONFIG.GREP_OPTIONS)
        gv.FLOW.RSYNC_BASE_OPTIONS        = appendReplCFGVars2(gv, sourceID=flowID, varName=RSYNC_BASE_OPTIONS,     currValue=gv.CONFIG.RSYNC_BASE_OPTIONS)
        gv.FLOW.RSYNC_EXCLUDED_PATTERN    = appendReplCFGVars2(gv, sourceID=flowID, varName=RSYNC_EXCLUDED_PATTERN, currValue=gv.CONFIG.RSYNC_EXCLUDED_PATTERN)
        gv.FLOW.RSYNC_OTHER_OPTIONS       = appendReplCFGVars2(gv, sourceID=flowID, varName=RSYNC_OTHER_OPTIONS,    currValue=gv.CONFIG.RSYNC_OTHER_OPTIONS)

        # LN.dict.printDictionaryTree(gv, gv.FLOW, header="CONFIG variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)

        # sys.exit()


            # - Lettura Hosts e Directory di Base
        sourceSystem                 = flowID.get(SOURCE_SYSTEM)
        targetSystem                 = flowID.get(TARGET_SYSTEM)
        if not sourceSystem:
            Prj.exit(gv, 2001, "Source SYSTEM not defined.")
        if not targetSystem:
            Prj.exit(gv, 2002, "Target SYSTEM not defined.")


        # gv.FLOW.SOURCE_SYSTEM  = flowID.get(SOURCE_SYSTEM)
        # gv.FLOW.TARGET_SYSTEM  = flowID.get(TARGET_SYSTEM)


        targetHost, targetRootDIR    = targetSystem.split(':/')
        sourceHost, sourceRootDIR    = sourceSystem.split(':/')

        if sourceRootDIR[0]         != '/': sourceRootDIR = '/' + sourceRootDIR
        if targetRootDIR[0]         != '/': targetRootDIR = '/' + targetRootDIR
        if sourceRootDIR[-1]        == '/': sourceRootDIR[:-1]
        if targetRootDIR[-1]        == '/': targetRootDIR[:-1]

        gv.FLOW.SOURCE_ROOT_DIR = sourceRootDIR
        gv.FLOW.TARGET_ROOT_DIR = targetRootDIR
        gv.FLOW.SOURCE_HOST     = sourceHost
        gv.FLOW.TARGET_HOST     = targetHost
        gv.FLOW.RSYNC_PROGRAM   = gv.INI.RSYNC_PROGRAM
        gv.FLOW.GREP_PROGRAM    = gv.INI.GREP_PROGRAM
        gv.FLOW.RSYNC_LOG_FILE  = gv.CONFIG.RSYNC_LOG_FILE

        xxID = gv.FLOW

    return xxID





########################################################################
# - Provvede a rimpiazzare una variabile con nuovo valore
# - Se il nuovo==None allora lascia il vecchio
########################################################################
import types
def appendReplCFGVars(gv, varName, currValue, newValue=None, sepChar=' '):
    logger = gv.LN.logger

    newVar = currValue

    if newValue == None:
        newVar = currValue

    elif isinstance(newValue, types.BooleanType):
        newVar = newValue

    elif len(newValue) == 0:
        newVar = ''

    else:
        if newValue[0] == '+':
            newVar += sepChar + newValue[1:].strip()
        else:
            newVar += sepChar + newValue.strip()

    logger.info('get var: "%s"' % (varName) )
    logger.info("      READ  :[%s]" % (newValue) )
    logger.info("      BEFORE:[%s]" % (currValue) )
    logger.info("      AFTER :[%s]" % (newVar) )
    return newVar

########################################################################
# - Provvede a rimpiazzare una variabile con nuovo valore
# - Se il nuovo==None allora lascia il vecchio
########################################################################
import types
def appendReplCFGVars2(gv, varName, currValue, sourceID, sepChar='.+'):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))



    baseValue = currValue
    appendValue = []
    for key, value in sourceID.items():
        if key == varName:
            baseValue = value
        elif key.startswith(varName + '.+'):
            appendValue.append(value)


    if appendValue:
        retValue = baseValue + ' ' + ' '.join(appendValue)
    else:
        retValue = baseValue



    logger.info('get var: "%s"'     % (varName) )
    logger.info("      PASSED:[%s]" % (currValue) )
    logger.info("      BEFORE:[%s]" % (baseValue) )
    logger.info("      READ  :[%s]" % (appendValue) )
    logger.info("      AFTER :[%s]" % (retValue) )


    fDEBUG = False
    if fDEBUG:
        print "%s = %s" % (varName, currValue)
        print "%s = %s" % (varName, retValue)
        LN.dict.printDictionaryTree(gv, sourceID, header="SourceID variables [%s]" % calledBy(0), retCols='TV', lTAB=' '*4, console=True)
        choice = LN.sys.getKeyboardInput(gv, "Pausa per visualizzazione.", validKeys='ENTER', exitKey='X')
    return retValue