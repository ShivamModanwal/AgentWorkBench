🚀 AgentWorkBench – AI Task Management Evaluation Environment

AgentWorkBench is an OpenEnv-compatible AI evaluation environment designed to measure how effectively AI agents can perform realistic productivity tasks such as classification, prioritization, scheduling, and task completion.

The environment simulates real assistant workflows and evaluates decision quality using a structured reward mechanism based on task difficulty.

🎯 Project Goal

The objective of AgentWorkBench is to:

• Evaluate AI agent decision making  
• Simulate realistic productivity workflows  
• Measure multi-step reasoning ability  
• Provide difficulty-based evaluation  
• Enable reproducible AI testing  

This project focuses on realistic AI assistant behaviour instead of toy environments.

🏗 System Architecture

The system follows a modular AI evaluation pipeline:

User Interface (FastAPI Dashboard)
    │
    ▼
FastAPI Backend API
    │
    ▼
AI Agent Logic (inference.py)
    │
    ▼
AgentWorkBench Environment
    │
    ▼
Task Evaluation Engine
    │
    ▼
Reward Computation
    │
    ▼
Agent Performance Score

⚙ System Flow

User → FastAPI UI → Agent → Environment → Reward System

🧠 Core Features

✔ OpenEnv compatible environment  
✔ Difficulty based task evaluation  
✔ Multi-factor reward system  
✔ Task classification testing  
✔ Priority reasoning evaluation  
✔ Scheduling decision testing  
✔ Partial reward scoring  
✔ Defensive reward normalization  
✔ FastAPI API backend  
✔ Docker container deployment  
✔ Interactive testing dashboard  

📁 Project Structure

AgentWorkBench/

├── env/
│   ├── environment.py
│   ├── tasks.py
│   ├── models.py
│   ├── reward.py
│   ├── grader.py
│
├── templates/
│   ├── index.html
│
├── app.py
├── server.py
├── inference.py
├── requirements.txt
├── Dockerfile
└── README.md

🔬 Environment Design

The environment evaluates agents across increasing difficulty levels:

EASY → Basic classification  
MEDIUM → Classification + priority reasoning  
HARD → Classification + priority + scheduling  

This progressive structure tests deeper reasoning ability.

🎮 Action Space

Agent predicts:

• Task category  
• Task priority  
• Schedule position  
• Completion decision  

👁 Observation Space

Agent receives:

• Task description  
• Task difficulty  
• Task metadata  
• Current environment state  
• Completed tasks  

🏆 Reward System (Actual Implementation)

The reward system is difficulty dependent and uses partial scoring.

EASY Tasks

Evaluation:

• Category prediction  
• Task completion  

Rewards:

Correct category → +0.8  
Wrong category → −0.1  
Mark complete → +0.2  

Maximum reward = 1.0

MEDIUM Tasks

Evaluation:

• Category prediction  
• Priority prediction  
• Completion decision  

Rewards:

Correct category → +0.5  
Wrong category → −0.1  

Correct priority → +0.3  
Wrong priority → −0.05  

Mark complete → +0.2  

Maximum reward = 1.0

HARD Tasks

Evaluation:

• Category prediction  
• Priority prediction  
• Scheduling position  
• Completion decision  

Rewards:

Correct category → +0.4  
Wrong category → −0.1  

Correct priority → +0.3  
Wrong priority → −0.05  

Correct scheduling → +0.2  

Mark complete → +0.2  

Maximum reward normalized to 1.0

📊 Reward Normalization Rules

To maintain stable evaluation:

Minimum reward capped at: −0.2

Maximum reward capped at: 1.0

Reward range: −0.2 → 1.0

This prevents reward collapse and keeps scoring stable.

🔌 OpenEnv API Endpoints

Core endpoints:

POST /reset → Reset environment

POST /step → Execute agent action

GET /state → Get environment state

GET /health → Health check

Agent evaluation endpoints:

GET /run_task/{task_id} → Run agent on one task

GET /run_all → Run full benchmark

GET /baseline → Run baseline policy

GET /tasks → View tasks

🧪 Example Evaluation

Task:

Category: Study  
Priority: High  
Schedule Position: 1  

Agent Prediction:

Category: Study ✔  
Priority: High ✔  
Schedule: 2 ✖  
Complete: True ✔  

Reward:

Category → +0.4  
Priority → +0.3  
Schedule → 0  
Completion → +0.2  

Total reward: 0.9

💻 Installation

Clone repository:

git clone <repo_url>

cd AgentWorkBench

Install dependencies:

pip install -r requirements.txt

▶ Running Locally

Run backend API:

uvicorn server:app --host 0.0.0.0 --port 7860

Run evaluation script:

python inference.py

🌐 Docker Deployment

This project is deployed as a Docker container to ensure reproducibility.

Build container:

docker build -t agentworkbench .

Run container:

docker run -p 7860:7860 agentworkbench

📊 HuggingFace Deployment

The project is deployed using HuggingFace Docker Spaces.

Live API testing available via:

/docs → FastAPI Swagger interface

Users can interact with the agent using the dashboard UI or API endpoints.

📊 Evaluation Metrics

Agents are evaluated based on:

• Prediction accuracy  
• Decision correctness  
• Scheduling quality  
• Task completion logic  
• Overall reward score  

🧩 Technologies Used

Python  
FastAPI  
Docker  
OpenEnv  
REST API  
LLM integration  

🎯 Use Cases

This environment can be used for:

AI agent benchmarking  
Assistant behaviour testing  
LLM reasoning evaluation  
Workflow automation research  
Agent decision testing  

👨‍💻 Author

Shivam Modanwal

B.Tech Computer Science  
AI Systems & Agent Development

🚀 Future Improvements

Multi-agent environments  
Advanced scheduling problems  
Memory based agents  
Reinforcement learning agents  
Complex workflow chains  

⭐ Conclusion

AgentWorkBench provides a structured evaluation environment for testing AI agents on realistic productivity tasks, focusing on multi-step reasoning and decision quality rather than simple task execution.