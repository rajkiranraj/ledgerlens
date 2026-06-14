import { useState, useEffect, useRef } from 'react';
import { Sparkles, Wallet, LogIn, ShieldAlert } from 'lucide-react';
import Dashboard from './components/Dashboard';
import CSVImportWizard from './components/CSVImportWizard';
import ImportReport from './components/ImportReport';
import { API_BASE_URL } from './config';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [groupId, setGroupId] = useState(null);
  const [importActive, setImportActive] = useState(false);
  const [selectedImportId, setSelectedImportId] = useState(null);

  // Login form state
  const [username, setUsername] = useState('demo'); // Default helper selection
  const [password, setPassword] = useState('password123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Grid scroll parallax and login card spotlight
  const gridRef = useRef(null);
  const loginCardRef = useRef(null);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setGroupId(null);
    setImportActive(false);
    setSelectedImportId(null);
  };

  const validateToken = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/status/`, {
        headers: { Authorization: `Token ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        fetchGroup(token);
      } else {
        handleLogout();
      }
    } catch {
      handleLogout();
    }
  };

  const fetchGroup = async (authToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/groups/`, {
        headers: { Authorization: `Token ${authToken}` },
      });
      if (response.ok) {
        const data = await response.json();
        if (data.length > 0) {
          setGroupId(data[0].id);
        } else {
          // If no groups, auto-create a default group
          createDefaultGroup(authToken);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    const handleScroll = () => {
      if (gridRef.current) {
        gridRef.current.style.backgroundPositionY = `${window.scrollY * 0.4}px`;
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Spotlight effect
  const handleSpotlight = (e) => {
    if (loginCardRef.current) {
      const rect = loginCardRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      loginCardRef.current.style.setProperty('--mouse-x', `${x}px`);
      loginCardRef.current.style.setProperty('--mouse-y', `${y}px`);
    }
  };

  // Validate session on load
  useEffect(() => {
    if (token) {
      validateToken();
    }
  }, [token]);

  const createDefaultGroup = async (authToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/groups/`, {
        method: 'POST',
        headers: {
          Authorization: `Token ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: 'LedgerLens Group' }),
      });
      if (response.ok) {
        const data = await response.json();
        setGroupId(data.id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogin = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error(
          "Invalid username or password. Seeding defaults use 'password123'"
        );
      }

      const data = await response.json();
      localStorage.setItem('token', data.token);
      setToken(data.token);
      setUser(data.user);
      fetchGroup(data.token);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Helper select profile to login instantly
  const quickLogin = (uname) => {
    setUsername(uname);
    setPassword('password123');
  };

  // Render Login Card
  const renderLogin = () => (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '90vh',
        padding: '16px',
      }}
    >
      <div
        ref={loginCardRef}
        className="glass-panel spotlight-card"
        style={{
          width: '100%',
          maxWidth: '440px',
          display: 'flex',
          flexDirection: 'column',
          gap: '24px',
          padding: '40px 32px',
        }}
        onMouseMove={handleSpotlight}
      >
        <div
          style={{
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <div
            style={{
              background: 'rgba(193, 255, 114, 0.2)',
              padding: '12px',
              borderRadius: '16px',
              border: '1px solid rgba(193, 255, 114, 0.4)',
              display: 'inline-flex',
            }}
          >
            <Wallet size={36} style={{ color: 'var(--text-primary)' }} />
          </div>
          <h1 style={{ fontSize: '1.8rem', margin: '8px 0 0' }}>
            LedgerLens AI
          </h1>
          <p style={{ fontSize: '0.85rem' }}>
            AI-powered expense intelligence platform
          </p>
        </div>

        {error && (
          <div
            style={{
              color: 'var(--danger)',
              background: 'var(--danger-bg)',
              border: '1px solid var(--danger-border)',
              padding: '10px 14px',
              borderRadius: '8px',
              fontSize: '0.85rem',
              display: 'flex',
              gap: '8px',
              alignItems: 'center',
              textAlign: 'left',
            }}
          >
            <ShieldAlert size={18} />
            {error}
          </div>
        )}

        <form
          onSubmit={handleLogin}
          style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}
        >
          <div className="form-group" style={{ margin: 0 }}>
            <label>Username</label>
            <input
              type="text"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group" style={{ margin: 0 }}>
            <label>Password</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px' }}
            disabled={loading}
          >
            {loading ? 'Authenticating...' : 'Login'} <LogIn size={16} />
          </button>
        </form>

        {/* Quick select profile list */}
        <div
          style={{
            borderTop: '1px solid var(--panel-border-secondary)',
            paddingTop: '20px',
          }}
        >
          <span
            style={{
              fontSize: '0.8rem',
              color: 'var(--text-secondary)',
              display: 'block',
              marginBottom: '12px',
              textAlign: 'center',
            }}
          >
            <Sparkles size={12} className="icon" /> Quick Profile Selector
          </span>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '8px',
            }}
          >
            {['demo', 'admin', 'user'].map((name) => (
              <button
                key={name}
                className="btn btn-secondary"
                style={{
                  padding: '6px 4px',
                  fontSize: '0.8rem',
                  background:
                    username === name
                      ? 'rgba(193, 255, 114, 0.2)'
                      : 'rgba(0,0,0,0.02)',
                  borderColor:
                    username === name
                      ? 'rgba(193, 255, 114, 0.5)'
                      : 'var(--panel-border-secondary)',
                }}
                onClick={() => quickLogin(name)}
              >
                {name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <>
      <div ref={gridRef} className="grid-lines" />
      <div className="app-container">
        {!token || !user ? (
          renderLogin()
        ) : selectedImportId ? (
          <ImportReport
            importId={selectedImportId}
            groupId={groupId}
            token={token}
            onBack={() => setSelectedImportId(null)}
          />
        ) : importActive ? (
          <CSVImportWizard
            groupId={groupId}
            token={token}
            onImportSuccess={() => setImportActive(false)}
            onCancel={() => setImportActive(false)}
          />
        ) : (
          <Dashboard
            groupId={groupId}
            token={token}
            user={user}
            onLogout={handleLogout}
            onTriggerImport={() => setImportActive(true)}
            onSelectImport={(id) => setSelectedImportId(id)}
          />
        )}
      </div>
    </>
  );
}
