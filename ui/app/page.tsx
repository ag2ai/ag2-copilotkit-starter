"use client";

import { useCopilotReadable } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useState } from "react";

export default function Home() {
  return (
    <main>
      <YourMainContent />
      <CopilotSidebar
        defaultOpen={true}
        labels={{
          title: "Popup Assistant",
          initial:
            "Hi! I can help you learn about mathematics. What subject you would like to explore?",
        }}
      />
    </main>
  );
}

function YourMainContent() {
  const [userName, setUserName] = useState("AG2 Super User");

  useCopilotReadable({
    description: "The name of the logged in user",
    value: userName,
  });

  // Render the main content
  return (
    <div className="h-screen w-screen flex justify-center items-center flex-col">
      <h1 className="bg-blue-500 p-10 rounded-xl text-white text-4xl">
        Welcome to CopilotKit! {userName}
      </h1>
    </div>
  );
}
