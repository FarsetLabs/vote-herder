# Register your models here.
from django.contrib import admin

from .models import Election, Candidate, Stage, StageCell

admin.site.register([Election, Candidate, Stage, StageCell])
