#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:45 
    Name  :     shell_tool.py
    Desc  :     
--------------------------------------
"""
import subprocess


def run_shell(cmd):

    try:
        # 使用 run 捕获 stdout 和 stderr，设置 text=True 直接返回字符串
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30          # 防止命令卡死
        )
        # 合并 stdout 和 stderr（通常 stderr 包含版本信息）
        output = result.stdout + result.stderr
        # 如果确实没有任何输出（比如命令只设置了退出码），至少返回一条提示
        return output if output else f"Command executed with exit code {result.returncode}"
    except subprocess.TimeoutExpired as e:
        return f"Timeout: {str(e)}"
    except Exception as e:
        return str(e)