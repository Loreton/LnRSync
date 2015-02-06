#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
# ##############################################################
# #
# ##############################################################
def MountDevice(device):
        # for device in gv.DEVICE.items():
    devName, deviceDict = device      # devName=str, val=dict
    mountDIR    = deviceDict.get('MountPoint')
    fsTYPE      = deviceDict['TYPE']
    label       = deviceDict['LABEL']

    if mountDIR and os.path.ismount(mountDIR):
        ln.wrLog("device already mounted on: {}".format(mountDIR), exit=True)

    mountDIR = '/mnt/{}'.format(label)
    ln.wrLog('{:<15} {:<25} {:<15}'.format('deviceName', 'mountPoint', 'fileType'))
    ln.wrLog('{:<15} {:<25} {:<15}'.format(devName, mountDIR, fsTYPE))

        # ----------------------------------------------
        # - preparazione parametri per il mount
        # ----------------------------------------------
    mountOPT = 'defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
    if   (fsTYPE == None):      ln.wrLog('filetype: None', exit=True)
    elif (fsTYPE == 'ntfs'):    fsTYPE = 'ntfs-3g'
    elif (fsTYPE == 'vfat'):    fsTYPE = 'vfat'
    else:                       fsTYPE = 'auto'


        # ----------------------------------------------
        # - preparazione parametri per il mount
        # ----------------------------------------------
    mountCMD = []
    mountCMD.append('sudo')
    createMountpoint(mountDIR)

    mountCMD.append('/bin/mount')
    mountCMD.append('-t{}'.format(fsTYPE.strip()))
    mountCMD.append("-o {}".format(mountOPT.strip()))
    mountCMD.append(devName.strip())
    mountCMD.append(mountDIR)

        # esecuzione comando
    ln.wrLog(' '.join(mountCMD), exit=False)
    rCode = subprocess.call( mountCMD )         # subprocess.check_call( mountCMD ) # da errore
    ln.wrLog('mount rCode: {}'.format(rCode) )



