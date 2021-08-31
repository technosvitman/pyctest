
import sys
import io
import os
import argparse
import yaml
from lxml import etree

'''
    @brief class to convert PycTester report to portable format
'''
class PycConverter():

    '''
        @brief initialise PycConverter
    '''
    def __init__(self):
        self.__report = {"suites":[]}
    
    '''
        @brief append report file to converter
        @param filename the report file to append
    '''
    def appendReport(self, filename):
        yaml_content = None
        try:
            with open(filename, "r") as f :                
                yaml_content = yaml.load(f, Loader=yaml.FullLoader)
        except IOError:
            yaml_content = {\
                    "start":0, \
                    "duration":0,\
                    "success":0,\
                    "failure":1,\
                    "error":0,\
                    "tests":[\
                        {\
                            "title":"Report file not found",\
                            "result":"%s Not found"%filename,\
                            "duration":0}\
                    ]}
        yaml_content["title"] = filename
        self.__report["suites"].append(yaml_content)
        
    '''
        @brief build JUnit report
        @param file the output report file
    '''
    def toJunit(self, file):
        suites = etree.Element("testsuites")
        
        st = 0
        sf = 0
        sd = 0
        
        for s in self.__report["suites"]:
            suite = etree.SubElement(suites, "testsuite")
            suite.set("name", "PycTest:%s"%s["title"])
            suite.set("failures", str(s["failure"]))
            suite.set("time", str(s["duration"]))
            sf += s["failure"]
            t=0
            sd += s["duration"]
            
            for c in s["tests"]:
                case = etree.SubElement(suite, "testcase")
                case.set("name", c["title"])
                case.set("time", str(c["duration"]))
                t += 1
                if c["result"] != "ok":
                    failure = etree.SubElement(case, "failure")
                    failure.set("message", c["result"])
            suite.set("tests", str(t))
            st += t
        
        suites.set("failures", str(sf))
        suites.set("tests", str(st))
        suites.set("time", str(sd))
        file.write(etree.tostring(suites, pretty_print=True))
                
     
    '''
        @brief string representation
    '''
    def __str__(self):
        return str(self.__report)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PycConverter : PycTester report converter')
    parser.add_argument("-i", nargs='+', type=str, required=True)
    parser.add_argument("-o", type=str, default=None)
    
    args = parser.parse_args()
    conv = PycConverter()
    for filename in args.i :
        conv.appendReport(filename)
        
            
    with open(args.o, "wb") as f:
        conv.toJunit(f)