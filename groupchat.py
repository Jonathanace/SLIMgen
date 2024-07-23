import autogen
from configs import local_llm_config
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
        llm_config=local_llm_config,
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
        groupchat=groupchat, llm_config=local_llm_config
    )

    groupchat_result = user_proxy.initiate_chat(
        manager,
        message=task
    )

def groupchat2():
    user_proxy = UserProxyAgent(
        name="User",
        code_execution_config=False,
        llm_config=False,
        description="""
        Always select me as a speaker after 'requirements agent', 'Code Agent', or 'Unit Test Writer' speaks.
        """
    )

    graph_dict = {}
    graph_dict[user_proxy] = [requirement_writer, source_code_writer, test_writer]
    graph_dict[requirement_writer] = [user_proxy]
    graph_dict[source_code_writer] = [user_proxy]
    graph_dict[test_writer] = [user_proxy]

    agents = [user_proxy, requirement_writer, source_code_writer, test_writer]

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
        message="Calcultor that can do all the basic math functions",
        clear_history=True
    )




if __name__ == "__main__": 
    groupchat2()