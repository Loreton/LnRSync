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
    import optparse
    global gv
    gv = GlobalVars

    usageMsg = "\n\nUsage: %prog ACTION [-d Debug]"
    # parser = optparse.OptionParser(usageMsg, version="%prog 1.0")

    parser = optparse.OptionParser()

    parser.add_option( "-a", "--action",
                       type="string",
                       dest="ACTION",
                       default='step',
                       help="You may indicate the ACTION with the -a option. Default is: [step]")

    parser.add_option( "-s", "--section",
                       type="string",
                       dest="SECTION_NAME",
                       default=None,
                       help="You may indicate a the section name to be executed")

    group = optparse.OptionGroup(parser,
                        "\n --------------- Optional parameters----------------",
                        "Use these options to set debug or other values.")

    group.add_option( "-c", "--configFile",
                       type="string",
                       dest="CONFIG_FILE",
                       default='LnRSync.cfg',
                       help="You may indicate the configuration file to be used")



    group.add_option( "-d", "--debug",
                       action="store_true",
                       dest="DEBUG",
                       default=False,
                       help="You may indicate a debug status with the -d option. Default is: [False]")

    group.add_option( "-v", "--version",
                       action="store_true",
                       dest="currVERSION",
                       default=False,
                       help="You may indicate a version status with the -v option.")


    parser.add_option_group(group)

    (options, args) = parser.parse_args()


    validActions =  ["GO", "DRY-RUN", "STEP"]
    if options.ACTION:
        actionUPP = ' ' + options.ACTION.upper() + ' '
        actionUPP = options.ACTION.upper()
        if not actionUPP in validActions:
            usage()
    else:
        usage()

    if options.currVERSION:
        print "LnRSync Version 1.0 - 2013-10-05"
        sys.exit()

    gv.INP_PARAM.fDEBUG           = options.DEBUG
    gv.INP_PARAM.action           = options.ACTION
    gv.INP_PARAM.actionUPP        = options.ACTION.upper()
    gv.INP_PARAM.mainCfgFile      = options.CONFIG_FILE
    gv.INP_PARAM.SECTION_NAME     = options.SECTION_NAME

    if not os.path.isfile(gv.INP_PARAM.mainCfgFile):
        gv.INP_PARAM.mainCfgFile = os.path.join(gv.mainConfigDIR, gv.INP_PARAM.mainCfgFile)


    return options
