#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
import sys;     sys.dont_write_bytecode = True
import os
import subprocess
import syslog

# #################################################################
# -  Comandi di utilità
# -     sudo blkid
# -         /dev/sdc1: LABEL="Lacie232GB_B" UUID="B222175022171945" TYPE="ntfs"
# -         ....
# -     sudo blkid -o udev -p /dev/sdc1
# -         ID_FS_LABEL=Lacie232GB_B
# -         ....
# -     udevadm info -a -n /dev/sdc1
# -         KERNEL=="sdc1"
# -         ....
# -     lsusb
# -         Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp.
# -         ....
# -     lsusb -v -s 001:007
# -         Bus 001 Device 007: ID 059f:101a LaCie, Ltd
# -         ....
# -     udevadm info -a -n /dev/sdc1 | grep -i product
# -         ATTRS{idProduct}=="101a"
# -         ....
# #################################################################

LOG=None
class LnClass(): pass


# ##############################################################
# #
# ##############################################################
def wrLog(data, fName=None, exit=False):
    global LOG
    lineNO = sys._getframe( 1 ).f_lineno

    if exit: data = data + ' [exiting]'

    if (fName):
        try:
            LOG = open(fName, "wb")
            print("Using log file:" + fName)

        except (IOError, os.error) as why:
            exit("ERROR writing file - {}".format(str(why)))

    if (LOG):
        dataLog = '[{}] {}'.format(lineNO, data)
        LOG.write(bytes(dataLog + '\n', 'UTF-8'))


    if gv.fCONSOLE:
        print('    ', data)

    if gv.fSysLOG:
        syslog.syslog(syslog.LOG_INFO, "Loreto - [{:<15}] - {}".format(gv.UUID, data))

    if exit and LOG:
        LOG.close()
        sys.exit()




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

# ###########################################################################
# # esegue il comando mount
# # Esempio di riga:
# #     /dev/root   on / type ext4 (rw,noatime,data=ordered)
# #     devtmpfs    on /dev type devtmpfs (rw,relatime,size=219744k,nr_inodes=54936,mode=755)
# #     tmpfs       on /run type tmpfs (rw,nosuid,noexec,relatime,size=44784k,mode=755)
# #     tmpfs       on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
# #     proc        on /proc type proc (rw,nosuid,nodev,noexec,relatime)
# #     sysfs       on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
# #     tmpfs       on /run/shm type tmpfs (rw,nosuid,nodev,noexec,relatime,size=89560k)
# #     devpts      on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
# #     /dev/mmcblk0p1 on /boot type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro)
# #     fusectl     on /sys/fs/fuse/connections type fusectl (rw,relatime)
# #     /dev/sde5   on /mnt/Lacie_232GB_A type fuseblk (rw,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other,blksize=4096)
# #   facciamo lo split su blank e prendiamo il primo e terzo valore
# ###########################################################################
def getMountedFS(mpRoot='/', fDEBUG=False):
    global gv
    res = subprocess.check_output(['mount'], stderr=subprocess.STDOUT)  # ritorna <class 'bytes'>
    res = res.decode('utf-8')       # converti in STRing


    for line in res.split('\n'):
        if not line: continue   # se vuota loop
        field = line.split()
        # print (len(field), line)
        devName     = field[0]
        mountPoint  = field[2]
        if mountPoint.startswith(mpRoot):
                # aggiungiamo al dictionary dei device
            if not devName in gv.DEVICE: gv.DEVICE[devName] = {}
            gv.DEVICE[devName]['MountPoint'] = field[2]



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



# ##############################################################
# #
# ##############################################################
def createMountpoint(MPdir):
    if os.path.isdir(MPdir):
        wrLog(MPdir + ' already exists')
        if os.path.ismount(MPdir):
            wrLog(MPdir + ' already mounted', exit=True)

    rCode = subprocess.call( ['sudo', 'mkdir', MPdir ] ) #  per usare il sudo
    wrLog('mkdir rCode: {}'.format(rCode) )






