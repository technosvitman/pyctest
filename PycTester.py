
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
from shutil import copyfile
from . import *

class PycTester():

    def __init__(self):                
        self.__ffi = FFI()
        self.__sources = ""
        self.__includes = ""
        self.__testcases = unittest.TestSuite()
        self.__loadedfiles = []
    
    '''
        @brief prepare file for compilation by copying to main directory
        @return temporary filename
    '''
    def __prepare(self, path):
        rel = os.path.relpath(path)
        dirname = os.path.dirname(rel)
        filename = os.path.basename(rel)
        if dirname != "":
            copyfile(path, filename)
            self.__loadedfiles.append(filename)
            return filename
        return path
        
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
        filename=self.__prepare(filename)
        self.load_source(str(open(filename).read()))
        
    '''
        @brief load from h file
        @param filename
    '''
    def load_header_file(self, filename): 
        # load header code
        filename=self.__prepare(filename)
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
        
        # clean temporary files
        os.remove(name+"_.c")
        for f in self.__loadedfiles:
            os.remove(f)
        
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
        @param out the log output
    '''
    def run(self, out = sys.stdout):      
        runner = unittest.TextTestRunner(out, verbosity=2)
        result = runner.run(self.__testcases)
        if not result.wasSuccessful():
            exit(-1)
        