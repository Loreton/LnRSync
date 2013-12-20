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
OpSys        = platform.system()


# NON HO ancora il LOG ATTIVO

class myClass():
    pass



# ##########################################################
# # readIniFile
# # return:
# #     log.xx tutti i valori relativi al file di LOG
# #     pkg.xx il path del package LN_Package
# ##########################################################
def readIniConfigFile(gv, iniFileName):
    Prj         = gv.Prj
    LN          = gv.LN
    # logger      = gv.LN.logger          #  Ancora non lo abbiamo
    calledBy    = gv.LN.sys.calledBy

    import getpass, ConfigParser

    OpSys   = platform.system()
    tempDir = os.getenv('TEMP', 'c:\\temp') if OpSys == 'Windows' else os.getenv('tmp', '/tmp')
        # con l'utente come suffix per evitare eventuali conflitti
    outFname    = os.path.join(tempDir, 'LnTemp_%s.ini' % (getpass.getuser()))

        # -----------------------------------------
        # - copiamo file.ini to temp.ini
        # - facendo lo strip delle righe
        # - per evitare che il parser dia errore
        # -----------------------------------------
    finp = open(iniFileName,"r")
    fout = open(outFname, "wb")
    for line in finp:
        line = line.strip()
        fout.write(line + '\n')

    finp.close()
    fout.close()

    config = ConfigParser.ConfigParser()
    config.read(outFname)


    # Otteniamo il nome del file di Log e relativi livelli di debug
    # gv.LOG = myClass()

    try:
        gv.LOG.logDir          = config.get('LOG', 'logDir')

        gv.LOG.fileName        = config.get('LOG', 'logFileName')
        gv.LOG.levelFile       = config.get('LOG', 'LogLEVEL_file')
        gv.LOG.levelConsole    = config.get('LOG', 'LogLEVEL_console')
        gv.LOG.loggerID        = config.get('LOG', 'loggerID')
        gv.LOG.maxBytes        = config.getint('LOG', 'maxBytes')
        gv.LOG.nFiles          = config.getint('LOG', 'nFiles')

        savedPath = os.getcwd()
        os.chdir(gv.LOG.logDir)
        os.chdir(savedPath)

        gv.INI.RSYNC_PROGRAM     = config.get('MAIN', 'rsyncPRG')
        gv.INI.GREP_PROGRAM      = config.get('MAIN',  'grepPRG')
        newPATH                  = config.get('MAIN',  'ADDPATH')
        gv.INI.TEMPDIR           = config.get('MAIN',  'TempDir')

    except (ConfigParser.Error), why:
        Prj.exit(gv, 1, "ERROR reading %s file - %s" % (iniFileName, str(why) ) )

    except (StandardError, IOError), why:
        Prj.exit(gv, 2, str(why))

    print ".................sono qui", tempDir, gv.INI.TEMPDIR

    if not os.path.isfile(gv.INI.RSYNC_PROGRAM):
        gv.INI.RSYNC_PROGRAM = LN.file.getFullPath(gv, gv.INI.RSYNC_PROGRAM, 'PATH', exitOnError=True)

    if not os.path.isfile(gv.INI.GREP_PROGRAM):
        gv.INI.GREP_PROGRAM  = LN.file.getFullPath(gv, gv.INI.GREP_PROGRAM,  'PATH', exitOnError=True)

    if newPATH:
        # print "Adding:", newPATH
        currPath = os.getenv('PATH')
        os.environ['PATH'] = newPATH + ';' + currPath


        # Creazione nome del log file con l'utente come suffix per evitare conflitti
    (fname, fext) = os.path.splitext(gv.LOG.fileName)
    gv.LOG.fileName  = "%s_%s%s" % (fname, getpass.getuser(), fext)

    return gv.LOG

