

# contain import into class 
from Modules.Estragon_Log import EstragonLog as Log
    

#   Class for saving estragon preferencies
class EstragonConfigFile    :
 
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

   