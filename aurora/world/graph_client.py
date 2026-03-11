#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-11 0:20 
    Name  :     graph_client.py
    Desc  :     Neo4j 操作封装
--------------------------------------
"""
from neo4j import GraphDatabase
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class GraphClient:
    """Neo4j 图数据库客户端"""

    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def _run_query(self, query: str, parameters: Dict[str, Any] = None):
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    # ---------- 实体操作 ----------
    def create_entity(self, label: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """创建单个实体，返回实体及其内部ID"""
        query = f"CREATE (n:{label} $props) RETURN n, id(n) as id"
        params = {"props": properties}
        result = self._run_query(query, params)
        if result:
            return {"id": result[0]["id"], "properties": result[0]["n"]}
        return None

    def get_entity(self, label: str, entity_id: int) -> Optional[Dict[str, Any]]:
        """通过内部ID获取实体"""
        query = f"MATCH (n:{label}) WHERE id(n) = $id RETURN n, id(n) as id"
        params = {"id": entity_id}
        result = self._run_query(query, params)
        if result:
            return {"id": result[0]["id"], "properties": result[0]["n"]}
        return None

    def find_entities(self, label: str, conditions: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """根据属性条件查询实体，conditions 为属性键值对"""
        query = f"MATCH (n:{label}) "
        params = {}
        if conditions:
            clauses = [f"n.{k} = ${k}" for k in conditions]
            query += "WHERE " + " AND ".join(clauses)
            params.update(conditions)
        query += " RETURN n, id(n) as id"
        result = self._run_query(query, params)
        return [{"id": rec["id"], "properties": rec["n"]} for rec in result]

    def update_entity(self, label: str, entity_id: int, properties: Dict[str, Any]) -> bool:
        """更新实体属性（覆盖）"""
        query = f"MATCH (n:{label}) WHERE id(n) = $id SET n = $props RETURN n"
        params = {"id": entity_id, "props": properties}
        result = self._run_query(query, params)
        return len(result) > 0

    def delete_entity(self, label: str, entity_id: int) -> bool:
        """删除实体及其所有关系"""
        query = f"MATCH (n:{label}) WHERE id(n) = $id DETACH DELETE n"
        params = {"id": entity_id}
        self._run_query(query, params)
        return True  # neo4j 不会返回删除计数，默认成功

    # ---------- 关系操作 ----------
    def create_relationship(self, from_id: int, to_id: int, rel_type: str, properties: Dict[str, Any] = None):
        """创建两个实体间的关系"""
        query = f"""
        MATCH (a) WHERE id(a) = $from_id
        MATCH (b) WHERE id(b) = $to_id
        CREATE (a)-[r:{rel_type} $props]->(b)
        RETURN r
        """
        params = {"from_id": from_id, "to_id": to_id, "props": properties or {}}
        result = self._run_query(query, params)
        return len(result) > 0

    def get_relationships(self, entity_id: int, direction: str = "both", rel_types: List[str] = None):
        """获取实体的所有关系（可选指定方向和类型）"""
        # direction: "out", "in", "both"
        if rel_types:
            rel_pattern = "|".join(rel_types)
        else:
            rel_pattern = ""
        if direction == "out":
            query = f"MATCH (n)-[r:{rel_pattern}]->(m) WHERE id(n) = $id RETURN r, id(m) as target_id"
        elif direction == "in":
            query = f"MATCH (n)<-[r:{rel_pattern}]-(m) WHERE id(n) = $id RETURN r, id(m) as source_id"
        else:
            query = f"MATCH (n)-[r:{rel_pattern}]-(m) WHERE id(n) = $id RETURN r, id(m) as other_id"
        params = {"id": entity_id}
        result = self._run_query(query, params)
        return result