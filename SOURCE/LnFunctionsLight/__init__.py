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
    from . Linix.getBlockID         import getBlockID
    from . Linix.getDevice          import getDevice
    from . Linix.getDF              import getDF
    from . Linix.getMountedFS       import getMountedFS
    from . Linix.MountDevice        import MountDevice
    from . Linix.Mountpoint         import Mountpoint
    from . Linix.uMountDevice       import uMountDevice




