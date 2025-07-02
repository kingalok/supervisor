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

from llm_provider import get_llm
# Jira
from jira import JIRA

load_dotenv()


# Jira

@tool("jira_unified_tool", return_direct=True)
def jira_unified_tool(
    action: str,
    issue_key: str = None,
    summary: str = None,
    description: str = None,
    project_key: str = "ECS",
    comment: str = None,
    issue_type: str = "Task",
    jql: str = None,
    max_results: int = 20
) -> str:
    """
    Unified Jira tool to perform create, update, comment, delete, search, and list actions.
    action: "create", "update", "comment", "delete", "search", or "list"
    """
    try:
        jira = JIRA(
            server=os.getenv('JIRA_SERVER'),
            basic_auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_TOKEN'))
        )

        if action == "create":
            if not summary or not description:
                return "Missing required fields for creating an issue: summary, description."
            issue = jira.create_issue(
                project=project_key,
                summary=summary,
                description=description,
                issuetype={'name': issue_type}
            )
            return f"Issue created: {issue.key}"

        elif action == "update":
            if not issue_key or not (summary or description):
                return "Missing required fields for updating an issue: issue_key and at least one of summary or description."
            fields = {}
            if summary:
                fields['summary'] = summary
            if description:
                fields['description'] = description
            issue = jira.issue(issue_key)
            issue.update(fields=fields)
            return f"Issue {issue_key} updated."

        elif action == "comment":
            if not issue_key or not comment:
                return "Missing required fields for adding a comment: issue_key and comment."
            issue = jira.issue(issue_key)
            jira.add_comment(issue, comment)
            return f"Comment added to issue {issue_key}."

        elif action == "delete":
            if not issue_key:
                return "Missing required field for deleting an issue: issue_key."
            issue = jira.issue(issue_key)
            issue.delete()
            return f"Issue {issue_key} deleted."

        elif action == "search":
            if not jql:
                return "Missing required field for searching issues: jql."
            issues = jira.search_issues(jql, maxResults=max_results)
            if not issues:
                return "No issues found matching the query."
            result = [f"{issue.key}: {issue.fields.summary}" for issue in issues]
            return "\n".join(result)

        elif action == "list":
            # List all issues in a project (default: ECS)
            jql_query = f"project = {project_key} ORDER BY created DESC"
            issues = jira.search_issues(jql_query, maxResults=max_results)
            if not issues:
                return f"No issues found in project {project_key}."
            result = [f"{issue.key}: {issue.fields.summary}" for issue in issues]
            return "\n".join(result)

        else:
            return "Unknown action. Supported actions: create, update, comment, delete, search, list."

    except Exception as e:
        return f"Error: {str(e)}"


model_id="gemini-2.5-flash-preview-05-20"
llm = get_llm(model_id=model_id, model_provider="google_vertexai")

#llm = init_chat_model(model=model_id,  model_provider="google_vertexai")
tools = [jira_unified_tool]
#jiraagent = create_react_agent(llm, tools)
jiraagent = create_react_agent(llm, tools, name="jiraagent")
graph = jiraagent