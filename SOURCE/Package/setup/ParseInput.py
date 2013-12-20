#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys
import  textwrap


def usage(exit=True):
    LN = gv.LN

    print LN.cCYAN + textwrap.dedent("""\
          Usage: %s ACTION JBossInstanceNAME [-d|--debug] [-f|--file=deployFile]

        --------------- ACTION - You may indicate: ----------------
        -v --version -  Display version level
        -c --config  -  configuration file containing the flows to be executed
        -s --section -  section name, in the configuration file, to be processed
        -d --debug   -  start debug trace
        -a --action  -  STEP      to just display rSync command to be executed
                        DRY-RUN   run rSync command in DRY-RUN mode
                        GO        run rSync command

        Example: -c HomeBackup.cfg -s Portit_DiscoL -a step

         """ % (gv.scriptName) )


    if exit: sys.exit()

# ######################################################################################
# # ParseInput()
# ######################################################################################
def parseInput(GlobalVars):
    global gv
    gv = GlobalVars

    usageMsg = "\n\nUsage: %prog ACTION [-d Debug]"
    # parser = optparse.OptionParser(usageMsg, version="%prog 1.0")

    import argparse
    parser = argparse.ArgumentParser(description='Process rsync operations.')

    parser.add_argument( "-a", "--action",
                       dest="ACTION",
                       default='step',
                       help="You may indicate the ACTION with the -a option. Default is: [step]")

    parser.add_argument( "-s", "--section",
                       dest="SECTION_NAME",
                       default=None,
                       help="You may indicate a the section name to be executed")

    group = parser.add_argument_group("\n --------------- Optional parameters----------------",
                                        "Use these options to set debug or other values.")

    group.add_argument( "-c", "--configFile",
                       dest="CONFIG_FILE",
                       default='LnRSync.cfg',
                       help="You may indicate the configuration file to be used")



    group.add_argument( "-d", "--debug",
                       action="store_true",
                       dest="DEBUG",
                       default=False,
                       help="You may indicate a debug status with the -d option. Default is: [False]")

    group.add_argument( "-v", "--version",
                       action="store_true",
                       dest="currVERSION",
                       default=False,
                       help="You may indicate a version status with the -v option.")


    args = parser.parse_args()



    validActions =  ["GO", "DRY-RUN", "STEP"]
    if args.ACTION:
        actionUPP = ' ' + args.ACTION.upper() + ' '
        actionUPP = args.ACTION.upper()
        if not actionUPP in validActions:
            usage()
    else:
        usage()

    if args.currVERSION:
        print "LnRSync Version 1.0 - 2013-10-05"
        sys.exit()

    gv.INP_PARAM.fDEBUG           = args.DEBUG
    gv.INP_PARAM.action           = args.ACTION
    gv.INP_PARAM.actionUPP        = args.ACTION.upper()
    gv.INP_PARAM.mainCfgFile      = args.CONFIG_FILE
    gv.INP_PARAM.SECTION_NAME     = args.SECTION_NAME

    if not os.path.isfile(gv.INP_PARAM.mainCfgFile):
        gv.INP_PARAM.mainCfgFile = os.path.join(gv.mainConfigDIR, gv.INP_PARAM.mainCfgFile)


    return args
