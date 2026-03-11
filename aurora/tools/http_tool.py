#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:45 
    Name  :     http_tool.py
    Desc  :     
--------------------------------------
"""
import requests

from aurora.tools import register_tool


@register_tool("http")
def run_http(url):

    try:
        r = requests.get(url)
        return r.text[:500]

    except Exception as e:
        return str(e)