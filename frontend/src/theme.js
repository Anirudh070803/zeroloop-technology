import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light', // Switch to light mode
    primary: {
      main: '#1976d2', // A standard blue for primary actions
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f4f6f8', // A light gray for the main background
      paper: '#ffffff',   // White for surfaces like sidebars and app bars
    },
    text: {
      primary: '#212121', // Dark gray for primary text
      secondary: '#757575',
    },
  },
});

export default theme;