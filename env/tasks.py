from .models import Task,TaskCategory,TaskPriority,TaskDifficulty

def load_tasks():

    return [

    Task(
    id="1",
    title="Fix login bug",
    description="Users unable to login",
    difficulty=TaskDifficulty.EASY,
    estimated_steps=2,
    deadline=3,
    true_category=TaskCategory.BUG,
    true_priority=TaskPriority.CRITICAL
    ),

    Task(
    id="2",
    title="Add dark mode",
    description="UI feature request",
    difficulty=TaskDifficulty.MEDIUM,
    estimated_steps=5,
    deadline=10,
    true_category=TaskCategory.FEATURE,
    true_priority=TaskPriority.MEDIUM
    ),

    Task(
    id="3",
    title="Update docs",
    description="API documentation update",
    difficulty=TaskDifficulty.EASY,
    estimated_steps=2,
    deadline=8,
    true_category=TaskCategory.DOCUMENTATION,
    true_priority=TaskPriority.LOW
    ),

    Task(
    id="4",
    title="Handle production outage",
    description="Critical production failure",
    difficulty=TaskDifficulty.HARD,
    estimated_steps=6,
    deadline=2,
    schedule_position=1,
    true_category=TaskCategory.DEVOPS,
    true_priority=TaskPriority.CRITICAL
    )

    ]
