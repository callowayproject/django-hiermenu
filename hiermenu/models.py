from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hiermenu import settings


class MenuManager(models.Manager):
    def get_items(self, menu, show_hidden=False, limit=None, user_groups=None):
        if user_groups == None:
            user_groups = []
        kwargs = {'display': True}
        if show_hidden:
            kwargs = {}
        q = self.get_query_set().filter(parent__pk=menu.pk, active=True,
            **kwargs).order_by('order')
        if isinstance(limit, int):
            q = q[:limit]
        for menu in q:
            menu_groups = menu.groups.all()
            if menu_groups and not set(menu_groups) & set(user_groups):
                q = q.exclude(pk=menu.pk)
        return q


class Menu(models.Model):
    name = models.SlugField(max_length=100,
        help_text=_('Menu name.'), unique=True)
    parent = models.ForeignKey("self", null=True, blank=True,
        help_text=_('The parent MenuItem this item will be a subitem of.'))
    text = models.CharField(blank=True, max_length=50,
        help_text=_('The text of the item.'))
    link = models.CharField(blank=True, max_length=255,
        help_text=_('The url in which this item links to.'))
    alt = models.CharField(blank=True, max_length=100,
        help_text=_('The alternate text.'))
    order = models.PositiveIntegerField(default=1,
        help_text=_('The order of the MenuItems.'))
    active_path_regex = models.CharField(blank=True, max_length=255,
        help_text=_('A regular expression to identify this menu as active.'))
    location = models.PositiveIntegerField(choices=settings.LOCATIONS,
        default=1, help_text=_('Location of menu.'))
    display = models.BooleanField(default=True,
        help_text=_('Show this menu item.'))
    cssclass = models.CharField(blank=True, max_length=100,
        help_text=_('Extra css classes.'))
    cssstyle = models.CharField(blank=True, max_length=100,
        help_text=_('Extra css styles.'))
    domid = models.CharField(blank=True, max_length=100,
        help_text=_('A dom ID.'))
    active_cssclass = models.CharField(blank=True, max_length=100,
        help_text=_('Extra css classes for active items.'))
    active_cssstyle = models.CharField(blank=True, max_length=100,
        help_text=_('Extra css styles for active items.'))
    active_domid = models.CharField(blank=True, max_length=100,
        help_text=_('A dom ID for active items.'))
    img = models.ImageField(blank=True, null=True,
        upload_to=settings.UPLOAD_IMG_PATH, help_text=_('A menu image.'))
    template_name = models.CharField(blank=True, max_length=100,
        help_text=_('Template override.'))
    active_template_name = models.CharField(blank=True, max_length=100,
        help_text=_('Acitve template override.'))
    active = models.BooleanField(default=True,
        help_text=_('Is this item active?'))
    groups = models.ManyToManyField(Group, blank=True, help_text=_('Add one '
        'group or more if you want to make the menu private'))

    objects = MenuManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
