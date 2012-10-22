from django.db import models
from django_deferred_polymorph.models import DeferredPolymorphManager

class TaxManager(DeferredPolymorphManager):
    _cache = {}
    
    def get_for_id(self, id):
        try:
            tax = self.__class__._cache[self.db][id]
        except KeyError:
            # This could raise a DoesNotExist; that's correct behavior and will
            # make sure that only correct ctypes get stored in the cache dict.
            tax = self.get(pk=id).get_real_instance()
            self._add_to_cache(self.db, tax)
        return tax

    def clear_cache(self):
        self.__class__._cache.clear()

    def _add_to_cache(self, using, tax):
        self.__class__._cache.setdefault(using, {})[tax.id] = tax

