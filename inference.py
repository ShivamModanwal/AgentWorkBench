"""
TaskMind AI Agent - Phase 2 compliant inference script
"""

AGENT_NAME = "TaskMind AI"
AGENT_VERSION = "1.0"
AGENT_MODE = "Autonomous Task Classification Agent"

import os
import time
import sys

from openai import OpenAI

from env.environment import AgentWorkBenchEnv
from env.tasks import TASKS
from env.models import Action, TaskCategory, TaskPriority


# =========================
# Environment
# =========================

env = AgentWorkBenchEnv()


# =========================
# LLM Client (REQUIRED)
# =========================

client = OpenAI(

    base_url=os.environ["API_BASE_URL"],

    api_key=os.environ["API_KEY"]

)

MODEL = os.environ.get("MODEL_NAME","gpt-4o-mini")


# =========================
# LLM Task Analyzer
# =========================

def analyze_task(description):

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role":"system",

                    "content":
                    """Classify this software engineering task.

Return only:
CATEGORY: BUG | FEATURE | DOCUMENTATION | DEVOPS
PRIORITY: CRITICAL | MEDIUM | LOW
"""
                },

                {
                    "role":"user",

                    "content":description
                }

            ],

            temperature=0

        )


        text = response.choices[0].message.content.lower()


        # category detection
        if "bug" in text:

            category = TaskCategory.BUG
            priority = TaskPriority.CRITICAL

        elif "feature" in text:

            category = TaskCategory.FEATURE
            priority = TaskPriority.MEDIUM

        elif "documentation" in text:

            category = TaskCategory.DOCUMENTATION
            priority = TaskPriority.LOW

        else:

            category = TaskCategory.DEVOPS
            priority = TaskPriority.CRITICAL


        return category, priority


    except Exception:

        # fallback (still valid)

        return TaskCategory.FEATURE, TaskPriority.MEDIUM


# =========================
# Task Runner
# =========================

def run_task(task):

    start = time.time()

    print(f"[START] task={task.title}", flush=True)

    try:

        env.reset()

        category, priority = analyze_task(task.description)


        action = Action(

            task_id=task.id,

            predicted_category=category,

            predicted_priority=priority,

            scheduled_position=1,

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


        return reward


    except Exception:

        print(

            f"[END] task={task.title} score=0 steps=1",

            flush=True

        )

        return 0


# =========================
# Evaluation
# =========================

def evaluate():

    print("[START] evaluation", flush=True)

    scores = []

    env.reset()

    for task in TASKS:

        reward = run_task(task)

        scores.append(reward)


    if len(scores)==0:

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

    evaluate()

    print("[END] run_complete", flush=True)

    sys.stdout.flush()


if __name__ == "__main__":

    main()
