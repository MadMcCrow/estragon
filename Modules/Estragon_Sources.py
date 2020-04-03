from Modules.Estragon_Log import EstragonLog as Log

#Class representing a git repository
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