#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:44 
    Name  :     memory.py
    Desc  :     
--------------------------------------
"""
import json
import datetime


class Memory:

    def __init__(self):

        self.file = "memory.json"

    async def store(self, goal, plan, result, attempt=1, reflection=None, causal_analysis=None):
        data = {
            "time": str(datetime.datetime.now()),
            "attempt": attempt,
            "goal": goal,
            "plan": plan,
            "result": result,
            "reflection": reflection,
            "causal_analysis": causal_analysis
        }

        with open(self.file, "a", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")