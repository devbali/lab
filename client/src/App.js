import './App.css';
import { Routes, Route } from "react-router-dom";
import Welcome from "./Welcome"
import {Signin, Signup} from "./Login"

const App = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Welcome/>}/>
        <Route path="/login" element={<Signin/>}/>
        <Route path="/forgot" element={<Signup/>}/>
      </Routes>
    </>

    
  );
}

export default App;
