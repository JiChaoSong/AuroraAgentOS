#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 22:49 
    Name  :     reflector.py
    Desc  :     
--------------------------------------
"""

from aurora.llm.llm_client import llm_call

class Reflector:
    """评估执行结果，判断目标是否达成，并生成反思信息"""

    async def reflect(self, goal: str, plan: list, result: list, causal_analysis: str = "", world_graph=None):
        world_info = ""
        if world_graph:
            # 可查询世界模型获取额外信息，例如执行前后的状态变化
            pass
        prompt = f"""
You are an AI evaluator. Determine if the goal has been achieved based on the execution result.

Goal: {goal}
Planned steps: {plan}
Execution results: {result}
{causal_analysis if causal_analysis else ""}
{world_info}

Answer in JSON format with two fields:
- "completed": true or false
- "reflection": a brief explanation of why it succeeded or failed, and suggestions for improvement if not completed.
Only output valid JSON.
"""
        response = llm_call(prompt)
        # 解析 JSON（需处理可能的格式异常）
        import json
        try:
            eval_result = json.loads(response)
        except:
            # 解析失败时保守处理：认为未完成，并记录原始响应作为反思
            eval_result = {
                "completed": False,
                "reflection": f"Failed to parse evaluation: {response}"
            }
        # 确保字段存在
        eval_result.setdefault("completed", False)
        eval_result.setdefault("reflection", "")
        eval_result["should_retry"] = not eval_result["completed"]  # 简单策略：未完成即可重试
        return eval_result