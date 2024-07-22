import autogen
from autogen import UserProxyAgent, ConversableAgent

local_llm_config={
    "config_list": [
        {
            "model": "NotRequired", # Loaded with LiteLLM command
            "api_key": "NotRequired", # Not needed
            "base_url": "http://0.0.0.0:4000"  # Your LiteLLM URL
        }
    ],
    "cache_seed": None # Turns off caching, useful for testing different models
}

# Create the agent that uses the LLM.
requirement_agent = autogen.AssistantAgent(
    name="requirements agent",
    system_message="You are a systems engineer. The user tells you what they want their code to do"
    "and you write requirements for that code before that code is written."
    "You will list out these requirements in a numbered list."
    "You will not write the code, you will only write the requirements.",
    llm_config=local_llm_config,
    description="""I am **ONLY** allowed to speak **immediately** after `User`.
If `User` asks to generate requirements, the next speaker must be `requirements agent`.
"""
)

sourcecode_agent = autogen.AssistantAgent(
    name = "Code Agent",
    system_message = "Your goal is write code that satisfies the user's prompt or requirements provided. If the user provides a list of requirements, you will generate code that satisfies those requrements. If the user also provides code, you will review the provided code, change it if necessary and incorporate it with the code you write. When you write code, include brief short comments to explain necessary portions. Respond only with the code and the comments within the code. Make sure all the requirements are satisfied by the code you write. Do not respond with text, respond with only code.",
    llm_config=local_llm_config,
    description="""I am **ONLY** allowed to speak **immediately** after `User` and 'requirements agent'.
If `User` asks to generate source code given requirements provided by 'requirements agent', the next speaker must be `Code Agent`.
"""
)

# Create the agent that represents the user in the conversation.
user_proxy = UserProxyAgent("user", code_execution_config=False)

if __name__=="__main__":
    # Let the assistant start the conversation.  It will end when the user types exit.
    requirement_agent.initiate_chat(user_proxy, message="How can I help you today?")
# Prompt: I need a Python class called calculator that can do addition and subtraction of two numbers.