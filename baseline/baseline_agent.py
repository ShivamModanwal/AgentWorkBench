"""
Baseline agent.

Simple deterministic rule-based agent.
Used only for benchmarking environment behavior.

"""
from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority

print("\nBASELINE AGENT RUNNING\n")

env = AgentWorkBenchEnv()

obs = env.reset()

task_scores = []

for t in obs.tasks:

    # simple rule based baseline
    if "bug" in t.title.lower():

        category = TaskCategory.BUG
        priority = TaskPriority.CRITICAL

    elif "feature" in t.title.lower() or "add" in t.title.lower():

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

    obs, reward, done, info = env.step(action)

    task_scores.append(reward)

    print(f"Task {t.id} Score: {round(reward,3)}")


state = env.state()

print("\nFINAL RESULTS")

print("Total Tasks:", state.total_tasks)
print("Completed:", state.completed_count)
print("Steps:", state.steps_taken)
print("Mistakes:", state.mistakes)

print("\nFinal Score:", state.score)

print("Efficiency:", state.efficiency)

print("Total Reward:", state.total_reward)

print("\nBASELINE COMPLETE")