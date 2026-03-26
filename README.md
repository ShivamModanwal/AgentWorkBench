# AgentWorkBench – Real-World AI Task Management Environment

## Overview

AgentWorkBench is an AI evaluation environment that tests how well an AI agent can manage real workplace tasks like classification, prioritization and scheduling.

This project simulates engineering workflow instead of games.

## Objective

The environment evaluates if AI can:

• Classify tasks  
• Assign priorities  
• Schedule tasks  
• Complete work efficiently  

## Environment API

The environment follows OpenEnv structure:

reset() → start environment  
step(action) → perform action  
state() → show results  

## Tasks

Easy:
Task classification only.

Medium:
Classification + priority.

Hard:
Classification + priority + scheduling.

## Reward System

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
