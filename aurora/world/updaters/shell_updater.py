#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-11 11:04 
    Name  :     shell_updater.py
    Desc  :     
--------------------------------------
"""
async def shell_updater(updater, command: str, result: dict, context: dict):
    """处理 shell 命令执行后的世界模型更新"""
    # 记录 Tool 实体
    tool_props = {
        "name": "shell",
        "command": command,
        "timestamp": str(__import__('datetime').datetime.now())
    }
    updater.graph.create_entity("Tool", tool_props)

    # 尝试从命令中解析文件操作（示例：检测 echo > file）
    if ">" in command and ("echo" in command or "type" in command):
        # 简单提取文件名，实际应更严谨
        parts = command.split(">")
        if len(parts) > 1:
            file_path = parts[1].strip()
            # 调用文件操作更新
            await updater.on_file_operation(file_path, "create_or_write")