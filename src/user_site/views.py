from django.views.generic import TemplateView, View
from django.urls import reverse
from django.shortcuts import redirect

from . import queries


class ConfigMixin(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = None

    def dispatch(self, request, *args, **kwargs):
        config = queries.fetch_active_config()
        if config is None:
            return redirect(reverse('config_not_found'))
        self.config = config
        return super().dispatch(request, *args, **kwargs)


class ConfigNotFoundView(TemplateView):
    template_name = 'user_site/config_not_found.html'


class HomeView(ConfigMixin, TemplateView):
    template_name = 'user_site/home.html'


class PersonRatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/person_rating.html'
