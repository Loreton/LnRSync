#!/usr/bin/python3
import sys, os

from . GlobalVars import GlobalVars as gv


LOG = None

# ##############################################################
# #
# ##############################################################
def wrLog(data='', fName=None, exitCode=None):
    global LOG
    lineNO = sys._getframe( 1 ).f_lineno    # ottieni la riga del chiamante

    if exitCode: data = data + ' [exiting]'

    if (fName):
        try:
            LOG = open(fName, "wb")
            if gv.fCONSOLE: print("Using log file:" + fName)

        except (IOError, os.error) as why:
            sys.exit("ERROR writing file - {}".format(str(why)))

    if (LOG):
        dataLog = '[{}] {}'.format(lineNO, data)
        LOG.write(bytes(dataLog + '\n', 'UTF-8'))


    if gv.fCONSOLE:
        print('    ', data)

    if gv.fSYSLOG:
        syslog.syslog(syslog.LOG_INFO, "Loreto - [{:<15}] - {}".format(gv.UUID, data))

    if exitCode:
        if LOG:
            LOG.close()
        sys.exit(exitCode)

    return LOG