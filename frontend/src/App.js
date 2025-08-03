import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, CssBaseline } from '@mui/material';

import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RegisterPage from './pages/RegisterPage'; // Import the new page

const PublicLayout = ({ children }) => (
  <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
    <CssBaseline />
    <Header />
    <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
      {children}
    </Box>
    <Footer />
  </Box>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} /> {/* Add this route */}
        <Route path="/" element={<PublicLayout><HomePage /></PublicLayout>} />
      </Routes>
    </Router>
  );
}

export default App;