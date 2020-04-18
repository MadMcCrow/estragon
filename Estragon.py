#
#   Estragon is a simple collection of tools 
#   to automate some frequent Godot tasks
#

#import modules
from Modules.Estragon_Log           import EstragonLog          as Log
from Modules.Estragon_Config        import EstragonConfigFile   as ConfigFile
from Modules.Estragon_GodotEditor   import EstragonGodotEditor  as GodotEditor 


class Version   :
    
    # Estragon Version
    VersionNum = 1.1
    Appendix = str()

    def __init__(self):
        super().__init__()
        try :
            from os import getcwd
            from os import path
            from git import Repo
            temprepo = Repo(path.join(getcwd()))
            assert not temprepo.bare      
        except AssertionError  :
            Log("Running a non-git version")
        else    :
            self.Appendix = temprepo.active_branch
        finally :
            vstr = "Estragon V" + str(self.VersionNum) + str(self.Appendix)
            print(vstr)
            Log(vstr)

# class to handle after program cleaning
class End :
    
    # if any cleaning necessary it will happen here
    def _Clean(self)    :
        return

    def __init__(self):
        super().__init__()
        self._Clean()
        print("That's all folks !")

class _EnumValue()    :

    __name__ = "TEST"
    def __repr__(self) :
        return "salut"

    def __str__(self) :
        return "salut"


# Main Estragon Class 
class Estragon      :
    
    # is defined as Estragon.Error 
    class Error(Exception) :
        pass

    # Class to define program tasks
    from enum import Enum
    class Task(Enum)  :
        Nothing     = 0
        GetEditor   = 1
        Build       = 2
        Run         = 3
        Interactive = 4
        


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

    def _help(self)  :
        helptext = """Usage : Estragon [options]

        Available commands : 
        -p  --path [path_to_godot]          : Specify the path for download/godot sources
        -e  --get_editor                    : get godot editor (download/update will not build)
        -b  --build                         : Build godot
        -a  --build_args [build_arguments]  : Build arguments
        -r  --repo                          : url of the godot repository you wanna use
        -i  --interactive                   : run interactively to have more functions
        commands can be set in any order
        """
        print(helptext)


    def _SaveConfigToFile(self) :
        if self._EstragonConfig is None:
            from os import getcwd
            self._EstragonConfig = ConfigFile(getcwd())
        if self._ExecPath is not None   :
            self._EstragonConfig.saveValue("Path", str(self._ExecPath))
        if self._ExtraArgs is not None  :
            self._EstragonConfig.saveValue("ExtraArgs", str(self._ExtraArgs))
        
    def _LoadFromConfig(self, pathToConfig):
            try:
                assert self._EstragonConfig is not None
                assert self._ExtraArgs is None
                assert self._ExecPath is None
                self._ExtraArgs = self._EstragonConfig.getValue("ExtraArgs")
                self._ExecPath = self._EstragonConfig.getValue("Path")
            except AssertionError :
                Log("Error occurs when trying to load from config")

    def _getEditor(self, path, branch = None) :
        Log("Getting Godot")
        self._Editor = GodotEditor(path)
        try :
            assert self._RepoUrl is not None
            self._Editor.InitFromSource(self._RepoUrl)
        except AssertionError   :                        
            self._Editor.InitFromSource()

    def _runInteractive(self) :
            from Modules.Estragon_Interactive import StartInteractive
            StartInteractive()

    def _build(self, path, args) :
        Log("Building Godot")
        if self._Editor is not None:
            self._Editor.BuildEditor(args)

    def _ParseArgs(self) :

        from sys    import argv      
        from getopt import getopt
        from getopt import GetoptError
        # alias for easier read
        Task = Estragon.Task

        try:   
            opts, args = getopt(argv[1:], "iheba:p:dr:", ["interactive", "help","get_editor", "build", "build_args=","path=", "debug", "repo="])
        except GetoptError:         
            self._help()
            raise Estragon.Error()
        Log("opts are " + str(opts))
        Log("args are " + str(args))
        for opt, arg in opts:      
            if opt in ('-i', "--interactive"):
                # ignore all other tasks
                self._Tasks = []
                self._Tasks.append(Task.Interactive)
                break
            elif opt in ("-h", "--help"):
                self._help()
            elif opt == '-d':
                Log.EnableDebug(True)
            elif opt in ("-p", "--path"):
                self._ExecPath = arg
            elif opt in ("-a", "--build_args"):
                self._ExtraArgs = arg
            elif opt in ("-e", "--get_editor"):
                self._Tasks.append(Task.GetEditor)
            elif opt in ("-r", "--repo"):
                self._RepoUrl = arg
            elif opt in ("-b", "--build"):
                self._Tasks.append(Task.Build)


    def _DoTask(self)   :
        Task = Estragon.Task
        try :
            assert self._Tasks is not None
            assert len(self._Tasks) > 0
        except AssertionError   :
            print("No command specified, please see help")
            Log("no task ordered, will not do anything")
            self._help()
        else :
            if Task.Interactive in self._Tasks    :
                Log("starting task : interactive")
                self._runInteractive()
                return
            if Task.GetEditor in self._Tasks    :
                Log("starting task : get editor")
                self._getEditor(self._ExecPath)
                return
            if Task.Build in self._Tasks    :
                Log("starting task : build")
                self._build(self._ExecPath, self._ExtraArgs)
        

    # init the main object
    def __init__(self):
        super().__init__()
        Version()
        try:
            self._ParseArgs()
            self._DoTask()
        except Exception as err:
            Log("Error occured when running Estragon")
            print(str(Log.GetLog()))
            print(err)
            raise
        finally :
            End()


# launch Estragon               
Main = Estragon()

