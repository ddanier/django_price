# coding: utf-8
import decimal
from . import settings as price_settings
from .utils import price_amount
from .currency import Currency
from .tax import NO_TAX


class Price(object):
    def __init__(self, net, currency=None, tax=None, gross=None):
        if currency is None:
            currency = price_settings.DEFAULT_CURRENCY
        if not isinstance(currency, Currency):
            currency = Currency(currency)
        self.currency = currency
        
        if not isinstance(net, decimal.Decimal):
            net = decimal.Decimal(str(net) or 'NaN')
        
        # support tax models
        if tax is not None and hasattr(tax, 'get_tax'):
            tax = tax.get_tax()
        
        # calculate tax, gross
        self._applied_taxes = {}
        if not tax is None and not gross is None:
            # we need to trust the external calculation here
            if not isinstance(gross, decimal.Decimal):
                gross = decimal.Decimal(str(gross or '') or 'NaN')
        elif not tax is None:
            # self.net is still not rounded here, so tax_amount is super-precise ;-)
            gross = tax.apply(net)
        elif not gross is None:
            raise RuntimeError('cannot specify gross amount without tax')
        else:
            # no tax applied
            gross = net
            tax = NO_TAX
        self._applied_taxes[tax.unique_id] = (tax, net, gross)
        self._recalculate_overall()
    
    def _recalculate_overall(self):
        # we pass net/gross through price_amount as late as possible, to avoid
        # removing decimal_places we might need to calculate the right
        # gross or tax. self._applied_taxes always stores the raw values without
        # any rounding. This way we do not loose precision on calculation.
        net = decimal.Decimal('0')
        gross = decimal.Decimal('0')
        for tax, tax_net, tax_gross in self._applied_taxes.values():
            # we have to round every net/gross on its own, otherwise
            # we would risk rounding issues (0.3 + 0.3 = 0.6, rounded
            # 0 + 0 = 1)
            net += price_amount(tax_net, self.currency)
            gross += price_amount(tax_gross, self.currency)
        self.net = net
        self.gross = gross
    
    def __str__(self):
        from django.utils.encoding import smart_str
        return smart_str(unicode(self))
    
    def __unicode__(self):
        from django.utils.translation import ugettext
        return ugettext('%(currency)s %(amount)s') % {
            'amount': self.formatted_gross,
            'currency': self.formatted_currency,
        }
    
    def copy(self):
        from copy import copy
        result = copy(self)
        result._applied_taxes = self._applied_taxes.copy()
        return result
    
    def rounded(self):
        applied_taxes = {}
        for tax, net, gross in self._applied_taxes.values():
            applied_taxes[tax.unique_id] = (
                tax,
                price_amount(net, self.currency),
                price_amount(gross, self.currency),
            )
        return CalculatedPrice(applied_taxes, self.currency)
    
    @property
    def precise_net(self):
        return sum([t[1] for t in self._applied_taxes.values()])
    
    @property
    def precise_gross(self):
        return sum([t[2] for t in self._applied_taxes.values()])
    
    @property
    def precise_tax(self):
        return sum([t[2] - t[1] for t in self._applied_taxes.values()])
    
    @property
    def tax(self):
        return self.gross - self.net
    
    @property
    def applied_tax(self):
        if len(self._applied_taxes) != 1:
            raise RuntimeError('This Price has multiple taxes, use obj.taxes instead')
        return self._applied_taxes.values()[0][0]
    
    @property
    def applied_taxes(self):
        return [
            Price(
                net = net,
                tax = tax,
                gross = gross,
                currency = self.currency,
            )
            for tax, net, gross
            in self._applied_taxes.values()
        ]
    
    @property
    def formatted_currency(self):
        return self.currency.symbol if self.currency.symbol else self.currency.iso_code
    
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
    def formatted_gross(self):
        return self._format_amount(self.gross)
    
    @property
    def formatted_tax(self):
        return self._format_amount(self.tax)
    
    def __add__(self, other):
        # EmptyPrice should work regardless of currency, does not change anything
        if isinstance(other, EmptyPrice):
            self.copy()
        if not isinstance(other, Price):
            raise TypeError('cannot add %s' % type(other))
        if self.currency != other.currency:
            raise TypeError('cannot add different currencies')
        applied_taxes = self._applied_taxes.copy()
        for tax, net, gross in other._applied_taxes.values():
            if tax.unique_id in applied_taxes:
                applied_taxes[tax.unique_id] = (
                    applied_taxes[tax.unique_id][0],
                    applied_taxes[tax.unique_id][1] + net,
                    applied_taxes[tax.unique_id][2] + gross,
                )
            else:
                applied_taxes[tax.unique_id] = (tax, net, gross)
        # filter out NO_TAX, if it is not relevant
        if NO_TAX.unique_id in applied_taxes \
            and applied_taxes[NO_TAX.unique_id][1] == 0 \
            and applied_taxes[NO_TAX.unique_id][2] == 0:
                del applied_taxes[NO_TAX.unique_id]
        return CalculatedPrice(applied_taxes, self.currency)
    
    def __neg__(self):
        applied_taxes = {}
        for tax, net, gross in self._applied_taxes.values():
            applied_taxes[tax.unique_id] = (tax, -net, -gross)
        return CalculatedPrice(applied_taxes, self.currency)
    
    def __mul__(self, factor):
        if not isinstance(factor, (int, long, float, decimal.Decimal)):
            raise TypeError("Cannot multiply with %s" % type(factor))
        if not isinstance(factor, decimal.Decimal):
            factor = decimal.Decimal(str(factor))
        if factor.is_nan():
            raise TypeError("Factor must be a number (!= 'NaN')")
        applied_taxes = {}
        for tax, net, gross in self._applied_taxes.values():
            calc_net = net * factor
            calc_gross = gross * factor
            applied_taxes[tax.unique_id] = (tax, calc_net, calc_gross)
        return CalculatedPrice(applied_taxes, self.currency)
    
    def __div__(self, factor):
        if not isinstance(factor, (int, long, float, decimal.Decimal)):
            raise TypeError("Cannot multiply with %s" % type(factor))
        if not isinstance(factor, decimal.Decimal):
            factor = decimal.Decimal(str(factor))
        if factor.is_nan():
            raise TypeError("Factor must be a number (!= 'NaN')")
        applied_taxes = {}
        for tax, net, gross in self._applied_taxes.values():
            calc_net = net / factor
            calc_gross = gross / factor
            applied_taxes[tax.unique_id] = (tax, calc_net, calc_gross)
        return CalculatedPrice(applied_taxes, self.currency)
    __truediv__ = __div__
    
    # django_ajax hook
    def ajax_data(self):
        return {
            'tax': self.formatted_tax,
            'net': self.formatted_net,
            'gross': self.formatted_gross,
            'currency': self.currency.ajax_data(),
        }


class CalculatedPrice(Price):
    def __init__(self, applied_taxes, currency=None):
        if currency is None:
            currency = price_settings.DEFAULT_CURRENCY
        if not isinstance(currency, Currency):
            currency = Currency(currency)
        self.currency = currency
        
        self._applied_taxes = applied_taxes
        self._recalculate_overall()


class EmptyPrice(Price):
    def __init__(self):
        self.net = decimal.Decimal('0')
        self.currency = Currency(price_settings.DEFAULT_CURRENCY)
        self.gross = decimal.Decimal('0')
        self._applied_taxes = {
            NO_TAX.unique_id: (NO_TAX, self.net, self.gross)
        }
    
    def copy(self):
        return self
    
    def __add__(self, other):
        return other.copy()
    
    def __mul__(self, factor):
        return self
    
    def __div__(self, factor):
        return self
    __truediv__ = __div__

