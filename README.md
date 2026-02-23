# AG2 + CopilotKit Starter

A weather agent demo built with [AG2](https://docs.ag2.ai) and the [AG-UI protocol](https://docs.ag2.ai/latest/docs/user-guide/ag-ui/). Includes two frontends: a React/CopilotKit app and a plain HTML page.

## Project Structure

```
ag2-copilotkit-starter/
├── agent-py/               # Python backend (AG2 weather agent)
│   ├── backend.py
│   └── requirements.txt
├── ui-react/               # UI Option 1: React + CopilotKit frontend
│   └── app/
│       ├── api/copilotkit/route.ts
│       ├── layout.tsx
│       ├── page.tsx
│       └── globals.css
├── ui-html/                # UI Option 2: Standalone HTML frontend
│   └── index.html
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18.18+
- OpenAI API key

## Backend Setup

```sh
cd agent-py
pip install -r requirements.txt
export OPENAI_API_KEY="your_openai_api_key"
python backend.py
```

The backend server starts at http://localhost:8008.

## Frontend Option 1: React + CopilotKit

```sh
cd ui-react
npm install
npm run dev
```

Open http://localhost:3000 and chat with the weather agent.

## Frontend Option 2: HTML

Open `ui-html/index.html` directly in a browser, or serve it:

```sh
cd ui-html
python -m http.server 8080
```

Then open http://localhost:8080. Make sure the backend is running on port 8008.

## Additional Resources

- [AG2 Documentation](https://docs.ag2.ai/latest/)
- [AG-UI Protocol Guide](https://docs.ag2.ai/latest/docs/user-guide/ag-ui/)
- [CopilotKit Documentation](https://docs.copilotkit.ai/)
