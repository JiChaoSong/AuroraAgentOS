#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 23:13 
    Name  :     reasoner.py
    Desc  :     
--------------------------------------
"""
# aurora/reasoner/reasoner.py
from aurora.llm.llm_client import llm_call
import json

class Reasoner:
    """逻辑推理器：分析目标、计划、结果，提供深度推理"""

    async def reason(self, goal: str, context: dict) -> dict:
        """
        参数 context 可包含：
        - plan: list, 当前计划（如果有）
        - result: list, 执行结果（如果有）
        - reflection: str, 上一轮反思（如果有）
        - world_state: dict, 世界模型状态（预留）
        返回推理结论，格式示例：
        {
            "logical_flaws": [...],          # 逻辑缺陷列表
            "suggestions": [...],             # 改进建议
            "causal_analysis": str,            # 因果分析
            "confidence": float                # 置信度
        }
        """
        # 构造提示词，要求 LLM 进行结构化推理
        prompt = self._build_prompt(goal, context)
        response = llm_call(prompt)
        # 解析 JSON（需容错）
        try:
            result = json.loads(response)
        except:
            result = {
                "logical_flaws": [],
                "suggestions": ["无法解析推理结果，请检查 LLM 输出"],
                "causal_analysis": "",
                "confidence": 0.0
            }
        return result

    def _build_prompt(self, goal: str, context: dict) -> str:
        prompt = f"""You are an AI reasoner. Perform deep logical reasoning and causal analysis based on the given goal and context.

Goal: {goal}

"""
        if "plan" in context:
            prompt += f"Current plan: {context['plan']}\n"
        if "result" in context:
            prompt += f"Execution result: {context['result']}\n"
        if "reflection" in context:
            prompt += f"Previous reflection: {context['reflection']}\n"

        prompt += """
Analyze the situation and output a JSON object with the following fields:
- "logical_flaws": list of strings, any logical issues in the plan or execution (empty if none)
- "suggestions": list of strings, actionable suggestions to improve the plan or achieve the goal
- "causal_analysis": string, explanation of why success/failure occurred
- "confidence": float between 0 and 1, your confidence in this analysis

Only output valid JSON, no other text.
"""
        return prompt