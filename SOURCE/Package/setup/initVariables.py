#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys, logging

class myClass():
    pass

def initVariables(gv):


    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    gv.STATUS                       = myClass()               # lo aggangiamo come sotto-insieme del gv
    gv.STATUS.DIR_NOT_FOUND         = 'DIR NOT FOUND'
    gv.STATUS.DIR_ALREADY_EXISTS    = 'DIR ALREADY EXISTs'
    gv.STATUS.CONFIG_NOT_FOUND      = 'CONFIG NOT FOUND'
    gv.STATUS.CONFIG_FILE_ERROR     = 'CONFIGURATION File Error'
    gv.STATUS.CONFIG_OK             = 'CONFIGURATION OK'
    gv.STATUS.INSTALLED             = 'INSTALLED'
    gv.STATUS.NO_AUTO_STOP          = 'NO AUTO-STOP'
    gv.STATUS.NO_AUTO_START         = 'NO AUTO-START'
    gv.STATUS.ALREADY_STOPPED       = 'ALREADY STOPPED'
    gv.STATUS.ALREADY_RUNNING       = 'ALREADY RUNNING'
    gv.STATUS.STOPPING              = 'STOPPING'
    gv.STATUS.NOT_RUNNING           = 'NOT RUNNING'
    gv.STATUS.RUNNING               = 'RUNNING'
    gv.STATUS.UNSTABLE              = 'Unrecognized Status - UNSTABLE'
    gv.STATUS.OK                    = 'OK'
    gv.STATUS.NOT_OK                = 'NOT OK'
    gv.STATUS.PROC_WAIT_TIMEOUT     = 'ERROR - Timeout occurs during Process WAITing'


    gv.RCODE  = myClass()               # lo aggangiamo come sotto-insieme del gv
    gv.RCODE.shortStatus            = ""
    gv.RCODE.errMsg                 = ""
    gv.RCODE.statusMsg              = ""


    gv.INP_PARAM                    = myClass()                     # Dati passati come parametri
    gv.INP_PARAM.fDEBUG             = False
    gv.INP_PARAM.action             = "TEST"                        # TEST - GO - DRY-RUN
    gv.INP_PARAM.actionUPP          = gv.INP_PARAM.action.upper()
    gv.INP_PARAM.mainCfgFile        = None
    gv.INP_PARAM.SECTION_NAME       = None


    gv.INI                          = myClass()                     # Dati relativi alla configurazione del file.ini
    gv.INI.RSYNC_PROGRAM            = None
    gv.INI.GREP_PROGRAM             = None


    gv.CONFIG                       = myClass()                     # Dati relativi alla configurazione del file applicativo.cfg


    gv.FLOW                         = myClass()                     # Dati relativi alla configurazione del file applicativo.cfg



    gv.LOG = myClass()
    gv.LOG.logDir          = None
    gv.LOG.fileName        = None
    gv.LOG.levelFile       = None
    gv.LOG.levelConsole    = None
    gv.LOG.loggerID        = None
    gv.LOG.nFiles          = 0
    gv.LOG.maxBytes        = 0
    gv.LOG.logger          = None



    logger.info('exiting - [called by:%s]' % (calledBy(1)))

