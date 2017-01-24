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




register.filter('preview', preview)
register.filter('part', part)

