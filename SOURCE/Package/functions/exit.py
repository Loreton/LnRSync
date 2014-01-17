#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types

def exit(gv, rcode, text):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

    if isinstance(text, types.ListType):
        textList = text
        pass
    else:
        textList = text.split('\n')

    if rcode == 0:
        print(LN.cGREEN + "[RCODE: %d] Text:" % (rcode))
    else:
        print("%s[RCODE: %d] Text:" % (LN.cGREEN, rcode))

    for line in textList:
        print(LN.cWARNING + ' '*10 + "%s" % (line))

    print

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    sys.exit(rcode)