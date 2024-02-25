from django import template
from datetime import datetime
import pytz

register = template.Library()


@register.simple_tag
def get_real_time(city='Europe/Moscow'):
    current_time = datetime.now(pytz.timezone(city))
    return current_time.strftime('%Y-%m-%d %H:%M:%S')
