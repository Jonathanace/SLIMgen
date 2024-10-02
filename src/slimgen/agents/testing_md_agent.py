import autogen
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from .configs import llama_3_1_config

# llama_3_1_config = {
#     "config_list": [
#         {
#             "model": "llama3.1",
#             "base_url": "http://localhost:11434/v1",
#             "api_key": "ollama"
#         }

#     ]
    
# }

llama_3_1_config["price"] = [0, 0]

# Start a groupchat of a three agent chat: user_proxy, testing_md_agent, and testing_md_critic
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
if __name__ == "__main__":

    user_proxy = UserProxyAgent(
        name="User Proxy",
        system_message="A human admin.",
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    testing_md_critic = autogen.AssistantAgent(
        name="TESTING.md Critic",
        system_message="""
        You are a critic. Double check plans, claims, and code from other agents and provide feedback.
        You will be reviewing the TESTING.md file created by the Test Plan Writer.
        You will create feedback for the Test Plan Writer on how to improve the TESTING.md. 
        Check whether the testing plan covers all possible testing categories.
        Check whether the testing plan covers all necessary sections for the testing categories it already has.
        Do **NOT** create your own TESTING.md, just provide written feedback.
        Review this TESTING.md template to check if the Test Plan Writer's own markdown file has all the required sections.
        
        # [INSERT PROJECT NAME HERE] Testing

        ## Introduction
        This document provides an overview of the testing architecture for [INSERT PROJECT NAME HERE]. It encompasses continuous testing concepts such as testing across the software development lifecycle as well as automated execution of tests through automation. 

        ---

        ## Testing Categories

        The below list of test categories are included in our testing setup. Further details are provided below.

        <!-- ADD / MODIFY BELOW CATEGORIES TO AS NEEDED -->
        - [ ] **Static Code Analysis:** checks code for syntax, style, vulnerabilities, and bugs
        - [ ] **Unit Tests:** tests functions or components to verify that they perform as intended
        - [ ] **Security Tests:** identifies potential security vulnerabilities
        - [ ] **Build Tests:** checks if the code builds into binaries or packages successfully
        - [ ] **Acceptance Tests:** validates against end-user & stakeholder requirements

        <!-- CHOOSE MORE FROM THE BELOW LIST OR CREATE YOUR OWN
        - [ ] **Integration Tests**
        - [ ] **System Tests**
        - [ ] **Performance Tests**
        - [ ] **Security Tests**
        - [ ] **Usability Tests**
        - [ ] **Regression Tests**
        - [ ] **Smoke Tests**
        -->

        <!-- REPEAT THIS SECTION AS NEEDED FOR ABOVE CATEGORIES -->
        ### [INSERT TESTING CATEGORY HERE] Tests

        <!-- ADD SUB-BLOCKS AS NEEDED FOR MULTIPLE TEST FILES OR GROUPS WITHIN SAME CATEGORY ABOVE -->
        <!-- #### [INSERT SUB-CATEGORY NAME IF MORE THAN ONE SUB-BLOCK] -->
        - Location: `[INSERT RELATIVE PATH TO SUB-FOLDER / FILE / FILE PATTERN HERE]`
        - Purpose: [INSERT A 1-SENTENCE PURPOSE STATEMENT FOR TEST HERE]
        - Running Tests:
        - Manually:
            1. [INSERT STEP 1]
            2. [INSERT STEP 2]
            3. [INSERT WHERE TO VIEW RESULTS]
        - Automatically:
            - Frequency:
            - [INSERT TRIGGER OF WHAT KICKS OFF YOUR TESTS, E.G. CODE CHANGES, COMMITS, ETC.]
            - [INSERT TIMING OF WHEN YOUR TESTS KICK OFF, E.G. NIGHTLY, EVERY WEEK, ETC.]
            - Results Location: `[INSERT PATH OR LOCATION WHERE RESULTS WILL RESIDE]`
        - Contributing:
        - Framework Used: [INSERT YOUR TESTING FRAMEWORK OF CHOICE]
        - Tips:
            - [INSERT TIPS ON CONTRIBUTING TESTS HERE]
            <!-- e.g. 
            - Test every non-trivial function or method in your code
            - Test conditions including malformed arguments and null conditions
            >  
        """,
        llm_config=llama_3_1_config,
    )

    testing_md_agent = autogen.AssistantAgent(
        name="TESTING.md Agent",
        system_message="""
        You are part of a development team tasked with making a continuous testing plan for the software your team is given. 
        Your specific job is to create a TESTING.md file that outlines the testing objectives and plans for the software in an easy-to-find location. 
        A critic will review the TESTING.md you create.
        After rewriting the TESTING.md to address the feedback, reply with a new TESTING.md including your changes.
        Do **NOT** reply with just the changes you make to your TESTING.md, reply with the entire TESTING.md.
        This file will provide your development team and contributors with:

        A list of the types of tests you run against your software.
        Locations where your tests are defined.
        When and how your tests are run.
        How to contribute/modify tests.

        Having this information in a single file helps guide your testing journey and adds clarity for your team.

        Use this TESTING.md template in every reply and do not stray away from the template under any circumstance.
        Do NOT create any new sub categories that are not in the template.
        Ensure the contents of the template are clear enough to where someone can write test cases from looking at the TESTING.md you create.

        # [INSERT PROJECT NAME HERE] Testing

        ## Introduction
        This document provides an overview of the testing architecture for [INSERT PROJECT NAME HERE]. It encompasses continuous testing concepts such as testing across the software development lifecycle as well as automated execution of tests through automation. 

        ---

        ## Testing Categories

        The below list of test categories are included in our testing setup. Further details are provided below.

        <!-- ADD / MODIFY BELOW CATEGORIES TO AS NEEDED -->
        - [ ] **Static Code Analysis:** checks code for syntax, style, vulnerabilities, and bugs
        - [ ] **Unit Tests:** tests functions or components to verify that they perform as intended
        - [ ] **Security Tests:** identifies potential security vulnerabilities
        - [ ] **Build Tests:** checks if the code builds into binaries or packages successfully
        - [ ] **Acceptance Tests:** validates against end-user & stakeholder requirements

        <!-- CHOOSE MORE FROM THE BELOW LIST OR CREATE YOUR OWN
        - [ ] **Integration Tests**
        - [ ] **System Tests**
        - [ ] **Performance Tests**
        - [ ] **Security Tests**
        - [ ] **Usability Tests**
        - [ ] **Regression Tests**
        - [ ] **Smoke Tests**
        -->

        <!-- REPEAT THIS SECTION AS NEEDED FOR ABOVE CATEGORIES -->
        ### [INSERT TESTING CATEGORY HERE] Tests

        <!-- ADD SUB-BLOCKS AS NEEDED FOR MULTIPLE TEST FILES OR GROUPS WITHIN SAME CATEGORY ABOVE -->
        <!-- #### [INSERT SUB-CATEGORY NAME IF MORE THAN ONE SUB-BLOCK] -->
        - Location: `[INSERT RELATIVE PATH TO SUB-FOLDER / FILE / FILE PATTERN HERE]`
        - Purpose: [INSERT A 1-SENTENCE PURPOSE STATEMENT FOR TEST HERE]
        - Running Tests:
        - Manually:
            1. [INSERT STEP 1]
            2. [INSERT STEP 2]
            3. [INSERT WHERE TO VIEW RESULTS]
        - Automatically:
            - Frequency:
            - [INSERT TRIGGER OF WHAT KICKS OFF YOUR TESTS, E.G. CODE CHANGES, COMMITS, ETC.]
            - [INSERT TIMING OF WHEN YOUR TESTS KICK OFF, E.G. NIGHTLY, EVERY WEEK, ETC.]
            - Results Location: `[INSERT PATH OR LOCATION WHERE RESULTS WILL RESIDE]`
        - Contributing:
        - Framework Used: [INSERT YOUR TESTING FRAMEWORK OF CHOICE]
        - Tips:
            - [INSERT TIPS ON CONTRIBUTING TESTS HERE]
            <!-- e.g. 
            - Test every non-trivial function or method in your code
            - Test conditions including malformed arguments and null conditions
            >  

        """,
        llm_config=llama_3_1_config
    )

    # Graph of allowed speaker transitions
    graph_dict = {}
    graph_dict[user_proxy] = [testing_md_agent]
    graph_dict[testing_md_agent] = [testing_md_critic]
    graph_dict[testing_md_critic] = [testing_md_agent]

    # Initialize groupchat with 8 rounds of agent interaction
    groupchat = autogen.GroupChat(
        agents=[user_proxy, testing_md_agent, testing_md_critic], 
        messages=[], 
        max_round=8,
        allowed_or_disallowed_speaker_transitions=graph_dict,
        speaker_transitions_type="allowed",
    )

    # Create groupchat manager
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llama_3_1_config)

    # Initiate groupchat with custom message
    user_proxy.initiate_chat(
        manager, 
        message="""
        Create a testing plan using the TESTING.md template for this Calculator class. Here is the code:
        class Calculator:
            def add(self, a=0, b=0):
                result = a + b
                print(f"Result of {a} + {b} = {result}")
                return result

            def subtract(self, a=0, b=0):
                result = a - b
                print(f"Result of {a} - {b} = {result}")
                return result
        """
    )

    # Ctrl + c to terminate chat before max round has been reached