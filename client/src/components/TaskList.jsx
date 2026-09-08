import { useState } from 'react';
import { api } from '../api';

const PRIORITIES = ['low', 'medium', 'high'];
const STATUSES = ['not_started', 'in_progress', 'completed'];

// Ranked tasks (from the most recent AI prioritization) come first, in rank
// order. Unranked tasks (never prioritized, or added after the last run)
// follow, in their original order.
function sortedTasks(tasks) {
  return [...tasks].sort((a, b) => {
    const rankA = a.priority_rank ?? Infinity;
    const rankB = b.priority_rank ?? Infinity;
    return rankA - rankB;
  });
}

function TaskRow({ task, onUpdate, onDelete }) {
  return (
    <li className={`task-row priority-${task.user_priority}`}>
      <div className="task-row-main">
        <span className="task-title">{task.title}</span>
      </div>

      <div className="task-row-controls">
        <input
          type="date"
          value={task.due_date || ''}
          onChange={(e) => onUpdate(task.id, { due_date: e.target.value })}
        />

        <select
          value={task.user_priority}
          onChange={(e) => onUpdate(task.id, { user_priority: e.target.value })}
        >
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>

        <select
          value={task.status}
          onChange={(e) => onUpdate(task.id, { status: e.target.value })}
        >
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {s.replace('_', ' ')}
            </option>
          ))}
        </select>

        <button className="task-delete" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>

      {task.priority_rank != null && (
        <div className="task-rationale">
          <span className="task-rank">#{task.priority_rank}</span>
          <p>{task.ai_rationale}</p>
        </div>
      )}
    </li>
  );
}

function TaskList({ projectId, tasks, onTasksChange }) {
  const [title, setTitle] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [priority, setPriority] = useState('medium');
  const [error, setError] = useState(null);

  function handleAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;

    const payload = {
      title,
      project_id: Number(projectId),
      user_priority: priority,
    };
    if (dueDate) payload.due_date = dueDate;

    api
      .createTask(payload)
      .then((task) => {
        onTasksChange([...tasks, task]);
        setTitle('');
        setDueDate('');
        setPriority('medium');
      })
      .catch((err) => setError(err.message));
  }

  function handleUpdate(taskId, changes) {
    api
      .updateTask(taskId, changes)
      .then((updated) => {
        onTasksChange(tasks.map((t) => (t.id === taskId ? updated : t)));
      })
      .catch((err) => setError(err.message));
  }

  function handleDelete(taskId) {
    api
      .deleteTask(taskId)
      .then(() => {
        onTasksChange(tasks.filter((t) => t.id !== taskId));
      })
      .catch((err) => setError(err.message));
  }

  return (
    <div className="task-list-section">
      <form className="task-form" onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
        <button type="submit">Add task</button>
      </form>

      {error && <p className="error-text">{error}</p>}

      {tasks.length === 0 ? (
        <p className="muted-text">No tasks yet. Add one above.</p>
      ) : (
        <ul className="task-list">
          {sortedTasks(tasks).map((task) => (
            <TaskRow
              key={task.id}
              task={task}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      )}
    </div>
  );
}

export default TaskList;
