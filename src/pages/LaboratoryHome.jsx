import React from 'react';
import { Link } from 'react-router-dom';
import recipes from '../data/recipes.json';

const LaboratoryHome = () => {
  return (
    <div className="fade-in">
      {/* Hero Section */}
      <section className="row align-items-center mb-5 animate-float">
        <div className="col-lg-4 text-center mb-4 mb-lg-0">
          <div className="glass-panel p-3 d-inline-block shadow-lg">
            <img 
              src="automation_portfolio/scripts/static/images/pyswisschef_ai_logo.png" 
              alt="PySwissShef Logo" 
              className="img-fluid rounded-circle" 
              style={{ maxWidth: '240px', border: '4px solid var(--gold)' }} 
            />
          </div>
        </div>
        <div className="col-lg-8">
          <h1 className="display-3 mb-3">Welcome to the <span className="text-gold">Laboratory</span></h1>
          <h4 className="fw-light mb-4">"Precisely code, high-heat automation, and gourmet diagnostics."</h4>
          <div className="glass-panel p-4">
            <p className="lead text-white-50">
              Explore my curated collection of Python automation recipes. 
              This <strong>React Tasting Room</strong> provides a high-fidelity preview of the Laboratory's tools, 
              complete with detailed stories and environment guides for high-heat execution.
            </p>
          </div>
        </div>
      </section>

      {/* Recipe Grid */}
      <section className="mb-5">
        <h2 className="mb-4 d-flex align-items-center">
          <span className="text-gold me-3">#</span> Chef's Tasting Menu
        </h2>
        
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-2 g-4">
          {recipes.map((recipe) => (
            <div className="col" key={recipe.id}>
              <div className="glass-card h-100 p-4 d-flex flex-column">
                <div className="mb-3 d-flex justify-content-between align-items-center">
                  <span className="badge rounded-pill bg-dark border border-secondary text-gold">
                    {recipe.category.toUpperCase()}
                  </span>
                  <small className="text-white-50 text-mono">{recipe.environment}</small>
                </div>
                <h3 className="h4 mb-3 text-white">{recipe.name}</h3>
                <p className="text-white-50 small mb-4">{recipe.description}</p>
                
                <div className="mt-auto pt-3 border-top border-secondary d-flex justify-content-between align-items-center">
                   <Link to={`/recipe/${recipe.id}`} className="btn btn-gourmet btn-sm">VIEW RECIPE</Link>
                   <span className={`small ${recipe.security.includes('High') ? 'text-danger' : 'text-success'}`}>
                     ● {recipe.security}
                   </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default LaboratoryHome;
