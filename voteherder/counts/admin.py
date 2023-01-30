# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Election, Ballot, Candidate, Stage, StageCell

admin.site.register([Election, Ballot, Candidate, StageCell])
admin.site.site_header = "VoteHerder Administration"
admin.site.site_title = "VoteHerder Admin Site"
admin.site.index_title = "VoteHerder Management Portal"


@admin.action(description="Mark selected stages as validated")
def validate_stage(modeladmin, request, queryset):
    queryset.update(validated_by=User)


class StageAdmin(admin.ModelAdmin):
    list_display = ["ballot", "count_stage", "author", "created"]
    ordering = ["ballot", "count_stage", "author", "created"]
    actions = [validate_stage]

    def get_form(self, request, obj=None, **kwargs):
        form = super(StageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["validated_by"].required = False
        form.base_fields["evidence_url"].required = False
        return form


admin.site.register(Stage, StageAdmin)
