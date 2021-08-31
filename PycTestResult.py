
import unittest
import time
from datetime import datetime
import yaml
from .PycTestCase import PycTestCase

'''
    @brief format output as yaml
'''
class PycTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        self.__report={\
                    "start":0, \
                    "duration":0,\
                    "success":0,\
                    "failure":0,\
                    "error":0,\
                    "tests":[]}
        self.__startdate = 0
        self.__testStart = 0
        super(PycTestResult, self).__init__(*args, **kwargs)
        
    '''
        @brief append test result line
        @param test current test
        @param result the result
    '''
    def __appendResult(self, test, result):
        self.__report["tests"].append(\
            {"title": str(test), "duration":test.getDuration(), "result":str(result)})
    
    '''
        @see unittest.TestResult
    '''
    def startTestRun(self):
        self.__startdate=time.time()
        self.__report["start"]=str(datetime.fromtimestamp(self.__startdate))
        super(PycTestResult, self).startTestRun()
    
    '''
        @see unittest.TestResult
    '''
    def stopTestRun(self):
        self.__report["duration"]=time.time()-self.__startdate
        super(PycTestResult, self).stopTestRun()
    
    '''
        @see unittest.TestResult
    '''
    def addError(self, test, err):
        self.__appendResult(test, err)
        self.__report["error"] += 1
        super(PycTestResult, self).addError(test, err)
    
    '''
        @see unittest.TestResult
    '''
    def addFailure(self, test, err):
        self.__appendResult(test, err)
        self.__report["failure"] += 1
        super(PycTestResult, self).addFailure(test, err)
    
    '''
        @see unittest.TestResult
    '''
    def addSuccess(self, test):
        self.__appendResult(test, "ok")
        self.__report["success"] += 1
        super(PycTestResult, self).addSuccess(test)
    
    '''
        @brief write report to file
        @param the file to write
    '''
    def toFile(self, file):
         yaml.dump(self.__report, file, default_flow_style=False, indent=1, sort_keys=False)

    
    
    
    
        