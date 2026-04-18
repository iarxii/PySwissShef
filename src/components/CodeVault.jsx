import React, { useState } from 'react';
import { Copy, Check, Code } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const CodeVault = ({ code, fileName }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Custom Bistro Code Style
  const customStyle = {
    ...atomDark,
    'pre[class*="language-"]': {
      ...atomDark['pre[class*="language-"]'],
      background: 'transparent',
      padding: '0',
      margin: '0',
    },
    'code[class*="language-"]': {
      ...atomDark['code[class*="language-"]'],
      background: 'transparent',
      fontFamily: '"JetBrains Mono", monospace',
      fontSize: '14px',
    },
    'keyword': { color: '#ffd43b', fontWeight: 'bold' },
    'function': { color: '#ffd43b' },
    'class-name': { color: '#ffd43b' },
    'string': { color: '#a5d6ff' },
    'comment': { color: '#6a737d', fontStyle: 'italic' },
    'number': { color: '#ff7b72' },
    'operator': { color: '#adb5bd' },
    'property': { color: '#ffd43b' }
  };

  return (
    <div className="glass-panel mt-5 overflow-hidden shadow-lg border-gold-glow animate-fade-in-up">
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
        <SyntaxHighlighter
          language="python"
          style={customStyle}
          showLineNumbers={true}
          lineNumberStyle={{ minWidth: '3.5em', paddingRight: '1em', color: '#4a4a4a', textAlign: 'right', borderRight: '1px solid #2d2d2d', marginRight: '1em' }}
          containerStyle={{ margin: 0, padding: '1.5rem 0' }}
        >
          {code}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export default CodeVault;
