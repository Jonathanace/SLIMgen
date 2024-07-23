import autogen
from configs import *
from agents import *
from autogen import UserProxyAgent, ConversableAgent
from autogen.agentchat import GroupChat, AssistantAgent, UserProxyAgent, GroupChatManager

def groupchat():
    task = "Write a blogpost about the stock price performance of"\
    "Nvidia in the past month. Today's date is 2024-07-20"

    user_proxy = autogen.ConversableAgent(
        name="Admin",
        system_message="Give the task, and send "
        "instructions to writer to refine the blog post.",
        code_execution_config=False,
        llm_config=codellama_config,
        human_input_mode="ALWAYS",
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, requirement_writer, source_code_writer, test_writer],
        messages=[],
        max_round=10,
        allowed_or_disallowed_speaker_transitions={
            user_proxy: [requirement_writer,  source_code_writer, test_writer], 
            requirement_writer: [user_proxy, source_code_writer],
            source_code_writer: [user_proxy, source_code_writer],
            test_writer: [user_proxy, source_code_writer]
        },
    speaker_transitions_type="allowed",
    )

    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llama_2_config
    )

    groupchat_result = user_proxy.initiate_chat(
        manager,
        message=task
    )




if __name__ == "__main__": 
    groupchat()