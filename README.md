# starterpack-telco-en

## Rasa Starter Pack: Telecom in English
<p align="center">
  <img src="images/telecom.png" alt="Alt Text">
</p>

Rasa has created a new starter pack for building AI assistants in Telecom with the Rasa CALM framework.
This repository contains a Rasa chatbot designed to assist customers with common internet service issues. The chatbot currently supports two primary flows:

- Troubleshooting Slow Internet
- Checking and Managing Bills

You can use this demo assistant as a starting point for your own Telecom Intelligent Assistant, or get ideas for features you might want to implement. It's free for you to copy and use locally with the Rasa Pro Developer Edition.

# Project Structure

Here's a brief description of the directories and files in the project root:
  - **README.md**: The file you're currently reading!
  - **actions:** Contains Python scripts defining custom actions for the Rasa assistant.
  - **csvs:** Contains csv file that are used to mimic the behavior of connecting to a database to get customer information.
  - **data:** Contains flow definitions for the assistant and NLY folder, for flows to be triggered by some intents.
  - **docs:** Contains sample documents for Enterprise Search.
  - **domain:** Contains domain files for the assistant.
  - **prompts**: Contains Jinja2 template files for generating prompts.
  - **tests:** Contains end-to-end test scenarios for the assistant where each subdirectory reflects a suite of tests (i.e. happy path).
  - **configs:** Contains multiple configuration files for the assistant (i.e. different language models and settings).
  - **credentials.yml**: Contains credentials for various services used by the Rasa assistant (i.e. Chat Widget)
  - **endpoints.yml**: Contains endpoint configurations for the Rasa assistant.

# Installation

## Prerequisites
- Rasa licence for 3.11 +
- Python 3.10 +
- Point to the LLM provider in the endpoint.yml and config.yml 
  it can be open AI, finetuned model or any other LLM provider see [here](https://rasa.com/docs/rasa-pro/concepts/components/llm-configuration-from-3-11)
  
## Set up 

- Clone the repository:
```git clone <rasa-customers/starterpack-telco-en.git>
cd <rasa-customers/starterpack-telco-en.gite>
```

- Create and activate a virtual environment, you can use `venv`(built-in Python virtual environment) or any other virtual environment manager.
```python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

- Train the Rasa model:
`rasa train`


# Running the Bot
- To run the bot you can use `rasa inspect --debug`
- After any changes made to your data, domain folder or config file you need to retrain the bot running `rasa train` and if changes are made in the custom actions just re-run `rasa inspect --debug`

# Tips

- when you are trying to debug look for these sections
  - Always review the prompt
  - search for `action_list` to see the command that was predicted by CALM, this will help you debug
    For instance, it can be `action_list=StartFlow(understand_bill)` or `action_list=SetSlot(bill_date, 2025-01-01)`
- search for `commands=` 
  For instance `commands=[StartFlowCommand(flow='bot_challenge')]`

# Contributing
Feel free to fork this repo and submit pull requests. Suggestions and improvements are always welcome!

# License
- This project is licensed under the MIT License.