# ##############################################################
# #
# ##############################################################
def removeMountPoint(MPdir):
    if os.path.isdir(MPdir):
        if os.path.ismount(MPdir):
            wrLog(MPdir + ' is mounted', exit=True)

    rCode = subprocess.call( ['sudo', 'rmdir', MPdir ] ) # solo per usare il sudo
    wrLog('rmdir rCode: {}'.format(rCode) )




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
        wrLog("device already mounted on: {}".format(mountDIR), exit=True)

    mountDIR = '/mnt/{}'.format(label)
    wrLog('{:<15} {:<25} {:<15}'.format('deviceName', 'mountPoint', 'fileType'))
    wrLog('{:<15} {:<25} {:<15}'.format(devName, mountDIR, fsTYPE))

        # ----------------------------------------------
        # - preparazione parametri per il mount
        # ----------------------------------------------
    mountOPT = 'defaults,noauto,relatime,nousers,rw,flush,utf8=1,uid=pi,gid=pi,dmask=002,fmask=113'
    if   (fsTYPE == None):      wrLog('filetype: None', exit=True)
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
    wrLog(' '.join(mountCMD), exit=False)
    rCode = subprocess.call( mountCMD )         # subprocess.check_call( mountCMD ) # da errore
    wrLog('mount rCode: {}'.format(rCode) )




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
            wrLog('hdparm flush rCode: {}'.format(rCode) )

                # sleep device
            rCode = subprocess.call( ['sudo', 'hdparm', '-y', devName ] ) #  mandalo in sleep
            wrLog('hdparm sleep rCode: {}'.format(rCode) )

                # umount device
            wrLog(' '.join(uMountCMD))
            rCode = subprocess.call( uMountCMD )
            wrLog('umount rCode: {}'.format(rCode) )

        else:
            wrLog(mountDIR + ' is NOT mounted', exit=True)

    else:
        wrLog(mountDIR + " doesn't exists", exit=True)

    removeMountPoint(mountDIR)


# ##############################################################
# #
# ##############################################################
def getDevice(reqMountPoint=None, reqUUID=None):
    print (reqMountPoint, reqUUID)
    for device in gv.DEVICE.items():
        devName, valDict = device       # devName=str, val=dict
        for key, val in valDict.items():
            if key == 'MountPoint' and val == reqMountPoint:
                return device

            if key == 'UUID' and val == reqUUID:
                return device

    return None



# ##############################################################
# #    M  A  I  N
# ==============================================================
# Testing new rules
#       sudo udevadm test $(udevadm info -q path -n /dev/sda1) 2>&1
#
# Loading new rules
#       Udev automatically detects changes to rules files,
#       so changes take effect immediately without requiring udev to be restarted.
#       However, the rules are not re-triggered automatically on already existing devices.
#       Hot-pluggable devices, such as USB devices, will probably have to be reconnected
#       for the new rules to take effect, or at least unloading and reloading the ohci-hcd
#       and ehci-hcd kernel modules and thereby reloading all USB drivers.
#
# If rules fail to reload automatically
#       udevadm control --reload-rules
#
# To manually force udev to trigger your rules (ma sembrano non funzionare)
#       sudo udevadm trigger
#       sudo udevadm trigger --attr-match=subsystem=block
# ##############################################################
if __name__ == "__main__":
    global gv
    gv = LnClass()
    gv.fCONSOLE = True                           # scrive anche a Console
    gv.fSysLOG  = False                          # scrive anche nel logger
    gv.DEVICE   = {}       # contiene la lista dei device ricavati dai comandi: mount (oppure df) e da blkid


        # - Apertura LOG
    scriptName  = os.path.basename(sys.argv[0]).split('.')[0]
    logFname    = "/tmp/{}.log".format(scriptName)
    wrLog("Apertura - log:{}".format(logFname), fName=logFname)


    gv.FS = getMountedFS('/mnt/')
    gv.BLKID = getBlockID()

    if False:
        for device in gv.DEVICE.items():
            print (device)


        # cerchiamo il parametro mount oppure umount e lo togliamo dalla lista
    # for inx, item in enumerate(sys.argv):
    #     if item.lower() in ['add', '-a', '--add', 'mount']:
    #         gv.ACTION = 'add'
    #         del sys.argv[inx]
    #     elif item.lower() in ['remove', '-r', '--remove', 'umount']:
    #         gv.ACTION = 'remove'
    #         del sys.argv[inx]


    gv.ACTION = None
    inpParam = None
    if len(sys.argv) > 1:
        if sys.argv[1][0] == '/':
            inpParam = sys.argv[1]
            gv.ACTION = 'umount'
        else:
            inpParam = sys.argv[1]
            gv.ACTION = 'mount'


    device = None
        # - Processo della richiesta
    if gv.ACTION == 'mount':
        device = getDevice(reqUUID=inpParam)
        if device: MountDevice(device)

    elif gv.ACTION == 'umount':
        device = getDevice(reqMountPoint=inpParam)
        if device: uMountDevice(device)


        # - Se comando non valido oppure device non trovato
    if not device:
        for device in gv.DEVICE.items():
            devName, valDict = device       # devName=str, val=dict
            print ('\n' + devName)
            for key, val in valDict.items():
                print ("    {:<30} = {}".format(key, val))

        print('''
        Immettere il valore:
            UUID        per  mount
            mountPoint  per umount

            il valore [{}] immesso non è valido.
            '''.format(inpParam))

    wrLog("Completed", exit=True)



