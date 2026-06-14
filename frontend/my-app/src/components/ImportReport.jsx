import { useState, useEffect } from 'react';
import { Download, ArrowLeft } from 'lucide-react';
import { API_BASE_URL } from '../config';

export default function ImportReport({ importId, groupId, token, onBack }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [aiSummary, setAiSummary] = useState(null);
  const [aiSummaryLoading, setAiSummaryLoading] = useState(false);

  const fetchReport = async () => {
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/groups/${groupId}/imports/${importId}/report/`,
        { headers: { Authorization: `Token ${token}` } }
      );
      if (!res.ok) throw new Error('Failed to fetch import report');
      const data = await res.json();
      setReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAiSummary = async () => {
    setAiSummaryLoading(true);
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/groups/${groupId}/ai/import-summary/${importId}/`,
        {
          method: 'POST',
          headers: {
            Authorization: `Token ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
      if (res.ok) {
        const data = await res.json();
        setAiSummary(data);
      }
    } catch (err) {
      console.error('Failed to fetch AI summary:', err);
    } finally {
      setAiSummaryLoading(false);
    }
  };

  const handleExport = async (formatType) => {
    try {
      const res = await fetch(
        `${API_BASE_URL}/api/groups/${groupId}/imports/${importId}/export/${formatType}/`,
        { headers: { Authorization: `Token ${token}` } }
      );
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `import-report-${importId}.${formatType}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export error:', err);
    }
  };

  useEffect(() => {
    if (importId) {
      fetchReport();
      fetchAiSummary();
    }
  }, [importId, groupId, token]);

  if (loading) {
    return (
      <div
        className="glass-panel"
        style={{ textAlign: 'center', padding: '60px 32px' }}
      >
        <h2>Loading Import Report...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel" style={{ padding: '32px' }}>
        <p style={{ color: 'var(--danger)' }}>{error}</p>
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={16} /> Go Back
        </button>
      </div>
    );
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'var(--danger)';
      case 'warning': return 'var(--warning)';
      case 'error': return 'var(--danger)';
      case 'info': return 'var(--text-secondary)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div
        className="glass-panel"
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '16px 24px',
        }}
      >
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-secondary" onClick={() => handleExport('json')}>
            <Download size={16} /> Export JSON
          </button>
          <button className="btn btn-primary" onClick={() => handleExport('pdf')}>
            <Download size={16} /> Export PDF
          </button>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '32px' }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1>Import Report</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
            File: {report?.import_record?.file_name}
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Imported at: {report?.import_record?.completed_at ? new Date(report.import_record.completed_at).toLocaleString() : 'N/A'}
          </p>
          {report?.processing_duration_seconds && (
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              Processing time: {report.processing_duration_seconds} seconds
            </p>
          )}
        </div>

        {report?.import_record && (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '16px',
              marginBottom: '32px',
            }}
          >
            <div
              style={{
                textAlign: 'center',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--panel-border)',
              }}
            >
              <div style={{ fontSize: '2rem', fontWeight: 700 }}>
                {report.import_record.total_rows}
              </div>
              <div
                style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}
              >
                Total Rows
              </div>
            </div>
            <div
              style={{
                textAlign: 'center',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--panel-border)',
              }}
            >
              <div
                style={{
                  fontSize: '2rem',
                  fontWeight: 700,
                  color: 'var(--success)',
                }}
              >
                {report.import_record.imported_rows}
              </div>
              <div
                style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}
              >
                Imported
              </div>
            </div>
            <div
              style={{
                textAlign: 'center',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--panel-border)',
              }}
            >
              <div
                style={{
                  fontSize: '2rem',
                  fontWeight: 700,
                  color: 'var(--accent)',
                }}
              >
                {report.import_record.corrected_rows}
              </div>
              <div
                style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}
              >
                Corrected
              </div>
            </div>
            <div
              style={{
                textAlign: 'center',
                padding: '16px',
                borderRadius: '8px',
                border: '1px solid var(--panel-border)',
              }}
            >
              <div
                style={{
                  fontSize: '2rem',
                  fontWeight: 700,
                  color: 'var(--danger)',
                }}
              >
                {report.import_record.rejected_rows}
              </div>
              <div
                style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}
              >
                Rejected
              </div>
            </div>
            {report?.anomaly_count !== undefined && (
              <div
                style={{
                  textAlign: 'center',
                  padding: '16px',
                  borderRadius: '8px',
                  border: '1px solid var(--panel-border)',
                }}
              >
                <div
                  style={{
                    fontSize: '2rem',
                    fontWeight: 700,
                    color: 'var(--warning)',
                  }}
                >
                  {report.anomaly_count}
                </div>
                <div
                  style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}
                >
                  Anomalies
                </div>
              </div>
            )}
          </div>
        )}

        {aiSummary?.summary && (
          <div
            className="glass-panel"
            style={{
              padding: '24px',
              marginBottom: '32px',
              background: 'linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(59,130,246,0.05) 100%)',
              border: '1px solid rgba(139,92,246,0.2)',
            }}
          >
            <h3 style={{ marginBottom: '16px' }}>AI Executive Summary</h3>
            <p style={{ lineHeight: '1.7', margin: 0 }}>
              {aiSummary.summary}
            </p>
          </div>
        )}

        {report?.anomaly_summary && Object.keys(report.anomaly_summary).length > 0 && (
          <div style={{ marginBottom: '32px' }}>
            <h3 style={{ marginBottom: '16px' }}>Anomaly Summary</h3>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Anomaly Type</th>
                    <th>Severity</th>
                    <th>Count</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(report.anomaly_summary).map(([type, data]) => (
                    <tr key={type}>
                      <td>{type}</td>
                      <td style={{ color: getSeverityColor(data.severity), fontWeight: 600 }}>
                        {data.severity}
                      </td>
                      <td>{data.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {report?.log_data?.logs && (
          <div>
            <h3 style={{ marginBottom: '16px' }}>Import Logs</h3>
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
                      <td>{log.csv_row || '-'}</td>
                      <td>{log.description}</td>
                      <td
                        style={{
                          color: log.action?.includes('Excluded')
                            ? 'var(--danger)'
                            : 'var(--success)',
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