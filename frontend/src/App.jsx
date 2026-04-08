import { useEffect, useMemo, useState } from "react";
import {
  BarChart, Bar, PieChart, Pie, LineChart, Line,
  XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid
} from "recharts";
import { apiRequest, login } from "./api";

const defaultIncident = {
  title: "",
  source: "Manual",
  severity: "Medium",
  threat_type: "Unknown",
  summary: "",
  analyst_notes: "",
  raw_event: "",
  status: "Open",
};

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [active, setActive] = useState("dashboard");
  const [metrics, setMetrics] = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [comments, setComments] = useState([]);
  const [triageResult, setTriageResult] = useState(null);
  const [message, setMessage] = useState("");
  const [loginForm, setLoginForm] = useState({ username: "admin", password: "Admin123!" });
  const [incidentForm, setIncidentForm] = useState(defaultIncident);
  const [triageText, setTriageText] = useState("Impossible travel sign-in followed by multiple failed login attempts from unknown IP.");
  const [commentBody, setCommentBody] = useState("");

  async function loadDashboard() {
    if (!token) return;
    const [m, i] = await Promise.all([
      apiRequest("/api/dashboard/metrics", "GET", null, token),
      apiRequest("/api/incidents", "GET", null, token),
    ]);
    setMetrics(m);
    setIncidents(i);
  }

  useEffect(() => {
    loadDashboard().catch((err) => setMessage(err.message));
  }, [token]);

  async function handleLogin(e) {
    e.preventDefault();
    setMessage("");
    try {
      const data = await login(loginForm.username, loginForm.password);
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
      setActive("dashboard");
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function handleCreateIncident(e) {
    e.preventDefault();
    setMessage("");
    try {
      await apiRequest("/api/incidents", "POST", incidentForm, token);
      setIncidentForm(defaultIncident);
      setMessage("Incident created.");
      await loadDashboard();
      setActive("incidents");
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function handleSelectIncident(incident) {
    setSelectedIncident(incident);
    setActive("incident-detail");
    try {
      const data = await apiRequest(`/api/incidents/${incident.id}/comments`, "GET", null, token);
      setComments(data);
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function handleAddComment(e) {
    e.preventDefault();
    if (!selectedIncident) return;
    try {
      await apiRequest(
        `/api/incidents/${selectedIncident.id}/comments`,
        "POST",
        { incident_id: selectedIncident.id, body: commentBody },
        token
      );
      setCommentBody("");
      const data = await apiRequest(`/api/incidents/${selectedIncident.id}/comments`, "GET", null, token);
      setComments(data);
    } catch (err) {
      setMessage(err.message);
    }
  }

  async function handleTriage(e) {
    e.preventDefault();
    try {
      const data = await apiRequest("/api/ai/triage", "POST", { text: triageText }, token);
      setTriageResult(data);
      setIncidentForm((prev) => ({
        ...prev,
        title: "AI Triaged Alert",
        severity: data.severity,
        threat_type: data.threat_type,
        summary: data.summary,
        analyst_notes: data.recommendation,
        raw_event: triageText,
      }));
    } catch (err) {
      setMessage(err.message);
    }
  }

  const severityData = useMemo(() => metrics?.by_severity || [], [metrics]);
  const sourceData = useMemo(() => metrics?.by_source || [], [metrics]);
  const timelineData = useMemo(() => metrics?.timeline || [], [metrics]);

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">CyberSec Copilot</div>
        <button className={active === "login" ? "nav active" : "nav"} onClick={() => setActive("login")}>Login</button>
        <button className={active === "dashboard" ? "nav active" : "nav"} onClick={() => setActive("dashboard")}>Dashboard</button>
        <button className={active === "triage" ? "nav active" : "nav"} onClick={() => setActive("triage")}>AI Triage</button>
        <button className={active === "create-incident" ? "nav active" : "nav"} onClick={() => setActive("create-incident")}>Create Incident</button>
        <button className={active === "incidents" ? "nav active" : "nav"} onClick={() => setActive("incidents")}>Incidents</button>
      </aside>

      <main className="main">
        <header className="topbar">
          <h1>{active === "dashboard" ? "Security Operations Dashboard" : "CyberSec Copilot Enterprise"}</h1>
          <div className="token-state">{token ? "Authenticated" : "Not logged in"}</div>
        </header>

        {message && <div className="banner">{message}</div>}

        {active === "login" && (
          <section className="card form-card">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
              <input value={loginForm.username} onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })} placeholder="Username" />
              <input type="password" value={loginForm.password} onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })} placeholder="Password" />
              <button type="submit">Sign in</button>
            </form>
            <p className="help-text">Default seeded admin: admin / Admin123!</p>
          </section>
        )}

        {active === "dashboard" && metrics && (
          <>
            <section className="stats-grid">
              <div className="stat-card"><span>Total Incidents</span><strong>{metrics.total_incidents}</strong></div>
              <div className="stat-card"><span>Open Incidents</span><strong>{metrics.open_incidents}</strong></div>
              <div className="stat-card"><span>High / Critical</span><strong>{metrics.high_critical_incidents}</strong></div>
              <div className="stat-card"><span>Comments</span><strong>{metrics.total_comments}</strong></div>
            </section>

            <section className="chart-grid">
              <div className="card chart-card">
                <h3>Severity Distribution</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={severityData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="card chart-card">
                <h3>Incidents by Source</h3>
                <ResponsiveContainer width="100%" height={260}>
                  <PieChart>
                    <Pie data={sourceData} dataKey="count" nameKey="name" outerRadius={90} />
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </section>

            <section className="card chart-card">
              <h3>Incident Timeline</h3>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={timelineData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="count" />
                </LineChart>
              </ResponsiveContainer>
            </section>
          </>
        )}

        {active === "triage" && (
          <section className="grid-two">
            <div className="card">
              <h2>AI Alert Triage</h2>
              <form onSubmit={handleTriage} className="form-stack">
                <textarea rows="10" value={triageText} onChange={(e) => setTriageText(e.target.value)} />
                <button type="submit">Analyze Alert</button>
              </form>
            </div>
            <div className="card">
              <h2>Triage Result</h2>
              {triageResult ? (
                <div className="result-box">
                  <p><strong>Severity:</strong> {triageResult.severity}</p>
                  <p><strong>Threat Type:</strong> {triageResult.threat_type}</p>
                  <p><strong>Summary:</strong> {triageResult.summary}</p>
                  <p><strong>Recommendation:</strong> {triageResult.recommendation}</p>
                  <p><strong>Provider:</strong> {triageResult.provider}</p>
                </div>
              ) : <p>No triage result yet.</p>}
            </div>
          </section>
        )}

        {active === "create-incident" && (
          <section className="card">
            <h2>Create Incident</h2>
            <form onSubmit={handleCreateIncident} className="form-stack">
              <input value={incidentForm.title} onChange={(e) => setIncidentForm({ ...incidentForm, title: e.target.value })} placeholder="Title" />
              <input value={incidentForm.source} onChange={(e) => setIncidentForm({ ...incidentForm, source: e.target.value })} placeholder="Source" />
              <select value={incidentForm.severity} onChange={(e) => setIncidentForm({ ...incidentForm, severity: e.target.value })}>
                <option>Low</option><option>Medium</option><option>High</option><option>Critical</option>
              </select>
              <input value={incidentForm.threat_type} onChange={(e) => setIncidentForm({ ...incidentForm, threat_type: e.target.value })} placeholder="Threat type" />
              <textarea rows="5" value={incidentForm.summary} onChange={(e) => setIncidentForm({ ...incidentForm, summary: e.target.value })} placeholder="Summary" />
              <textarea rows="4" value={incidentForm.analyst_notes} onChange={(e) => setIncidentForm({ ...incidentForm, analyst_notes: e.target.value })} placeholder="Analyst notes" />
              <textarea rows="4" value={incidentForm.raw_event} onChange={(e) => setIncidentForm({ ...incidentForm, raw_event: e.target.value })} placeholder="Raw event" />
              <button type="submit">Save Incident</button>
            </form>
          </section>
        )}

        {active === "incidents" && (
          <section className="card">
            <h2>Incidents</h2>
            <div className="incident-list">
              {incidents.map((incident) => (
                <button key={incident.id} className="incident-row" onClick={() => handleSelectIncident(incident)}>
                  <div>
                    <strong>{incident.title}</strong>
                    <div className="muted">{incident.source}</div>
                  </div>
                  <div>{incident.severity}</div>
                  <div>{incident.status}</div>
                </button>
              ))}
            </div>
          </section>
        )}

        {active === "incident-detail" && selectedIncident && (
          <section className="grid-two">
            <div className="card">
              <h2>{selectedIncident.title}</h2>
              <p><strong>Severity:</strong> {selectedIncident.severity}</p>
              <p><strong>Source:</strong> {selectedIncident.source}</p>
              <p><strong>Threat Type:</strong> {selectedIncident.threat_type}</p>
              <p><strong>Status:</strong> {selectedIncident.status}</p>
              <p><strong>Summary:</strong> {selectedIncident.summary}</p>
              <p><strong>Analyst Notes:</strong> {selectedIncident.analyst_notes || "None"}</p>
              <pre className="raw-box">{selectedIncident.raw_event || "No raw event"}</pre>
            </div>

            <div className="card">
              <h2>Comments</h2>
              <div className="comment-list">
                {comments.map((comment) => (
                  <div key={comment.id} className="comment">
                    <strong>{comment.author}</strong>
                    <p>{comment.body}</p>
                  </div>
                ))}
              </div>
              <form onSubmit={handleAddComment} className="form-stack">
                <textarea rows="4" value={commentBody} onChange={(e) => setCommentBody(e.target.value)} placeholder="Add analyst comment" />
                <button type="submit">Add Comment</button>
              </form>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
