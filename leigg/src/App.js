import './App.css';
import Navbar from './components/Navbar.js';
import Search from './components/Search.js';
import Footer from './components/Footer.js';
import Forum from './components/Forum.js';
import Coach from './components/Coach.js';
import Login from './components/Login.js';
import Signup from './components/Signup.js';
import Forgot from './components/Forgot.js';
import PostDetail from './components/PostDetail.js';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="App">
              <Navbar />
              <Search />
              <Footer />
            </div>
          }
          />
          <Route path="/forum" element={<Forum />} />
          <Route path="/coaching" element={<Coach />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/forgot-password" element={<Forgot />} />
          <Route path="/post/:postid" element={<PostDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
