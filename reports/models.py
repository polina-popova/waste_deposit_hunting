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

    class Meta:
        verbose_name = 'Свалка'
        verbose_name_plural = 'Свалки'
        ordering = ('pk', )


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
        WasteDeposit, on_delete=models.CASCADE, related_name='reports',
        verbose_name='Свалка'
    )

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

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering = ('-pk', )
