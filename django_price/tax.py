# coding: utf-8
import decimal
from django.utils.translation import ugettext_lazy as _


class Tax(object):
    def __init__(self, name):
        self.name = name
        self._unique_id = None
    
    def __str__(self):
        from django.utils.encoding import smart_str
        return smart_str(unicode(self))
    
    def __unicode__(self):
        return self.name
    
    @property
    def unique_id(self):
        if self._unique_id is None:
            return self._get_unique_id()
        return self._unique_id
    
    def _get_id(self):
        raise NotImplemented()
    
    def amount(self, net):
        raise NotImplemented()
    
    def apply(self, net):
        return net + self.amount(net)
    
    def reverse(self, gross):
        raise NotImplemented()


class NoTax(Tax):
    def __init__(self):
        self.name = _('No Tax')
        self._unique_id = 'none'
    
    def amount(self, net):
        return decimal.Decimal('0')
    
    def reverse(self, gross):
        return gross
NO_TAX = NoTax()


class LinearTax(Tax):
    def __init__(self, name, percent):
        super(LinearTax, self).__init__(name)
        if not isinstance(percent, decimal.Decimal):
            percent = decimal.Decimal(str(percent) or 'NaN')
        self.percent = percent
    
    def _get_unique_id(self):
        return 'linear-%s' % str(self.percent)
    
    def amount(self, net):
        return net * self.percent
    
    def reverse(self, gross, currency=None):
        return gross / (1 + self.percent)


class MultiTax(Tax):
    def __init__(self, taxes, name=None):
        if name is None:
            super(MultiTax, self).__init__(' + '.join([t.name for t in taxes]))
        else:
            super(MultiTax, self).__init__(name)
        self.taxes = taxes
    
    def _get_unique_id(self):
        return 'multi-%s' % '-'.join(list(sort([t.get_id() for t in self.taxes])))
    
    def amount(self, net):
        amount = decimal.Decimal(0)
        for tax in self.taxes:
            amount += tax.amount(net)
        return amount
    
    def reverse(self, gross, currency=None):
        result = gross
        for tax in reversed(self.taxes):
            result = tax.reverse(result)
        return result



