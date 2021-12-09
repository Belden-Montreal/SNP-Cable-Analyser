from anytree import AnyNode, RenderTree, Node, search
from dialogs import reportConfig 
import pandas as pd
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox
from PyQt5.Qt import Qt

class ExcelReportBuilder():

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

            if s.sampleType == "Alien":
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
                    


        
        return configTree

    def displayUI(self):
        gui = reportConfig.ReportConfig(self.configTree, "excel")
        res = gui.dialog.exec_()
        print("REs = ", res)
        #gui.displayTree()
        if res == QtWidgets.QDialog().Accepted:
            self.outputFile , self.configTree = gui.getNewConfig()

    def generateExcel(self):
        writer = pd.ExcelWriter(self.outputFile) 
        samples = search.findall_by_attr(self.configTree, True, name = "selected", maxlevel=2)
        samples = samples[1:] #Skip root
        for s in samples:


            if s.sampleType == "SNP":
                col = pd.MultiIndex.from_arrays([[],[],[]])  #sub headers  :  Parameter ->Pair ->Real/Imag
                df = pd.DataFrame(columns=col, index = s.sample.freq)
                freq_title = f"Freq({s.sample.freq_unit})"
                new_freq=df.index.set_names(freq_title)
                df.index=new_freq
                #df['','', freq_title] = s.sample.freq
                #df.set_index([('', '', freq_title)], inplace=True)
                params = search.findall_by_attr(s, True, name = "selected", maxlevel=2)
                params = params[1:] #Skip root
                for p in params:
                    param_name = p.name
                    series = search.findall_by_attr(p , True, name = "selected", maxlevel=2)
                    series = series[1:] #Skip root
                    for line in series:
                        line_name = line.name  #pair
                        if p.complex:
                            if line_name == "Limit":
                                pass

                            else:
                                df[param_name, line_name, "Re"] = np.real(s.sample.getParam(param_name, z=True)[line_name])
                                df[param_name, line_name, "Im"] = np.imag(s.sample.getParam(param_name,z=True)[line_name])
                        else:
                            if param_name == "Propagation Delay":
                                if line_name == "Limit":
                                    lim = s.sample.standard.limits['PropagationDelay'].getArray()
                                    #df[param_name, line_name, "ns"] = np.NaN
                                    idx, val = zip(*lim)
                                    #for idx, val in lim.items() :  # i in enumerate(idx):
                                    df[param_name, line_name, "ns"] = val
                                else:
                                    df[param_name, line_name, "ns"] = s.sample.getParam(param_name, z=False)[line_name]
                            else:
                                if line_name == "Limit":
                                    try:
                                        lim = s.sample.standard.limits[param_name].getArray()
                                        #df[param_name, line_name, "db"] = np.NaN
                                        idx, val = zip(*lim)
                                        #for idx, val in lim.items() :  # i in enumerate(idx):
                                        #print(idx, val)
                                        df[param_name, line_name, "db"] = val
                                        #df[param_name, line_name, "db"] = val
                                    except Exception as e:
                                        print("FAIL on LIMIT : ", param_name, e)
                                        print(val)
                                else:
                                    df[param_name, line_name, "db"] = s.sample.getParam(param_name, z=False)[line_name]
                try:
                    print("sample name : ", s.sample.name)
                    df.to_excel(writer, sheet_name=s.sample.name, engine='openpyxl')
                    writer.book[s.sample.name].delete_rows(3)
                    writer.save()
                except Exception as e:
                    print(e)

            if s.sampleType == "Alien":

                params = search.findall_by_attr(s, True, name = "selected", maxlevel=2)
                params = params[1:] #Skip root
                for p in params:

                    col = pd.MultiIndex.from_arrays([[],[],[]])  #sub headers  :  Parameter ->Pair ->Real/Imag
                    df = pd.DataFrame(columns=col, index = s.sample.freq)
                    freq_title = f"Freq({s.sample.freq_unit})"
                    new_freq=df.index.set_names(freq_title)
                    df.index=new_freq

                    param_name = p.name
                    series = search.findall_by_attr(p , True, name = "selected", maxlevel=2)
                    series = series[1:] #Skip root
                    for line in series:
                        line_name = line.name  #pair
                        if line_name == "Limit" or line_name == "Avg Limit":
                            try:
                                lim = line.series.getArray()
                                #df[param_name, line_name, "db"] = np.NaN
                                idx, val = zip(*lim)
                                #for idx, val in lim.items() :  # i in enumerate(idx):
                                #print(idx, val)
                                df[param_name, line_name, "db"] = val
                                #df[param_name, line_name, "db"] = val
                            except Exception as e:
                                print("FAIL on LIMIT : ", param_name, e)
                        else:
                            df[param_name, line_name, "db"] = line.series
                    try:
                        print("sample name : ", s.sample.name)
                        df.to_excel(writer, sheet_name=s.sample.name + " - " + param_name)
                    except Exception as e:
                        print(e)



        writer.save()




