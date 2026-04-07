# 🚀 AgentWorkBench – AI Task Management Evaluation Environment

AgentWorkBench is an OpenEnv-compatible AI evaluation environment designed to measure how effectively AI agents can perform realistic productivity tasks such as classification, prioritization, scheduling, and task completion.

The environment simulates real assistant workflows and evaluates decision quality using a structured reward mechanism based on task difficulty.

---

# 🎯 Project Goal

The objective of AgentWorkBench is to:

• Evaluate AI agent decision making
• Simulate realistic productivity workflows
• Measure multi-step reasoning ability
• Provide difficulty-based evaluation
• Enable reproducible AI testing

This project focuses on realistic AI assistant behaviour instead of toy environments.

---

# 🏗 System Architecture

The system follows a modular AI evaluation pipeline:

```
User Input
    │
    ▼
Gradio Interface
    │
    ▼
AI Agent
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
```

---

# ⚙ System Flow

User → Gradio UI → Agent → Environment → Reward System

---

# 🧠 Core Features

✔ OpenEnv compatible environment
✔ Difficulty based task evaluation
✔ Multi-factor reward system
✔ Task classification testing
✔ Priority reasoning evaluation
✔ Scheduling decision testing
✔ Partial reward scoring
✔ Defensive reward normalization
✔ FastAPI integration
✔ Gradio interface

---

# 📁 Project Structure

```
AgentWorkBench/

├── env/
│   ├── environment.py
│   ├── tasks.py
│   ├── models.py
│   ├── reward.py
│   ├── grader.py
│
├── api/
├── baseline/
│
├── app.py
├── inference.py
├── openenv.yaml
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# 🔬 Environment Design

The environment evaluates agents across increasing difficulty levels:

EASY → Basic classification
MEDIUM → Classification + priority reasoning
HARD → Classification + priority + scheduling

This progressive structure tests deeper reasoning ability.

---

# 🎮 Action Space

Agent predicts:

• Task category
• Task priority
• Schedule position
• Completion decision

---

# 👁 Observation Space

Agent receives:

• Task description
• Task difficulty
• Task metadata
• Current environment state
• Completed tasks

---

# 🏆 Reward System (Actual Implementation)

The reward system is difficulty dependent and uses partial scoring.

## EASY Tasks

Evaluation:

• Category prediction
• Task completion

Rewards:

Correct category → +0.8
Wrong category → −0.1
Mark complete → +0.2

Maximum reward = 1.0

---

## MEDIUM Tasks

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

---

## HARD Tasks

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

---

# 📊 Reward Normalization Rules

To maintain stable evaluation:

Minimum reward capped at:
**−0.2**

Maximum reward capped at:
**1.0**

Reward range:
**−0.2 → 1.0**

This prevents reward collapse and keeps scoring stable.

---

# 🔌 OpenEnv API Endpoints

The environment exposes required OpenEnv endpoints:

POST **/reset** → Reset environment

POST **/step** → Execute agent action

GET **/state** → Get environment state

GET **/health** → Health check

Additional helper endpoints:

GET **/tasks**
GET **/grader**
GET **/baseline**

---

# 🧪 Example Evaluation

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

Total reward:
**0.9**

---

# 💻 Installation

Clone repository:

```
git clone <repo_url>

cd AgentWorkBench
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶ Running Locally

Run agent:

```
python inference.py
```

Run interface:

```
python app.py
```

---

# 🌐 Deployment

The project is deployed using HuggingFace Spaces for live testing.

The environment is designed to be easily reproducible and OpenEnv compliant.

---

# 📊 Evaluation Metrics

Agents are evaluated based on:

• Prediction accuracy
• Decision correctness
• Scheduling quality
• Task completion logic
• Overall reward score

---

# 🧩 Technologies Used

Python
FastAPI
Gradio
OpenEnv
LLM integration
Docker

---

# 🎯 Use Cases

This environment can be used for:

AI agent benchmarking
Assistant behaviour testing
LLM reasoning evaluation
Workflow automation research
Agent decision testing

---

# 👨‍💻 Author

Shivam Modanwal

B.Tech Computer Science
AI Systems & Agent Development

---

# 🚀 Future Improvements

Multi-agent environments
Advanced scheduling problems
Memory based agents
Reinforcement learning agents
Complex workflow chains

---

# ⭐ Conclusion

AgentWorkBench provides a structured evaluation environment for testing AI agents on realistic productivity tasks, focusing on multi-step reasoning and decision quality rather than simple task execution.
