import textwrap

from django.contrib import admin

from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from . import models


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
    search_fields = ('name',)

    def has_module_permission(self, request):
        return False


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'faculty__name', 'faculty__university__name')

    def has_module_permission(self, request):
        return False


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
    list_filter = ('person_types__name',)

    def university(self, obj: models.Person):
        return obj.department.faculty.university.name

    def faculty(self, obj: models.Person):
        return obj.department.faculty.name

    def department(self, obj: models.Person):
        return obj.department.name


@admin.register(models.PersonType)
class PersonTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)
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


@admin.register(models.Revision)
class RevisionAdmin(admin.ModelAdmin):
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_display_links = None
    list_display = (
        'created_at', 'scopus_snapshots', 'google_scholar_snapshots', 'semantic_scholar_snapshots', 'wos_snapshots'
    )

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


class BaseSnapshotAdmin(admin.ModelAdmin):
    list_select_related = ('person', 'revision')
    ordering = ('-revision__created_at',)
    list_display = ('person', 'revision')
    list_filter = ('revision',)
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
