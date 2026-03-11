#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:43 
    Name  :     executor.py
    Desc  :     
--------------------------------------
"""
from aurora.tools import shell_tool, python_tool, http_tool, get_tool
import logging

logger = logging.getLogger(__name__)

class Executor:

    def __init__(self, world_updater=None):
        self.world_updater = world_updater

    async def execute(self, plan):
        results = []
        for step in plan:

            # 解析步骤格式为 "tool_name: arguments"
            if ":" not in step:
                results.append(f"Invalid step format: {step}")
                continue
            tool_name, arg = step.split(":", 1)
            tool_name = tool_name.strip()
            arg = arg.strip()

            tool_func = get_tool(tool_name)
            if not tool_func:
                results.append(f"Unknown tool: {tool_name}")
                continue

            try:
                result = tool_func(arg)  # 所有工具函数统一接受字符串参数
                # 世界模型更新
                if self.world_updater:
                    await self.world_updater.update(tool_name, arg, result)

                results.append(result)

            except Exception as e:
                error_result = {"error": str(e)}
                results.append({"error": str(e)})
                # 即使工具执行异常，也可尝试更新世界模型（记录失败）
                if self.world_updater:
                    await self.world_updater.update(tool_name, arg, error_result)
        return results