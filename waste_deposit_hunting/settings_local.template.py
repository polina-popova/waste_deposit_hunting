import logging


# Django settings

SECRET_KEY = ''

LOGGER = logging.getLogger('main')


# Errors messages

INVALID_STATE_ERROR = 'К сожалению, на данным момент приложение не работает в вашем регионе.'

NO_PHOTO_ERROR = 'Фотография является обязательной.'

NO_LONG_ERROR = 'Широта является обязательной.'

NO_LAT_ERROR = 'Долгота является обязательной.'

INVALID_LAT_ERROR = 'Невалидная долгота.'

INVALID_LONG_ERROR = 'Невалидная широта.'

NO_COMPLAIN_BODY_ERROR = 'Добавьте текст жалобы.'


# Email setting

EMAIL_HOST_PASSWORD = ''

EMAIL_TITLE = 'Охота на свалку'


# Reports settings

PHOTO_MAX_HEIGHT = 1750
