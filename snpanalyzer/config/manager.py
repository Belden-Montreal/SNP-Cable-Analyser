from snpanalyzer.config.vna import VNAConfiguration

from json import dump, load
from pathlib import Path
from appdirs import user_data_dir
from singleton_decorator import singleton

@singleton
class ConfigurationManager(object):
    def __init__(self):
        self.__data = Path(user_data_dir("snpanalyzer"))
        self.__data.mkdir(parents=True, exist_ok=True)
        self.load()

    def getVNAConfiguration(self):
        return self.__vna

    def save(self):
        self.__vna.save(self.__data.joinpath("vna.json"))

    def load(self):
        self.__vna = VNAConfiguration.load(self.__data.joinpath("vna.json"))

