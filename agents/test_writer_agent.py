# Import libraries
from autogen import UserProxyAgent, ConversableAgent

# Docker libraries
from pathlib import Path
from autogen.coding import DockerCommandLineCodeExecutor


# Docker implementation
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)

with DockerCommandLineCodeExecutor(work_dir=work_dir) as code_executor:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        code_execution_config={"work_dir": "web"},
    )


# Holds configuration parameters for LLM
config_list_unit_test_writer = [
    {
        "model": "NULL", # Model is set when running LiteLLM command
        "api_key": "NULL", # Not required if running locally
        "base_url": "http://0.0.0.0:4000"  # LiteLLM URL
    }
]

# LLM Configuration
local_llm_config={
    "config_list": config_list_unit_test_writer,
    "cache_seed": None # Disables caching, useful for testing different models without interference from previous results
}

# LLM-based agent
assistant = ConversableAgent(
    name="Unit Test Writer",
    system_message="You are a quality assurance engineer that tests all functions in a given program."
    "The user will provide the code and functions for you to test."
    "You must write code to thoroughly (including edge cases) test each function."
    "You will print out the code for each unit test."
    "You will run the written code and test each function thoroughly.",
    llm_config=local_llm_config,
)

if __name__ == "__main__":
    # User agent
    user_proxy = UserProxyAgent("user", code_execution_config=False)


    if __name__=="__main__":
        # Assistant starts conversation. Ends when user types 'exit'.
        assistant.initiate_chat(user_proxy, message="How can I help you today?")


    # Prompt: Write a python script to test each function of the following code:

    # Additional Prompt: Here is the code, please write a comprehensive set of unit tests to test all the functions: class Calculator:
    #   def add(a, b):      return a + b   def subtract(a, b):      return a - bdef main():   a=int(input("Enter a: "))   b=int(input("Enter b: "))   print(Calculator.add(a,b))   print(Calculator.subtract(a,b))if __name__ == "__main__":    main()