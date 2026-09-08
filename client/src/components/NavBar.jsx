import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <header className="navbar">
      <Link to="/" className="navbar-title">
        Smart Task Prioritizer
      </Link>
    </header>
  );
}

export default NavBar;
