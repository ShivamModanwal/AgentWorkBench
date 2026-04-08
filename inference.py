"""
TaskMind AI Agent - HTTP-based inference script
"""

AGENT_NAME = "TaskMind AI"
AGENT_VERSION = "1.0"
AGENT_MODE = "Autonomous Task Classification Agent"

import time
import sys

from env.environment import AgentWorkBenchEnv
from env.tasks import TASKS
from env.models import Action, TaskCategory, TaskPriority


env = AgentWorkBenchEnv()


# =========================
# Intelligent Task Analyzer
# =========================

def analyze_task(description):

    text = description.lower()

    reasoning = []
    confidence = 0.7

    if any(word in text for word in ["login","bug","error","fail"]):

        category = TaskCategory.BUG
        priority = TaskPriority.CRITICAL

        confidence = 0.9

    elif any(word in text for word in ["feature","ui","add"]):

        category = TaskCategory.FEATURE
        priority = TaskPriority.MEDIUM

        confidence = 0.85

    elif any(word in text for word in ["doc","documentation","api"]):

        category = TaskCategory.DOCUMENTATION
        priority = TaskPriority.LOW

        confidence = 0.8

    elif any(word in text for word in ["production","outage","critical"]):

        category = TaskCategory.DEVOPS
        priority = TaskPriority.CRITICAL

        confidence = 0.95

    else:

        category = TaskCategory.FEATURE
        priority = TaskPriority.MEDIUM

        confidence = 0.6


    return category, priority, confidence


# =========================
# Agent Execution
# =========================

def run_task(task):

    start = time.time()

    try:

        print(f"[START] task={task.title}", flush=True)

        env.reset()

        category, priority, confidence = analyze_task(task.description)


        action = Action(

            task_id=task.id,

            predicted_category=category,

            predicted_priority=priority,

            scheduled_position=getattr(task,"schedule_position",1),

            mark_complete=True

        )


        obs, reward, done, info = env.step(action)


        print(
            f"[STEP] task={task.title} step=1 reward={round(reward,3)}",
            flush=True
        )


        runtime = round(time.time()-start,2)


        print(
            f"[END] task={task.title} score={round(reward,3)} steps=1",
            flush=True
        )


        return {

            "task":task.title,

            "reward":reward,

            "runtime":runtime,

            "status":"SUCCESS" if reward >= 0.5 else "FAILED"

        }


    except Exception:

        print(
            f"[END] task={task.title} score=0 steps=1",
            flush=True
        )

        return {

            "task":task.title,

            "reward":0,

            "status":"FAILED"

        }


# =========================
# Evaluation Runner
# =========================

def evaluate():

    print("[START] evaluation", flush=True)

    scores = []

    env.reset()

    for task in TASKS:

        result = run_task(task)

        scores.append(result["reward"])


    if len(scores) == 0:

        print("[END] evaluation score=0 steps=0", flush=True)

        return 0


    avg = sum(scores)/len(scores)


    print(
        f"[END] evaluation score={round(avg,3)} steps={len(TASKS)}",
        flush=True
    )

    return avg

# =========================
# Main Entrypoint
# =========================

def main():

    print("[START] evaluation", flush=True)

    evaluate()

    print("[END] evaluation_complete", flush=True)


if __name__ == "__main__":

    main()
