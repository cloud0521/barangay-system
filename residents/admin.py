from django.contrib import admin
from .models import Resident, Transaction, Official

# Register your models here.
admin.site.register(Resident)
admin.site.register(Transaction)
admin.site.register(Official)