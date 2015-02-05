#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:

# ###########################################################################
# # esegue il comando blkid
# # Esempio di riga:
# #   /dev/sdb5: LABEL="Lacie232GB_A" UUID="1448564A48562AAE" TYPE="ntfs"
# ###########################################################################
def getBlockID(reqUUID=None):
    global gv

    res = subprocess.check_output('blkid', stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    res = res.decode('utf-8')       # converti in STRing

    for line in res.split('\n'):
        if not line: continue   # se vuota loop
        devName, rest = line.split(':')                         # prendi nome device ...
        if not devName in gv.DEVICE: gv.DEVICE[devName] = {}    # creiamo l'entry, se non esiste
        vals = rest.split()                                     # la parte restante la spezziamo
        for val in vals:
            name, value = val.split('=')
            gv.DEVICE[devName][name] = value.strip('"')


