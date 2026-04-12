"""
Baseline inference script for AgentWorkBench.
Emits stdout in the OpenEnv hackathon format.
"""

import json
import os
import sys
from typing import List, Optional, Tuple

from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority
from env.score_utils import clamp_score, format_clamped_score
from env.tasks import TASKS

try:
    from openai import OpenAI
except Exception:
    OpenAI = None
    

ENV_NAME = "agentworkbench-FIXED"
API_BASE_URL = os.getenv("API_BASE_URL") or "https://api.openai.com/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "gpt-4o-mini"
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY")


def strict_score(value: object) -> float:
    return clamp_score(value)


def get_client() -> Optional["OpenAI"]:
    if OpenAI is None or not HF_TOKEN:
        return None
    try:
        return OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    except Exception:
        return None


CLIENT = get_client()


def log_start(task_name: str) -> None:
    print(
        f"[START] task={task_name} env={ENV_NAME} model={MODEL_NAME}",
        flush=True,
    )


def format_reward(value: object) -> str:
    """
    Yeh function strictly string ko control karega taaki 
    round off hokar bhi 1.0 print na ho.
    """
    try:
        val = float(value)
        # Ek baar aur strictly clamp karo
        clamped_val = max(0.001, min(0.999, val))
        # Exact 4 decimal places print karo (jaise 0.9990)
        return f"{clamped_val:.4f}"
    except Exception:
        # Agar error aaye toh safe string
        return "0.0010"

def log_step(step_num: int, action: dict, reward: float, done: bool, error: Optional[str]) -> None:
    error_text = error if error else "null"
    action_text = json.dumps(action, separators=(",", ":"))
    print(
        f"[STEP] step={step_num} action={action_text} reward={format_reward(reward)} "
        f"done={str(done).lower()} error={error_text}",
        flush=True,
    )


def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    reward_list = ",".join(format_reward(reward) for reward in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={reward_list}",
        flush=True,
    )


def analyze_task(description: str) -> Tuple[TaskCategory, TaskPriority]:
    text = description.lower()

    if CLIENT is not None:
        try:
            response = CLIENT.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Classify this software task.\n"
                            "Return two lines only.\n"
                            "CATEGORY: BUG | FEATURE | DOCUMENTATION | DEVOPS\n"
                            "PRIORITY: CRITICAL | MEDIUM | LOW"
                        ),
                    },
                    {"role": "user", "content": description},
                ],
                temperature=0,
            )
            text = response.choices[0].message.content.lower()
        except Exception:
            pass

    if "bug" in text or "error" in text or "fix" in text or "auth" in text:
        return TaskCategory.BUG, TaskPriority.CRITICAL
    if "feature" in text or "add" in text or "implement" in text:
        return TaskCategory.FEATURE, TaskPriority.MEDIUM
    if "doc" in text or "readme" in text or "documentation" in text:
        return TaskCategory.DOCUMENTATION, TaskPriority.LOW
    if "outage" in text or "production" in text or "failure" in text or "deploy" in text:
        return TaskCategory.DEVOPS, TaskPriority.CRITICAL
    return TaskCategory.DEVOPS, TaskPriority.MEDIUM


def build_action(task) -> dict:
    category, priority = analyze_task(task.description)
    return {
        "task_id": task.id,
        "predicted_category": category.value,
        "predicted_priority": priority.value,
        "scheduled_position": getattr(task, "schedule_position", 1),
        "mark_complete": True,
    }


def run_task(task) -> float:
    env = AgentWorkBenchEnv()
    env.reset()
    log_start(task.title)
    
    action_payload = build_action(task)
    error = None
    rewards: List[float] = []
    
    try:
        action = Action(**action_payload)
        _, reward, done, info = env.step(action)
        
        # Yahan score safely clamp ho gaya
        score = clamp_score(info.get("score", reward) if isinstance(info, dict) else reward)
        rewards.append(score)
        
        # ✅ FIX: Raw 'reward' ki jagah clamped 'score' ko log mein bhejo
        log_step(1, action_payload, score, done, error)
        
        log_end(score >= 0.5, 1, rewards)
        return score
        
    except Exception as exc:
        error = str(exc).replace("\n", " ")
        fallback = clamp_score(0.5)
        rewards.append(fallback)
        log_step(1, action_payload, fallback, True, error)
        log_end(False, 1, rewards)
        return fallback


def evaluate() -> float:
    scores = [clamp_score(run_task(task)) for task in TASKS]
    return clamp_score(sum(scores) / len(scores)) if scores else clamp_score(0.5)


def main() -> None:
    evaluate()
    sys.stdout.flush()


if __name__ == "__main__":
    main()
