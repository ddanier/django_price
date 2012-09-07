# coding: utf-8
import decimal
from . import settings as price_settings
from .utils import price_amount
from .currency import Currency


class Price(object):
    def __init__(self, net, currency=None, tax=None, gross=None):
        if currency is None:
            currency = price_settings.DEFAULT_CURRENCY
        if not isinstance(currency, Currency):
            currency = Currency(currency)
        self.currency = currency
        
        if not isinstance(net, decimal.Decimal):
            net = decimal.Decimal(str(net) or 'NaN')
        # we pass net through price_amount as late as possible, to avoid
        # removing decimal_places we might need to calculate the right
        # gross or tax
        self.net = net
        
        # support tax models
        if tax is not None and hasattr(tax, 'get_tax'):
            tax = tax.get_tax()
        
        # calculate tax, gross
        self.applied_taxes = {}
        if not tax is None and not gross is None:
            # we need to trust the external calculation here
            if not isinstance(gross, decimal.Decimal):
                gross = decimal.Decimal(str(gross or '') or 'NaN')
            self.net = price_amount(self.net, self.currency)
            self.gross = price_amount(gross, self.currency)
            self.applied_taxes[tax] = self.gross - self.net
        elif not tax is None:
            # self.net is still not rounded here, so tax_amount is super-precise ;-)
            tax_amount = tax.amount(self.net)
            self.net = price_amount(self.net, self.currency)
            self.gross = price_amount(self.net + tax_amount, self.currency)
            # we passed gross/net through price_amount while tax_amount and gross
            # was calculated precisely. So rounding tax_amount might give the
            # wrong value (0.4(net) + 0.4(tax) = 0.8(gross), rounded: 0 + 0 = 1)
            # to avoid this issue the stored tax_amount is calculated
            # using the rounded gross/net
            self.applied_taxes[tax] = self.gross - self.net
        elif not gross is None:
            raise RuntimeError('cannot specify gross amount without tax')
        else:
            # no tax applied
            self.net = price_amount(self.net, self.currency)
            self.gross = self.net
    
    def copy(self):
        result = Price(
            net = self.net,
            currency = self.currency,
        )
        result.gross = self.gross
        result.applied_taxes = self.applied_taxes.copy()
        return result
    
    @property
    def tax(self):
        return self.gross - self.net
    
    def _format_amount(self, value):
        from django.utils.formats import number_format
        # workaround for django not treating decimal_places==0 is implied
        # as prices always are rounded to their decimal_places, see
        # utils.price_amount
        # see https://code.djangoproject.com/ticket/13810
        return number_format(value, self.currency.decimal_places or 0)
    
    @property
    def formatted_net(self):
        return self._format_amount(self.net)
    
    @property
    def formatted_tax(self):
        return self._format_amount(self.tax)
    
    @property
    def formatted_taxes(self):
        return dict([(t, self._format_amount(ta)) for t, ta in self.applied_taxes.iteritems()])
    
    @property
    def formatted_gross(self):
        return self._format_amount(self.gross)
    
    #def __eq__(self, other):
    #    if not isinstance(other, Price):
    #        return False
    #    if self.currency != other.currency:
    #        return False # cannot compare different currencies
    #    # TODO: Compare taxes?
    #    return self.net == other.net and self.gross == other.gross
    #
    #def __ne__(self, other):
    #    return not self == other
    
    def __add__(self, other):
        if not isinstance(other, Price):
            raise TypeError('cannot add %s' % type(other))
        if self.currency != other.currency:
            raise TypeError('cannot add different currencies')
        result = Price(
            net = self.net + other.net,
            currency = self.currency,
        )
        result.gross = self.gross + other.gross
        result.applied_taxes = self.applied_taxes.copy()
        for tax, amount in other.applied_taxes.iteritems():
            if tax in result.applied_taxes:
                result.applied_taxes[tax] += amount
            else:
                result.applied_taxes[tax] = amount
        return result
    
    def __neg__(self):
        result = Price(
            net = -self.net,
            currency = self.currency,
        )
        result.gross = -self.gross
        for tax, amount in self.applied_taxes.iteritems():
            if tax in result.applied_taxes:
                result.applied_taxes[tax] -= amount
            else:
                result.applied_taxes[tax] = -amount
        return result
    
    def __mul__(self, factor):
        if not isinstance(factor, (int, long, float, decimal.Decimal)):
            raise TypeError("Cannot multiply with %s" % type(factor))
        if not isinstance(factor, decimal.Decimal):
            factor = decimal.Decimal(str(factor))
        if factor.is_nan():
            raise TypeError("Factor must be a number (!= 'NaN')")
        result = Price(
            net = self.net * factor,
            currency = self.currency,
        )
        gross = result.net
        for tax, amount in self.applied_taxes.iteritems():
            tax_amount = price_amount(amount * factor, self.currency)
            result.applied_taxes[tax] = tax_amount
            gross += tax_amount
        result.gross = gross
        return result
    
    def __div__(self, factor):
        if not isinstance(factor, (int, long, float, decimal.Decimal)):
            raise TypeError("Cannot multiply with %s" % type(factor))
        if not isinstance(factor, decimal.Decimal):
            factor = decimal.Decimal(str(factor))
        if factor.is_nan():
            raise TypeError("Factor must be a number (!= 'NaN')")
        result = Price(
            net = self.net / factor,
            currency = self.currency,
        )
        gross = result.net
        for tax, amount in self.applied_taxes.iteritems():
            tax_amount = price_amount(amount / factor, self.currency)
            result.applied_taxes[tax] = tax_amount
            gross += tax_amount
        result.gross = gross
        return result
    __truediv__ = __div__
    
    # django_ajax hook
    def ajax_data(self):
        return {
            'tax': self.formatted_tax,
            'net': self.formatted_net,
            'gross': self.formatted_gross,
            'currency': self.currency.ajax_data(),
        }


class EmptyPrice(Price):
    def __init__(self):
        self.net = decimal.Decimal('0')
        self.currency = Currency(price_settings.DEFAULT_CURRENCY)
        self.applied_taxes = {}
        self.gross = decimal.Decimal('0')
    
    def copy(self):
        return self
    
    def __add__(self, other):
        return other.copy()
    
    def __mul__(self, factor):
        return self
    
    def __div__(self, factor):
        return self
    __truediv__ = __div__

