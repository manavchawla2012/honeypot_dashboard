from django import template
import json
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.simple_tag
def get_pages(current_page, total_pages, stix_type):
    page_list = []
    count_link = 3
    count_link = total_pages if total_pages < count_link else count_link
    if current_page == 1:
        for i in range(1, count_link + 1):
            page_list.append(i)
        page_list.append(None)
        page_list.append(total_pages)
    elif current_page != 1 and current_page != total_pages:
        if current_page - 1 != 1:
            page_list.append(1)
            if current_page - 2 != 1:
                page_list.append(None)
        page_list.append(current_page - 1)
        page_list.append(current_page)
        page_list.append(current_page + 1)
        if current_page + 1 != total_pages:
            page_list.append(None)
            page_list.append(total_pages)
    else:
        page_list.append(1)
        page_list.append(None)
        for i in range(total_pages - count_link + 1, total_pages + 1):
            page_list.append(i)
    tags = ""
    for link in page_list:
        if link:
            if link == current_page:
                is_selected = "active"
            else:
                is_selected = ""
            tags = tags + f"""<li class="page-item {is_selected}"><a class="page-link" href="?page={link}&stix_type={stix_type}">{link}</a></li>"""
        else:
            tags = tags + """<li class="page-item disabled"><a class="page-link">...</a></li>"""

    return mark_safe(tags)
