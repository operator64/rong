from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import User
from .models import Profile, ProfileExpander, Expander, EType, Node, NodeTrait, Trait, NodeNote
from mptt.admin import MPTTModelAdmin

#import nested_admin

#class FieldAdmin(admin.ModelAdmin):
#    pass

#class FieldInline(admin.TabularInline):
#    model = field.profile.through

#class FieldtypeInline(admin.TabularInline):
#    model = FieldType

#class FieldInline(admin.TabularInline):
#    model = Field

class NodeNoteInline(admin.StackedInline):
    model = NodeNote
    extra = 0

    verbose_name = 'Comment'
    verbose_name_plural = 'Comments'

class NodeTraitInline(admin.TabularInline):
    model = NodeTrait
    extra = 0

    verbose_name = 'Property'
    verbose_name_plural = 'Properties'
        
class NodeAdmin(MPTTModelAdmin):
    model = Node
    inlines = (NodeTraitInline, NodeNoteInline)

    verbose_name = 'Entry'
    verbose_name_plural = 'Entries'

class TraitAdmin(admin.ModelAdmin):
    model = Trait

    verbose_name = 'Property'
    verbose_name = 'Properties'

  

class ETypeAdmin(admin.ModelAdmin):
    model = EType


class ProfileExpanderInline(admin.TabularInline):
    model = ProfileExpander
    extra = 1
    #inlines = (FieldInline,)
    verbose_name_plural = "Additional Profile Fields"

class ProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileExpanderInline,)

class ExpanderAdmin(admin.ModelAdmin):
    model = Expander
#    inlines = (FieldtypeInline,)
#    list_select_related=('ftype',)

#    def get_fieldtype(seld, instance):
#        return instance.field.fieldtype
    verbose_name = "Profile Field"


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
    inlines = (ProfileInline,)
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
admin.site.register(Expander, ExpanderAdmin)
admin.site.register(EType, ETypeAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Trait, TraitAdmin)
# Register your models here.


