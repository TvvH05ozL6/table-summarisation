from mantistablex.process.utils.data_type import DataTypeEnum
from mantistablex.process.utils.validator import Validator


def check_type(value):
    """
    Tag value with corresponding data_type
    :param value: 
    :return DataTypeEnum:
    """

    validator = Validator()
    type_map = [
        # type, predicate
        (DataTypeEnum.EMPTY, validator.is_empty),
        (DataTypeEnum.NUMERIC, validator.is_numeric),
        (DataTypeEnum.BOOLEAN, validator.is_boolean),
        (DataTypeEnum.DATE, validator.is_date),
        (DataTypeEnum.GEOCOORD, validator.is_geocoords),
        (DataTypeEnum.DESCRIPTION, validator.is_description),
        (DataTypeEnum.NOANNOTATION, validator.is_no_annotation),
        (DataTypeEnum.ID, validator.is_id),
        (DataTypeEnum.URL, validator.is_url),
        (DataTypeEnum.EMAIL, validator.is_email),
        (DataTypeEnum.ADDRESS, validator.is_address),
        (DataTypeEnum.HEXCOLOR, validator.is_hexcolor),
        (DataTypeEnum.IP, validator.is_ip),
        (DataTypeEnum.CREDITCARD, validator.is_creditcard),
        (DataTypeEnum.IMAGE, validator.is_image),
        #(DataTypeEnum.ISBN, validator.is_isbn),
        (DataTypeEnum.ISO8601, validator.is_iso8601),
        (DataTypeEnum.CURRENCY, validator.is_currency),
        (DataTypeEnum.IATA, validator.is_iata),
    ]

    """
    """

    for (data_type, predicate) in type_map:
        if predicate(value):
            return data_type

    return DataTypeEnum.NONE
