 # Supervisor Multi-Agent System

This project demonstrates a multi-agent orchestration using [LangGraph](https://github.com/langchain-ai/langgraph) and [LangGraph Supervisor](https://github.com/langchain-ai/langgraph-supervisor), featuring:

- **Supervisor Agent:** Orchestrates and manages tasks between sub-agents.
- **Jira Agent:** Handles Jira operations (create, update, comment, delete, search, list).
- **Web Agent:** Provides current weather information for any location.

---

## 📂 Project Structure

```
supervisor/
├── jira_agent.py # Jira agent definition
├── web_agent.py # Web agent (weather) definition
├── supervisor.py # Supervisor agent orchestration
├── llm_provider.py # Centralized LLM initialization
├── requirements.txt # Python dependencies
└── README.md # This file

```

---

## 🚀 Features

- **Centralized LLM Configuration:** All agents use a shared, configurable LLM connection.
- **Modular Agents:** Each agent is defined in its own file for clarity and reusability.
- **LangGraph Supervisor:** Easily add or remove agents and manage workflows.
- **Environment Variables:** Sensitive data (like Jira credentials) are loaded from `.env`.

---

## 🛠️ Setup

### 1. Clone the Repository


```
git clone <your-repo-url>
cd supervisor

```


### 2. Create and Activate a Virtual Environment
```
python3 -m venv .venv
source .venv/bin/activate
```


### 3. Install Dependencies

```
pip install -r requirements.txt
```


### 4. Set Up Environment Variables

Create a `.env` file in the root directory with your credentials:
```
JIRA_SERVER=https://your-jira-instance.atlassian.net
JIRA_USER=your-email@example.com
JIRA_TOKEN=your-jira-api-token
OPENWEATHERMAP_API_KEY=your-openweathermap-api-key
```

---

## 🧩 Usage

### 1. Start the LangGraph Dev Server

```
langgraph dev --allow-blocking
```


- **API:** http://127.0.0.1:2024
- **Studio UI:** https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

### 2. Supervisor Agent

The `supervisor.py` script initializes the supervisor agent, which delegates tasks to:

- **Jira Agent:** For Jira-related actions.
- **Web Agent:** For weather queries.

### 3. Example Agent Usage

#### Jira Agent

Handles actions such as:
- Creating issues
- Updating issues
- Adding comments
- Deleting issues
- Searching and listing issues

#### Web Agent

Handles:
- Fetching current weather for a given location using OpenWeatherMap.

---

## 🏗️ How It Works

- **llm_provider.py:**  
  Centralizes LLM initialization.  
  Example:




- **jira_agent.py:**  
Defines Jira tools and creates the Jira agent.

- **web_agent.py:**  
Defines the weather tool and creates the Web agent.

- **supervisor.py:**  
Imports both agents and creates a supervisor agent to manage them.

---

## 📝 Customization

- **Add More Agents:**  
Define new agents in their own files and add them to the supervisor.

- **Change LLM Model:**  
Update the model ID or provider in `llm_provider.py` or pass as an argument.

- **Extend Functionality:**  
Add new tools to agents as needed.

---

## 📦 Requirements

- Python 3.9+
- [langgraph](https://pypi.org/project/langgraph/)
- [langgraph-supervisor](https://pypi.org/project/langgraph-supervisor/)
- [langchain](https://pypi.org/project/langchain/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [jira](https://pypi.org/project/jira/)
- [openweathermap](https://openweathermap.org/api)

See `requirements.txt` for the full list.

---

## 🤝 Credits

- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com/)
- [OpenWeatherMap](https://openweathermap.org/)
- [Atlassian Jira](https://www.atlassian.com/software/jira)

---

## 🧑‍💻 License

MIT License

---

**Happy hacking!**  
For questions or contributions, open an issue or pull request.





