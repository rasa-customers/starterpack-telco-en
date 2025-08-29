# starterpack-telco-en

## Rasa Starter Pack: Telecom - English
<p align="center">
  <img src="images/Rasa_starterpack_telecom.png" alt="Rasa Telecom Starter Pack">
</p>

Rasa has created a new starter pack for building AI assistants in Telecom with the Rasa CALM framework.
This repository contains a Rasa chatbot designed to assist customers with common internet service issues. The chatbot currently supports two primary flows:

- Troubleshooting Slow Internet
  - In this flow we help the user solve the issue what the chatbot can do for the user
    - Run diagnostics : to make sure the speed test is in order.
    - Reset the router for the user if restarting the router doesn't help. Resetting router is an action that the bot will perform, restarting the bot is an action that we ask the user to do.
- Checking and Managing Bills
  - Run custom actions the check our DataBase (in our case our CSV).
  - Give a recap on the experience the user is having.
  - Connect them to a human agent if needed and make sure they always have a way to get their answer.

You can use this demo assistant as a starting point for your own Telecom Intelligent Assistant, or get ideas for features you might want to implement. It's free for you to copy and use locally with the Rasa Pro Developer Edition.

# Project Structure
Here's a brief description of the directories and files in the project root:
  - **README.md**: The file you're currently reading!
  - **actions:** Contains Python scripts defining custom actions for the Rasa assistant.
  - **csvs:** Contains csv files that are used to mimic the behavior of connecting to a database to get customer information.
  - **data:** Contains flow definitions for the assistant. If needed, flows can be triggered by some intents by adding the nlu file with examples for intents.
  - **docs:** Contains sample documents for Enterprise Search.
  - **domain:** Contains domain files for the assistant.
  - **prompts**: Contains Jinja2 template files for generating custom prompts.
  - **tests:** Contains end-to-end test scenarios for the assistant where each subdirectory reflects a suite of tests (i.e. happy path).
  - **config.yml** Contains configuration components for the assistant (e.g. different language models and settings).
  - **credentials.yml**: Contains credentials for various services used by the Rasa assistant (e.g. Chat Widget)
  - **endpoints.yml**: Contains endpoint configurations for the Rasa assistant.
    - How to run the action server is added
    - How to call NLG server
    - How to define the model group

# Conversation design
 ![conversation example](images/conversation_example.png)
# Conversation example
##  **First example**:<br>Happy path with solving "internet slow" issue
  - **Bot**: Hey Serena 👋
        I am your virtual AI assistant that can check your bills or resolve issues with Internet speed.
        How may I help you?
  - **User**: My internet is slow
  - **Bot**: <BR>
            I see. <BR>
            Let me try identify the root cause of the issue you are facing.<BR>
            I will run a network diagnostics for you 🛜 <BR>
            Wait a moment please... <BR>
            Thank you for waiting... ✅ <BR>
            Your network download speed is 53 Mbps. <BR>
            That's definitely not good. <BR>
            Let's reboot your router.
            It helps resolving most issues with speed.
            Please turn the router off, wait 10 seconds and turn it back on.
            Let me know when you are done!
  - **User**: Done
  - **Bot**: <BR>
            I will run a network diagnostics for you 🛜 <BR>
            Wait a moment please... <BR>
            Thank you for waiting... ✅ <BR>
            111 Mbps, Awesome! 🚀 <BR>
            If the Internet gets slow again, you can always reset the router. <BR>
            If that doesn't help, let me know, and we can try something else. 😊 <BR>

##  **Second example**:<br>Providing human agent help when needed in the "billing" use case
  - **User**: Can you explain my bill in detail? <BR>
  - **Bot**: <BR>
            Alright. Could you please specify the month? 📅
  - **User**: Feb
  - **Bot**: <BR>
            Your bill for February 2025 is $55.00.<BR>
            The average of your past bills is $88.50.<BR>
            This bill is lower than your average by $33.50.<BR>
            Would you like to see the breakdown of the costs?
  - **User**: Nope
  - **Bot**: Did I manage to provide all the information you need?
  - **User**: No
  - **Bot**: <BR>
            Let me connect you to our human support managers. They will help you further! <BR>
          Please hold on while I connect you to our expert 📲 <BR>

