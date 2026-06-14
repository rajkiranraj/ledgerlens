import { useState, useEffect } from "react";
import { FileText, Download, ArrowLeft, CheckCircle } from "lucide-react";
import { API_BASE_URL } from "../config";

export default function ImportReport({ importId, groupId, token, onBack }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [aiSummary, setAiSummary] = useState(null);
  const [aiSummaryLoading, setAiSummaryLoading] = useState(false);

  const fetchAiSummary = async () => {
    setAiSummaryLoading(true);
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/groups/${groupId}/ai/import-summary/${importId}/`,
        {
          method: "POST",
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
        },
      );
      if (res.ok) {
        const data = await res.json();
        setAiSummary(data);
      }
    } catch (err) {
      console.error("Failed to fetch AI summary:", err);
    } finally {
      setAiSummaryLoading(false);
    }
  };

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await fetch(
          `${API_BASE_URL}/api/groups/${groupId}/imports/${importId}/report/`,
          { headers: { Authorization: `Token ${token}` } },
        );
        if (!res.ok) throw new Error("Failed to fetch import report");
        const data = await res.json();
        setReport(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    if (importId) {
      fetchReport();
      fetchAiSummary();
    }
  }, [importId, groupId, token]);

  const handleDownloadReport = () => {
    if (!report) return;
    const content = JSON.stringify(report, null, 2);
    const blob = new Blob([content], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `import-report-${importId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div
        className="glass-panel"
        style={{ textAlign: "center", padding: "60px 32px" }}
      >
        <h2>Loading Import Report...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel" style={{ padding: "32px" }}>
        <p style={{ color: "var(--danger)" }}>{error}</p>
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={16} /> Go Back
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      <div
        className="glass-panel"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "16px 24px",
        }}
      >
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
        <button className="btn btn-primary" onClick={handleDownloadReport}>
          <Download size={16} /> Download Report
        </button>
      </div>

      <div className="glass-panel" style={{ padding: "32px" }}>
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <CheckCircle
            size={48}
            style={{ color: "var(--success)", marginBottom: "16px" }}
          />
          <h1>Import Report {report.import_record?.id}</h1>
          <p style={{ color: "var(--text-secondary)", marginTop: "8px" }}>
            Imported at {new Date(report.imported_at).toLocaleString()}
          </p>
        </div>

        {report.import_record && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: "16px",
              marginBottom: "24px",
            }}
          >
            <div
              style={{
                textAlign: "center",
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid var(--panel-border)",
              }}
            >
              <div style={{ fontSize: "2rem", fontWeight: 700 }}>
                {report.import_record.total_rows}
              </div>
              <div
                style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}
              >
                Total Rows
              </div>
            </div>
            <div
              style={{
                textAlign: "center",
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid var(--panel-border)",
              }}
            >
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  color: "var(--success)",
                }}
              >
                {report.import_record.imported_rows}
              </div>
              <div
                style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}
              >
                Imported
              </div>
            </div>
            <div
              style={{
                textAlign: "center",
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid var(--panel-border)",
              }}
            >
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  color: "var(--accent)",
                }}
              >
                {report.import_record.corrected_rows}
              </div>
              <div
                style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}
              >
                Corrected
              </div>
            </div>
            <div
              style={{
                textAlign: "center",
                padding: "16px",
                borderRadius: "8px",
                border: "1px solid var(--panel-border)",
              }}
            >
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  color: "var(--danger)",
                }}
              >
                {report.import_record.rejected_rows}
              </div>
              <div
                style={{ fontSize: "0.85rem", color: "var(--text-secondary)" }}
              >
                Rejected
              </div>
            </div>
          </div>
        )}

        {/* AI Executive Summary */}
        <div
          className="glass-panel"
          style={{
            padding: "24px",
            marginBottom: "24px",
            background: "linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(59,130,246,0.05) 100%)",
            border: "1px solid rgba(139,92,246,0.2)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "16px" }}>
            <span style={{ fontSize: "1.5rem" }}>⚡</span>
            <h3 style={{ margin: 0 }}>AI Executive Summary</h3>
          </div>

          {aiSummaryLoading ? (
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <div style={{
                width: "32px",
                height: "32px",
                border: "3px solid rgba(139,92,246,0.2)",
                borderTop: "3px solid #8b5cf6",
                borderRadius: "50%",
                animation: "spin 1s linear infinite",
              }}></div>
              <p style={{ color: "var(--text-secondary)", margin: 0 }}>
                Analyzing import with NVIDIA AI...
              </p>
            </div>
          ) : aiSummary?.summary ? (
            <div style={{
              padding: "16px",
              background: "rgba(255,255,255,0.08)",
              borderRadius: "12px",
              border: "1px solid rgba(139,92,246,0.15)",
            }}>
              <p style={{ margin: 0, lineHeight: "1.7", fontWeight: "500" }}>
                {aiSummary.summary}
              </p>
            </div>
          ) : (
            <div style={{ textAlign: "center", padding: "16px" }}>
              <p style={{ color: "var(--text-secondary)", margin: 0 }}>
                No AI summary available.
              </p>
            </div>
          )}
        </div>

        {report.log_data?.logs && (
          <div>
            <h3 style={{ marginBottom: "16px" }}>
              <FileText size={20} className="icon" /> Import Logs
            </h3>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>CSV Row</th>
                    <th>Description</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {report.log_data.logs.map((log, idx) => (
                    <tr key={idx}>
                      <td>{log.csv_row || "-"}</td>
                      <td>{log.description}</td>
                      <td
                        style={{
                          color: log.action?.includes("Excluded")
                            ? "var(--danger)"
                            : "var(--success)",
                        }}
                      >
                        {log.action}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
