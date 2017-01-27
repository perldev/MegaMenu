# -*- coding: utf-8 -*-

from django import template

register = template.Library()


def preview(value):
    """Converts a string into all lowercase"""
    arr = value.split("<!-- my page break -->")

    return arr[0]

def part(value):
    """Converts a string into all lowercase"""
    arr = value.split("<!-- my page break -->")
    if len(arr)>1:
        return arr[1]
    else:
        return value

def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )

register.filter('get_range', get_range)
register.filter('preview', preview)
register.filter('part', part)

