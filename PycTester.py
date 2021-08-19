
import sys
import io
import os
import cffi
from cffi import *
import pycparser
import pycparser_fake_libc
import subprocess
import re
import importlib
import unittest
from ctypes import *
from . import *

class PycTester():

    def __init__(self):                
        self.__ffi = FFI()
        self.__sources = ""
        self.__includes = ""
        self.__testcases = unittest.TestSuite()
        
    '''
        @brief load from c string
        @param filename
    '''
    def load_source(self, code): 
        # load source code
        self.__sources += code
        
    '''
        @brief load from h string
        @param filename
    '''
    def load_header(self, code): 
        # load header code
        self.__includes += code
        
    '''
        @brief load from c file
        @param filename
    '''
    def load_source_file(self, filename): 
        # load source code
        self.load_source(str(open(filename).read()))
        
    '''
        @brief load from h file
        @param filename
    '''
    def load_header_file(self, filename): 
        # load header code
        self.load_header(str(open(filename).read()))
        
    '''
        @brief build library from module files
        @param filename
    '''
    def load_module(self, filename): 
        # load source code
        self.load_source_file(filename + '.c')
        self.load_header_file(filename + '.h')
        if os.path.exists( filename + '_types.h' ) :
            self.load_header_file(filename + '_types.h')
        
    '''
        @brief build library from c file
    '''
    def preprocess(self):
        return subprocess.run(['gcc', '-nostdinc', '-E', "-I" + pycparser_fake_libc.directory, '-P', '-'],
            input=self.__includes, stdout=subprocess.PIPE,
            universal_newlines=True, check=True).stdout
            
            
    '''
        @brief build library
        @param name the custom lib name
    '''
    def build(self, name):
        print("Compile lib\t\t"+name)
        # pass source code to CFFI
        self.__ffi.cdef(self.preprocess())
        self.__ffi.set_source(name + '_', self.__sources)
        self.__ffi.compile()
        
        # import resulting module
        module = importlib.import_module(name + '_')
        
        self.__lib = module.lib
        
    '''
        @brief append test case
    '''
    def appendTest(self, test):      
        test.setFFI(self.__ffi)     
        test.setLib(self.__lib)
        self.__testcases.addTest(test)    
            
            
    '''
        @brief unitary test for C library
    '''
    def run(self):      
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(self.__testcases)
        if not result.wasSuccessful():
            exit(-1)
        