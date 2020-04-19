#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.


# useful modules
from estragon_log       import log
from shutil             import which
from sys                import platform
from multiprocessing    import cpu_count
from os                 import chdir
from datetime           import datetime
import time

from subprocess import DEVNULL
from subprocess import check_call as call
from shlex import split as clisplit


# A nice tool to build godot editor with the appropriate parameters.
class build_godot()   :
    
   
    # Number of CPU core available
    _CPUAvailable   = cpu_count()

    # Path to Godot sources
    _SourcesPath     = None

    # Whether llvm is available
    _llvm   = which("clang") is not None

    # whether scons is available
    _scons  = which("scons") is not None

    _plateform = "x11" if platform.startswith('linux') else ("windows" if platform.startswith('win')  else None)

    def buildGodot(self, path, extraArgs) :
        assert self._llvm
        assert self._scons
        assert self._plateform is not None
        #avoid null argument
        if extraArgs is None    :
            extraArgs = ''

        #look for the correct path

        chdir(self._SourcesPath)
        log("Building godot on path = " + self._SourcesPath)

        # building the command line
        cli = "scons " + "-j"+ str(self._CPUAvailable) + " platform=" + self.platform + " " + extraArgs + " -Q"
        log( "Build command  = " + cli)

        # time stamping
        startTime = time.time()
        log("Scons started at " + str(datetime.fromtimestamp(startTime)))
 
        # for windows be sure to launch command in powershell, not CMD
        if platform.startswith('win')   :
           cli = "powershell" + cli

        # launching scons
        # asking the system to run the command
        if log.isDebug() :
            call(clisplit(cli),stdin=DEVNULL)
        else            :
            call(clisplit(cli),stdin=DEVNULL, stdout=DEVNULL)
            
        # timestamping again
        endTime = time.time()
        log("Scons finished at " + str(datetime.fromtimestamp(endTime)))
        duration = endTime - startTime
        log("Build Took :" + f"{duration:.3f}" + "s")

    # init the builder
    # find how many threads are availables
    def __init__(self, path : str )  :
        super().__init__()
        self._SourcesPath = path


    # build editor with this current builder
    def BuildEditor(self, extraArgs : str)    :
        if self._SourcesPath is not None     :
            self.buildGodot(self._SourcesPath, extraArgs)
        return


