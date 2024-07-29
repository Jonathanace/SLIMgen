from tools import code_reader
from autogen import AssistantAgent, UserProxyAgent, register_function
from configs import llama_groq_config

tool_executor = AssistantAgent(
    name = "Code Agent",
    system_message = "You will help the user fufill the provided task."
    "You can read code from a file.",
    llm_config=llama_groq_config
)



if __name__ == "__main__":
    user_proxy = UserProxyAgent("user", code_execution_config=False) # create user proxy

    tool_executor.register_for_llm(name="file_reader", description="A simple tool to read code from a file")(code_reader)

    user_proxy.register_for_execution(name="file_reader")(code_reader)

    register_function(
        code_reader,
        caller=tool_executor,
        executor=user_proxy,
        name="file_reader",
        description="reads code from a file"
    )

    # Assistant starts conversation. Ends when user types 'exit'.
    user_proxy.initiate_chat(tool_executor, message="Read the code from agents/sourcecode_agent.py")