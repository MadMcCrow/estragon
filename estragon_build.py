#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.

# useful modules
from estragon_log       import log
from shutil             import which
from sys                import platform
from multiprocessing    import cpu_count
from os                 import path
from os                 import chdir
from datetime           import datetime
import time
from subprocess import DEVNULL
from subprocess import check_call as call
from shlex import split as clisplit


#
# Base class for building godot, godot tools, and godot projects
#
class build()   :
    

    # Do we display scons output
    _showSconsOutput = True
    
    # Number of CPU core available
    _CPUAvailable   = cpu_count()

    # Path to Godot sources
    _SourcesPath     = None

    # Whether llvm is available
    _llvm   = which("clang") is not None

    # whether scons is available
    _scons  = which("scons") is not None

    _plateform = "x11" if platform.startswith('linux') else ("windows" if platform.startswith('win')  else None)

    def build(self, extraArgs : str = str()) :
        log("checking requisites :" ,self._SourcesPath, self._llvm, self._scons, self._plateform)
        assert path.exists(self._SourcesPath)
        assert self._scons
        assert self._plateform is not None
        #avoid null argument

        #look for the correct path
        chdir(self._SourcesPath)
        log("Building godot on path = ", self._SourcesPath)

        # building the command line
        llvm        = "".join(["llvm=",("yes" if self._llvm else "no")])
        threads     = "".join(["-j",str(self._CPUAvailable)])
        plateform   = "".join(["platform=" + self._plateform])
        
        try :
            extraArgs = " ".join(extraArgs)
        except TypeError :
            extraArgs = ""

        cli = " ".join(["scons", threads, plateform, llvm, extraArgs,"-Q"])
        log( "Build command  = ", cli)

        # time stamping
        startTime = time.time()
        log("Scons started at ", datetime.fromtimestamp(startTime))
 
        # for windows be sure to launch command in powershell, not CMD
        if platform.startswith('win')   :
           cli = " ".join(["powershell" ,cli])

        # launching scons
        # asking the system to run the command
        if self._showSconsOutput :
            call(clisplit(cli),stdin=DEVNULL)
        else            :
            call(clisplit(cli),stdin=DEVNULL, stdout=DEVNULL)
            
        # timestamping again
        endTime = time.time()
        log("Scons finished at ",datetime.fromtimestamp(endTime))
        duration = endTime - startTime
        log("Build Took :" + f"{duration:.3f}" + "s")

    # init the builder
    # find how many threads are availables
    def __init__(self, path : str  = None, out : bool = False )  :
        super().__init__()
        self._SourcesPath = path

        

