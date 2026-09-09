const BASE_URL = 'http://localhost:5555';

function buildQuery(params) {
  const query = new URLSearchParams(params).toString();
  return query ? `?${query}` : '';
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include', // sends/receives the session cookie cross-port
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (res.status === 204) {
    if (!res.ok) throw new Error('Request failed.');
    return null;
  }

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const message = data?.error || `Request failed with status ${res.status}`;
    throw new Error(message);
  }

  return data;
}

export const api = {
  signup: (payload) =>
    request('/signup', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload) =>
    request('/login', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request('/logout', { method: 'DELETE' }),
  checkSession: () => request('/check_session'),

  // Both return { items, page, per_page, total, pages }
  getProjects: (params = {}) => request(`/projects${buildQuery(params)}`),
  getTasks: (params = {}) => request(`/tasks${buildQuery(params)}`),

  createProject: (payload) =>
    request('/projects', { method: 'POST', body: JSON.stringify(payload) }),
  getProject: (id) => request(`/projects/${id}`),
  deleteProject: (id) => request(`/projects/${id}`, { method: 'DELETE' }),

  createTask: (payload) =>
    request('/tasks', { method: 'POST', body: JSON.stringify(payload) }),
  updateTask: (id, payload) =>
    request(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteTask: (id) => request(`/tasks/${id}`, { method: 'DELETE' }),

  prioritize: (projectId) =>
    request(`/projects/${projectId}/prioritize`, { method: 'POST' }),
};

