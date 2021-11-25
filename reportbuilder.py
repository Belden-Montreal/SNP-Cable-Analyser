from anytree import AnyNode, RenderTree, Node, search
from dialogs import reportConfig 
import pandas as pd
import numpy as np
class ReportBuilder():

    def __init__(self, samples):

        self.samples = samples
        self.configTree = self.getConfigTree()

    def getConfigTree(self):
        configTree = Node(name="configTree", selected = True)
        for sample in self.samples:
            s = Node(name = sample.name , nodeType = "sample", sampleType = sample.__repr__(), sample = sample, selected = True, parent = configTree)
            
            if s.sampleType == "SNP":
                params = sample.parameters
                for param in params:
                    print(param)
                    p = Node(name = param, nodeType = "parameter", parameter = sample.getParam(param), selected = True, parent = s)
                    series = p.parameter.keys()
                    if sample.standard is not None and param in sample.standard.limits:
                        series.append("Limit")
                    for line in series:
                        l = Node(name = line, nodeType = "series", series = line, selected = True, parent = p)

        
        return configTree

    def displayUI(self):
        gui = reportConfig.ReportConfig(self.configTree)
        gui.displayTree()
        self.configTree = gui.getNewConfig()

    def generateExcel(self):
        samples = search.findall(self.configTree,  filter_=lambda node: node.selected is True, maxlevel=2)
        samples = samples[1:] #Skip root
        for s in samples:


            if s.sampleType == "SNP":
                col = pd.MultiIndex.from_arrays([[],[],[]])  #sub headers  :  Parameter ->Pair ->Real/Imag
                df = pd.DataFrame(columns=col)

                df['','',"Freq"] = s.sample.freq
                params = search.findall(s,  filter_=lambda node: node.selected is True, maxlevel=2)
                params = params[1:] #Skip root
                for p in params:
                    param_name = p.name
                    series = search.findall(p,  filter_=lambda node: node.selected is True, maxlevel=2)
                    series = series[1:] #Skip root
                    for line in series:
                        line_name = line.name  #pair
                        df[param_name, line_name, "Re"] = np.real(s.sample.getParam(param_name, z=True)[line_name])
                        df[param_name, line_name, "Im"] = np.imag(s.sample.getParam(param_name,z=True)[line_name])


        print(df)


