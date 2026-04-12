from inference import run_task
from env.score_utils import clamp_score
from env.tasks import TASKS


def normalize_score(score: float) -> float:
    return clamp_score(score)


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

            "reward":float(clamp_score(0.5)),
            "score":float(clamp_score(0.5)),

            "status":"failed"

        }


    score=clamp_score(run_task(task))


    return {

        "task":task.title,

        "description":task.description,

        "reward":float(clamp_score(score)),
        "score":float(clamp_score(score)),

        "status":"completed"

    }


# =========================
# Run all tasks
# =========================

def run_all_tasks():

    outputs=[]

    total=0


    for task in TASKS:

        score=clamp_score(run_task(task))

        total+=score


        outputs.append({

            "task":task.title,

            "reward":float(clamp_score(score)),
            "score":float(clamp_score(score)),

            "status":"completed"

        })


    if len(TASKS)==0:

        avg=clamp_score(0.5)

    else:

        avg=clamp_score(total/len(TASKS))


    return {

        "results":outputs,

        "score":float(avg),

        "average_score":float(avg),

        "final_score":float(avg)

    }


# =========================
# Health check (Docker needs this)
# =========================

def health():

    return {

        "status":"running"

    }
