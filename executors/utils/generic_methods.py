class GenericMethods:

    @staticmethod
    def get_fhir_id_from_headers(headers):
        '''
        Retrieve the Location header and just take the resource id
        '''

        url = ""
        id = None

        if headers[0].status_code == 201:
            for header in headers[0].headers.raw:
                if header[0].decode('utf-8') == 'Location':
                    url = header[1].decode('utf-8')
                    break

            id = url.split("/")[6]

        return id

    @staticmethod
    def translate_gender(gender):
        if gender.upper() == "M":
            return "male"
        elif gender.upper() == "F":
            return "female"
        else:
            return "other"

    @staticmethod
    def translate_gender_based_on_number(gender):
        return {1: 'male', 2: 'female'}.get(gender, 'other')

    @staticmethod
    def convert_string_to_float(value):

        '''
        Auxiliary method to read a decimal number containing a comma and convert it into a float variable
        '''
        if isinstance(value, str):
            if ',' in value:
                try:
                    value = float(value.replace(',', ''))
                    return value
                except ValueError:
                    print("Error: Unable to convert string to float")
            else:
                return float(value)

        return value