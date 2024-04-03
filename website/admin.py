from django.contrib import admin
from .models import Student
from .models import Map
from .models import Report

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "age", "level", "strand", "num_id", "status")

class MapAdmin(admin.ModelAdmin):
    list_display = ("title", "image_path")

class ReportAdmin(admin.ModelAdmin):
    list_display = ('location', 'map', 'status')
    list_filter = ('status',)
    actions = ['approve_reports']

    def approve_reports(self, request, queryset):
        queryset.update(status='Active')


admin.site.register(Student, StudentAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Report, ReportAdmin)
