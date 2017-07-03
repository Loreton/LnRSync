#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
# by Loreto Notarantonio LnVer_2017-07-03_17.56.53
# ######################################################################################
import sys
import os


# ##############################################################
# - rSync LOG File
# ##############################################################
def rsyncLogFile(gv, LOG, sectionName, subDir):

    if   LOG.lower() in ( 'none', ''):
        logFileName = None

    elif LOG.lower() in ('true'):
        logFileName = gv.ini.MAIN.LOGDir + '/' + sectionName + '.' + subDir + '.log'

    else:
        logFileName = gv.ini.MAIN.LOGDir + '/' + LOG

    print ()
    print ('....', logFileName)
    print ()

    if logFileName and os.path.isfile(logFileName):
        os.remove(logFileName)

    return logFileName
