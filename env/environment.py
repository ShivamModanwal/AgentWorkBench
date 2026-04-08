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

<<<<<<< HEAD
        print("Loaded tasks:", len(self.tasks))
=======
        print("Loaded tasks:",len(self.tasks))
>>>>>>> 1633981 (Initial commit)

        self._task_map = {t.id:t for t in self.tasks}

        self.max_steps = max(len(self.tasks)*2,1)

        self.reset()


    # =========================
<<<<<<< HEAD
    # Reward safety function
=======
    # Reward safety
>>>>>>> 1633981 (Initial commit)
    # =========================

    def safe_reward(self,r):

        try:
            r=float(r)
<<<<<<< HEAD
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
=======

        except:
            return 0.5


        # strict clamp (never edges)
        r=max(0.02,min(0.98,r))
>>>>>>> 1633981 (Initial commit)

        return r


<<<<<<< HEAD
=======
    # =========================
    # Reset
    # =========================

>>>>>>> 1633981 (Initial commit)
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


<<<<<<< HEAD
    def step(self, action):

        if self.done:

            return self._get_obs(), 0.02, True, {}
=======
    # =========================
    # Step
    # =========================

    def step(self,action):

        if self.done:

            return self._get_obs(),0.02,True,{}
>>>>>>> 1633981 (Initial commit)


        self.current_step+=1


        task=self._task_map.get(str(action.task_id))


        if task is None:

            self.mistakes+=1

            return self._get_obs(),0.02,self.done,{

                "error":"Invalid task_id",

                "score":0.02

<<<<<<< HEAD
            return self._get_obs(), 0.02, self.done, {
                "error": "Invalid task_id"
=======
>>>>>>> 1633981 (Initial commit)
            }


        if task.id in self.completed:

            self.mistakes+=1

            r=self.ALREADY_COMPLETED_REWARD

            r=self.safe_reward(r)

            return self._get_obs(),r,self.done,{

                "error":"Already completed",

                "score":r

            }


        try:

            r=compute_reward(task,action)

            if r is None:
<<<<<<< HEAD
                r = 0.5
=======

                r=0.5
>>>>>>> 1633981 (Initial commit)

        except Exception as e:

            print("Reward error:",e)

<<<<<<< HEAD
            r = 0.5
=======
            r=0.5
>>>>>>> 1633981 (Initial commit)

            self.mistakes+=1

<<<<<<< HEAD

        # CRITICAL SAFETY FIX
        r = self.safe_reward(r)


        print("STEP:", self.current_step)
        print("TASK:", task.title)
        print("REWARD:", r)


        self.total_reward += r
=======

        # normalize reward
        r=self.safe_reward(r)


        # apply step penalty BEFORE adding
        r=self.safe_reward(r-self.STEP_PENALTY)


        self.total_reward+=r
>>>>>>> 1633981 (Initial commit)

        self.reward_log.append(r)


<<<<<<< HEAD

=======
>>>>>>> 1633981 (Initial commit)
        if action.mark_complete:

            if r>0.05:

                self.completed.add(task.id)

            else:

                self.mistakes+=1

<<<<<<< HEAD

        if r > 0 and self.current_step <= len(self.tasks):
=======
>>>>>>> 1633981 (Initial commit)

        # efficiency bonus
        if r>0.1 and self.current_step<=len(self.tasks):

<<<<<<< HEAD

        if len(self.completed) == len(self.tasks):
=======
            self.total_reward+=self.EFFICIENCY_BONUS
>>>>>>> 1633981 (Initial commit)


<<<<<<< HEAD

        if self.current_step >= self.max_steps:
=======
        if len(self.completed)==len(self.tasks):
>>>>>>> 1633981 (Initial commit)

            self.done=True

<<<<<<< HEAD

        obs = self._get_obs()


        info = {

            "step_reward": r,

            "total_reward": float(self.total_reward),

            "completed": len(self.completed)
=======

        if self.current_step>=self.max_steps:

            self.done=True


        obs=self._get_obs()


        info={

            "step_reward":self.safe_reward(r),

            "total_reward":self.safe_reward(self.total_reward),

            "completed":len(self.completed),

            "score":self.safe_reward(r)
>>>>>>> 1633981 (Initial commit)

        }


<<<<<<< HEAD
        # FINAL SAFETY RETURN
        r = self.safe_reward(r)


        return obs, r, self.done, info
=======
        return obs,self.safe_reward(r),self.done,info


    # =========================
    # Observation
    # =========================
>>>>>>> 1633981 (Initial commit)


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


<<<<<<< HEAD
=======
    # =========================
    # State (Evaluator uses this)
    # =========================

>>>>>>> 1633981 (Initial commit)
    def state(self):

        score=grade(

            str(self.total_reward),

            str(self.mistakes)

<<<<<<< HEAD
        # FIXED grader call
        score = grade(
            str(self.total_reward),
            str(self.mistakes)
=======
>>>>>>> 1633981 (Initial commit)
        )


<<<<<<< HEAD
        avg_reward = 0.5
=======
        score=self.safe_reward(score)
>>>>>>> 1633981 (Initial commit)


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

<<<<<<< HEAD
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
=======
            score=score,
>>>>>>> 1633981 (Initial commit)

            avg_reward=avg_reward,

            total_reward=self.safe_reward(self.total_reward),

            efficiency=efficiency,

            done=self.done
<<<<<<< HEAD
        )
=======

        )
>>>>>>> 1633981 (Initial commit)
