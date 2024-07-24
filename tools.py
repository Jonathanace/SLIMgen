import os
from autogen import ConversableAgent, register_function, GroupChat, GroupChatManager
from configs import local_llm_config, llama_groq_config, codellama_config
import pprint
from typing_extensions import Annotated

### Tools
def list_dir(directory: Annotated[str, "Directory to check."]):
    files = os.listdir(directory)
    return files

def code_reader(file_path: str) -> str:
    with open(os.path.join(file_path), 'r') as file:
        code = file.read()
    return code

### Tests
def test_code_reader():
    # Let's first define the assistant agent that suggests tool calls.
    assistant = ConversableAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant. "
        "You can help with reading local files. "
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

    groupchat = GroupChat(
        agents=[assistant, user_proxy],
        messages=[],
        max_round=500,
        speaker_selection_method="round_robin",
        enable_clear_history=True,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=local_llm_config)



    # # Register the tool signature with the assistant agent.
    # assistant.register_for_llm(name="code_reader", description="A simple tool to read code from a file")(code_reader)

    # # Register the tool function with the user proxy agent.
    # user_proxy.register_for_execution(name="code_reader")(code_reader)

    register_function(
        code_reader,
        caller=assistant,
        executor=user_proxy,
        name="code_reader",
        description="outputs code for a given file"
    )

    # print(assistant.llm_config["tools"])
    chat_result = user_proxy.initiate_chat(manager, message="Show me the code found in examples/calculator/calculator.py", clear_history=True, silent=False)

    return 

if __name__ == '__main__':
    test_code_reader()