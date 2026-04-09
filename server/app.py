from app import run_selected_task, run_all_tasks
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority
import uvicorn

app = FastAPI(title="AgentWorkBench Environment")
env = AgentWorkBenchEnv()

# =========================
# Security Guard for Scores
# =========================
def clamp_score(val):
    """Ensures no score leaves the API as exactly 0.0 or 1.0"""
    try:
        return max(0.01, min(0.99, float(val)))
    except:
        return 0.5

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
        "reward": clamp_score(r),  # Guarded
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
    state_dict = env.state().model_dump()
    
    # Explicitly guard any score fields in the state dump
    for key in ["score", "total_reward", "efficiency"]:
        if key in state_dict:
            state_dict[key] = clamp_score(state_dict[key])
            
    # Guard individual task scores if present
    if "task_results" in state_dict and isinstance(state_dict["task_results"], list):
        for task in state_dict["task_results"]:
            for k in ["reward", "score"]:
                if k in task:
                    task[k] = clamp_score(task[k])
                    
    return state_dict

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
            "reward": clamp_score(r) # Guarded
        })
        
    state=env.state()
    return {
        "task_results":results,
        "final_score": clamp_score(state.score),       # Guarded
        "efficiency": clamp_score(state.efficiency),     # Guarded
        "total_reward": clamp_score(state.total_reward)  # Guarded
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
    return result

# =========================
# Main
# =========================
def main():
    uvicorn.run(
<<<<<<< HEAD
        "server:app",
=======

        "server.app:app",

>>>>>>> c67467c (Fix OpenEnv score range metadata and app entrypoints)
        host="0.0.0.0",
        port=7860,
        reload=False
    )

if __name__=="__main__":
<<<<<<< HEAD
=======

>>>>>>> c67467c (Fix OpenEnv score range metadata and app entrypoints)
    main()
