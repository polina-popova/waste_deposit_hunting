import os

from io import BytesIO

from PIL import Image
from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings

from reports.helpers import get_desired_width


WASTE_DEPOSIT_STATUSES = (
    ('new', '1'),
)


class WasteDeposit(models.Model):
    """Model of the waste deposit object """

    lat = models.FloatField(verbose_name='Широта')
    long = models.FloatField(verbose_name='Долгота')
    status = models.CharField(
        choices=WASTE_DEPOSIT_STATUSES, max_length=100, default='1',
        verbose_name='Статус'
    )

    @property
    def location(self):
        return self.lat, self.long

    @property
    def reports_amount(self):
        return self.reports.count()

    @property
    def datetime_last_received(self):
        return self.reports.order_by('-datetime_received').first().datetime_received

    @property
    def datetime_penult_received(self):
        if self.reports_amount > 1:
            return self.reports.order_by('-datetime_received')[1].datetime_received

    @property
    def state(self):
        return self.reports.first().state

    def __str__(self):
        return f'Свалка №{self.pk}'

    class Meta:
        verbose_name = 'Свалка'
        verbose_name_plural = 'Свалки'
        ordering = ('-pk', )


class State(models.Model):
    state_name = models.CharField(max_length=500, verbose_name='Область')
    emails = models.CharField(
        blank=True, null=True, max_length=1500,
        verbose_name='Адреса почт координаторов'
    )
    is_draft = models.BooleanField(default=True, verbose_name='Черновик')

    def __str__(self):
        return self.state_name

    class Meta:
        verbose_name = 'Подключенная область'
        verbose_name_plural = 'Подключенные области'
        unique_together = [['id', 'state_name']]


class Report(models.Model):
    """Model of the report about waste deposit """

    datetime_received = models.DateTimeField(
        auto_now=True, verbose_name='Дата получения отчета'
    )

    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    lat = models.FloatField(blank=True, verbose_name='Широта')
    long = models.FloatField(blank=True, verbose_name='Долгота')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    feedback_info = models.TextField(blank=True, null=True, verbose_name='Обратная связь')

    waste_deposit = models.ForeignKey(
        WasteDeposit, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='reports', verbose_name='Свалка'
    )

    was_sent = models.BooleanField(default=False, verbose_name='Включено в ежедневный отчет')

    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='reports',
        verbose_name='Область', default=1
    )
    verbose_address = models.TextField(blank=True, null=True, verbose_name='Адрес')

    @property
    def image_filename(self):
        return os.path.basename(self.photo.name)

    @property
    def location(self):
        return self.lat, self.long

    def save(self, *args, **kwargs):
        if self.pk is None:  # Resize photo on first save
            opened_photo = Image.open(self.photo)

            if opened_photo.height > settings.PHOTO_MAX_HEIGHT:
                desired_width = get_desired_width(settings.PHOTO_MAX_HEIGHT, opened_photo)
                resized_photo = opened_photo.resize((round(desired_width), settings.PHOTO_MAX_HEIGHT), Image.ANTIALIAS)

                new_image_io = BytesIO()

                if opened_photo.format == 'JPEG':
                    resized_photo.save(new_image_io, format='JPEG')
                elif opened_photo.format == 'PNG':
                    resized_photo.save(new_image_io, format='PNG')

                temp_name = self.photo.name
                self.photo.delete(save=False)

                self.photo.save(
                    temp_name,
                    content=ContentFile(new_image_io.getvalue()),
                    save=False
                )

        return super(Report, self).save(*args, **kwargs)

    def delete(self, **kwargs):
        path = self.photo.path
        deletion_info = super().delete(**kwargs)

        os.remove(path)

        return deletion_info

    def __str__(self):
        return self.verbose_address or f'{self.lat}, {self.long}'

    class Meta:
        verbose_name = 'Сообщение о свалке'
        verbose_name_plural = 'Сообщения о свалках'
        ordering = ('-pk', )


class ContentComplain(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name='Сообщение о свалке')
    body = models.TextField(blank=True)
    datetime_received = models.DateTimeField(
        auto_now=True, verbose_name='Дата получения жалобы на контент'
    )

    def __str__(self):
        return f'Жалоба на сообщение {self.report_id}'

    class Meta:
        verbose_name = 'Жалоба на контент'
        verbose_name_plural = 'Жалобы на контент'
        ordering = ('-datetime_received', )
