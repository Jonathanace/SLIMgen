from autogen import ConversableAgent
import os
from configs import llama_3_1_config
from tools import read_code
from autogen import UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability
import glob
from pathlib import Path
from pprint import pprint

llama_3_1_config["price"] = [0, 0]

# The Number Agent always returns the same numbers.

# description_agent.llm_config["clear_history"] = True

task = "What does examples/calculator/calculator.py do?"
project_dir = ''

def train_teachable_agent(project_path, memory_path="./tmp/interactive/teachability_db", reset=False):
    if not reset:
        if os.path.isdir(memory_path):
            print('Loading memory...')
            mem_ok = True
        else:
            print(f'No memory found at {memory_path}')

    teachable_memory_agent = ConversableAgent(
        name="Memory_Agent",
        system_message="Your memorize what each file in the project does. Always remember the full filepath of each file.",
        llm_config=llama_3_1_config,
        human_input_mode="NEVER"
        )
    teachability = Teachability(
        reset_db=reset,  # Use True to force-reset the memo DB, and False to use an existing DB.
        path_to_db_dir=memory_path  # Can be any path, but teachable agents in a group chat require unique paths.
    )
    teachability.add_to_agent(teachable_memory_agent)

    if not mem_ok: # Train the memory agent 
        description_agent = ConversableAgent(
            name="Description_Agent",
            system_message="You write a detailed but concise description on what the following file does currently. Do NOT provide any suggestions for future improvements, or refer to anything outside of what the code already does. Start each message by repeating the file's path.",
            llm_config=llama_3_1_config,
            human_input_mode="NEVER",
        )

        files = list(Path(project_path).rglob("*.py"))

        for file in files:
            message = f'{file}\n{read_code(file)}'
            teachable_memory_agent.initiate_chat(description_agent, message=message, max_turns=2, silent=False)

    return teachable_memory_agent

    



