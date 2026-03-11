#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-11 0:20 
    Name  :     model.py
    Desc  :     实体/关系定义
--------------------------------------
"""
# 实体标签常量
ENTITY_USER = "User"
ENTITY_PROJECT = "Project"
ENTITY_FILE = "File"
ENTITY_TOOL = "Tool"
ENTITY_AGENT = "Agent"
ENTITY_TASK = "Task"

# 关系类型常量
REL_OWNS = "OWNS"
REL_CONTAINS = "CONTAINS"
REL_DEPENDS_ON = "DEPENDS_ON"
REL_EXECUTED_BY = "EXECUTED_BY"
REL_CREATED = "CREATED"
REL_MODIFIED = "MODIFIED"
REL_READ = "READ"

# 实体的属性名可自由定义，这里只做规范