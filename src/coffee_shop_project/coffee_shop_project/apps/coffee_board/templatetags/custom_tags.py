from django import template
from datetime import date

register = template.Library()

@register.simple_tag()
def date_now():
    current_date = date.today()
    return current_date.strftime("%d %B, %Y")
