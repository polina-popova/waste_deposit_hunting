from django.contrib import admin, auth

from .models import Report, WasteDeposit


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'datetime_received', 'was_sent', 'photo', 'waste_deposit')
    readonly_fields = (
        'was_sent', 'datetime_received', 'photo', 'comment', 'feedback_info',
        'lat', 'long', 'verbose_address'
    )

    list_filter = ('datetime_received', 'waste_deposit')
    # list_editable = ('waste_deposit', )

    def has_add_permission(self, request):
        return False


@admin.register(WasteDeposit)
class WasteDepositAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'lat', 'long')
    readonly_fields = ('lat', 'long')
    exclude = ('status', )
    list_display_links = None

    def has_add_permission(self, request):
        return False


admin.site.unregister(auth.models.Group)
admin.site.unregister(auth.models.User)
