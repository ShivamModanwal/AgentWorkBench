from inference import run_task
from env.tasks import TASKS


# =========================
# Run single task
# =========================

def run_selected_task(task_id:int):

    task = TASKS[task_id]

    result = run_task(task)

    return {

        "task": task.title,

        "description": task.description,

        "agent_output": result["agent_output"],

        "reward": result["reward"],

        "runtime": result["runtime"],

        "status": result["status"]

    }


# =========================
# Run all tasks
# =========================

def run_all_tasks():

    outputs = []

    total = 0

    for task in TASKS:

        result = run_task(task)

        total += result["reward"]

        outputs.append({

            "task":task.title,

            "reward":result["reward"],

            "status":result["status"]

        })

    avg = total / len(TASKS)

    return {

        "results":outputs,

        "average_score":round(avg,3)

    }


# =========================
# Health check (important for Docker)
# =========================

def health():

    return {

        "status":"running"

    }