from json import dump, load

class JSONConfiguration(object):
    def save(self, path):
        with path.open(mode='w+') as f:
            dump(self.toJSON(), f, sort_keys=True, indent=4, separators=(',', ': '))

    @classmethod
    def load(cls, path):
        # create default configuration the path doesn't exist
        if not path.exists():
            return cls()

        # read the configuration if the file exists
        with path.open(mode='r+') as f:
            return cls.fromJSON(load(f))

    def toJSON(self):
        raise NotImplementedError

    @staticmethod
    def fromJSON(json):
        raise NotImplementedError
