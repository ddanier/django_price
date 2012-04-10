from django import forms
from .price import Price
from .currency import Currency


class NetPriceField(forms.DecimalField):
    def prepare_value(self, value):
        if isinstance(value, Price):
            value = value.net
        return super(NetPriceField, self).prepare_value(value)


class GrossPriceField(forms.DecimalField):
    def prepare_value(self, value):
        if isinstance(value, Price):
            value = value.gross
        return super(GrossPriceField, self).prepare_value(value)


class CurrencyField(forms.TypedChoiceField):
    def prepare_value(self, value):
        if isinstance(value, Currency):
            value = value.iso_code
        return super(CurrencyField, self).prepare_value(value)
    
    def valid_value(self, value):
        if isinstance(value, Currency):
            value = value.iso_code
        return super(CurrencyField, self).valid_value(value)

