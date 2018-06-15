from parameters.anext import ANEXT

class AFEXT(ANEXT):
    """
        AFEXT is calculated by taking both the FEXT and the Insertion Loss of the disturbed hardware
        For AFEXT measurements to be valid, the measurements must be done on the opposite side :

        measurement (disturbed) []------            --------//[]
                                        |           |
                                         -----------
                                         -----------
                                        |           |
                               []//------            --------[] measurement (disturber) 
    """

    def __init__(self, ports, freq, matrices, fext, il):
        super(AFEXT, self).__init__(ports, freq, matrices, fext, il)
