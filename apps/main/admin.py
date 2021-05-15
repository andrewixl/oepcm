from django.contrib import admin
from .models import Change
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# admin.site.register(Change)

class ChangeResource(resources.ModelResource):
    class Meta:
        model = Change

class ChangeAdmin(ImportExportModelAdmin):
    resource_class = ChangeResource

admin.site.register(Change, ChangeAdmin)