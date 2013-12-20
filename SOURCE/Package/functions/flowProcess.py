#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, os


def flowProcess(gv, flowID, flowVARs):
    LN = gv.LN
    Prj = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    if flowVARs == None: return

        # -------------------------------------------
        # - Lettura delle subDir da processare
        # -------------------------------------------
    PathID = flowID.get('PATHS', [])    #     pprint( PathID)
    #print gv.FLOW.SOURCE_SYSTEM, gv.FLOW.TARGET_SYSTEM

    for srcDir, tgtDir, includePATTERN, fBACKUP, backupSUFFIX in PathID:

            # ADD relative PATH to BASE_DIR
            # La dir di Backup sara': TargetROOTDir + '__BACKUP' + targetPATHID
        sourceDIR = gv.FLOW.SOURCE_ROOT_DIR  + srcDir

        if sourceDIR[-1] == '/':
            targetDIR = (gv.FLOW.TARGET_ROOT_DIR  + tgtDir).replace("=", srcDir)
            BackupDIR = gv.FLOW.TARGET_ROOT_DIR  + '/__BACKUP' + tgtDir.replace("=", srcDir)
        else:
            pos = sourceDIR.rfind('/')
            appo = sourceDIR[:pos]
            targetDIR = (gv.FLOW.TARGET_ROOT_DIR  + tgtDir).replace("=", appo)
            BackupDIR = gv.FLOW.TARGET_ROOT_DIR  + '/__BACKUP' + tgtDir.replace("=", appo)

        gv.FLOW.SOURCE_DIR  = sourceDIR
        gv.FLOW.TARGET_DIR  = targetDIR

        if fBACKUP:
            backupOptions = "--backup --backup-dir=%s --suffix=_%s" % (BackupDIR, backupSUFFIX)
        else:
            backupOptions = ""


        if gv.FLOW.SOURCE_HOST != 'LOCAL' and gv.FLOW.TARGET_HOST != 'LOCAL':
            Prj.exit(gv, 2010, "Source e Destination HOSTS remoti non contemplato.")

        if gv.FLOW.SOURCE_HOST == 'LOCAL':
            sourceFullPath = gv.FLOW.SOURCE_DIR
            LN.file.makeDirs(gv, sourceFullPath, exitOnError=True)
        else:
            sourceFullPath = gv.FLOW.SOURCE_HOST + ':' + gv.FLOW.SOURCE_DIR

        if gv.FLOW.TARGET_HOST == 'LOCAL':
            targetFullPath = gv.FLOW.TARGET_DIR
            LN.file.makeDirs(gv, targetFullPath)
        else:
            targetFullPath = gv.FLOW.TARGET_HOST + ':' + gv.FLOW.TARGET_DIR


        fDEBUG = True
        fDEBUG = False
        if fDEBUG:
            print "\n"*2;pprint(globalARGs);print "\n"*2
            print "\n"*2;pprint(flowVARs);print "\n"*2



        # #########################################################################################################
        # # Preparazione RSYNC command
        # #########################################################################################################

        rSyncOPTIONS = ''
        INCLUDE = False
        rSyncOPTIONS += ' ' + gv.FLOW.RSYNC_BASE_OPTIONS
        rSyncOPTIONS += ' ' + gv.FLOW.RSYNC_OTHER_OPTIONS
        rSyncOPTIONS += ' ' + backupOptions
        rSyncOPTIONS += ' ' + gv.FLOW.RSYNC_LOG_FILE

        for pattern in includePATTERN:
            if pattern != '' and pattern != '*':
                rSyncOPTIONS += " --include='%s'" % (pattern)
                INCLUDE = True                      # SET Flag


        if INCLUDE:
            # rSyncOPTIONS += " --include='*/'"       # include le Subdirs
            rSyncOPTIONS += " --exclude='*'"        # Esclude tutto il resto
        else:
            rSyncOPTIONS += " " + gv.FLOW.RSYNC_EXCLUDED_PATTERN


        isDRY_RUN = "--dry-run" if gv.INP_PARAM.action.upper() == 'DRY-RUN' else  ""

        rSyncCmd = "%s %s %s %s %s" % (gv.FLOW.RSYNC_PROGRAM, isDRY_RUN, rSyncOPTIONS, sourceFullPath, targetFullPath)
        displayRSyncCommand(gv, rSyncCmd, fDEBUG=False)

        if gv.INP_PARAM.action.upper() == 'STEP':
            choice = LN.sys.getKeyboardInput(gv, "..... [P=Process D=dry-run ENTER=Skip]           ", validKeys='ENTER|p|d', exitKey='X')
            if   choice.upper() == 'P':
                isDRY_RUN = ""
            elif choice.upper() == 'D':
                isDRY_RUN = '--dry-run'
            else:
                continue

                # ricostruiamo il comando di rSync con il dry-run impostato
            rSyncCmd = "%s %s %s %s %s" % (gv.FLOW.RSYNC_PROGRAM, isDRY_RUN, rSyncOPTIONS, sourceFullPath, targetFullPath)
            displayRSyncCommand(gv, rSyncCmd)


        if gv.CONFIG.COMMAND_TYPE == 'SYSTEM':
            logger.info('[SYSTEM] executing command: %s' % (rSyncCmd))
            rCode = os.system(rSyncCmd)
            if rCode != 0:
                print
                print "*"*50
                print "Command:%s" % (rSyncCmd)
                print '......... retCode ', rCode
                print "*"*50
                print

        else:
            logger.info('[TRAPPED] executing command: %s' % (rSyncCmd))
            # (iCode, sOUT) = LnSys.getstatusoutput(rSyncCmd)
            retVal = LN.proc.runCommand_New(gv, rSyncCmd, wkdir='.', argsList=[], PWAIT=0, stdOUTfile=False, exit=False)

            if retVal.rcode != 0:
                print "\nCommand:%s" % (rSyncCmd)
                print '......... retCode ', retVal.err
                print '......... textCode', retVal.output

            print
            # for line in sOUT.split('\n'):
            #     if len(line.strip()) > 0:
            #         if gv.CONFIG.ACTION.upper() == 'GO':
            #             print "    ...copying...", line
            #         else:
            #             print "    ...(DRY RUN)...", line

        print


def displayRSyncCommand(gv, rSyncCmd, fDEBUG=False):
    print "\n"*3
    print "\n"*3,"#"*90
    print "[%s]:%s ---> [%s]:%s" % (gv.FLOW.SOURCE_HOST, gv.FLOW.SOURCE_DIR, gv.FLOW.TARGET_HOST, gv.FLOW.TARGET_DIR)
    print
    print rSyncCmd
    print "#"*90,"\n"*3

    if fDEBUG:
        print "\n"*2,"-"*60
        optList = gv.LN.string.stringToList(gv, rSyncCmd, sepChars=' ')
        print optList[0]
        for optVal in optList[1:]:
            if not optVal.startswith('-'):
                print '  ',
            print '      ', optVal
        print "-"*60,"\n"*3



