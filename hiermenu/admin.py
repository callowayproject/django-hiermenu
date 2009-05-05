from django.contrib import admin
from hiermenu.models import Menu

class MenuItemInline(admin.TabularInline):
    model = Menu
    extra = 3
    
    
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline,]
    fieldsets = (
        (None, {'fields': ('name', 'parent', 'location', 'text', 'link', 'order', 'display', 'active',)}),
        ('Display Options', {'classes': ('collapse',),
            'fields': ('cssclass', 'cssstyle', 'template_name', 'active_template_name', 'img',)}),
        ('Advanced Options', {'classes': ('collapse',), 
            'fields': ('alt', 'domid', 'active_path_regex',)}),
    )
    list_display = ('name', 'parent', 'hierarchy', 'order', 'display', 'active')
    list_filter = ('parent',)
    search_fields = ('name', 'text')
    ordering = ('name',)

    def hierarchy(self, obj):
        parent, text, ret = obj.parent, obj.text or obj.name, obj.text or obj.name
        while parent:
            ret = ret + " > %s" % parent.text or parent.name
            parent = parent.parent
        return ret
    hierarchy.short_description = 'Hierarchy'