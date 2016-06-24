from django.contrib import admin


from  fixitTradesmen.models import Biodata, CoporateData, Documents, JobList, Tradesman

class CoporateAdmin(admin.ModelAdmin):
	prepopulated_fields   =   {'name_slug': ('company_name',)}


# Register your models here.
admin.site.register(Biodata)
admin.site.register(CoporateData, CoporateAdmin)
admin.site.register(Documents)
admin.site.register(JobList)
admin.site.register(Tradesman)