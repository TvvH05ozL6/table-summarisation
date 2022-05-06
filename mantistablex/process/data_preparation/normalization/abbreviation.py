from mantistablex.process.utils.assets.assets import Assets
from mantistablex.process.utils.singleton import Singleton


class Abbreviator(metaclass=Singleton):
    def __init__(self):
        self.collection = Assets().load_list('units/Abbreviation.txt')

    def get_abbr(self, word):
        """
        Taken a word, if it is an abbreviation it returns the meaning
        :param word:
        :return abbreviation if found or None:
        """
        assert (self.collection is not None)

        for conv in self.collection:
            ln = conv.split("*")
            if word == ln[0]:
                return ln[1]

        return None
