import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import logo from '../../assets/logo-light.png';

const Header = () => {
  return (
    <AppBar position="static" color="transparent" elevation={1}>
      <Toolbar>
        <img src={logo} alt="ZeroLoop Logo" style={{ height: '40px', marginRight: '16px' }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          ZeroLoop Technology
        </Typography>
        <Button color="inherit" component={Link} to="/">Home</Button>
        <Button color="inherit">About Us</Button>
        <Button color="inherit">Services</Button>
        <Button color="inherit" component={Link} to="/login">Login</Button>
        <Button variant="contained" component={Link} to="/register">Sign Up</Button>
      </Toolbar>
    </AppBar>
  );
};
export default Header;