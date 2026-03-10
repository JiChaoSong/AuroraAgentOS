#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:45 
    Name  :     python_tool.py
    Desc  :     
--------------------------------------
"""
def run_python(code):

    try:

        local_vars = {}

        exec(code, {}, local_vars)

        return local_vars

    except Exception as e:
        return str(e)