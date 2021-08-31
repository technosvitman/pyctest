import unittest
import time

class PycTestCase(unittest.TestCase):
    
    '''
        @brief init Test case for C lib
    '''
    def __init__(self):
        super(unittest.TestCase, self).__init__("runTest")
        self.__ffi = None
        self._l = None
        self.__testDuration=0
        self.__testStartTime=0
    
    '''
        @see unittest.Testcase
    '''
    def setUp(self):
        self.__testStartTime = time.time()
   
    '''
        @see unittest.Testcase
    '''
    def tearDown(self):
        self.__testDuration = time.time() - self.__testStartTime
        
    '''
        @brief return test duration        
    '''   
    def getDuration(self):
        return self.__testDuration
          
    '''
        @brief return a null pointer
    '''
    def NULL(self): 
        return self.__ffi.NULL
    
    '''
        @brief call C method with it's name
    '''
    def call(self, name, args=None):
        meth = getattr(self, "c_"+name)
        if args :
            return meth(*args)
        else:
            return meth()
    
    '''
        @brief set ffi 
        @param ffi the ffi instance
        @warning only called by PycTester
    '''
    def setFFI(self, ffi):    
        self.__ffi = ffi
    
    '''
        @brief create new var
        @param var_type the new variable type
        @param var_content the initialization content
        @return the new variable
    '''
    def new(self, var_type, var_content=None):    
        return self.__ffi.new(var_type, var_content)
    
    '''
        @brief get address of a variable
        @param variable the variable
        @return the address
    '''
    def addressof(self, variable):    
        return self.__ffi.addressof(variable)
    
    '''
        @brief get string object for c string
        @param variable the variable
        @return the string
    '''
    def tostring(self, variable):    
        return self.__ffi.string(variable)
        
    '''
        @brief set generated lib  
        @param lib the lib instance
        @warning only called by PycTester
    '''
    def setLib(self, lib):    
        self.__lib = lib
        for element in dir(self.__lib):
            setattr(self , "c_"+element, getattr(self.__lib, element) )
        
    '''
        @brief test method called by the test case
    '''
    def runTest(self):
        pass