#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
# ##############################################################
# #
# ##############################################################
def uMountDevice(device):

    devName, deviceDict = device            # devName=str, val=dict
    mountDIR    = deviceDict['MountPoint']

        # ----------------------------------------------
        # - preparazione parametri per il mount
        # ----------------------------------------------
    if os.path.isdir(mountDIR):
        if os.path.ismount(mountDIR):
            uMountCMD = []
            uMountCMD.append('sudo')
            uMountCMD.append('/bin/umount')
            uMountCMD.append("-l")
            uMountCMD.append(mountDIR)

                # Flush cache
            rCode = subprocess.call( ['sudo', 'hdparm', '-f', devName ] ) #  mandalo in sleep
            ln.wrLog('hdparm flush rCode: {}'.format(rCode) )

                # sleep device
            rCode = subprocess.call( ['sudo', 'hdparm', '-y', devName ] ) #  mandalo in sleep
            ln.wrLog('hdparm sleep rCode: {}'.format(rCode) )

                # umount device
            ln.wrLog(' '.join(uMountCMD))
            rCode = subprocess.call( uMountCMD )
            ln.wrLog('umount rCode: {}'.format(rCode) )

        else:
            ln.wrLog(mountDIR + ' is NOT mounted', exit=True)

    else:
        ln.wrLog(mountDIR + " doesn't exists", exit=True)

    removeMountPoint(mountDIR)

