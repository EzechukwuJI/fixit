from django.contrib import admin

# models: JobCategories, SubCategories, PostedJob, JobUploads, Responses
# Country State Zone Area

from fixitMain.models import * 

class CatAdmin(admin.ModelAdmin):
	# fields = ['category_title', 'caption']
	prepopulated_fields   =   {'title_slug': ('category_title',)}


class CatSubAdmin(admin.ModelAdmin):
	# fields                =   ['subcategory_title', 'caption', 'category']
	prepopulated_fields   =   {'title_slug': ('subcategory_title',)}


class PostedAdmin(admin.ModelAdmin):
	prepopulated_fields   =   {'title_slug': ('job_title',)}
	# fields = []

class ResponseAdmin(admin.ModelAdmin):
	fields = []


class UploadsAdmin(admin.ModelAdmin):
	fields = []

# Register your models here.
admin.site.register(JobCategories,   CatAdmin)
admin.site.register(SubCategories,   CatSubAdmin)
admin.site.register(PostedJob,       PostedAdmin)
admin.site.register(JobUploads,      UploadsAdmin)
admin.site.register(Responses,       ResponseAdmin)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Zone)
admin.site.register(Area)
admin.site.register(Messages)
