#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  ............
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys; sys.dont_write_bytecode = True
import os

import collections
import configparser
import codecs

# ######################################################
# # https://docs.python.org/3/library/configparser.html
# ######################################################
def readIniFile(fileName, RAW=False, exitOnError=False):
        # Setting del parser
    configMain = configparser.ConfigParser( allow_no_value=False,
                                        delimiters=('=', ':'),
                                        comment_prefixes=('#',';'),
                                        inline_comment_prefixes=(';',),
                                        strict=True,          # impone key unica
                                        # strict=False,
                                        empty_lines_in_values=True,
                                        default_section='DEFAULT',
                                        interpolation=configparser.ExtendedInterpolation()
                                    )
    configMain.optionxform = str        # mantiene il case nei nomi delle section e delle Keys (Assicurarsi che i riferimenti a vars interne siano case-sensitive)

    try:
        data = codecs.open(fileName, "r", "utf8")
        configMain.readfp(data)

    except (Exception) as why:
        print("Errore nella lettura del file: {} - {}".format(fileName, str(why)))
        sys.exit(-1)


        # Parsing del file
    if type(configMain) in [configparser.ConfigParser]:
        configDict = iniConfigAsDict(configMain, raw=RAW)
    else:
        configDict = configMain

    return configMain, configDict


############################################################
#
############################################################
def iniConfigAsDict(INIConfig, sectionName=None, raw=False):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """

    the_dict = collections.OrderedDict({})
    fDEBUG = False
    try:
        for section in INIConfig.sections():
            the_dict[section] = collections.OrderedDict({})
            if fDEBUG: print ()
            if fDEBUG: print ('[{}]'.format(section))
            for key, val in INIConfig.items(section, raw=raw):
                the_dict[section][key] = val
                if fDEBUG: print ('    {:<30} : {}'.format(key, val))

    except (configparser.InterpolationMissingOptionError) as why:
        print("\n"*2)
        print("="*60)
        print("ERRORE nella validazione del file")
        print("-"*60)
        print(str(why))
        print("="*60)
        sys.exit(-2)

    if sectionName:
        return the_dict[sectionName]
    else:
        return the_dict




############################################################
#
############################################################
def printINIconfigparser(INI_raw):
    for section in INI_raw.sections():
        print ()
        print ('[{}]'.format(section))
        for key, val in INI_raw.items(section):
            print ('    {:<30} : {}'.format(key, val))

