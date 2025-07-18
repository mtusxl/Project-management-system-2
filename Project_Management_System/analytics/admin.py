from django.contrib import admin

from .models import *

admin.site.register(ProjectMetrics)
admin.site.register(UserPerformance)
admin.site.register(Report)
admin.site.register(ScheduledReport)
