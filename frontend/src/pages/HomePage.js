import React from 'react';
import { Box, Typography, Container, Grid, Paper } from '@mui/material';
import SpeedIcon from '@mui/icons-material/Speed';
import BugReportIcon from '@mui/icons-material/BugReport';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';

const features = [
  {
    icon: <SpeedIcon fontSize="large" color="primary" />,
    title: 'AI-Powered Static Analysis',
    description: 'Our engine uses advanced static analysis tools like Slither, enhanced with AI, to find common vulnerabilities in your smart contract code in minutes, not weeks.'
  },
  {
    icon: <BugReportIcon fontSize="large" color="primary" />,
    title: 'Advanced Dynamic Fuzzing',
    description: 'We go beyond static code reading by using dynamic analysis with tools like Echidna to stress-test your contract with thousands of transactions, finding complex, exploitable bugs.'
  },
  {
    icon: <VerifiedUserIcon fontSize="large" color="primary" />,
    title: 'Human-in-the-Loop Verification',
    description: 'AI is powerful, but human expertise is essential. Our network of freelance security experts verifies critical findings to eliminate false positives and provide actionable advice.'
  }
];

const HomePage = () => {
  return (
    <Container maxWidth="lg" sx={{ my: 4 }}>
      <Box sx={{ textAlign: 'center', my: 10 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          Welcome to ZeroLoop Technology
        </Typography>
        <Typography variant="h5" color="text.secondary">
          The future of Automated Blockchain Security.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {features.map((feature, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
              {feature.icon}
              <Typography variant="h6" component="h3" sx={{ mt: 2, mb: 1, fontWeight: 'bold' }}>
                {feature.title}
              </Typography>
              <Typography color="text.secondary">
                {feature.description}
              </Typography>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default HomePage;