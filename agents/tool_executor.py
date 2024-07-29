from tools import code_reader
from autogen import AssistantAgent, UserProxyAgent, register_function
from configs import llama_groq_config

tool_executor = AssistantAgent(
    name = "Code Agent",
    system_message = "Your goal is write code that satisfies the user's prompt or requirements provided. If the user provides a list of requirements, you will generate code that satisfies those requrements. If the user also provides code, you will review the provided code, change it if necessary and incorporate it with the code you write. When you write code, include brief short comments to explain necessary portions. Respond only with the code and the comments within the code. Make sure all the requirements are satisfied by the code you write. Do not respond with text, respond with only code.",
    llm_config=llama_groq_config
)

if __name__ == "__main__":
    user_proxy = UserProxyAgent("user", code_execution_config=False) # create user proxy

    register_function(
        code_reader,
        caller=tool_executor,
        executor=user_proxy,
        name="code_reader",
        description="reads code from a file"
    )

    # Assistant starts conversation. Ends when user types 'exit'.
    user_proxy.initiate_chat(tool_executor, message="Read the code from agents/sourcecode_agent.py"