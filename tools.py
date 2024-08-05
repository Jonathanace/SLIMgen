import os
from autogen import ConversableAgent, register_function
from configs import llama_groq_config
import pprint
from typing_extensions import Annotated
from pathlib import Path

### Tools
def read_code(file_path: str) -> str:
    try:
        project
    except:
        file_path = Path(file_path)
        print('No project directory set.')
        set_project(file_path.parents[0])
    file = project / file_path.name
    if not file:
        raise Exception('file does not exist')
    contents = file.read_text()
    return contents

def set_project(project_path: Annotated[str, "The path of the project the user wants to analyze"])->str:
    global project
    try:
        project = Path(project_path)
        print(f'Project path set to {project_path}')
    except Exception as exception:
        return str(exception)


### Tests
def test_read_code():
    # Let's first define the assistant agent that suggests tool calls.
    assistant = ConversableAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant. "
        "You can help with reading local files. "
        "You can set the path for the project the user wants to analyze. "
        "Return 'TERMINATE' when the task is done.",
        llm_config=llama_groq_config,
        max_consecutive_auto_reply=1
    )

    # The user proxy agent is used for interacting with the assistant agent
    # and executes tool calls.
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    # Register the tool signature with the assistant agent.
    assistant.register_for_llm(name="read_code", description="A simple tool to read code from a file")(read_code)

    # Register the tool function with the user proxy agent.
    user_proxy.register_for_execution(name="read_code")(read_code)

    register_function(
        set_project,
        caller=assistant,
        executor=user_proxy,
        name="set_project",
        description="Sets the path for the project the user wants to analyze"
    )

    chat_result = user_proxy.initiate_chat(assistant, message="Show me the code found in examples/calculator/calculator.py", clear_history=True, silent=False)

    return 

if __name__ == '__main__':
    test_read_code()