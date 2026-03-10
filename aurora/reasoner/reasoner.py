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
import json
import re
from aurora.llm.llm_client import llm_call

class Reasoner:
    """逻辑推理器：分析目标、计划、结果，提供深度推理"""

    async def reason(self, goal: str, context: dict) -> dict:
        prompt = self._build_prompt(goal, context)
        response = llm_call(prompt)
        return self._parse_response(response)

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

    def _parse_response(self, response: str) -> dict:
        # 尝试提取 JSON（支持 Markdown 代码块和直接 JSON）
        json_str = self._extract_json(response)
        if json_str:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # 解析失败时返回一个干净的默认结构，将原始响应放入 causal_analysis 便于调试
        return {
            "logical_flaws": [],
            "suggestions": [],
            "causal_analysis": f"Failed to parse LLM response. Raw response: {response[:200]}...",
            "confidence": 0.0
        }

    def _extract_json(self, text: str) -> str | None:
        """从文本中提取 JSON 字符串（去除 Markdown 代码块标记和前后空白）"""
        # 尝试匹配 ```json ... ``` 或 ``` ... ```
        pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        # 如果没有代码块，尝试直接解析（去除首尾空白）
        stripped = text.strip()
        if stripped.startswith('{') and stripped.endswith('}'):
            return stripped
        # 最后尝试查找第一个 { 和最后一个 } 之间的内容（忽略前后文本）
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            return text[start:end+1].strip()
        return None