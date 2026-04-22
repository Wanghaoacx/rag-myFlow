import "@testing-library/jest-dom/vitest";

import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import App from "../App";

const fetchMock = vi.fn<typeof fetch>();

vi.stubGlobal("fetch", fetchMock);

beforeEach(() => {
  fetchMock.mockReset();
  fetchMock.mockImplementation(async (input) => {
    const url = typeof input === "string" ? input : input.toString();

    if (url === "/api/health") {
      return new Response(JSON.stringify({ status: "ok", workspace: "local" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }

    if (url === "/api/chat/answer") {
      return new Response(
        JSON.stringify({
          answer: "基于知识库 kb-local 的结果：用户、登录与 OCR 已从 rag-myFlow 中移除。",
          citations: [
            {
              document_id: "doc-001",
              chunk_id: "chunk-001",
              snippet: "用户、登录与 OCR 已从 rag-myFlow 中移除。",
            },
          ],
        }),
        {
          status: 200,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    if (url === "/api/documents") {
      return new Response(
        JSON.stringify({
          code: "ocr_removed",
          message: "该文件类型依赖 OCR，rag-myFlow 当前版本不支持。",
        }),
        {
          status: 415,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    if (url === "/api/documents/upload") {
      return new Response(
        JSON.stringify({
          code: "ocr_removed",
          message: "该文件类型依赖 OCR，rag-myFlow 当前版本不支持。",
        }),
        {
          status: 415,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    if (url === "/api/workflows/run") {
      return new Response(
        JSON.stringify({
          status: "completed",
          outputs: [
            {
              answer: "基于知识库 kb-local 的结果：用户、登录与 OCR 已从 rag-myFlow 中移除。",
              citations: [
                {
                  document_id: "doc-001",
                  chunk_id: "chunk-001",
                  snippet: "用户、登录与 OCR 已从 rag-myFlow 中移除。",
                },
              ],
            },
          ],
        }),
        {
          status: 200,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    throw new Error(`unexpected fetch call: ${url}`);
  });
});

test("renders primary navigation", () => {
  render(<App />);

  expect(screen.getByText("知识库")).toBeInTheDocument();
  expect(screen.getByText("对话")).toBeInTheDocument();
  expect(screen.getByText("工作流")).toBeInTheDocument();
  expect(screen.getByText("设置")).toBeInTheDocument();
});

test("loads health data in settings page", async () => {
  render(<App />);

  fireEvent.click(screen.getByRole("button", { name: "设置" }));

  await waitFor(() => {
    expect(screen.getByText("工作区：local")).toBeInTheDocument();
  });
});

test("submits chat form and renders answer", async () => {
  render(<App />);

  fireEvent.click(screen.getByRole("button", { name: "对话" }));
  fireEvent.click(screen.getByRole("button", { name: "发送问题" }));

  await waitFor(() => {
    expect(screen.getByText(/基于知识库 kb-local 的结果/)).toBeInTheDocument();
  });
});

test("shows OCR rejection in knowledge page", async () => {
  render(<App />);

  const fileInput = screen.getByLabelText("选择文件");
  fireEvent.change(fileInput, {
    target: {
      files: [new File(["fake-png"], "scan.png", { type: "image/png" })],
    },
  });
  fireEvent.click(screen.getByRole("button", { name: "上传文件" }));

  await waitFor(() => {
    expect(screen.getByRole("alert")).toHaveTextContent("该文件类型依赖 OCR");
  });
});
