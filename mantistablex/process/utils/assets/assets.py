import os
import app.settings
from mantistablex.process.utils.singleton import Singleton


class Assets(metaclass=Singleton):
    def __init__(self):
        self.__list_cache = {}

    def get_asset(self, path):
        """
        Get asset raw content
        :param path:
        :return string:
        """
        p = os.path.join(app.settings.MANTIS_RES_DIR, path)
        with open(p, 'r') as asset:
            data = asset.read()

        return data

    def load_list(self, path):
        """
        Load an asset as 1D list
        :param path:
        :return:
        """
        if path not in self.__list_cache.keys():
            currency = "".join(self.get_asset(path).split('\r')).split('\n')
            self.__list_cache[path] = currency

        return self.__list_cache[path]

    def list_files(self, path):
        """
        List assets directory files
        :param path:
        :return list:
        """
        p = os.path.join(app.settings.MANTIS_RES_DIR, path)
        return [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
