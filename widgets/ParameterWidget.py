from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QListWidgetItem, QPushButton
from widgets.SmartFlowWidget import SmartFlowWidget

from UI import ParameterWidget as PW

from matplotlib.pyplot import cm
import matplotlib.ticker

import numpy as np

class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget():
    def __init__(self, param, sample, graph):
        self.widget  = QtWidgets.QWidget()
        self.paramWidget = PW.Ui_ParameterWidget()
        self.paramWidget.setupUi(self.widget)
        self.paramWidget.paramLabel.setText(param)
        self.param = param
        self.sample = sample
        self.graphicsView = graph
        self.paramWidget.marginListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.MARGIN))
        self.paramWidget.worstListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.VALUE))
        self.setPairsList()
        self.hasPassed = True

        if self.sample.standard is not None:
            #print("PARAM WIDGET PARAM : ", self.sample.worstValue)
            try:
                values = [self.sample.worstValue[param], self.sample.worstMargin[param]]
                if values[0][0] and values[1]:
                    self.worstValue = values[0]
                    self.worstMargin = values[1]
                    if self.worstValue[1] == "Pass" and self.worstMargin[1] == "Pass":
                        self.paramWidget.passLabel.setText("Pass")
                        self.hasPassed = True
                    else:
                        self.paramWidget.passLabel.setText("Fail")
                        self.hasPassed = False
            except:
                self.worstMargin = None
                self.worstValue = None
                self.paramWidget.passLabel.setText("Fail")
                self.hasPassed = False

                #print("NO WORST VALUE",self.sample.worstValue )
        #self.setResults()
        #self.paramWidget.resultsList.itemChanged.connect(self.getPlotLines)

        self.graphicsView.mpl_connect('pick_event', self.onpick)
        self.lined = dict()

    def setPairsList(self):
        try:
            self.paramWidget.marginListWidget.addItems(getattr(self.sample, self.param))
            self.paramWidget.marginListWidget.sortItems()
            self.paramWidget.worstListWidget.addItems(getattr(self.sample, self.param))
            self.paramWidget.worstListWidget.sortItems()
        except Exception as e:
            return

    def pairSelected(self, pair, listIndex):
        if self.sample.standard is not None:
            self.setLabels(listIndex, pair)

    def setLabels(self, listIndex, pair):
        if self.worstMargin and listIndex == valueType.MARGIN: #Worst margin
            self.paramWidget.marginValueLabel.setText(self.worstMargin[0][pair][0].__str__())
            self.paramWidget.marginFreqLabel.setText(self.worstMargin[0][pair][1].__str__())
            self.paramWidget.marginLimitLabel.setText(self.worstMargin[0][pair][2].__str__())
            self.paramWidget.marginLabel.setText(self.worstMargin[0][pair][3].__str__())
        elif self.worstValue: #worst value
            self.paramWidget.worstValueLabel.setText(self.worstValue[0][pair][0].__str__())
            self.paramWidget.worstFreqLabel.setText(self.worstValue[0][pair][1].__str__())
            self.paramWidget.worstLimitLabel.setText(self.worstValue[0][pair][2].__str__())
            self.paramWidget.worstMarginLabel.setText(self.worstValue[0][pair][3].__str__())



    def getPlotLines(self, item):
        line = item.text()
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            self.ignore.remove(line)
        else:
            self.ignore.append(line)
        #self.plotUpdate()

    def plotUpdate(self, sample, activeParameter, ignore = None):
        self.activeParameter = activeParameter
        limit = None
        if sample.standard is not None:
            if self.activeParameter.replace(" ","") in sample.standard.limits:
                if self.activeParameter == "Propagation Delay":
                    limit = sample.standard.limits[self.activeParameter.replace(" ","")].getArray()
                else:
                    limit = sample.standard.limits[self.activeParameter.replace(" ","")].getArray()
                    #print(sample.freq)
        self.plot(self.sample.freq, getattr(self.sample, self.activeParameter.replace(" ", "")), limit = limit , unit = sample.freq_unit)
        

    def plot(self, x=None, param_dict=None, limit = None, unit = "Mhz", avgLimit = None):

        self.graphicsView.figure.clear()
        #ax.set_xlim(300*(10**3), 10**9)
        #self.ax.semilogx(x, self.pitch, '.-', label=label, c=color)
        if x is not None or param_dict is not None:
            ax=self.graphicsView.figure.add_subplot(111)
            #print param_dict.keys()
            color=iter(cm.rainbow(np.linspace(0,1,len(param_dict.keys()))))
            lines = []
            for key in sorted(param_dict.keys()):
                c = next(color)
                #print key

                #a = scipy.signal.decimate(x, 10)
                if len(x) == len(param_dict[key]):
                    lines.append(ax.semilogx(x, param_dict[key], label=key, c = c))
                #print key 

            ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())


            #self.figure.tight_layout()

            ax.grid(which="both")

            ax.set_xlabel('Freq ({})'.format(unit))
            ax.set_ylabel('dB')
            ax.set_title(self.activeParameter)
            if self.activeParameter.replace(" ", "") == "PropagationDelay":
                ax.set_ylabel('nSec')

            if limit is not None:
                lines.append(ax.semilogx(*zip(*limit), linestyle = '--', label="limit", c = c))


            if avgLimit is not None:
                ax.semilogx(*zip(*avgLimit), linestyle = '--', label="average limit", c = c)
            leg =  ax.legend(loc='upper left', ncol = 1 if len(param_dict.keys()) <= 8 else 2 , fancybox=True, shadow=True)

            leg.get_frame().set_alpha(1)
            # we will set up a dict mapping legend line to orig line, and enable
            # picking on the legend line
            #print(zip(leg.get_lines(), lines))
            self.lined = dict()
            self.line_text_dict = dict()

            for legline, legtext, origline in zip(leg.get_lines(), leg.get_texts(), lines):
                #print(legline, origline[0])
                legline.set_picker(5)  # 5 pts tolerance
                legtext.set_picker(6)  # 5 pts tolerance

                self.lined[legline] = origline[0]
                self.lined[legtext] = origline[0]
                self.line_text_dict[legline] = legtext
                self.line_text_dict[legtext] = legline
     
            #self.ax.legend()
        self.graphicsView.draw()
        
    def onpick(self, event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        legline = event.artist
        origline = self.lined[legline]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
        if vis:
            legline.set_alpha(1.0)
            self.line_text_dict[legline].set_alpha(1.0)

        else:
            legline.set_alpha(0.2)
            self.line_text_dict[legline].set_alpha(0.2)
        self.graphicsView.draw()

