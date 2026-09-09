import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { api } from '../api';

function ProjectList({
  projects,
  loading,
  error: fetchError,
  onProjectCreated,
  hasMore,
  onLoadMore,
}) {
  const [name, setName] = useState('');
  const [createError, setCreateError] = useState(null);

  function handleSubmit(e) {
    e.preventDefault();
    if (!name.trim()) return;

    api
      .createProject({ name }) // owner is inferred from the session server-side
      .then((project) => {
        onProjectCreated(project);
        setName('');
      })
      .catch((err) => setCreateError(err.message));
  }

  const displayError = fetchError || createError;

  return (
    <aside className="sidebar">
      <h2 className="sidebar-heading">Projects</h2>

      {displayError && <p className="error-text">{displayError}</p>}

      {loading ? (
        <p className="muted-text">Loading projects…</p>
      ) : projects.length === 0 ? (
        <p className="muted-text">No projects yet. Add one below to get started.</p>
      ) : (
        <>
          <nav className="project-nav">
            {projects.map((project) => (
              <NavLink
                key={project.id}
                to={`/projects/${project.id}`}
                className={({ isActive }) =>
                  `project-nav-link${isActive ? ' active' : ''}`
                }
              >
                {project.name}
              </NavLink>
            ))}
          </nav>

          {hasMore && (
            <button type="button" className="load-more-button" onClick={onLoadMore}>
              Load more
            </button>
          )}
        </>
      )}

      <form className="new-project-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New project name"
        />
        <button type="submit">Add project</button>
      </form>
    </aside>
  );
}

export default ProjectList;
