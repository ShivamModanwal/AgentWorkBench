from fastapi import FastAPI
from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority

app = FastAPI(title="AgentWorkBench Environment")

env = AgentWorkBenchEnv()


@app.get("/")
def home():

    return {"message":"AgentWorkBench Environment Running"}


@app.get("/health")
def health():

    return {"status":"ok"}


@app.post("/reset")
def reset_env():

    obs = env.reset()
    return obs.model_dump()
    

@app.post("/step")
def step_env(action: Action):

    obs,r,done,info = env.step(action)

    return {

        "observation":obs.model_dump(),

        "reward":r,

        "done":done,

        "info":info

    }


@app.get("/state")
def get_state():

    state = env.state()

    return state.model_dump()


@app.get("/tasks")
def get_tasks():

    obs = env.reset()

    return obs.model_dump()


@app.get("/grader")
def get_grader():

    state = env.state()

    return state.model_dump()


@app.get("/baseline")
def run_baseline():

    obs = env.reset()

    results = []

    for t in obs.tasks:

        if "bug" in t.title.lower():

            category = TaskCategory.BUG
            priority = TaskPriority.CRITICAL

        elif "add" in t.title.lower():

            category = TaskCategory.FEATURE
            priority = TaskPriority.MEDIUM

        elif "docs" in t.title.lower():

            category = TaskCategory.DOCUMENTATION
            priority = TaskPriority.LOW

        else:

            category = TaskCategory.DEVOPS
            priority = TaskPriority.CRITICAL


        action = Action(

            task_id=t.id,

            predicted_category=category,

            predicted_priority=priority,

            scheduled_position=1,

            mark_complete=True
        )

        obs,r,done,info = env.step(action)

        results.append({

            "task_id":t.id,

            "reward":round(r,3)

        })


    state = env.state()

    return {

        "task_results":results,

        "final_score":state.score,

        "efficiency":state.efficiency,

        "total_reward":state.total_reward
    }
