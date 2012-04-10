# coding: utf-8
import decimal


class Tax(object):
    def __init__(self, name):
        self.name = name
    
    def amount(self, net):
        raise NotImplemented()
    
    def apply(self, net):
        return net + self.amount(net)
    
    def reverse(self, gross):
        raise NotImplemented()


class LinearTax(Tax):
    def __init__(self, name, percent):
        super(LinearTax, self).__init__(name)
        self.percent = percent
    
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
    
    def amount(self, net):
        amount = decimal.Decimal(0)
        for tax in self.taxes.all():
            amount += tax.amount(net)
        return amount
    
    def reverse(self, gross, currency=None):
        result = gross
        for tax in self.taxes.all():
            result = tax.reverse(result)
        return result



