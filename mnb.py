"""
Minimal Service File to get the latest Exchange Rates from the Hungarian Central Bank (MNB).
MNB provide a SOAP service to access the data.
No XDS schema, so  need to use xmltodict to get a python object
"""
import os
import datetime

from zeep import Client as ZeepClient, Settings as ZeepSettings
import xmltodict

class MNB:
    def __init__(self):
        url = 'http://www.mnb.hu/arfolyamok.asmx?wsdl'

        zeep_settings = ZeepSettings(strict=False, xml_huge_tree=True)

        self.client = ZeepClient(url, settings=zeep_settings)

    def get_currencies(self):
        """ return the available currencies as a list"""
        currencies = self.client.service.GetCurrencies()
        currencies = xmltodict.parse(currencies)
        return currencies['MNBCurrencies']['Currencies']['Curr']

    def get_current_exchange_rates(self):
        """
        Return the latest available Exchangerates for all the Currencies

        :return: tuple
            - dict, where the Currencies are the keys and the ExchangeRates are the values (str)
            - date object, latest day when there is an available rate
        """
        resp = self.client.service.GetCurrentExchangeRates()
        resp = xmltodict.parse(resp)

        day = resp['MNBCurrentExchangeRates']['Day']['@date']
        day = datetime.datetime.strptime(day, '%Y-%m-%d').date()

        rates = resp['MNBCurrentExchangeRates']['Day']['Rate']

        rates_dict = {}

        for rate in rates:
            rates_dict[rate['@curr']] = rate['#text']

        return rates_dict, day

    def get_latest_exchange_rate_by_currency(self, currency):
        """ return the latest exchange rate for a given currency"
            :return: tuple
            - rate for the given currency (string)
            - latest day when there is an available rate
        """
        rates, day = self.get_current_exchange_rates()

        rate = rates.get(currency, None)

        if not rate:
            raise ValueError('Currency not found.')

        return rate, day



