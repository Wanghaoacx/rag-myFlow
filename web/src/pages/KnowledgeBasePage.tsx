import { useState, type FormEvent } from "react";

import { type DocumentResponse, uploadDocument } from "../lib/api";

export function KnowledgeBasePage() {
  const [file, setFile] = useState<File | null>(null);
  const [hasTextLayer, setHasTextLayer] = useState(true);
  const [result, setResult] = useState<DocumentResponse | null>(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!file) {
      setError("请先选择文件");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await uploadDocument(file, hasTextLayer);
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
      <p>当前页已接入真实文件上传入口；文本类文件会进入最小解析链路，OCR 依赖型文件会被显式拒绝。</p>

      <form onSubmit={handleSubmit}>
        <label>
          选择文件
          <input
            type="file"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
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
          {isSubmitting ? "上传中..." : "上传文件"}
        </button>
      </form>

      {file ? (
        <p>
          已选择文件：{file.name}（{file.type || "未知 MIME"}）
        </p>
      ) : null}

      {result ? (
        <div>
          <h3>导入结果</h3>
          <p>文档 ID：{result.document_id}</p>
          <p>文件名：{result.file_name}</p>
          <p>MIME：{result.mime_type}</p>
          <p>Chunk 数：{result.chunk_count}</p>
          <p>文本预览：{result.preview_text ?? "当前文件尚未提取到可检索文本"}</p>
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
