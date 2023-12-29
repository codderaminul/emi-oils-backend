from django.contrib import admin
from account.models import DefaultCompany, Subscriber, Category,Company,EmailOTP,CustomUser
# Register your models here.

admin.site.register(EmailOTP)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Company)
class DefaultCompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(DefaultCompany,DefaultCompanyAdmin)
    
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email','phone')
    list_max_show_all = 100
admin.site.register(Subscriber, SubscriberAdmin)


