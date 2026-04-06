import gradio as gr
from inference import run_task
from env.tasks import TASKS


# =========================
# Run single task
# =========================

def run_selected_task(task_id):

    task = TASKS[int(task_id)]

    result = run_task(task)

    return (
        task.description,
        result["agent_output"],
        result["reward"],
        result["runtime"],
        result["status"]
    )


# =========================
# Run all tasks (benchmark)
# =========================

def run_all_tasks():

    outputs = []

    total = 0

    for task in TASKS:

        result = run_task(task)

        total += result["reward"]

        outputs.append(
            f"Task: {task.title}\nReward: {result['reward']}\nStatus: {result['status']}\n"
        )

    avg = total / len(TASKS)

    return "\n".join(outputs), round(avg,3)


# =========================
# UI
# =========================

with gr.Blocks() as demo:

    gr.Markdown("""
    # AgentWorkBench AI Environment
    
    ## AI Software Engineering Agent Benchmark
    
    This environment evaluates AI agents on:
    • Bug fixing  
    • Feature planning  
    • Documentation tasks  
    • Task prioritization  
    
    Built for OpenEnv evaluation.
    """)


    with gr.Row():

        with gr.Column():

            gr.Markdown("## Select Task")

            task_dropdown = gr.Dropdown(

                choices=[(t.title,i) for i,t in enumerate(TASKS)],

                value=0,

                label="Available Tasks"
            )

            run_button = gr.Button("Run Agent", variant="primary")

            gr.Markdown("## Task Description")

            task_text = gr.Textbox(
                lines=4,
                label="Task Details"
            )


        with gr.Column():

            gr.Markdown("## Agent Output")

            agent_output = gr.Textbox(
                lines=12,
                label="Agent Response"
            )

            reward_box = gr.Number(
                label="Reward Score"
            )

            runtime_box = gr.Number(
                label="Execution Time (sec)"
            )

            status_box = gr.Textbox(
                label="Execution Status"
            )


    gr.Markdown("## Benchmark Evaluation")

    run_all = gr.Button(
        "Run Full Evaluation",
        variant="secondary"
    )

    evaluation_output = gr.Textbox(
        lines=10,
        label="Evaluation Results"
    )

    avg_score = gr.Number(
        label="Average Score"
    )


    # =========================
    # Button actions
    # =========================

    run_button.click(

        fn=run_selected_task,

        inputs=task_dropdown,

        outputs=[
            task_text,
            agent_output,
            reward_box,
            runtime_box,
            status_box
        ]

    )


    run_all.click(

        fn=run_all_tasks,

        outputs=[
            evaluation_output,
            avg_score
        ]

    )


# =========================
# Launch (HF safe)
# =========================

if __name__ == "__main__":
    demo.launch(ssr_mode=False)