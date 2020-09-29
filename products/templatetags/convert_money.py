from django import template

register = template.Library()

@register.filter(name="convert_money")
def convert_cents_to_dollars(value):
    return '{0:.2f}'.format(value/100)

