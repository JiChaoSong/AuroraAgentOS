#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:42 
    Name  :     main.py
    Desc  :     
--------------------------------------
"""
from fastapi import FastAPI
from aurora.agent.agent import Agent
from aurora.planner.planner import Planner
from aurora.executor.executor import Executor
from aurora.memory.memory import Memory
from aurora.reasoner.reasoner import Reasoner
from aurora.reflector.reflector import Reflector

app = FastAPI()

memory = Memory()
planner = Planner()
executor = Executor()
reflector = Reflector()
reasoner = Reasoner()


agent = Agent(planner, executor, memory, reflector, reasoner, max_retries=3)


@app.post("/agent/run")
async def run_agent(goal: str):
    result = await agent.run(goal)
    return {"result": result}