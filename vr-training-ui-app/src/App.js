import logo from './logo.svg';
import './App.css';
import background1 from './bg-1.png';
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ExperimentUI from './components/experiment-ui';
import ExperimentHasFinished from './components/experiment-has-finished';
import ExperimentWillStart from './components/experiment-will-start';
import ExperimentCurrent from './components/experiment-current';


function App() {
  return (
    <BrowserRouter>
   <Routes>
      <Route path="/start" element={<ExperimentWillStart />} />
      <Route path="/experiment" element={<ExperimentCurrent auditOnly={false} />} />
      <Route path="/end" element={<ExperimentHasFinished />} />
      <Route path="/audit-experiment" element={<ExperimentCurrent auditOnly={true} />} />
      <Route exact path="/" element={<ExperimentWillStart />} />
      
    </Routes>
  </BrowserRouter>
  );
}

export default App;
