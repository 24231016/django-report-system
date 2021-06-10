from django.contrib import admin
from .models import User,ExploitReport,Images #,InforCollectReport
# Register your models here.
class ExploitReportAdmin(admin.ModelAdmin):
    list_display = ('target_name', 'user', 'upload_date' , 'status')

class InforCollectReportAdmin(admin.ModelAdmin):
    list_display = ('target_name', 'user', 'upload_date','status')

admin.site.register(User)
admin.site.register(Images)
admin.site.register(ExploitReport, ExploitReportAdmin)
# admin.site.register(InforCollectReport, InforCollectReportAdmin)
