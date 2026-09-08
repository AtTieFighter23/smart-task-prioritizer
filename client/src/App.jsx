import { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import ProjectList from './components/ProjectList';
import ProjectDetail from './components/ProjectDetail';
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
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .getProjects()
      .then(setProjects)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  function handleProjectCreated(project) {
    setProjects((prev) => [...prev, project]);
  }

  function handleProjectDeleted(projectId) {
    setProjects((prev) => prev.filter((p) => p.id !== projectId));
  }

  return (
    <div className="app-shell">
      <NavBar />
      <div className="app-body">
        <ProjectList
          projects={projects}
          loading={loading}
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
