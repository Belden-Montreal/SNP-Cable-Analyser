from unittest import TestCase
from unittest.mock import MagicMock, patch

from parameters.parameter_factory import ParameterFactory

class TestParameterFactory(TestCase):
    def setUp(self):
        self._config     = MagicMock()
        self._freq       = MagicMock()
        self._matrices   = MagicMock()
        self._parameters = dict()
        self._factory = ParameterFactory(
            self._config,
            self._freq,
            self._matrices,
            self._parameters
        )

    @patch('parameters.parameter_factory.FEXT')
    @patch('parameters.parameter_factory.PSFEXT')
    def testDependentParameterBefore(self, mock_psfext, mock_fext):
        # set up mocked objects
        mock_fext_obj = MagicMock()
        mock_fext.return_value = mock_fext_obj
        mock_psfext_obj = MagicMock()

        # call the tested method
        self._factory.getParameter("PSFEXT")

        # make sure the FEXT was computed
        mock_fext.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices
        )

        # make sure the PSFEXT was computed
        mock_psfext.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices,
            mock_fext_obj
        )

    @patch('parameters.parameter_factory.NEXT')
    def testNoRecompute(self, mock_next):
        # set up mocked objects
        mock_next_obj = MagicMock()
        mock_next.return_value = mock_next_obj

        # call the tested method
        self._factory.getParameter("NEXT")

        # make sure the parameter was created
        mock_next.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices
        )
        mock_next.reset_mock()

        # call it again
        self._factory.getParameter("NEXT")

        # make sure the parameter wasn't created another time
        mock_next.assert_not_called()
