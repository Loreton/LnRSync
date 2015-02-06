#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
# ##############################################################
# #
# ##############################################################
def createMountpoint(MPdir):
    if os.path.isdir(MPdir):
        ln.wrLog(MPdir + ' already exists')
        if os.path.ismount(MPdir):
            ln.wrLog(MPdir + ' already mounted', exit=True)

    rCode = subprocess.call( ['sudo', 'mkdir', MPdir ] ) #  per usare il sudo
    ln.wrLog('mkdir rCode: {}'.format(rCode) )






# ##############################################################
# #
# ##############################################################
def removeMountPoint(MPdir):
    if os.path.isdir(MPdir):
        if os.path.ismount(MPdir):
            ln.wrLog(MPdir + ' is mounted', exit=True)

    rCode = subprocess.call( ['sudo', 'rmdir', MPdir ] ) # solo per usare il sudo
    ln.wrLog('rmdir rCode: {}'.format(rCode) )

