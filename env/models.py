from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


# =========================
# Enums
# =========================

class TaskCategory(str,Enum):

    BUG="bug"

    FEATURE="feature"

    DOCUMENTATION="documentation"

    DEVOPS="devops"

    SUPPORT="support"



class TaskPriority(str,Enum):

    LOW="low"

    MEDIUM="medium"

    HIGH="high"

    CRITICAL="critical"



class TaskDifficulty(str,Enum):

    EASY="easy"

    MEDIUM="medium"

    HARD="hard"



# =========================
# Task Model
# =========================

class Task(BaseModel):

    id:str

    title:str

    description:str

    difficulty:TaskDifficulty

    estimated_steps:int = Field(default=1,ge=1)

    deadline:int = Field(default=1,ge=0)

    schedule_position:int = Field(default=1,ge=0)

    true_category:TaskCategory

    true_priority:TaskPriority



# =========================
# Observation Models
# =========================

class TaskObservation(BaseModel):

    id:str

    title:str

    description:str

    difficulty:TaskDifficulty

    estimated_steps:int

    deadline:int



class Observation(BaseModel):

    tasks:List[TaskObservation] = Field(default_factory=list)

    current_step:int = Field(default=0,ge=0)

    max_steps:int = Field(default=1,ge=1)

    completed_tasks:List[str] = Field(default_factory=list)



# =========================
# Action Model
# =========================

class Action(BaseModel):

    task_id:str

    predicted_category:Optional[TaskCategory]=None

    predicted_priority:Optional[TaskPriority]=None

    scheduled_position:Optional[int]=Field(default=1,ge=0)

    mark_complete:bool=False



# =========================
# Reward Model
# =========================

class Reward(BaseModel):

    classification_reward:float=Field(default=0.001,gt=0,lt=1)

    priority_reward:float=Field(default=0.001,gt=0,lt=1)

    scheduling_reward:float=Field(default=0.001,gt=0,lt=1)

    efficiency_reward:float=Field(default=0.001,gt=0,lt=1)

    penalty:float=Field(default=0.001,gt=0,lt=1)

    total:float=Field(default=0.5,gt=0,lt=1)



# =========================
# Environment State
# =========================

class EnvironmentState(BaseModel):

    total_tasks:int = Field(default=0,ge=0)

    completed_count:int = Field(default=0,ge=0)

    steps_taken:int = Field(default=0,ge=0)

    mistakes:int = Field(default=0,ge=0)

    score:float = Field(default=0.5,gt=0,lt=1)

    avg_reward:float = Field(default=0.5,gt=0,lt=1)

    total_reward:float = Field(default=0.5,gt=0,lt=1)

    efficiency:float = Field(default=0.5,gt=0,lt=1)

    done:bool = False
