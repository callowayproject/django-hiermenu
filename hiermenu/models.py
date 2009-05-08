from django.db import models
from hiermenu import settings

class MenuManager(models.Manager):
    def get_items(self, menu, show_hidden=False, limit=None):
        kwargs = {'display': True}
        if show_hidden:
            kwargs = {}
        q = self.get_query_set().filter(parent__pk=menu.pk, active=True, 
            **kwargs).order_by('order')
        if isinstance(limit, int):
            q = q[:limit]
        return q
        

class Menu(models.Model):
    name = models.SlugField(max_length=100, 
        help_text='Menu name.')
    parent = models.ForeignKey("self", null=True, blank=True, 
        help_text='The parent MenuItem this item will be a subitem of.')
    text = models.CharField(blank=True, max_length=50, 
        help_text='The text of the item.')
    link = models.CharField(blank=True, max_length=255, 
        help_text='The url in which this item links to.')
    alt = models.CharField(blank=True, max_length=100,  
        help_text='The alternate text.')
    order = models.PositiveIntegerField(default=1, 
        help_text='The order of the MenuItems.')
    active_path_regex = models.CharField(blank=True, max_length=255, 
        help_text='A regular expression to identify this menu as active.')
    location = models.PositiveIntegerField(choices=settings.LOCATIONS, 
        default=1, help_text='Location of menu.')
    display = models.BooleanField(default=True,
        help_text='Show this menu item.')
    cssclass = models.CharField(blank=True, max_length=100, 
        help_text='Extra css classes.')
    cssstyle = models.CharField(blank=True, max_length=100,
        help_text='Extra css styles.')
    domid = models.CharField(blank=True, max_length=100,
        help_text='A dom ID.')
    active_cssclass = models.CharField(blank=True, max_length=100, 
        help_text='Extra css classes for active items.')
    active_cssstyle = models.CharField(blank=True, max_length=100,
        help_text='Extra css styles for active items.')
    active_domid = models.CharField(blank=True, max_length=100, 
        help_text='A dom ID for active items.')
    img = models.ImageField(blank=True, null=True, 
        upload_to=settings.UPLOAD_IMG_PATH, help_text='A menu image.')
    template_name = models.CharField(blank=True, max_length=100, 
        help_text='Template override.')
    active_template_name = models.CharField(blank=True, max_length=100, 
        help_text='Acitve template override.')
    active = models.BooleanField(default=True, 
        help_text='Is this item active?')
    
    objects = MenuManager()
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['order']

