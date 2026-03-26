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

Rewards include:

• Correct classification  
• Correct priority assignment  
• Correct scheduling  
• Efficient task completion  

Penalties include:

• Incorrect decisions  
• Duplicate actions  
• Unnecessary steps  

Final scores are normalized between **0.0 and 1.0**.

---

## Architecture Overview

The project follows a modular environment design:

Environment Layer → Task simulation and state transitions  
Reward Layer → Decision evaluation logic  
Grader Layer → Score normalization  
Baseline Layer → Deterministic benchmark agent  
API Layer → Environment interaction endpoints  

This modular design ensures deterministic evaluation and maintainability.

---

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
Dockerfile  
requirements.txt  
README.md  

---

## How to Run

### Install dependencies

pip install -r requirements.txt

### Run baseline agent

python -m baseline.baseline_agent

### Run API server

uvicorn api.server:app --reload

Open in browser:

http://127.0.0.1:8000/docs

---

## API Endpoints

/tasks → List available tasks  

/grader → Return evaluation state  

/baseline → Run baseline benchmark  

---

## Evaluation Philosophy

The environment prioritizes:

• Decision correctness  
• Workflow efficiency  
• Task prioritization quality  

rather than simple task completion to better reflect real-world AI workplace evaluation.

---

## Use Cases

This environment can be used for:

• AI agent evaluation  
• Workflow optimization testing  
• Task management benchmarking  
• Research experimentation  

---

## Troubleshooting

If dependencies missing:

pip install -r requirements.txt

If port is busy:

uvicorn api.server:app --port 8001

---

## Design Goals

The environment was built with three priorities:

Reliability → deterministic grading  

Realism → workplace simulation  

Simplicity → clean environment interface  

---

## Author

Shivam Modanwal  
B.Tech – AI Environment Evaluation Project
