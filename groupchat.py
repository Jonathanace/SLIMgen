import autogen
from autogen import UserProxyAgent, ConversableAgent
#from requirement_agent import requirement_agent
#from sourcecode_agent import sourcecode_agent
#from test_writer_agent import testwrite_agent
from autogen.agentchat import GroupChat, AssistantAgent, UserProxyAgent, GroupChatManager
from autogen.oai.openai_utils import config_list_from_dotenv
from configs import codellama_config

codellama_config = {
    "config_list": [
        {
            "model": "codellama",
            "base_url": "http://localhost:11434",
            "api_key": "codellama",
        }
    ]
}

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

testwrite_agent = ConversableAgent(
    name="Unit Test Writer",
    system_message="You are a quality assurance engineer that tests all functions in a given program."
    "The user will provide the code and functions for you to test."
    "You must write code to thoroughly (including edge cases) test each function."
    "You will print out the code for each unit test."
    "You will run the written code and test each function thoroughly.",
    llm_config=local_llm_config,
    description="""I am **ONLY** allowed to speak **immediately** after `User` and 'Code Agent'.
If `User` asks to generate test code given source code provided by 'Code Agent', the next speaker must be `Unit Test Writer`.
"""
)

user_proxy = UserProxyAgent(
    name="User",
    code_execution_config=False,
    llm_config=False,
    description="""
Always select me as a speaker after 'requirements agent', 'Code Agent', or 'Unit Test Writer' speaks.
"""
)

graph_dict = {}
graph_dict[user_proxy] = [requirement_agent, sourcecode_agent, testwrite_agent]
graph_dict[requirement_agent] = [user_proxy]
graph_dict[sourcecode_agent] = [user_proxy]
graph_dict[testwrite_agent] = [user_proxy]

agents = [user_proxy, requirement_agent, sourcecode_agent, testwrite_agent]

# create the groupchat
group_chat = GroupChat(agents=agents, messages=[], max_round=6, allowed_or_disallowed_speaker_transitions=graph_dict, allow_repeat_speaker=None, speaker_transitions_type="allowed")

# create the manager
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=local_llm_config,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
)

user_proxy.initiate_chat(
    manager,
    message="Python calculator class that can do addition and subtraction",
    clear_history=True
)