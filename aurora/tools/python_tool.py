#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:45 
    Name  :     python_tool.py
    Desc  :     
--------------------------------------
"""
import sys
import io
import contextlib

from aurora.tools import register_tool


@register_tool("python")
def run_python(code):
    """执行 Python 代码，返回 stdout 和 stderr（JSON 可序列化）"""
    try:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec(code)
        return {
            "success": True,
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }