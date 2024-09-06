import autogen
from autogen import UserProxyAgent, ConversableAgent
from configs import codellama_config

# Create the agent that uses the LLM.
# assistant = ConversableAgent("agent", llm_config=local_llm_config)

source_code_writer = autogen.AssistantAgent(
    name = "Code Agent",
    system_message = "Your goal is write code that satisfies the requirements provided."
    "If the user provides a list of requirements, you will generate executable code that satisfies those requrements." 
    "If the user also provides code, you will review the provided code, change it if necessary and incorporate it with the code you write."
    "When you write code, include brief short comments to explain necessary portions." 
    "Respond only with the code and the comments within the code."
    "Make sure all the requirements are satisfied by the code you write."
    "Do not respond with text, respond with only code."
    "Another agent may run your code, if it fails fix the error within the code.",
    llm_config=codellama_config,
    #description="I am responsible for writing the source code"
)

if __name__ == "__main__":
    # Create the agent that represents the user in the conversation.
    user_proxy = UserProxyAgent("user", code_execution_config=False)

    # Let the assistant start the conversation.  It will end when the user types exit.
    source_code_writer.initiate_chat(user_proxy, message="How can I help you today?")