from app import run_selected_task, run_all_tasks

from fastapi import FastAPI

from fastapi.responses import JSONResponse

from env.environment import AgentWorkBenchEnv

from env.models import Action, TaskCategory, TaskPriority

import uvicorn


app = FastAPI(title="AgentWorkBench Environment")


env = AgentWorkBenchEnv()


# =========================
# Home
# =========================

@app.get("/")
def home():

    return {"message":"AgentWorkBench Environment Running"}


# =========================
# Health
# =========================

@app.get("/health")
def health():

    return {"status":"ok"}


# =========================
# Reset
# =========================

@app.post("/reset")
def reset_env():

    obs = env.reset()

    return JSONResponse(content=obs.model_dump())


# =========================
# Step
# =========================

@app.post("/step")
def step_env(action:Action):

    obs,r,done,info = env.step(action)

    return {

        "observation":obs.model_dump(),

        "reward":float(r),

        "done":done,

        "info":info

    }


# =========================
# State
# =========================

@app.get("/state")
def get_state():

    state = env.state()

    return state.model_dump()


# =========================
# Tasks
# =========================

@app.get("/tasks")
def get_tasks():

    obs = env.reset()

    return obs.model_dump()


# =========================
# Grader state
# =========================

@app.get("/grader")
def get_grader():

    state = env.state()

    return state.model_dump()


# =========================
# Baseline agent
# =========================

@app.get("/baseline")
def run_baseline():

    env.reset()

    obs = env._get_obs()

    results=[]


    for t in obs.tasks:

        title=t.title.lower()


        if "bug" in title or "fix" in title:

            category=TaskCategory.BUG
            priority=TaskPriority.CRITICAL


        elif "add" in title or "feature" in title:

            category=TaskCategory.FEATURE
            priority=TaskPriority.MEDIUM


        elif "doc" in title:

            category=TaskCategory.DOCUMENTATION
            priority=TaskPriority.LOW


        else:

            category=TaskCategory.DEVOPS
            priority=TaskPriority.MEDIUM


        action=Action(

            task_id=t.id,

            predicted_category=category,

            predicted_priority=priority,

            scheduled_position=1,

            mark_complete=True

        )


        obs,r,done,info = env.step(action)


        results.append({

            "task_id":t.id,

            "reward":round(float(r),3)

        })


    state=env.state()


    return {

        "task_results":results,

        "final_score":float(state.score),

        "efficiency":float(state.efficiency),

        "total_reward":float(state.total_reward)

    }


# =========================
# Run single task
# =========================

@app.get("/run_task/{task_id}")
def api_run_task(task_id:str):

    result=run_selected_task(task_id)

    return result


# =========================
# Run all tasks
# =========================

@app.get("/run_all")
def api_run_all():

    result=run_all_tasks()

<<<<<<< HEAD:server/app.py
    return result 

import uvicorn

=======
    return result


# =========================
# Main
# =========================
>>>>>>> 1633981 (Initial commit):api/server.py

def main():

    uvicorn.run(

<<<<<<< HEAD:server/app.py
        "server.app:app",

        host="0.0.0.0",

        port=7860
=======
        "server:app",

        host="0.0.0.0",

        port=7860,

        reload=False
>>>>>>> 1633981 (Initial commit):api/server.py

    )


<<<<<<< HEAD:server/app.py
if __name__ == "__main__":

    main()
=======
if __name__=="__main__":

    main()
>>>>>>> 1633981 (Initial commit):api/server.py
