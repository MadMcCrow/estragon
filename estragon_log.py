#Copyright (c) 2020 Noé Perard-Gayot. All rights reserved.
# This work is licensed under the terms of the MIT license. 
# For a copy, see <https://opensource.org/licenses/MIT>.

# A nice log that behave as a singleton.
# Allows you to store debug info and display them if an error occurs at some point
class log(object)   :

    #inner singleton class
    class __estragon_log:

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
        def printToLog(self, *intexts)    :
            # formating variadic
            text = str()
            itemlist = list(*intexts)
            for t in itemlist   :
                text += str(t) + " "
            
            # getting context :
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
            raise NotImplementedError



    #instance of singleton
    instance = None

    # call to log()
    def __init__(self, *arg):
        if not log.instance:
            log.instance = log.__estragon_log()
        log.instance.printToLog(arg)

    #def __getattr__(self, name):
    #   return getattr(self.instance, name)

    @staticmethod
    def enable_debug(enable :bool = True)   :
        log.instance.debug = enable

    @staticmethod
    def is_debug()   :
        return log.instance.debug is True


    @staticmethod
    def get_log()    :
        return log.instance
    
    
