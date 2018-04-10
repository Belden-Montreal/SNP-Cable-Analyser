from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = r'C:\Users\LXF09011\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\LXF09011\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'
additional_mods = ['numpy.core._methods', 'numpy.lib.format', 'matplotlib', "tkinter", "scipy.spatial.ckdtree", "visa", "pyvisa"]


setup(name = "Belden SNP Analyzer" ,
      version = "0.1" ,
      description = "" ,
      
      options = {'build_exe': {"packages":['pkg_resources._vendor', "skrf", "tkinter","numpy", "scipy", "matplotlib", "visa", "pyvisa"],
                               'includes': additional_mods,
                               'include_files': ['favicon.ico', 'C:/Users/LXF09011/AppData/Local/Programs/Python/Python36-32/DLLs/tcl86t.dll', 'C:/Users/LXF09011/AppData/Local/Programs/Python/Python36-32/DLLs/tk86t.dll']}},
      executables = [Executable("GuiMain.py",targetName="Belden SNP Analyzer.exe",  icon="favicon.ico")])

