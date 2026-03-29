try:

    from openai import OpenAI

    client = OpenAI()

except:

    client = None
    
import os

from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority

# Required environment variables (for submission compatibility)
API_BASE_URL = os.getenv("API_BASE_URL","")
MODEL_NAME = os.getenv("MODEL_NAME","baseline")
HF_TOKEN = os.getenv("HF_TOKEN","")

print("Running AgentWorkBench inference")

env = AgentWorkBenchEnv()

obs = env.reset()

for t in obs.tasks:

    if "login" in t.title.lower():

        category = TaskCategory.BUG
        priority = TaskPriority.CRITICAL

    elif "dark" in t.title.lower():

        category = TaskCategory.FEATURE
        priority = TaskPriority.MEDIUM

    elif "doc" in t.title.lower():

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

    obs,reward,done,info = env.step(action)

    print(f"Task {t.id} Score:", round(reward,3))


state = env.state()

print("\nFinal Score:", state.score)
print("Efficiency:", state.efficiency)