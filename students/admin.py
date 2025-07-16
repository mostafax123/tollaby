from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.Group)
admin.site.register(models.Session)
admin.site.register(models.Attendance)
admin.site.register(models.Payment)
admin.site.register(models.Offer)