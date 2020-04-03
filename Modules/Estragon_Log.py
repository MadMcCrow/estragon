#   Class for log, will allow for more custom log
class EstragonLog(object)   :

    #inner singleton class
    class __EstragonLog:

        # the enitre log string. 
        _LogString = str()
        
        # wether we should actually print to screen
        debug  = False

        # actual singleton init
        def __init__(self):
            self._LogString = str()

        # transform to string
        def __str__(self):
            return self._LogString

        # actual method called on init
        def PrintToLog(self, intext)    :
            text = str(intext)
            import inspect
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            # calframe[steps backs][info]
            # 2 steps backs correspond to the function directly calling EstragonLog()
            # which file called this
            from os.path import basename
            callfile = basename(str(calframe[2][1]))
            # which line
            callline = str(calframe[2][2])
            # wich function
            callfunc = str(calframe[2][3])
            # make a readable sentence out of it
            newlogstr = str(callfile +" " +  callfunc + " l" + callline + " : " + text)
            if self.debug  :
                print(newlogstr)
            self._LogString = self._LogString + " \n" + newlogstr

        # write entire log to file
        def WriteToFile(self, logfilepath)    :
            return NotImplemented

    #instance of singleton
    instance = None

    # call to Log()
    def __init__(self, arg):
        if not EstragonLog.instance:
            EstragonLog.instance = EstragonLog.__EstragonLog()
        EstragonLog.instance.PrintToLog(arg)

    #def __getattr__(self, name):
    #   return getattr(self.instance, name)

    @staticmethod
    def EnableDebug(Enable = True)   :
        EstragonLog.instance.debug = Enable

    @staticmethod
    def IsDebug()   :
        return EstragonLog.instance.debug is True

    
    