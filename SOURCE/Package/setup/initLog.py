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

import os, sys
import platform
import logging



# #####################################
# # Init LOG
# #####################################
def initLog(gv):
    myLogger    = gv.LN.logger
    log         = gv.LOG

    OpSys  = platform.system()
    logger = myLogger.init(log.loggerID, log.logDir, log.fileName, maxBytes=log.maxBytes, nFiles=log.nFiles)

        # ---------------------------------------------------------------------------------
        # Posso scrivere in due modi sul log:
        #   1 - logger.info()   - utilizzo direttamente sul logger
        #   2 - myLogger.info() - utilizzo le funzioni all'interno di LnLogger.py
        # importante l'ordine per non vedere l'output del file su console
        # ---------------------------------------------------------------------------------
    myLogger.setConsoleLevel(eval(log.levelConsole))
    myLogger.setFileLevel(eval(log.levelFile))

    myLogger.setShortLine()
    myLogger.info("Program started")

    os.environ['LoggerID'] = log.loggerID # per gli altri moduli
    gv.LOG.logger          = logger

    myLogger.setConsoleAnyway(False)              # flag to display error messages before logfile is opened

    return
