from django import template
import requests
import json
from datetime import datetime
from frontend.common import common as mcm
from frontend.common import constant as mcs
import textwrap
import collections
import re

register = template.Library()

@register.inclusion_tag('pdfgeneration/style.html', takes_context=True)
def get_exportorders_style(context):
    # request = context.dicts[1]['request']

    page_size = 'A4'  # 21 * 29.7
    page_width = 29.7
    page_height = 21
    page_orientation = 'landscape'

    styleconext = {}
    styleconext['page_size'] = page_size
    styleconext['page_orientation'] = page_orientation
    styleconext['pagesize'] = '%s %s' % (styleconext['page_size'], styleconext['page_orientation'])
    styleconext['margin_left'] = 0.6
    styleconext['margin_right'] = 0.6
    styleconext['margin_top'] = 0.8
    styleconext['margin_height'] = page_height - styleconext['margin_top'] - 0.5
    styleconext['margin_width'] = page_width - styleconext['margin_left'] - styleconext['margin_right']
    return styleconext

@register.inclusion_tag('pdfgeneration/exportorders.html', takes_context=True)
def exportorders(context):
    headerinfo = [
        {'field': 'no', 'fieldAlias': 'No'},
        {'field': 'username', 'fieldAlias': 'User'},
        {'field': 'service_name', 'fieldAlias': 'Service'},
        {'field': 'description', 'fieldAlias': 'Description'},
        {'field': 'price', 'fieldAlias': 'Price'},
        {'field': 'paid_price', 'fieldAlias': 'Paid Price'},
        {'field': 'service_status_name', 'fieldAlias': 'Service Status'},
        {'field': 'date_booked', 'fieldAlias': 'Date Booked'},
        {'field': 'date_created', 'fieldAlias': 'Date Created'},
    ]

    return {
        'headers': headerinfo,
        'orders': context["param"],
        'export_from': context["export_from"],
        'export_to': context["export_to"],
        'logo_url': "/static/img/logo.png"
    }

