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


class PriceObjectAttr(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name
    
    def __get__(self, obj, type=None):
        value = getattr(obj, self.field.attname, None)
        if value is None:
            return None
        return self.field._get_price(obj, value)
    
    def __set__(self, obj, value):
        if isinstance(value, Price):
            self.field._set_currency(obj, value)
            setattr(obj, self.field.attname, self.field._get_price_value(value))
        else:
            setattr(obj, self.field.attname, value)


class PriceObjectField(PriceField):
    def __init__(self, *args, **kwargs):
        self.currency = kwargs.pop('currency', None)
        self.tax = kwargs.pop('tax', None)
        self.property_name = kwargs.pop('property_name', '%s_obj')
        super(PriceObjectField, self).__init__(*args, **kwargs)
    
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
        tax = self.tax
        if hasattr(self.tax, '__call__'):
            tax = tax(instance)
        if isinstance(tax, Tax):
            return tax
        return getattr(instance, tax)
    
    def get_prep_value(self, value):
        if isinstance(value, Price):
            value = self._get_price_value(value)
        return super(PriceObjectField, self).get_prep_value(value)
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, Price):
            value = self._get_price_value(value)
        return super(PriceObjectField, self).get_db_prep_value(value, connection=connection, prepared=prepared)
    
    def get_db_prep_save(self, value, connection):
        if isinstance(value, Price):
            value = self._get_price_value(value)
        return super(PriceObjectField, self).get_db_prep_save(value, connection=connection)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        if isinstance(value, Price):
            value = self._get_price_value(value)
        return value
    
    def to_python(self, value):
        if isinstance(value, Price):
            return value
        return super(PriceObjectField, self).to_python(value)
    
    def _get_price(self, instance, price):
        raise NotImplemented()
    
    def _get_price_value(self, price):
        raise NotImplemented()
    
    def contribute_to_class(self, cls, name):
        if not isinstance(self.tax, Tax):
            field = cls._meta.get_field(self.tax)
            if not isinstance(field, models.ForeignKey):
                raise RuntimeError('invalid tax')
        super(PriceObjectField, self).contribute_to_class(cls, name)
        property_name = self.property_name
        if '%s' in property_name:
            property_name = property_name % name
        setattr(cls, property_name, PriceObjectAttr(cls, self, name))
        def get_price(s):
            return getattr(s, property_name)
        setattr(cls, "get_%s" % name, get_price)
        def set_price(s, v):
            return setattr(s, property_name, v)
        setattr(cls, "set_%s" % name, set_price)
    
    def formfield(self, **kwargs):
        raise NotImplemented()
    
    def south_field_triple(self):
        field_class, args, kwargs = south_field_triple(self)
        kwargs['currency'] = repr(self.currency)
        kwargs['tax'] = repr(self.tax)
        kwargs['property_name'] = repr(self.property_name)
        return field_class, args, kwargs


class NetPriceField(PriceObjectField):
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
    
    def formfield(self, **kwargs):
        from .forms import NetPriceField as NetPriceFormField
        defaults = {
            'form_class': NetPriceFormField,
        }
        defaults.update(kwargs)
        # we skip PriceObjectField.formfield, as this raises NotImplemented
        return super(PriceObjectField, self).formfield(**defaults)


class GrossPriceField(PriceObjectField):
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
    
    def formfield(self, **kwargs):
        from .forms import GrossPriceField as GrossPriceFormField
        defaults = {
            'form_class': GrossPriceFormField,
        }
        defaults.update(kwargs)
        # we skip PriceObjectField.formfield, as this raises NotImplemented
        return super(PriceObjectField, self).formfield(**defaults)


# currency


class CurrencyObjectAttr(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name
    
    def __get__(self, obj, type=None):
        value = getattr(obj, self.field.attname, None)
        if value is None:
            return None
        currency = Currency(
            iso_code = value,
        )
        return currency
    
    def __set__(self, obj, value):
        if isinstance(value, Currency):
            setattr(obj, self.field.attname, self.field._get_currency_value(value))
        else:
            setattr(obj, self.field.attname, value)


class CurrencyField(models.CharField):
    ''' Currency '''
    
    def __init__(self, *args, **kwargs):
        from .currencies import CURRENCIES
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('default', price_settings.DEFAULT_CURRENCY)
        kwargs.setdefault('choices', [(i[0], i[0]) for i in CURRENCIES])
        self.property_name = kwargs.pop('property_name', '%s_obj')
        super(CurrencyField, self).__init__(*args, **kwargs)
    
    def get_prep_value(self, value):
        if isinstance(value, Currency):
            value = self._get_currency_value(value)
        return super(CurrencyField, self).get_prep_value(value)
    
    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, Currency):
            value = self._get_currency_value(value)
        return super(CurrencyField, self).get_db_prep_value(value, connection=connection, prepared=prepared)
    
    def get_db_prep_save(self, value, connection):
        if isinstance(value, Currency):
            value = self._get_currency_value(value)
        return super(CurrencyField, self).get_db_prep_save(value, connection=connection)
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        if isinstance(value, Currency):
            value = self._get_currency_value(value)
        return value
    
    def to_python(self, value):
        if isinstance(value, Currency):
            return value
        return super(CurrencyField, self).to_python(value)
    
    def clean(self, value, model_instance):
        if isinstance(value, Currency):
            value = value.iso_code
        return super(CurrencyField, self).clean(value, model_instance)
    
    def _get_currency_value(self, currency):
        return currency.iso_code
    
    def contribute_to_class(self, cls, name):
        super(CurrencyField, self).contribute_to_class(cls, name)
        property_name = self.property_name
        if '%s' in property_name:
            property_name = property_name % name
        setattr(cls, property_name, CurrencyObjectAttr(cls, self, name))
        def get_currency(s):
            return getattr(s, property_name)
        setattr(cls, "get_%s" % name, get_currency)
        def set_currency(s, v):
            return setattr(s, property_name, v)
        setattr(cls, "set_%s" % name, set_currency)
    
    def formfield(self, **kwargs):
        # choice fields ignore form_class param, so we have to do this some other way here
        field = super(CurrencyField, self).formfield(**kwargs)
        old_prepare_value = field.prepare_value
        old_valid_value = field.valid_value
        def currency_prepare_value(value):
            if isinstance(value, Currency):
                value = value.iso_code
            return old_prepare_value(value)
        def currency_valid_value(value):
            if isinstance(value, Currency):
                value = value.iso_code
            return old_valid_value(value)
        field.prepare_value = currency_prepare_value
        field.valid_value = currency_valid_value
        return field
    
    def south_field_triple(self):
        field_class, args, kwargs = south_field_triple(self)
        kwargs['property_name'] = repr(self.property_name)
        return field_class, args, kwargs

