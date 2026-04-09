"""
Baseline inference script for AgentWorkBench.
Compliant with strict structured stdout logging and OpenEnv score bounds.
"""

import json
import os
import sys
from typing import Optional, Tuple

from env.environment import AgentWorkBenchEnv
from env.models import Action, TaskCategory, TaskPriority
from env.tasks import TASKS

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


ENV_NAME = "agentworkbench"
API_BASE_URL = os.getenv("API_BASE_URL") or "https://api.openai.com/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "gpt-4o-mini"
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY")


def strict_score(value: object) -> float:
    try:
        score = float(value)
    except Exception:
        return 0.5
    return max(0.02, min(0.98, score))


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


def log_step(step_num: int, action: dict, reward: float, done: bool, error: Optional[str]) -> None:
    error_text = error if error else "null"
    action_text = json.dumps(action, separators=(",", ":"))
    print(
        f"[STEP] step={step_num} action={action_text} reward={strict_score(reward):.3f} "
        f"done={str(done).lower()} error={error_text}",
        flush=True,
    )


def log_end(task_name: str, score: float, success: bool) -> None:
    print(
        f"[END] task={task_name} success={str(success).lower()} score={strict_score(score):.3f}",
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

    try:
        action = Action(**action_payload)
        _, reward, done, info = env.step(action)
        score = strict_score(info.get("score", reward) if isinstance(info, dict) else reward)
        log_step(1, action_payload, reward, done, error)
        log_end(task.title, score, score >= 0.5)
        return score
    except Exception as exc:
        error = str(exc).replace("\n", " ")
        fallback = 0.5
        log_step(1, action_payload, fallback, True, error)
        log_end(task.title, fallback, False)
        return fallback


def evaluate() -> float:
    print(f"[START] evaluation env={ENV_NAME} model={MODEL_NAME}", flush=True)
    scores = [strict_score(run_task(task)) for task in TASKS]
    avg = strict_score(sum(scores) / len(scores)) if scores else 0.5
    print(f"[END] evaluation score={avg:.3f}", flush=True)
    return avg


def main() -> None:
    evaluate()
    print("[END] run_complete", flush=True)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
