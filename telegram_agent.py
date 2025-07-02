# Environment and OS
import os
import re
from dotenv import load_dotenv
import requests

# LangChain core and community
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage

# LangChain chat models and agent toolkits
from langchain.chat_models import init_chat_model

# LangGraph for workflow orchestration
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent, ToolNode
from llm_provider import get_llm
# Telegram

@tool("send_telegram_message", return_direct=True)
def send_telegram_message(chat_id: str, message: str) -> str:
    """
    Sends a message to a Telegram chat using the Telegram Bot API.

    Args:
        chat_id (str): The chat ID of the Telegram user or group.
        message (str): The message to be sent.

    Returns:
        str: Response status or error message.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        return "Bot token not found in environment."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return "Telegram message sent successfully!"
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Failed to send message: {str(e)}"

model_id="gemini-2.5-flash-preview-05-20"
llm = get_llm(model_id=model_id, model_provider="google_vertexai")

#llm = init_chat_model(model=model_id,  model_provider="google_vertexai")
tools = [send_telegram_message]
#jiraagent = create_react_agent(llm, tools)
teleagent = create_react_agent(llm, tools, name="teleagent")
graph = teleagent