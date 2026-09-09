import { Link } from 'react-router-dom';

function NavBar({ currentUser, onLogout }) {
  return (
    <header className="navbar">
      <Link to="/" className="navbar-title">
        Smart Task Prioritizer
      </Link>

      {currentUser && (
        <div className="navbar-user">
          <span className="muted-text">{currentUser.username}</span>
          <button className="logout-button" onClick={onLogout}>
            Log out
          </button>
        </div>
      )}
    </header>
  );
}

export default NavBar;
