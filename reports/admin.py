from django.contrib import admin

from .models import Report, WasteDeposit


admin.site.register(WasteDeposit, admin.ModelAdmin)
admin.site.register(Report, admin.ModelAdmin)
