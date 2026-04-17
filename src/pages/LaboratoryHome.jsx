import React from 'react';
import { Link } from 'react-router-dom';
import recipes from '../data/recipes.json';

const LaboratoryHome = () => {
  return (
    <div className="fade-in">
      {/* Hero Section - Streamlined for Premium Focus */}
      <section className="row align-items-center mb-5 py-4">
        <div className="col-12 text-center mb-4">
          <div className="animate-float d-inline-block">
            <div className="glass-panel p-2 rounded-circle shadow-lg" style={{ background: 'rgba(255, 212, 59, 0.05)' }}>
              <img 
                src="/images/pyswisschef_ai_logo.png" 
                alt="PySwissShef Logo" 
                className="img-fluid rounded-circle" 
                style={{ width: '160px', height: '160px', border: '2px solid var(--gold)', objectFit: 'contain' }} 
              />
            </div>
          </div>
          <h1 className="display-4 mt-4 fw-bold">THE <span className="text-gold">LABORATORY</span></h1>
          <p className="lead text-white-50 mx-auto" style={{ maxWidth: '700px' }}>
            A curated space for high-heat Python automation and gourmet diagnostic recipes. 
            Experience code precision in our controlled tasting room.
          </p>
        </div>
      </section>

      {/* Recipe Grid - Restored with Native Bootstrap */}
      <section className="mb-5">
        <h2 className="mb-4 d-flex align-items-center h4">
          <span className="text-gold me-3">#</span> Chef's Tasting Menu
        </h2>
        
        <div className="row g-4">
          {recipes.map((recipe) => (
            <div className="col-md-6 col-lg-6 mb-2" key={recipe.id}>
              <div className="glass-card h-100 p-4 d-flex flex-column">
                <div className="mb-3 d-flex flex-wrap justify-content-between align-items-center gap-2">
                  <span className="badge rounded-pill bg-dark border border-secondary text-gold px-3 py-2">
                    {recipe.category.toUpperCase()}
                  </span>
                  <small className="text-white-50 text-mono bg-dark px-2 py-1 rounded border border-secondary">
                    {recipe.environment}
                  </small>
                </div>
                <h3 className="h5 mb-3 text-white fw-bold">{recipe.name}</h3>
                <p className="text-white-50 small mb-4 flex-grow-1" style={{ lineHeight: '1.7' }}>
                  {recipe.description}
                </p>
                
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
