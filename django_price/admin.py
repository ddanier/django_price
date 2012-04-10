from django.contrib import admin
from .models import *


admin.site.register(LinearTax, admin.ModelAdmin)
admin.site.register(MultiTax, admin.ModelAdmin)

