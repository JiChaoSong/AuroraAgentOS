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
        print(f'data: {data}')

        with open(self.file, "a", encoding='utf-8') as f:
            f.write(json.dumps(data) + "\n")

    def get_all(self):
        """读取 memory.json 中的所有记录，返回列表"""
        records = []
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
        except FileNotFoundError:
            pass  # 文件不存在时返回空列表
        return records