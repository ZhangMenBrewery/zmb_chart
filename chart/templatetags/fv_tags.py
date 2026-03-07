# chart/templatetags/fv_tags.py
from django import template

register = template.Library()

@register.filter
def split_space(value):
    """將空格分隔的字符串分割成列表"""
    if value:
        return str(value).split()
    return []
