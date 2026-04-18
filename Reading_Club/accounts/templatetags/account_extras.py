from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def display_name(user):
    if not user:
        return "Anonymous"
    return getattr(user, "nickname", None) or getattr(user, "username", None) or "Anonymous"


@register.simple_tag
def profile_link(user, css_class=""):
    if not user:
        return "Anonymous"
    name = getattr(user, "nickname", None) or getattr(user, "username", None) or "Anonymous"
    url = reverse("accounts:public_profile", kwargs={"username": user.username})
    return f'<a href="{url}" class="text-decoration-none {css_class}">{name}</a>'