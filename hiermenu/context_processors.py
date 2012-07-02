from models import Menu


def menu(request):
    """ context_processor function to return a menu filtered with the user's
    groups permissions"""
    menus_parents = Menu.objects.filter(parent=None)
    user_groups = []
    if getattr(request, "user"):
        user_groups = request.user.groups.all()
    for menu in menus_parents:
        menu_groups = menu.groups.all()
        if menu_groups and not set(menu_groups) & set(user_groups):
            menus_parents = menus_parents.exclude(pk=menu.pk)
    return {
        'items': menus_parents,
    }
