#!/usr/bin/python3

# dictTYPES = [dict, configparser.ConfigParser, configparser.SectionProxy, gv.Prj.LnClass, gv.LN.LnClass, collections.OrderedDict]
def printLnClass(dictID, level=1):
    classesTYPES = [ln.LnClass, type, GlobalVars]
    print (type(dictID))
    # dictID = vars(dictID)
    if dictID in classesTYPES:
    # if isinstance(dictID, LnClass):
        dictID = vars(dictID)

    print()
    print('     ---- level ---', level)
    print()
    for key, val in dictID.items():
        if key.startswith('__') and key.endswith('__'): continue    # elimina tutti i built-in (presente in un modulo)
        if isinstance(val, LnClass):
            printLnClass(val, level=level+1)

        print('[{}] {}{:<20} : {}'.format(level, ' '*level*4, key, val))

