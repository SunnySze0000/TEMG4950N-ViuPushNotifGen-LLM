import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Homepage } from "./pages/Homepage";
import { TestPage } from "./fetch";
import GenerationPage from './pages/GenerationPage';
import ViuDataComponent from './pages/ViuDataComponent';

function App() {
  
  return (
    // <div>
    //   <h1>Viu Data</h1>
    //   <ViuDataComponent />
    // </div>

    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/generation" element={<GenerationPage />} />
          <Route path="/test" element={<TestPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;