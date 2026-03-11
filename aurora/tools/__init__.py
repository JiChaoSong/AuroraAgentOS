#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 22:41 
    Name  :     __init__.py
    Desc  :     
--------------------------------------
"""

_TOOL_REGISTRY = {}

def register_tool(name):

    def decorator(func):

        _TOOL_REGISTRY[name] = func

        return func

    return decorator

def get_tool(name):
    """根据名称获取工具函数"""
    return _TOOL_REGISTRY.get(name)

def list_tools():
    """列出所有已注册工具"""
    return list(_TOOL_REGISTRY.keys())