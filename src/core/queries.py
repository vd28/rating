from typing import Union

from . import models


def fetch_latest_revision() -> Union[models.Revision, None]:
    return models.Revision.objects.order_by('-created_at').first()
