import { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import ProjectList from './components/ProjectList';
import ProjectDetail from './components/ProjectDetail';
import AuthForm from './components/AuthForm';
import { api } from './api';

function EmptyState() {
  return (
    <div className="empty-state">
      <h1>Select a project</h1>
      <p className="muted-text">
        Choose a project from the sidebar, or create one to get started.
      </p>
    </div>
  );
}

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [checkingSession, setCheckingSession] = useState(true);
  const [projects, setProjects] = useState([]);
  const [loadingProjects, setLoadingProjects] = useState(false);
  const [error, setError] = useState(null);

  // On load, see if a session cookie from a previous visit is still valid.
  useEffect(() => {
    api
      .checkSession()
      .then(setCurrentUser)
      .catch(() => setCurrentUser(null))
      .finally(() => setCheckingSession(false));
  }, []);

  // Once logged in, load this user's projects.
  useEffect(() => {
    if (!currentUser) return;
    setLoadingProjects(true);
    api
      .getProjects()
      .then(setProjects)
      .catch((err) => setError(err.message))
      .finally(() => setLoadingProjects(false));
  }, [currentUser]);

  function handleProjectCreated(project) {
    setProjects((prev) => [...prev, project]);
  }

  function handleProjectDeleted(projectId) {
    setProjects((prev) => prev.filter((p) => p.id !== projectId));
  }

  function handleLogout() {
    api.logout().then(() => {
      setCurrentUser(null);
      setProjects([]);
    });
  }

  if (checkingSession) {
    return <p className="muted-text" style={{ padding: 24 }}>Loading…</p>;
  }

  if (!currentUser) {
    return <AuthForm onAuthenticated={setCurrentUser} />;
  }

  return (
    <div className="app-shell">
      <NavBar currentUser={currentUser} onLogout={handleLogout} />
      <div className="app-body">
        <ProjectList
          projects={projects}
          loading={loadingProjects}
          error={error}
          onProjectCreated={handleProjectCreated}
        />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<EmptyState />} />
            <Route
              path="/projects/:id"
              element={<ProjectDetail onProjectDeleted={handleProjectDeleted} />}
            />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
