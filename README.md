# AgentWorkBench – Real-World AI Task Management OpenEnv Environment

AgentWorkBench is an OpenEnv-compatible evaluation environment designed to test how well AI agents can manage real-world workplace tasks such as task classification, priority assignment, and workflow scheduling. Unlike game environments, this project focuses on realistic engineering workflow evaluation with deterministic grading.

---

## Objectives

The environment evaluates whether AI agents can:

• Classify engineering tasks  
• Assign correct priorities  
• Schedule workflows efficiently  
• Complete tasks correctly  
• Minimize unnecessary actions  

---

## Environment Interface

The environment follows the OpenEnv interaction model:

reset() → Initialize environment  
step(action) → Execute agent decision  
state() → Return evaluation results  

---

## Task Difficulty Progression

Easy → Task classification only  

Medium → Classification + priority assignment  

Hard → Classification + priority + scheduling optimization  

---

## Reward Design

Rewards:
Correct classification  
Correct priority  
Correct scheduling  
Efficiency  

Penalties:
Wrong decisions  
Extra steps  

Score range:
0 to 1.

## Project Structure

AgentWorkBench/

env/
environment.py
tasks.py
grader.py
reward.py
models.py

baseline/
baseline_agent.py

api/
server.py

openenv.yaml

## Run Project

Install:

pip install -r requirements.txt

Run baseline:

python -m baseline.baseline_agent

Run API:

uvicorn api.server:app --reload

Open browser:

http://127.0.0.1:8000/docs

## Author

Shivam Modanwal

## Architecture Overview

AgentWorkBench follows a modular environment design:

Environment Layer:
Handles task simulation, state transitions and episode lifecycle.

Reward Layer:
Evaluates decision correctness and efficiency.

Grader Layer:
Normalizes reward into final performance score.

Baseline Layer:
Provides deterministic benchmark agent.

API Layer:
Exposes environment interaction endpoints.

This separation ensures maintainability and deterministic evaluation.

## Design Goals

This environment was designed with three priorities:

1 Reliability → deterministic grading
2 Realism → workplace task simulation
3 Simplicity → clean environment interface


## Evaluation Philosophy

The environment prioritizes correctness, efficiency, and decision quality rather than raw task completion to better reflect real-world AI workplace performance.