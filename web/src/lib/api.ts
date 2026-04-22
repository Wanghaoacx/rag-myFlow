export type HealthResponse = {
  status: string;
  workspace: string;
};

export type ApiErrorPayload = {
  code?: string;
  message?: string;
  detail?: {
    message?: string;
  };
};

export type DocumentRequest = {
  file_name: string;
  mime_type: string;
  has_text_layer: boolean;
};

export type DocumentResponse = {
  document_id: string;
  file_name: string;
  mime_type: string;
};

export type Citation = {
  document_id: string;
  chunk_id: string;
  snippet: string;
};

export type ChatRequest = {
  question: string;
  knowledge_base_ids: string[];
};

export type ChatResponse = {
  answer: string;
  citations: Citation[];
};

export type WorkflowStep = {
  kind: string;
  payload: Record<string, unknown>;
};

export type WorkflowRequest = {
  workflow_id: string;
  steps: WorkflowStep[];
};

export type WorkflowResponse = {
  status: string;
  outputs: Array<Record<string, unknown>>;
};

function getErrorMessage(payload: ApiErrorPayload | null, fallback: string): string {
  if (!payload) {
    return fallback;
  }

  if (payload.message) {
    return payload.message;
  }

  if (payload.detail?.message) {
    return payload.detail.message;
  }

  return fallback;
}

async function parseJson<T>(response: Response): Promise<T> {
  return (await response.json()) as T;
}

async function request<T>(input: string, init?: RequestInit): Promise<T> {
  const isFormData = init?.body instanceof FormData;
  const response = await fetch(input, {
    headers: isFormData
      ? init?.headers
      : {
          "Content-Type": "application/json",
          ...(init?.headers ?? {}),
        },
    ...init,
  });

  if (!response.ok) {
    let payload: ApiErrorPayload | null = null;
    try {
      payload = await parseJson<ApiErrorPayload>(response);
    } catch {
      payload = null;
    }
    throw new Error(getErrorMessage(payload, `request failed: ${response.status}`));
  }

  return parseJson<T>(response);
}

export async function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/api/health");
}

export async function createDocument(payload: DocumentRequest): Promise<DocumentResponse> {
  return request<DocumentResponse>("/api/documents", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function uploadDocument(
  file: File,
  hasTextLayer: boolean,
): Promise<DocumentResponse> {
  const payload = new FormData();
  payload.append("file", file);
  payload.append("has_text_layer", String(hasTextLayer));

  return request<DocumentResponse>("/api/documents/upload", {
    method: "POST",
    body: payload,
  });
}

export async function answerQuestion(payload: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat/answer", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function runWorkflow(payload: WorkflowRequest): Promise<WorkflowResponse> {
  return request<WorkflowResponse>("/api/workflows/run", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
