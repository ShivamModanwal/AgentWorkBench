from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class TaskCategory(str, Enum):
    BUG="bug"
    FEATURE="feature"
    DOCUMENTATION="documentation"
    DEVOPS="devops"
    SUPPORT="support"


class TaskPriority(str, Enum):
    LOW="low"
    MEDIUM="medium"
    HIGH="high"
    CRITICAL="critical"


class TaskDifficulty(str, Enum):
    EASY="easy"
    MEDIUM="medium"
    HARD="hard"


class Task(BaseModel):

    id:str

    title:str

    description:str

    difficulty:TaskDifficulty

    estimated_steps:int

    deadline:int

    schedule_position:int = 0

    true_category:TaskCategory

    true_priority:TaskPriority


class TaskObservation(BaseModel):

    id:str

    title:str

    description:str

    difficulty:TaskDifficulty

    estimated_steps:int

    deadline:int


class Observation(BaseModel):

    tasks:List[TaskObservation] = Field(default_factory=list)

    current_step:int = 0

    max_steps:int = 0

    completed_tasks:List[str] = Field(default_factory=list)


class Action(BaseModel):

    task_id:str

    predicted_category:Optional[TaskCategory]=None

    predicted_priority:Optional[TaskPriority]=None

    scheduled_position:Optional[int]=None

    mark_complete:bool=False


class Reward(BaseModel):

    classification_reward:float=0

    priority_reward:float=0

    scheduling_reward:float=0

    efficiency_reward:float=0

    penalty:float=0

    total:float=0


class EnvironmentState(BaseModel):

    avg_reward:float = 0

    total_reward:float = 0

    total_tasks:int = 0

    completed_count:int = 0

    steps_taken:int = 0

    mistakes:int = 0

    score:float = 0

    efficiency:float = 0

    done:bool = False