#
#   Estragon is a simple collection of tools 
#   to automate some frequent Godot tasks
#

#   Class for log, will allow for more custom log
class EstragonLog   :

    def PrintToLog(self, text)  :
        import inspect
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print(str(calframe[1][3]) + " - "+ str(calframe[2][3]) + " : " + text)


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
    _settingsDictionnary = None

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
        return _Path

    # allow to get the current branch we're using
    def getBranch(self) :
        return _branch

    # default initializer should not be called directly
    def __init__(self):
        super().__init__()


    def _UpdateFromRepo(self)   :
        from git import Repo
        self._Path   = self._repo.working_tree_dir
        self._branch = self._repo.active_branch
        Log( str(self._Path) + " is on branch " + str(self._branch) )

    
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
    