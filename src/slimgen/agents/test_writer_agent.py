# Import libraries
from autogen import UserProxyAgent, ConversableAgent

# Docker libraries
from pathlib import Path
from autogen.coding import DockerCommandLineCodeExecutor

from .configs import codellama_config



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

# LLM-based agent
test_writer = ConversableAgent(
    name="Test Code Writer",
    system_message= "If the previous speaker is source code executor, you will ignore their message and generate test code based on the most recent provided source code."
    "You are a quality assurance engineer that writes test cases for all functions in a given program."
    "The user will provide the code and functions for you to test."
    "You must write code to thoroughly (including edge cases) test each function."
    "You will print out the code for each unit test."
    "You will reply with executable code for testing the source code."
    "If the previous speaker is test case executor, and if the test code executed correctly then report back what cases failed and how to fix them."
    "If the previous speaker is test case executor, and if the test code did not execute correctly then fix the test code and send the fixed test code.",
    llm_config = codellama_config,
    description = "I am responsible for writing test code. Select me as the speaker when the User asks for test code to be generated."
)

if __name__ == "__main__":
    # User agent
    user_proxy = UserProxyAgent("user", code_execution_config=False)


    # Assistant starts conversation. Ends when user types 'exit'.
    test_writer.initiate_chat(user_proxy, message="How can I help you today?")


    # Prompt: Write a python script to test each function of the following code:

    # Additional Prompt: Here is the code, please write a comprehensive set of unit tests to test all the functions: class Calculator:
    #   def add(a, b):      return a + b   def subtract(a, b):      return a - bdef main():   a=int(input("Enter a: "))   b=int(input("Enter b: "))   print(Calculator.add(a,b))   print(Calculator.subtract(a,b))if __name__ == "__main__":    main()