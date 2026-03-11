#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-11 11:04 
    Name  :     http_updater.py
    Desc  :     
--------------------------------------
"""
# aurora/world/updaters/http_updater.py
async def http_updater(updater, url: str, result: dict, context: dict):
    tool_props = {
        "name": "http",
        "url": url,
        "method": "GET",
        "status": result.get("status_code") if isinstance(result, dict) else None,
        "timestamp": str(__import__('datetime').datetime.now())
    }
    updater.graph.create_entity("Tool", tool_props)