import os
import yaml

class Config:
    """
    Config
    ------
    Base configuration class for
    a browser using pySteer

    set the config file path using
    the method setConfig or
    the env variable $PYSTEER_CONFIG


    soon: more format options
    and a base class
    """
    _CONFIG_FILE=""

    @classmethod
    def setFile(cls, filePath):
        """
        """
        cls._CONFIG_FILE=filePath

    @classmethod
    def registerDrivers(cls, **kwargs):
        """
        """
        cls._drivers=kwargs

    def __init__(self):
        """
        """
        if not self._CONFIG_FILE:
            config=os.environ.get("PYSTEER_CONFIG")
            if not config:
                raise Exception("[-] No config to load")
        self.file=self._CONFIG_FILE
        self.load()
        self.test()

    def load(self):
        """
        soon: this guy should
        be smart to choose from
        different formats
        """
        fd=open(self.file, "r")
        cfg=yaml.load(fd)
        fd.close()
        for key,values in cfg.items():
            setattr(self, key, values)

    def test(self):
        """
        """
        if self.driver["name"] not in self._drivers:
            raise Exception("[-] Unkwon driver")

    def getDriver(self, **kwargs):
        """
        """
        return self._drivers[self.driver["name"]](**kwargs)
