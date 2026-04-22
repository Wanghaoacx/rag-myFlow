import "@testing-library/jest-dom/vitest";

import { render, screen } from "@testing-library/react";

import App from "../App";

test("renders primary navigation", () => {
  render(<App />);

  expect(screen.getByText("知识库")).toBeInTheDocument();
  expect(screen.getByText("对话")).toBeInTheDocument();
  expect(screen.getByText("工作流")).toBeInTheDocument();
  expect(screen.getByText("设置")).toBeInTheDocument();
});
