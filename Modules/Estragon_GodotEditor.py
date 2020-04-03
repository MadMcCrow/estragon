
from Modules.Estragon_Log       import EstragonLog  as Log
from Modules.Estragon_Sources   import GodotSources as Sources

class Build()   :
    
    # Number of CPU core available
    _CPUAvailable   = 1

    # Path to Godot sources
    _SourcesPath     = None

    # Check if we have all necessary Build tools
    @staticmethod
    def CheckBuildTools()   :
        from shutil import which
        if which("scons") is None:
            return False
        from sys import platform
        if platform.startswith('win'):
            from os import environ
            if environ.get('VS140COMNTOOLS') is None :
                Log("Building on windows without visual studio, not supported by Estragon ")
                return False
        return True  
    

    def buildGodot(self, path, extraArgs) :
        if Build.CheckBuildTools() is False   :
            return
        #avoid null argument
        if extraArgs is None    :
            extraArgs = ''

        # make sure the target is the correct platform
        from sys import platform
        buildplateform = platform
        if platform.startswith('linux'):
            buildplateform = "x11"
        if platform.startswith('win'):
            buildplateform = "windows"

        #look for the correct path
        from os import chdir
        from os import path
        buildpath = path.join(self._SourcesPath, 'godot')
        chdir(buildpath)
        Log("Building godot on path = " + buildpath)

        # building the command line
        cli = "scons " + "-j"+ str(self._CPUAvailable) + " platform=" + buildplateform + " " + extraArgs + " -Q"
        Log( "Build command  = " + cli)

        # time stamping
        import time
        from datetime import datetime
        startTime = time.time()
        Log("Scons started at " + str(datetime.fromtimestamp(startTime)))
 
        # for windows be sure to launch command in powershell, not CMD
        if platform.startswith('win')   :
           cli = "powershell" + cli

        # launching scons
        # asking the system to run the command
        from subprocess import DEVNULL
        from subprocess import check_call as call
        from shlex import split as clisplit

        if Log.IsDebug :
            call(clisplit(cli),stdin=DEVNULL)
        else            :
            call(clisplit(cli),stdin=DEVNULL, stdout=DEVNULL)
            
        # timestamping again
        endTime = time.time()
        Log("Scons finished at " + str(datetime.fromtimestamp(endTime)))
        duration = endTime - startTime
        Log("Build Took :" + f"{duration:.3f}" + "s")


    # init the builder
    # find how many threads are availables
    def __init__(self, path = None)  :
        super().__init__()
        from multiprocessing    import cpu_count
        self._CPUAvailable = cpu_count()
        self._SourcesPath = path

    # build editor with this current builder
    def BuildEditor(self, extraArgs = None)    :
        if self._SourcesPath is not None     :
            self.buildGodot(self._SourcesPath, extraArgs)
        return


# Class representing the Editor
# contains a builder, a path and access to source version management
class EstragonGodotEditor    :

    # Path to this Editor
    _EditorPath = None

    # Access to Code Source
    _Source = None

    # Access to Build Tool
    _Builder = None

    def InitFromSource(self, repo = "https://github.com/godotengine/godot.git") :
        self._Source = Sources.GetGodotSource(self._EditorPath, repo)

    def BuildEditor(self, Args) :
        self._Builder = Build(self._EditorPath)
        self._Builder.BuildEditor(Args)

    def __init__(self, Path = None)    :
        super().__init__()
        self._EditorPath = Path
        if Path is None    :
            from os import getcwd
            self._EditorPath = getcwd()

