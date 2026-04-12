"""
AgentWorkBench Environment
Simulates workplace task management for AI agents.
"""

from .tasks import TASKS
from .models import Observation, TaskObservation, EnvironmentState
from .reward import compute_reward
from .grader import grade


class AgentWorkBenchEnv:

    MISTAKE_PENALTY = 0.05
    ALREADY_COMPLETED_REWARD = 0.02
    STEP_PENALTY = 0.02
    EFFICIENCY_BONUS = 0.2


    def __init__(self):

        self.tasks = TASKS

        self._task_map = {t.id:t for t in self.tasks}

        self.max_steps = max(len(self.tasks)*2,1)

        self.reset()


    # =========================
    # Reward safety function
    # =========================

    def safe_reward(self,r):

        try:
            r=float(r)
        except:
            return 0.5

        # strict clamp (never edges)
        r=max(0.02,min(0.98,r))

        return r


    def build_info(self, step_reward, error=None):

        safe_step_reward = self.safe_reward(step_reward)

        info = {

            "step_reward": safe_step_reward,

            "total_reward": self.safe_reward(self.total_reward),

            "completed": len(self.completed),

            "score": safe_step_reward

        }

        if error is not None:

            info["error"] = error

        return info


    # =========================
    # Reset
    # =========================

    def reset(self):

        self.current_step=0

        self.completed=set()

        self.total_reward=0.5   # NEVER start at zero

        self.mistakes=0

        self.done=False

        self.reward_log=[]


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

            completed_tasks=list(self.completed)

        )


    # =========================
    # Step
    # =========================

    def step(self,action):

        if self.done:

            r = self.safe_reward(self.ALREADY_COMPLETED_REWARD)

            return self._get_obs(),r,True,self.build_info(
                r,
                error="Episode already finished"
            )

        self.current_step+=1


        task=self._task_map.get(str(action.task_id))


        if task is None:

            self.mistakes+=1

            r = self.safe_reward(0.02)

            return self._get_obs(),r,self.done,self.build_info(
                r,
                error="Invalid task_id"
            )


        if task.id in self.completed:

            self.mistakes+=1

            r=self.ALREADY_COMPLETED_REWARD

            r=self.safe_reward(r)

            return self._get_obs(),r,self.done,self.build_info(
                r,
                error="Already completed"
            )


        try:

            r=compute_reward(task,action)

            if r is None:

                r=0.5

        except Exception as e:

            print("Reward error:",e)

            r=0.5

            self.mistakes+=1


        # normalize reward
        r=self.safe_reward(r)


        # apply step penalty BEFORE adding
        r=self.safe_reward(r-self.STEP_PENALTY)


        self.total_reward+=r

        self.reward_log.append(r)


        if action.mark_complete:

            if r>0.05:

                self.completed.add(task.id)

            else:

                self.mistakes+=1


        # efficiency bonus
        if r>0.1 and self.current_step<=len(self.tasks):

            self.total_reward+=self.EFFICIENCY_BONUS


        if len(self.completed)==len(self.tasks):

            self.done=True


        if self.current_step>=self.max_steps:

            self.done=True


        obs=self._get_obs()


        info=self.build_info(r)


        return obs,self.safe_reward(r),self.done,info


    # =========================
    # Observation
    # =========================


    def _get_obs(self):

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

            completed_tasks=list(self.completed)

        )


    # =========================
    # State (Evaluator uses this)
    # =========================


    def state(self):

        score=grade(

            str(self.total_reward),

            str(self.mistakes)

        )

        score=self.safe_reward(score)


        avg_reward=0.5

        if len(self.reward_log)>0:

            avg_reward=sum(self.reward_log)/len(self.reward_log)


        avg_reward=self.safe_reward(avg_reward)


        efficiency=len(self.completed)/max(len(self.tasks),1)

        efficiency=self.safe_reward(efficiency)



        avg_reward = self.safe_reward(avg_reward)


        return EnvironmentState(

            total_tasks=len(self.tasks),

            completed_count=len(self.completed),

            steps_taken=self.current_step,

            mistakes=self.mistakes,

            score=score,

            avg_reward=avg_reward,

            total_reward=self.safe_reward(self.total_reward),

            efficiency=efficiency,

            done=self.done

        )
