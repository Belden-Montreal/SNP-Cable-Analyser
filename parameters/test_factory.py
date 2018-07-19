from unittest import TestCase
from unittest.mock import MagicMock, patch

from parameters.factory import ParameterFactory
from parameters.type import ParameterType

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

    @patch('parameters.fext.FEXT')
    @patch('parameters.psfext.PSFEXT')
    def testDependentParameterBefore(self, mock_psfext, mock_fext):
        # set up mocked objects
        mock_fext_obj = MagicMock()
        mock_fext.return_value = mock_fext_obj
        mock_psfext_obj = MagicMock()

        # call the tested method
        self._factory.getParameter(ParameterType.PSFEXT)

        # make sure the FEXT was computed
        mock_fext.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices,
            forward=True,
            reverse=True
        )

        # make sure the PSFEXT was computed
        mock_psfext.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices,
            mock_fext_obj
        )

    @patch('parameters.next.NEXT')
    def testNoRecompute(self, mock_next):
        # set up mocked objects
        mock_next_obj = MagicMock()
        mock_next.return_value = mock_next_obj

        # call the tested method
        self._factory.getParameter(ParameterType.NEXT)

        # make sure the parameter was created
        mock_next.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices,
            mains=True,
            remotes=True,
            order=True
        )
        mock_next.reset_mock()

        # call it again
        self._factory.getParameter(ParameterType.NEXT)

        # make sure the parameter wasn't created another time
        mock_next.assert_not_called()

    @patch('parameters.next.NEXT')
    @patch('parameters.psnext.PSNEXT')
    def testOnlyRequestedInParameter(self, mock_psnext, mock_next):
        # set up mocked objects
        mock_next_obj = MagicMock()
        mock_next.return_value = mock_next_obj
        mock_psnext_obj = MagicMock()

        # call the tested method
        self._parameters[ParameterType.PSNEXT] = self._factory.getParameter(ParameterType.PSNEXT)

        # make sure the NEXT was computed
        mock_next.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices,
            mains=True,
            remotes=True,
            order=True
        )

        # make sure the PSNEXT was computed
        mock_psnext.assert_called_once_with(
            self._config,
            self._freq,
            self._matrices,
            mock_next_obj
        )

        # NEXT shouldn't be in parameters
        self.assertEqual(len(self._parameters), 1)
        self.assertEqual(ParameterType.PSNEXT in self._parameters.keys(), True)
