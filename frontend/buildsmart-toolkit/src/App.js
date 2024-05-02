import './App.css';
import Helmet from "react-helmet";
import { BrowserRouter, Route, Link, Routes } from 'react-router-dom';
import { ResultDay, ResultWeek } from "./Result.js"
import { Home } from "./Home.js"

function App() {
  return (
    <div>
      <Helmet>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
      </Helmet>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict-day" element={<ResultDay />} />
          <Route path="/predict-week" element={<ResultWeek />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
