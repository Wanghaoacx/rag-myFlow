import { useEffect, useState } from "react";

import { getHealth, type HealthResponse } from "../lib/api";

export function SettingsPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  async function loadHealth() {
    setError("");
    setIsLoading(true);

    try {
      const response = await getHealth();
      setHealth(response);
    } catch (loadingError) {
      setError(loadingError instanceof Error ? loadingError.message : "读取系统状态失败");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadHealth();
  }, []);

  return (
    <section>
      <h2>模型与系统设置</h2>
      <button type="button" onClick={() => void loadHealth()}>
        刷新系统状态
      </button>

      {isLoading ? <p>读取系统状态中...</p> : null}
      {health ? (
        <div>
          <p>工作区：{health.workspace}</p>
          <p>状态：{health.status}</p>
        </div>
      ) : null}
      {error ? <p role="alert">{error}</p> : null}
    </section>
  );
}
