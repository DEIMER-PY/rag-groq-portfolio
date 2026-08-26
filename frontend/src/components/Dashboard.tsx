import { useStats } from "../hooks/useStats";

export function Dashboard() {
  const { stats, isLoading, error } = useStats();

  if (isLoading) return <div className="dashboard-status">Cargando estadísticas…</div>;
  if (error) return <div className="dashboard-status" role="alert">{error}</div>;
  if (!stats) return null;

  const maxChunks = Math.max(1, ...stats.documents_by_module.map((m) => m.chunk_count));
  const webFallbackPct = stats.total_queries
    ? Math.round((stats.web_fallback_queries / stats.total_queries) * 100)
    : 0;

  return (
    <div className="dashboard">
      <div className="dashboard-cards">
        <StatCard label="Chunks indexados" value={stats.total_documents} />
        <StatCard label="Preguntas respondidas" value={stats.total_queries} />
        <StatCard label="% con fallback web" value={`${webFallbackPct}%`} />
      </div>

      <section>
        <h3>Base de conocimiento por módulo</h3>
        <div className="module-bars">
          {stats.documents_by_module.map((m) => (
            <div className="module-bar-row" key={m.module}>
              <span className="module-bar-label">{m.module}</span>
              <div className="module-bar-track">
                <div
                  className="module-bar-fill"
                  style={{ width: `${(m.chunk_count / maxChunks) * 100}%` }}
                />
              </div>
              <span className="module-bar-value">{m.chunk_count}</span>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h3>Preguntas recientes</h3>
        {stats.recent_queries.length === 0 ? (
          <p className="dashboard-status">Todavía no hay preguntas registradas.</p>
        ) : (
          <ul className="recent-queries">
            {stats.recent_queries.map((q, i) => (
              <li key={i}>
                <span className={`scope-dot ${q.in_scope ? "in-scope" : "out-of-scope"}`} />
                <span className="recent-query-text">{q.query}</span>
                {q.used_web_fallback && <span className="web-tag">🌐 web</span>}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="stat-card">
      <div className="stat-card-value">{value}</div>
      <div className="stat-card-label">{label}</div>
    </div>
  );
}
