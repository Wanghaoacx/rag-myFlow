import { useState } from "react";

import { ChatPage } from "./pages/ChatPage";
import { KnowledgeBasePage } from "./pages/KnowledgeBasePage";
import { SettingsPage } from "./pages/SettingsPage";
import { WorkflowPage } from "./pages/WorkflowPage";

type TabKey = "knowledge" | "chat" | "workflow" | "settings";

const tabs: Array<{ key: TabKey; label: string }> = [
  { key: "knowledge", label: "知识库" },
  { key: "chat", label: "对话" },
  { key: "workflow", label: "工作流" },
  { key: "settings", label: "设置" },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<TabKey>("knowledge");

  return (
    <main>
      <h1>rag-myFlow</h1>
      <nav aria-label="主导航">
        {tabs.map((tab) => (
          <button key={tab.key} type="button" onClick={() => setActiveTab(tab.key)}>
            {tab.label}
          </button>
        ))}
      </nav>
      {activeTab === "knowledge" && <KnowledgeBasePage />}
      {activeTab === "chat" && <ChatPage />}
      {activeTab === "workflow" && <WorkflowPage />}
      {activeTab === "settings" && <SettingsPage />}
    </main>
  );
}
