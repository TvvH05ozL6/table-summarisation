import re
import socket
from mimetypes import MimeTypes

#import isbnlib
#import dateutil.parser as dateutil

from mantistablex.process.utils.nlp import utils as nlp
from mantistablex.process.data_preparation.normalization.converter import Converter
from mantistablex.process.utils.assets.assets import Assets

class Validator:
    __months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
        "sep", "oct", "nov", "dec"
    ]

    @staticmethod
    def is_empty(s):
        sl = s.lower()
        return len(sl) == 0 or nlp.retain_alpha_nums(sl) == ""

    @staticmethod
    def is_geocoords(s):
        # Geographic coordinates (e.g. 46.1368155, 9.61057690000007)
        reg1 = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
        # Geographic coordinates (e.g. 35°56′51″N 75°45′12″E)
        reg2 = r"^[0-9]+°[0-9]+(′|')[0-9]+(″|''|′′)\s*[N|S](,)*\s*[0-9]+°[0-9]+(′|')[0-9]+(″|''|′′)\s*[W,E]"

        return re.search(reg1, s, flags=re.I | re.M) is not None or re.search(reg2, s, flags=re.I | re.M) is not None

    @staticmethod
    def is_numeric(s):
        def is_unit(s):
            if Validator.is_decimal(s):
                unit_list = Converter().get_units_list()

                for unit in unit_list:
                    if unit in s:
                        return True

            return False

        return Validator.is_decimal(s) or is_unit(s.lower())

    @staticmethod
    def is_decimal(s):
        # not a number is not a decimal
        if s.lower() == "nan":
            return False

        # check "." and ","
        if s.find(".") >= 0 and s.find(",") >= 0:
            return False
        else:
            s = s.replace(",", ".")

        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_address(s):
        reg1 = r"\d+\s+\w+\s+(?:st(?:\.|reet)?|ave(?:nue)?|lane|dr(?:\.|ive)?)"
        reg2 = r"^[\d]+[A-z\s,]+[\d]"

        # Original code is possibly wrong:
        # oldValue.length is out of range for charAt since the last index is at oldValue.length-1
        # !isNaN(parseInt(oldValue.charAt(oldValue.length), 10)))
        try:
            int(s[len(s) - 1])
            last_char_is_int = True
        except ValueError:
            last_char_is_int = False

        return re.search(reg1, s.lower()) is not None or (re.search(reg2, s) is not None and last_char_is_int)

    @staticmethod
    def is_hexcolor(s):
        return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', s) is not None

    @staticmethod
    def is_url(s):
        # NOTE: regex does not match urls without http header
        reg = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        return re.search(reg, s.lower(), re.M) is not None

    @staticmethod
    def is_image(s):
        mime = MimeTypes()
        mime_type = mime.guess_type(s)[0]

        if mime_type is None:
            return False

        return "image" in mime_type.split("/")[0]

    @staticmethod
    def is_creditcard(s):
        # luhn algorithm to validate credit cards numbers
        def luhn(number):
            digits = [int(c) for c in number if c.isdigit()]
            if len(digits) <= 0:
                return False

            checksum = digits.pop()
            digits.reverse()
            doubled = [2 * d for d in digits[0::2]]
            total = sum(d - 9 if d > 9 else d for d in doubled) + sum(digits[1::2])
            return (total * 9) % 10 == checksum

        cc = re.sub(r"\s", "", s)
        return cc.isdigit() and luhn(cc.lower())

    @staticmethod
    def is_email(s):
        reg = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        return re.search(reg, s.lower()) is not None

    @staticmethod
    def is_ip(s):
        def is_ipv(family, addr):
            try:
                socket.inet_pton(family, addr)
            except socket.error:
                return False

            return True

        return is_ipv(socket.AF_INET, s.lower()) or is_ipv(socket.AF_INET6, s.lower())

    #@staticmethod
    #def is_isbn(s):
    #    return isbnlib.is_isbn10(s) or isbnlib.is_isbn13(s)

    @staticmethod
    def is_iso8601(s):
        reg = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"
        return re.search(reg, s) is not None

    @staticmethod
    def is_boolean(s):
        reg = "^(?:y(?:es)?|1)$|^(?:n(?:o)?|0)$"
        return re.search(reg, s.lower(), flags=re.I) or s.lower() in ["true", "false"]

    @staticmethod
    def is_date(s):
        def regex_test(s):
            date_match = re.search(r'[0-9]+-[0-9]+-[0-9]+', s)
            return date_match is not None and (len(s) - len(date_match[0])) <= 19

        def month_test(s):
            words = s.lower().split(' ')
            for word in words:
                return word in Validator.__months
        ''' 
        def date_format_test(s):
            try:
                dateutil.parse(s)
                return True
            except (ValueError, OverflowError):
                return False
'''
        '''regex_test(s) or'''
        return month_test(s) or (regex_test(s) and date_format_test(s) and not Validator.is_decimal(s))

    @staticmethod
    def is_description(s):
        return len(s) > 80

    @staticmethod
    def is_id(s):
        if len(s) < 15:
            # Remove everything which is not a word or a single whitespace
            valuex = re.sub(r"[^\w\s]", ' ', s)
            valuex = nlp.remove_extra_spaces(valuex)
            valuex = valuex.strip()

            # They contain the number of letters, digits and words in the string
            countletters = len(re.sub(r"[^A-Z]", '', valuex, flags=re.I))
            countdigits = len(re.sub(r"[^0-9]", '', valuex, flags=re.I))
            countws = len(re.sub(r"[^\s]", '', valuex, flags=re.I))

            # If it is a single word composed of both digits and letters
            if countws == 0:
                # If it is composed of both digits and letters
                if countdigits > 0 and countletters > 0 and len(valuex) < 5:
                    return True

                # If it has only uppercase characters
                if valuex == valuex.upper():
                    # If it is a small word
                    if countletters > 0 and len(valuex) < 6:
                        return True

                    # If it is a small word with no digits
                    if len(valuex) < 7 and countdigits == 0 and countletters > 0:
                        return True

            # If it has 2 words and every character is uppercase
            if countws == 1 and valuex == valuex.upper() and countdigits > 0 and s.find(" ") == -1:  # add countdigits > 0:
                return True

            ''' If it has more than 2 words, every character is uppercase
                but with length limitations and no spaces
            '''
            return countws >= 1 and valuex == valuex.upper() and len(
                    valuex) < 15 and countdigits > 0 and s.find(" ") == -1  # add countdigits > 0

    @staticmethod
    def is_currency(s):
        if len(s) < 15:
            # Remove everything which is not a word or a single whitespace
            valuex = re.sub(r"[^\w\s]", ' ', s)
            valuex = nlp.remove_extra_spaces(valuex)
            valuex = valuex.strip()

            countws = len(re.sub(r"[^\s]", '', valuex, flags=re.I))

            # If it is a single word composed of both digits and letters
            if countws == 0:
                if valuex in Assets().load_list("currency.txt"):
                    return True

        return False

    @staticmethod
    def is_iata(s):
        words = re.sub(r"[-/&,:;_]", ' ', s.lower())
        if len(s) == 3 or (3 < len(words) < 9):
            words = words.split(" ")

            if len(words) < 3:
                for i in range(0, len(words)):
                    if 2 < len(words[i]) < 5:
                        if words[i].upper() in Assets().load_list("iatacodes.txt"):
                            return True

        return False

    @staticmethod
    def is_no_annotation(s):
        return s.count(",") > 1
