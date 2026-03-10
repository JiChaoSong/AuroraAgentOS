#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:43 
    Name  :     executor.py
    Desc  :     
--------------------------------------
"""
from aurora.tools.shell_tool import run_shell
from aurora.tools.python_tool import run_python
from aurora.tools.http_tool import run_http


class Executor:

    async def execute(self, plan):

        results = []

        for step in plan:

            if "shell:" in step:
                cmd = step.replace("shell:", "")
                result = run_shell(cmd)

            elif "python:" in step:
                code = step.replace("python:", "")
                result = run_python(code)

            elif "http:" in step:
                url = step.replace("http:", "")
                result = run_http(url)

            else:
                result = f"Skipped step: {step}"

            results.append(result)

        return results