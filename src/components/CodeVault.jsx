import React, { useState } from 'react';
import { Copy, Check, Code } from 'lucide-react';

const CodeVault = ({ code, fileName }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = code.split('\n');

  return (
    <div className="glass-panel mt-5 overflow-hidden shadow-lg border-gold-glow">
      <div className="bg-dark p-3 d-flex justify-content-between align-items-center border-bottom border-secondary">
        <div className="d-flex align-items-center">
          <Code className="text-gold me-2" size={20} />
          <span className="text-white-50 small text-mono">{fileName}</span>
        </div>
        <button 
          onClick={copyToClipboard}
          className="btn btn-sm btn-bistro-outline d-flex align-items-center"
        >
          {copied ? (
            <><Check size={14} className="me-2 text-success" /> COPIED</>
          ) : (
            <><Copy size={14} className="me-2" /> COPY CODE</>
          )}
        </button>
      </div>
      
      <div className="code-viewer-container" style={{ maxHeight: '80vh', overflowY: 'auto', background: '#0a0a0a' }}>
        <div className="d-flex w-100">
          {/* Gutter / Line Numbers */}
          <div className="bg-dark text-end p-3 pe-4 text-white-50 text-mono border-end border-secondary" style={{ minWidth: '60px', userSelect: 'none', fontSize: '13px' }}>
            {lines.map((_, i) => (
              <div key={i}>{i + 1}</div>
            ))}
          </div>

          {/* Code Content */}
          <div className="p-3 w-100 text-mono" style={{ whiteSpace: 'pre', overflowX: 'auto', fontSize: '14px', color: '#e9ecef' }}>
            {code}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CodeVault;
