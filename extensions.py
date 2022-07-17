import requests # для формирования запросов к API
import json # для парсинга ответов от API

from config import API_KEY, keys

# класс исключений, связанных с неправильными параметрами в запросе на конвертацию
class APIException(Exception):
    pass


# класс для конвертации валют
class Converter:
    @staticmethod
    # base - валюта 1, quote - валюта 2, amount - количетво валюты 1
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError: # если неправильно задана валюта 1
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote.lower()]
        except KeyError: # если неправильно задана валюта 2
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key: # если валюты в запрсе совпадают
            raise APIException(f"Невозможно конвертировать одинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError: # если неправильно задано количество валюты 1
            raise APIException(f"Не удалось обработать количество {amount}!")

        # формирование запроса к API и парсинг ответа
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={quote_key}&base={base_key}"
        payload = {}
        headers = {"apikey": API_KEY}
        r = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(r.content)
        # формирование ответа после успешной конвертации
        new_price = round(response['rates'][quote_key] * amount, 2)
        message = f"Цена {amount} {base_key} в {quote_key}: {new_price}"
        return message

