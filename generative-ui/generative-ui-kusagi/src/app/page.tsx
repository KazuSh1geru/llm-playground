"use client";

import { useState } from "react";
import { ClientMessage } from "./actions";
import { useActions, useUIState } from "ai/rsc";
import { generateId } from "ai";

export default function Home() {
  const [input, setInput] = useState("");
  const [conversation, setConversation] = useUIState();
  const { continueConversation } = useActions();

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="flex-1 overflow-y-auto p-4">
        {conversation.map((message: ClientMessage) => (
          <div key={message.id} className={`p-2 my-2 rounded-lg ${message.role === "user" ? "bg-blue-500 text-white self-end" : "bg-gray-300 text-black self-start"}`}>
            <span className="font-bold">{message.role}:</span> {message.display}
          </div>
        ))}
      </div>
      <div className="p-4 bg-white border-t border-gray-300">
        <input
          type="text"
          value={input}
          onChange={(event) => {
            setInput(event.target.value);
          }}
          className="w-full p-2 border border-gray-300 rounded-lg"
          placeholder="Type your message..."
        />
        <button
          onClick={async () => {
            setConversation((currentConversation: ClientMessage[]) => [
              ...currentConversation,
              { id: generateId(), role: "user", display: input },
            ]);

            const message = await continueConversation(input);

            setConversation((currentConversation: ClientMessage[]) => [
              ...currentConversation,
              message,
            ]);
            setInput("");
          }}
          className="mt-2 w-full bg-blue-500 text-white p-2 rounded-lg"
        >
          Send Message
        </button>
      </div>
    </div>
  );
}