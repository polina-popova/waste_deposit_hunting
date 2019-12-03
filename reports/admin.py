from django.contrib.gis import admin

from .models import Report, WasteDeposit


admin.site.register(WasteDeposit, admin.OSMGeoAdmin)
admin.site.register(Report, admin.OSMGeoAdmin)
