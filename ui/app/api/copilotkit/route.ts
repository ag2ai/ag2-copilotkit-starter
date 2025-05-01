import { CustomHttpAgent } from "@/app/api/copilotkit/your-custom-http-agent";
import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  ExperimentalEmptyAdapter,
} from "@copilotkit/runtime";

const serviceAdapter = new ExperimentalEmptyAdapter();

const BASE_URL = "http://127.0.0.1:8008";

const agenticChatAgent = new CustomHttpAgent({
  url: `${BASE_URL}/fastagency/awp`,
});

const runtime = new CopilotRuntime({
  agents: {
    agenticChatAgent,
  },
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
