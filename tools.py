import os
from autogen import ConversableAgent, register_function
from configs import llama_groq_config, llama_3_1_config
import pprint
from typing_extensions import Annotated
from pathlib import Path

global project
project = None

### Agents
tool_executor = ConversableAgent(
        name="Tool_Executor",
        human_input_mode="NEVER",
        llm_config=False,
        is_termination_msg=True
    )

### Tools
def read_code(file_path: Annotated[str, "File or path to read code from"]) -> str:
    file_path = Path(file_path)
    if not project:
        print('No project directory set.')
        set_project(file_path.parents[0])
    file = project / file_path.name
    if not file:
        raise Exception('file does not exist')
    contents = file.read_text()
    return contents

def set_project(
        project_path: Annotated[str, "The path of the project the user wants to analyze"]
        )->str:
    global project
    if project:
        print(f'Project is already {str(project)}. Overriding to {project_path}')
    try:
        project = Path(project_path)
        print(f'Project path set to {project}')
        return str(project) + " is now set as the project directory."
    except Exception as exception:
        return 'Exception!' + str(exception)
    
def save_code(
        file_path: Annotated[str, "The path to the file to save the code to"], 
        code: Annotated[str, "The code to save to the file"]
        ) -> str:
    global project
    file_path = Path(file_path)
    if file_path.is_relative_to(str(project)):
        new_file_path = file_path
    else:
        new_file_path = project / file_path
    new_file_path.touch()
    new_file_path.write_text(code)
    return f'The contents of {file_path} are now {read_code(file_path)}'

def check_readme()->bool:
    global project
    if not project:
        return 'Project not set. Please enter your desired project path first.'
    if (project / 'README.md').is_file():
        return 'A README file exists in the project directory'
    else:
        return 'A README file doesn\'t exist in the project directory'

def walk_directory()->str:
    global project
    # for file in project.rglob('*'):
    #     print(read_code(file))
    return '\n'.join([read_code(file) for file in project.rglob('*')])

### Tests
def test_read_code():
    # Let's first define the assistant agent that suggests tool calls.
    assistant = ConversableAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant. "
        "You must *ALWAYS* begin by asking the user to set a project directory with set_project()"
        "You can help with reading local files. "
        "To set the path for the project call set_project(desired_path). "
        "You can save or edit code for a specified file or file path but you **MUST** use the save_code tool to do so."
        "Call check_readme() to check if the project has a README file."
        "Call walk_directory to output all files in a directory."
        "Return 'TERMINATE' when the task is done.",
        llm_config=llama_groq_config,
        # max_consecutive_auto_reply=1,
        human_input_mode="NEVER",
        code_execution_config=False
    )

    # The user proxy agent is used for interacting with the assistant agent
    # and executes tool calls.
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and ("TERMINATE" in msg["content"] or "USER INPUT:" in msg["content"]),
        human_input_mode="TERMINATE",
        code_execution_config=False,
        max_consecutive_auto_reply=1
    )

    # Register the tool signature with the assistant agent.
    # assistant.register_for_llm(name="read_code", description="A simple tool to read code from a file")(read_code)

    # Register the tool function with the user proxy agent.
    # user_proxy.register_for_execution(name="read_code")(read_code)

    register_function(
        read_code,
        caller=assistant,
        executor=user_proxy,
        name="read_code",
        description="Reads code from a file."
    )

    register_function(
        set_project,
        caller=assistant,
        executor=user_proxy,
        name="set_project",
        description="A simple tool to set the project path"
    )

    register_function(
        save_code,
        caller=assistant,
        executor=user_proxy,
        name="save_code",
        description="A simple tool to save code."
    )

    register_function(
        check_readme,
        caller=assistant,
        executor=user_proxy,
        name="check_readme",
        description="A simple tool to checks if a README file exists."
    )

    register_function(
        walk_directory,
        caller=assistant,
        executor=user_proxy,
        name="walk_directory",
        description="Outputs all files in the project directory"
    )

    ### Nested chats
    # tool_executor.register_nested_chats(
    #     trigger=user_proxy,
    #     chat_queue=[
    #         {
    #             "sender": user_proxy,
    #             "recipient": tool_executor,
    #             "summary_method": "last_msg",
    #         }
    #     ]
    # )
    # print(assistant.llm_config["tools"])
    chat_result = assistant.initiate_chat(user_proxy, message="Please enter your project's relative path. USER INPUT:", clear_history=True, silent=False)
    # return

if __name__ == '__main__':
    test_read_code()