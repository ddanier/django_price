# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_deferred_polymorph.models import SubDeferredPolymorphBaseModel
import decimal
import datetime
from .manager import TaxManager


# TODO: Versionized Tax (Tax should NEVER get changed, as this may
# create an invalid state if you store net + gross for invoices
class Tax(SubDeferredPolymorphBaseModel):
    name = models.CharField(max_length=25)
    
    created = models.DateTimeField(editable=False, default=datetime.datetime.now)
    modified = models.DateTimeField(editable=False, default=datetime.datetime.now, auto_now=True)
    
    objects = TaxManager()
    
    def __unicode__(self):
        return self.name
    
    @property
    def unique_id(self):
        return self.get_tax().unique_id
    
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
        tax = LinearTax(self.name, self.percent)
        tax._unique_id = 'linear-pk-%d' % self.pk
        tax._model_instance = self
        return tax


class MultiTax(Tax):
    taxes = models.ManyToManyField(Tax, related_name='+')
    
    def get_tax(self):
        from . import MultiTax
        tax = MultiTax(list(self.taxes.all()), self.name)
        tax._unique_id = 'multi-pk-%d' % self.pk
        tax._model_instance = self
        return tax

