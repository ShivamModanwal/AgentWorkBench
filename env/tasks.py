from .models import Task, TaskCategory, TaskPriority, TaskDifficulty


def load_tasks():

    tasks = [

        Task(
            id="1",
            title="Fix login bug",
            description="Users unable to login due to authentication error",
            difficulty=TaskDifficulty.EASY,
            estimated_steps=2,
            deadline=3,
            schedule_position=2,
            true_category=TaskCategory.BUG,
            true_priority=TaskPriority.CRITICAL
        ),

        Task(
            id="2",
            title="Add dark mode",
            description="Implement UI dark mode feature",
            difficulty=TaskDifficulty.MEDIUM,
            estimated_steps=5,
            deadline=10,
            schedule_position=3,
            true_category=TaskCategory.FEATURE,
            true_priority=TaskPriority.MEDIUM
        ),

        Task(
            id="3",
            title="Update docs",
            description="Update API documentation",
            difficulty=TaskDifficulty.EASY,
            estimated_steps=2,
            deadline=8,
            schedule_position=4,
            true_category=TaskCategory.DOCUMENTATION,
            true_priority=TaskPriority.LOW
        ),

        Task(
            id="4",
            title="Handle production outage",
            description="Resolve critical production failure",
            difficulty=TaskDifficulty.HARD,
            estimated_steps=6,
            deadline=2,
            schedule_position=1,
            true_category=TaskCategory.DEVOPS,
            true_priority=TaskPriority.CRITICAL
        )

    ]

    # deterministic ordering (important for evaluation)
    tasks = sorted(tasks, key=lambda x: x.id)

    return tasks


# Global task list (used by environment)
TASKS = load_tasks()