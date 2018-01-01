from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\test\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\test\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'


setup(
    name = "Variation Calculator" ,
    version = "1.0" ,
    options= { 'build_exe':{"packages": ["numpy"],
			"include_files": ["tcl86t.dll", "tk86t.dll",]}},
    description = "abc" ,
    executables = [Executable(script="var.py", base = "Win32GUI")]  ,
)
