# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Election, Candidate, Stage, StageCell

admin.site.register([Election, Candidate, StageCell])


@admin.action(description="Mark selected stages as validated")
def validate_stage(modeladmin, request, queryset):
    queryset.update(validated_by=User)


class StageAdmin(admin.ModelAdmin):
    list_display = ["election", "count_stage", "author", "created"]
    ordering = ["election", "count_stage", "author", "created"]
    actions = [validate_stage]

    def get_form(self, request, obj=None, **kwargs):
        form = super(StageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["validated_by"].required = False
        form.base_fields["evidence_url"].required = False
        return form


admin.site.register(Stage, StageAdmin)
