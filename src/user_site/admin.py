from django.contrib import admin
from . import models
from django import forms
from django.shortcuts import render, redirect
from django.contrib import admin, messages
import textwrap
import json
from django.db import transaction

@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('university', 'revision', 'active')
    list_editable = ('active',)
    list_select_related = ('revision', 'university')
    ordering = ('-revision__created_at', 'university__name')
    autocomplete_fields = ('university',)

    def save_model(self, request, obj, form, change):
        models.Config.objects.select_for_update().filter(active=True).update(active=False)
        super().save_model(request, obj, form, change)





@admin.register(models.Doc_knowledge)
class Doc_knowledge_Admin(admin.ModelAdmin):
    field_of_knowledge = ()
    number =()
    actions_list = ('import_revision',)

    list_display = ("field_of_knowledge" , )
    search_fields = ('field_of_knowledge', )
    ordering = ( 'field_of_knowledge',)
    sortable_by = ('field_of_knowledge',)

    def university(self, obj):
        return obj.university.name

@admin.register(models.Cooperating)
class Cooperating_Admin(admin.ModelAdmin):
    organization_name = ()
    number =()

    list_display = ("organization_name" , )
    search_fields = ('organization_name', )
    ordering = ( 'organization_name',)
    sortable_by = ('organization_name',)


@admin.register(models.Post)
class Cooperating_Admin(admin.ModelAdmin):
    list_display = ("title" , )
    search_fields = ('title', )
    ordering = ( 'title',)
    sortable_by = ('title',)
@admin.register(models.ClasterAnalysis)
class Claster_Analysis(admin.ModelAdmin):
    list_display = ("date",)
    search_fields = ('date',)
    ordering = ('date',)
    sortable_by = ('date',)


