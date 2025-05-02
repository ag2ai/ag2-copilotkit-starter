import type { Metadata } from "next";

import { CopilotKit } from "@copilotkit/react-core";

import "@copilotkit/react-ui/styles.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "CopilotKit-AG2 Starter",
  description: "CopilotKit-AG2 Starter",
};

export default function RootLayout({ children }: { children: any }) {
  return (
    <html lang="en">
      <body>
        <CopilotKit
          agent="agenticChatAgent"
          runtimeUrl="/api/copilotkit"
          showDevConsole={false}
        >
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
