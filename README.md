# pyctest

C unit test with python
This library implement a C code compiler and loader interface

## Tester instance

In all this file we will use the following instance : 

```C
    myTester = PycTester()
```

## load code

To load code you have many method described here

### Load code from string

You can load from direct text like in example with these method:

* load_source
* load_header

```C
    myTester.load_source("#include \"sco_types.h\" \n")
```

### Load code from files

You can load from direct text like in example with these method:

* load_source_file
* load_header_file

```C
    myTester.load_source_file("my_file.c")
```

### Load code from module

These method load a module with following file construction :
*my_module.c
*my_module.h
*my_module_types.h

```C
    myTester.load_module("my_module")
```

## Build

Build previously loaded code with
   
```C     
    myTester.build("my_lib_name")
```

## Generate test cases

### Build your specific test

Extends the PycTestCase to build your own test class.
The *runTest* method will be runned automatically.
Refers to *Unittest* library

```Python
class MyTest(PycTestCase):
    def __init__(self, param1=None, param2=None):
    
        super(PycTestCase, self).__init__()
        self.__param1=param1
        self.__param2=param2
        
    def runTest(self):
        #your code here
        pass

```   

You can access the loaded lib method with : 

```Python
    self.c_{c object name}

```

You can access the ffi instance to declare some C variables or other stuff : 

```Python
    self.new(...)
    self.addressof(...)
```
  
### append test

Append to tester previously builded test
   
```C     
    myTester.appendTest(MyTest(param1, param2))
```

## Run test
   
```C     
    myTester.run()
```

## Output file

The report is a yaml file with:
* Report date
* Test duration
* Tests results
* Success, failure, error counters

You can change the filename on *run* call : 

```C     
    myTester.run("my_nice_report.yml")
```

## Convert report format

Report files can be converted to usual report format like JUnit

Call converter script using : 

```
    python PycConverter.py -i report1.yml report2.yml .. reportn.yml -o report.xml"
```

where : 
* -i file1 file2 .. file3 : the input file list
* -o file : the JUnit output file