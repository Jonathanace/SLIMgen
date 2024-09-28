import os
from autogen import ConversableAgent, register_function, register_function, GroupChat, GroupChatManager
from .configs import llama_groq_config, llama_3_1_config, llama_groq_config, codellama_config
import pprint
from typing_extensions import Annotated
from pathlib import Path
# from directory_tree import display_tree
from autogen import Agent, GroupChat, GroupChatManager, UserProxyAgent


global project
project = None # FIXME: Should default to the current directory

### Agents
tool_executor = ConversableAgent(
        name="Tool_Executor",
        human_input_mode="NEVER",
        llm_config=False,
        is_termination_msg=True
    )

# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    # "You must *ALWAYS* begin by asking the user to set a project directory with set_project()"
    "Call show_project_files() to output all the files in the current project."
    "Call read_code(file_path) to read code from a file. "
    "Call set_project() to set the filepath for the current project. "
    "Call check_readme() to check if the project has a README file."
    "Return 'TERMINATE' when the task is done."
    "You can learn more about how a project works by using read_code() to read python code from a file. "
    "If the user refers to any files, first use read_code(file_path) to get more context. ",
    llm_config=llama_groq_config,
    # max_consecutive_auto_reply=2,
    human_input_mode="NEVER",
    code_execution_config=False
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = UserProxyAgent(
    name="User",    
    is_termination_msg=lambda msg: msg.get("content") is not None and ("TERMINATE" in msg["content"] or "USER INPUT:" in msg["content"]),
    human_input_mode="TERMINATE",
    code_execution_config=False,
    max_consecutive_auto_reply=1
)

### Tools
def read_code(file_path: Annotated[str, "File or path to read code from."]) -> str:
    global project
    # if not project:
    #     return 'No project directory set. Please set one and try again.'
    
    
    try:
        contents = Path(file_path).read_text()
        return contents
    except:
        file = project / file_path
        try:
            contents = file.read_text()
        except:
            raise Exception('File not found.')

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

def show_all_files_in_dir(file_path: Annotated[str, "Directory to show files from."])->str:
    global project
    # for file in project.rglob('*'):
    #     print(read_code(file))
    return display_tree(file_path, string_rep=True, show_hidden=True)

def register_funcs(caller, executor):
    register_function(
        read_code,
        caller=caller,
        executor=executor,
        name="read_code",
        description="Reads code from a file."
    )

    register_function(
        set_project,
        caller=caller,
        executor=executor,
        name="set_project",
        description="A simple tool to set the project path."
    )

    register_function(
        save_code,
        caller=caller,
        executor=executor,
        name="save_code",
        description="A simple tool to save code."
    )

    register_function(
        check_readme,
        caller=caller,
        executor=executor,
        name="check_readme",
        description="A simple tool to checks if a README file exists."
    )

    register_function(
        show_all_files_in_dir,
        caller=caller,
        executor=executor,
        name="show_all_files_in_dir",
        description="Shows all the files in a directory."
    )


### Tests
def test_read_code():
    register_funcs(caller=assistant, executor=user_proxy) 
    chat_result = assistant.initiate_chat(user_proxy, message="Please enter your project's relative path. USER INPUT:", clear_history=True, silent=False)
    # return

def state_transition(last_speaker: Agent, groupchat: GroupChat):
    # return "auto"
    messages = groupchat.messages
    if "tool_calls" in messages[-1]:
        called = messages[-1]["tool_calls"][0]["function"]["name"]
        if called in last_speaker.function_map:
            return last_speaker
    return "auto"

def expert_chat():
    register_funcs(assistant, user_proxy)
    assistant.initiate_chat(user_proxy, message="What do you want to set as your project path? USER INPUT:")

def test_groupchat():
    allowed_transitions = {
        assistant: [user_proxy, assistant],
        user_proxy: [assistant]
    }

    register_funcs(assistant, assistant)

    groupchat = GroupChat(
        agents=[user_proxy, assistant],
        speaker_selection_method=state_transition,
        send_introductions=True,
        messages=[],
        speaker_transitions_type="allowed",
        allowed_or_disallowed_speaker_transitions=allowed_transitions,
        select_speaker_auto_verbose=True
    )

    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llama_3_1_config,
    )

    chat_result = user_proxy.initiate_chat(manager, message="My project is at examples/calculator", clear_history=True)


if __name__ == '__main__':
    test_read_code()

# FIXME: show_project_files