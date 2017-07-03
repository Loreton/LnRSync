#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

cPrint = None
def SetGlobals(color):
    global cPrint
    cPrint = color



####################################
# - executeOptions
####################################
def ExecuteOptions(myParser, required=False):
    mandatory = cPrint.getYellowH('MANDATORY - ') if required else 'OPTIONAL - '
    myParser.add_argument( "--go",
                            action="store_true",
                            dest="fEXECUTE",
                            default=required,
                            help=mandatory + cPrint.getYellow("""Execute commands.
    [DEFAULT: False, run in DRY-RUN mode]
    """))




####################################
# - encryptOptions
####################################
def DestServer(myParser, required):
    mandatory = cPrint.getMagentaH('MANDATORY - ') if required else 'OPTIONAL - '

    myParser.add_argument( "-fs", "--from-server",
                            type=str,
                            required=required,
                            dest="fromServer",
                            default=None,
                            help=mandatory + cPrint.getYellow("""FROM Server Name.
    [DEFAULT: None]
    """))

    myParser.add_argument( "-ts", "--to-server",
                            type=str,
                            required=required,
                            dest="toServer",
                            default=None,
                            help=mandatory + cPrint.getYellow("""TO Server Name.
    [DEFAULT: None]
    """))


    # myParser.add_argument( "-fp", "--port",
    #                         type=str,
    #                         required=required,
    #                         dest="loginUser",
    #                         default=None,
    #                         help=mandatory + cPrint.getYellow("""Server Name to connect.
    # [DEFAULT: None]
    # """))

    # myParser.add_argument( "-fu", "--from-user",
    #                         type=str,
    #                         required=required,
    #                         dest="loginUser",
    #                         default=None,
    #                         help=mandatory + cPrint.getYellow("""Server Name to connect.
    # [DEFAULT: None]
    # """))

