import { useState } from "react";
import { ChatWindow } from "./components/ChatWindow";
import { Dashboard } from "./components/Dashboard";

type Tab = "chat" | "dashboard";

export default function App() {
  const [tab, setTab] = useState<Tab>("chat");

  return (
    <main className="app-shell">
      <header>
        <h1>RAG-AI</h1>
        <p>Asistente RAG de desarrollo de software, IA/RAG y DevOps.</p>
      </header>

      <nav className="tab-nav" role="tablist">
        <button role="tab" aria-selected={tab === "chat"} onClick={() => setTab("chat")}>
          💬 Chat
        </button>
        <button role="tab" aria-selected={tab === "dashboard"} onClick={() => setTab("dashboard")}>
          📊 Dashboard
        </button>
      </nav>

      {tab === "chat" ? <ChatWindow /> : <Dashboard />}
    </main>
  );
}
