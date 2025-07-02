from jira_agent import jiraagent
from web_agent import webagent
from telegram_agent import teleagent
# Environment and OS
import os
import re
from dotenv import load_dotenv

# LangChain core and community
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage

# LangChain chat models and agent toolkits
from langchain.chat_models import init_chat_model

# LangGraph for workflow orchestration
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent, ToolNode

# Jira
from jira import JIRA

load_dotenv()


# Creating a supervisor agent
from langgraph_supervisor import create_supervisor

model_id="gemini-2.5-flash-preview-05-20"
llm = init_chat_model(model=model_id,  model_provider="google_vertexai")


supervisor = create_supervisor(
    model=llm,
    agents=[jiraagent, webagent, teleagent],
    prompt=(
        """
Supervisor Agent Prompt

 You are a supervisor managing three agents:

 1. **jiraagent**: Handles all activities related to Jira, such as creating, updating, commenting, deleting, searching, and listing issues.
 2. **webagent**: Provides current weather information for a given location.
 3. **teleagent**: Manages sending and receiving messages via Telegram, including notifications and chat interactions. 
    Use the default telegram group -1002787003234 to send message if not given

 Your job is to analyze each incoming task or request and delegate it to the most appropriate agent.
 - If the task involves Jira operations, assign it to jiraagent.
 - If the task is about weather information, assign it to webagent.
 - If the task involves Telegram messaging or chat, assign it to telegramagent.
    

    If a user asks to get information (such as weather) and send it via Telegram, you must:
    - First, use the appropriate agent to get the information.
    - Then, pass the result to the Telegram agent to send as a message.
    Do not ask the user to manually transfer information between agents.
    
 **Do not perform any tasks yourself. Only delegate work to the agents and coordinate their responses.

        """
    ),
    add_handoff_back_messages=True,
    output_mode="full_history"
     ).compile( name="supervisor" )

graph = supervisor

