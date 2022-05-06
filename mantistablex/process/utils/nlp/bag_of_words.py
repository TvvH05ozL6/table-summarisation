import urllib.parse

import nltk
from nltk.corpus import stopwords
from pattern.en import singularize, pluralize

from mantistable.process.data_preparation.normalization.transformer import transformer
from mantistablex.process.utils.nlp import utils


def get_singular(word):
    return singularize(word)


def get_plural(word):
    return pluralize(word)


def bow_text(text):
    """
    It returns an array of string terms without terms with length == 1
    :param text:
    :return:
    """
    tokens = nltk.word_tokenize(text)
    return list(filter(lambda x: len(x) > 1, tokens))


def bow_set_text(tokens):
    return utils.bow(tokens)


def get_name_from_entity(entity):
    def decode_uri_component(uri):
        return urllib.parse.unquote(uri)

    entity = decode_uri_component(entity)
    name = " ".join(entity[28:].split("_")).lower()

    return transformer(name)[0]


def get_row_context(header, rows, current_col_name):
    context = ''
    for col_name in header:
        if col_name != current_col_name:
            context += rows[col_name]["value"] + ' '

    context = context.strip()
    context = bow_set_text(bow_text(context))
    return context


def get_header_context_from_header_table(header):
    return bow_set_text(header)


def get_bow_set(cell, entity, abstract):
    bow_set_cell = bow_set_text(bow_text(cell))
    bow_set_entity = bow_set_text(bow_text(get_name_from_entity(entity)))
    bow_set_abstract = bow_set_text(bow_text(abstract.lower()))

    return bow_set_cell, bow_set_entity, bow_set_abstract


def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    return [
        w
        for w in words
        if w not in stop_words
    ]

def get_row_bow_context(row_context):
    clean_rows = []
    for row in row_context:
        if row.startswith('http'):
            if "http://dbpedia.org/resource/" in row:
                clean_rows.append(row[28:].replace('_', ' ').lower())    
        else:
            clean_rows.append(row)
    return bow_set_text(" ".join(clean_rows).split(" "))       
