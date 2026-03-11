#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-11 0:21 
    Name  :     updater.py
    Desc  :     自动更新钩子
--------------------------------------
"""
from typing import Dict, Callable, Any

from aurora.world.graph_client import GraphClient
from aurora.world import model
import os
import hashlib
import logging

logger = logging.getLogger(__name__)

class WorldUpdater:
    """根据工具执行结果更新世界模型"""

    def __init__(self, graph_client: GraphClient):
        self.graph = graph_client
        self._updaters: Dict[str, Callable] = {}

    def register_updater(self, tool_name: str, updater_func: Callable):
        """注册某个工具对应的世界模型更新器"""
        self._updaters[tool_name] = updater_func
        logger.info(f"Registered world updater for tool: {tool_name}")

    async def update(self, tool_name: str, arg: str, result: Any, context: dict = None):
        """执行工具后调用，根据工具名称分发到对应的更新器"""
        updater = self._updaters.get(tool_name)
        if updater:
            try:
                await updater(self, arg, result, context or {})
            except Exception as e:
                logger.error(f"World updater for tool '{tool_name}' failed: {e}")
        else:
            logger.warning(f"No world updater registered for tool: {tool_name}")