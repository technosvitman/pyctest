
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
        @param file the report file to append
        @param file the output report file
    '''
    def appendReport(self, file, title):
        yaml_content = yaml.load(file, Loader=yaml.FullLoader)
        yaml_content["title"] = title
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
        with open(filename, "r") as f :
            conv.appendReport(f, filename)
            
    with open(args.o, "wb") as f:
        conv.toJunit(f)