#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:43 
    Name  :     planner.py
    Desc  :     
--------------------------------------
"""
from aurora.llm.llm_client import llm_call


class Planner:

    async def create_plan(self, goal: str, context: str = "", world_graph=None):
        context_part = f"Previous attempt reflection: {context}\n" if context else ""
        # 如果有世界模型，可以查询相关信息并加入提示词
        world_info = ""
        if world_graph:
            # 示例：查询当前目录下的文件列表（需定义如何获取当前目录）
            # 这里简化为固定查询，实际应结合 Agent 的工作目录
            files = world_graph.find_entities("File")
            if files:
                file_names = [f["properties"].get("name", "unknown") for f in files[:5]]
                world_info = f"Existing files in workspace: {', '.join(file_names)}.\n"
        prompt = f"""You are an AI planner. Break the goal into executable steps.
Available tools: shell (run shell command), python (execute Python code), http (make HTTP GET request).
Return ONLY a list of steps, each line starting with exactly one of the following prefixes:
- "shell: " followed by the shell command
- "python: " followed by the Python code
- "http: " followed by the URL

Do not include any explanations, numbering, or extra text. Only the lines with prefixes.

{world_info}
{context_part}
Goal: {goal}

Steps:"""

        response = llm_call(prompt)

        steps = response.split("\n")

        return steps