import collections
import re
import string

from nltk.corpus import stopwords


def remove_punctuations(s):
    """
    Remove punctuations characters
    :param s:
    :return:
    """
    return s.translate(str.maketrans("", "", string.punctuation))


def remove_extra_spaces(s):
    """
    Remove unnecessary spaces
    :param s:
    :return:
    """
    return " ".join(s.split())


def remove_stopwords(tokens):
    """
    Remove english stopwords
    :param tokens:
    :return:
    """
    stops = set(stopwords.words("english"))
    return [word for word in tokens if word not in stops]


def retain_alpha_nums(s):
    """
    Remove all non alpha-numeric characters
    :param s:
    :return:
    """
    return re.sub(r'[^a-zA-Z0-9]', ' ', s)


# bag of words
def bow(tokens):
    """
    Make bag of words table
    :param tokens:
    :return:
    """
    return dict(collections.Counter(re.findall(r'\w+', " ".join(tokens))))


# TODO: Challenge only
def is_person(value):
    m = re.search(r"^([A-Z]\.\s*)+(\w+\'*)+", value, re.IGNORECASE)
    return bool(m)