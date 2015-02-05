#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
# ###########################################################################
# # esegue il comando df -h
# # Esempio di riga:
# #     Filesystem      Size  Used Avail Use% Mounted on
# #     rootfs          7.2G  2.7G  4.3G  39% /
# #     /dev/root       7.2G  2.7G  4.3G  39% /
# #     devtmpfs        215M     0  215M   0% /dev
# #     /dev/mmcblk0p1   56M  9.7M   47M  18% /boot
# #     /dev/sde5       233G  216G   18G  93% /mnt/Lacie_232GB_A
# ###########################################################################
def getDF(mpRoot='/', fDEBUG=False):
    global gv
    retList = []
        # get  df -h
    res = subprocess.check_output(['df',  '-h'], stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    res = res.decode('utf-8')       # converti in STRing


    for line in res.split('\n'):
        field = line.split()
        if len(field) < 6: continue
        devName = field[0]
        mountPoint = field[5]
        if mountPoint.startswith(mpRoot):
            linea = '   {:<30} - {}'.format(devName, mountPoint)
            retList.append(linea)
            if fDEBUG: print(linea)
                # aggiungiamo al dictionary dei device
            if not devName in gv.DEVICE: gv.DEVICE[devName] = {}
            gv.DEVICE[devName]['MountPoint'] = mountPoint

    return retList
