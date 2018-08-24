from snpanalyzer.sample.alien import AlienSample
from snpanalyzer.parameters.type import ParameterType
from snpanalyzer.analysis.alien_parameter import AlienParameterAnalysis

class VictimSample(AlienSample):
    def __init__(self, snp, samples, config=None, **kwargs):
        self._samples = samples

        # make sure all samples are all remote or main
        if len(self._samples):
            remotes = set(d.isRemote() for d in self._samples)
            if len(remotes) != 1:
                error = ValueError("Remote mismatch between disturber samples")
                raise error
            kwargs["remote"] = next(iter(remotes))

        super(VictimSample, self).__init__(snp, config=config, **kwargs)

    def createAnalyses(self):
        super(VictimSample, self).createAnalyses()
        if self._remote:
            self._analyses[ParameterType.PSAFEXT] = AlienParameterAnalysis(self._parameters[ParameterType.PSAFEXT])
            self._analyses[ParameterType.PSAACRF] = AlienParameterAnalysis(self._parameters[ParameterType.PSAACRF])
        else:
            self._analyses[ParameterType.PSANEXT] = AlienParameterAnalysis(self._parameters[ParameterType.PSANEXT])
            self._analyses[ParameterType.PSAACRN] = AlienParameterAnalysis(self._parameters[ParameterType.PSAACRN])

    def setStandard(self, standard):
        super(VictimSample, self).setStandard(standard)
        if self._remote:
            if len(standard.limits["AVG"+ParameterType.PSAACRF.name].functions) > 0:
                self._parameters[ParameterType.PSAACRF].setAverageLimit(standard.limits["AVG"+ParameterType.PSAACRF.name])
                self._analyses[ParameterType.PSAACRF].addAverageLimit()
        else:
            if len(standard.limits["AVG"+ParameterType.PSANEXT.name].functions) > 0:
                self._parameters[ParameterType.PSANEXT].setAverageLimit(standard.limits["AVG"+ParameterType.PSANEXT.name])
                self._analyses[ParameterType.PSANEXT].addAverageLimit()

    def getDefaultConfiguration(self):
        # make sure all configuration are the same
        try:
            ports = [s.getConfig().getPorts() for s in self._samples]
            if ports[1:] != ports[1:]:
                error = ValueError("Configuration mismatch between disturber samples")
                raise error
            config = next(iter([s.getConfig() for s in self._samples]))
        except StopIteration:
            config = super(VictimSample, self).getDefaultConfiguration()

        return config

    def getDefaultParameters(self):
        if self._remote:
            parameters = [s.getParameter(ParameterType.AFEXT) for s in self._samples]
            return {ParameterType.AFEXTD: parameters}
        else:
            parameters = [s.getParameter(ParameterType.ANEXT) for s in self._samples]
            return {ParameterType.ANEXTD: parameters}

    def getAvailableParameters(self):
        if self._remote:
            return [ParameterType.IL, ParameterType.PSAFEXT, ParameterType.PSAACRF]
        else:
            return [ParameterType.IL, ParameterType.PSANEXT, ParameterType.PSAACRN] 

    def recalculate(self, disturbers):
        #We keep the insertion loss to not recalculate it
        il = self._parameters[ParameterType.IL]

        if self._remote:
            param = ParameterType.AFEXTD
            parameters = [s.getParameter(ParameterType.AFEXT) for s in disturbers]
        else:
            param = ParameterType.ANEXTD
            parameters = [s.getParameter(ParameterType.ANEXT) for s in disturbers]

        #re-create the parameters
        self._parameters = {ParameterType.IL: il, param: parameters}
        #re-create the factory
        self._factory = self.getFactory()
        for parameter in self.getAvailableParameters():
            if parameter in self._parameters.keys():
                continue
            self._parameters[parameter] = self._factory.getParameter(parameter)
        if self._standard:
            self.setStandard(self._standard)
        self.createAnalyses()

    def resetDisturbers(self):
        self.recalculate(self._samples)

    def setDisturbers(self, samples):
        self._samples = samples
        remotes = set(d.isRemote() for d in self._samples)
        if len(remotes) != 1:
            error = ValueError("Remote mismatch between disturber samples")
            raise error
        remote = next(iter(remotes))
        self._remote = remote
        self.recalculate(self._samples)
