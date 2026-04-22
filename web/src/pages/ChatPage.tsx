import { useState, type FormEvent } from "react";

import { answerQuestion, type ChatResponse } from "../lib/api";

export function ChatPage() {
  const [question, setQuestion] = useState("rag-myFlow 删除了什么能力？");
  const [knowledgeBaseIds, setKnowledgeBaseIds] = useState("kb-local");
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResult(null);
    setIsSubmitting(true);

    try {
      const response = await answerQuestion({
        question,
        knowledge_base_ids: knowledgeBaseIds
          .split(",")
          .map((value) => value.trim())
          .filter(Boolean),
      });
      setResult(response);
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "问答失败");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section>
      <h2>检索对话</h2>
      <form onSubmit={handleSubmit}>
        <label>
          问题
          <input value={question} onChange={(event) => setQuestion(event.target.value)} />
        </label>
        <label>
          知识库 ID
          <input
            value={knowledgeBaseIds}
            onChange={(event) => setKnowledgeBaseIds(event.target.value)}
          />
        </label>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "提问中..." : "发送问题"}
        </button>
      </form>

      {result ? (
        <div>
          <h3>回答</h3>
          <p>{result.answer}</p>
          <h3>引用</h3>
          <ul>
            {result.citations.map((citation) => (
              <li key={citation.chunk_id}>
                {citation.document_id} / {citation.chunk_id} / {citation.snippet}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {error ? <p role="alert">{error}</p> : null}
    </section>
  );
}
