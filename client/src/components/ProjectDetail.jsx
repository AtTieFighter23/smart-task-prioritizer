import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api';
import TaskList from './TaskList';
import PrioritizeButton from './PrioritizeButton';

function ProjectDetail({ onProjectDeleted }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    setProject(null);
    setError(null);
    api
      .getProject(id)
      .then((data) => {
        setProject(data);
        setTasks(data.tasks);
      })
      .catch((err) => setError(err.message));
  }, [id]);

  function handleDeleteProject() {
    if (!window.confirm(`Delete "${project.name}" and all its tasks?`)) return;
    api
      .deleteProject(id)
      .then(() => {
        onProjectDeleted(Number(id));
        navigate('/');
      })
      .catch((err) => setError(err.message));
  }

  // The /prioritize endpoint only ranks non-completed tasks, so merge the
  // returned results back into the full list rather than replacing it —
  // completed tasks (excluded from ranking) must stay untouched.
  function handlePrioritized(rankedTasks) {
    setTasks((prev) =>
      prev.map((t) => rankedTasks.find((r) => r.id === t.id) || t)
    );
  }

  if (error) return <p className="error-text">{error}</p>;
  if (!project) return <p className="muted-text">Loading…</p>;

  return (
    <div>
      <div className="project-header">
        <h1 className="project-title">{project.name}</h1>
        <button className="delete-project-button" onClick={handleDeleteProject}>
          Delete project
        </button>
      </div>

      <PrioritizeButton
        projectId={id}
        disabled={tasks.length === 0}
        onPrioritized={handlePrioritized}
      />

      <TaskList projectId={id} tasks={tasks} onTasksChange={setTasks} />
    </div>
  );
}

export default ProjectDetail;
