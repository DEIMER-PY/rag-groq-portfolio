import { ChatWindow } from "./components/ChatWindow";

export default function App() {
  return (
    <main className="app-shell">
      <header>
        <h1>RAG-AI</h1>
        <p>Asistente RAG de desarrollo de software, IA/RAG y DevOps.</p>
      </header>
      <ChatWindow />
    </main>
  );
}
