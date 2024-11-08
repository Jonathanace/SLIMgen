# langgraph implementation
# Using llama.cpp


# using ollama
# easier installation, use, changing models
# ONLY supports structured output in json format

from langchain_ollama import OllamaLLM, ChatOllama
from pydantic import BaseModel, Field, model_validator
from typing_extensions import TypedDict, Annotated
from langchain_ollama import ChatOllama
from pprint import pprint
import webbrowser
import os
import markdown

output_dir = os.path.dirname(os.path.abspath(__file__))

def md_to_html(markdown_content):
    html_content = markdown.markdown(markdown_content)
    html_file_name = "output.html"
    html_file_path = os.path.join(output_dir, html_file_name)
    with open(html_file_path, "w", encoding="utf-8") as file: 
        file.write(html_content)
    webbrowser.open(f"file://{html_file_path}")

class readme(BaseModel):
    """Information for a README.md file"""

    repo_name: str = Field(description="the name of the repo")
    description: str = Field(description="a single sentence describing the purpose of the repo")
    features: str = Field(description="a bullet-point list of repo features")
    requirements: str = Field(description="a numbered list of requirements, including hardware if applicable")
    setup_instructions: str = Field(description="a numbered list of how to set up the software prior to running")
    run_instructions: str = Field(description="a numbered list of run instructions, including expected results")
    usage_examples: str = Field(description="a list of  usage examples, including screenshots if possible, and link to external documentation for details")
    build_instructions: str = Field(description="a numbered list of build instructions, including expected results / outputs with optional screenshots")

readme_template = """
<!-- Header block for project -->
<hr>

<div align="center">

[INSERT YOUR LOGO IMAGE HERE (IF APPLICABLE)]
<!-- ☝️ Replace with your logo (if applicable) via ![](https://uri-to-your-logo-image) ☝️ -->
<!-- ☝️ If you see logo rendering errors, make sure you're not using indentation, or try an HTML IMG tag -->

<h1 align="center">{}</h1>


</div>

<pre align="center">{}</pre>


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
{}

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
{}

### Setup Instructions
{}

### Run Instructions
{}

### Usage Examples
{}

### Build Instructions (if applicable)
{}
"""

llm = ChatOllama(model="llama3.1")
structured_llm = llm.with_structured_output(readme)
readme_data = structured_llm.invoke("Create a README.md file for a calculator program")

formatted_readme = readme_template.format(
    readme_data.repo_name,
    readme_data.description,
    readme_data.features,
    readme_data.requirements,
    readme_data.setup_instructions,
    readme_data.run_instructions,
    readme_data.usage_examples,
    readme_data.build_instructions
)

pprint(formatted_readme)

file_name = "output.md"
file_path = os.path.join(output_dir, file_name)

with open(file_path, "w+", encoding="utf-8") as file:
    file.write(formatted_readme)

md_to_html(formatted_readme)