"""
AgentWorkBench Environment
Simulates workplace task management for AI agents.
"""

from .tasks import load_tasks
from .models import Observation, TaskObservation, EnvironmentState
from .reward import compute_reward
from .grader import grade


class AgentWorkBenchEnv:

    MISTAKE_PENALTY = 0.05
    ALREADY_COMPLETED_REWARD = -0.1
    STEP_PENALTY = 0.02
    EFFICIENCY_BONUS = 0.2

    def __init__(self):

        self.reward_log = []
        from .tasks import TASKS

        self.tasks = TASKS

        print("Loaded tasks:", len(self.tasks))   # debug

        self._task_map = {t.id: t for t in self.tasks}

        self.max_steps = max(len(self.tasks) * 2, 1)

        self.reset()

    def reset(self):

        self.current_step = 0
        self.completed = set()
        self.total_reward = 0
        self.mistakes = 0
        self.done = False
        self.reward_log = []

        obs = [TaskObservation(
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
            completed_tasks=list(self.completed)
        )

    def step(self, action):

        if self.done:

            return self._get_obs(), 0, True, {}

        self.current_step += 1

        task = self._task_map.get(str(action.task_id))

        if task is None:

            self.mistakes += 1

            return self._get_obs(), -0.1, self.done, {
                "error": "Invalid task_id"
            }

        if task.id in self.completed:

            self.mistakes += 1

            self.total_reward -= self.MISTAKE_PENALTY

            return self._get_obs(), self.ALREADY_COMPLETED_REWARD, self.done, {
                "error": "Already completed"
            }

        # compute reward safely
        try:

            r = compute_reward(task, action)

            if r is None:
                r = 0

        except Exception as e:

            print("Reward error:", e)

            r = 0

            self.mistakes += 1

        print("STEP:", self.current_step)
        print("TASK:", task.title)
        print("REWARD:", r)

        self.total_reward += r

        self.reward_log.append(r)

        self.total_reward -= self.STEP_PENALTY

        # mark complete only if reward positive
        if action.mark_complete:

            if r > 0:

                self.completed.add(task.id)

            else:

                self.mistakes += 1

        # efficiency bonus only for correct steps
        if r > 0 and self.current_step <= len(self.tasks):

            self.total_reward += self.EFFICIENCY_BONUS

        # check done
        if len(self.completed) == len(self.tasks):

            self.done = True

        if self.current_step >= self.max_steps:

            self.done = True

        obs = self._get_obs()

        info = {
            "step_reward": r,
            "total_reward": round(self.total_reward,3),
            "completed": len(self.completed)
        }

        return obs, r, self.done, info

    def _get_obs(self):

        obs = [TaskObservation(
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
            completed_tasks=list(self.completed)
        )

    def state(self):

        max_possible = max(len(self.tasks),1)

        score = grade(
            self.total_reward,
            max_possible,
            self.mistakes
        )

        efficiency = len(self.completed) / max(self.current_step,1)

        avg_reward = 0

        if len(self.reward_log) > 0:

            avg_reward = sum(self.reward_log)/len(self.reward_log)

        return EnvironmentState(

            total_tasks=len(self.tasks),

            completed_count=len(self.completed),

            steps_taken=self.current_step,

            mistakes=self.mistakes,

            score=round(score,3),

            avg_reward=round(avg_reward,3),

            total_reward=round(self.total_reward,3),

            efficiency=round(efficiency,2),

            done=self.done
        )