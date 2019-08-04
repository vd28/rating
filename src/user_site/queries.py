from . import models


def fetch_active_config() -> models.Config:
    return models.Config.objects \
        .select_related('revision', 'university') \
        .filter(active=True) \
        .order_by('-created_at') \
        .first()
