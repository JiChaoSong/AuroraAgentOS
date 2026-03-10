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

    async def create_plan(self, goal: str, context: str = ""):
        context_part = f"Previous attempt reflection: {context}\n" if context else ""
        prompt = f"""You are an AI planner. Break the goal into executable steps.
    Available tools: shell (run shell command), python (execute Python code), http (make HTTP GET request).
    Return ONLY a list of steps, each line starting with exactly one of the following prefixes:
    - "shell: " followed by the shell command
    - "python: " followed by the Python code
    - "http: " followed by the URL

    Do not include any explanations, numbering, or extra text. Only the lines with prefixes.

    {context_part}
    Goal: {goal}

    Steps:"""

        response = llm_call(prompt)

        steps = response.split("\n")

        return steps