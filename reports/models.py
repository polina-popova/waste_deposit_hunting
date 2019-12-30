from django.db import models


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

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering = ('-pk', )
