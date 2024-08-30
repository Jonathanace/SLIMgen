from autogen import ConversableAgent
import os
from configs import llama_3_1_config
from tools import read_code

# The Number Agent always returns the same numbers.
description_agent = ConversableAgent(
    name="Description_Agent",
    system_message="You write a detailed but concise description on what the following file does currently. Do NOT provide any suggestions for future improvements, or refer to anything outside of what the code already does.",
    llm_config=llama_3_1_config,
    human_input_mode="NEVER",
)
description_agent.llm_config["clear_history"] = False

memory_agent = ConversableAgent(
    name="Memory_Agent",
    system_message="You keep a list of descriptions of all the files in the project.",
    llm_config=llama_3_1_config,
    human_input_mode="NEVER"
)


task = "What does examples/calculator/calculator.py do?"

# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
if __name__ == "__main__":
    chat_results = memory_agent.initiate_chats(
        [
            {
                "recipient": description_agent,
                "message": read_code('examples/calculator/calculator.py'),
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": description_agent,
                "message": read_code('examples/fibonacci/fibonacci.py'),
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": memory_agent,
                "message": "What does examples/calculator/calculator.py do?",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": memory_agent,
                "message": "Write a README file for the project.",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
        ]
    )

# reply = memory_agent.generate_reply(messages=[{"content": task, "role": "user"}])
# print(reply)