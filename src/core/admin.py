import textwrap
import json

from django.db import transaction
from django import forms
from django.shortcuts import render, redirect
from django.contrib import admin, messages
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from nested_admin.nested import NestedTabularInline, NestedModelAdmin
from admin_actions.admin import ActionsModelAdmin

from . import models
from .validators import FileValidator
from .loaders import LoaderError
from .loaders.revision import RevisionLoader


class ArticleItemInline(admin.TabularInline):
    model = models.ArticleItem
    autocomplete_fields = ('article', 'person')
    extra = 1


class DepartmentInline(NestedTabularInline):
    model = models.Department
    ordering = ('name',)
    extra = 0


class FacultyInline(NestedTabularInline):
    model = models.Faculty
    ordering = ('name',)
    inlines = (DepartmentInline,)
    extra = 1


@admin.register(models.University)
class UniversityAdmin(NestedModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = (FacultyInline,)


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')
    list_select_related = ('university',)
    search_fields = ('name', 'university__name')
    ordering = ('university__name', 'name',)
    sortable_by = ('name',)
    inlines = (DepartmentInline,)
    list_filter = (
        ('university', RelatedDropdownFilter),
    )

    def university(self, obj):
        return obj.university.name


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'university')
    search_fields = ('name', 'faculty__name', 'faculty__university__name')
    list_select_related = ('faculty__university',)
    ordering = ('faculty__university__name', 'faculty__name', 'name')
    sortable_by = ('name',)
    list_filter = (
        ('faculty__university', RelatedDropdownFilter),
        ('faculty', RelatedDropdownFilter)
    )

    def university(self, obj):
        return obj.faculty.university.name

    def faculty(self, obj):
        return obj.faculty.name


class PersonKeysFilter(admin.SimpleListFilter):
    title = _('key')
    parameter_name = 'key'

    def lookups(self, request, model_admin):
        return (
            ('orcid', 'ORCID'),
            ('scopus_key', 'Scopus'),
            ('google_scholar_key', 'Google Scholar'),
            ('semantic_scholar_key', 'Semantic Scholar'),
            ('wos_key', 'Web of Science')
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value not in set(lookup[0] for lookup in self.lookup_choices):
            return queryset
        return queryset.filter(**{f'{value}__isnull': False})


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_select_related = ('department__faculty__university',)
    list_display = ('full_name', 'university', 'faculty', 'department')
    search_fields = (
        'full_name', '=orcid', '=scopus_key', '=google_scholar_key', '=semantic_scholar_key', '=wos_key',
        'department__name', 'department__faculty__name', 'department__faculty__university__name'
    )
    ordering = ('full_name',)
    autocomplete_fields = ('department',)
    filter_horizontal = ('person_types',)
    sortable_by = ('full_name',)
    fieldsets = (
        (None, {
            'fields': ('full_name', 'department', 'person_types')
        }),
        ('Keys', {
            'classes': ('collapse',),
            'fields': ('orcid', 'scopus_key', 'google_scholar_key', 'semantic_scholar_key', 'wos_key')
        })
    )
    list_filter = ('person_types__name', PersonKeysFilter)
    actions = ('export_keys',)

    def university(self, obj: models.Person):
        return obj.department.faculty.university.name

    def faculty(self, obj: models.Person):
        return obj.department.faculty.name

    def department(self, obj: models.Person):
        return obj.department.name

    def export_keys(self, request, queryset):

        data = {}
        for person in queryset:
            if person.scopus_key:
                data.setdefault('scopus', []).append(person.scopus_key)

            if person.google_scholar_key:
                data.setdefault('google_scholar', []).append(person.google_scholar_key)

            if person.semantic_scholar_key:
                data.setdefault('semantic_scholar', []).append(person.semantic_scholar_key)

            if person.wos_key:
                data.setdefault('wos', []).append(person.wos_key)

        response = HttpResponse(json.dumps(data, indent=4, separators=(',', ': ')), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=keys.json'
        return response


@admin.register(models.PersonType)
class PersonTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'year')
    ordering = ('title', '-year')
    search_fields = ('title', 'persons__full_name')
    inlines = (ArticleItemInline,)

    def short_title(self, obj: models.Article):
        return textwrap.shorten(obj.title, width=200, placeholder='...')

    short_title.short_description = 'title'


class RevisionImportForm(forms.Form):
    file = forms.FileField(validators=[
        FileValidator(max_size=1024 * 600, content_types=('application/json', 'text/plain'))
    ])


@admin.register(models.Revision)
class RevisionAdmin(ActionsModelAdmin):
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_display_links = None
    list_display = (
        'created_at', 'source', 'scopus_snapshots', 'google_scholar_snapshots', 'semantic_scholar_snapshots',
        'wos_snapshots'
    )
    actions_list = ('import_revision',)

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('scopussnapshot_set') \
            .prefetch_related('googlescholarsnapshot_set') \
            .prefetch_related('semanticscholarsnapshot_set') \
            .prefetch_related('wossnapshot_set')

    def scopus_snapshots(self, obj: models.Revision):
        return obj.scopussnapshot_set.count()

    scopus_snapshots.short_description = 'Scopus Snapshots'

    def google_scholar_snapshots(self, obj: models.Revision):
        return obj.googlescholarsnapshot_set.count()

    google_scholar_snapshots.short_description = 'Google Scholar Snapshots'

    def semantic_scholar_snapshots(self, obj: models.Revision):
        return obj.semanticscholarsnapshot_set.count()

    semantic_scholar_snapshots.short_description = 'Semantic Scholar Snapshots'

    def wos_snapshots(self, obj: models.Revision):
        return obj.wossnapshot_set.count()

    wos_snapshots.short_description = 'Web of Science Snapshots'

    def has_change_permission(self, request, obj=None):
        return False

    @transaction.atomic
    def import_revision(self, request):
        context = self.admin_site.each_context(request)
        context['opts'] = self.opts
        context['has_view_permission'] = self.has_view_permission(request)
        context['title'] = _('Import revision')

        if request.method != 'POST':
            context['form'] = RevisionImportForm()
            return render(request, 'core/admin/revision_import.html', context)

        form = RevisionImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'core/admin/revision_import.html', context)

        try:
            loader = RevisionLoader(
                json.load(form.cleaned_data['file']),
                revision_source=models.Revision.SOURCE_IMPORT,
                chuck_size=200
            )
            loader.load()

        except json.JSONDecodeError:
            self.message_user(request, _('The file must be a valid JSON file.'), level=messages.ERROR)

        except LoaderError:
            self.message_user(request, _('Failed to import revision.'), level=messages.ERROR)

        else:
            self.message_user(request, _('Revision has been imported successfully.'), level=messages.SUCCESS)

        return redirect('admin:core_revision_changelist')

    import_revision.short_description = _('Import revision')
    import_revision.url_path = 'import'


