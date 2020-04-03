#
#   Estragon is a simple collection of tools 
#   to automate some frequent Godot tasks
#

class Version   :

    def __init__(self):
        super().__init__()
        print("Estragon V1.0")

debug = False

#   Class for log, will allow for more custom log
class EstragonLog   :

    _LogString = str()

    def PrintToLog(self, intext)    :
        text = str()
        if isinstance(intext, str)  :
            text = intext
        if isinstance(intext, list) :
            if len(intext) > 0      :
                if isinstance(intext[0], str)   :
                    text =  ', '.join(intext)
        
        import inspect
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        global debug
        if debug :
            print(str(calframe[1][3]) + " - "+ str(calframe[2][3]) + " : " + text)
        self._LogString = self._LogString + str(calframe[1][3]) + " - "+ str(calframe[2][3]) + " : " + text + "\n"


    def __init__(self)          :
        super().__init__()

# spawning a Log singleton and declaring its function
MainLog = EstragonLog()
def Log(text)   :
    MainLog.PrintToLog(text)

#   Class for saving estragon preferencies
class ConfigFile    :
    # path to the file
    _configPath = None

    # path to the file
    _settingsDictionnary = dict()

    #read the dictionnary from an actual file
    def _ReadFromFile(self) :
        file_object = open(self._configPath, "r")
        lines = file_object.readlines()
        file_object.close()
        for t in lines	:
            pair = t.split("=")
            field = pair[0]
            value = pair[1]
            Log("retrieving " + field + " : " + value + " from "  + self._configPath)
            self._settingsDictionnary[field] = value
        

    #save the dictionnary to an actual file
    def _saveToFile(self)   :
        file_object = open(self._configPath, "w")
        x = self._settingsDictionnary.items()
        for t in x	:
            strln = str(t[0]) + "=" + str(t[1])
            Log("adding " + strln + " to file " + self._configPath)
            file_object.write(strln)
        file_object.close() 


    # make sure that the file and the object are in sync
    def sync(self)  :
        self._saveToFile()
        self._ReadFromFile()

    # save a value (new or not) to this file
    def saveValue (self, field, value)     :
        if field in self._settingsDictionnary    :
            Log(("Overriding " + field + " with " + value))
        else                                :
            Log(("Adding " + field + " with " + value))
        ''' actually saving the variable '''
        self._settingsDictionnary[field] = value 
        self.sync()

    # save a value (new or not) to this file
    def getValue (self, field)     :
        self.sync()
        return self._settingsDictionnary[field]

    def __init__(self, path):
        super().__init__()
        self._configPath = path
        self.sync()

   

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
    
    @staticmethod
    def buildGodot(path, extraArgs) :
        import time;
        startTime = time.time()
        if Build.CheckBuildTools() is False   :
            return
        if extraArgs is None    :
            extraArgs = ''
        from sys import platform
        buildplateform = platform
        if platform.startswith('linux'):
            buildplateform = "x11"
        if platform.startswith('win'):
            buildplateform = "windows"
        from os import chdir
        from os import path as ospath
        chdir(ospath.join(path, 'godot'))
        cli = "scons platform=" + buildplateform + " " + extraArgs
        Log( "Build command  = " + cli)
        from os import system
        if platform.startswith('win'):
            system("powershell" + cli)
        else:
            system(cli)
        endTime = time.time()
        Log("Scons finished at endTime")
        duration = endTime - startTime
        Log("Build Took :" + duration + "s")

    def __init__(self, path = None)  :
        super().__init__()
        from multiprocessing    import cpu_count
        self._CPUAvailable = cpu_count
        self._SourcesPath = path

    def BuildEditor(self, extraArgs = None)    :
        if self._SourcesPath is not None     :
            self.buildGodot(self._SourcesPath, extraArgs)
        return


# Class representing the editor
class GodotEditor    :

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



