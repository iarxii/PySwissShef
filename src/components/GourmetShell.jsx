import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const GourmetShell = ({ children }) => {
  const [showSecurity, setShowSecurity] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const accepted = localStorage.getItem('pyswissshef_lab_accepted');
    if (!accepted) {
      setShowSecurity(true);
    }
  }, []);

  const acceptPolicy = () => {
    localStorage.setItem('pyswissshef_lab_accepted', 'true');
    setShowSecurity(false);
  };

  return (
    <div className={`lab-wrapper ${showSecurity ? 'hidden-overflow' : ''}`}>
      {/* Security Modal Overlay */}
      {showSecurity && (
        <div id="security-modal-overlay">
          <div className="glass-panel modal-content-glass shadow-lg">
            <h2 className="text-gold mb-4">🛡️ Laboratory Protocol</h2>
            <p className="mb-4 text-white">Welcome to the <strong>PySwissShef React Portal</strong>. You are accessing a high-fidelity simulation and documentation station for Python automation.</p>
            <div className="text-start mb-4 p-3 bg-dark border border-secondary rounded">
              <small className="text-gold fw-bold">ENV NOTICE:</small>
              <p className="small text-white-50 mb-0">This React portal is optimized for the 'Tasting Room' philosophy. To execute full-heat automation recipes, please use our Replit or Codespaces stations.</p>
            </div>
            <button 
              onClick={acceptPolicy}
              className="btn btn-gourmet w-100 p-3"
            >
              I UNDERSTAND & ENTER LABORATORY
            </button>
          </div>
        </div>
      )}

      {/* Gourmet Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark navbar-bistro sticky-top">
        <div className="container">
          <Link className="navbar-brand d-flex align-items-center" to="/">
            <img 
              src="/images/pyswisschef_ai_logo.png" 
              alt="Logo" 
              width="40" 
              height="40" 
              className="rounded-circle shadow-sm" 
            />
            <span className="ms-3 text-gold">PySwissShef <span className="fw-light small">LAB</span></span>
          </Link>
          <div className="ms-auto d-flex align-items-center">
            <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>MENU</Link>
            <a href="docs/LAB_STATIONS.md" className="nav-link">STATIONS</a>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="container py-5">
        {children}
      </main>

      {/* Global Footer */}
      <footer className="container py-4 mt-5 text-center border-top border-secondary">
        <p className="small text-mono text-gold">&copy; 2026 PySwissShef | Precise Code & Gourmet Diagnostics</p>
      </footer>
    </div>
  );
};

export default GourmetShell;
