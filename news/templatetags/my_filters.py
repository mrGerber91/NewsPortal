from django import template
import re

register = template.Library()


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Censor filter can only be applied to strings.")

    # Цензурированные слова
    censored_words = ['редиска', 'редиску', 'редиской', 'редиски']

    # Заменяем цензурированные слова
    for word in censored_words:
        # Используем регулярное выражение для замены цензурированных слов в
        # любом регистре
        value = re.sub(
            re.compile(
                re.escape(word),
                re.IGNORECASE),
            '*' * len(word),
            value)

    return value
