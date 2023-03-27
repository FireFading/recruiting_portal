from django.contrib import admin

from projects.models import Project, Review, Tag


admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Review)
