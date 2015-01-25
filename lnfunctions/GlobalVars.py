#!/usr/bin/python3

import sys; sys.dont_write_bytecode = True

import platform
import os
import tempfile


class GlobalVars():
    fCONSOLE        = False
    fSYSLOG         = False
    fDEBUG          = False
    OpSys           = platform.system()
    scriptDir       = os.path.dirname(os.path.abspath(sys.argv[0]))
    scriptName      = os.path.basename(os.path.abspath(sys.argv[0])).split('.')[0]
    if scriptName == '__main__': scriptName = os.path.basename(scriptDir)
    sys.path.insert(0, scriptDir)
    tempDir         = tempfile.gettempdir()
    tempDir         = '/tmp'
    logFname        = os.path.abspath(os.path.join(tempDir, scriptName) + '.log')