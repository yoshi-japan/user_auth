from django.contrib import admin
from . import models
# Register your models here.

# this enable us to edit items in database at admin page.
admin.site.register(models.Topic)
admin.site.register(models.Comment)
admin.site.register(models.Category)