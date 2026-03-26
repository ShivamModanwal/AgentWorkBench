"""
AgentWorkBench Environment

Simulates workplace task management for AI agents.
Implements OpenEnv interface:
reset(), step(), state()
"""
from .tasks import load_tasks
from .models import Observation,TaskObservation,EnvironmentState
from .reward import compute_reward
from .grader import grade

class AgentWorkBenchEnv:

    # Reward constants
    MISTAKE_PENALTY = 0.05
    ALREADY_COMPLETED_REWARD = -0.1
    STEP_PENALTY = 0.02
    EFFICIENCY_BONUS = 0.2

    def __init__(self):

        self.reward_log = []
        self.tasks = load_tasks()
        self._task_map = {t.id: t for t in self.tasks}  # O(1) task lookup
        self.max_steps = len(self.tasks) * 2
        self.reset()

    def reset(self):

        self.current_step = 0
        self.completed = set()  # Use set for O(1) membership testing
        self.total_reward = 0
        self.mistakes = 0
        self.done = False

        obs=[TaskObservation(
            id=t.id,
            title=t.title,
            description=t.description,
            difficulty=t.difficulty,
            estimated_steps=t.estimated_steps,
            deadline=t.deadline
        ) for t in self.tasks]

        return Observation(
            tasks=obs,
            current_step=0,
            max_steps=self.max_steps,
            completed_tasks=[]
        )

    def step(self, action):

        if self.done:
            return self._get_obs(), 0, True, {}

        self.current_step += 1

        task = self._task_map.get(action.task_id)

        if task is None:
            return self._get_obs(), 0, self.done, {"error": "Invalid task_id"}

        if task.id in self.completed:

            self.mistakes += 1
            self.total_reward -= self.MISTAKE_PENALTY

            return self._get_obs(), self.ALREADY_COMPLETED_REWARD, self.done, {"error": "Task already completed"}

        r = compute_reward(task, action)

        self.total_reward += r
        self.reward_log.append(r)

        # step efficiency penalty
        self.total_reward -= self.STEP_PENALTY

        if action.mark_complete:

            self.completed.add(task.id)

        if len(self.completed) == len(self.tasks):

            self.done = True

        # efficiency bonus
        if self.current_step <= len(self.tasks):

            self.total_reward += self.EFFICIENCY_BONUS

        elif self.current_step >= self.max_steps:

            self.done = True

        obs = self._get_obs()

        info = {"reward": r}

        return obs, r, self.done, info

    def _get_obs(self):

        from .models import TaskObservation,Observation

        obs=[TaskObservation(
            id=t.id,
            title=t.title,
            description=t.description,
            difficulty=t.difficulty,
            estimated_steps=t.estimated_steps,
            deadline=t.deadline
        ) for t in self.tasks]

        return Observation(
            tasks=obs,
            current_step=self.current_step,
            max_steps=self.max_steps,
            completed_tasks=self.completed
        )
    def state(self):

        from .models import EnvironmentState

        max_possible = len(self.tasks)

        from .grader import grade
        
        score = grade(self.total_reward, max_possible, self.mistakes)
        
        efficiency = len(self.tasks) / max(self.current_step,1)

        avg_reward = 0

        if len(self.reward_log) > 0:

            avg_reward = sum(self.reward_log)/len(self.reward_log)
        
        return EnvironmentState(

            total_tasks=len(self.tasks),

            completed_count=len(self.completed),

            steps_taken=self.current_step,

            mistakes=self.mistakes,

            score=score,

            avg_reward=round(avg_reward,3),

            total_reward=round(self.total_reward,3),

            efficiency=round(efficiency,2),

            done=self.done
        )