class Main      :
    

    class Task()        :

        from enum import Enum
        class Type(Enum)          :
            Nothing     = 0
            GetEditor   = 1
            Build       = 2
            Run         = 3

        _Value = Type.Nothing

        def ToString(self)        :
            switcher = {
                        Main.Task.Type.Nothing   : "Nothing",
                        Main.Task.Type.GetEditor : "GetEditor",
                        Main.Task.Type.Build     : "Build",
                        Main.Task.Type.Run       : "Run" 
                        }
            return switcher.get(self._Value)

        @staticmethod
        def FromString(String)      :
            switcher = {
                        "Nothing"       : Main.Task.Type.Nothing ,
                        "GetEditor"     : Main.Task.Type.GetEditor,
                        "Build"         : Main.Task.Type.Build  ,
                        "Run"           : Main.Task.Type.Run 
                        }
            return Main.Task(switcher.get(String))

        def __init__(self, newType)  :
            super().__init__()
            self.Set(newType)

        def Get(self)   :
            return self._Value

        def Set(self, newType)  :
            self._Value = newType

        def Is(self, compType)  :
            return (self._Value == compType)

       

    # Path Given to the main
    _ExecPath = None

    #Args you want to specify for build
    _ExtraArgs = None

    # Tasks
    _Tasks = [] 

    # Editor to use
    _Editor = None

    # Configuration data we should be able to read and write
    _EstragonConfig = None

    # url to use when cloning from github
    _RepoUrl = None

    # Whether we should be debugging or not 
    _debug = False

    def _help(self, reason = 0)  :
        from sys import exit    
        helptext = """Usage : Estragon [options]

        Available commands : 
        -p  --path [path_to_godot]          : Specify the path for download/godot sources
        -e  --get_editor                    : get godot editor (download/update will not build)
        -b  --build                         : Build godot
        -a  --extra_args [build_arguments]  : Build arguments
        -r  --repo                          : url of the godot repository you wanna use

        commands can be set in any order
        """
        if reason != 0  :
            print("you have to specify arguments for Estragon \n")
        print(helptext)
        exit(reason)


    def _SaveConfigToFile(self) :
        if self._EstragonConfig is None:
            from os import getcwd
            self._EstragonConfig = ConfigFile(getcwd())
        if self._ExecPath is not None   :
            self._EstragonConfig.saveValue("Path", str(self._ExecPath))
        if self._ExtraArgs is not None  :
            self._EstragonConfig.saveValue("ExtraArgs", str(self._ExtraArgs))
        
    def _LoadFromConfig(self, pathToConfig):
            if self._EstragonConfig is not None:
                if self._ExtraArgs is not None :
                    Log("overriding Extra Args ")
                self._ExtraArgs = self._EstragonConfig.getValue("ExtraArgs")
                if self._ExecPath is not None :
                    Log("overriding Exec path ")
                self._ExecPath = self._EstragonConfig.getValue("Path")

    def _getEditor(self, path) :
        Log("Getting Godot")
        self._Editor = GodotEditor(path)
        if self._RepoUrl is not None :
            self._Editor.InitFromSource(self._RepoUrl)
        else                         :
            self._Editor.InitFromSource()

    
    def _build(self, path, args) :
        Log("Building Godot")
        if self._Editor is not None:
            self._Editor.BuildEditor(args)

    def _ParseArgs(self) :
        from sys    import argv      
        from getopt import getopt
        from getopt import GetoptError
        try:   
            opts, args = getopt(argv[1:], "heba:p:dr:", ["help","get_editor", "build", "build_args=","path=", "debug", "repo="])
        except GetoptError:          
            self._help(2)
        Log(opts)
        Log(args)
        for opt, arg in opts:               
            if opt in ("-h", "--help"):
                self._help()
            elif opt == '-d':
                global debug
                debug = True
            elif opt in ("-p", "--path"):
                self._ExecPath = arg
            elif opt in ("-a", "--build_args"):
                self._ExtraArgs = arg
            elif opt in ("-e", "--get_editor"):
                self._Tasks.append(Main.Task(Main.Task.Type.GetEditor))
            elif opt in ("-r", "--repo"):
                self._RepoUrl = arg
            elif opt in ("-b", "--build"):
                self._Tasks.append(Main.Task(Main.Task.Type.Build))


    def _DoTask(self)   :

        if  self._Tasks is None or (len(self._Tasks) <= 0 or self._Tasks[0].Is(Main.Task.Type.Nothing) ) :
            Log(" No task ordered, will not do anything")
            self._help()
            return
        Gets =  [i for i, x in enumerate(self._Tasks) if x.Is(Main.Task.Type.GetEditor)]
        if len(Gets) >= 1 :
            Log("starting task : get editor")
            self._getEditor(self._ExecPath)
        Builds =  [i for i, x in enumerate(self._Tasks) if x.Is(Main.Task.Type.Build)]
        if len(Builds) >= 1 :
            Log("starting task : build")
            self._build(self._ExecPath, self._ExtraArgs)
        
    

    # init the main object
    def __init__(self):
        super().__init__()
        Version()
        self._ParseArgs()
        self._DoTask()
        return


# launch Estragon               
Estragon = Main()

