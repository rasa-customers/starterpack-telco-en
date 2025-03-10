# starterpack-telco-en

## Rasa Starter Pack: Telecom in English
<p align="center">
  <img src="images/telecom.png" alt="Alt Text">
</p>

Rasa has created a new starter pack for building AI assistants in Telecom with the Rasa CALM framework.
This repository contains a Rasa chatbot designed to assist customers with common internet service issues. The chatbot currently supports two primary flows:

- Troubleshooting Slow Internet
  - In this flow we help the user solve the issue what the chatbot can do for the user
    - run diagnostics : to make sure the speed test is in order
    - reset the router for the user if restarting the router doesn't help. resetting router is an action that the bot will perform, restarting the bot is ans action that we ask the user to do.
- Checking and Managing Bills
  - run custom actions the check our DataBase(in our case our CSV)
  - give a recap on the expensed the user is having
  - connect them to a human agent if needed and make sure they always have a way to get their answer.

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
  - **Config:** Contains multiple configuration components for the assistant (i.e. different language models and settings). since Intents are added then we need the NLU pipeline for it(tokennizer, featurizer, intent classifier ..) and **NLUCommandAdaptor** will be the component that will start a flow based on the intent prediction.
  - **Credentials**: Contains credentials for various services used by the Rasa assistant (i.e. Chat Widget)
  - **Endpoints**: Contains endpoint configurations for the Rasa assistant. 
    - How to run the action server is added
    - How to call NLG server
    - How to define the model group

# Conversation Examples
 ![conversation example](images/conversation_example.png)

# Features and bot content explanation.
 You can find in this bot
 - **Actions** : custom actions, mimic getting information from a DB, either adding it to the session start or afterwards in the conversation. I mimic this behavior by getting information about customers from two CSVs.
 - **RAG** : enterprise search if the ask knowledge base questions
 - **Data**
  - **Flows** : are build to handle user questions about "internet is slow" or "check their bill". Different features are used : calling or linking a flow, branching on a slot value.
  - **NLU** : Some flows will be triggered by NLU and if the confidence level is not too high then we can rely on our LLM. This usually used when we have a good set of examples for generic intents, like greet/goodbye, bot challenge ...
  You can use `nlu_trigger`
  - **Patterns** : Over-ride some patterns, to change the behavior. make sure to add the same patterns name as the originals.
 - **Documents** : have general information on what is a router how to start it ... this can be triggered at any point of the conversation and then the assistant will go back to finish the flow
 - **Domain** : contains all bot answeres, details/definition about all slots and mention the custom actions
  - **Responses** : I added simple once, one with buttons and others with images
  - ***Slots** : different slot type and mapping
    - **type** : Float, text, bool
    - **mappings** : from_llm, and custom
 - **Images** : These images are used in the README
 - **Prompts** : This prompt looks like the original, I just remove the **CHITCHAT** command and added details for the `SearchAndReply()`. in the config you can see that I pointed to use this prompt.
 - **Tests** : this is a good way to test the bot's capabilities and ensure the same behavior when doing changes and updates. With Assertions we can track commands and when slots are set.
 - **Config**  


# Installation

## Prerequisites
- Rasa licence for 3.11 +
- Python 3.10 +
- Point to the LLM provider in the endpoint.yml and config.yml 
  it can be open AI, finetuned model or any other LLM provider see [here](https://rasa.com/docs/rasa-pro/concepts/components/llm-configuration-from-3-11)

## Set up 

- Clone the repository:

  ```shell
  git clone <rasa-customers/starterpack-telco-en.git>
  cd <rasa-customers/starterpack-telco-en>
  ```

- Create and activate a virtual environment, you can use `venv` (built-in Python virtual environment) or any other virtual environment manager.

```shell
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
```

- Train the Rasa model: `rasa train`


# Running the Bot
- To run the bot you can use `rasa inspect --debug`
- After any changes made to your data, domain folder or config file you need to retrain the bot running `rasa train` and if changes are made in the custom actions just re-run `rasa inspect --debug`
- you can also add `e2e test cases` and ras `rasa test` to see how the bot is performing

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
- This project is licensed under the MIT? License. ?????
