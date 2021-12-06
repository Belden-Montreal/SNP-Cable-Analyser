from anytree import AnyNode, RenderTree, Node, search
from dialogs import reportConfig 
import pandas as pd
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox
from PyQt5.Qt import Qt


import os, base64, preppy
from xml.sax.saxutils import escape, unescape
from reportPackages.rlextra.radxml.xmlutils import TagWrapper
from reportPackages.rlextra.radxml.html_cleaner import cleanInline
from reportPackages.rlextra.rml2pdf import rml2pdf
import trml2pdf

import pyRXPU
#required for python 2.7 & >=3.3
from reportPackages.reportlab.lib.utils import getBytesIO, isUnicode, asUnicode, asNative, asBytes, unicodeT


class PDFReportBuilder():

    def __init__(self, samples):

        self.samples = samples
        self.configTree = self.getConfigTree()
        self.outputFile = None

    def getConfigTree(self):
        configTree = Node(name="configTree", selected = True)
        for sample in self.samples:

            s = Node(name = sample.name , nodeType = "sample", sampleType = sample.__repr__(), sample = sample, selected = True, parent = configTree)
            
            if s.sampleType == "SNP":
                params = sample.parameters
                for param in params:
                    print(param)
                
                    p = Node(name = param, nodeType = "parameter", parameter = sample.getParam(param), selected = True, parent = s, hasComplex = sample.hasComplex(param), complex=False)
                    series = list(p.parameter.keys())

                    if sample.standard is not None and sample.standard.limits[param.replace(" ", "")].resultsList is not None:
                        series.insert(0, "Limit")
                    for line in series:
                        l = Node(name = line, nodeType = "series", series = line, selected = True, parent = p)

            '''if s.sampleType == "Alien":
                for name, (parameter, limit, avglimit) in sample.getParameters().items():
                    if len(parameter):
                        p = Node(name = name, nodeType = "parameter", parameter = parameter, selected = True, parent = s, hasComplex = False, complex=False)
                        if limit is not None and limit.resultsList is not None:
                            l = Node(name = "Limit", nodeType = "series", series = limit, selected = True, parent = p) 
                        if avglimit is not None and avglimit.resultsList is not None:
                            l = Node(name = "Avg Limit", nodeType = "series", series = avglimit, selected = True, parent = p) 
                        series = list(p.parameter.keys())
                        for line in series:
                            l = Node(name = line, nodeType = "series", series = p.parameter[line], selected = True, parent = p) 
            '''


        
        return configTree

    def displayUI(self):
        gui = reportConfig.ReportConfig(self.configTree)
        res = gui.dialog.exec_()
        print("REs = ", res)
        #gui.displayTree()
        if res == QtWidgets.QDialog().Accepted:
            self.outputFile , self.configTree = gui.getNewConfig()

    def generatePDF(self):

        class SampleData:
            pass

        samples = search.findall_by_attr(self.configTree, True, name = "selected", maxlevel=2)
        samples = samples[1:] #Skip root

        sample_list = []
        for s in samples:
            class ParamData:
                pass
            if s.sampleType == "SNP":

                freq_title = f"Freq({s.sample.freq_unit})"
                sd = SampleData()
                sd.type = "SNP"
                sd.name = s.sample.name
                sd.freq =  s.sample.freq
                sd.freq_unit = s.sample.freq_unit
                params = search.findall_by_attr(s, True, name = "selected", maxlevel=2)
                params = params[1:] #Skip root
                param_list = []
                for p in params:

                    pd = ParamData()
                    param_name = p.name
                    pd.name = param_name 

                    series = search.findall_by_attr(p , True, name = "selected", maxlevel=2)
                    series = series[1:] #Skip root

                    series_list = []
                    class LineData:
                        pass
                    for line in series:
                        ld = LineData()
                        line_name = line.name  #pair
                        ld.name = line_name
                        if p.complex:
                            if line_name == "Limit":
                                pass

                            else:
                                pass
                        else:
                            if param_name == "Propagation Delay":
                                if line_name == "Limit":
                                    lim = s.sample.standard.limits['PropagationDelay'].getArray()
                                    #df[param_name, line_name, "ns"] = np.NaN
                                    idx, val = zip(*lim)
                                    #for idx, val in lim.items() :  # i in enumerate(idx):
                                    
                                else:
                                    pass
                            else:
                                if line_name == "Limit":
                                    try:
                                        lim = s.sample.standard.limits[param_name].getArray()
                                        #df[param_name, line_name, "db"] = np.NaN
                                        idx, val = zip(*lim)
                                        #for idx, val in lim.items() :  # i in enumerate(idx):
                                        #print(idx, val)
                                        #df[param_name, line_name, "db"] = val
                                    except Exception as e:
                                        print("FAIL on LIMIT : ", param_name, e)
                                        print(val)
                                else:
                                    pass
                        series_list.append(ld)
                    pd.lines = series_list
                    param_list.append(pd)
                sd.params = param_list
                sample_list.append(sd)
                try:
                    print("sample name : ", s.sample.name)
                except Exception as e:
                    print(e)

        template = "graphs_report.prep"
        RML_DIR = "templates"
        DATA_DIR = os.path.join(RML_DIR, "data")
        output = "testOut.pdf"
        templateName = os.path.join(RML_DIR, template)
        template = preppy.getModule(templateName)
        namespace = {
            'samples': sample_list,
            'RML_DIR': RML_DIR,
            'IMG_DIR': 'img'
            }
        rml = template.getOutput(namespace)
        open(os.path.join(DATA_DIR,'latest.rml'), 'w').write(rml)
        #print(rml)
        buf = getBytesIO()
        print(rml2pdf.go(asBytes(rml), outputFileName=output))
        #buf = trml2pdf.parseString(asBytes(rml))








