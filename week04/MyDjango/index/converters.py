class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        # url 转给 python
        return int(value)

    def to_url(self, value):
        # python 转给 url
        return str(value)

class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_str(self, value):
        return f'{value}'