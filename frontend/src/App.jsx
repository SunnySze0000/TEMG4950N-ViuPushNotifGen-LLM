import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Homepage } from "./pages/Homepage";
import { TestPage } from "./fetch";
import GenerationPage from './pages/GenerationPage';
import { SettingsProvider } from './pages/SettingsContext';
//hi
function App() {
  
  return (
    <SettingsProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/generation" element={<GenerationPage />} />
          <Route path="/test" element={<TestPage />} />
        </Routes>
      </Router>
    </SettingsProvider>
  );
}

export default App;