##  **Third example**:<br>Intervening and asking a knowledge questions base during a conversation
  - **User**: My internet is so slow lately
  - **Bot**: <BR>
          I see.
          Let me try identify the root cause of the issue you are facing.<BR>
          I will run a network diagnostics for you 🛜<BR>
          Wait a moment please... <BR>
          .. 10 second pass ..  <BR>
          Thank you for waiting... ✅   <BR>
          102 Mbps sounds right. The speed seems to be in order.<BR>
          The result of my test shows that there is no technical issues between your home and our core network.<BR>
          However, if you're still experiencing slow browsing or buffering,it could be due to network congestion, too many connected devices, or Wi-Fi interference.<BR>
          Try moving closer to your router or disconnecting unused devices.<BR>
          I can connect you to a human agent for further assistance. <BR>
          Would you like me to do that now?<BR>
  - **User**: "what is a speed test"
  - **Bot**: <BR>
          A speed test is a process run by specific software to measure the performance of your internet connection. <BR>
          It evaluates your download and upload speeds, latency, and jitter to determine how fast data is sent and received. This can impact activities like streaming, gaming, and video calls.<BR>
  - **Bot**: <BR>
          I can connect you to a human agent for further assistance. <BR>
          Would you like me to do that now?<BR>
  - **User**: "Yes, please"
  - **Bot**: <BR>
          Please hold on while I connect you to our expert 📲<BR>

##  **Fourth example**:<br>Digression and updating an information during the conversation
  - **User**: I would like to verify my expenses for January's bill
  - **Bot**: <BR>
           Your bill for January 2025 is $150.50. <BR>
           The average of your past bills is $88.50. <BR>
           This bill is higher than your average by $62.00.<BR>
  - **Bot**: <BR>
          Would you like to see the breakdown of the costs?
  - **User**: oh no I meant February
  - **Bot**: <BR>
          Alright, I'm changing the bill month to February for you.
          Your bill for February 2025 is $55.00.<BR>
          The average of your past bills is $88.50.<BR>
          This bill is lower than your average by $33.50. <BR>
  - **Bot**: <BR>
          Would you like to see the breakdown of the costs?
  - **User**: No, that's fine
  - **Bot**: <BR>
          Did I manage to provide all the information you need?<BR>
  - **User**: Yup
  - **Bot**: <BR>
          Glad, I helped ✨ <BR>
          Have a nice day! <BR>

# Features and bot content explanation
 What you will find in this bot project:
 - **Actions** : custom actions, mimic getting information from a DB, either adding it to the session start or afterwards in the conversation. I mimic this behavior by getting information about customers from two CSVs.
 - **RAG** : enterprise search if the ask knowledge base questions
 - **Data**
    - **Flows** : are built to handle user questions about "internet is slow" or "check their bill". Different features are used : calling or linking a flow, branching on a slot value.
    - **Patterns** : Over-ride some patterns, to change the behavior. make sure to add the same patterns name as the originals.
 - **Documents** : have general information on what is a router how to start it ... this can be triggered at any point of the conversation and then the assistant will go back to finish the flow
 - **Domain** : contains all bot answers, details/definition about all slots and mention the custom actions
  - **Responses** : I added simple once, one with buttons and others with images
  - **Slots** : different slot type and mapping
    - **type** : Float, text, bool and categorical
    - **mappings** : from_llm, and custom
 - **Images** : These images are used in the README
 - **Prompts** : Optional prompts.  You can customize prompt(s) here and refer to them in the config.yml file. The example prompt here looks like the original; the **CHITCHAT** command has been removed and additional details have been added for the `SearchAndReply()`.
 - **Tests** : This is a good way to test the bot's capabilities and ensure the same behavior when doing changes and updates. With Assertions we can track commands and when slots are set. The folder contains 7 test cases, this can help you better understand how the bot function. Results of the current tests are available in the tests folder to illustrate how e2e test works, however you can obtain the same result by running the command `make test`
 - **Config**: We have two sections, the pipeline and the policies
     - the pipeline we have `SearchReadyLLMCommandGenerator` that will convert user messages into commands, we add the LLM we want to use here
     - the policies: two policies are used in this assistant the `FlowPolicy` and the `EnterpriseSearchPolicy`

