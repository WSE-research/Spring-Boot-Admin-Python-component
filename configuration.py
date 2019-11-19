import configparser
import os.path
import logging


class Configuration:
    """
        parse and validates information provided by 
    """

    demandedConfigurationKeys = []
    configfile = ""

    def __init__(self, configfile, demandedConfigurationKeys=[]):
        self.configfile = configfile
        if os.path.exists(self.configfile):
            self.demandedConfigurationKeys = demandedConfigurationKeys
            self.integrateDataFromConfigfile()
        else:
            logging.error("config file '%s' not found" % (configfile))
            raise Exception(
                "no configuration present in file '%s'" % (configfile))

    def integrateDataFromConfigfile(self) -> None:
        config = configparser.ConfigParser()
        config.read(self.configfile)
        configvalues = dict(config.items("ServiceConfiguration"))

        # set all configuration values as object properties
        for key in configvalues:
            setattr(self, key, configvalues[key])
            if configvalues[key]:
                try:
                    self.demandedConfigurationKeys.remove(key)
                except:
                    pass
            logging.debug("configuration: %s=%s" % (key, configvalues[key]))

        # test if all mandatory configuration values are present
        if(len(self.demandedConfigurationKeys) != 0):
            raise Exception("The following values are missing in config file '%s': %s" % (
                self.configfile, self.demandedConfigurationKeys))
