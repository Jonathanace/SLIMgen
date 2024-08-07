import autogen
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor
from configs import *

def example():
    executor = LocalCommandLineCodeExecutor(work_dir="coding")
    code_executor_agent = ConversableAgent(
        name="code_executor_agent",
        llm_config=False,
        code_execution_config={
            "executor": executor,
        },
        human_input_mode="NEVER",
    )

    user_proxy = UserProxyAgent(
        name="User",
        code_execution_config=False,
        llm_config=False,
    )

    user_proxy.initiate_chat(
        code_executor_agent,
        message="""
        Execute this Python code: 
        # calculator.py
        class Calculator:
            def add(self, a, b):
                return a + b

            def subtract(self, a, b):
                return a - b
        """,
        clear_history=True
    )

def ex_gc():

    task = "Write a blogpost about the stock price performance of "\
    "Nvidia in the past month. Today's date is 2024-07-25."

    user_proxy = autogen.ConversableAgent(
        name="Admin",
        system_message="Give the task, and send "
        "instructions to writer to refine the blog post.",
        code_execution_config=False,
        llm_config=codellama_config,
        human_input_mode="ALWAYS",
    )

    planner = autogen.ConversableAgent(
        name="Planner",
        system_message="Given a task, please determine "
        "what information is needed to complete the task. "
        "Please note that the information will all be retrieved using"
        " Python code. Please only suggest information that can be "
        "retrieved using Python code. "
        "After each step is done by others, check the progress and "
        "instruct the remaining steps. If a step fails, try to "
        "workaround",
        description="Given a task, determine what "
        "information is needed to complete the task. "
        "After each step is done by others, check the progress and "
        "instruct the remaining steps",
        llm_config=codellama_config,
    )

    engineer = autogen.AssistantAgent(
        name="Engineer",
        llm_config=codellama_config,
        description="Write code based on the plan "
        "provided by the planner.",
    )

    writer = autogen.ConversableAgent(
        name="Writer",
        llm_config=codellama_config,
        system_message="Writer. "
        "Please write blogs in markdown format (with relevant titles)"
        " and put the content in pseudo ```md``` code block. "
        "You take feedback from the admin and refine your blog.",
        description="After all the info is available, "
        "write blogs based on the code execution results and take "
        "feedback from the admin to refine the blog. ",
    )

    executor = autogen.ConversableAgent(
        name="Executor",
        description="Execute the code written by the "
        "engineer and report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "coding",
            "use_docker": False,
        },
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, engineer, writer, executor, planner],
        messages=[],
        max_round=10,
        allowed_or_disallowed_speaker_transitions={
            user_proxy: [planner],
            engineer: [executor],
            writer: [planner],
            executor: [engineer, planner],
            planner: [engineer, writer],
        },
        speaker_transitions_type="allowed",
    )

    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=codellama_config
    )

    groupchat_result = user_proxy.initiate_chat(
        manager,
        message=task,
    )

if __name__ == "__main__": 
    ex_gc()