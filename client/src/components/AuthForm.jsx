import { useState } from 'react';
import { api } from '../api';

function AuthForm({ onAuthenticated }) {
  const [mode, setMode] = useState('login'); // 'login' | 'signup'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const submit = mode === 'login' ? api.login : api.signup;

    submit({ username, password })
      .then(onAuthenticated)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  return (
    <div className="auth-screen">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h1 className="auth-title">Smart Task Prioritizer</h1>
        <p className="muted-text">
          {mode === 'login' ? 'Log in to continue.' : 'Create an account to get started.'}
        </p>

        {error && <p className="error-text">{error}</p>}

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Sign up'}
        </button>

        <button
          type="button"
          className="auth-toggle"
          onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}
        >
          {mode === 'login'
            ? "Need an account? Sign up"
            : 'Already have an account? Log in'}
        </button>
      </form>
    </div>
  );
}

export default AuthForm;
