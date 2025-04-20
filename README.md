# LangGraph Email Processing System

This project is an intelligent email processing pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [Ollama](https://ollama.com/). It classifies emails as spam or not, suggests responses, and tracks LLM usage with [Langfuse](https://langfuse.com/).

## Features

- **Spam Detection:** Automatically classifies emails as spam or legitimate.
- **Response Suggestions:** Drafts responses for legitimate emails using an LLM.
- **Traceability:** Tracks and visualizes LLM calls and workflow execution with Langfuse.

## Quick Start

1. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```
2. **Set up the Environment Varaibles:
  create a .env file with LANGFUSE credentials
3. **Start OLLAMA**
  Make sure it is installed and running on your machine
4. **Run the app**
   python app.py

### CHECK Project Tracing
[View Traces on LangFuse](https://cloud.langfuse.com/project/cm9owmw1x00kuad07gyk0xs5r/traces)
### Local models tested and performed magnificent: `misral:latest`, `llama3.2:latest`
