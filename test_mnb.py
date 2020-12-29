import datetime
from django.test import TestCase
from services.mnb import MNB


class TestMNB(TestCase):
    def setUp(self):
        self.mnb_service = MNB()

    def test_is_client(self):
        self.assertTrue(self.mnb_service.client)

    def test_get_currencies(self):
        currencies = self.mnb_service.get_currencies()

        self.assertTrue(isinstance(currencies, list))

    def test_get_current_exchange_rates(self):
        rates, day = self.mnb_service.get_current_exchange_rates()

        self.assertTrue(isinstance(rates, dict))
        self.assertTrue(isinstance(day, datetime.date))

    def test_get_current_exchange_rate_by_currency_eur(self):
        currency = 'EUR'
        rate, day = self.mnb_service.get_latest_exchange_rate_by_currency(currency)

        self.assertTrue(isinstance(rate, str))

    def test_get_current_exchange_rate_by_currency_usd(self):
        currency = 'USD'
        rate, day = self.mnb_service.get_latest_exchange_rate_by_currency(currency)

        self.assertTrue(isinstance(rate, str))