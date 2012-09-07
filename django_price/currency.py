# coding: utf-8
from .currencies import CURRENCIES


class Currency(object):
    CURRENCIES = dict([(c[0], c[1:]) for c in CURRENCIES])
    
    def __init__(self, iso_code):
        if not iso_code in self.CURRENCIES:
            raise TypeError('unknown currency (%s)' % iso_code)
        self.iso_code = iso_code
        self.iso_num, self.decimal_places, self.rounding, self.name, self.symbol = self.CURRENCIES[iso_code]
    
    def __str__(self):
        from django.utils.encoding import smart_str
        return smart_str(unicode(self))
    
    def __unicode__(self):
        return self.iso_code
    
    def __eq__(self, other):
        if not isinstance(other, Currency):
            # allow direct comparision to iso codes
            if other in self.CURRENCIES:
                return self.iso_code == other
            return False
        return self.iso_code == other.iso_code
    
    def __ne__(self, other):
        return not self == other
    
    # django_ajax hook
    def ajax_data(self):
        return {
            'iso_code': self.iso_code,
            'name': self.name,
            'symbol': self.symbol,
        }


