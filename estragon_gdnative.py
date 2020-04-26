#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.

# useful modules
from estragon_log       import log
from estragon_build     import build
from sys                import platform
from os                 import path

# A nice tool to build godot editor with the appropriate parameters.
class build_gdnative_cpp(build)   :

    # folder where built binaries 
    _buildtargetpath = "./bin"

    # for gdnative it's x11
    def plateform(self) :
        return "x11" if platform.startswith('linux') else ("windows" if platform.startswith('win')  else None)

    # in godot-cpp and gdnative it's use_llvm instead of llvm
    def ccArguments(self)  :
        return "".join(["use_llvm=",("yes" if self._llvm else "no")])

    # build editor with this current builder
    def build_gdnative_libs(self, extraArgs : str = str())    :
        try :
            self.makeDir(path.normpath(path.join(self.getSconsPath(), self._buildtargetpath)))
            target_path = "".join(["target_path=", self._buildtargetpath])
            self.build(" ".join([extraArgs,target_path]))
        except AssertionError :
            log("failed to build editor")
            raise
        
# allow to run from a shell-run python:
# python3 estragon_gdnative.py path to godot project root
if __name__ == "__main__":
    print("estragon estragon_gdnative command called from shell")
    from sys import argv
    try:
        builder = build_gdnative_cpp(argv[1], True)
        builder.build_gdnative_libs(" ".join(argv[2:]))
    except Exception:
        print ("an error occured, printing log : ")
        print(log.get_log())
        print("end of log \n")
        raise
    
