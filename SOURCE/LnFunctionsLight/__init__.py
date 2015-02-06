class LnClass():
    pass
import sys
import platform

MY_CONSTANT = 42
OpSys       = platform.system()



from . Common.wrLog                import wrLog
from . Common.GlobalVars           import GlobalVars as gv
from . Common.IniFile              import readIniFile
from . Common.IniFile              import printINIconfigparser
from . Common.printDict            import printLnClass

if OpSys == 'Windows':
    pass

elif OpSys == 'Linux':
    from . Linux.getBlockID         import getBlockID
    from . Linux.getDevice          import getDevice
    from . Linux.getDF              import getDF
    from . Linux.getMountedFS       import getMountedFS
    from . Linux.MountDevice        import MountDevice
    from . Linux.Mountpoint         import createMountpoint
    from . Linux.Mountpoint         import removeMountPoint
    from . Linux.uMountDevice       import uMountDevice




