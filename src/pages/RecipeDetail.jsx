import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Terminal, Shield, ChefHat, Play, Github, Download, Eye } from 'lucide-react';
import recipes from '../data/recipes.json';
import CodeVault from '../components/CodeVault';

// Gourmet Script Imports (Raw)
import excelScript from '../data/raw_scripts/Upload_Data_DB.py?raw';
import sentimentScript from '../data/raw_scripts/sentiment_analysis.py?raw';
import keywordScript from '../data/raw_scripts/textual_data_keyword_extractor.py?raw';
import schemaScript from '../data/raw_scripts/sql_analyser_mssql_db.py?raw';

const scriptMapping = {
  'Upload_Data_DB.py': excelScript,
  'sentiment_analysis.py': sentimentScript,
  'textual_data_keyword_extractor.py': keywordScript,
  'sql_analyser_mssql_db.py': schemaScript
};

const RecipeDetail = () => {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [isTasting, setIsTasting] = useState(false);
  const [consoleLogs, setConsoleLogs] = useState([]);
  const [showCode, setShowCode] = useState(false);

  useEffect(() => {
    const found = recipes.find(r => r.id === id);
    setRecipe(found);
    window.scrollTo(0, 0);
  }, [id]);

  const startTasting = () => {
    setIsTasting(true);
    setConsoleLogs(["[SYSTEM] Initializing In-Process Tasting engine...", "[SYSTEM] Loading recipe metadata..."]);
    
    // Simulate Gourmet Logs
    const simulatedLogs = [
      `[INFO] Target: ${recipe.file}`,
      "[INFO] Checking local environment constraints...",
      "[WARN] Restricted WASM environment detected (StackBlitz).",
      "[INFO] Executing gourmet diagnostic simulation...",
      ">>> PROCESSING LAYER 1: DATA INGESTION",
      ">>> PROCESSING LAYER 2: LOGIC RECONCILIATION",
      "[SUCCESS] Tasting complete. Diagnostic metrics captured.",
      "[NOTICE] To run this recipe at scale with actual file access, please switch to a High-Heat station."
    ];

    simulatedLogs.forEach((log, index) => {
      setTimeout(() => {
        setConsoleLogs(prev => [...prev, log]);
      }, (index + 1) * 600);
    });
  };

  if (!recipe) return <div className="text-center py-5"><h2 className="text-gold">Recipe Not Found</h2></div>;

  const scriptContent = scriptMapping[recipe.file] || "# RAW ACCESS RESTRICTED: Script not found in local vault.";

  return (
    <div className="fade-in">
      <nav aria-label="breadcrumb" className="mb-4 d-flex justify-content-between align-items-center">
        <Link to="/" className="text-gold text-decoration-none small">← BACK TO MENU</Link>
        <button 
          onClick={() => setShowCode(!showCode)} 
          className="btn btn-sm btn-bistro-outline d-flex align-items-center border-gold"
        >
          <Eye size={16} className="me-2" /> {showCode ? 'HIDE SOURCE' : 'INSPECT SOURCE'}
        </button>
      </nav>

      <div className="row g-5">
        <div className="col-lg-7">
          <div className="glass-panel p-5">
            <div className="d-flex align-items-center mb-3">
              <ChefHat className="text-gold me-3" size={32} />
              <h1 className="h2 text-white m-0">{recipe.name}</h1>
            </div>
            
            <div className="badge rounded-pill bg-dark border border-gold text-gold mb-4 p-2 px-3">
              {recipe.category}
            </div>

            <p className="lead text-white-50 mb-4">{recipe.description}</p>
            
            <h3 className="h5 text-gold mb-3 border-bottom border-secondary pb-2">The Gourmet Story</h3>
            <p className="text-white-50 mb-5">{recipe.detailed_description}</p>

            <div className="row g-4 mb-4">
              <div className="col-md-6">
                <div className="p-3 bg-dark rounded border border-secondary h-100">
                  <div className="d-flex align-items-center text-gold mb-2">
                    <Shield size={18} className="me-2" />
                    <strong>Security Profile</strong>
                  </div>
                  <small className="text-white-50">{recipe.security}</small>
                </div>
              </div>
              <div className="col-md-6">
                <div className="p-3 bg-dark rounded border border-secondary h-100">
                  <div className="d-flex align-items-center text-gold mb-2">
                    <Terminal size={18} className="me-2" />
                    <strong>Environment</strong>
                  </div>
                  <small className="text-white-50">{recipe.environment}</small>
                </div>
              </div>
            </div>

            <div className="d-flex gap-3">
              {recipe.repo_url && (
                <a href={recipe.repo_url} target="_blank" className="btn btn-bistro-outline d-flex align-items-center">
                  <Github size={18} className="me-2" /> GITHUB REPO
                </a>
              )}
              {recipe.release_url && (
                <a href={recipe.release_url} target="_blank" className="btn btn-bistro-outline d-flex align-items-center">
                  <Download size={18} className="me-2" /> DOWNLOAD
                </a>
              )}
            </div>
          </div>
        </div>

        <div className="col-lg-5">
          <div className="glass-panel p-4 h-100">
            <h3 className="h5 text-gold mb-4 d-flex align-items-center">
              <Play size={18} className="me-2" /> Tasting Terminal
            </h3>
            
            {!isTasting ? (
              <div className="text-center py-5">
                <p className="text-white-50 mb-4">Ready to taste the diagnostic output of this recipe?</p>
                <button onClick={startTasting} className="btn btn-gourmet">PREPARE & EXECUTE</button>
              </div>
            ) : (
              <div className="console-output shadow-lg mb-0" style={{ minHeight: '340px' }}>
                <pre className="m-0 small">
                  {consoleLogs.map((log, i) => (
                    <div key={i} className="mb-1">{log}</div>
                  ))}
                </pre>
              </div>
            )}

            <div className="mt-4 p-3 border border-warning rounded bg-warning bg-opacity-10">
              <p className="small text-warning mb-0">
                <strong>STRICTURE:</strong> Execution in this tasting room is simulated. Use Replit for native high-heat performance.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Full-Width Code Vault Section */}
      {showCode && (
        <div className="animate-fade-in-up">
          <CodeVault code={scriptContent} fileName={recipe.file} />
        </div>
      )}
    </div>
  );
};

export default RecipeDetail;
