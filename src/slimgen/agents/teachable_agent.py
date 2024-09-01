from autogen import ConversableAgent
import os
from configs import llama_3_1_config
from tools import read_code
from autogen import UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability

# The Number Agent always returns the same numbers.
description_agent = ConversableAgent(
    name="Description_Agent",
    system_message="You write a detailed but concise description on what the following file does currently. Do NOT provide any suggestions for future improvements, or refer to anything outside of what the code already does.",
    llm_config=llama_3_1_config,
    human_input_mode="NEVER",
)
# description_agent.llm_config["clear_history"] = True

teachable_memory_agent = ConversableAgent(
    name="Memory_Agent",
    system_message="You keep a list of descriptions of all the files in the project.",
    llm_config=llama_3_1_config,
    human_input_mode="NEVER"
)

teachability = Teachability(
    reset_db=False,  # Use True to force-reset the memo DB, and False to use an existing DB.
    path_to_db_dir="./tmp/interactive/teachability_db"  # Can be any path, but teachable agents in a group chat require unique paths.
)

teachability.add_to_agent(teachable_memory_agent
task = "What does examples/calculator/calculator.py do?"
project_dir = ''

# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
if __name__ == "__main__":
    teachable_memory_agent.reset()
    description_agent.reset()
    files = [
        'examples/calculator/calculator.py',
        'examples/fibonacci/fibonacci.py'
    ]
    for file in files:
        teachable_memory_agent.initiate_chat(description_agent, message=read_code(file), max_turns=2)

    questions = [
        "Write a README file for the project.", 
        "What does examples/calculator/calculator.py do?"
    ]


    
    for question in questions:
        response = teachable_memory_agent.generate_reply(messages=[{"content": question, "role": "user"}])
        print(question)
        print(response)


# Alternative method of teaching the agent 
# chat_results = teachable_memory_agent.initiate_chats(
#     [
#         {
#             "recipient": description_agent,
#             "message": read_code('examples/calculator/calculator.py'),
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#         {
#             "recipient": description_agent,
#             "message": read_code('examples/fibonacci/fibonacci.py'),
#             "max_turns": 2,
#             "summary_method": "last_msg",
#         },
#     ]
# )
# Change this to just normal chats, not consecutive chats. (MAYBE?)