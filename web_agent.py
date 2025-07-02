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
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.tools.tavily_search import TavilySearchResults

# LangGraph for workflow orchestration
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent, ToolNode

# weather
from langchain_community.utilities import OpenWeatherMapAPIWrapper

from llm_provider import get_llm

# Weather

weather_api = OpenWeatherMapAPIWrapper()
# tools = [weather.run]


load_dotenv()

@tool("weather", return_direct=True)
def get_weather(location: str) -> str:
    """
    Gets the current weather for a given location using OpenWeatherMap.
    
    Args:
        location (str): Name of the city or place (e.g., Delhi, London).
    
    Returns:
        str: Weather description with temperature.
    """
    return weather_api.run(location)


model_id="gemini-2.5-flash-preview-05-20"
llm = get_llm(model_id=model_id, model_provider="google_vertexai")
tools = [get_weather]
webagent = create_react_agent(llm, tools, name="webagent")
graph = webagent