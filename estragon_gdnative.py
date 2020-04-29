#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.

# useful modules
from estragon_log       import log
from estragon_build     import build
from estragon_file      import configFile
from estragon_file      import fileTools
from sys                import platform
from os                 import path



## gdlib_file
## file to make libraries available inside godot 
class gdlib_file(configFile):

    ## _libname
    ## name of module we're making a description of
    _libname = str()

    ## _libname
    ## name of module we're making a description of
    _buildpath = str()


    # File looks like this
    '''
    [general]
    singleton=false
    load_once=true
    symbol_prefix="godot_"
    reloadable=false

    [entry]
    Linux.64="res://bin/x11/libgdexample.so"
    Windows.64="res://bin/win64/libgdexample.dll"
    OSX.64="res://bin/osx/libgdexample.dylib"

    [dependencies]
    Linux.64=[]
    Windows.64=[]
    OSX.64=[]
    '''

    # static dictionnary of plateforms and path
    s_plateforms = {
        "Linux.64"      : "x11",
        "Windows.64"    : "win64",
        "OSX.64"        : "osx"
        }

    s_plateforms_lib_ext = {
        "Linux.64"      : ".so",
        "Windows.64"    : ".dll",
        "OSX.64"        : ".dylib"
        }

    # static string for empty plateform
    s_emptyentry = "[]"


    _IsSingleton    = False
    _LoadOnce       = True
    _symbol_prefix  = '"godot_"'
    _reloadable     = False


    def general(self) -> dict  :
        return  dict(
            {
                "singleton"     : self._IsSingleton,
                "load_once"     : self._LoadOnce, 
                "symbol_prefix" : self._symbol_prefix, 
                "reloadable"    : self._reloadable
            })


    ## entries : list
    ## we find the correct folder base on a dict for now
    ## TODO : implement auto detection
    def entry(self) -> dict  :
        retdict = dict()
        for platf, folder in gdlib_file.s_plateforms.items() :
            retdict[platf] = "\"res://" + path.realpath(path.join(self._buildpath, folder, self._libname + gdlib_file.s_plateforms_lib_ext[platf]))+ "\""
        return retdict

    ## dependencies : list
    ## dependencies are not auto detected
    def dependencies(self) -> dict  :
        retdict = dict()
        for platf in gdlib_file.s_plateforms.keys() :
            retdict[platf] = gdlib_file.s_emptyentry
        return retdict


    def __init__(self, build_path : str, lib_name : str):
        try :
            self._libname   = lib_name
            self._buildpath = build_path
            filename = ".".join([lib_name, "gdnlib"])
            filepath = path.join(self._buildpath, filename)
            super().__init__(filepath, '[]')
            assert len(lib_name) > 0 
            assert not fileTools.checkFileExist(filepath)
            self.addSection("general",self.general())
            self.addSection("entry",self.entry())
            self.addSection("dependencies",self.dependencies())
            self.writeConfig()
        except AssertionError   :
            log("Warning : could not create gdnlib file")

        
        
## gdns
## file to make add library as a ressource in godot
class gdns_file(configFile):

    ## _libname
    ## name of module we're making a description of
    _libname = str()

    ## _libname
    ## name of module we're making a description of
    _buildpath = str()


    # File looks like this
    '''
    [gd_resource type="NativeScript" load_steps=2 format=2]

    [ext_resource path="res://bin/gdexample.gdnlib" type="GDNativeLibrary" id=1]

    [resource]

    resource_name = "gdexample"
    class_name = "GDExample"
    library = ExtResource( 1 )
    '''

    def gd_ressource(self) -> str :
        return "gd_resource type=\"NativeScript\" load_steps=2 format=2"

    def ext_resource(self) -> str :
        respath = "\"res://" + path.realpath(path.join(self._buildpath, self._libname + ".gdnlib"))+ "\""
        return "ext_resource path=" + respath +  " type=\"GDNativeLibrary\" id=1"

    def resource(self) -> dict :
        return {
            "resource_name" :  "\"" + self._libname + "\"",
            "class_name"    :  "\"" + self._libname + "\"",
            "library"       :  "ExtResource( 1 )"
        }

    def __init__(self, build_path : str, lib_name : str):
        try :
            self._libname   = lib_name
            self._buildpath = build_path
            filename = ".".join([lib_name, "gdns"])
            filepath = path.join(self._buildpath, filename)
            super().__init__(filepath, '[]')
            assert len(lib_name) > 0 
            assert not fileTools.checkFileExist(filepath)
            self.addSection(self.gd_ressource(),dict())
            self.addSection(self.ext_resource(), dict())
            self.addSection("resource",self.resource())
            self.writeConfig()
        except AssertionError   :
            log("Warning : could not create gdns_file file")



## build_gdnative_cpp :
## A nice tool to build godot editor with the appropriate parameters.
class build_gdnative_cpp(build)   :

    # folder where built binaries 
    _buildtargetpath = "./bin"

    # for gdnative it's x11
    def plateform(self) :
        return "x11" if platform.startswith('linux') else ("windows" if platform.startswith('win')  else None)

    # in godot-cpp and gdnative it's use_llvm instead of llvm
    def ccArguments(self)  :
        return "".join(["use_llvm=",("yes" if self._llvm else "no")])

    ## build_gdnative_libs : 
    ## build libraries with this current builder
    ## TODO : autodetect modules to build them separately
    def build_gdnative_libs(self, extraArgs : str = str())    :
        fileTools.makeDir(path.normpath(path.join(self.getSconsPath(), self._buildtargetpath)))
        target_path = "".join(["target_path=", self._buildtargetpath])
        self.build(" ".join([extraArgs,target_path]))

    ## connect_to_godot :
    ## create the gdnlib file to make this library available in godot
    def connect_to_godot(self) :
        basepath = path.normpath(path.join(self.getSconsPath(), self._buildtargetpath))
        scanpath = path.normpath(path.join(basepath, self.plateform()))
        
        try :
            for f in fileTools.getSubFiles(scanpath) :
                log("making gdnlib files : ", f)
                if fileTools.getFileExt(f) in {'.so' , '.dll', '.dylib'} :
                    libname = fileTools.getFileBase(f)
                    filename = ".".join([libname, "gdnlib"])
                    filepath = path.join(self.getSconsPath(), self._buildtargetpath, filename)
                    assert not fileTools.checkFileExist(filepath)
                    gdlib_file(basepath, libname)
                    gdns_file(basepath, libname)
        except AssertionError :
            log("gdnlib file already exist, cannot create it")
            raise
        



# allow to run from a shell-run python:
# python3 estragon_gdnative.py path_to_godot_project_root
if __name__ == "__main__":
    print("estragon estragon_gdnative command called from shell")
    from sys import argv
    try:
        builder = build_gdnative_cpp(argv[1], True)
        builder.build_gdnative_libs(" ".join(argv[2:]))
        builder.connect_to_godot()
    except Exception:
        print ("an error occured, printing log : ")
        print(log.get_log())
        print("end of log \n")
        raise
    
