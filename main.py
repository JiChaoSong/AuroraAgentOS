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
from aurora.world.graph_client import GraphClient
from aurora.world.updater import WorldUpdater
from aurora.config import get_config
from aurora.world.updaters.http_updater import http_updater
from aurora.world.updaters.python_updater import python_updater
from aurora.world.updaters.shell_updater import shell_updater

app = FastAPI()

config = get_config()


# 初始化记忆
memory = Memory()

# 初始化世界模型
neo4j_config = config.get('neo4j', {})
graph_client = GraphClient(
    uri=neo4j_config.get('uri', 'bolt://localhost:7687'),
    user=neo4j_config.get('user', 'neo4j'),
    password=neo4j_config.get('password', 'password'),
    database=neo4j_config.get('database', 'neo4j')
)

# 创建 WorldUpdater 实例
world_updater = WorldUpdater(graph_client)

# 注册各工具的更新器
world_updater.register_updater("shell", shell_updater)
world_updater.register_updater("python", python_updater)
world_updater.register_updater("http", http_updater)

# 初始化其他组件
planner = Planner()
executor = Executor()
reflector = Reflector()
reasoner = Reasoner()

# 创建 Agent，同时传入 world 相关（可选，供未来使用）
agent = Agent(
    planner=planner,
    executor=executor,
    memory=memory,
    reflector=reflector,
    reasoner=reasoner,
    world_graph=graph_client,  # 新增参数，以便 Planner 等可以查询
    max_retries=3
)

@app.post("/agent/run")
async def run_agent(goal: str):
    result = await agent.run(goal)
    return {"result": result}

@app.get("/api/memory")
async def get_memory():
    return memory.get_all()

# 可添加世界模型查询接口（可选）
@app.get("/world/entities")
async def list_entities(label: str = None):
    if label:
        entities = graph_client.find_entities(label)
    else:
        # 获取所有实体？需要支持多个标签，暂简化
        entities = []
    return {"entities": entities}