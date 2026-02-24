# AG2 + CopilotKit Starter

A weather agent demo built with [AG2](https://docs.ag2.ai) and the [AG-UI protocol](https://docs.ag2.ai/latest/docs/user-guide/ag-ui/).

## Project Structure

```
ag2-copilotkit-starter/
├── agent-py/               # Python backend (AG2 agent + AG-UI endpoint)
│   ├── backend.py
│   └── requirements.txt
├── ui-react/               # React + CopilotKit frontend
│   └── app/
│       ├── api/copilotkit/route.ts
│       ├── layout.tsx
│       ├── page.tsx
│       └── globals.css
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

## React + CopilotKit Frontend Setup

```sh
cd ui-react
npm install
npm run dev
```

Open http://localhost:3000 and chat with the weather agent.

## Additional Resources

- [AG2 Documentation](https://docs.ag2.ai/latest/)
- [AG-UI Protocol Guide](https://docs.ag2.ai/latest/docs/user-guide/ag-ui/)
- [CopilotKit Documentation](https://docs.copilotkit.ai/)
