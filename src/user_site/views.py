from django.views.generic import TemplateView, View
from django.views.generic.base import ContextMixin
from django.urls import reverse
from django.shortcuts import redirect

from core import queries as core_queries
from . import queries


class ConfigMixin(ContextMixin, View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = None

    def dispatch(self, request, *args, **kwargs):
        config = queries.fetch_active_config()
        if config is None:
            return redirect(reverse('config_not_found'))
        self.config = config
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['config'] = self.config
        data['university'] = self.config.university
        data['revision'] = self.config.revision
        return data


class ConfigNotFoundView(TemplateView):
    template_name = 'user_site/config_not_found.html'


class HomeView(ConfigMixin, TemplateView):
    template_name = 'user_site/home.html'


class PersonRatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/person_rating.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['person_types'] = tuple(core_queries.fetch_person_types())
        return data


class FacultyRatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/faculty_rating.html'


class DepartmentRatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/department_rating.html'
