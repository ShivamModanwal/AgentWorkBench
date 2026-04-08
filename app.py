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

<<<<<<< HEAD
        "agent_output":result["agent_output"],

        "reward":result["reward"],

        "runtime":result["runtime"],

        "status":result["status"]
=======
        "reward":float(score),

        "status":"completed"
>>>>>>> 1633981 (Initial commit)

    }


# =========================
# Run all tasks
# =========================

def run_all_tasks():

<<<<<<< HEAD
    results = []
=======
    outputs=[]

    total=0
>>>>>>> 1633981 (Initial commit)


    for i in range(len(TASKS)):

<<<<<<< HEAD
        result = run_selected_task(i)
=======
        score=run_task(task)

        score=float(score)

        total+=score
>>>>>>> 1633981 (Initial commit)


<<<<<<< HEAD
        results.append(result)
=======
        outputs.append({

            "task":task.title,

            "reward":score,

            "status":"completed"

        })
>>>>>>> 1633981 (Initial commit)


    if len(TASKS)==0:

        avg=0.5

    else:

        avg=total/len(TASKS)


    return {

        "results":results,

        "average_score":round(avg,3)

    }


# =========================
<<<<<<< HEAD
# Health check
=======
# Health check (Docker needs this)
>>>>>>> 1633981 (Initial commit)
# =========================

def health():

    return {

        "status":"running"

    }
