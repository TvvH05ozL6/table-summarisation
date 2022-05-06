import re

from mantistablex.process.utils.assets.assets import Assets
from mantistablex.process.utils.singleton import Singleton


class Converter(metaclass=Singleton):
    def __init__(self):
        self.conversions = self.__converter()

    # TODO: For now this method is unused
    def get_type(self, num, data):
        """
        It tests lots of combinations of number representations to find
        which is used for the 'num' variable
        :param num:
        :param data:
        :return:
        """
        mod_number = num

        if num.find(',') >= 0:
            if num.find('.') >= 0:
                # Number with points and a comma for the decimal value (e.g. 123.456.789,0123)
                struct_number = re.findall(r'[.,]', num)
                if len(struct_number):
                    for i in range(0, len(struct_number) - 1):
                        mod_number = mod_number.replace(struct_number[i], '')

                    mod_number = mod_number.replace(struct_number[len(struct_number) - 1], '.')
            elif len(re.findall(r',', num)) > 1:
                # Number without points and with a comma for the decimal value (e.g. 33,2)
                mod_number = mod_number.replace(',', '')
            else:
                # Number with commas but without a decimal value (e.g. 123,456,789)
                mod_number2 = mod_number.split(',')
                if re.search(r'[0-9]{3}', mod_number2[1]) is not None:
                    mod_number = mod_number.replace(',', '')
                else:
                    mod_number = mod_number.replace(',', '.')

        elif num.find('.') >= 0:
            if len(re.findall(r'\.', num)) > 1:
                # Number with points but without a decimal value (e.g. 123.456.678)
                mod_number = mod_number.replace('.', '')

        # ------

        for conv in self.conversions:
            # It matches the name
            if data == conv[2]:
                # [type, (modNumber * converterMul) + converterSum, defaultName]
                return [conv[1], (mod_number * conv[3]) + conv[4], conv[0]]

            # It iterates through the abbreviations array
            for abbr in conv[5]:
                if data == abbr:
                    # [type, (modNumber * converterMul) + converterSum, defaultName]
                    return [conv[1], (mod_number * conv[3]) + conv[4], conv[0]]

        return None

    def get_units_list(self):
        units = []
        for k in range(0, len(self.conversions)):
            for j in range(0, len(self.conversions[k][5])):
                units.append(self.conversions[k][5][j].lower())

        return units

    def __converter(self):
        # Maps from units of measurement to the relative quantity        
        conversion = [
            Assets().get_asset("units/Area.txt"),
            Assets().get_asset('units/Currency.txt'),
            Assets().get_asset('units/Density.txt'),
            Assets().get_asset('units/ElectricCurrent.txt'),
            Assets().get_asset('units/Energy.txt'),
            Assets().get_asset('units/Flowrate.txt'),
            Assets().get_asset('units/Force.txt'),
            Assets().get_asset('units/Frequency.txt'),
            Assets().get_asset('units/FuelEfficiency.txt'),
            Assets().get_asset('units/InformationUnit.txt'),
            Assets().get_asset('units/Length.txt'),
            Assets().get_asset('units/LinearMassDensity.txt'),
            Assets().get_asset('units/Mass.txt'),
            Assets().get_asset('units/Numbers.txt'),
            Assets().get_asset('units/PopulationDensity.txt'),
            Assets().get_asset('units/Power.txt'),
            Assets().get_asset('units/Pressure.txt'),
            Assets().get_asset('units/Speed.txt'),
            Assets().get_asset('units/Temperature.txt'),
            Assets().get_asset('units/Time.txt'),
            Assets().get_asset('units/Torque.txt'),
            Assets().get_asset('units/Voltage.txt'),
            Assets().get_asset('units/Volume.txt'),
        ]

        conversions = []
        for element in conversion:
            lines = re.compile(r'\r\n|\n').split(element)
            first_line_elem = lines[0].split('|')

            # It removes the double quotes that surround the string
            element_name = first_line_elem[1][1:-1]

            for line in lines:
                # It parses the string and return an object
                conversions.append(self.__convert_obj(line, element_name))

        return conversions

    def __convert_obj(self, ln, nm):
        fields = ln.split('|')

        # Depending on the format type there are two different way to have the name
        if len(fields) < 4:
            # It removes the double quotes that surround the string
            default_name = fields[1][1:-1]
        else:
            default_name = nm

        field_type = fields[0][1:-1]
        field_name = fields[1][1:-1]

        abbrs = fields[2].split(',')
        for i in range(0, len(abbrs)):
            abbrs[i] = abbrs[i][1:-1]

        converter_mul = 1.0
        if len(fields) >= 4:
            if fields[3].find('/') >= 0:
                # If there is a slash it is a fraction
                numb_tmp = fields[3][1:-1].split("/")
                converter_mul = float(numb_tmp[0]) / float(numb_tmp[1])
            else:
                converter_mul = float(fields[3][1:-1])

        converter_sum = 0
        if len(fields) == 5:
            if fields[4].find('/') >= 0:
                numb_tmp = fields[4][1:-1].split("/")
                converter_sum = float(numb_tmp[0]) / float(numb_tmp[1])
            else:
                converter_sum = float(fields[4][1:-1])

        return default_name, field_type, field_name, converter_mul, converter_sum, abbrs
