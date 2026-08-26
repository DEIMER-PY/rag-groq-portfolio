import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Dashboard } from "./Dashboard";
import * as statsClient from "../api/statsClient";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Dashboard", () => {
  it("renders stats after loading", async () => {
    vi.spyOn(statsClient, "fetchStats").mockResolvedValue({
      total_documents: 185,
      documents_by_module: [
        { module: "backend", chunk_count: 39 },
        { module: "frontend", chunk_count: 31 },
      ],
      total_queries: 10,
      in_scope_queries: 8,
      web_fallback_queries: 2,
      recent_queries: [
        { query: "que es SOLID", in_scope: true, used_web_fallback: false, created_at: "2026-01-01T00:00:00Z" },
      ],
    });

    render(<Dashboard />);

    expect(screen.getByText(/cargando/i)).toBeInTheDocument();

    await waitFor(() => expect(screen.getByText("185")).toBeInTheDocument());
    expect(screen.getByText("10")).toBeInTheDocument();
    expect(screen.getByText("20%")).toBeInTheDocument();
    expect(screen.getByText("backend")).toBeInTheDocument();
    expect(screen.getByText("que es SOLID")).toBeInTheDocument();
  });

  it("shows an error message when the request fails", async () => {
    vi.spyOn(statsClient, "fetchStats").mockRejectedValue(new Error("network error"));

    render(<Dashboard />);

    await waitFor(() => expect(screen.getByRole("alert")).toBeInTheDocument());
  });

  it("shows an empty state when there are no recent queries", async () => {
    vi.spyOn(statsClient, "fetchStats").mockResolvedValue({
      total_documents: 0,
      documents_by_module: [],
      total_queries: 0,
      in_scope_queries: 0,
      web_fallback_queries: 0,
      recent_queries: [],
    });

    render(<Dashboard />);

    await waitFor(() => expect(screen.getByText(/todavía no hay preguntas/i)).toBeInTheDocument());
  });
});
