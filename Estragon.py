#
#   Estragon is a simple collection of tools 
#   to automate some frequent Godot tasks
#

#import modules
from Modules.Estragon_Log           import EstragonLog          as Log
from Modules.Estragon_Config        import EstragonConfigFile   as ConfigFile
from Modules.Estragon_GodotEditor   import EstragonGodotEditor  as GodotEditor 


#
class Version   :
    
    # Estragon Version
    VersionNum = 1.1

    def __init__(self):
        super().__init__()
        vstr = "Estragon V" + str(self.VersionNum)
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


# Main Estragon Class 
class Main      :
    

    # Class to define program tasks
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
        -a  --build_args [build_arguments]  : Build arguments
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
        Log("opts are " + str(opts))
        Log("args are " + str(args))
        for opt, arg in opts:               
            if opt in ("-h", "--help"):
                self._help()
            elif opt == '-d':
                Log.EnableDebug(True)
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
        End()
        return


# launch Estragon               
Estragon = Main()

