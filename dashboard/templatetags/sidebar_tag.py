from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_sidebar_element(request, name, url, code, icon="fa-home"):
    html = f"""<li>
                    <a href="{reverse(url)}">
                        <i class="fa {icon} fa-fw"></i>
                        <span>{name}</span>
                    </a>
                </li>"""
    if not request.user.is_superuser == 1:
        try:
            permission = request.user.role.rolepermissions_set.filter(permission__codename=code)
            if permission:
                return mark_safe(html)
            else:
                return ""
        except:
            return ""
    else:
        return mark_safe(html)