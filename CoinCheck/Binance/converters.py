import re
from urllib.parse import quote

class FullTicker:
    regex = "[a-z]{6,8}"

    def to_python(self, value):
        if re.match(self.regex, value):
            return value
        raise ValueError("Invalid ticker: must be 6 to 8 lowercase letters.")

    def to_url(self, value):
        return quote(value.lower())  # Кодируем строку для использования в URL
