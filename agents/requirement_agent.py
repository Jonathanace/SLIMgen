import autogen
from autogen import UserProxyAgent, ConversableAgent
from configs import llama_2_config

# Create the agent that uses the LLM.
requirement_writer = autogen.AssistantAgent(
    name="requirements agent",
    system_message="You are a systems engineer. The user tells you what they want their code to do"
    "and you write requirements for that code before that code is written."
    "You will list out these requirements in a numbered list."
    "You will not write the code, you will only write the requirements.",
    llm_config=llama_2_config,
    description="""I am **ONLY** allowed to speak **immediately** after `User`.
    If `User` asks to generate requirements, the next speaker must be `requirements agent`.
    """
)

if __name__ == "__main__":
    # Create the agent that represents the user in the conversation.
    user_proxy = UserProxyAgent("user", code_execution_config=False)

    # Let the assistant start the conversation.  It will end when the user types exit.
    requirement_writer.initiate_chat(user_proxy, message="How can I help you today?")
    # Prompt: I need a Python class called calculator that can do addition and subtraction of two numbers.