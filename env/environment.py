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
    ALREADY_COMPLETED_REWARD = 0.02
    STEP_PENALTY = 0.02
    EFFICIENCY_BONUS = 0.2

    def __init__(self):

        self.reward_log = []
        from .tasks import TASKS

        self.tasks = TASKS

        print("Loaded tasks:", len(self.tasks))

        self._task_map = {t.id: t for t in self.tasks}

        self.max_steps = max(len(self.tasks) * 2, 1)

        self.reset()


    # =========================
    # Reward safety function
    # =========================

    def safe_reward(self,r):

        try:
            r=float(r)
        except:
            return 0.5

        if r <= 0:
            r = 0.02

        if r >= 1:
            r = 0.98

        if r < 0.02:
            r = 0.02

        if r > 0.98:
            r = 0.98

        return r


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

            return self._get_obs(), 0.02, True, {}

        self.current_step += 1

        task = self._task_map.get(str(action.task_id))

        if task is None:

            self.mistakes += 1

            return self._get_obs(), 0.02, self.done, {
                "error": "Invalid task_id"
            }


        if task.id in self.completed:

            self.mistakes += 1

            self.total_reward -= self.MISTAKE_PENALTY

            return self._get_obs(), self.ALREADY_COMPLETED_REWARD, self.done, {
                "error": "Already completed"
            }


        try:

            r = compute_reward(task, action)

            if r is None:
                r = 0.5

        except Exception as e:

            print("Reward error:", e)

            r = 0.5

            self.mistakes += 1


        # CRITICAL SAFETY FIX
        r = self.safe_reward(r)


        print("STEP:", self.current_step)
        print("TASK:", task.title)
        print("REWARD:", r)


        self.total_reward += r

        self.reward_log.append(r)

        self.total_reward -= self.STEP_PENALTY


        if action.mark_complete:

            if r > 0:

                self.completed.add(task.id)

            else:

                self.mistakes += 1


        if r > 0 and self.current_step <= len(self.tasks):

            self.total_reward += self.EFFICIENCY_BONUS


        if len(self.completed) == len(self.tasks):

            self.done = True


        if self.current_step >= self.max_steps:

            self.done = True


        obs = self._get_obs()


        info = {

            "step_reward": r,

            "total_reward": float(self.total_reward),

            "completed": len(self.completed)

        }


        # FINAL SAFETY RETURN
        r = self.safe_reward(r)


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

        # FIXED grader call
        score = grade(
            str(self.total_reward),
            str(self.mistakes)
        )

        efficiency = len(self.completed) / max(self.current_step,1)

        avg_reward = 0.5

        if len(self.reward_log) > 0:

            avg_reward = sum(self.reward_log)/len(self.reward_log)


        avg_reward = self.safe_reward(avg_reward)


        return EnvironmentState(

            total_tasks=len(self.tasks),

            completed_count=len(self.completed),

            steps_taken=self.current_step,

            mistakes=self.mistakes,

            score=self.safe_reward(score),

            avg_reward=self.safe_reward(avg_reward),

            total_reward=self.safe_reward(self.total_reward),

            efficiency=float(efficiency),

            done=self.done
       )

            total_tasks=len(self.tasks),

            completed_count=len(self.completed),

            steps_taken=self.current_step,

            mistakes=self.mistakes,

            score=round(self.safe_reward(score),3),

            avg_reward=round(avg_reward,3),

            total_reward=round(self.total_reward,3),

            efficiency=round(efficiency,2),

            done=self.done
        )
