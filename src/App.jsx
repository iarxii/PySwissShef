import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GourmetShell from './components/GourmetShell';
import LaboratoryHome from './pages/LaboratoryHome';
import RecipeDetail from './pages/RecipeDetail';

function App() {
  return (
    <Router>
      <GourmetShell>
        <Routes>
          <Route path="/" element={<LaboratoryHome />} />
          <Route path="/recipe/:id" element={<RecipeDetail />} />
          {/* Fallback to home */}
          <Route path="*" element={<LaboratoryHome />} />
        </Routes>
      </GourmetShell>
    </Router>
  );
}

export default App;
