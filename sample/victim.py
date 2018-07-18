from sample.alien import AlienSample

class VictimSample(AlienSample):
    def __init__(self, snp, samples, config=None):
        self._samples = samples

        # make sure all samples are all remote or main
        remotes = set(d.isRemote() for d in self._samples)
        if len(remotes) != 1:
            error = ValueError("Remote mismatch between disturber samples")
            raise error
        remote = next(iter(remotes))

        super(VictimSample, self).__init__(snp, remote=remote, config=config)

    def getDefaultConfiguration(self):
        # make sure all configuration are the same
        ports = [s.getConfig().getPorts() for s in self._samples]
        if ports[1:] != ports[1:]:
            error = ValueError("Configuration mismatch between disturber samples")
            raise error
        config = next(iter([s.getConfig() for s in self._samples]))

        return config

    def getDefaultParameters(self):
        if self._remote:
            parameters = [s.getParameter("AFEXT") for s in self._samples]
            return {"AFEXTD": parameters}
        else:
            parameters = [s.getParameter("ANEXT") for s in self._samples]
            return {"ANEXTD": parameters}

    def getAvailableParameters(self):
        if self._remote:
            return {"AFEXTD", "PSAFEXT", "PSAACRF"}
        else:
            return {"ANEXTD", "PSANEXT", "PSAACRN"}

    def setAXEXTD(self, axextd):
        # TODO: what is this?
        self._axextd = axextd
        self._parameters["PS"+self._param].recalculate(self._axextd)
        if self._param == "ANEXT":
            name = "N"
        else:
            name = "F"
        self._parameters["PSAACR"+name].recalculate(self._parameters["PS"+self._param])
