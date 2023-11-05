## pip install pyautogen pymemgpt

import os
import autogen
import memgpt.autogen.memgpt_agent as memgpt_autogen
import memgpt.autogen.interface as autogen_interface
import memgpt.agent as agent       
import memgpt.system as system
import memgpt.utils as utils 
import memgpt.presets as presets
import memgpt.constants as constants 
import memgpt.personas.personas as personas
import memgpt.humans.humans as humans
from memgpt.persistence_manager import InMemoryStateManager, InMemoryStateManagerWithPreloadedArchivalMemory, InMemoryStateManagerWithEmbeddings, InMemoryStateManagerWithFaiss
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent, create_memgpt_autogen_agent_from_config
import openai

config_list = [
    {
        "api_type": "open_ai",
        "api_base": "http://127.0.0.1:5001/v1",
        "api_key": "NULL",
    },
]

llm_config = {"config_list": config_list, "seed": 42}

# If USE_MEMGPT is False, then this example will be the same as the official AutoGen repo
# (https://github.com/microsoft/autogen/blob/main/notebook/agentchat_groupchat.ipynb)
# If USE_MEMGPT is True, then we swap out the "coder" agent with a MemGPT agent

USE_MEMGPT = True

## api keys for the memGPT
openai.api_base="http://127.0.0.1:5001/v1"
openai.api_key="NULL"


# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",  # needed?
    default_auto_reply="Come up with another new tweet when you're done.",
)

pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)

interface = autogen_interface.AutoGenInterface()
persistence_manager=InMemoryStateManager()
persona =f"I am a 10x full stack engineer and expert in python, My code is impecable, efficient and works flawlessy as my life depends on it. I was the first hire at uber. "
f"(which I make sure to tell everyone I work with).\n"
f"You are participating in a group chat with a user ({user_proxy.name}) "
f"and a product manager ({pm.name})."
human = "Im a team manager at this company"
memgpt_agent=presets.use_preset(presets.DEFAULT_PRESET, model='gpt-4', persona=persona, human=human, interface=interface, persistence_manager=persistence_manager, agent_config=llm_config)



    # This MemGPT agent will have all the benefits of MemGPT, ie persistent memory, etc.
coder = memgpt_autogen.MemGPTAgent(
        name="MemGPT_coder",
        agent=memgpt_agent,
)
groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the group chat with a message from the user
user_proxy.initiate_chat(
    manager,
    message="how are you doing?"
    )