<br><br><br>
# Installation (Docker)
> **Note:** You can find alternative installation methods in the [Rasa documentation](https://rasa.com/docs/pro/installation/overview).
<br>

## Installation Steps
- Before You Begin
- Setting Environment Variables for Rasa
- Install Docker
- Download Rasa Telecom Starter Pack
- Starting the Demo Assistant
<br>

## Before You Begin

**To use this starter pack, you will need:**
1. A free [Rasa Developer Edition license](https://rasa.com/rasa-pro-developer-edition-license-key-request/). To get the free license use the link and complete the form. You’ll be emailed the license key. Store this somewhere safe as you’ll need it a bit later in the instructions below. The actual installation of the Rasa Pro platform will be performed during the installation steps described below.
2. An API key from OpenAI (the default model provider for this starter pack, though CALM supports other LLMs, too).
    - If you haven't already, sign up for an account on the OpenAI platform.
    - Then, navigate to the [OpenAI Key Management](https://platform.openai.com/api-keys) (Dashboard > API keys) page and click on the "Create New Secret Key" button to initiate obtaining `<your-openai-api-key>`.
3. A computer. Instructions are available for MacOS, Linux & Windows.
> **Note for Windows users:**  
> If you don’t already have `make`, you’ll need to install it:
>
> - **Option 1:** Install [Chocolatey](https://chocolatey.org/install).  
>   👉 Open **PowerShell as Administrator** (Start → search "PowerShell" → right-click → *Run as Administrator*).  
>   Then run:
>   ```powershell
>   choco install make -y
>   ```
>   Verify with:
>   ```powershell
>   make --version
>   ```
>
> - **Option 2:** Install [Git for Windows](https://git-scm.com/download/win), which includes Git Bash (and `make`).  
>   Open **Git Bash** instead of PowerShell to run your commands.
<br>

## Setting Environment Variables for Rasa

You'll need to save your **Rasa Pro license key** and **OpenAI API key** as environment variables so they can be used by the application.

**MacOS, Linux**
1. Open your terminal, and edit your shell config
    - `nano ~/.zshrc` (or `~/.bashrc` if you’re using Linux bash)
2. At the bottom of the file, add lines like this (replace the values with your actual keys):
    - `export RASA_PRO_LICENSE=<your-rasa-pro-license-key>`
    - `export OPENAI_API_KEY=sk-<your-openai-api-key>`
    1. For example, it may look something like this:
        - `RASA_PRO_LICENSE=etou948949theu`
        - `OPENAI_API_KEY=sk-proj-ntehoitnhtnoe`
3. Save the file (`CTRL+O`, `Enter`, `CTRL+X` in nano), then reload it
    - `source ~/.zshrc`  (or `~/.bashrc` if you’re using Linux bash)
4. Check that the variables are set:
    - `echo $RASA_PRO_LICENSE`
    - `echo $OPENAI_API_KEY`

**Windows**
1. Press `Win + S` and type `Environment Variables`, then select `Edit the system environment variables`.
2. In the `System Properties` window, click `Environment Variables`.
3. Under `User variables` (applies only to your user), click `New`.
    1. For `Name`, enter: `RASA_PRO_LICENSE`
    2. For `Value`, enter: `<your-rasa-pro-license-key>`
4. Repeat for `OPENAI_API_KEY`.
5. Click `OK` → `OK` to save and close all windows.
6. Restart your terminal (PowerShell) so the new values load.
7. Verify the variables are set (PowerShell):
    1. `echo $env:RASA_PRO_LICENSE`
    2. `echo $env:OPENAI_API_KEY`
<br>

## Install Docker
1. Download & install docker:
    - MacOS:   https://docs.docker.com/desktop/setup/install/mac-install/
    - Linux:   https://docs.docker.com/engine/install/
    - Windows: https://docs.docker.com/desktop/setup/install/windows-install/
        - Use WSL 2 backend (not Hyper-V)
3. Start Docker Desktop. Make sure Docker Desktop (the Docker daemon) is running before you run any commands.
    - Windows: Follow prompted instructions for WSL (e.g. `wsl --update`)
4. Verify Installation. Open your terminal (Mac/Linux shell, or PowerShell on Windows) and run:
    1. `docker --version`
5. Download the Rasa Pro Docker image. Open your terminal and run:
    1. `docker pull rasa/rasa-pro:3.13.7`
<br>

## Download Rasa Telecom Starter Pack
1. Download the Source Code Assets for the [latest release from GitHub](https://github.com/rasa-customers/starterpack-telco-en/releases)
2. Uncompress the assets in a local directory of your choice.
    1. The **starterpack-telco-en** directory (created when uncompressed) contains a README file with additional instructions on installing dependencies, training the model, and running the assistant locally.
3. Open your terminal (or PowerShell on Windows) and navigate to the directory where you uncompressed the **starterpack-telco-en** files.
Congratulations, you have successfully installed Rasa and are ready to use the Telecom Starter Pack as a demo or as a foundation for your custom flows.
<br>

## Starting the Demo Assistant
To start up the Telecom Demo Assistant, ensure you're in the **starterpack-telco-en** directory.
1. **Train the Rasa model**
2. **Start the Rasa Inspector** or
3. **Start the Rasa Chat Widget**
<br>

## 1. Train the Rasa model
`make model`
<br>

You will find your trained model inside the `models/` directory.
You can now test your assistant using the Rasa Inspector or Rasa Chat Widget.
<br><br>

## 2. Start the Rasa Inspector
`make inspect`
1. Once you see the “Starting worker” message in your terminal, proceed to the next step.
2. In your browser go to: http://localhost:5005/webhooks/socketio/inspect.html
<br><br>

## 3. Start the Rasa Chat Widget
`make run`
1. Once you see the “Starting worker” message in your terminal, proceed to the next step.
2. Open Finder (Mac) or File Explorer (Windows).
3. Navigate to the chatwidget directory inside the **starterpack-telco-en** folder you uncompressed earlier.
4. Double-click `chatwidget/index.html` to open the demo in your browser.
5. You can now interact with the Telco Demo Assistant using Rasa’s chat widget.
<br><br>
> [!TIP]
> You can also edit chatwidget/index.html to customize the look and behavior of the demo.

> [!NOTE]
> For a full list of Rasa CLI commands refer to: https://rasa.com/docs/reference/api/command-line-interface/#cheat-sheet
<br>

## Stopping the Demo Assistant
1. To stop the Rasa server, return to the terminal window where it is running and press **Ctrl+C**.
2. That's it, you’ve successfully run your first Rasa Assistant! You can now close the terminal window if you wish.
<br>

## Restarting the Demo Assistant
1. Open your terminal and navigate to the **starterpack-telco-en** directory.
2. Then, follow the same steps from **Starting the Demo Assistant** to run the assistant again.
<br>

# Tips
- Check our docs to understand all [Rasa primitives](https://rasa.com/docs/reference/primitives/)
  - Get familiar with all flow properties, patterns, responses
- Start writing e2e test cases right when you start writing your flows, you can start by copying what we have in **inspector view** in the **end-2-end test** section. Read more in our Documentation: [Evaluating Your Assistant](https://rasa.com/docs/pro/testing/evaluating-assistant/)
- When you are trying to debug look for these sections in your logs.
  - Always review the prompt in the logs to make sure the right flows and slots are available and check the conversation history to better understand the bot's behavior.
  - Search for `action_list` to see the command that was predicted by CALM, this will help you debug.
    For instance, it can be `action_list=StartFlow(understand_bill)` or `action_list=SetSlot(bill_month, 2025-01-01)`
  - Search for `commands=`
    For instance `commands=[StartFlowCommand(flow='bot_challenge')]`
  - Check the **tracker state** in the **inspector view**
  - Add `logging.info` to you custom actions to get more visibility.
<br>

# Next Steps
- Identify the use cases you would like to add to this assistant.
  - It can be improving the existing two or adding new ones.
    Examples:
    - Create and track support tickets for unresolved issues.
    - Notify users about due dates and payment confirmations.
    - Detect suspicious account activity and alert customers.
- Create diagrams that illustrates the conversation flow. A conversation designer will be a perfect expert to rely on to accomplish this step.
- Start building the flows and adding e2e test cases
- Share the first versions with your colleague to test and provide feedback.
- Improve, test, re-share.
<br>

# Contributing
Feel free to fork this repo and submit pull requests. Suggestions and improvements are always welcome!
<br><br>

# License
This project is licensed under the Apache 2.0 License, allowing modification, distribution, and usage with proper attribution.
