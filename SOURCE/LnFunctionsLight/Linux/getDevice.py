#!/usr/bin/python3
# vim:enc=utf-8:nu:ai:si:et:ts=4:sw=4:ft=udevrules:
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

