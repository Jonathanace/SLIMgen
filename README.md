# SLIMgen

> Authors: Aaron Lin, Raul Razo, Jonathan Emmons, Yuchen Zhu

## Overview

SLIMgen is an innovative project initially developed during the DS-PATH Summer Fellowship at NASA JPL and the University of California, Riverside. This project leverages multi-agent collaboration to automate software development, from requirement generation to code execution, using advanced AI models.

## Motivation

Software systems, particularly those at NASA, are often developed by multiple teams, leading to inconsistencies in project specifications. Additionally, many NASA software repositories lack standardized documentation and testing. SLIMgen aims to address these challenges by:<br>
Standardizing, governing, and modernizing software systems through the Software Lifecycle Improvement & Modernization (SLIM) initiative by NASA JPL.<br>
Utilizing AutoGen, an open-source framework by Microsoft, to enable multi-agent collaboration.

## Features

- Requirements Generation: Automatic generation of software requirements based on user prompts.
- Source Code Generation: Creation of source code that fulfills generated requirements.
- Test Code Generation: Automatic generation of test code using the produced requirements and source code.
- Code Execution: Running the generated source and test code automatically.
- Agent Collaboration: LLM agents simulate a human development team, working together to produce and validate code.
- Retrieval-Augmented Generation (RAG): Allows agents to read and incorporate external resources into their responses.

## Prototype
- A video demonstrating our DS-PATH Fellowship prototype. All agents are using llama3.1 as their LLM configuration.

[![Prototype Video](https://via.placeholder.com/600x400.png?text=Click+to+Watch+Video)](https://drive.google.com/file/d/1Vwhdo5Wuc7aDdFKWIqaKMjPur1SkNBAe/view?usp=sharing)

## TESTING.md Agent
- A video demonstrating our future work towards different agents, for example our dedicated Test Plan Writer agent. All agents are using llama3.1 as their LLM configuration.

[![Prototype Video](https://via.placeholder.com/600x400.png?text=Click+to+Watch+Video)](https://drive.google.com/file/d/1PFtjXdlCNw0gKBSi5WsXjmQ-73rM855N/view?usp=sharing)

## Future Work
- Increase the automation of agentic chats.
- Implement stricter speaker selection using activation phrases in nested chats.
- Automate cloning of GitHub repositories through tool use.
- Create dedicated agents for each step of continuous testing frameworks.


## Acknowledgments

This work is supported by the DS-PATH Summer Fellowship Program under the National Science Foundation Harnessing Data Revolution Data Science Corps Award #2123444, #2123271, #2123313.

The work detailed in this project was made possible through AutoGen, an open-source framework from Microsoft.

We would like to thank our industry mentor, Kyongsik Yun (NASA JPL), and our faculty mentors, Mariam Salloum and Analisa Flores, for their continued guidance and support throughout the program.


## Features

- Requirements Generation: Automatic generation of software requirements based on user prompts.
- Source Code Generation: Creation of source code that fulfills generated requirements.
- Test Code Generation: Automatic generation of test code using the produced requirements and source code.
- Code Execution: Running the generated source and test code automatically.
- Agent Collaboration: LLM agents simulate a human development team, working together to produce and validate code.
- Retrieval-Augmented Generation (RAG): Allows agents to read and incorporate external resources into their responses.

## Future Work
- Increase the automation of agentic chats.
- Implement stricter speaker selection using activation phrases in nested chats.
- Automate cloning of GitHub repositories through tool use.

## Acknowledgments

This work is supported by the DS-PATH Summer Fellowship Program under the National Science Foundation Harnessing Data Revolution Data Science Corps Award #2123444, #2123271, #2123313.

The work detailed in this project was made possible through AutoGen, an open-source framework from Microsoft.

We would like to thank our industry mentor, Kyongsik Yun (NASA JPL), and our faculty mentors, Mariam Salloum and Analisa Flores, for their continued guidance and support throughout the program.
