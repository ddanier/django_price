from django.db import models
from . import settings as price_settings
from .price import Price
from .tax import Tax
from .currency import Currency


def south_field_triple(self):
    from south.modelsinspector import introspector
    field_class = self.__class__.__module__ + "." + self.__class__.__name__
    args, kwargs = introspector(self)
    return (field_class, args, kwargs)


# price


class PriceField(models.DecimalField):
    ''' Price '''
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 15)
        kwargs.setdefault('decimal_places', 3)
        super(PriceField, self).__init__(*args, **kwargs)
    
    south_field_triple = south_field_triple


class PrecisePriceField(PriceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 21)
        kwargs.setdefault('decimal_places', 9)
        super(PrecisePriceField, self).__init__(*args, **kwargs)


class PriceObjectAttr(object):
    def __init__(self, model, access, name):
        self.model = model
        self.access = access
        self.name = name
    
    def __get__(self, obj, type=None):
        value = getattr(obj, self.access.price, None)
        if value is None:
            return None
        return self.access._get_price(obj, value)
    
    def __set__(self, obj, value):
        if isinstance(value, Price):
            self.access._set_currency(obj, value)
            setattr(obj, self.access.price, self.access._get_price_value(value))
        else:
            setattr(obj, self.access.price, value)


class PriceAccessBase(object):
    def __init__(self, price, tax, currency=None):
        self.price = price
        self.tax = tax
        self.currency = currency
    
    def _get_currency(self, instance):
        if self.currency is None:
            return None # Price() will default to DEFAULT_CURRENCY
        currency = self.currency
        if hasattr(currency, '__call__'):
            currency = currency(instance)
        else:
            if self.currency[0] == '=':
                return Currency(self.currency[1:])
            return getattr(instance, self.currency)
    
    def _set_currency(self, instance, price):
        currency = price.currency
        if not isinstance(currency, Currency):
            currency = Currency(currency)
        if hasattr(self.currency, '__call__'):
            self.currency(instance, currency)
        else:
            if self.currency is None: # we always use the default currency, so make sure it fits
                if currency.iso_code != price_settings.DEFAULT_CURRENCY:
                    raise RuntimeError('cannot change fixed (default) currency')
                return
            elif self.currency[0] == '=': # currency is fixed, make sure it fits
                if currency.iso_code != self.currency[1:]:
                    raise RuntimeError('cannot change fixed currency')
                return
            setattr(instance, self.currency, currency)
    
    def _get_tax(self, instance):
        from django.db.models.fields import FieldDoesNotExist
        from .models import Tax
        tax = self.tax
        if hasattr(self.tax, '__call__'):
            tax = tax(instance)
        if isinstance(tax, Tax):
            return tax
        try:
            field = instance._meta.get_field(tax)
        except FieldDoesNotExist:
            return getattr(instance, tax)
        tax_id = getattr(instance, field.attname)
        return Tax.objects.get_for_id(tax_id)
    
    def _get_price(self, instance, price):
        raise NotImplemented()
    
    def _get_price_value(self, price):
        raise NotImplemented()
    
    def contribute_to_class(self, cls, name):
        setattr(cls, name, PriceObjectAttr(cls, self, name))
        def get_price(s):
            return getattr(s, name)
        setattr(cls, "get_%s" % name, get_price)
        def set_price(s, v):
            return setattr(s, name, v)
        setattr(cls, "set_%s" % name, set_price)


class NetPriceAccess(PriceAccessBase):
    def _get_price(self, instance, price):
        tax = self._get_tax(instance)
        price = Price(
            net = price,
            currency = self._get_currency(instance),
            tax = tax,
        )
        return price
    
    def _get_price_value(self, price):
        return price.net


class GrossPriceAccess(PriceAccessBase):
    def _get_price(self, instance, price):
        tax = self._get_tax(instance)
        net = tax.reverse(price)
        price = Price(
            net = net,
            currency = self._get_currency(instance),
            tax = tax,
            gross = price,
        )
        return price
    
    def _get_price_value(self, price):
        return price.gross


# currency


class CurrencyField(models.CharField):
    def __init__(self, *args, **kwargs):
        from .currencies import CURRENCIES
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('default', price_settings.DEFAULT_CURRENCY)
        kwargs.setdefault('choices', [(i[0], i[0]) for i in CURRENCIES])
        super(CurrencyField, self).__init__(*args, **kwargs)
    
    south_field_triple = south_field_triple


class CurrencyObjectAttr(object):
    def __init__(self, model, access, name):
        self.model = model
        self.access = access
        self.name = name
    
    def __get__(self, obj, type=None):
        value = getattr(obj, self.access.currency, None)
        if value is None:
            return None
        currency = Currency(
            iso_code = value,
        )
        return currency
    
    def __set__(self, obj, value):
        if isinstance(value, Currency):
            setattr(obj, self.access.currency, self.access._get_currency_value(value))
        else:
            setattr(obj, self.access.currency, value)


class CurrencyAccess(models.CharField):
    def __init__(self, currency):
        self.currency = currency
    
    def _get_currency_value(self, currency):
        return currency.iso_code
    
    def contribute_to_class(self, cls, name):
        setattr(cls, name, CurrencyObjectAttr(cls, self, name))
        def get_currency(s):
            return getattr(s, name)
        setattr(cls, "get_%s" % name, get_currency)
        def set_currency(s, v):
            return setattr(s, name, v)
        setattr(cls, "set_%s" % name, set_currency)


# tax


class TaxField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        from .models import Tax
        kwargs.setdefault('to', Tax)
        kwargs.setdefault('related_name', '+')
        super(TaxField, self).__init__(*args, **kwargs)
    
    south_field_triple = south_field_triple

