from app import run_selected_task, run_all_tasks
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority
from env.score_utils import clamp_score
import uvicorn

app = FastAPI(title="AgentWorkBench Environment")
env = AgentWorkBenchEnv()

# =======================================================
# THE ULTIMATE SAFEGUARD: Recursive Clamper
# Yeh function JSON ke kisi bhi kone se score dhoondh kar lock kar dega
# =======================================================
def deep_clamp_scores(obj):
    if isinstance(obj, dict):
        clamped_dict = {}
        for key, value in obj.items():
            k_str = str(key).lower()
            # Agar key ke naam mein yeh words hain, toh uski value clamp hogi
            is_score_key = any(x in k_str for x in ["score", "reward", "efficiency", "penalty", "bonus", "result"])
            
            if isinstance(value, (dict, list)):
                clamped_dict[key] = deep_clamp_scores(value)
            elif is_score_key and isinstance(value, (int, float)):
                try:
                    clamped_dict[key] = float(clamp_score(value))
                except Exception:
                    clamped_dict[key] = 0.5
            else:
                clamped_dict[key] = value
        return clamped_dict
    elif isinstance(obj, list):
        return [deep_clamp_scores(item) for item in obj]
    return obj


def build_task_results():
    grader_env = AgentWorkBenchEnv()
    grader_env.reset()
    results = []

    for task in grader_env.tasks:
        title = task.title.lower()

        if "bug" in title or "fix" in title:
            category = TaskCategory.BUG
            priority = TaskPriority.CRITICAL
        elif "add" in title or "feature" in title:
            category = TaskCategory.FEATURE
            priority = TaskPriority.MEDIUM
        elif "doc" in title:
            category = TaskCategory.DOCUMENTATION
            priority = TaskPriority.LOW
        else:
            category = TaskCategory.DEVOPS
            priority = TaskPriority.CRITICAL

        action = Action(
            task_id=task.id,
            predicted_category=category,
            predicted_priority=priority,
            scheduled_position=getattr(task, "schedule_position", 1),
            mark_complete=True
        )

        _, reward, _, _ = grader_env.step(action)
        results.append({
            "task_id": task.id,
            "reward": reward,
            "score": reward
        })

    state = grader_env.state()

    return {
        "task_results": results,
        "score": state.score,
        "final_score": state.score,
        "efficiency": state.efficiency,
        "total_reward": state.total_reward,
    }


# =========================
# Home & Health
# =========================
@app.get("/")
def home():
    return {"message":"AgentWorkBench Environment Running"}

@app.get("/health")
def health():
    return {"status":"ok"}

# =========================
# Reset
# =========================
@app.post("/reset")
def reset_env():
    obs = env.reset()
    # Pura JSON response deep_clamp se guzrega
    return JSONResponse(content=deep_clamp_scores(obs.model_dump()))

# =========================
# Step
# =========================
@app.post("/step")
def step_env(action:Action):
    obs, r, done, info = env.step(action)
    raw_response = {
        "observation": obs.model_dump(),
        "reward": r,
        "score": r,
        "done": done,
        "info": {
            "step_reward": r,
            "score": r,
            "total_reward": getattr(env, "total_reward", 0.5),
            "completed": len(getattr(env, "completed", [])),
            **(info if isinstance(info, dict) else {}),
        }
    }
    return deep_clamp_scores(raw_response)

# =========================
# State
# =========================
@app.get("/state")
def get_state():
    state_payload = env.state().model_dump()
    state_payload["task_results"] = build_task_results()["task_results"]
    return deep_clamp_scores(state_payload)

# =========================
# Tasks
# =========================
@app.get("/tasks")
def get_tasks():
    task_env = AgentWorkBenchEnv()
    obs = task_env.reset()
    return deep_clamp_scores(obs.model_dump())

# =========================
# Grader state
# =========================
@app.get("/grader")
def get_grader():
    return deep_clamp_scores(build_task_results())

# =========================
# Baseline agent
# =========================
@app.get("/baseline")
def run_baseline():
    return deep_clamp_scores(build_task_results())

# =========================
# Run single task
# =========================
@app.get("/run_task/{task_id}")
def api_run_task(task_id:str):
    result = run_selected_task(task_id)
    # THE FIX: Ab yahan se dictionary bina clamp huye nahi jayegi
    return deep_clamp_scores(result)

# =========================
# Run all tasks
# =========================
@app.get("/run_all")
def api_run_all():
    result = run_all_tasks()
    # THE FIX: Yahan bhi clamp lag gaya!
    return deep_clamp_scores(result)

# =========================
# Main
# =========================
def main():
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False
    )

if __name__=="__main__":
    main()
