import './App.css';
import { HeaderSection } from "./components/Header.js";
import { Query } from "./components/Query.js";
import { PredictQuery } from "./components/PredictQuery.js";
import Helmet from "react-helmet";

function App() {
  return (
    <div>
      <Helmet>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
      </Helmet>
      <HeaderSection />
      <Query />
      <PredictQuery />
    </div>
  );
}

export default App;
