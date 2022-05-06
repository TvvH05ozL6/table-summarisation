from math import floor
import re


def decade_counter(list_of_dates):
    decades = dict()
    for el in list_of_dates:
        de = floor(el.year / 10) * 10
        if (de in decades.keys()):
            decades[de] = decades[de] + 1
        else:
            decades.setdefault(de, 1)
    return decades

def word_counter(word_list):
    words = dict()
    for w in word_list:
        if w in words:
            words[w] += 1
        else:
            words[w] = 1
    return words

def get_name_from_entity(entity):
    name = ""
    entity = entity[4:]
    if entity[0].isupper(): # dbo:Mountain or dbr:Mount_Everest
        name = entity.lower().replace('_', '')
    elif entity.islower(): # dbo:elevation
        name = entity
    else: # dbo:mountainRange
        entity = entity[0].upper() + entity[1:]
        words = re.findall('[a-z]|[A-Z][^A-Z]*', entity)  # Split by upper case letter
        for w in words:
            name = name + " " + w.lower()
    return name

def find_reference(i, j, data):
    for sentence in data:
        print(sentence)
        print(j)
        if float(sentence[int(i)].replace(',', '')) == j:
            return sentence[int(subject_col)]