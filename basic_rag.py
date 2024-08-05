from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent
from configs import llama_3_config


problem = "What are the key components of a good requirement?"


# NO-RAG AGENTS
no_rag_agent = AssistantAgent(
    name="NO-RAG Agent",
    llm_config=llama_3_config,
    human_input_mode="NEVER"
)

user_proxy = UserProxyAgent(name="user_proxy", code_execution_config=False)


# RAG AGENTS
rag_assistant_agent = RetrieveAssistantAgent(
    name="RAG Assistant Agent",
    system_message="You are a helpful assistant.",
    llm_config=llama_3_config,
    human_input_mode="NEVER"
)

rag_agent = RetrieveUserProxyAgent(
    name="RAG Agent",
    retrieve_config={
        "task": "qa",
        "docs_path": "./nasa_requirements.txt",
        "model": "llama3",
        "get_or_create": True,
    },
    human_input_mode="NEVER"
)


# TEST
rag_assistant_agent.reset()

print("NO RAG CHAT")
print("")
norag_response = user_proxy.initiate_chat(no_rag_agent, message=problem, max_turns=1)

rag_assistant_agent.reset()

print("RAG CHAT")
print("")
rag_response = rag_agent.initiate_chat(rag_assistant_agent, message=rag_agent.message_generator, problem=problem)
