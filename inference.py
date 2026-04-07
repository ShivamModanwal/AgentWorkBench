AGENT_NAME = "TaskMind AI"
AGENT_VERSION = "1.0"
AGENT_MODE = "Autonomous Task Classification Agent"


import os
import time
from typing import Dict, List

from env.environment import AgentWorkBenchEnv
from env.tasks import TASKS
from env.models import Action, TaskCategory, TaskPriority


# =========================
# Environment
# =========================

env = AgentWorkBenchEnv()


# =========================
# Intelligent Task Analyzer
# =========================

def analyze_task(description):

    text = description.lower()

    reasoning = []
    confidence = 0.7

    # category detection
    if any(word in text for word in ["login","bug","error","fail"]):

        category = TaskCategory.BUG
        priority = TaskPriority.CRITICAL

        reasoning.append("Detected failure related keywords")

        confidence = 0.9

    elif any(word in text for word in ["feature","ui","add"]):

        category = TaskCategory.FEATURE
        priority = TaskPriority.MEDIUM

        reasoning.append("Detected feature request pattern")

        confidence = 0.85

    elif any(word in text for word in ["doc","documentation","api"]):

        category = TaskCategory.DOCUMENTATION
        priority = TaskPriority.LOW

        reasoning.append("Detected documentation keywords")

        confidence = 0.8

    elif any(word in text for word in ["production","outage","critical"]):

        category = TaskCategory.DEVOPS
        priority = TaskPriority.CRITICAL

        reasoning.append("Detected production severity indicators")

        confidence = 0.95

    else:

        category = TaskCategory.FEATURE
        priority = TaskPriority.MEDIUM

        reasoning.append("Fallback classification")

        confidence = 0.6


    return category, priority, reasoning, confidence


# =========================
# Agent confidence evaluator
# =========================

def agent_confidence_score(reward):

    if reward >= 0.9:
        return "High"

    elif reward >= 0.6:
        return "Medium"

    else:
        return "Low"


# =========================
# Agent Execution
# =========================

def run_task(task):

    start = time.time()

    try:
        env.reset()

        # AI analysis simulation
        category, priority, reasoning, confidence = analyze_task(task.description)


        action = Action(

            task_id=str(task.id),

            predicted_category=category,

            predicted_priority=priority,

            scheduled_position=getattr(task,"schedule_position",1),

            mark_complete=True
        )


        obs, reward, done, info = env.step(action)


        runtime = round(time.time()-start,2)


        explanation = f"""
AI Task Analysis Report
Task: {task.title}
Understanding:
{task.description}
Reasoning Steps:
{chr(10).join(reasoning)}
Predictions:
Category → {category}
Priority → {priority}
Confidence Score:
{round(confidence*100)}%
Performance Metrics:
Decision Confidence: {round(confidence*100)}%
Efficiency Score: {round(reward,2)}
Execution Steps: 1
Confidence Level:
{agent_confidence_score(reward)}
Decision:
Task processed and marked complete.
"""


        return {

            "task": task.title,

            "agent_output": explanation,

            "reward": reward,

            "runtime": runtime,

            "status": "SUCCESS" if reward >= 0.5 else "FAILED",

            "metrics": {

                "decision_confidence": round(confidence,2),

                "steps_used": 1,

                "efficiency_score": round(reward,2),

                "completion_rate": 1.0 if reward > 0 else 0.0

            }

        }

    except Exception as e:

        return {

            "task": task.title,

            "agent_output": "Agent execution failed",

            "reward": 0,

            "runtime": 0,

            "status": "FAILED",

            "error": str(e)

        }


# =========================
# Evaluation Runner
# =========================

def evaluate():

    scores = []

    print("\nBenchmark Evaluation Started\n")

    env.reset()   # FIX: reset once

    for task in TASKS:

        result = run_task(task)

        print(task.title,"→",result["reward"])

        scores.append(result["reward"])


    if len(scores) == 0:

        return 0


    avg = sum(scores)/len(scores)


    print("\nFinal Score:",round(avg,3))

    return avg


# =========================
# Main
# =========================

if __name__ == "__main__":

    evaluate()

    print("\nAgent Evaluation Complete")