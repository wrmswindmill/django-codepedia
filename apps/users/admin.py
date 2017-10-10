from django.contrib import admin

# Register your models here.
class ProjectAdmin(object):
    list_display = ['name', 'path','rel_path','github','ossean','language','tags']
    search_field = ['name', 'path','rel_path','github','ossean','language','tags']
    list_filter = ['name', 'path','rel_path','github','ossean','language','tags']