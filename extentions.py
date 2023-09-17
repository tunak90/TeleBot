from config import keys
import requests
import json

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()
        if quote == base:
            raise APIException(f'You can not transfer the same currencies: {base}.')
        # quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Can not process this currency {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Can not process this currency {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Wrong amount type {amount}')
        if amount < 0:
            raise APIException(f'Negative amount of currency')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]*amount
        return total_base

