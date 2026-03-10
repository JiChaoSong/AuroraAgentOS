#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:44 
    Name  :     llm_client.py
    Desc  :     
--------------------------------------
"""
from openai import OpenAI

from aurora.config import get_config

config = get_config()

api_key = config['deepseek']['API_KEY']
base_url = config['deepseek']['BASE_URL']
model=config['deepseek']['MODEL']

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def llm_call(prompt: str):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
