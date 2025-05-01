"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <main>
      <YourMainContent />
      <CopilotSidebar
        defaultOpen={true}
        labels={{
          title: "Popup Assistant",
          initial:
            "👋 Hey there! You’re now chatting with your AG2 workflow. Just type a message to get started!",
        }}
      />
    </main>
  );
}

function YourMainContent() {
  // Render the main content
  return (
    <div className="h-screen w-screen flex justify-center items-center flex-col">
      <h1 className="bg-blue-500 p-10 rounded-xl text-white text-4xl">
        Welcome to CopilotKit!
      </h1>
    </div>
  );
}
