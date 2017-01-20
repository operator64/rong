from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import User
from .models import Profile, profilefieldview, Field, FieldType

#import nested_admin

#class FieldAdmin(admin.ModelAdmin):
#    pass

#class FieldInline(admin.TabularInline):
#    model = field.profile.through

#class FieldtypeInline(admin.TabularInline):
#    model = FieldType

#class FieldInline(admin.TabularInline):
#    model = Field
class FieldTypeAdmin(admin.ModelAdmin):
    model = FieldType


class profilefieldviewInline(admin.TabularInline):
    model = profilefieldview
    extra = 1
    #inlines = (FieldInline,)
    verbose_name_plural = "Profile Fields"

class ProfileAdmin(admin.ModelAdmin):
    inlines = (profilefieldviewInline,)

class FieldAdmin(admin.ModelAdmin):
    model = Field
#    inlines = (FieldtypeInline,)
#    list_select_related=('ftype',)

#    def get_fieldtype(seld, instance):
#        return instance.field.fieldtype


class ProfileInline(admin.TabularInline):
#    inlines = (FieldInline,)
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
#    filter_horizontal = ('field',)

#    def get_inline_instances(self, request, obj=None):
#        if not obj:
#            return list()
#        return super(ProfileInline, self).get_inline_instances(request, obj)


#class FieldInline(admin.TabularInline):
#    model = profilefieldview



class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username','email','first_name','last_name','is_staff','get_location')
    list_select_related = ('profile',)

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(FieldType,FieldTypeAdmin)
# Register your models here.


