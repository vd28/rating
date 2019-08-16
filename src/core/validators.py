from typing import Optional, Iterable

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

import magic


@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': _("Ensure this file size is not greater than %(max_size)s. Your file size is %(size)s."),
        'min_size': _("Ensure this file size is not less than %(min_size)s. Your file size is %(size)s."),
        'content_type': _("Files of type %(content_type)s are not supported.")
    }

    def __init__(self, *, max_size: Optional[int] = None, min_size: Optional[int] = None,
                 content_types: Optional[Iterable[str]] = None):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = tuple(content_types) if content_types is not None else None

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'], code='max_size', params=params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.mix_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], code='min_size', params=params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'], code='content_type', params=params)

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.max_size == other.max_size and
            self.min_size == other.min_size and
            self.content_types == other.content_types
        )
