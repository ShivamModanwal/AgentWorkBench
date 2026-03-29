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

This modular design ensures deterministic evaluation, maintainability, and reproducible benchmarking.

---

## Project Structure

AgentWorkBench/

env/  
 environment.py  
 tasks.py  
 grader.py  
 reward.py  
 models.py  

api/  
 server.py  

baseline/ (development reference)

inference.py  

openenv.yaml  
Dockerfile  
requirements.txt  
README.md  
.gitignore  

---

## How to Run

### Install dependencies

pip install -r requirements.txt

### Run inference script (baseline evaluation)

python inference.py

Expected output:

Task 1 Score: X  
Task 2 Score: X  
Task 3 Score: X  

Final Score: X  

### Run API server

uvicorn api.server:app --reload

Open:

http://127.0.0.1:8000/docs

---

## API Endpoints

/reset → Reset environment  

/tasks → List available tasks  

/grader → Get evaluation state  

/baseline → Run baseline evaluation  

/health → Environment status  

---

## OpenEnv Compliance

This project implements:

• Typed observation models  
• Typed action models  
• Typed reward outputs  
• reset(), step(), state() interface  
• Deterministic grading  
• Reproducible inference script  
• OpenEnv metadata configuration  

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
• OpenEnv evaluation pipelines  

---

## Design Goals

The environment was built with three priorities:

Reliability → deterministic grading  

Realism → workplace simulation  

Simplicity → clean environment interface  

---

## Troubleshooting

If dependencies missing:

pip install -r requirements.txt

If API port busy:

uvicorn api.server:app --port 8001

If inference fails:

Ensure Python version ≥ 3.9.

---

## Future Improvements

Possible extensions:

• Multi-agent evaluation  
• Dynamic task generation  
• Advanced scheduling optimization  
• Learning agent integration  

---

## Team

Shivam Modanwal  
B.Tech (Information Technology), 3rd Year  
Role: Environment Architecture & Integration  

Mohd. Salim Naeem  
B.Tech (Artificial Intelligence & Machine Learning), 3rd Year  
Role: Task Design, Testing & Validation  

---

## Author Notes

This project was developed as part of an AI environment evaluation assessment focused on real-world AI task management scenarios rather than synthetic benchmarks.

---

## License

Educational / Research Use
