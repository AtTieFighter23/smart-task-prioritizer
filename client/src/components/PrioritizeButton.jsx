import { useState } from 'react';
import { api } from '../api';

function PrioritizeButton({ projectId, disabled, onPrioritized }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleClick() {
    setLoading(true);
    setError(null);
    api
      .prioritize(projectId)
      .then(onPrioritized)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  return (
    <div className="prioritize-section">
      <button
        className="prioritize-button"
        onClick={handleClick}
        disabled={disabled || loading}
      >
        {loading ? 'Prioritizing…' : 'Prioritize tasks'}
      </button>
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}

export default PrioritizeButton;
