
from Modules.Estragon_Log import EstragonLog as Log

#   Class for godot sources and installation
class Sources       :


    _branch = "master"  # the installed branch
    _Path   = None      # the path to the installation
    _repo   = None

    # gets the path of this repository
    def getPath(self)   :
        return self._Path

    # allow to get the current branch we're using
    def getBranch(self) :
        return self._branch

    # default initializer should not be called directly
    def __init__(self):
        super().__init__()


    def _UpdateFromRepo(self)   :
        from git import Repo
        if self._repo  is not None:
            self._Path   = self._repo.working_tree_dir
            self._branch = self._repo.active_branch
            self._repo.git.pull()
            Log(self._repo.git.status())


    # static method to get a valid Sources object with a local repository
    @staticmethod
    def GetLocalSource( path)    :
        import os.path
        from git import Repo
        retsource = Sources()
        retsource._repo = Repo(os.path.join(path, 'godot'))
        retsource._UpdateFromRepo()
        return retsource

    # static method to get a valid Sources object with a distant repository
    @staticmethod
    def GetFromOriginSource(path, originRepo = "https://github.com/godotengine/godot.git")    :
        import os.path
        from git import Repo
        retsource = Sources()
        retsource._repo = Repo.clone_from(originRepo, os.path.join(path, 'godot'))
        retsource._UpdateFromRepo()
        return retsource

    # static method to get a valid Sources object fully automated (will select for you the correct version)
    @staticmethod
    def GetGodotSource(path, originRepo = "https://github.com/godotengine/godot.git")   :
        import os.path 
        fullpath = os.path.join(path, 'godot')
        if os.path.isfile(os.path.join(fullpath,"README.md"))   :
            Log("path already in use, trying to get repo")
            return Sources.GetLocalSource(path)
        else                                            :
            Log("path not in use, cloning repo")
            return Sources.GetFromOriginSource(path, originRepo)
        return None

        
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