class BaseSnapshotAdmin(admin.ModelAdmin):
    list_select_related = ('person', 'revision')
    ordering = ('-revision__created_at',)
    list_display = ('person', 'revision')
    list_filter = (
        ('revision', RelatedDropdownFilter),
    )
    search_fields = (
        'person__full_name', '=person__orcid', '=person__scopus_key', '=person__google_scholar_key',
        '=person__semantic_scholar_key', '=person__wos_key'
    )
    autocomplete_fields = ('person',)


@admin.register(models.ScopusSnapshot)
class ScopusRevisionAdmin(BaseSnapshotAdmin):
    list_display = BaseSnapshotAdmin.list_display + ('h_index', 'documents', 'citations')
    ordering = BaseSnapshotAdmin.ordering + ('-h_index', '-documents', '-citations')
    list_editable = ('h_index', 'documents', 'citations')


@admin.register(models.GoogleScholarSnapshot)
class GoogleScholarRevisionAdmin(BaseSnapshotAdmin):
    list_display = BaseSnapshotAdmin.list_display + ('h_index', 'citations')
    ordering = BaseSnapshotAdmin.ordering + ('-h_index', '-citations')
    list_editable = ('h_index', 'citations')


@admin.register(models.SemanticScholarSnapshot)
class SemanticScholarRevisionAdmin(BaseSnapshotAdmin):
    list_display = BaseSnapshotAdmin.list_display + ('citation_velocity', 'influential_citation_count')
    ordering = BaseSnapshotAdmin.ordering + ('-citation_velocity', '-influential_citation_count')
    list_editable = ('citation_velocity', 'influential_citation_count')


@admin.register(models.WosSnapshot)
class WosRevisionAdmin(BaseSnapshotAdmin):
    list_display = BaseSnapshotAdmin.list_display + ('publications',)
    ordering = BaseSnapshotAdmin.ordering + ('-publications',)
    list_editable = ('publications',)
