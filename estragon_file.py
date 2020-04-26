# Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.


from estragon_log   import log
from os             import mkdir
from os             import path
from os             import listdir


## fileTools :
## collection of tools to use files and folders
class fileTools():

    ## makeDir :
    ## Try to make a directory. also works if folder already exists
    @staticmethod
    def makeDir(dir_path) :
        try:
            mkdir(dir_path)
        except FileExistsError      :
            log("Directory " ,dir_path, " already exists")
            # this is fine
        except FileNotFoundError    :
            # this is wrong
            log("Directory " ,dir_path , " failed to create folder")
            raise
        else    :
            log("Directory " , dir_path, " Created ") 


    ## CheckFileExist : bool
    ## use within an assert for contract programming
    @staticmethod
    def checkFileExist(file_path) -> bool :
        if not path.isfile(file_path):
            return False

    ## getSubdirs : list
    ## get a list of subfolders in a folder
    @staticmethod
    def getSubdirs(abs_path_dir : str) -> list : 
        lst = [ name for name in listdir(abs_path_dir) if path.isdir(path.join(abs_path_dir, name)) and name[0] != '.' ]
        lst.sort()
        return lst

    ## getSubFiles : list
    ## get a list of files in a folder
    @staticmethod
    def getSubFiles(abs_path_dir : str) ->list : 
        lst = [ name for name in listdir(abs_path_dir) if path.isfile(path.join(abs_path_dir, name)) and name[0] != '.' ]
        lst.sort()
        return lst

    ## getFileExt : str
    ## get the extension from any file, anywhere
    @staticmethod
    def getFileExt(abs_path :str) -> str :
        return path.splitext(path.basename(abs_path))[1]

    ## getFileBase : str
    ## get the base name without extension from any file, anywhere
    @staticmethod
    def getFileBase(abs_path :str) -> str :
        return path.splitext(path.basename(abs_path))[0]


## file
## estragon abstaction of file concept
## TODO : file is not a keyword in python, but may cause conflicts
class file(object) :

    # os path to this file
    _path = str()
    
    # reference to the file content
    _file = None

    # sanity variable
    _is_open = False

    ## create :
    ## close file with extra debugging
    def close(self) :
        try:
            self._file.close()
        except IOError:
            log("could not close : file not accessible, stopping")
            raise
        else:
            self._is_open = False
            self._file = None
    
    ## create :
    ## open file with extra debugging in write mode
    def create(self) :
        try:
            self._file = open(self._path, "w")
        except IOError:
            log("could not create/overwrite : file not accessible, stopping")
            raise
        else:
            self._is_open = True

    ## open :
    ## open file with extra debugging
    def open(self)  :
        try:
            self._file = open(self._path, "a")
        except IOError:
            log("could not open : file not accessible, stopping")
            raise
        else:
            self._is_open = True

    ## writeText
    ## write text to file, assume it's open
    def writeText(self, text : str):
        assert self._is_open
        assert self._file is not None
        self._file.write(text)

    ## __init__ :
    ## init a file with path
    def __init__(self, file_path: str):
        super().__init__()
        self._path = file_path
    
## configFile :
## represent a config file with sections
## TODO : Read from file formated
class configFile(file)  :

    ## section
    ## class to write down info
    class section(object)   :

        _SectionName = str()
        _SectionNameDelimiters = '[]'
        _SectionEntries = dict()

        def __init__(self, name : str = 'entry' , delimiters : str = '[]') :
            super().__init__()
            assert len(name) > 0
            assert len(delimiters)%2 == 0
            self._SectionName = name
            self._SectionNameDelimiters = delimiters
            self._SectionEntries = dict()


        def lDelimiter(self) -> str :
            return self._SectionNameDelimiters[:int(len(self._SectionNameDelimiters)/2)]
        
        def rDelimiter(self) -> str :
            return self._SectionNameDelimiters[int(len(self._SectionNameDelimiters)/2):]

        def title(self) -> str :
            return "".join([self.lDelimiter(), self._SectionName, self.rDelimiter()])

        def addEntry (self, key : str, value : str) :
            self._SectionEntries[key] =  value

        def addEntries (self, entries : dict)   :
            self._SectionEntries.update(entries)

        def format(self) -> str:
            return "\n".join([self.title(),*( '%s=%s' % (str(key), str(value)) for (key, value) in self._SectionEntries.items())]) + "\n"

        def __str__(self)  ->str :
            return self.format()

        def __repr__(self)  :
            return self.__str__()


    ## _Sections : list
    ## list of all the sections in this file
    _Sections = list()

    ## _SectiondDel :
    ## Section name delimiters
    ## TODO : store only at file level
    _SectiondDel = '[]'

    def __init__(self, file_path, delimiters : str = '[]') :
        super().__init__(file_path)
        self._Sections = list()
    
    def addSection(self, name : str, entries : dict):
        newSection = self.section(name, self._SectiondDel)
        newSection.addEntries(entries)
        self._Sections.append(newSection)

    def writeConfig(self) :
        self.create()
        self.writeText("\n".join(( (str(sect) for (sect) in self._Sections))))
        self.close()



