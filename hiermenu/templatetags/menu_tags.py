import re

from django.template import Library, Node, TemplateSyntaxError, Variable
from django.template.loader import get_template, render_to_string
from django.core.cache import cache

from hiermenu import settings
from hiermenu.models import Menu

register = Library()


def map_location(loc):
    for val in settings.LOCATIONS:
        if val[1].lower() == loc.lower():
            return val
    return settings.LOCATIONS[0]


class RenderMenuNode(Node):
    """
    Render menu node will render a given menu or menu_name.
    """
    menu_name, loc, loc_name, template_prefix, override_match = None, '', '', '', ''

    def __init__(self, menu_name, location, template_prefix='', override_match=''):
        self.menu_name = menu_name
        self.loc, self.loc_name = map_location(location)
        self.template_prefix = template_prefix
        self.override_match = override_match

    def render(self, context):
        m_name, menu, request = self.menu_name, None, None
        loc, loc_name = int(self.loc), self.loc_name.lower()
        tmp_pre, override_match = self.template_prefix, self.override_match
        cache_menu, cache_items = False, False
        # Try to resolve the menu_name argument, incase it is a Menu object,
        # we set m_name to menu.name if it is not a Menu object but
        # still resolves, we use that as the name.
        try:
            menu = Variable(m_name).resolve(context)
            if isinstance(menu, Menu):
                m_name = menu.name.lower()
            else:
                m_name = menu
                menu = None
        except:
            pass

        try:
            override_match = Variable(override_match).resolve(context)
        except:
            pass

        # Resolve the request context
        user_groups = []
        if 'request' in context:
            request = Variable('request').resolve(context)
            if getattr(request, "user"):
                user_groups = request.user.groups.all()

        # Build the cache keys, one for the menu object and one for the menu
        # items.
        cache_replace = u'---------------------------------!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz-------------------------------------------------------------------------------------------------------------------------------------'
        key = '%s.hiermenu.%s' % (settings.CACHE_KEY_PREFIX, m_name.translate(cache_replace))
        key_items = key + '.items'

        # If the menu was not resolved, this means a name was passed in,
        # therefore we get the menu object by name, but first we try to
        # get a cached version of the menu object.
        if not menu:
            try:
                menu = cache.get(key)
                if not menu:
                    cache_menu = True
                    menu = Menu.objects.get(name__iexact=m_name, location=loc)
            except Menu.DoesNotExist:
                return ''

        # Get the items from the cache, if nothing is returned we retrieve
        # the items from the database.
        items = cache.get(key_items)
        if not items:
            cache_items = True
            items = Menu.objects.get_items(menu, user_groups=user_groups)

        # Determine if the current menu is an active menu according to the
        # request.path and the menu's active_regex_path. If it is active
        # we set is_active to True
        suffix_template_name = ''
        setattr(menu, 'is_active', False)
        if hasattr(request, 'path') and menu.active_path_regex:
            r = re.compile(menu.active_path_regex, re.IGNORECASE)
            if override_match:
                if override_match.lower() == m_name:
                    setattr(menu, 'is_active', True)
                    suffix_template_name = '_active'
            elif r.match(request.path):
                setattr(menu, 'is_active', True)
                suffix_template_name = '_active'

        # Get the template that will be used to render the menu, first we
        # check if the menu has any overrides specified, then we check for
        # templates with the name of the menu, and finally default to
        # default.html if no others were found.
        try:
            template = None
            try:
                # Item specific template names
                if menu.is_active:
                    template = get_template('hiermenu/%s' % menu.active_template_name)
                else:
                    template = get_template('hiermenu/%s' % menu.template_name)
            except:
                template = None

            # Menu name templates
            if not template:
                try:
                    template = get_template('hiermenu/%s%s%s%s.html' (
                        tmp_pre, m_name, loc_name, suffix_template_name))
                except:
                    try:
                        template = get_template('hiermenu/%s%s%s.html' % (
                            tmp_pre, m_name, suffix_template_name))
                    except:
                        template = get_template('hiermenu/%s%s.html' % (
                            tmp_pre, m_name))
        except:
            try:
                # Default template names
                try:
                    template = get_template('hiermenu/%sdefault%s.html' % (
                        tmp_pre, suffix_template_name))
                except:
                    template = get_template('hiermenu/%sdefault.html' % tmp_pre)
            except:
                template = get_template('hiermenu/default.html')

        # Loop all the items, determining if one or more of the items are
        # active according to the request.path and the item's active_regex_path
        if hasattr(request, 'path'):
            for i in items:
                setattr(i, 'is_active', False)
                if i.active_path_regex:
                    r = re.compile(i.active_path_regex, re.IGNORECASE)
                    if override_match:
                        if override_match.lower() == i.name.lower():
                            setattr(i, 'is_active', True)
                    elif r.match(request.path):
                        setattr(i, 'is_active', True)

        # Build the context to be sent to the template. We send the request
        # so request.path is preserved.
        c = {'menu': menu, 'items': items, 'request': request}
        # Render the template
        ret = render_to_string(template.name, c)
        # Set the cache keys, only if items were not retrieved from cache.
        if cache_menu:
            cache.set(key, menu, settings.CACHE_TIMEOUT)
        if cache_items:
            cache.set(key_items, items, settings.CACHE_TIMEOUT)
        # Return the render template.
        return ret


def do_render_menu(parser, token):
    """
    Render the menu

        {% render_menu menu_name location [template_prefix] [override_match]  %}

    Examples

        {% render_menu main_menu none %}

        {% render_menu main_menu top main_ %}

    """
    argv = token.contents.split()
    argc = len(argv)
    if argc == 3:
        return RenderMenuNode(argv[1], argv[2])
    elif argc == 4:
        return RenderMenuNode(argv[1], argv[2], argv[3])
    elif argc == 5:
        return RenderMenuNode(argv[1], argv[2], argv[3], argv[4])
    raise TemplateSyntaxError("Tag %s takes at least 2 argument." % argv[0])

register.tag("render_menu", do_render_menu)
