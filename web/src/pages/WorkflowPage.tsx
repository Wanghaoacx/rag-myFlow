import { useState } from "react";

import { runWorkflow, type WorkflowResponse } from "../lib/api";

export function WorkflowPage() {
  const [question, setQuestion] = useState("测试问题");
  const [result, setResult] = useState<WorkflowResponse | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleRunRagQuery() {
    setError("");
    setResult(null);
    setIsSubmitting(true);

    try {
      const response = await runWorkflow({
        workflow_id: "wf-001",
        steps: [
          {
            kind: "rag_query",
            payload: {
              question,
              knowledge_base_ids: ["kb-local"],
            },
          },
        ],
      });
      setResult(response);
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "工作流执行失败");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleRunRemovedFeature() {
    setError("");
    setResult(null);
    setIsSubmitting(true);

    try {
      await runWorkflow({
        workflow_id: "wf-ocr",
        steps: [
          {
            kind: "ocr_extract",
            payload: {
              file_name: "scan.png",
            },
          },
        ],
      });
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "工作流执行失败");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section>
      <h2>工作流与 Agent</h2>
      <p>当前页先接通最小 workflow API，并保留一个“已删除能力”的显式失败入口。</p>
      <label>
        RAG 查询问题
        <input value={question} onChange={(event) => setQuestion(event.target.value)} />
      </label>
      <div>
        <button type="button" disabled={isSubmitting} onClick={handleRunRagQuery}>
          运行 rag_query
        </button>
        <button type="button" disabled={isSubmitting} onClick={handleRunRemovedFeature}>
          触发已删除 OCR 步骤
        </button>
      </div>

      {result ? (
        <div>
          <h3>运行结果</h3>
          <p>状态：{result.status}</p>
          <pre>{JSON.stringify(result.outputs, null, 2)}</pre>
        </div>
      ) : null}

      {error ? <p role="alert">{error}</p> : null}
    </section>
  );
}
