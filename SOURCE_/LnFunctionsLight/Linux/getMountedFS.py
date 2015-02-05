#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
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

