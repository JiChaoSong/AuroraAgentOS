# AURORA AgentOS(当前：MVP阶段)

**The Dawn of Autonomous Intelligence**

AURORA AgentOS 是一个企业级分布式智能体操作系统的 MVP（最小可行产品）实现。它展示了智能体核心执行闭环：接收目标 → 规划 → 执行工具 → 反思改进 → 记忆存储，为构建可自治、可协作、可学习的企业级智能体底座奠定基础。

## ✨ 核心特性

- **目标驱动**：通过自然语言目标，自动拆解为可执行步骤。
- **多工具支持**：内置 Shell、Python、HTTP 工具调用，易于扩展。
- **记忆存储**：所有交互记录持久化，支持后续分析。
- **反思与推理**：
  - **Reflector**：评估执行结果是否达成目标，生成反思建议。
  - **Reasoner**：深度因果分析，识别计划逻辑缺陷，提供改进洞察。
- **迭代优化**：未达目标时可自动重试，结合反思重新规划，直至成功或达到最大尝试次数。
- **简单部署**：基于 FastAPI 提供 REST API，一键启动。

## 🧱 系统架构

```Plain Text
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│            Web Dashboard / SDK / Open API / CLI              │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                      API Gateway Layer                      │
│            Auth / Routing / RateLimit / Audit Log           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                    Agent Control Layer                       │
│            Agent Manager / Lifecycle / Resource              │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                      Cognitive Layer                         │
│  Planner / Reasoner / Reflector / Decision / World Model    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                       Memory Layer                           │
│        Episodic / Semantic / Procedural Memory Engine       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                      Execution Layer                         │
│  Task Orchestrator / Skill System / Tool Runtime / Swarm    │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   Infrastructure Layer                       │
│  K8s / PG / Redis / Kafka / Milvus / Neo4j / Object Storage │
└─────────────────────────────────────────────────────────────┘
```

text

- **Agent**：核心调度器，协调各模块完成闭环。
- **Planner**：调用 LLM 将目标拆解为带工具前缀的步骤。
- **Executor**：解析步骤，调用对应工具执行。
- **Tools**：具体工具实现（shell、python、http）。
- **Memory**：以 JSON 格式记录每次尝试的目标、计划、结果、反思、因果分析。
- **Reflector**：评估执行结果，判断目标是否完成，生成反思文本。
- **Reasoner**：分析计划和执行结果，提供因果分析和逻辑缺陷检测。

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 依赖：`fastapi`, `uvicorn`, `openai`, `requests`, `tomli`（或 `tomllib`，Python 3.11+ 内置）

### 安装

1. 克隆仓库
 ```bash
 https://github.com/JiChaoSong/AuroraAgentOS.git
 cd AuroraAgentOS
 ```
2. 安装依赖

 ```bash
  pip install -r requirements.txt
 ```
   
3. 配置 LLM API
 ```bash
  复制 config.toml.example 为 config.toml

  填入你的 DeepSeek / OpenAI API 密钥、Base URL 和模型名称
  
 ```
 ```toml
  [deepseek]
  API_KEY = "your-api-key"
  BASE_URL = "https://api.deepseek.com/v1"
  MODEL = "deepseek-chat"
  ```
4. 运行/启动 API 服务：


``` bash
uvicorn main:app --reload

# 服务默认运行在 http://localhost:8000。
```

5. 📡 API 使用
```txt
执行目标
端点：POST /agent/run

参数（query 参数或 JSON body）：

goal：字符串，要完成的目标（例如 "检查 Java 版本"）
```
示例请求：

```bash
curl -X POST "http://localhost:8000/agent/run?goal=检查%20Java%20版本"
```
响应示例：

```json
{
  "goal": "检查 Java 版本",
  "attempts": 1,
  "final_result": [
    "java version \"21.0.9\" 2025-10-21 LTS\nJava(TM) SE Runtime Environment ..."
  ],
  "reflection": {
    "completed": true,
    "reflection": "成功获取 Java 版本信息，目标达成。"
  },
  "causal_analysis": {
    "logical_flaws": [],
    "suggestions": [],
    "causal_analysis": "执行命令 java -version 成功返回版本信息，无异常。",
    "confidence": 1.0
  },
  "all_attempts": []
}

```
![run_example.png](https://github.com/JiChaoSong/AuroraAgentOS/blob/main/docs/assets/run_example.png?raw=true)

6. 查看记忆
```txt
端点：GET /api/memory
返回所有历史记录的列表（每行为一个 JSON 对象，实际返回数组）。
```

### 📁 项目结构

```text
aurora-agent/
├── main.py                     # FastAPI 入口
├── config.toml                 # 配置文件
├── memory.json                 # 记忆存储文件（自动生成）
├── aurora/
│   ├── agent/
│   │   └── agent.py            # Agent 核心调度器
│   ├── planner/
│   │   └── planner.py          # 规划器
│   ├── executor/
│   │   └── executor.py         # 执行器
│   ├── tools/
│   │   ├── shell_tool.py
│   │   ├── python_tool.py
│   │   └── http_tool.py
│   ├── memory/
│   │   └── memory.py           # 记忆存储
│   ├── reflector/
│   │   └── reflector.py        # 反思器
│   ├── reasoner/
│   │   └── reasoner.py         # 推理器
│   └── llm/
│       └── llm_client.py       # LLM 调用封装
```
### 🔧 自定义与扩展
```txt
添加新工具：在 aurora/tools/ 下新建工具文件，实现一个函数（如同步函数），并在 executor.py 的 execute 方法中增加对应分支（或重构为动态注册机制）。

修改 LLM 客户端：可替换 llm_client.py 中的实现，支持其他模型提供商。

调整最大重试次数：在 main.py 中实例化 Agent 时传入 max_retries 参数。
```

### 🧪 运行测试
（可选）运行单元测试：

```bash
pytest tests/
```

### 🤝 贡献指南
欢迎贡献代码、报告问题或提出新功能建议。请遵循以下步骤：

### Fork 本仓库

创建功能分支 (git checkout -b feature/amazing-feature)

提交更改 (git commit -m 'Add some amazing feature')

推送到分支 (git push origin feature/amazing-feature)

打开 Pull Request

### 📅 未来规划
集成世界模型（Neo4j 知识图谱），实现环境感知

技能系统（向量存储与复用）

多智能体协同（Agent Swarm）

任务编排（Temporal/Ray）

持续学习与自动技能生成

### 📄 许可证
MIT

### 🌟 致谢
感谢所有贡献者和开源社区的支持。