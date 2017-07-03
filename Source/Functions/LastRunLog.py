#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
# by Loreto Notarantonio LnVer_2017-07-03_17.40.15
# ######################################################################################
import sys
import os


LAST_RUN    = None
lastRunData = []
#####################################################
# lastRUN()
#    fname not None: create and init
#####################################################
def LastRunLog(gv, data=None, fName=None, quit=False):
    global LAST_RUN, lastRunData

    cPrint = gv.Ln.LnColor()
    if (fName):
        if not os.path.isfile(fName):
            openMODE = 'wb'

        else:
            msg = 'Il file {0} esiste. Vuoi rimpiazzarlo? [y/N]'.format(fName)
            choice   = input(msg).strip()
            if choice.upper() == 'Y':
                openMODE    = 'wb'
                lastRunData = []

                # - leggiamo il file con gli ultimi RUN
            else:
                with open(fName) as f: lastRunData = f.read().splitlines()
                openMODE = 'ab+'

        try:
            LAST_RUN = open(fName, openMODE)
            cPrint.Yellow('lastRUN log file: {}'.format(fName), tab=4)

        except (IOError, os.error) as why:
            sys.exit("ERROR writing file - {}".format(str(why)))

    if (LAST_RUN) and data:
        LAST_RUN.write(bytes(data + '\n', 'UTF-8'))
        LAST_RUN.flush()
        lastRunData.append(data)

    if quit:
        if LAST_RUN:
            LAST_RUN.close()


    return lastRunData
