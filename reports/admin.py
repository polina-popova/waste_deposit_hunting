import json

from django.contrib import admin, auth
from django.core.validators import EmailValidator
from django import forms

from .helpers import clean_up_emails
from .models import Report, WasteDeposit, ContentComplain, State


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


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        exclude = ('id', )

    def clean(self):
        emails = self.cleaned_data.get('emails')
        if emails:
            emails_list = []
            validator = EmailValidator()

            for email in clean_up_emails(emails).split(','):
                stripped_email = email.strip()

                validator(stripped_email)
                emails_list.append(stripped_email)

            self.cleaned_data['emails'] = json.dumps(emails_list)

        return self.cleaned_data


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    form = StateForm
    list_display = ('state_name', 'emails', 'is_draft')


admin.site.register(ContentComplain)


admin.site.unregister(auth.models.Group)
admin.site.unregister(auth.models.User)
