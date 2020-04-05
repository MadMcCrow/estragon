from Modules.Estragon_Log import EstragonLog as Log

#Class representing a git repository
class Sources       :

    _branch     = "master"  # the installed branch
    _Path       = None      # the path to the installation
    _repo       = None      # the repository object used in this object
    _OriginUrl  = None      # the git distant repository

    # gets the path of this repository
    def getPath(self)   :
        return self._Path

    # allow to get the current branch we're using
    def getBranch(self) :
        return self._branch

    # look if path is a valid repo or an empty folder
    def _initFromPath(self) :

        # without path we cannot init
        if self._Path is None:
            return False

        # Check path exists create folder if :
        from os import mkdir
        try:
            # Create target Directory
            mkdir(self._Path)
            Log("Directory "  + self._Path + " Created ") 
        except FileExistsError      :
            Log("Directory " + self._Path + " already exists")
        except FileNotFoundError    :
            Log("Directory " + self._Path + " failed to create folder")
            return False
        
        #TODO : improve that if Else logic

        # we now have a folder.
        from os import listdir
        # not not enable turning list dir into a boolean
        if not not listdir(self._Path)  : 
            # directory is not empty
            from os import path
            from git import Repo
            temprepo = Repo(path.join(self._Path))
            # it's an actual repo
            if not temprepo.bare       :
                # we have a valid repository
                if temprepo.remotes.count > 0 :
                    Log("Checking git config to get first remote url")
                    repoOriginUrl = temprepo.git.config('--get', 'remote.%s.url' % temprepo.remotes)
                    if self._OriginUrl is not None:
                        # comppare it and throw an error if it's not the same
                        if self._OriginUrl != repoOriginUrl :
                            Log("Error : Repo is not the same origin, please fix using git and come back later" )
                            return False
                        else                            :
                            # init our repo
                            self._repo = temprepo
                            self._OriginUrl = repoOriginUrl
                            self._branch = temprepo.head.reference.name
                            return True
                    else    :
                        Log("Warning local repo has no remote origin" )
                        self._repo = temprepo
                        self._branch = temprepo.head.reference.name
                        return False
                else    :
                    Log("Error this path is not a git repository")
                    return False
            else    :
               # Repository is empty
               Log("Error this path is not a git repository")
               return False
            

    # default initializer should not be called directly
    def __init__(self, Path = None, Origin = None, Branch = None):
        super().__init__()
        if Branch is not None :
            self._branch = Branch
        if Origin is not None :
            self._OriginUrl = None
        if Path is not None :
            self._Path   = None


    def _UpdateFromRepo(self)   :
        from git import Repo
        if self._repo  is not None:
            self._Path   = self._repo.working_tree_dir
            self._branch = self._repo.active_branch
            self._repo.git.pull()
            Log(self._repo.git.status())





# class representing Godot Sources
class GodotSources(Sources) :

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
            return GodotSources.GetLocalSource(path)
        else                                            :
            Log("path not in use, cloning repo")
            return GodotSources.GetFromOriginSource(path, originRepo)
        return None


    # static method to get a valid Sources object with a local repository
    @staticmethod
    def GetLocalSource( path)    :
        import os.path
        from git import Repo
        retsource = Sources()
        retsource._repo = Repo(os.path.join(path, 'godot'))
        retsource._UpdateFromRepo()
        return retsource