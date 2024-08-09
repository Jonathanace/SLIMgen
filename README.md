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
