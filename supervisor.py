from jira_agent import jiraagent
from web_agent import webagent
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
    agents=[jiraagent, webagent],
    prompt=(
        """
        You are a supervisor managing two agents
        1. jiraagent agent. Managing any activities related to Jira
          such as perform create, update, comment, delete, search, and list actions
        2. webagent agent, Just provide current weather for a given locationall agents in parallel
        
        Do not work yourself
        
        """
    ),
    add_handoff_back_messages=True,
    output_mode="full_history"
     ).compile( name="supervisor" )

graph = supervisor

