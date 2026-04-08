from inference import run_task
from env.tasks import TASKS


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

        score=float(score)

        total+=score


        outputs.append({

            "task":task.title,

            "reward":score,

            "status":"completed"

        })


    if len(TASKS)==0:

        avg=0.5

    else:

        avg=total/len(TASKS)


    return {

        "results":outputs,

        "average_score":round(avg,3)

    }


# =========================
# Health check (Docker needs this)
# =========================

def health():

    return {

        "status":"running"

    }