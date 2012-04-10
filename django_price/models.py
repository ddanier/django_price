# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django_model_utils.models import StatMixin
from django.db import models
from django_deferred_polymorph.models import SubDeferredPolymorphBaseModel
import decimal


# TODO: Versionized Tax (Tax should NEVER get changed, as this may
# create an invalid state if you store net + gross for invoices
class Tax(StatMixin, SubDeferredPolymorphBaseModel):
    name = models.CharField(max_length=25)
    
    def __unicode__(self):
        return self.name
    
    def amount(self, net):
        return self.get_tax().amount(net)
    
    def apply(self, net):
        return self.get_tax().apply(net)
    
    def reverse(self, gross):
        return self.get_tax().reverse(gross)
    
    def get_tax(self):
        raise RuntimeError('subclass must implement this')


class LinearTax(Tax):
    # TODO: PercentField?
    percent = models.DecimalField(max_digits=6, decimal_places=3)
    
    def get_tax(self):
        from . import LinearTax
        return LinearTax(self.name, self.percent)


class MultiTax(Tax):
    taxes = models.ManyToManyField(Tax, related_name='+')
    
    def get_tax(self):
        from . import MultiTax
        return MultiTax(self.taxes, self.name)

