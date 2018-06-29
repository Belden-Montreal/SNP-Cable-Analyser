import unittest
import numpy as np

from unittest.mock import MagicMock, patch, call
from parameters.plot import ParameterPlot

class DummyParameter(object):
    def getName(self):
        return "Dummy Parameter"

    def getPorts(self):
        return {0: ('Port 1', False), 1: ('Port 2', False), 2: ('Port 3', False), 3: ('Port 4', False)}

    def getNumPorts(self):
        return len(self.getPorts())

    def getParameter(self):
        return [
            [ 1,  2,  3,  4],
            [ 5,  6,  7,  8],
            [ 9, 10, 11, 12],
            [13, 14, 15, 16],
        ]

    def getFrequencies(self):
        return [100, 200, 300, 400]

class TestParameterPlot(unittest.TestCase):
    def setUp(self):
        self._parameter = DummyParameter()
        self._plot = ParameterPlot(self._parameter, selection=[0, 1])
    
    def testResetSelection(self):
        self._plot.drawFigure = MagicMock()
        self._plot.resetSelection()
        self._plot.drawFigure.assert_called_with()
        self.assertEqual(len(self._plot.getSelection()), 0)

    def testAddSelectionNew(self):
        self._plot.drawFigure = MagicMock()
        self._plot.addSelection(2)
        self._plot.drawFigure.assert_called_with()
        self.assertEqual(len(self._plot.getSelection()), 3)

    def testAddSelectionExising(self):
        self._plot.drawFigure = MagicMock()
        self._plot.addSelection(1)
        self._plot.drawFigure.assert_called_with()
        self.assertEqual(len(self._plot.getSelection()), 2)

    def testRemoveSelectionPresent(self):
        self._plot.drawFigure = MagicMock()
        self._plot.removeSelection(1)
        self._plot.drawFigure.assert_called_with()
        self.assertEqual(len(self._plot.getSelection()), 1)

    def testRemoveSelectionNotPresent(self):
        self._plot.drawFigure = MagicMock()
        self._plot.removeSelection(2)
        self._plot.drawFigure.assert_called_with()
        self.assertEqual(len(self._plot.getSelection()), 2)

    def testGetFigureAndDraw(self):
        self._plot.drawFigure = MagicMock()
        self._plot.getFigure()
        self._plot.drawFigure.assert_called_with()

    def testGetFigureAndDontDraw(self):
        with patch.object(self._plot, "_figure", "something not None"):
            self._plot.drawFigure = MagicMock()
            self.assertNotEqual(self._plot.getFigure(), None)
            self._plot.drawFigure.assert_not_called()

    def testDrawFigureNoSelection(self):
        self._plot.resetSelection()

        with patch("parameters.plot.plt") as mockedplt:
            mockedplt.figure = MagicMock(return_value=self)
            mockedplt.cm = MagicMock()
            mockedplt.cm.rainbow = MagicMock(return_value=[10,20,30,40])
            mockedplt.semilogx = MagicMock()

            self._plot.drawFigure()

            mockedplt.figure.assert_called_with(dpi=80, figsize=(18.75, 6.25))
            arg = mockedplt.cm.rainbow.call_args[0][0]
            np.testing.assert_array_almost_equal(arg, np.array([0, 0.25, 0.5, 0.75, 1]))
            mockedplt.semilogx.assert_has_calls([
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[0],
                    label=self._parameter.getPorts()[0][0], c=10
                ),
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[1],
                    label=self._parameter.getPorts()[1][0], c=20
                ),
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[2],
                    label=self._parameter.getPorts()[2][0], c=30
                ),
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[3],
                    label=self._parameter.getPorts()[3][0], c=40
                ),
            ], any_order=True)
 
    def testDrawFigureWithSelection(self):
        with patch("parameters.plot.plt") as mockedplt:
            mockedplt.figure = MagicMock(return_value=self)
            mockedplt.cm = MagicMock()
            mockedplt.cm.rainbow = MagicMock(return_value=[10,20,30,40])
            mockedplt.semilogx = MagicMock()

            self._plot.drawFigure()

            mockedplt.figure.assert_called_with(dpi=80, figsize=(18.75, 6.25))
            arg = mockedplt.cm.rainbow.call_args[0][0]
            np.testing.assert_array_almost_equal(arg, np.array([0, 0.25, 0.5, 0.75, 1]))
            mockedplt.semilogx.assert_has_calls([
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[0],
                    label=self._parameter.getPorts()[0][0], c=10
                ),
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[1],
                    label=self._parameter.getPorts()[1][0], c=20
                ),
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[2],
                    label=self._parameter.getPorts()[2][0], c='grey'
                ),
                call(
                    self._parameter.getFrequencies(),
                    self._parameter.getParameter()[3],
                    label=self._parameter.getPorts()[3][0], c='grey'
                ),
            ], any_order=True)

if __name__ == '__main__':
    unittest.main()
