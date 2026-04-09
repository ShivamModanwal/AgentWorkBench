from inference import run_task
from env.tasks import TASKS


def normalize_score(score: float) -> float:

    try:
        score = float(score)
    except Exception:
        return 0.5

    return max(0.02, min(0.98, score))


# =========================
# Run single task
# =========================

def run_selected_task(task_id:str):

    task=None

    for t in TASKS:

        if t.id==str(task_id):

            task=t

            break


    if task is None:

        return {

            "task":"unknown",

            "reward":0.5,

            "status":"failed"

        }


    score=run_task(task)
    score=normalize_score(score)


    return {

        "task":task.title,

        "description":task.description,

        "reward":float(score),

        "status":"completed"

    }


# =========================
# Run all tasks
# =========================

def run_all_tasks():

    outputs=[]

    total=0


    for task in TASKS:

        score=run_task(task)

        score=normalize_score(score)

        total+=score


        outputs.append({

            "task":task.title,

            "reward":float(score),

            "status":"completed"

        })


    if len(TASKS)==0:

        avg=0.5

    else:

        avg=normalize_score(total/len(TASKS))


    return {

        "results":outputs,

        "average_score":float(avg)

    }


# =========================
# Health check (Docker needs this)
# =========================

def health():

    return {

        "status":"running"

    }