# Start a sequence of two-agent chats.
# Each element in the list is a dictionary that specifies the arguments
# for the initiate_chat method.
if __name__ == "__main__":

    memory_agent = train_teachable_agent("examples/unity-initiator")
    
    questions = [
        """Fill out the following README.MD template using information from the files provided to you:
<!-- Header block for project -->
<hr>

<div align="center">

[INSERT YOUR LOGO IMAGE HERE (IF APPLICABLE)]
<!-- ☝️ Replace with your logo (if applicable) via ![](https://uri-to-your-logo-image) ☝️ -->
<!-- ☝️ If you see logo rendering errors, make sure you're not using indentation, or try an HTML IMG tag -->

<h1 align="center">[INSERT YOUR REPO / PROJ NAME HERE]</h1>
<!-- ☝️ Replace with your repo name ☝️ -->

</div>

<pre align="center">[INSERT A SINGLE SENTENCE DESCRIBING THE PURPOSE OF YOUR REPO / PROJ]</pre>
<!-- ☝️ Replace with a single sentence describing the purpose of your repo / proj ☝️ -->

<!-- Header block for project -->

[INSERT YOUR BADGES HERE (SEE: https://shields.io)] [![SLIM](https://img.shields.io/badge/Best%20Practices%20from-SLIM-blue)](https://nasa-ammos.github.io/slim/)
<!-- ☝️ Add badges via: https://shields.io e.g. ![](https://img.shields.io/github/your_chosen_action/your_org/your_repo) ☝️ -->

[INSERT SCREENSHOT OF YOUR SOFTWARE, IF APPLICABLE]
<!-- ☝️ Screenshot of your software (if applicable) via ![](https://uri-to-your-screenshot) ☝️ -->

[INSERT MORE DETAILED DESCRIPTION OF YOUR REPOSITORY HERE]
<!-- ☝️ Replace with a more detailed description of your repository, including why it was made and whom its intended for.  ☝️ -->

[INSERT LIST OF IMPORTANT PROJECT / REPO LINKS HERE]
<!-- example links>
[Website](INSERT WEBSITE LINK HERE) | [Docs/Wiki](INSERT DOCS/WIKI SITE LINK HERE) | [Discussion Board](INSERT DISCUSSION BOARD LINK HERE) | [Issue Tracker](INSERT ISSUE TRACKER LINK HERE)
-->

## Features

* [INSERT LIST OF FEATURES IMPORTANT TO YOUR USERS HERE]

<!-- ☝️ Replace with a bullet-point list of your features ☝️ -->

## Contents

* [Quick Start](#quick-start)
* [Changelog](#changelog)
* [FAQ](#frequently-asked-questions-faq)
* [Contributing Guide](#contributing)
* [License](#license)
* [Support](#support)

## Quick Start

This guide provides a quick way to get started with our project. Please see our [docs]([INSERT LINK TO DOCS SITE / WIKI HERE]) for a more comprehensive overview.

### Requirements

* [INSERT LIST OF REQUIREMENTS HERE]

<!-- ☝️ Replace with a numbered list of your requirements, including hardware if applicable ☝️ -->

### Setup Instructions

1. [INSERT STEP-BY-STEP SETUP INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a numbered list of how to set up your software prior to running ☝️ -->

### Run Instructions

1. [INSERT STEP-BY-STEP RUN INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a numbered list of your run instructions, including expected results ☝️ -->

### Usage Examples

* [INSERT LIST OF COMMON USAGE EXAMPLES HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a list of your usage examples, including screenshots if possible, and link to external documentation for details ☝️ -->

### Build Instructions (if applicable)

1. [INSERT STEP-BY-STEP BUILD INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a numbered list of your build instructions, including expected results / outputs with optional screenshots ☝️ -->

### Test Instructions (if applicable)

1. [INSERT STEP-BY-STEP TEST INSTRUCTIONS HERE, WITH OPTIONAL SCREENSHOTS]

<!-- ☝️ Replace with a numbered list of your test instructions, including expected results / outputs with optional screenshots ☝️ -->

## Changelog

See our [CHANGELOG.md](CHANGELOG.md) for a history of our changes.

See our [releases page]([INSERT LINK TO YOUR RELEASES PAGE]) for our key versioned releases.

<!-- ☝️ Replace with links to your changelog and releases page ☝️ -->

## Frequently Asked Questions (FAQ)

[INSERT LINK TO FAQ PAGE OR PROVIDE FAQ INLINE HERE]
<!-- example link to FAQ PAGE>
Questions about our project? Please see our: [FAQ]([INSERT LINK TO FAQ / DISCUSSION BOARD])
-->

<!-- example FAQ inline format>
1. Question 1
- Answer to question 1
2. Question 2
- Answer to question 2
-->

<!-- example FAQ inline with no questions yet>
No questions yet. Propose a question to be added here by reaching out to our contributors! See support section below.
-->

<!-- ☝️ Replace with a list of frequently asked questions from your project, or post a link to your FAQ on a discussion board ☝️ -->

## Contributing

[INSERT LINK TO CONTRIBUTING GUIDE OR FILL INLINE HERE]
<!-- example link to CONTRIBUTING.md>
Interested in contributing to our project? Please see our: [CONTRIBUTING.md](CONTRIBUTING.md)
-->

<!-- example inline contributing guide>
1. Create an GitHub issue ticket describing what changes you need (e.g. issue-1)
2. [Fork](INSERT LINK TO YOUR REPO FORK PAGE HERE, e.g. https://github.com/my_org/my_repo/fork) this repo
3. Make your modifications in your own fork
4. Make a pull-request in this repo with the code in your fork and tag the repo owner / largest contributor as a reviewer

**Working on your first pull request?** See guide: [How to Contribute to an Open Source Project on GitHub](https://kcd.im/pull-request)
-->

[INSERT LINK TO YOUR CODE_OF_CONDUCT.md OR SHARE TEXT HERE]
<!-- example link to CODE_OF_CONDUCT.md>
For guidance on how to interact with our team, please see our code of conduct located at: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
-->

<!-- ☝️ Replace with a text describing how people may contribute to your project, or link to your contribution guide directly ☝️ -->

[INSERT LINK TO YOUR GOVERNANCE.md OR SHARE TEXT HERE]
<!-- example link to GOVERNANCE.md>
For guidance on our governance approach, including decision-making process and our various roles, please see our governance model at: [GOVERNANCE.md](GOVERNANCE.md)
-->

## License

See our: [LICENSE](LICENSE)
<!-- ☝️ Replace with the text of your copyright and license, or directly link to your license file ☝️ -->

## Support

[INSERT CONTACT INFORMATION OR PROFILE LINKS TO MAINTAINERS AMONG COMMITTER LIST]

<!-- example list of contacts>
Key points of contact are: [@github-user-1](link to github profile) [@github-user-2](link to github profile)
-->

<!-- ☝️ Replace with the key individuals who should be contacted for questions ☝️ -->""", 
        # "What does examples/calculator/calculator.py do?"
    ]
    
    questions = ["Write a README.md file for the unity-initiator repository."]

    for question in questions:
        response = memory_agent.generate_reply(messages=[{"content": question, "role": "user"}])
        pprint(question)
        pprint(response)


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