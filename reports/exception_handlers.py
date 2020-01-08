from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework import exceptions

from reports.serializers import CustomValidationError


def custom_exception_handler(exc, context):
    """Redefine format of custom type errors. """

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, CustomValidationError):
        data = {'msg': exc.detail, 'code': exc.code}

        set_rollback()
        return Response(data, status=exc.status_code)

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            try:
                code = exc.code
            except AttributeError:
                code = exc.default_code
            data = {'msg': exc.detail, 'code': code}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
