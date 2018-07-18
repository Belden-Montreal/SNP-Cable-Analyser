from unittest import TestCase
from unittest.mock import MagicMock, patch

class TestSample(object):
    def setUp(self):
        self._params = set()
        self._snp = "mock.snp"

    def createSample(self):
        raise NotImplementedError

    def getNumberOfPorts(self):
        raise NotImplementedError

    def getExpectedComputedParameters(self):
        raise NotImplementedError

    def getShouldntRunParameters(self):
        raise NotImplementedError

    @patch('sample.sample.Sample.loadSNP')
    @patch('sample.sample.Sample.getFactory')
    def testParameterBuilding(self, mock_getfactory, mock_loadsnp):
        if type(self) == TestSample:
            return

        # mock the network
        (mock_network, mock_date) = (MagicMock(), MagicMock())
        mock_loadsnp.return_value = (mock_network, mock_date)
        mock_network.se2gmm = MagicMock()
        mock_network.number_of_ports = self.getNumberOfPorts()

        # mock the factory
        def getParameter(value):
            return value
        mock_factory = MagicMock()
        mock_factory.getParameter = MagicMock(side_effect=getParameter)
        mock_getfactory.return_value = mock_factory

        # create the sample
        sample = self.createSample()

        # make sure the expected parameters were computed
        for expected in self.getExpectedComputedParameters():
            mock_factory.getParameter.assert_any_call(expected)

        # make sure some parameters we're not overriden
        for expected in self.getShouldntRunParameters():
            try:
                mock_factory.getParameter.assert_any_call(expected)
            except AssertionError:
                continue
            error = AssertionError("Parameter '{}' shouldn't be recomputed".format(expected))
            raise error
