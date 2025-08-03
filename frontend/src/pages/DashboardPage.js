import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Drawer, AppBar, Toolbar, Typography, List, ListItem, ListItemButton, ListItemIcon, ListItemText, CssBaseline, Divider } from '@mui/material';
import AssessmentIcon from '@mui/icons-material/Assessment';
import SettingsIcon from '@mui/icons-material/Settings';
import logo from '../assets/logo-light.png'; // Ensure correct file name
import Scanner from '../components/Scanner';

const drawerWidth = 240;

const DashboardPage = () => {
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: `calc(100% - ${drawerWidth}px)`,
          ml: `${drawerWidth}px`,
          backgroundColor: 'background.paper',
          color: 'text.primary'
        }}
        elevation={1}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: 'background.paper',
            borderRight: '1px solid rgba(0, 0, 0, 0.12)' // Darker divider for light theme
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <Box
          component={Link}
          to="/"
          sx={{
            p: 2,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: 64
          }}
        >
            <Box
              component="img"
              sx={{
                width: '90%', // Slightly larger logo
                height: 'auto',
              }}
              alt="ZeroLoop Technology Logo"
              src={logo}
            />
        </Box>
        <Divider sx={{ borderColor: 'rgba(0, 0, 0, 0.12)' }} />
        <List>
          {['Scanner', 'Settings'].map((text, index) => (
            <ListItem key={text} disablePadding>
              <ListItemButton>
                <ListItemIcon>
                  {index % 2 === 0 ? <AssessmentIcon /> : <SettingsIcon />}
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, bgcolor: 'background.default' }}
      >
        <Toolbar />
        <Scanner />
      </Box>
    </Box>
  );
};

export default DashboardPage;