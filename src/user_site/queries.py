from . import models


def fetch_active_config() -> models.Config:
    return models.Config.objects.filter(active=True).order_by('-created_at').first()
