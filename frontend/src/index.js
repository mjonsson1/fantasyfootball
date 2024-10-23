import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Make sure you have an App.js file as well
// import './index.css'; // Optional, for your CSS styles

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
