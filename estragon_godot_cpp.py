#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.

# useful modules
from estragon_log       import log
from estragon_build     import build

# A nice tool to build godot editor with the appropriate parameters.
class build_godot_cpp()   :
    

    # build editor with this current builder
    def build_godot_cpp_bindings(self, extraArgs : str = str())    :
        try :
            self.build(extraArgs.join(" generate_bindings=yes"))
        except AssertionError :
            log("failed to build editor")
            raise
        
# allow to run from a shell-run python:
# python3 estragon_build_godot.py path_to_godot
if __name__ == "__main__":
    print("estragon godot_cpp command called from shell")
    from sys import argv
    try:
        builder = build_godot_cpp(argv[1], True)
        builder.build_godot_cpp_bindings(argv[2:])
    except Exception:
        print ("an error occured, printing log : ")
        print(log.get_log())
        print("end of log \n")
        raise
    
