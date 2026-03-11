#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-11 11:04 
    Name  :     python_updater.py
    Desc  :     
--------------------------------------
"""

# aurora/world/updaters/python_updater.py
async def python_updater(updater, code: str, result: dict, context: dict):
    # 记录 Tool 实体
    tool_props = {
        "name": "python",
        "code_snippet": code[:100],
        "timestamp": str(__import__('datetime').datetime.now())
    }
    updater.graph.create_entity("Tool", tool_props)

    # 如果有文件操作信息，可以从 result 中获取（需要工具返回）
    if isinstance(result, dict) and result.get("file_operations"):
        for op in result["file_operations"]:
            await updater.on_file_operation(op["path"], op["operation"])