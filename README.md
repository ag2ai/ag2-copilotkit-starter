# CopilotKit-AG2 Starter

This repository contains a simple starter project that demonstrates how to build AI agents with AG2 that interact with CopilotKit.

## Project Structure

```
ag2-copilotkit-starter/
├── agent-py/           # Python backend with AG2 agents
│   └── simple_workflow.py
│   └── hitl_workflow.py
└── ui/                 # Frontend application
```

## Prerequisites

- Python 3.9 or newer
- Node.js 18.18.0 or newer (specifically: ^18.18.0 || ^19.8.0 || >= 20.0.0)
- pnpm (for package management)
- OpenAI API key

## Backend Setup

### 1. Install Python Backend Dependencies

> Note: We recommend using a virtual environment for your project to keep your packages contained. See <a href="https://docs.python.org/3/library/venv.html" target="_blank">venv</a>.

```sh
cd agent-py
pip install -r requirements.txt
```

### 2. Set up your API Key

Before running the code, you need to set your OpenAI API key as an environment variable:

**macOS/Linux:**
```sh
export OPENAI_API_KEY="your_openai_api_key"
```

**Windows:**
```sh
setx OPENAI_API_KEY "your_openai_api_key"
```

> Note: This example (simple_workflow.py) uses `gpt-4o-mini` by default, but you can replace it with any other model supported by AG2 by modifying the configuration in the code.

### 3. Start the Backend Server

The command below assumes that you are already inside the `agent-py` directory. If not please `cd` into the directory before running the command.

```sh
uvicorn simple_workflow:app --port 8008 --reload
```

> The command above starts the simple agent chat workflow. You can explore other workflows available in the `agent-py` directory, try them out, or even create your own. Each workflow file includes the command to run it at the bottom.

The backend server will start at http://localhost:8008.

## Frontend Setup

### 1. Install Frontend Dependencies

Open a new terminal session and run the below command

```sh
cd ui
pnpm i
```

### 2. Start the Frontend Application

The command below assumes that you are already inside the `ui` directory. If not please `cd` into the directory before running the command.

```sh
pnpm run dev
```

The frontend application will start at http://localhost:3000.

After starting the frontend, please allow a few moments for the Next.js application to compile fully. Once compilation is complete, you can interact with the chat window to communicate with the AG2 agent.

## Additional Resources

- <a href="https://docs.ag2.ai/latest/" target="_blank">AG2 Documentation</a>
- <a href="https://docs.copilotkit.ai/" target="_blank">CopilotKit Documentation</a>
