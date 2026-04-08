from inference import run_task
from env.tasks import TASKS


# =========================
# Run single task
# =========================

def run_selected_task(task_id:int):

    task = TASKS[task_id]

    result = run_task(task)

    return {

        "task":task.title,

        "description":task.description,

        "agent_output":result["agent_output"],

        "reward":result["reward"],

        "runtime":result["runtime"],

        "status":result["status"]

    }


# =========================
# Run all tasks
# =========================

def run_all_tasks():

    results = []

    total = 0

    for i in range(len(TASKS)):

        result = run_selected_task(i)

        total += result["reward"]

        results.append(result)

    avg = total / len(TASKS)

    return {

        "results":results,

        "average_score":round(avg,3)

    }


# =========================
# Health check
# =========================

def health():

    return {

        "status":"running"

    }
