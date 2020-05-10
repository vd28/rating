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

class ClasterAnalysisView(ConfigMixin,TemplateView):
    template_name = "user_site/claster_analysis.html"


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


class DepartmentPersonRatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/department_person_rating.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['person_types'] = tuple(core_queries.fetch_person_types())
        data['department'] = core_queries.fetch_department(self.kwargs['department_id'])
        return data


class FacultyDepartmentRatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/faculty_department_rating.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['faculty'] = core_queries.fetch_faculty(self.kwargs['faculty_id'])
        return data


class PersonView(ConfigMixin, TemplateView):
    template_name = 'user_site/person.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['person'] = core_queries.fetch_person(self.kwargs['person_id'], load_university=True)
        return data


class PersonsSearchResultsView(ConfigMixin, TemplateView):
    template_name = 'user_site/persons_search_results.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['persons'] = tuple(core_queries.search_persons(self.request.GET.get('t', None)))
        return data


class DocKnowledgeView(ConfigMixin, TemplateView):
    template_name = 'user_site/doc_knowledge.html'


class CooperatingView(ConfigMixin, TemplateView):
    template_name = 'user_site/cooperating.html'

class PostView(ConfigMixin, TemplateView):
    template_name = 'user_site/post.html'
