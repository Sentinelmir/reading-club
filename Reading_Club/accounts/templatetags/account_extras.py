from django import template

register = template.Library()

@register.filter
def display_name(user):
    if not user:
        return "Anonymous"

    nickname = getattr(user, "nickname", None)
    if nickname:
        return nickname

    username = getattr(user, "username", None)
    if username:
        return username

    return "Anonymous"