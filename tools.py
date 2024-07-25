import os
from autogen import ConversableAgent
from configs import llama_groq_config
import pprint

### Tools
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

    # Register the tool signature with the assistant agent.
    assistant.register_for_llm(name="code_reader", description="A simple tool to read code from a file")(code_reader)

    # Register the tool function with the user proxy agent.
    user_proxy.register_for_execution(name="code_reader")(code_reader)

    chat_result = user_proxy.initiate_chat(assistant, message=None, clear_history=True, silent=False)

    return 

if __name__ == '__main__':
    test_code_reader()