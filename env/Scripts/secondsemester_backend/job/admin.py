from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser
# Register your models here.
from .models import History, Category, Notification, totalSlots, parkingSlots, availableSlots, CustomUser#, AccountAdmin
# from django.contrib.auth.admin import UserAdmin

admin.site.register(Notification)
admin.site.register(Category)
admin.site.register(History)
admin.site.register(totalSlots) # added
admin.site.register(availableSlots) # added
admin.site.register(parkingSlots) # added
# admin.site.register(AccountAdmin)
# for mongodb
# admin.site.register(User, UserAdmin)


# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Additional Info',
#             {
#                 'fields':(
#                     'first_name',
#                     'last_name',
#                 )
#             }
#         )
#     )

# admin.site.register(NewUser,CustomUserAdmin)
# admin.site.register(CustomUser)