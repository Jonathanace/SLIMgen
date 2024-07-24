import autogen
from autogen import register_function
from configs import *, codellama_config
from agents import *
from autogen import UserProxyAgent, ConversableAgent
from autogen.agentchat import GroupChat, AssistantAgent, UserProxyAgent, GroupChatManager
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor
from typing import Dict, List
from autogen import Agent

from tools import code_reader

def groupchat():
    task = "Analyze the code found in examples/calculator/calculator.py"

    user_proxy = autogen.ConversableAgent(
        name="Admin",
        system_message="Give the task, and send "
        "instructions to writer to refine the blog post.",
        code_execution_config=False,
        llm_config=codellama_config,
        human_input_mode="ALWAYS",
    )

    executor = autogen.ConversableAgent(
        name="Executor",
        description="Execute the code written by the engineer and  report the result.",
        human_input_mode="NEVER",
        code_execution_config={
            "last_n_messages": 3,
            "work_dir": "coding",
            "use_docker": False
        }
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

    register_function(
        code_reader,
        caller=manager,
        executor=executor,
        name="code_reader",
        description="Read code from a file."
    )

    groupchat_result = user_proxy.initiate_chat(
        manager,
        message=task
    )

def groupchat_yzhu_graph():
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
        llm_config=llama_2_config,
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )

    user_proxy.initiate_chat(
        manager,
        message="Generate me requirements for a calculator that can do all the basic math functions",
        clear_history=True
    )

def groupchat_yzhu_cust():
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

    def custom_speaker_selection_func(last_speaker: Agent, groupchat: autogen.GroupChat):
        messages = groupchat.messages
        if last_speaker is user_proxy:
            if "NXcode" in messages[-1]["content"]:
                return source_code_writer
            elif "NXrequirements" in messages[-1]["content"]:
                return requirement_writer
            elif "NXtest" in messages[-1]["content"]:
                return test_writer
        else:
            return user_proxy

    # create the groupchat
    group_chat = GroupChat(
        agents=agents, 
        messages=[], 
        max_round=6, 
        allowed_or_disallowed_speaker_transitions=graph_dict, 
        allow_repeat_speaker=None, 
        speaker_transitions_type="allowed",
        speaker_selection_method=custom_speaker_selection_func
    )

    # create the manager
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=llama_2_config,
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )

    user_proxy.initiate_chat(
        manager,
        message="Generate me requirements for a calculator that can do all the basic math functions. NXrequirements",
        clear_history=True
    )

    
def groupchat_raul():
   user_proxy = autogen.ConversableAgent(
       name="User",
       system_message="Give the task, and send "
       "instructions to writer to refine the blog post.",
       code_execution_config=False,
       llm_config=codellama_config,
       human_input_mode="ALWAYS",


   )


   software_engineer = autogen.AssistantAgent(
       name="Software Engineer",
       llm_config=codellama_config,
        system_message = "Your goal is write code that satisfies the requirements provided."
        "If the user provides a list of requirements, you will generate code that satisfies those requrements." 
        "If the user also provides code, you will review the provided code, change it if necessary and incorporate it with the code you write."
        "When you write code, include brief short comments to explain necessary portions." 
        "Respond only with the code and the comments within the code."
        "Make sure all the requirements are satisfied by the code you write."
        "Do not respond with text, respond with only code.",
       description="A software engineer that writes code based on the requirements provided by "
       "the systems engineer.",
   )


   qa_engineer = autogen.ConversableAgent(
       name="Quality Assurance Engineer",
       system_message= "Write unit tests for the code written by the software engineer using the PyUnit testing framework."
       "If the test executor reports errors when executing the unit tests, revise your code to fix those errors.",
       description="A quality assurance engineer that writes tests cases using the PyUnit testing framework "
       "based off the code written by the software engineer.",
       llm_config=codellama_config,
   )


   sys_engineer = autogen.ConversableAgent(
       name="Systems Engineer",
       system_message="You are a systems engineer. The user tells you what they want their code to do"
       "and you write requirements for that code before that code is written."
       "You will list out these requirements in a numbered list."
       "You will not write the code, you will only write the requirements.",
       description="A systems engineer that writes requirements for code based off the user's prompt."
       "This is the first agent that will speak in the conversation.",
       llm_config=codellama_config,
   )


   executor = LocalCommandLineCodeExecutor(work_dir="coding")


   swe_executor = ConversableAgent(
       name="source code executor",
       system_message= """
       You execute the code written by the software engineer. You report the results and verify that
       there are no errors in the execution. You verify that the code written by the software engineer
       can run to completion without errors. If there are errors when executing the code, then you will tell the
       software engineer to rewrite the code to fix those errors. Once the code runs without errors, you will
       give the code to the quality assurance engineer so they can write test cases for it.
       """,
       description="""
       Code executor that executes code written by the software engineer.
       If there are errors with the execution, the software engineer will revise the code.
       Once the code executes successfully with no errors, then the quality assurance speaker
       will write test cases for it and the software engineer is NO LONGER NEEDED and can stop speaking.
       """,
       llm_config=False,
       code_execution_config={
           "executor": executor,
       },
       human_input_mode="NEVER",
   )


   test_executor = ConversableAgent(
       name="test case executor",
       system_message= """
       You execute the code written by the quality assurance engineer. You report the results and verify that
       there are no errors in the execution. You verify that the code written by the quality assurance engineer
       can run to completion without errors. If there are errors when executing the code, then you will tell the
       quality assurance engineer to rewrite the code to fix those errors. Once the code runs without errors, your job
       will be finished.
       """,
       description="""
       Code executor that executes code written by the quality assurance engineer.
       If there are errors with the execution, the quality assurance engineer will revise the code.
       Once the code executes successfully with no errors, then the code executor will no longer be needed.
       """,
       llm_config=False,
       code_execution_config={
           "executor": executor,
       },
       human_input_mode="NEVER",
   )


  


   graph_dict = {}
   graph_dict[user_proxy] = [sys_engineer]
   graph_dict[sys_engineer] = [software_engineer]
   graph_dict[software_engineer] = [swe_executor]
   graph_dict[swe_executor] = [qa_engineer, software_engineer]
   graph_dict[qa_engineer] = [user_proxy]


   agents = [user_proxy, sys_engineer, software_engineer, qa_engineer, swe_executor, test_executor]




   # create the groupchat
   group_chat = GroupChat(
       agents=agents,
       messages=[],
       max_round=20,
       speaker_selection_method="manual",
       allow_repeat_speaker=None,
       speaker_transitions_type="allowed",
       )


   # create the manager
   manager = GroupChatManager(
       groupchat=group_chat,
       llm_config=llama_3_config,
       is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
       code_execution_config=False,
   )


   user_proxy.initiate_chat(
       manager,
       message="Generate requirements for a Python class named \"Calculator\" with add and subtract functions stored in a file "
       "named \"calculator.py\"",
   )


if __name__ == "__main__": 
    groupchat_yzhu_cust()