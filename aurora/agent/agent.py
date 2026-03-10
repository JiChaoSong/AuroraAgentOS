#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:43 
    Name  :     agent.py
    Desc  :     Agent 核心调度器，集成 Planner、Executor、Memory、Reflector、Reasoner
--------------------------------------
"""
class Agent:

    def __init__(self, planner, executor, memory, reflector, reasoner, max_retries = 3):
        self.planner = planner
        self.executor = executor
        self.memory = memory
        self.reflector = reflector
        self.reasoner = reasoner
        self.max_retries = max_retries

    async def run(self, goal: str):
        attempt = 0
        context = ""  # 反思上下文
        all_results = []  # 记录所有尝试

        # 初始化变量，确保作用域覆盖
        plan = None
        result = None
        reflection = None
        causal_analysis = None

        while attempt < self.max_retries:
            attempt += 1
            print(f"Attempt {attempt} for goal: {goal}")

            # 1. 规划
            plan = await self.planner.create_plan(goal, context=context)
            print("Plan:", plan)

            # 2. 规划后推理（可选，此处仅打印缺陷，不修改计划）
            plan_context = {"plan": plan}
            reason_result = await self.reasoner.reason(goal, plan_context)
            if reason_result.get("logical_flaws"):
                print("Logical flaws detected:", reason_result["logical_flaws"])
            # 可将 reason_result 存入某处，但当前不存储

            # 3. 执行
            result = await self.executor.execute(plan)
            print("Execution result:", result)

            # 4. 执行后推理（因果分析）
            exec_context = {"plan": plan, "result": result}
            causal_analysis = await self.reasoner.reason(goal, exec_context)
            print("Causal analysis:", causal_analysis)

            # 5. 反思（结合因果分析）
            reflection = await self.reflector.reflect(
                goal, plan, result,
                causal_analysis=causal_analysis.get("causal_analysis", "")
            )
            print("Reflection:", reflection)

            # 6. 存储本轮记录
            await self.memory.store(
                goal, plan, result,
                attempt=attempt,
                reflection=reflection,
                causal_analysis=causal_analysis
            )

            # 7. 判断是否完成
            if reflection.get("completed"):
                print("Goal achieved!")
                return self._build_final_output(
                    goal, attempt, result, reflection, all_results, causal_analysis
                )
            else:
                # 未完成，更新上下文，并记录本轮结果
                context = reflection.get("reflection", "")
                all_results.append({
                    "attempt": attempt,
                    "plan": plan,
                    "result": result,
                    "reflection": reflection,
                    "causal_analysis": causal_analysis
                })
                # 继续循环

        # 达到最大重试次数
        final_reflection = {"completed": False, "reflection": "Max retries reached, goal not achieved."}
        return self._build_final_output(
            goal, attempt, result, final_reflection, all_results, causal_analysis
        )

    @staticmethod
    def _build_final_output(goal, attempts, final_result, reflection, all_results, causal_analysis):
        """构造统一的最终输出格式"""
        return {
            "goal": goal,
            "attempts": attempts,
            "final_result": final_result,
            "reflection": reflection,
            "causal_analysis": causal_analysis,
            "all_attempts": all_results
        }