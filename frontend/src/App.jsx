import React from "react";
import {
  Calendar,
  CheckSquare,
  FileText,
  LayoutDashboard,
  MessageSquare,
  Plus,
  StickyNote,
} from "lucide-react";
import "./App.css";

export default function App() {
  const [activeTab, setActiveTab] = React.useState("dashboard");
  const [message, setMessage] = React.useState(
    "Schedule interview tomorrow at 5 PM and create a task to prepare resume and save note: focus on backend questions"
  );
  const [response, setResponse] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [tasks, setTasks] = React.useState([]);
  const [events, setEvents] = React.useState([]);
  const [notes, setNotes] = React.useState([]);

  const API_BASE = "http://127.0.0.1:8000";

  const fetchCollection = async (path, setter, key) => {
    try {
      const res = await fetch(`${API_BASE}${path}`);
      if (!res.ok) throw new Error(`Failed to load ${key}`);
      const data = await res.json();
      setter(data[key] || []);
    } catch (err) {
      console.error(err);
    }
  };

  const refreshData = async () => {
    await Promise.all([
      fetchCollection("/tasks/", setTasks, "tasks"),
      fetchCollection("/events/", setEvents, "events"),
      fetchCollection("/notes/", setNotes, "notes"),
    ]);
  };

  React.useEffect(() => {
    refreshData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const res = await fetch(`${API_BASE}/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Request failed");
      }

      const data = await res.json();
      setResponse(data);
      await refreshData();
      setActiveTab("chat");
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "chat", label: "Chat", icon: MessageSquare },
    { id: "tasks", label: "Tasks", icon: CheckSquare },
    { id: "events", label: "Events", icon: Calendar },
    { id: "notes", label: "Notes", icon: FileText },
  ];

  const quickActions = [
    { label: "Start Chat", icon: MessageSquare, iconClass: "blue", tab: "chat" },
    { label: "New Task", icon: Plus, iconClass: "green", tab: "tasks" },
    { label: "Add Event", icon: Calendar, iconClass: "blue", tab: "events" },
    { label: "New Note", icon: StickyNote, iconClass: "purple", tab: "notes" },
  ];

  const formatMaybeDate = (value) => {
    if (!value) return "Not set";
    const d = new Date(value);
    return Number.isNaN(d.getTime()) ? value : d.toLocaleString();
  };

  const SidebarItem = ({ item }) => {
    const Icon = item.icon;
    const active = activeTab === item.id;

    return (
      <button
        onClick={() => setActiveTab(item.id)}
        className={`sidebar-item ${active ? "active" : ""}`}
      >
        <Icon size={20} />
        <span>{item.label}</span>
      </button>
    );
  };

  const ListItemCard = ({ title, subtitle, badge }) => (
    <div className="list-item-card">
      <div className="list-item-main">
        <div className="list-item-title">{title}</div>
        <div className="list-item-subtitle">{subtitle}</div>
      </div>
      {badge ? <span className="badge">{badge}</span> : null}
    </div>
  );

  const SectionCard = ({ title, icon: Icon, children }) => (
    <div className="section-card">
      <div className="section-header">
        <h3>{title}</h3>
        {Icon ? <Icon size={20} className="section-icon" /> : null}
      </div>
      {children}
    </div>
  );

  const DashboardView = () => (
    <div className="page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Welcome to your productivity assistant</p>
      </div>

      <div className="quick-grid">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <button
              key={action.label}
              className="quick-card"
              onClick={() => setActiveTab(action.tab)}
            >
              <Icon size={34} className={`quick-icon ${action.iconClass}`} />
              <div className="quick-label">{action.label}</div>
            </button>
          );
        })}
      </div>

      <div className="content-grid">
        <SectionCard title="Recent Tasks" icon={CheckSquare}>
          <div className="stack">
            {tasks.length ? (
              tasks.slice(0, 5).map((task) => (
                <ListItemCard
                  key={task.id}
                  title={task.title}
                  subtitle={`Due: ${formatMaybeDate(task.due_date)}`}
                  badge={task.priority || "medium"}
                />
              ))
            ) : (
              <div className="empty-box">No tasks yet.</div>
            )}
          </div>
        </SectionCard>

        <SectionCard title="Upcoming Events" icon={Calendar}>
          <div className="stack">
            {events.length ? (
              events.slice(0, 5).map((event) => (
                <ListItemCard
                  key={event.id}
                  title={event.title}
                  subtitle={formatMaybeDate(event.start_time)}
                />
              ))
            ) : (
              <div className="empty-box">No events yet.</div>
            )}
          </div>
        </SectionCard>

        <SectionCard title="Recent Notes" icon={FileText}>
          <div className="stack">
            {notes.length ? (
              notes.slice(0, 5).map((note) => (
                <ListItemCard
                  key={note.id}
                  title={note.title || "Quick Note"}
                  subtitle={note.content || "No content"}
                />
              ))
            ) : (
              <div className="empty-box">No notes yet.</div>
            )}
          </div>
        </SectionCard>
      </div>
    </div>
  );

  const ChatView = () => (
    <div className="page">
      <div className="page-header">
        <h1>Chat</h1>
        <p>Send one request to your orchestrator agent</p>
      </div>

      <div className="section-card">
        <form onSubmit={handleSubmit} className="chat-form">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            rows={5}
            className="chat-textarea"
            placeholder="Type your request here..."
          />
          <div className="chat-actions">
            <button type="submit" className="primary-btn" disabled={loading}>
              {loading ? "Running..." : "Send Request"}
            </button>
            <button
              type="button"
              className="secondary-btn"
              onClick={() =>
                setMessage(
                  "Schedule project review tomorrow at 4 PM, create a task to prepare slides, and save note: discuss API deployment"
                )
              }
            >
              Load Demo Prompt
            </button>
          </div>
        </form>
      </div>

      {error ? <div className="error-box">{error}</div> : null}

      {response ? (
        <div className="response-stack">
          <SectionCard title="Final Response">
            <p className="final-response">{response.final_response}</p>
          </SectionCard>

          <SectionCard title="Agents Used">
            <div className="agent-tags">
              {(response.agents_used || []).map((agent) => (
                <span key={agent} className="agent-tag">
                  {agent}
                </span>
              ))}
            </div>
          </SectionCard>

          <SectionCard title="Actions Returned">
            <div className="stack">
              {(response.actions || []).map((action, idx) => (
                <div key={idx} className="action-card">
                  <div className="action-tags">
                    <span className="action-agent">{action.agent}</span>
                    <span className="action-tool">{action.tool}</span>
                  </div>
                  <pre className="action-pre">
                    {JSON.stringify(action.input, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      ) : null}
    </div>
  );

  const CollectionView = ({ title, items, renderItem, emptyText }) => (
    <div className="page">
      <div className="page-header">
        <h1>{title}</h1>
        <p>Live data loaded from your FastAPI backend</p>
      </div>

      <SectionCard title={title}>
        <div className="stack">
          {items.length ? items.map(renderItem) : <div className="empty-box">{emptyText}</div>}
        </div>
      </SectionCard>
    </div>
  );

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <h2>Productivity Assistant</h2>
          <p>AI-powered task management</p>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <SidebarItem key={item.id} item={item} />
          ))}
        </nav>
      </aside>

      <main className="main-content">
        {activeTab === "dashboard" && DashboardView()}
        {activeTab === "chat" && ChatView()}
        {activeTab === "tasks" && (
          <CollectionView
            title="Tasks"
            items={tasks}
            emptyText="No tasks yet."
            renderItem={(task) => (
              <ListItemCard
                key={task.id}
                title={task.title}
                subtitle={`Due: ${formatMaybeDate(task.due_date)}`}
                badge={task.priority || "medium"}
              />
            )}
          />
        )}
        {activeTab === "events" && (
          <CollectionView
            title="Events"
            items={events}
            emptyText="No events yet."
            renderItem={(event) => (
              <ListItemCard
                key={event.id}
                title={event.title}
                subtitle={formatMaybeDate(event.start_time)}
              />
            )}
          />
        )}
        {activeTab === "notes" && (
          <CollectionView
            title="Notes"
            items={notes}
            emptyText="No notes yet."
            renderItem={(note) => (
              <ListItemCard
                key={note.id}
                title={note.title || "Quick Note"}
                subtitle={note.content || "No content"}
              />
            )}
          />
        )}
      </main>
    </div>
  );
}