import { useState, type FormEvent } from "react";

import { createDocument, type DocumentResponse } from "../lib/api";

const mimeTypeOptions = [
  { value: "application/pdf", label: "PDF 文本层" },
  { value: "image/png", label: "PNG 图片" },
  { value: "text/plain", label: "纯文本" },
];

export function KnowledgeBasePage() {
  const [fileName, setFileName] = useState("guide.pdf");
  const [mimeType, setMimeType] = useState("application/pdf");
  const [hasTextLayer, setHasTextLayer] = useState(true);
  const [result, setResult] = useState<DocumentResponse | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResult(null);
    setIsSubmitting(true);

    try {
      const response = await createDocument({
        file_name: fileName,
        mime_type: mimeType,
        has_text_layer: hasTextLayer,
      });
      setResult(response);
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "导入失败");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section>
      <h2>知识库与文档管理</h2>
      <p>当前页先接通最小文档导入校验链路，用来验证无 OCR 约束是否生效。</p>

      <form onSubmit={handleSubmit}>
        <label>
          文件名
          <input value={fileName} onChange={(event) => setFileName(event.target.value)} />
        </label>
        <label>
          MIME 类型
          <select value={mimeType} onChange={(event) => setMimeType(event.target.value)}>
            {mimeTypeOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>
        <label>
          <input
            type="checkbox"
            checked={hasTextLayer}
            onChange={(event) => setHasTextLayer(event.target.checked)}
          />
          文档包含文本层
        </label>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "导入中..." : "模拟导入"}
        </button>
      </form>

      {result ? (
        <div>
          <h3>导入结果</h3>
          <p>文档 ID：{result.document_id}</p>
          <p>文件名：{result.file_name}</p>
          <p>MIME：{result.mime_type}</p>
        </div>
      ) : null}

      {error ? (
        <p role="alert">
          导入失败：
          {error}
        </p>
      ) : null}
    </section>
  );
}
