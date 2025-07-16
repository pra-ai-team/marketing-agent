import React from 'react';
import ReactDOM from 'react-dom/client';
import CADEngine from './components/cad-engine/CADEngine';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CADEngine />
  </React.StrictMode>
);